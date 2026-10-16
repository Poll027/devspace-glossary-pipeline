#!/usr/bin/env python3
"""Run generator stage 08 (segment detection) on GLM via AWS Bedrock, one call per video.

    python3 glm_generate.py <batch_dir> <chunk_id> [--only VIDEO_ID ...] [--dry-run]

Writes <batch_dir>/segment_proposals.part.<chunk_id>.json, same shape the Sonnet subagent wrote.
Credentials: default AWS chain only (env / ~/.aws / SSO). Model id: env GLM_MODEL_ID (Bedrock model
or inference-profile id as shown in the console). Region: env AWS_REGION / AWS_DEFAULT_REGION.
--dry-run builds and prints the first prompt without calling AWS (no boto3 needed).
# ponytail: stage 08 only; stages 11/12 need their own prompt builder, add when they move to GLM.
"""
import argparse, hashlib, json, os, re, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CORE = ROOT / "00_GLOSSARY_PIPELINE_CORE"
BANK = CORE / "video_bank"
STAGE = "08_segment_detection"
norm = lambda s: re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def load_env():
    """Read the gitignored .env (KEY=value lines); real env vars win."""
    if (ROOT / ".env").exists():
        for ln in (ROOT / ".env").read_text().splitlines():
            if "=" in ln and not ln.lstrip().startswith("#"):
                k, v = ln.split("=", 1); os.environ.setdefault(k.strip(), v.strip().strip("'\""))


def load(p):
    return json.loads(Path(p).read_text())


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def playbook_excerpt():
    lines = (CORE / "PLAYBOOK_v3.md").read_text().splitlines()
    return "\n".join(lines[1072:1175] + lines[1714:1752])  # §14-16 and §28.3


def video_prompt(batch, vid, pairs, C, briefs, pa, names, header):
    cat = load(BANK / "catalogue" / f"{vid}.json")
    tr = BANK / "transcripts" / f"{vid}.json"
    transcript = ""
    if tr.exists():
        transcript = "\n".join(f"[{int(s['start_seconds'])}] {s['text']}" for s in load(tr)["segments"])
    concepts = []
    for cid in pairs:
        c = C[cid]
        concepts.append({
            "concept_id": cid, "concept_name": c["concept_name"], "path_id": c["path_id"],
            "video_need": pa[cid]["video_need"], "teaching_notes": pa[cid]["teaching_notes"],
            "required_facts": [{"id": f["id"], "statement": f["statement"]} for f in briefs[cid]["evidence"]["required_facts"]],
            "blocked_knowledge": [f"{b} ({names.get(b, '?')})" for b in c["blocked_knowledge_ids"]],
            "allowed_knowledge": c["allowed_knowledge_ids"],
        })
    return f"""{header}

# Stage instructions (GENERATOR.md)
{(ROOT / '01_GLOSSARY_PACK_TEMPLATE' / STAGE / 'GENERATOR.md').read_text()}

# Playbook excerpt (§14-16, §28.3)
{playbook_excerpt()}

# Your single video: {vid}
Catalogue entry: {json.dumps({k: cat.get(k) for k in ('title', 'duration_seconds', 'playable_in_embed', 'transcript_available', 'chapters')})}

Concepts this video is a kept candidate for:
{json.dumps(concepts, indent=1)}

Transcript (one line per caption, `[start_seconds] text`; auto-captions overlap slightly):
{transcript or '(NO TRANSCRIPT)'}

# Output
Reply with ONE JSON object and nothing else:
{{"proposals": [{{proposal_id, concept_id, path_id, video_id, start_seconds, end_seconds, label, role, covered_fact_ids, visual_mode, chapter_aligned, transcript_evidence, issues}}],
 "rejected_videos": [{{video_id, concept_id, reason}}]}}
Every concept above must appear in exactly one of the two lists. start/end are integers taken from real transcript timestamps.
role is one of mental_model|visual_mechanism|worked_example|live_code_demo|tool_workflow. visual_mode must be a value from the Final Schema visual_mode enum (e.g. annotated_code, data_table_demo, annotated_ui, talking_head_only).
transcript_evidence must be copied verbatim from a caption line INSIDE [start_seconds, end_seconds]."""


