#!/usr/bin/env python3
"""Stage 11 (reconciliation) EVALUATOR on AWS Bedrock, one fresh call per concept.

    python3 bedrock_evaluate.py <batch_dir> <chunk_id> [--only CONCEPT_ID ...]

Reads glossary_bundles_draft.part.<chunk>.json (run bedrock_reconcile.py / the schema check first) and
writes working/eval_11_<chunk>.json: {"verdict": PASS|FAIL, "defects": [{concept_id, severity, field,
problem, fix}]}. FAIL iff any BLOCKING defect. Model: env EVAL_MODEL_ID (default Opus 4.6 profile).
Each call sees only the sources + the bundle, never the generator's reasoning.
# ponytail: stage 11 only; other evaluator stages keep their EVALUATOR.md and need their own prompt.
"""
import argparse, hashlib, json, os, sys, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from bedrock_reconcile import ROOT, STAGE, concept_data, load_inputs  # noqa: E402
from glm_generate import LAST, USED, call_glm, load, load_env, make_client, parse, used_label  # noqa: E402

PROMPT_VERSION = "v2-optional-facts-and-scope"  # bump when the evaluation prompt changes

CHECKLIST = """Severity (from the pipeline's evaluator definition):
- BLOCKING: a claim its source doesn't support or contradicts; a missing required fact or uncovered item; later-taught knowledge the learner must UNDERSTAND to follow the content; a structural break (wrong ids, altered copied fields). A needed new claim is BLOCKING, not ADVISORY.
- ADVISORY: everything else (wording, repetition, example choice, style). A passing mention of a later idea the learner can follow without is at most advisory.

Calibration rules: (a) ANY bridge_note/summary/label claim that the transcript range contradicts or overstates (patterns 1 below) is BLOCKING, because a learner is told something false about the clip; (b) a practice_anchor that relies on blocked syntax or cannot be done with allowed knowledge is BLOCKING; (c) the words watch/clip/video are NORMAL in bridge_note, summary and label (that is where they belong), so never flag them there, only inside teaching blocks; (d) never list a defect you retract: if you decide it is not a defect, leave it out.

(e) Fact ids: the Sources list "required_facts" AND "optional_enrichment_facts". Teaching blocks and segments may legitimately cite an optional-enrichment id (e.g. f6); that is NOT a defect. (f) The teaching blocks are already-gated Pass A text and are OUT OF SCOPE: report nothing about them, except a required fact id that no block covers.

Defect patterns earlier chunks actually had; look for each of these on THIS concept:
1. A bridge_note or summary claim about a clip that its transcript range contradicts (e.g. "only a spoken mention" when the clip shows and runs it; "fixes it" when the first attempt still errors; "both clips do X" when only one does; "never shows the earlier query" when it is on screen; "a table" when the clip shows slides). Verify every specific claim, positive or negative, against the transcript range given, for EVERY clip in the group.
2. A clip caveat missed: a clip uses a synonym for a Devspace term, states something factually wrong, or relies on a later/blocked tool, and the bridge note says nothing.
3. practice_anchor internally inconsistent: success/objective/starter relies on syntax listed in blocked_syntax (e.g. requires print() while blocked), or blocks a literal kind the examples use; allowed_syntax includes something taught LATER; duplicate list entries; starter data uses columns/names that are not in the concept's running example or shared schema; the practice cannot be done with allowed knowledge only.
4. assessment_anchors cite wrong/unknown fact ids, or don't reflect the TOC assessment_target; a TOC conflict (objective needs a blocked concept) is not recorded in teaching_notes, or is recorded twice.
5. bridge_note long-winded (>60 words per half) or generic ("watch the video").
6. A blocked concept named in summary/bridge_note/label, or the words video/clip/watch inside the teaching blocks (those must stand alone).
7. A required fact the clips don't cover and the bridge does not say the text carries it; any teaching block that is missing a required fact id.
8. visual_anchor describing how something looks instead of what must become visible, or inconsistent with the video_need."""


def evaluate_prompt(cid, data, bundle):
    shown = {k: bundle[k] for k in ("media", "assessment_anchors", "practice_anchor", "visual_anchor", "teaching_notes")}
    return f"""You are an independent evaluator for one concept of stage {STAGE} of the Devspace glossary pipeline. You never saw the generator's reasoning. Re-derive from the sources below; do not trust the bundle's own claims.

# Evaluator instructions
{(ROOT / '01_GLOSSARY_PACK_TEMPLATE' / STAGE / 'EVALUATOR.md').read_text()}

{CHECKLIST}

Segment fields (ids, urls, times, fact_ids) and the copied context/coverage/teaching blocks were already verified byte-exact by script. Judge the AUTHORED parts only: media (group_title, labels, summaries, bridge_note), assessment_anchors, practice_anchor, visual_anchor, teaching_notes. The teaching text is below for coverage checks.

# Sources for {cid}
{json.dumps(data, indent=1)}

# Bundle under evaluation (authored parts)
{json.dumps(shown, indent=1)}

# Output
First enumerate the checks, then the defects. Reply with ONE JSON object and nothing else:
{{"claims_checked": [{{"where": "e.g. media.bridge_note.after or segment <id> summary or practice_anchor.success", "claim": "one specific claim the bundle makes about a clip/the syntax/the example", "evidence": "the transcript line (with [timestamp]) or fact/syntax entry that settles it", "supported": true|false}}],
 "defects": [{{"severity": "BLOCKING"|"ADVISORY", "field": "e.g. media.bridge_note.after", "problem": "what is wrong, citing the transcript timestamp or fact id", "fix": "pinned replacement wording or the exact change"}}]}}
An empty list means you found nothing. claims_checked must include EVERY specific factual claim in the bridge notes and summaries (positive and negative: "only a spoken mention", "never shows", "both clips", "fixes it"), each with the quoted evidence from the transcript range, plus the practice_anchor consistency check (does success/objective/starter rely on anything in blocked_syntax?). Every claim with supported=false must appear in defects. Be specific enough that the fix can be applied without re-deriving your reasoning; do not invent defects to look thorough."""


