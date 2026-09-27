"""02_registry_lookup: decide, per (concept_id, path_id), whether canonical evidence is reused or built. Deterministic.

Reuse is an exact concept_id match — the TOC pipeline's global concept registry already gives the same
concept the same id in every path. Near-duplicates with different ids are the TOC registry's problem, not this one's.

Usage: python3 registry_lookup.py <extracted_concepts.json> <concept_evidence_registry_snapshot.json>
                                  <approved_segments_snapshot.json> <out registry_lookup.json>
"""
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from schema_check import validate


def load(p):
    return json.loads(Path(p).read_text())


def sha256(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def lookup(extracted, registry, segments):
    known = {e["concept_id"] for e in registry["entries"]}
    segs_by_concept = {}
    for s in segments["segments"]:
        segs_by_concept.setdefault(s["concept_id"], []).append(s["segment_id"])

    owner = {}  # first path in this batch that builds a concept's canonical evidence
    rows = []
    for c in extracted["concepts"]:
        cid, pid = c["concept_id"], c["path_id"]
        if cid in known:
            status, built_by = "reuse_registry", None
        elif cid in owner:
            status, built_by = "shared_in_batch", owner[cid]
        else:
            status, built_by = "new", pid
            owner[cid] = pid
        rows.append({"concept_id": cid, "path_id": pid, "canonical_status": status,
                     "evidence_built_by_path_id": built_by,
                     "reusable_segment_ids": segs_by_concept.get(cid, [])})
    return rows


def main(ext_p, reg_p, seg_p, out_p):
    ext = load(ext_p)
    rows = lookup(ext, load(reg_p), load(seg_p))
    out = {
        "metadata": {
            "artifact_type": "registry_lookup", "artifact_version": "1.0.0", "schema_version": "1.0.0",
            "batch_id": ext["batch_id"], "run_id": ext["batch_id"], "prompt_version": "n/a-deterministic",
            "model": "deterministic/registry_lookup.py", "generated_at": datetime.now(timezone.utc).isoformat(),
            "source_snapshot_id": ext["batch_id"],
            "parent_artifact_hashes": {Path(p).name: sha256(p) for p in (ext_p, reg_p, seg_p)},
        },
        "batch_id": ext["batch_id"],
        "lookups": rows,
    }
    validate(out, "registry_lookup.schema.json")
    Path(out_p).write_text(json.dumps(out, indent=2))
    counts = {}
    for r in rows:
        counts[r["canonical_status"]] = counts.get(r["canonical_status"], 0) + 1
    print(f"wrote {len(rows)} lookups {counts} -> {out_p}")


if __name__ == "__main__":
    if len(sys.argv) != 5:
        sys.exit(__doc__)
    main(*sys.argv[1:])