def make_client():
    import boto3
    from botocore.config import Config  # adaptive retry/backoff: parallel runs get throttled otherwise
    return boto3.client("bedrock-runtime", config=Config(retries={"max_attempts": 12, "mode": "adaptive"}, read_timeout=600))


def price_usd(model, usage):
    """USD for one call. Per-million-token (in, out): Opus-class 5/25, else 3/15. Override env PRICE_EVAL / PRICE_GEN = in,out."""
    role = "EVAL" if "opus" in model.lower() else "GEN"
    pin, pout = (5.0, 25.0) if role == "EVAL" else (3.0, 15.0)
    if os.environ.get(f"PRICE_{role}"):
        pin, pout = (float(x) for x in os.environ[f"PRICE_{role}"].split(","))
    return usage.get("inputTokens", 0) / 1e6 * pin + usage.get("outputTokens", 0) / 1e6 * pout


def log_usage(model, usage, label=""):
    """Append the call's estimated cost to $COST_LOG (set by the driver) so every script's spend is counted."""
    p = os.environ.get("COST_LOG")
    if p:
        with open(p, "a") as f:
            f.write(json.dumps({"t": datetime.now(timezone.utc).isoformat(timespec="seconds"), "model": model, "label": label or Path(sys.argv[0]).name,
                                "in": usage.get("inputTokens", 0), "out": usage.get("outputTokens", 0), "usd": round(price_usd(model, usage), 4)}) + "\n")


def call_glm(client, model, prompt, max_tokens=32000):  # reasoning is always on and counts against this
    r = client.converse(modelId=model, messages=[{"role": "user", "content": [{"text": prompt}]}],
                        inferenceConfig={"maxTokens": max_tokens, "temperature": 0.2})
    log_usage(model, r["usage"])
    return "".join(b.get("text", "") for b in r["output"]["message"]["content"])


def parse(text):
    """First JSON object in the reply (tolerates prose/fences before it and extra text after)."""
    return json.JSONDecoder().raw_decode(text[text.index("{"):])[0]