def ask(client, model, prompt, tries=4):
    """One evaluation call, retried with backoff on throttling/API errors and unparseable replies (a fresh sample usually parses)."""
    for i in range(tries):
        try:
            return parse(call_glm(client, model, prompt, 16000))
        except Exception as ex:
            if i == tries - 1 or "per day" in str(ex):  # a daily token quota does not recover by retrying
                raise
            time.sleep(15 * (i + 1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("batch_dir"); ap.add_argument("chunk"); ap.add_argument("--only", nargs="*"); ap.add_argument("--part", help="part file suffix if different from chunk"); ap.add_argument("--passes", type=int, default=2, help="independent evaluations per concept; defects are unioned")
    a = ap.parse_args()
    sys.stdout.reconfigure(line_buffering=True)
    load_env()
    B = Path(a.batch_dir); B = B if B.is_absolute() else ROOT / B
    model = os.environ.get("EVAL_MODEL_ID") or "EVAL"  # pinned id, or the EVAL ladder
    client = make_client()
    ec, names, cbs, pas, dcs, sels, segj = load_inputs(B)
    bundles = {b["context"]["concept_id"]: b for b in load(B / f"glossary_bundles_draft.part.{a.part or a.chunk}.json")["bundles"]}
    defects, errors, details = [], [], {}
    cache_path = B / "working" / f"eval_cache_11_{a.part or a.chunk}.json"  # concept -> {bundle hash, defects}: a rerun pays only for concepts that changed or errored
    cache = json.loads(cache_path.read_text()) if cache_path.exists() else {}
    for cid, b in bundles.items():
        if a.only and cid not in a.only:
            continue
        h = hashlib.sha256((PROMPT_VERSION + json.dumps(b, sort_keys=True)).encode()).hexdigest()  # a prompt change invalidates cached verdicts
        if cache.get(cid, {}).get("hash") == h:
            defects += cache[cid]["defects"]; print(f"{cid}: cached"); continue
        t0 = time.time()
        prompt = evaluate_prompt(cid, concept_data(cid, ec, names, cbs[cid], pas[cid], dcs[cid], sels[cid], segj), b)
        found, models = {}, set()  # independent passes, union of defects keyed by (field, kind), highest severity wins
        try:
            for _ in range(a.passes):
                out = ask(client, model, prompt); models.add(LAST["model"])
                for d in out["defects"]:
                    if d.get("severity") in ("BLOCKING", "ADVISORY"):
                        k = (d["field"], d["problem"][:40])
                        if k not in found or d["severity"] == "BLOCKING":
                            found[k] = {"concept_id": cid, **d}
            ds = list(found.values())
        except Exception as e:  # unparseable or API error: report it, never count as a pass
            errors.append(cid); details[cid] = f"{type(e).__name__}: {str(e)[:300]}"; print(f"{cid}: EVAL ERROR {details[cid]}", file=sys.stderr); continue
        defects += ds
        cache[cid] = {"hash": h, "defects": ds, "models": sorted(models)}  # which model(s) judged it, so a weaker-model result can be re-checked later
        cache_path.write_text(json.dumps(cache))
        print(f"{cid}: {sum(d['severity'] == 'BLOCKING' for d in ds)}B {sum(d['severity'] == 'ADVISORY' for d in ds)}A ({time.time() - t0:.0f}s)")
    verdict = "FAIL" if any(d["severity"] == "BLOCKING" for d in defects) else ("INCOMPLETE" if errors else "PASS")
    rep = {"chunk": a.chunk, "evaluator_model": used_label(), "verdict": verdict, "not_evaluated_due_to_errors": errors, "error_details": details, "defects": defects}
    dest = B / "working" / f"eval_11_{a.part or a.chunk}.json"
    dest.write_text(json.dumps(rep, indent=2))
    print(f"VERDICT: {verdict}; {sum(d['severity'] == 'BLOCKING' for d in defects)} blocking, {sum(d['severity'] == 'ADVISORY' for d in defects)} advisory, {len(errors)} errors -> {dest}")


if __name__ == "__main__":
    main()
