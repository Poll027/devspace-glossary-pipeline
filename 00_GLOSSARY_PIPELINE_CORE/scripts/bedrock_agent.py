"""Minimal tool-using agent over the pipeline's Converse-shaped client (Azure OpenAI via llm_azure.py; Bedrock still works): the stand-in for a Claude Code subagent.

The stage instruction files are written for agents that read inputs and write artifacts themselves, so this runs the same
instructions with three tools: read_file, write_file, bash. A fresh call = a fresh context.

    text = run_agent("GEN"|"EVAL"|<model id>, system, task, budget, write_roots=[batch_dir, scratch_dir], call_cap_usd=4)

Spend is counted from the token usage of every call (shared cost log). Budget.check() raises BudgetExceeded past the run cap;
call_cap_usd stops one runaway agent loop long before the run cap does.
# ponytail: no prompt caching, no streaming; old tool results are elided once the context gets large.
"""
import json, random
import os
import re
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from bedrock_llm import LAST, ROOT, converse_ladder, load_env, log_usage, make_client  # noqa: E402

MAX_TOOL_CHARS = 14000
DENY = re.compile(r"\b(sudo|git\s+(push|reset|checkout|clean|commit)|aws\s|az\s|shutdown|reboot|mkfs|dd\s+if=)\b|rm\s+-rf\s+(/|~|\.\.)")


class BudgetExceeded(Exception):
    pass


class Budget:
    """Spend cap over the shared cost log (every caller appends to it via bedrock_llm.log_usage)."""

    def __init__(self, max_usd, log_path):
        self.max_usd, self.log_path = max_usd, str(log_path)
        os.environ["COST_LOG"] = self.log_path  # subprocesses inherit it
        os.environ.setdefault("QUOTA_STATE", str(Path(self.log_path).parent / "quota_state.json"))

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
    {"toolSpec": {"name": "bash", "description": "Run a shell command from the pack root (python3 here has jsonschema; use it for scripts, JSON work, grep). No sudo, git writes or aws.",
                  "inputSchema": {"json": {"type": "object", "properties": {"command": {"type": "string"}, "timeout": {"type": "integer"}}, "required": ["command"]}}}},
]}


