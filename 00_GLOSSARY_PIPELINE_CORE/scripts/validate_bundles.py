"""15_final_validation, mechanical half: check every path bundle and write glossary_validation_report.json.

The judgment half (does the text read well, do text and video complement each other) is
15_final_validation/CLAUDE_CROSS_ARTIFACT_REVIEW.md, which amends this report.

Usage: python3 validate_bundles.py <batch_dir>
"""
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

from schema_check import validate

VIDEO_REFERENCE = re.compile(r"\b(the|this|that|above|below) (video|clip)\b|\bas (shown|seen|explained) in\b", re.I)
LONG_CLIP_SECONDS = 360  # playbook §15: longest typical band is 6 minutes; longer needs a stated reason


def load(p):
    return json.loads(Path(p).read_text())


def check_bundle(b, extracted_row, errors, warnings):
    ctx = b["context"]
    key = f"{ctx['concept_id']}@{ctx['path_id']}"
    required = {f["id"] for f in b["coverage"]["required_facts"]}
    taught = {fid for tb in b["teaching_blocks"] for fid in tb["fact_ids"]}
    if required - taught:
        errors.append(f"{key}: required facts not taught by any teaching block: {sorted(required - taught)}")
    for tb in b["teaching_blocks"]:
        if VIDEO_REFERENCE.search(tb["content"]):
            errors.append(f"{key}: {tb['id']} refers to the video — text must stand alone")
        if set(tb["fact_ids"]) - required:
            errors.append(f"{key}: {tb['id']} cites unknown facts {sorted(set(tb['fact_ids']) - required)}")
    for a in b["assessment_anchors"]:
        if set(a["fact_ids"]) - required:
            errors.append(f"{key}: assessment anchor '{a['capability']}' cites unknown facts")
    if set(ctx["prerequisites"]) != set(extracted_row["direct_prerequisite_ids"]):
        errors.append(f"{key}: context.prerequisites differ from the frozen TOC")

    if b["media"] is None:
        return
    segs = b["media"]["segments"]
    for i, s in enumerate(segs):
        where = f"{key} segment[{i}] {s['segment_id']}"
        if s["segment_id"] != f"seg_{ctx['concept_id']}_{s['video_id']}_{s['start_seconds']}_{s['end_seconds']}":
            errors.append(f"{where}: segment_id does not match concept + video + cut")
        if s["youtube_url"] != f"https://www.youtube.com/watch?v={s['video_id']}":
            errors.append(f"{where}: youtube_url does not derive from video_id")
        if s["review_url"] != f"https://www.youtube.com/watch?v={s['video_id']}&t={s['start_seconds']}s":
            errors.append(f"{where}: review_url does not derive from video_id + start_seconds")
        if s["end_seconds"] <= s["start_seconds"]:
            errors.append(f"{where}: end_seconds <= start_seconds")
        if set(s["fact_ids"]) - required:
            errors.append(f"{where}: cites facts that aren't required facts of this concept")
        if s["transcript_ref"] != f"{s['video_id']}:{s['start_seconds']}-{s['end_seconds']}":
            errors.append(f"{where}: transcript_ref does not match the approved cut")
        if s["end_seconds"] - s["start_seconds"] > LONG_CLIP_SECONDS:
            warnings.append(f"{where}: clip longer than {LONG_CLIP_SECONDS}s — confirm the reason")
        for t in segs[i + 1:]:
            if s["video_id"] == t["video_id"] and s["start_seconds"] < t["end_seconds"] and t["start_seconds"] < s["end_seconds"]:
                errors.append(f"{where}: overlaps {t['segment_id']} in the same media group")


def run(batch_dir):
    d = Path(batch_dir)
    ctx = load(d / "batch_run_context.json")
    extracted = load(d / "extracted_concepts.json")
    rows = {(c["path_id"], c["concept_id"]): c for c in extracted["concepts"]}
    errors, warnings = [], []
    checks = {}

    bundles_ok, seen = True, set()
    for p in ctx["paths"]:
        f = d / f"path_glossary_bundle.{p['path_id']}.json"
        if not f.exists():
            errors.append(f"missing {f.name}")
            bundles_ok = False
            continue
        bundle = load(f)
        try:
            validate(bundle, "path_glossary_bundle.schema.json")
        except Exception as e:  # jsonschema.ValidationError; message is what the report needs
            errors.append(f"{f.name}: schema: {str(e).splitlines()[0]}")
            bundles_ok = False
            continue
        for b in bundle["bundles"]:
            key = (b["context"]["path_id"], b["context"]["concept_id"])
            seen.add(key)
            check_bundle(b, rows[key], errors, warnings)
        tiles = {c["concept_id"]: c["toc_location"]["tile_id"] for c in extracted["concepts"] if c["path_id"] == p["path_id"]}
        for cl in bundle["clusters"]:
            if {tiles[c] for c in cl["concept_ids"]} != {cl["tile_id"]}:
                errors.append(f"cluster {cl['cluster_id']}: crosses tiles")
    checks["every_path_has_schema_valid_bundle"] = bundles_ok
    missing = set(rows) - seen
    checks["every_toc_concept_has_a_bundle"] = not missing
    if missing:
        errors.append(f"{len(missing)} TOC concepts have no bundle, e.g. {sorted(missing)[:3]}")
    checks["leakage_blocking_count_zero"] = load(d / "leakage_audit_report.json")["blocking_issue_count"] == 0
    checks["bundle_content_checks_pass"] = not errors

    report = {
        "metadata": {
            "artifact_type": "glossary_validation_report", "artifact_version": "1.0.0", "schema_version": "1.0.0",
            "batch_id": ctx["batch_id"], "run_id": ctx["batch_id"], "prompt_version": "n/a-deterministic",
            "model": "deterministic/validate_bundles.py", "generated_at": datetime.now(timezone.utc).isoformat(),
            "source_snapshot_id": ctx["batch_id"],
            "parent_artifact_hashes": {f.name: hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(d.glob("path_glossary_bundle.*.json"))},
        },
        "batch_id": ctx["batch_id"],
        "validation_status": "PASS" if all(checks.values()) and not errors else "FAIL",
        "checks": checks, "warnings": warnings, "blocking_errors": errors,
    }
    validate(report, "glossary_validation_report.schema.json")
    (d / "glossary_validation_report.json").write_text(json.dumps(report, indent=2))
    return report


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    r = run(sys.argv[1])
    print(r["validation_status"], f"— {len(r['blocking_errors'])} errors, {len(r['warnings'])} warnings")
    for e in r["blocking_errors"][:20]:
        print("  ERROR", e)
