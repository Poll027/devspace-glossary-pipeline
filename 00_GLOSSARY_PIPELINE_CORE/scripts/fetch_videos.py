"""07_transcript_sync: for every kept candidate video, cache its metadata and English transcript in the video bank.

Never downloads video. A video already in video_bank/catalogue/ is never fetched again (cost gate 6).
Needs yt-dlp on PATH.

Usage: python3 fetch_videos.py <batch_dir> <video_bank_dir>
  reads  batch_dir/video_candidates.json
  writes video_bank_dir/catalogue/<video_id>.json, video_bank_dir/transcripts/<video_id>.json,
         batch_dir/transcript_sync_report.json
"""
import json
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

from schema_check import validate

PACE_SECONDS = 2  # ponytail: fixed delay between network fetches; add proxy rotation only if 429s appear at volume
RETRY_WAIT_SECONDS = 20


def now():
    return datetime.now(timezone.utc).isoformat()


def ytdlp(*args, client=None):
    # ponytail: a single player client occasionally 429s on captions for one
    # video while the rest succeed; retry() below switches client, not just time.
    extra = ["--extractor-args", f"youtube:player_client={client}"] if client else []
    r = subprocess.run(["yt-dlp", "--no-warnings", *extra, *args], capture_output=True, text=True, timeout=180)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip().splitlines()[-1] if r.stderr.strip() else f"yt-dlp exit {r.returncode}")
    return r.stdout


def pick_track(meta):
    """Prefer a creator-uploaded English track over auto captions."""
    for lang in meta.get("subtitles") or {}:
        if lang.startswith("en") and lang != "live_chat":
            return lang, "creator_uploaded", "--write-subs"
    auto = meta.get("automatic_captions") or {}
    for lang in ("en-orig", "en"):
        if lang in auto:
            return lang, "auto_generated", "--write-auto-subs"
    return None


def parse_json3(raw):
    events = [e for e in json.loads(raw).get("events", []) if e.get("segs")]
    segments = []
    for i, e in enumerate(events):
        text = "".join(s.get("utf8", "") for s in e["segs"]).replace("\n", " ").strip()
        if not text:
            continue
        start = e["tStartMs"] / 1000
        end = start + e["dDurationMs"] / 1000 if "dDurationMs" in e else (
            events[i + 1]["tStartMs"] / 1000 if i + 1 < len(events) else start + 2)
        segments.append({"start_seconds": round(start, 2), "end_seconds": round(end, 2), "text": text})
    return segments


def fetch_one(video_id, bank, client=None):
    url = f"https://www.youtube.com/watch?v={video_id}"
    meta = json.loads(ytdlp("--skip-download", "--dump-single-json", url, client=client))
    track = pick_track(meta)
    segments, track_kind = [], None
    if track:
        lang, track_kind, flag = track
        with tempfile.TemporaryDirectory() as tmp:
            ytdlp("--skip-download", flag, "--sub-langs", lang, "--sub-format", "json3", "-o", f"{tmp}/%(id)s", url, client=client)
            files = list(Path(tmp).glob("*.json3"))
            if files:
                segments = parse_json3(files[0].read_text())
    tool = f"yt-dlp {ytdlp('--version').strip()}"

    if segments:
        transcript = {"video_id": video_id, "channel_id": meta["channel_id"], "fetched_at": now(), "fetch_tool": tool,
                      "caption_track_type": track_kind, "segments": segments}
        validate(transcript, "video_transcript.schema.json")
        (bank / "transcripts" / f"{video_id}.json").write_text(json.dumps(transcript))

    d = meta.get("upload_date") or ""
    entry = {
        "video_id": video_id, "youtube_url": url, "channel_id": meta["channel_id"], "title": meta.get("title", ""),
        "publish_date": f"{d[:4]}-{d[4:6]}-{d[6:]}" if len(d) == 8 else "",
        "duration_seconds": int(meta.get("duration") or 0), "language": meta.get("language"),
        "playable_in_embed": meta.get("playable_in_embed"),
        "caption_tracks": [{"lang": l, "kind": "creator"} for l in meta.get("subtitles") or {} if l != "live_chat"]
                          + [{"lang": l, "kind": "auto"} for l in ("en-orig", "en") if l in (meta.get("automatic_captions") or {})],
        "chapters": [{"title": c["title"], "start_seconds": c["start_time"], "end_seconds": c["end_time"]} for c in meta.get("chapters") or []],
        "thumbnail_urls": [meta["thumbnail"]] if meta.get("thumbnail") else [],
        "transcript_available": bool(segments), "fetched_at": now(), "fetch_tool": tool, "judged_ranges": [],
    }
    validate(entry, "video_catalogue_entry.schema.json")
    (bank / "catalogue" / f"{video_id}.json").write_text(json.dumps(entry, indent=2))
    return "fetched" if segments else "failed_no_captions"


def main(batch_dir, bank_dir):
    batch, bank = Path(batch_dir), Path(bank_dir)
    (bank / "catalogue").mkdir(exist_ok=True)
    (bank / "transcripts").mkdir(exist_ok=True)
    cands = json.loads((batch / "video_candidates.json").read_text())
    video_ids = sorted({c["video_id"] for s in cands["searches"] for c in s["candidates"] if c["filter_verdict"] == "kept"})

    results = []
    for i, vid in enumerate(video_ids):
        if (bank / "catalogue" / f"{vid}.json").exists():
            results.append({"video_id": vid, "outcome": "already_cached", "error_detail": None})
            continue
        if i:
            time.sleep(PACE_SECONDS)
        for attempt in (1, 2):
            try:
                client = "android" if attempt == 2 else None  # retry on a different client, not just after a wait
                results.append({"video_id": vid, "outcome": fetch_one(vid, bank, client=client), "error_detail": None})
                break
            except Exception as e:  # network/yt-dlp failure: record it, the batch continues without this video
                if attempt == 2:
                    results.append({"video_id": vid, "outcome": "failed_fetch_error", "error_detail": str(e)[:300]})
                else:
                    time.sleep(RETRY_WAIT_SECONDS)

    report = {
        "metadata": {
            "artifact_type": "transcript_sync_report", "artifact_version": "1.0.0", "schema_version": "1.0.0",
            "batch_id": cands["batch_id"], "run_id": cands["batch_id"], "prompt_version": "n/a-deterministic",
            "model": "deterministic/fetch_videos.py", "generated_at": now(), "source_snapshot_id": cands["batch_id"],
            "parent_artifact_hashes": {},
        },
        "batch_id": cands["batch_id"], "results": results,
    }
    validate(report, "transcript_sync_report.schema.json")
    (batch / "transcript_sync_report.json").write_text(json.dumps(report, indent=2))
    counts = {}
    for r in results:
        counts[r["outcome"]] = counts.get(r["outcome"], 0) + 1
    print(f"{len(results)} videos: {counts}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(*sys.argv[1:])
