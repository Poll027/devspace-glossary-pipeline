"""Record a stage gate, or verify the whole ledger. The only writer of glossary_stage_gate_ledger.json.

Record (run by the orchestrator right after a stage's gate decision):
  python3 update_ledger.py <batch_dir> record <stage_id> <artifact filename or glob> <PASS|FAIL>
                           [--generator MODEL] [--evaluator MODEL] [--unresolved N]
Verify (15b_stage_gate_ledger): exits 1 if any gate is FAIL, stale (artifact changed since gated), or missing.
  python3 update_ledger.py <batch_dir> verify <stage_id> [<stage_id> ...]
"""
import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from schema_check import validate


def artifact_hash(batch_dir, artifact):
    files = sorted(Path(batch_dir).glob(artifact))
    if not files:
        raise FileNotFoundError(f"no file matches {artifact} in {batch_dir}")
    h = hashlib.sha256()
    for f in files:
        h.update(f.read_bytes())
    return h.hexdigest()


def load_ledger(d):
    p = Path(d) / "glossary_stage_gate_ledger.json"
    if p.exists():
        return json.loads(p.read_text())
    batch_id = json.loads((Path(d) / "batch_run_context.json").read_text())["batch_id"]
    return {"metadata": {}, "batch_id": batch_id, "gates": []}


def record(d, stage_id, artifact, verdict, generator=None, evaluator=None, unresolved=0):
    ledger = load_ledger(d)
    now = datetime.now(timezone.utc).isoformat()
    row = {"stage_id": stage_id, "artifact": artifact, "artifact_hash": artifact_hash(d, artifact),
           "generator_model": generator, "evaluator_model": evaluator, "verdict": verdict,
           "unresolved_issue_count": unresolved, "gated_at": now}
    ledger["gates"] = [g for g in ledger["gates"] if g["stage_id"] != stage_id] + [row]
    ledger["metadata"] = {
        "artifact_type": "glossary_stage_gate_ledger", "artifact_version": "1.0.0", "schema_version": "1.0.0",
        "batch_id": ledger["batch_id"], "run_id": ledger["batch_id"], "prompt_version": "n/a-deterministic",
        "model": "deterministic/update_ledger.py", "generated_at": now, "source_snapshot_id": ledger["batch_id"],
        "parent_artifact_hashes": {}}
    validate(ledger, "glossary_stage_gate_ledger.schema.json")
    (Path(d) / "glossary_stage_gate_ledger.json").write_text(json.dumps(ledger, indent=2))


def verify(d, required_stages):
    gates = {g["stage_id"]: g for g in load_ledger(d)["gates"]}
    problems = [f"{s}: no gate recorded" for s in required_stages if s not in gates]
    for s, g in gates.items():
        if g["verdict"] != "PASS":
            problems.append(f"{s}: verdict {g['verdict']}")
        try:
            if artifact_hash(d, g["artifact"]) != g["artifact_hash"]:
                problems.append(f"{s}: STALE — {g['artifact']} changed after it was gated")
        except FileNotFoundError as e:
            problems.append(f"{s}: {e}")
    return problems


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("batch_dir")
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("record")
    r.add_argument("stage_id"), r.add_argument("artifact"), r.add_argument("verdict", choices=["PASS", "FAIL"])
    r.add_argument("--generator"), r.add_argument("--evaluator"), r.add_argument("--unresolved", type=int, default=0)
    v = sub.add_parser("verify")
    v.add_argument("stages", nargs="*")
    a = ap.parse_args()
    if a.cmd == "record":
        record(a.batch_dir, a.stage_id, a.artifact, a.verdict, a.generator, a.evaluator, a.unresolved)
        print(f"recorded {a.stage_id} {a.verdict}")
    else:
        probs = verify(a.batch_dir, a.stages)
        print("LEDGER OK" if not probs else "\n".join(probs))
        sys.exit(1 if probs else 0)
