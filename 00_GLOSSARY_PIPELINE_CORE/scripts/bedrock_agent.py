#!/usr/bin/env python3
"""Minimal tool-using agent on AWS Bedrock (Converse API): the stand-in for a Claude Code subagent.

The stage instruction files are written for agents that read inputs and write artifacts themselves, so this
runs the same instructions with three tools: read_file, write_file, bash. A fresh call = a fresh context.

    from bedrock_agent import run_agent, Budget
    text = run_agent(model_id, system, task, budget, write_roots=[batch_dir, scratch_dir])

Spend is counted from the token usage of every call (shared cost log); Budget.check() raises BudgetExceeded past the cap.
# ponytail: no prompt caching, no streaming; old tool results are elided once the context gets large.
"""
import json, os, re, subprocess, sys, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from glm_generate import ROOT, load_env, log_usage, make_client  # noqa: E402

MAX_TOOL_CHARS = 14000
DENY = re.compile(r"\b(sudo|git\s+(push|reset|checkout|clean)|aws\s|shutdown|reboot|mkfs|dd\s+if=)\b|rm\s+-rf\s+(/|~|\.\.)")


class BudgetExceeded(Exception):
    pass


class Budget:
    """Spend cap over the shared cost log (every script and agent appends to it via glm_generate.log_usage)."""

    def __init__(self, max_usd, log_path):
        self.max_usd, self.log_path = max_usd, str(log_path)
        os.environ["COST_LOG"] = self.log_path  # subprocesses inherit it

    def spent(self):
        try:
            return sum(json.loads(ln)["usd"] for ln in open(self.log_path) if ln.strip())
        except FileNotFoundError:
            return 0.0

    def check(self):
        s = self.spent()
        if s > self.max_usd:
            raise BudgetExceeded(f"estimated spend ${s:.2f} passed the cap ${self.max_usd:.2f}")


TOOLS = {"tools": [
    {"toolSpec": {"name": "read_file", "description": "Read a text file (path relative to the pack root, or absolute). Returns numbered lines; use offset/limit for big files.",
                  "inputSchema": {"json": {"type": "object", "properties": {"path": {"type": "string"}, "offset": {"type": "integer"}, "limit": {"type": "integer"}}, "required": ["path"]}}}},
    {"toolSpec": {"name": "write_file", "description": "Write (overwrite) a text file. Only allowed under the batch folder and the scratch folder.",
                  "inputSchema": {"json": {"type": "object", "properties": {"path": {"type": "string"}, "content": {"type": "string"}}, "required": ["path", "content"]}}}},
    {"toolSpec": {"name": "bash", "description": "Run a shell command from the pack root (python3 here has jsonschema; use it for scripts, jq-style JSON work, grep, curl, pdftotext). No sudo/git push/aws.",
                  "inputSchema": {"json": {"type": "object", "properties": {"command": {"type": "string"}, "timeout": {"type": "integer"}}, "required": ["command"]}}}},
]}


def _clip(s, n=MAX_TOOL_CHARS):
    return s if len(s) <= n else s[: n // 2] + f"\n...[{len(s) - n} chars elided]...\n" + s[-n // 2:]


def _resolve(p):
    p = Path(p)
    return (p if p.is_absolute() else ROOT / p).resolve()


def run_tool(name, args, write_roots):
    try:
        if name == "read_file":
            f = _resolve(args["path"])
            lines = f.read_text(errors="replace").splitlines()
            off, lim = int(args.get("offset", 0)), int(args.get("limit", 600))
            body = "\n".join(f"{i + 1}\t{ln}" for i, ln in enumerate(lines[off:off + lim], start=off))
            tail = f"\n[lines {off + 1}-{min(off + lim, len(lines))} of {len(lines)}]" if len(lines) > lim else ""
            return _clip(body) + tail
        if name == "write_file":
            f = _resolve(args["path"])
            if not any(f.is_relative_to(Path(r).resolve()) for r in write_roots):
                return f"ERROR: writes are only allowed under {[str(r) for r in write_roots]}"
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_text(args["content"])
            return f"wrote {len(args['content'])} chars to {f}"
        if name == "bash":
            cmd = args["command"]
            if DENY.search(cmd):
                return "ERROR: command not allowed"
            r = subprocess.run(["bash", "-lc", cmd], cwd=ROOT, capture_output=True, text=True, timeout=min(int(args.get("timeout", 120)), 600))
            return _clip((r.stdout + r.stderr) or "(no output)") + (f"\n[exit {r.returncode}]" if r.returncode else "")
        return f"ERROR: unknown tool {name}"
    except subprocess.TimeoutExpired:
        return "ERROR: command timed out"
    except Exception as e:  # tool errors go back to the model, they never crash the run
        return f"ERROR: {type(e).__name__}: {e}"


def _elide_old(messages, keep=10, limit_chars=500_000):
    if len(json.dumps(messages)) < limit_chars:
        return
    results = [b for m in messages if m["role"] == "user" for b in m["content"] if isinstance(b, dict) and "toolResult" in b]
    for b in results[:-keep]:
        b["toolResult"]["content"] = [{"text": "[old tool result elided to save context; re-read the file if you need it]"}]


def run_agent(model_id, system, task, budget, role="GEN", write_roots=(), max_turns=90, label=""):
    load_env()
    client = make_client()
    messages = [{"role": "user", "content": [{"text": task}]}]
    for _ in range(max_turns):
        _elide_old(messages)
        for attempt in range(6):
            try:
                r = client.converse(modelId=model_id, system=[{"text": system}], messages=messages, toolConfig=TOOLS,
                                    inferenceConfig={"maxTokens": 32000, "temperature": 0.2})
                break
            except Exception as e:
                if attempt == 5 or "Throttling" not in type(e).__name__ + str(e):
                    raise
                time.sleep(5 * 2 ** attempt)
        log_usage(model_id, r["usage"], label)
        budget.check()
        msg = r["output"]["message"]
        messages.append(msg)
        uses = [b["toolUse"] for b in msg["content"] if "toolUse" in b]
        if r["stopReason"] != "tool_use" or not uses:
            return "".join(b.get("text", "") for b in msg["content"])
        messages.append({"role": "user", "content": [
            {"toolResult": {"toolUseId": u["toolUseId"], "content": [{"text": run_tool(u["name"], u["input"], write_roots)}]}} for u in uses]})
    return "ERROR: agent hit the turn limit without finishing"
