#!/usr/bin/env python3
"""Stage 11 (reconciliation) generator on AWS Bedrock, one call per concept.

    python3 bedrock_reconcile.py <batch_dir> <chunk_id> [--only CONCEPT_ID ...] [--out-name NAME] [--dry-run]

Mechanical fields (context, coverage, teaching blocks, segment ids/urls/times, flags) are assembled by
this script from the gated artifacts. The model only writes: segment label/summary, group_title,
bridge_note, assessment_anchors, practice_anchor, visual_anchor. Writes
<batch_dir>/glossary_bundles_draft.part.<out-name or chunk>.json. Creds/model via .env (see glm_generate.py).
# ponytail: sequential, no concurrency; add a ThreadPool if a chunk takes too long.
"""
import argparse, json, os, re, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from glm_generate import BANK, CORE, ROOT, call_glm, load, load_env, make_client, parse, sha, used_label  # noqa: E402

STAGE = "11_reconciliation"
PRACTICE = "live_code|spreadsheet|field_selection|ordering|matching|tool_simulation|data_cleanup|UI_edit|formula|external_proof"
VISUAL = "diagram|data_table|spreadsheet|code|UI_state|process_flow|before_after|comparison|formula|chart|annotated_screenshot"
RULES = """Hard rules (each was an evaluator-caught defect in earlier chunks):
- The teaching text (given below, already written) must teach every required fact alone. Wherever a segment's fact_ids omit a required fact, the bridge note says what the clip lacks and that the text covers it.
- Every claim about a clip (in summary or bridge_note) must be TRUE of what is said in the transcript range given, and true of EVERY clip in the group; say "the first clip..., the second..." when they differ. Do not say a clip lacks something it actually says. Describe visuals only as the transcript supports.
- bridge_note.before and .after are each SHORT (about 15-40 words, never over 60). before = what to watch for + any term caveat (clip synonym, blocked tool, factual slip in the clip). after = the takeaway or the gap Devspace's text fills.
- summary: Devspace's voice, an accurate read-alternative of that range that makes sense alone; do not copy the transcript. label: what the learner is about to watch, in Devspace terms.
- Never name a blocked_knowledge concept in summary/bridge_note; use the teaching text's wording. Never mention "video/clip/watch" in anything except bridge_note, summary and label.
- assessment_anchors: from the TOC assessment_target; each cites only real fact ids or misconception ids; capability is snake_case. Never write question text.
- practice_anchor.type must be EXACTLY one of live_code|spreadsheet|field_selection|ordering|matching|tool_simulation|data_cleanup|UI_edit|formula|external_proof. Words like before_after, diagram, comparison, chart are VISUAL types for visual_anchor only, never a practice type.
- practice_anchor: from the TOC practice_objective; achievable with ALLOWED knowledge only. If the TOC objective needs something blocked, adapt it (and the teaching_notes already record the conflict). type live_code for coding concepts, with required_skill, allowed_syntax (only syntax taught by this concept and the allowed prior concepts), blocked_syntax (syntax of later concepts, no duplicates), starter_state_intent, observable_success. The objective/success/starter text must NOT rely on anything in blocked_syntax (e.g. do not require print() while it is blocked; do not block a literal kind the examples use). Starter data must use only columns/names of the concept's running example. Other types need no live_code object.
- visual_anchor: what must become visible, or null.
- media is null in your output exactly when the input says there are no segments."""


