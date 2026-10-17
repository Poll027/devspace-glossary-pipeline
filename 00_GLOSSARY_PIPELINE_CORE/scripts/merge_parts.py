"""Combine a fanned-out stage's part files into its single artifact.

Parts are <artifact>.part.<chunk>.json in the batch folder. Top-level lists are concatenated,
top-level integers summed (e.g. blocking_issue_count), everything else taken from the first part.
Rejects duplicate rows, so an overlapping fan-out is caught instead of silently merged.

Usage: python3 merge_parts.py <batch_dir> <artifact.json> <schema file name>
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from schema_check import validate

ROW_KEYS = ("concept_id", "path_id", "proposal_id", "video_id", "cluster_id")


def row_key(row):
    if not isinstance(row, dict):
        return row
    key = tuple(row.get(k) for k in ROW_KEYS)
    if all(v is None for v in key) and isinstance(row.get("context"), dict):  # glossary_bundles_draft rows carry their ids in "context"
        key = tuple(row["context"].get(k) for k in ROW_KEYS)
    return key


def merge(parts):
    out = json.loads(json.dumps(parts[0]))
    for p in parts[1:]:
        for k, v in p.items():
            if isinstance(v, list):
                out[k] = out.get(k, []) + v
            elif isinstance(v, int) and not isinstance(v, bool):
                out[k] = out.get(k, 0) + v
    for k, v in out.items():
        if isinstance(v, list):
            keys = [row_key(r) for r in v]
            dupes = {x for x in keys if keys.count(x) > 1}
            if dupes:
                sys.exit(f"duplicate rows in '{k}' across parts: {sorted(map(str, dupes))[:5]}")
    if isinstance(out.get("metadata"), dict):
        out["metadata"]["generated_at"] = datetime.now(timezone.utc).isoformat()
    return out


def main(batch_dir, artifact, schema):
    d = Path(batch_dir)
    stem = artifact.removesuffix(".json")
    files = sorted(d.glob(f"{stem}.part.*.json"))
    if not files:
        sys.exit(f"no {stem}.part.*.json files in {d}")
    out = merge([json.loads(f.read_text()) for f in files])
    validate(out, schema)
    (d / artifact).write_text(json.dumps(out, indent=2))
    print(f"merged {len(files)} parts -> {artifact}")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    main(*sys.argv[1:])