def _clip(s, n=MAX_TOOL_CHARS):
    return s if len(s) <= n else s[: n // 2] + f"\n...[{len(s) - n} chars elided]...\n" + s[-n // 2:]


def _resolve(p):
    p = Path(p)
    return (p if p.is_absolute() else ROOT / p).resolve()


def run_tool(name, args, write_roots, protected=()):
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
            if any(f == Path(q).resolve() or f.is_relative_to(Path(q).resolve()) for q in protected):
                return f"ERROR: {f.name} belongs to a finished stage (or is pipeline-owned) and may not be edited; write only your own stage's artifact"
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_text(args["content"])
            return f"wrote {len(args['content'])} chars to {f}"
        if name == "bash":
            cmd = args["command"]
            if DENY.search(cmd):
                return "ERROR: command not allowed"
            env = {**os.environ, "PATH": f"{Path(sys.executable).parent}:{os.environ['PATH']}"}  # the interpreter that has jsonschema
            r = subprocess.run(["bash", "-c", cmd], cwd=ROOT, capture_output=True, text=True, env=env, timeout=min(int(args.get("timeout", 120)), 600))
            return _clip((r.stdout + r.stderr) or "(no output)") + (f"\n[exit {r.returncode}]" if r.returncode else "")
        return f"ERROR: unknown tool {name}"
    except subprocess.TimeoutExpired:
        return "ERROR: command timed out"
    except Exception as e:  # tool errors go back to the model, they never crash the run
        return f"ERROR: {type(e).__name__}: {e}"


TRANSIENT = ("Throttling", "ConnectionClosed", "EndpointConnection", "Timeout", "ProtocolError", "ServiceUnavailable", "InternalServer", "ModelStreamError")


def transient(e):
    """Errors a plain retry usually clears: throttling, dropped connections, timeouts, 5xx. (Quota-per-day and access errors are not.)"""
    return isinstance(e, (ConnectionError, TimeoutError)) or any(k in type(e).__name__ + str(e) for k in TRANSIENT)


CACHE = {"cachePoint": {"type": "default"}}
_NO_CACHE = set()  # models that rejected a cachePoint: stop sending it


def with_cache(model_id, system, messages):
    """Prompt caching: checkpoints after the system prompt, the tool list and the newest message, so each turn re-reads the whole
    earlier conversation at 10% of the input price. Only one message carries a checkpoint (the previous one is stripped): the cache
    prefix is everything before it. Returns (system, toolConfig, messages) for one call; ponytail: 5-minute cache, no 1-hour TTL."""
    for m in messages:
        m["content"] = [b for b in m["content"] if "cachePoint" not in b]
    if model_id in _NO_CACHE:
        return [{"text": system}], TOOLS, messages
    messages[-1]["content"].append(dict(CACHE))
    return [{"text": system}, dict(CACHE)], {"tools": TOOLS["tools"] + [dict(CACHE)]}, messages


def _elide_old(messages, keep=10, limit_chars=500_000):
    if len(json.dumps(messages)) < limit_chars:
        return
    results = [b for m in messages if m["role"] == "user" for b in m["content"] if isinstance(b, dict) and "toolResult" in b]
    for b in results[:-keep]:
        b["toolResult"]["content"] = [{"text": "[old tool result elided to save context; re-read the file if you need it]"}]


def run_agent(model_id, system, task, budget, role="GEN", write_roots=(), max_turns=90, label="", call_cap_usd=None, protected=()):
    load_env()
    client = make_client()
    messages = [{"role": "user", "content": [{"text": task}]}]
    mine = 0.0
    for turn in range(max_turns):
        if turn == max_turns - 3:  # nudge: an agent that keeps investigating must still give its final reply
            messages[-1]["content"].append({"text": "You are nearly out of turns. Stop investigating and give your final reply now."})
        _elide_old(messages)
        for attempt in range(10):
            try:
                sysb, tools, msgs = with_cache(model_id, system, messages)
                kw = dict(system=sysb, messages=msgs, toolConfig=tools, inferenceConfig={"maxTokens": 32000, "temperature": 0.2})
                if model_id in ("GEN", "EVAL"):  # role ladder: falls back per call when a model's daily quota is hit
                    r = converse_ladder(client, model_id, label=label, **kw)
                else:
                    r = client.converse(modelId=model_id, **kw)
                    log_usage(model_id, r["usage"], label)
                break
            except Exception as e:
                if "cachePoint" in str(e) and model_id not in _NO_CACHE:  # this model does not support caching: retry once without it
                    _NO_CACHE.add(model_id)
                    continue
                if attempt == 9 or "per day" in str(e) or not transient(e):
                    raise
                time.sleep(min(5 * 2 ** attempt, 120) + random.uniform(0, 5))  # capped backoff + jitter: parallel chunks and sibling services share one deployment's rate limit
        mine += LAST.get("usd", 0.0)
        msg = r["output"]["message"]
        messages.append(msg)
        uses = [b["toolUse"] for b in msg["content"] if "toolUse" in b]
        if r["stopReason"] != "tool_use" or not uses:  # a finished reply is returned even if its own cost crossed a cap: the work is already paid for
            return "".join(b.get("text", "") for b in msg["content"])
        budget.check()
        if call_cap_usd and mine > call_cap_usd:
            raise BudgetExceeded(f"agent call '{label}' spent ${mine:.2f}, over its per-call ceiling ${call_cap_usd:.2f}")
        messages.append({"role": "user", "content": [
            {"toolResult": {"toolUseId": u["toolUseId"], "content": [{"text": run_tool(u["name"], u["input"], write_roots, protected)}]}} for u in uses]})
    return "ERROR: agent hit the turn limit without finishing"