def concept_data(cid, ec, names, cb, pa, dc, sel, segj):
    c = ec[cid]
    segs = []
    for s in sel["segments"]:
        tr = load(BANK / "transcripts" / f"{s['video_id']}.json")["segments"]
        text = "\n".join(f"[{int(x['start_seconds'])}] {x['text']}" for x in tr if x["end_seconds"] > s["start_seconds"] and x["start_seconds"] < s["end_seconds"])
        j = segj.get((cid, s["video_id"]))
        segs.append({"segment_id": s["segment_id"], "video_id": s["video_id"], "start": s["start_seconds"], "end": s["end_seconds"],
                     "fact_ids_the_clip_teaches": s["fact_ids"], "current_label": s.get("label"), "judge_reasoning": j, "transcript_range": text})
    ev = cb["evidence"]
    data = {
        "concept_id": cid, "concept_name": c["concept_name"], "depth_tier": dc, "path_title": None,
        "assessment_target": c["assessment_target"], "practice_objective": c["practice_objective"],
        "required_facts": [{"id": f["id"], "statement": f["statement"]} for f in ev["required_facts"]],
        "misconceptions": ev.get("misconceptions", []),
        "optional_enrichment_facts": [{"id": f["id"], "statement": f["statement"]} for f in ev.get("optional_enrichment", [])],  # valid ids teaching blocks and segments may cite
        "allowed_prior_concepts": [f"{k} ({names.get(k, '?')})" for k in c["allowed_knowledge_ids"]],
        "blocked_later_concepts": [f"{k} ({names.get(k, '?')})" for k in c["blocked_knowledge_ids"]],
        "teaching_notes": pa["teaching_notes"], "video_need": pa["video_need"],
        "teaching_text_blocks": pa["teaching_blocks"],
        "segments": segs,
    }
    return data


def concept_prompt(cid, ec, names, cb, pa, dc, sel, segj, header):
    data = concept_data(cid, ec, names, cb, pa, dc, sel, segj)
    return f"""{header}

# Stage instructions (GENERATOR.md)
{(ROOT / '01_GLOSSARY_PACK_TEMPLATE' / STAGE / 'GENERATOR.md').read_text()}

{RULES}

# Concept input
{json.dumps(data, indent=1)}

# Output
Reply with ONE JSON object and nothing else:
{{"media": null | {{"group_title": str, "segments": [{{"segment_id": <exactly as given>, "label": str, "summary": str}}], "bridge_note": {{"before": str, "after": str}}}},
 "assessment_anchors": [{{"fact_ids": [..], "capability": snake_case}}],
 "practice_anchor": {{"type": one of {PRACTICE}, "objective": str, "success": str, "live_code": {{"required_skill","allowed_syntax":[..],"blocked_syntax":[..],"starter_state_intent","observable_success"}} (only when type is live_code)}},
 "visual_anchor": null | {{"type": one of {VISUAL}, "purpose": str}},
 "teaching_notes_extra": [optional strings: ONE note per TOC conflict you had to adapt the practice/assessment around (the TOC objective needs a blocked concept); omit if none, never repeat a note already in teaching_notes]}}"""


def load_inputs(B):
    ec = {c["concept_id"]: c for c in load(B / "extracted_concepts.json")["concepts"]}
    names = {k: v["concept_name"] for k, v in ec.items()}
    cbs = {b["concept_id"]: b for b in load(B / "coverage_briefs.json")["briefs"]}
    pas = {e["concept_id"]: e for e in load(B / "glossary_pass_a.json")["entries"]}
    dcs = load(B / "depth_classification.json")
    dcs = {x["concept_id"]: x["depth_tier"] for x in dcs.get("classifications", dcs.get("concepts", []))}
    sels = {s["concept_id"]: s for s in load(B / "selected_media.json")["selections"]}
    pmap = {p["proposal_id"]: (p["concept_id"], p["video_id"]) for p in load(B / "segment_proposals.json")["proposals"]}
    segj = {pmap[j["proposal_id"]]: j["reasoning"] for j in load(B / "segment_judgments.json")["judgments"] if j["verdict"] == "approved"}
    return ec, names, cbs, pas, dcs, sels, segj