def mechanical_check(vid, pairs, out):
    """Free deterministic checks (cost-control rule 1) before anything reaches the judge."""
    errs, segs = [], load(BANK / "transcripts" / f"{vid}.json")["segments"] if (BANK / "transcripts" / f"{vid}.json").exists() else []
    seen = [p["concept_id"] for p in out.get("proposals", [])] + [r["concept_id"] for r in out.get("rejected_videos", [])]
    for cid in pairs:
        if seen.count(cid) != 1:
            errs.append(f"concept {cid} must appear exactly once across proposals/rejected_videos (found {seen.count(cid)})")
    for p in out.get("proposals", []):
        if p["video_id"] != vid or p["concept_id"] not in pairs:
            errs.append(f"{p.get('proposal_id')}: wrong video_id/concept_id")
        if not p["start_seconds"] < p["end_seconds"]:
            errs.append(f"{p['proposal_id']}: start >= end")
        inside = " ".join(s["text"] for s in segs if s["end_seconds"] > p["start_seconds"] and s["start_seconds"] < p["end_seconds"])
        if not all(norm(q) in norm(inside) for q in re.split(r"\.{3}|…", p["transcript_evidence"]) if norm(q)):  # "a ... b" stitched quotes allowed
            errs.append(f"{p['proposal_id']}: transcript_evidence not found verbatim inside the range")
    return errs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("batch_dir"); ap.add_argument("chunk"); ap.add_argument("--only", nargs="*"); ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    sys.stdout.reconfigure(line_buffering=True)  # live progress when redirected to a log
    B = Path(a.batch_dir)
    B = B if B.is_absolute() else ROOT / B
    batch_id = B.name
    vids = a.only or load(B / "chunks_08.json")["chunks"][a.chunk]["video_ids"]

    cands = {}  # video -> [concept_id] for kept candidates
    for s in load(B / "video_candidates.json")["searches"]:
        for c in s["candidates"]:
            if c["filter_verdict"] == "kept":
                cands.setdefault(c["video_id"], []).append(s["concept_id"])
    ec = load(B / "extracted_concepts.json")
    C = {c["concept_id"]: c for c in ec["concepts"]}
    names = {k: v["concept_name"] for k, v in C.items()}
    briefs = {b["concept_id"]: b for b in load(B / "coverage_briefs.json")["briefs"]}
    pa = {e["concept_id"]: e for e in load(B / "glossary_pass_a.json")["entries"]}
    header = f"Pack root: {ROOT}. You are the generator for stage {STAGE}. You cannot read files; everything you need is below."

    load_env()
    client = model = None
    if not a.dry_run:
        model = os.environ.get("GLM_MODEL_ID") or sys.exit("set GLM_MODEL_ID to the GLM Bedrock model/inference-profile id")
        client = make_client()  # default credential chain only

    proposals, rejected = [], []
    for vid in vids:
        pairs = list(dict.fromkeys(cands.get(vid, [])))
        if not pairs:
            print(f"{vid}: no kept candidate concepts, skipping"); continue
        prompt = video_prompt(B, vid, pairs, C, briefs, pa, names, header)
        if a.dry_run:
            print(prompt[:3000], f"\n... [{len(prompt)} chars total, {len(pairs)} concepts]"); return
        out, errs = None, []
        for attempt in range(3):
            text = call_glm(client, model, prompt if not errs else prompt + "\n\nYour previous answer failed these checks, fix them and resend the full JSON:\n- " + "\n- ".join(errs))
            try:
                out = parse(text); errs = mechanical_check(vid, pairs, out)
            except (ValueError, KeyError, TypeError) as e:
                errs = [f"unparseable or missing field: {e}"]
            if not errs:
                break
        if errs and not out:
            print(f"{vid}: unparseable after retries, left out: {errs}", file=sys.stderr); continue
        for p in out["proposals"]:  # deterministic unique ids; the model's own are inconsistent
            if any(p["proposal_id"] + ":" in e for e in errs):
                p["issues"].append("script check: transcript_evidence not matched verbatim inside range; judge verify")
            p["proposal_id"] = f"prop_{vid}_{p['concept_id'].split('.')[-1]}"
        if errs:
            print(f"{vid}: kept with flagged proposals: {errs}", file=sys.stderr)
        proposals += out["proposals"]; rejected += out["rejected_videos"]
        print(f"{vid}: {len(out['proposals'])} proposals, {len(out['rejected_videos'])} rejected")

    parents = {f: sha(B / f) for f in ("video_candidates.json", "coverage_briefs.json", "extracted_concepts.json")}
    doc = {"metadata": {"artifact_type": "segment_proposals", "artifact_version": "1.0.0", "schema_version": "1.0.0",
                        "batch_id": batch_id, "run_id": batch_id, "prompt_version": f"{STAGE}@v1", "model": f"glm-bedrock:{model}",
                        "generated_at": datetime.now(timezone.utc).isoformat(), "source_snapshot_id": "data_analytics.source_pack",
                        "parent_artifact_hashes": parents},
           "batch_id": batch_id, "proposals": proposals, "rejected_videos": rejected}
    dest = B / f"segment_proposals.part.{a.chunk}.json"
    dest.write_text(json.dumps(doc, indent=2))
    subprocess.run([sys.executable, str(CORE / "scripts" / "schema_check.py"), "segment_proposals.schema.json", str(dest)], check=True)
    print(f"wrote {dest}: {len(proposals)} proposals, {len(rejected)} rejected")


if __name__ == "__main__":
    main()
