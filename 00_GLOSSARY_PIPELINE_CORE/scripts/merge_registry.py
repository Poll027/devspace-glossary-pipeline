"""16b_registry_merge: fold an audited batch into the cross-batch stores. Deterministic.

Refuses to run unless the independent audit passed and every stage gate is PASS and not stale.
Writes: registry/concept_evidence_registry.json, video_bank/approved_segments.json,
        video_bank/catalogue/<video_id>.json judged_ranges.

Usage: python3 merge_registry.py <batch_dir> <core_dir>
"""
import json
import sys
from pathlib import Path

from schema_check import validate
from update_ledger import verify


def load(p, default=None):
    p = Path(p)
    if not p.exists() and default is not None:
        return default
    return json.loads(p.read_text())


def save(p, obj):
    Path(p).write_text(json.dumps(obj, indent=2))


def main(batch_dir, core_dir):
    d, core = Path(batch_dir), Path(core_dir)
    audit = load(d / "glossary_independent_audit_report.json")
    if audit["verdict"] not in ("PASS", "PASS_WITH_NONBLOCKING_CHANGES"):
        sys.exit(f"refusing to merge: audit verdict {audit['verdict']}")
    manifest = load(core / "pipeline_manifest.json")
    gated = [s["id"] for s in manifest["stages"] if s.get("gated", True)]
    problems = verify(d, gated)
    if problems:
        sys.exit("refusing to merge, ledger problems:\n" + "\n".join(problems))

    batch_id = audit["batch_id"]
    reg_path = core / "registry" / "concept_evidence_registry.json"
    registry = load(reg_path, {"entries": []})
    entries = {e["concept_id"]: e for e in registry["entries"]}
    for b in load(d / "coverage_briefs.json")["briefs"]:
        ev = entries.get(b["concept_id"])
        if ev is None and b["canonical_status"] == "new":
            ev = {**b["evidence"], "created_in_batch_id": batch_id, "used_by_path_ids": []}
            validate(ev, "concept_evidence.schema.json")
            entries[b["concept_id"]] = ev
        if ev is not None and b["path_id"] not in ev["used_by_path_ids"]:
            ev["used_by_path_ids"].append(b["path_id"])
    registry["entries"] = list(entries.values())
    save(reg_path, registry)

    selected = {s["segment_id"]: s for sel in load(d / "selected_media.json")["selections"] for s in sel["segments"]}
    seg_path = core / "video_bank" / "approved_segments.json"
    bank = load(seg_path, {"segments": []})
    segs = {s["segment_id"]: s for s in bank["segments"]}
    for f in sorted(d.glob("path_glossary_bundle.*.json")):
        for b in load(f)["bundles"]:
            for m in (b["media"] or {}).get("segments", []):
                rec = segs.get(m["segment_id"])
                if rec is None:
                    sel = selected[m["segment_id"]]
                    rec = {**m, "concept_id": b["context"]["concept_id"], "channel_id": sel["channel_id"],
                           "visual_mode": sel["visual_mode"], "role": sel["role"], "mean_score": sel["mean_score"],
                           "approved_in_batch_id": batch_id, "used_by_path_ids": []}
                    validate(rec, "approved_segment.schema.json")
                    segs[m["segment_id"]] = rec
                if b["context"]["path_id"] not in rec["used_by_path_ids"]:
                    rec["used_by_path_ids"].append(b["context"]["path_id"])
    bank["segments"] = list(segs.values())
    save(seg_path, bank)

    props = {p["proposal_id"]: p for p in load(d / "segment_proposals.json")["proposals"]}
    touched = 0
    for j in load(d / "segment_judgments.json")["judgments"]:
        p = props[j["proposal_id"]]
        cat_path = core / "video_bank" / "catalogue" / f"{p['video_id']}.json"
        cat = load(cat_path)
        judged = {
            "concept_id": p["concept_id"],
            "start_seconds": j["final_start_seconds"] if j["final_start_seconds"] is not None else p["start_seconds"],
            "end_seconds": j["final_end_seconds"] if j["final_end_seconds"] is not None else p["end_seconds"],
            "verdict": j["verdict"], "batch_id": batch_id}
        if judged not in cat["judged_ranges"]:  # re-running a merge must not duplicate history
            cat["judged_ranges"].append(judged)
            save(cat_path, cat)
            touched += 1
    print(f"merged: {len(registry['entries'])} concepts in registry, {len(bank['segments'])} approved segments, "
          f"{touched} judged ranges recorded")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(*sys.argv[1:])