def check(out, sel, fact_ids):
    errs = []
    segs = sel["segments"]
    m = out.get("media")
    if bool(segs) != bool(m):
        errs.append("media must be null exactly when there are no segments")
    if m:
        if sorted(s["segment_id"] for s in m["segments"]) != sorted(s["segment_id"] for s in segs):
            errs.append("media.segments must contain exactly one entry for each given segment_id (copy each id exactly, none missing, none extra)")
        for k in ("before", "after"):
            n = len(m["bridge_note"][k].split())
            if not 5 <= n <= 60:
                errs.append(f"bridge_note.{k} has {n} words (want about 15-40, max 60)")
        for s in m["segments"]:
            if not s.get("label") or len(s.get("summary", "").split()) < 10:
                errs.append(f"{s['segment_id']}: needs a label and a real summary")
    if not out.get("assessment_anchors"):
        errs.append("need at least one assessment anchor")
    for a in out.get("assessment_anchors", []):
        bad = [f for f in a["fact_ids"] if f not in fact_ids]
        if bad or not re.fullmatch(r"[a-z][a-z0-9_]*", a["capability"]):
            errs.append(f"assessment anchor {a}: unknown fact ids {bad} or non-snake_case capability")
    p = out["practice_anchor"]
    if p["type"] not in PRACTICE.split("|"):
        errs.append(f"practice type {p['type']} invalid")
    lc = p.get("live_code")
    if (p["type"] == "live_code") != bool(lc):
        errs.append("live_code object must be present exactly when type is live_code")
    if lc:
        for k in ("allowed_syntax", "blocked_syntax"):
            if len(set(lc[k])) != len(lc[k]):
                errs.append(f"duplicate entries in {k}")
        text = " ".join([p["objective"], p["success"], lc["starter_state_intent"], lc["observable_success"], lc["required_skill"]]).lower()
        for b in lc["blocked_syntax"]:  # a blocked call like print() must not be needed by the task text
            w = re.match(r"([a-z_]+)\(\)", b.strip())
            if w and re.search(rf"\b{w.group(1)}\b", text):
                errs.append(f"practice text mentions {w.group(1)}() but it is in blocked_syntax")
    v = out.get("visual_anchor")
    if v and v["type"] not in VISUAL.split("|"):
        errs.append(f"visual_anchor type {v['type']} invalid")
    return errs


