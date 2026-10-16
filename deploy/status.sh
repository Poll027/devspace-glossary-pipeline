#!/usr/bin/env bash
# One-shot progress report for a running (or stopped) pipeline.  Run from the repo root:
#   bash deploy/status.sh [batches/<batch_id>]     (default: the pilot)
B="${1:-batches/glossary_batch_001_data_analyst_pilot}"
PY="${PY:-$HOME/env/bin/python}"
echo "== process"; pgrep -fl run_pipeline >/dev/null && echo "RUNNING" || echo "not running"
echo "== stopped/done markers"; ls "$B"/working/DRIVER_STOPPED.md "$B"/working/DRIVER_DONE.md 2>/dev/null || echo "(none)"
echo "== stages gated"
"$PY" - "$B" <<'E'
import json, sys, glob, os
b = sys.argv[1]
try:
    for g in json.load(open(f"{b}/glossary_stage_gate_ledger.json"))["gates"]:
        print(f"  {g['stage_id']:26} {g['verdict']}")
except FileNotFoundError:
    print("  (no ledger yet)")
st = sorted(glob.glob(f"{b}/working/state_*.json"))
print(f"== chunks passed (this run): {len(st)}")
for f in st:
    print("  ", os.path.basename(f)[6:-5])
try:
    rows = [json.loads(l) for l in open(f"{b}/working/cost_log.jsonl") if l.strip()]
    print(f"== spend: ${sum(r['usd'] for r in rows):.2f} over {len(rows)} model calls")
except FileNotFoundError:
    print("== spend: $0.00 (no calls yet)")
E
echo "== last 12 log lines"; tail -n 12 "$B"/working/driver.log 2>/dev/null || echo "(no log yet)"
