"""LLM plumbing shared by the driver, the agent loop and the supervisor: client, model ladders, pricing, cost log, alerts.
Role-agnostic. Generalised from the glossary pack's glm_generate.py (stage-08 code dropped). (File name kept from the Bedrock days.)

Provider: LLM_PROVIDER=azure (default; Azure OpenAI / Foundry via llm_azure.py, deployment names as model ids) or bedrock (boto3, legacy).
Env: GEN_LADDER / EVAL_LADDER (comma lists of model ids / deployment names), PRICE_GEN / PRICE_EVAL ("in,out" USD per million tokens, overrides the table),
     COST_LOG (set by Budget), QUOTA_STATE, QUOTA_COOLDOWN_H, NOTIFY_WEBHOOK_URL, AZURE_OPENAI_ENDPOINT / AZURE_OPENAI_API_KEY (see llm_azure.py).
Prices come from 00_FINAL_PIPELINE_CORE/model_prices.json (matched by name substring; unknown models get the most expensive rate).
"""
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

DEFAULT_LADDERS = {  # deployment names in Foundry; provisional until the bake-off picks models (override with GEN_LADDER / EVAL_LADDER)
    "GEN": ["gpt-6.1-sol"],
    # evaluators stay top-tier: when a rung is out of quota the run waits instead of silently getting a weaker gate
    "EVAL": ["gpt-6-astra"],
}
USED, LAST = set(), {}  # models called in this process / the latest call's model and cost
_WARNED = set()  # models already reported as missing from the price table
_MEM = {}  # quota block list when no QUOTA_STATE file is configured


def load_env():
    """Read the gitignored .env (KEY=value lines); real env vars win."""
    if (ROOT / ".env").exists():
        for ln in (ROOT / ".env").read_text().splitlines():
            if "=" in ln and not ln.lstrip().startswith("#"):
                k, v = ln.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip("'\""))


def make_client():
    load_env()
    if os.environ.get("LLM_PROVIDER", "azure") == "bedrock":  # legacy path; boto3 is no longer in requirements.txt
        import boto3
        from botocore.config import Config
        region = os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION") or "us-east-1"
        return boto3.client("bedrock-runtime", region_name=region,
                            config=Config(retries={"max_attempts": 6, "mode": "standard"}, read_timeout=300, connect_timeout=20))
    from llm_azure import AzureClient
    return AzureClient()


def rates(model):
    """The price-table entry whose key is the longest substring of the model's name; unknown models cost the table's default (the dearest)."""
    t, m = json.loads(next(q for q in (ROOT / "00_GLOSSARY_PIPELINE_CORE" / "model_prices.json", ROOT / "00_FINAL_PIPELINE_CORE" / "model_prices.json") if q.exists()).read_text()), model.lower()
    for k in sorted(t["models"], key=len, reverse=True):
        if k in m:
            return t["models"][k]
    if model not in _WARNED:
        _WARNED.add(model)
        warn(f"no price entry matches '{model}': costing it at the table default; add it to model_prices.json")
    return t["default"]


def price_usd(model, usage):
    r = rates(model)
    pin, pout = r["in"], r["out"]
    role = "EVAL" if model in ladder("EVAL") else "GEN"
    if os.environ.get(f"PRICE_{role}"):
        pin, pout = (float(x) for x in os.environ[f"PRICE_{role}"].split(","))
    flex = 0.5 if usage.get("serviceTier") == "flex" else 1.0  # Azure price list: every GPT-6 Flex meter is half its Standard meter
    return flex * ((usage.get("inputTokens", 0) + r["cache_read"] * usage.get("cacheReadInputTokens", 0) + r["cache_write"] * usage.get("cacheWriteInputTokens", 0)) / 1e6 * pin
                   + usage.get("outputTokens", 0) / 1e6 * pout)


def log_usage(model, usage, label=""):
    """Append the call's estimated cost to $COST_LOG so every caller's spend is counted. Returns the USD."""
    usd = round(price_usd(model, usage), 4)
    LAST["usd"] = usd
    p = os.environ.get("COST_LOG")
    if p:
        with open(p, "a") as f:
            f.write(json.dumps({"t": datetime.now(timezone.utc).isoformat(timespec="seconds"), "model": model, "label": label or Path(sys.argv[0]).name,
                                "tier": usage.get("serviceTier", "default"), "in": usage.get("inputTokens", 0), "cache_read": usage.get("cacheReadInputTokens", 0), "cache_write": usage.get("cacheWriteInputTokens", 0), "out": usage.get("outputTokens", 0), "usd": usd}) + "\n")
    return usd


def ladder(role):
    v = os.environ.get(f"{role}_LADDER")
    return [x.strip() for x in v.split(",") if x.strip()] if v else DEFAULT_LADDERS[role]


def _state():
    p = os.environ.get("QUOTA_STATE")
    if not p:
        return _MEM
    try:
        return json.loads(Path(p).read_text())
    except (OSError, ValueError):
        return {}


def _put_state(st):
    p = os.environ.get("QUOTA_STATE")
    if p:
        Path(p + ".tmp").write_text(json.dumps(st))
        os.replace(p + ".tmp", p)


def _block(model, hours):
    st = _state()
    st[model] = time.time() + hours * 3600
    _put_state(st)


def warn(msg):
    print(f"[ladder] {msg}", file=sys.stderr, flush=True)


def alert(subject, body):
    """POST a notification to NOTIFY_WEBHOOK_URL (Slack/Discord-style JSON). No webhook configured: do nothing. Never raises."""
    url = os.environ.get("NOTIFY_WEBHOOK_URL")
    if not url:
        return
    try:
        import urllib.request
        text = f"*{subject}*\n{body[:3500]}"
        urllib.request.urlopen(urllib.request.Request(url, json.dumps({"text": text, "content": text[:1900]}).encode(), {"Content-Type": "application/json"}), timeout=15)
    except Exception as e:
        warn(f"alert failed: {e}")


def converse_ladder(client, role, label="", **kw):
    """Converse on the first model of the role's ladder that is not quota-blocked. A daily-token-quota error blocks that model for
    QUOTA_COOLDOWN_H hours (default 1); the call moves to the next rung. All blocked: wait and re-probe."""
    announced = False
    while True:
        st, now = _state(), time.time()
        free = [m for m in ladder(role) if st.get(m, 0) <= now]
        if not free:
            wake = min(st.get(m, 0) for m in ladder(role))
            warn(f"all {role} models are out of quota; waiting until {time.strftime('%H:%M', time.localtime(wake))}")
            key = f"__announced_{role}"  # one notification per role per 6h across processes
            if not announced and now - st.get(key, 0) > 6 * 3600:
                announced = True
                st[key] = now
                _put_state(st)
                alert(f"Final pipeline waiting on {role} quota", f"All {role} models are out of daily quota. The run waits and retries automatically.")
            time.sleep(min(max(wake - now, 5), 600))
            continue
        m = free[0]
        try:
            r = client.converse(modelId=m, **kw)
        except Exception as e:
            s = str(e)
            if "per day" in s:
                _block(m, float(os.environ.get("QUOTA_COOLDOWN_H", 1)))
                warn(f"{m}: daily quota hit, falling back")
                continue
            if "not available for this account" in s or "AccessDenied" in type(e).__name__ or "DeploymentNotFound" in s:
                _block(m, 24)
                warn(f"{m}: no access on this account, skipping for 24h")
                continue
            raise
        USED.add(m)
        LAST["model"] = m
        log_usage(m, r["usage"], label)
        return r