def assemble(cid, ec, cb, pa, dc, sel, out):
    c = ec[cid]
    media = None
    if out["media"]:
        by = {s["segment_id"]: s for s in out["media"]["segments"]}
        media = {"group_title": out["media"]["group_title"],
                 "segments": [{"segment_id": s["segment_id"], "label": by[s["segment_id"]]["label"], "video_id": s["video_id"],
                               "youtube_url": s["youtube_url"], "review_url": s["review_url"], "start_seconds": s["start_seconds"],
                               "end_seconds": s["end_seconds"], "summary": by[s["segment_id"]]["summary"], "fact_ids": s["fact_ids"],
                               "transcript_ref": s["transcript_ref"]} for s in sel["segments"]],
                 "bridge_note": out["media"]["bridge_note"]}
    loc = c["toc_location"]
    ev = cb["evidence"]
    return {"context": {"concept_id": cid, "concept_name": c["concept_name"], "path_id": c["path_id"], "depth_tier": dc,
                        "toc_location": {k: loc[k] for k in ("region_id", "terrain_id", "tile_id")},
                        "prerequisites": c["direct_prerequisite_ids"], "blocked_future_concepts": c["blocked_knowledge_ids"]},
            "coverage": {"learning_objective": cb["learning_objective"], "required_facts": ev["required_facts"], "misconceptions": ev.get("misconceptions", [])},
            "teaching_blocks": pa["teaching_blocks"], "video_need": pa["video_need"], "media": media,
            "assessment_anchors": out["assessment_anchors"], "practice_anchor": out["practice_anchor"],
            "visual_anchor": out.get("visual_anchor"), "teaching_notes": pa["teaching_notes"] + [n for n in out.get("teaching_notes_extra", []) if n not in pa["teaching_notes"]], "cluster_ref": None,
            "validation": {"source_supported": True, "prerequisite_safe": True, "media_aligned": True, "ready_for_final_schema": True}}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("batch_dir"); ap.add_argument("chunk"); ap.add_argument("--only", nargs="*"); ap.add_argument("--out-name"); ap.add_argument("--dry-run", action="store_true"); ap.add_argument("--fresh", action="store_true")
    a = ap.parse_args()
    sys.stdout.reconfigure(line_buffering=True)
    load_env()
    B = Path(a.batch_dir); B = B if B.is_absolute() else ROOT / B
    batch_id = B.name
    ids = a.only or load(B / "chunks.json")["chunks"][a.chunk]["concept_ids"]
    ec, names, cbs, pas, dcs, sels, segj = load_inputs(B)
    header = f"Pack root: {ROOT}. You are the generator for stage {STAGE}. You cannot read files; everything you need is below."

    client = model = None
    if not a.dry_run:
        model = os.environ.get("GLM_MODEL_ID") or "GEN"  # pinned id, or the GEN ladder
        client = make_client()

    dest = B / f"glossary_bundles_draft.part.{a.out_name or a.chunk}.json"
    bundles, failed = [], []
    if dest.exists() and not a.fresh:  # resume: keep finished concepts, redo only the rest
        bundles = [b for b in load(dest)["bundles"] if b["context"]["concept_id"] in ids]
    done = {b["context"]["concept_id"] for b in bundles}
    for cid in ids:
        if cid in done:
            continue
        sel = sels[cid]
        fact_ids = {f["id"] for f in cbs[cid]["evidence"]["required_facts"]} | {m["id"] for m in cbs[cid]["evidence"].get("misconceptions", [])}
        prompt = concept_prompt(cid, ec, names, cbs[cid], pas[cid], dcs[cid], sel, segj, header)
        if a.dry_run:
            print(prompt[-9000:], f"\n[{len(prompt)} chars]"); return
        out, errs = None, []
        for _ in range(3):
            try:
                text = call_glm(client, model, prompt if not errs else prompt + "\n\nYour previous answer failed these checks; fix them and resend the full JSON:\n- " + "\n- ".join(errs), 16000)
            except Exception as e:  # API error after SDK retries: leave this concept for a resume run
                out, errs = None, [f"api error: {str(e)[:120]}"]; break
            try:
                out = parse(text); errs = check(out, sel, fact_ids)
            except (ValueError, KeyError, TypeError) as e:
                out, errs = None, [f"unparseable or missing field: {e}"]
            if not errs:
                break
        if errs or not out:
            failed.append(cid); print(f"{cid}: FAILED after retries: {errs}", file=sys.stderr); continue
        bundles.append(assemble(cid, ec, cbs[cid], pas[cid], dcs[cid], sel, out)); print(f"{cid}: ok ({len(sel['segments'])} segments)")

    parents = {f: sha(B / f) for f in ("glossary_pass_a.json", "selected_media.json", "coverage_briefs.json", "depth_classification.json", "extracted_concepts.json")}
    doc = {"metadata": {"artifact_type": "glossary_bundles_draft", "artifact_version": "1.0.0", "schema_version": "1.0.0", "batch_id": batch_id, "run_id": batch_id,
                        "prompt_version": f"{STAGE}@v1", "model": f"bedrock:{used_label()}", "generated_at": datetime.now(timezone.utc).isoformat(),
                        "source_snapshot_id": "data_analytics.source_pack", "parent_artifact_hashes": parents},
           "batch_id": batch_id, "bundles": bundles}
    dest.write_text(json.dumps(doc, indent=2))
    order = {c: i for i, c in enumerate(ids)}
    doc["bundles"].sort(key=lambda b: order[b["context"]["concept_id"]])
    dest.write_text(json.dumps(doc, indent=2))
    subprocess.run([sys.executable, str(CORE / "scripts" / "schema_check.py"), "glossary_bundles_draft.schema.json", str(dest)], check=True)
    print(f"wrote {dest}: {len(bundles)}/{len(ids)} bundles; failed (rerun to resume): {failed}")


if __name__ == "__main__":
    main()
