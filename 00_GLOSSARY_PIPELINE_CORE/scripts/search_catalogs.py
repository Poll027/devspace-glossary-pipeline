#!/usr/bin/env python3
"""Keyword search over the channel video catalogues, for stage 06.

Usage:
  python3 search_catalogs.py "pandas groupby" [--limit 20] [--channel-ids UC1,UC2]

Prints one JSON line per match (ranked by keyword-hit count, then channel
trust_tier), each with video_id, title, channel_id, channel_name,
duration_seconds, career_family_ids. Doesn't read every catalogue into an
agent's context — run this as a subprocess and read only the output.
"""
import json
import re
import sys
from pathlib import Path

CORE = Path(__file__).resolve().parent.parent
CATALOGS = CORE / "video_bank" / "channel_catalogs"
ALLOWLIST = CORE / "video_bank" / "channel_allowlist.json"

TRUST_RANK = {"high": 0, "medium": 1, "low": 2}


def load_allowlist():
    d = json.load(open(ALLOWLIST))
    chans = d.get("channels", d if isinstance(d, list) else [])
    return {c["channel_id"]: c for c in chans}


def tokenize(q):
    # "A/B" testing loses both letters under a plain len>1 alnum filter
    # (each side of the slash is a single character), so normalize the
    # common "a/b" pattern into one word before splitting on alnum runs.
    q = re.sub(r"\ba\s*/\s*b\b", "ab", q.lower())
    return [t for t in re.findall(r"[a-z0-9]+", q) if len(t) > 1]


def main():
    if len(sys.argv) < 2:
        print("usage: search_catalogs.py '<query words>' [--limit N] [--channel-ids UC1,UC2]", file=sys.stderr)
        sys.exit(1)
    args = sys.argv[1:]
    query = args[0]
    limit = 20
    channel_filter = None
    i = 1
    while i < len(args):
        if args[i] == "--limit":
            limit = int(args[i + 1]); i += 2
        elif args[i] == "--channel-ids":
            channel_filter = set(args[i + 1].split(",")); i += 2
        else:
            i += 1

    terms = tokenize(query)
    if not terms:
        sys.exit(0)
    phrase = re.sub(r"\ba\s*/\s*b\b", "ab", query.lower().strip())

    allowlist = load_allowlist()
    results = []
    for f in sorted(CATALOGS.glob("*.json")):
        cid = f.stem
        if channel_filter and cid not in channel_filter:
            continue
        meta = allowlist.get(cid, {})
        chan_name = meta.get("channel_name", cid)
        trust = meta.get("trust_tier", "medium")
        families = meta.get("career_family_ids", [])
        try:
            d = json.load(open(f))
        except Exception:
            continue
        for v in d.get("videos", []):
            title = (v.get("title") or "")
            title_l = re.sub(r"\ba\s*/\s*b\b", "ab", title.lower())
            matched = sum(1 for t in terms if t in title_l)
            if matched == 0:
                continue
            all_terms = matched == len(terms)
            phrase_bonus = 1 if phrase in title_l else 0
            # Rank full-term matches first, then phrase hits, then partial
            # matches by how many terms they got — a single stray word
            # ("data") must not bury a video that matches every word.
            hits = (100 if all_terms else 0) + phrase_bonus * 10 + matched
            results.append({
                "hits": hits,
                "trust_rank": TRUST_RANK.get(trust, 1),
                "video_id": v.get("video_id"),
                "title": title,
                "channel_id": cid,
                "channel_name": chan_name,
                "duration_seconds": v.get("duration_seconds"),
                "career_family_ids": families,
            })

    results.sort(key=lambda r: (-r["hits"], r["trust_rank"]))
    for r in results[:limit]:
        r.pop("trust_rank", None)
        print(json.dumps(r, ensure_ascii=False))


if __name__ == "__main__":
    main()
