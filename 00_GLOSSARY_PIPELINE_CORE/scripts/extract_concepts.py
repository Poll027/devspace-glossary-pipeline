"""01_extraction: frozen TOC workspaces -> extracted_concepts.json. Deterministic; no model involved.

Usage: python3 extract_concepts.py <batch_run_context.json> <out extracted_concepts.json>
"""
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from schema_check import validate


def load(path):
    return json.loads(Path(path).read_text())


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def extract_path(path_id, ws):
    ws = Path(ws)
    if not (ws / "freeze_manifest.json").exists():
        sys.exit(f"{path_id}: no freeze_manifest.json in {ws} — not eligible")

    seq = sorted(load(ws / "ordered_concept_sequence.json")["concepts"], key=lambda c: c["sequence_index"])
    graph = {c["concept_id"]: c for c in load(ws / "prerequisite_graph.json")["concepts"]}
    atom = {c["concept_id"]: c for c in load(ws / "atomicity_validation_report.json")["concept_results"]}
    names = {c["concept_id"]: c["canonical_name"] for c in load(ws / "concept_inventory.json")["candidate_concepts"]}
    spec = load(ws / "path_specification.json")

    tiles = {}
    for r in load(ws / "toc.json")["regions"]:
        for t in r["terrains"]:
            for ti in t["tiles"]:
                for cid in ti["concept_unit_refs"]:
                    tiles[cid] = {"region_id": r["region_id"], "terrain_id": t["terrain_id"], "tile_id": ti["tile_id"],
                                  "tile_title": ti["title"], "tile_summary": ti["summary"]}

    order = [c["concept_id"] for c in seq]
    missing = [c for c in order if c not in graph or c not in atom or c not in tiles]
    if missing:
        sys.exit(f"{path_id}: concepts missing from prerequisite_graph/atomicity report/toc: {missing[:5]}")

    centrality = {cid: 0 for cid in order}
    for c in graph.values():
        for p in c["direct_prerequisite_ids"]:
            if p in centrality:
                centrality[p] += 1

    rows = []
    for i, c in enumerate(seq):
        cid, g, a = c["concept_id"], graph[c["concept_id"]], atom[c["concept_id"]]
        rows.append({
            "concept_id": cid,
            # atomicity splits create children the inventory never named; fall back to the id's last segment
            "concept_name": names.get(cid) or cid.split(".")[-1].replace("_", " ").capitalize(),
            "path_id": path_id,
            "concept_family_id": c["concept_family_id"],
            "toc_sequence_position": c["sequence_index"],
            "toc_location": tiles[cid],
            "direct_prerequisite_ids": g["direct_prerequisite_ids"],
            "allowed_knowledge_ids": order[:i],
            "blocked_knowledge_ids": order[i + 1:],
            "inline_vocabulary": g["inline_vocabulary"],
            "forward_preview_ids": g["forward_preview_ids"],
            "dependency_graph_centrality": centrality[cid],
            "primary_objective": a["primary_objective"] or "",
            "assessment_target": a["assessment_target"] or "",
            "practice_objective": a["practice_objective"] or "",
            "central_mental_model": a["central_mental_model"] or "",
        })
    path_row = {"path_id": path_id, "toc_workspace": str(ws), "path_title": spec["title"],
                "learner_scope": spec["learner_scope"], "concept_count": len(rows)}
    return path_row, rows


def main(ctx_path, out_path):
    ctx = load(ctx_path)
    paths, concepts = [], []
    for p in ctx["paths"]:
        path_row, rows = extract_path(p["path_id"], p["toc_workspace"])
        paths.append(path_row)
        concepts.extend(rows)

    out = {
        "metadata": {
            "artifact_type": "extracted_concepts", "artifact_version": "1.0.0", "schema_version": "1.0.0",
            "batch_id": ctx["batch_id"], "run_id": ctx["batch_id"], "prompt_version": "n/a-deterministic",
            "model": "deterministic/extract_concepts.py", "generated_at": datetime.now(timezone.utc).isoformat(),
            "source_snapshot_id": ctx["batch_id"],
            "parent_artifact_hashes": {"batch_run_context.json": sha256(ctx_path)},
        },
        "batch_id": ctx["batch_id"],
        "paths": paths,
        "concepts": concepts,
    }
    validate(out, "extracted_concepts.schema.json")
    Path(out_path).write_text(json.dumps(out, indent=2))
    print(f"wrote {len(concepts)} concept rows across {len(paths)} path(s) -> {out_path}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
