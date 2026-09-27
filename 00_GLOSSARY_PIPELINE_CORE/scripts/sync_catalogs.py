"""Video-bank maintenance (not a per-batch stage): list every upload of every allowlisted channel into
video_bank/channel_catalogs/<channel_id>.json. One request per channel, no YouTube API key, no quota.

Run after the allowlist grows, or occasionally to pick up new uploads.

Usage: python3 sync_catalogs.py <video_bank_dir> [channel_id ...]   (no ids = every allowlisted channel)
"""
import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from schema_check import validate


def sync(channel_id, out_dir):
    raw = subprocess.run(
        ["yt-dlp", "--no-warnings", "--flat-playlist", "--dump-single-json", f"https://www.youtube.com/channel/{channel_id}/videos"],
        capture_output=True, text=True, timeout=300, check=True).stdout
    entries = [e for e in json.loads(raw).get("entries", []) if e.get("id")]
    catalog = {
        "channel_id": channel_id,
        "synced_at": datetime.now(timezone.utc).isoformat(),
        # flat listing gives no description/date; 07_transcript_sync fetches full metadata only for candidates
        "videos": [{"video_id": e["id"], "title": e.get("title") or "", "description": None,
                    "duration_seconds": int(e.get("duration") or 0), "published_at": None} for e in entries],
    }
    validate(catalog, "channel_video_catalog.schema.json")
    (out_dir / f"{channel_id}.json").write_text(json.dumps(catalog, indent=2))
    return len(catalog["videos"])


def main(bank_dir, ids):
    bank = Path(bank_dir)
    out = bank / "channel_catalogs"
    out.mkdir(exist_ok=True)
    allow = json.loads((bank / "channel_allowlist.json").read_text())["channels"]
    targets = ids or [c["channel_id"] for c in allow]
    for i, cid in enumerate(targets):
        if i:
            time.sleep(2)
        for attempt in (1, 2):  # YouTube returns transient 400/429s at volume; one retry clears most
            try:
                print(f"{cid}: {sync(cid, out)} videos", flush=True)
                break
            except subprocess.CalledProcessError as e:
                if attempt == 2:
                    print(f"{cid}: FAILED {e.stderr.strip().splitlines()[-1] if e.stderr else e}", flush=True)
                else:
                    time.sleep(20)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2:])
