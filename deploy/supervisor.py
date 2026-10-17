#!/usr/bin/env python3
"""Keep the pipeline driver running unattended and deal with stops.  Run under systemd (see install_service.sh):

    python3 deploy/supervisor.py batches/<batch_id> [--max-usd 300] [--driver-args "--no-push"]

- Runs run_pipeline.py and appends its output to run.log. Exit 0 = batch done.
- Stall watchdog: no file in the batch's working/ folder has changed for STALL_WARN_MIN (25) minutes -> SNS warning;
  for STALL_KILL_MIN (45) -> kill and restart (the driver resumes; finished chunks are cached/gated).
- On a stop (driver exit 2 or a crash) a triage agent reads the stop file and logs and classifies it:
    transient -> wait, then restart automatically (max MAX_RESTARTS per distinct cause)
    content / code / human -> email you with the reason; for code bugs the agent writes working/proposed_fix.md
  The triage agent cannot edit code and is told never to weaken evaluators, gates or the ledger. It is never trusted to
  auto-apply a fix: you review proposed_fix.md.
- Budget: stops for good (email) when the shared cost log passes --max-usd. Triage spend counts too.
# ponytail: one batch per supervisor; the triage verdict is advisory text from a model, so only 'transient' is acted on.
"""
import argparse, json, os, re, shlex, signal, subprocess, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "00_GLOSSARY_PIPELINE_CORE" / "scripts"))
from bedrock_agent import Budget, BudgetExceeded, run_agent  # noqa: E402
from glm_generate import load_env  # noqa: E402

STALL_WARN_MIN = float(os.environ.get("STALL_WARN_MIN", 25))
STALL_KILL_MIN = float(os.environ.get("STALL_KILL_MIN", 45))
MAX_RESTARTS = int(os.environ.get("MAX_RESTARTS", 3))

TRIAGE_SYSTEM = """You triage why an unattended data pipeline stopped. You have read_file and bash (read-only investigation: tail, grep, cat, python for parsing).
You may write ONLY under the batch's working/ folder. You can NOT edit any code. Classify the stop into exactly one class:
- transient: infrastructure/service trouble a plain rerun will likely clear (network errors, timeouts, throttling, a service error, a killed process, a reboot).
- content: the generator/evaluator loop could not resolve a content defect (an evaluator finding that repairs did not fix).
- code: a bug in our own scripts (traceback in our code, bad path, our own parsing/schema failure).
- human: budget cap reached, missing credentials/permissions, a quota that needs raising, or anything ambiguous or needing a decision.
Rules: never recommend weakening an evaluator, a gate, the ledger or a check just to make the run pass. If a repeated evaluator finding looks like a false positive, say so under class "human" and quote it. If class is code, write your proposed fix (precise diff or description) to working/proposed_fix.md.
Be efficient: use at most about 8 tool calls (read the stop file first, then only what you need), then answer. Finish with ONE JSON object and nothing else: {"class": "...", "reason": "one or two sentences with the key error text", "action": "what you did or what the human should do"}"""


def notify(subject, body):
    print(f"[supervisor] {subject}\n{body[:1500]}", flush=True)
    topic = os.environ.get("SNS_TOPIC_ARN")
    if topic:
        try:
            import boto3
            boto3.client("sns", region_name=topic.split(":")[3]).publish(TopicArn=topic, Subject=subject[:100], Message=body[:20000])
        except Exception as e:
            print(f"[supervisor] SNS failed: {e}", flush=True)


def last_activity(B):
    files = list((B / "working").glob("*.log")) + [B / "working" / "cost_log.jsonl", B / "working" / "driver.log", ROOT / "run.log"]  # run.log: the driver's own stderr incl. "[ladder] waiting for quota" lines
    return max((f.stat().st_mtime for f in files if f.exists()), default=0)


def run_driver(cmd, B):
    """Returns the driver's exit code, or 98 if it was killed for stalling."""
    with open(ROOT / "run.log", "a") as log:
        p = subprocess.Popen(cmd, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT, env={**os.environ, "SUPERVISED": "1"}, start_new_session=True)
        warned, started = False, time.time()
        while p.poll() is None:
            time.sleep(30)
            idle = (time.time() - max(last_activity(B), started)) / 60
            if idle > STALL_KILL_MIN:
                notify("Glossary pipeline stalled, restarting", f"No activity for {idle:.0f} min in {B.name}/working. Killing the driver; it will resume.")
                os.killpg(p.pid, signal.SIGKILL); p.wait()
                return 98
            if idle > STALL_WARN_MIN and not warned:
                warned = True
                notify("Glossary pipeline looks stalled", f"No activity for {idle:.0f} min in {B.name}/working. It restarts at {STALL_KILL_MIN:.0f} min.")
        return p.returncode


