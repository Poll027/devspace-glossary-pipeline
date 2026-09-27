"""14_bundle_assembly: glossary_bundles_draft.json + clusters.json -> path_glossary_bundle.<path_id>.json. Deterministic.

Refuses to run while leakage_audit_report.json has blocking issues.

Usage: python3 assemble_bundles.py <batch_dir>
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from schema_check import validate


def load(p):
    return json.loads(Path(p).read_text())


def assemble(draft, clusters, extracted):
    order = {(c["path_id"], c["concept_id"]): c["toc_sequence_position"] for c in extracted["concepts"]}
    cluster_of = {(cl["path_id"], cid): cl["cluster_id"] for cl in clusters["clusters"] for cid in cl["concept_ids"]}
    by_path = {}
    for b in draft["bundles"]:
        pid, cid = b["context"]["path_id"], b["context"]["concept_id"]
        by_path.setdefault(pid, []).append({**b, "cluster_ref": cluster_of.get((pid, cid))})

    now = datetime.now(timezone.utc).isoformat()
    out = {}
    for pid, bundles in by_path.items():
        bundles.sort(key=lambda b: order[(pid, b["context"]["concept_id"])])
        tiers = [b["context"]["depth_tier"] for b in bundles]
        with_media = [b for b in bundles if b["media"]]
        out[pid] = {
            "path_id": pid, "batch_id": draft["batch_id"], "assembled_at": now, "bundles": bundles,
            "clusters": [cl for cl in clusters["clusters"] if cl["path_id"] == pid],
            "counts": {"concepts": len(bundles), "with_video": len(with_media),
                       "segments": sum(len(b["media"]["segments"]) for b in with_media),
                       "core": tiers.count("core"), "standard": tiers.count("standard"), "reference": tiers.count("reference")},
        }
    return out


def main(batch_dir):
    d = Path(batch_dir)
    leak = load(d / "leakage_audit_report.json")
    if leak["blocking_issue_count"]:
        sys.exit(f"refusing to assemble: {leak['blocking_issue_count']} blocking leakage issues — fix the owning stage first")
    for pid, bundle in assemble(load(d / "glossary_bundles_draft.json"), load(d / "clusters.json"),
                                load(d / "extracted_concepts.json")).items():
        validate(bundle, "path_glossary_bundle.schema.json")
        (d / f"path_glossary_bundle.{pid}.json").write_text(json.dumps(bundle, indent=2))
        print(f"{pid}: {bundle['counts']}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
