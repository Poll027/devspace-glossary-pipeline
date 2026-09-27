"""10_media_selection: approved judgments -> selected_media.json. Deterministic; no model involved.

Per (concept, path): skip if video_need is LOW/NONE; otherwise greedily pick approved segments that cover
required facts not yet covered, best first (mean score, then channel trust tier, then shorter clip).

Usage: python3 select_media.py <batch_dir> <video_bank_dir>
  reads  batch_dir/{coverage_briefs,glossary_pass_a,segment_proposals,segment_judgments}.json
         video_bank_dir/channel_allowlist.json, video_bank_dir/catalogue/<video_id>.json
  writes batch_dir/selected_media.json
"""
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from schema_check import validate

MAX_SEGMENTS = 3  # ponytail: fixed cap per concept; tune from Phase 1 pilot data (playbook §34)
TRUST_RANK = {"high": 0, "standard": 1}


def load(p):
    return json.loads(Path(p).read_text())


def youtube_url(video_id):
    return f"https://www.youtube.com/watch?v={video_id}"


def review_url(video_id, start):
    return f"https://www.youtube.com/watch?v={video_id}&t={start}s"


def overlaps(a, b):
    return a["video_id"] == b["video_id"] and a["start_seconds"] < b["end_seconds"] and b["start_seconds"] < a["end_seconds"]


def select(briefs, pass_a, proposals, judgments, trust_by_channel, channel_by_video):
    need = {(e["concept_id"], e["path_id"]): e["video_need"]["level"] for e in pass_a["entries"]}
    props = {p["proposal_id"]: p for p in proposals["proposals"]}
    approved = {}
    for j in judgments["judgments"]:
        if j["verdict"] != "approved":
            continue
        p = props[j["proposal_id"]]
        start, end = j["final_start_seconds"], j["final_end_seconds"]
        channel = channel_by_video[p["video_id"]]
        approved.setdefault((p["concept_id"], p["path_id"]), []).append({
            # concept is part of the identity: fact_ids and summary are concept-scoped, so one clip serving
            # two concepts is two records. Same concept + same cut in another path -> same id -> reuse.
            "segment_id": f"seg_{p['concept_id']}_{p['video_id']}_{start}_{end}",
            "label": p["label"], "video_id": p["video_id"], "channel_id": channel,
            "youtube_url": youtube_url(p["video_id"]), "review_url": review_url(p["video_id"], start),
            "start_seconds": start, "end_seconds": end,
            "fact_ids": j["confirmed_fact_ids"], "transcript_ref": f"{p['video_id']}:{start}-{end}",
            "visual_mode": p["visual_mode"], "role": p["role"],
            "mean_score": round(sum(j["scores"].values()) / len(j["scores"]), 2),
        })

    rows = []
    for b in briefs["briefs"]:
        key = (b["concept_id"], b["path_id"])
        required = [f["id"] for f in b["evidence"]["required_facts"]]
        row = {"concept_id": key[0], "path_id": key[1], "segments": [], "uncovered_fact_ids": required}
        if need.get(key) in (None, "LOW", "NONE"):
            rows.append({**row, "media_status": "no_video_needed"})
            continue
        ranked = sorted(approved.get(key, []), key=lambda s: (
            -s["mean_score"], TRUST_RANK.get(trust_by_channel.get(s["channel_id"]), 2), s["end_seconds"] - s["start_seconds"]))
        covered, picked = set(), []
        for s in ranked:
            if len(picked) == MAX_SEGMENTS:
                break
            if set(s["fact_ids"]) - covered and not any(overlaps(s, x) for x in picked):
                picked.append(s)
                covered |= set(s["fact_ids"])
        rows.append({**row, "media_status": "selected" if picked else "no_segment_found", "segments": picked,
                     "uncovered_fact_ids": [f for f in required if f not in covered]})
    return rows


def main(batch_dir, bank_dir):
    batch_dir, bank_dir = Path(batch_dir), Path(bank_dir)
    names = ["coverage_briefs", "glossary_pass_a", "segment_proposals", "segment_judgments"]
    briefs, pass_a, proposals, judgments = (load(batch_dir / f"{n}.json") for n in names)
    trust = {c["channel_id"]: c["trust_tier"] for c in load(bank_dir / "channel_allowlist.json")["channels"]}
    videos = {p["video_id"] for p in proposals["proposals"]}
    channel_by_video = {v: load(bank_dir / "catalogue" / f"{v}.json")["channel_id"] for v in videos}

    rows = select(briefs, pass_a, proposals, judgments, trust, channel_by_video)
    out = {
        "metadata": {
            "artifact_type": "selected_media", "artifact_version": "1.0.0", "schema_version": "1.0.0",
            "batch_id": briefs["batch_id"], "run_id": briefs["batch_id"], "prompt_version": "n/a-deterministic",
            "model": "deterministic/select_media.py", "generated_at": datetime.now(timezone.utc).isoformat(),
            "source_snapshot_id": briefs["batch_id"],
            "parent_artifact_hashes": {f"{n}.json": hashlib.sha256((batch_dir / f"{n}.json").read_bytes()).hexdigest() for n in names},
        },
        "batch_id": briefs["batch_id"],
        "selections": rows,
    }
    validate(out, "selected_media.schema.json")
    (batch_dir / "selected_media.json").write_text(json.dumps(out, indent=2))
    counts = {}
    for r in rows:
        counts[r["media_status"]] = counts.get(r["media_status"], 0) + 1
    print(f"wrote {len(rows)} selections {counts}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(*sys.argv[1:])