def stop_reason(B):
    f = B / "working" / "DRIVER_STOPPED.md"
    if f.exists():
        return f.read_text()
    tail = (ROOT / "run.log").read_text()[-3000:] if (ROOT / "run.log").exists() else ""
    return "No stop file; the driver crashed. Tail of run.log:\n" + tail


def triage(B, budget, reason):
    task = (f"The pipeline driver for batch folder `{B.relative_to(ROOT)}` stopped. Stop reason:\n\n{reason[-4000:]}\n\n"
            f"Investigate with the tools: `{B.relative_to(ROOT)}/working/driver.log`, `run.log` in the pack root, and `{B.relative_to(ROOT)}/working/sub_*.log` "
            f"(live logs of the generator/evaluator subprocesses). Then classify and reply with the JSON.")
    try:
        text = run_agent("GEN", TRIAGE_SYSTEM, task, budget, role="GEN", write_roots=[B / "working"], max_turns=14, label="triage")
        m = re.search(r"\{.*\}", text, re.S)
        v = json.loads(m.group(0))
        if v.get("class") in ("transient", "content", "code", "human"):
            return v
    except BudgetExceeded:
        raise
    except Exception as e:
        return {"class": "human", "reason": f"triage agent failed: {e}", "action": "read the stop reason yourself"}
    return {"class": "human", "reason": "triage gave no usable verdict", "action": "read the stop reason yourself"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("batch_dir"); ap.add_argument("--max-usd", type=float, default=float(os.environ.get("MAX_USD", 300)))
    ap.add_argument("--driver-args", default=os.environ.get("DRIVER_ARGS", ""))
    ap.add_argument("--driver-cmd", help="override the driver command (testing)")
    a = ap.parse_args()
    load_env()
    B = Path(a.batch_dir); B = B if B.is_absolute() else ROOT / B
    (B / "working").mkdir(parents=True, exist_ok=True)
    budget = Budget(a.max_usd, B / "working" / "cost_log.jsonl")
    cmd = shlex.split(a.driver_cmd) if a.driver_cmd else [sys.executable, str(ROOT / "00_GLOSSARY_PIPELINE_CORE/scripts/run_pipeline.py"), str(B),
                                                           "--max-usd", str(a.max_usd), *shlex.split(a.driver_args)]
    restarts = {}
    while True:
        if budget.spent() > a.max_usd:
            notify(f"Glossary pipeline stopped: budget cap ${a.max_usd:.0f}", f"Spend ${budget.spent():.2f}. Raise MAX_USD and restart the service to continue."); sys.exit(3)
        (B / "working" / "DRIVER_STOPPED.md").unlink(missing_ok=True)  # only a stop written by THIS run may be triaged
        code = run_driver(cmd, B)
        if code == 0:
            print("[supervisor] driver finished cleanly", flush=True); return
        stalled = code == 98
        reason = "stalled: no activity, killed by the watchdog" if stalled else stop_reason(B)
        first = next((ln for ln in reason.splitlines() if ln.strip() and not ln.startswith("#")), reason[:120])
        sig = "stalled" if stalled else re.sub(r"\d+", "#", first[:120])
        if "passed the cap" in reason:
            notify("Glossary pipeline stopped: spend cap", reason); sys.exit(3)
        try:
            v = {"class": "transient", "reason": reason, "action": "restart"} if stalled else triage(B, budget, reason)
        except BudgetExceeded as e:
            notify("Glossary pipeline stopped: spend cap", str(e)); sys.exit(3)
        print(f"[supervisor] triage: {v}", flush=True)
        if v["class"] == "transient" and restarts.get(sig, 0) < MAX_RESTARTS:
            restarts[sig] = restarts.get(sig, 0) + 1
            (B / "working" / "DRIVER_STOPPED.md").unlink(missing_ok=True)
            wait = int(os.environ.get("RESTART_WAIT_S", 60)) * restarts[sig]
            print(f"[supervisor] transient; restart {restarts[sig]}/{MAX_RESTARTS} in {wait}s", flush=True)
            time.sleep(wait)
            continue
        fix = B / "working" / "proposed_fix.md"
        body = (f"Class: {v['class']}\nReason: {v['reason']}\nAction: {v['action']}\n\nStop reason:\n{reason[-2500:]}"
                + (f"\n\nProposed fix (NOT applied):\n{fix.read_text()[:6000]}" if fix.exists() else "")
                + (f"\n\n(transient but restarted {MAX_RESTARTS} times already)" if v["class"] == "transient" else ""))
        notify(f"Glossary pipeline needs you ({v['class']})", body)
        sys.exit(2)


if __name__ == "__main__":
    main()
