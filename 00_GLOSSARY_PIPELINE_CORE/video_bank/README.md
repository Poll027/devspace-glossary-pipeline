# Video Bank

Cross-batch, fetched-once assets. Nothing here is regenerated per batch.

| Path | What | Written by |
|---|---|---|
| `channel_allowlist.json` | Trusted teaching channels, with verified stats and trust tier | `CHANNEL_DISCOVERY_GENERATOR.md` + `_EVALUATOR.md`, run occasionally |
| `channel_catalogs/<channel_id>.json` | Every upload of each allowlisted channel (id, title, duration) | `scripts/sync_catalogs.py` — one request per channel, no API quota |
| `catalogue/<video_id>.json` | Full metadata for every video that was ever a candidate: chapters, thumbnail, embed flag, caption tracks, and every range already judged | `scripts/fetch_videos.py` (stage 07); `judged_ranges` from `merge_registry.py` |
| `transcripts/<video_id>.json` | Timestamped English transcript | `scripts/fetch_videos.py` |
| `approved_segments.json` | Every segment that shipped in an audited batch, reusable by any path teaching the same concept | `scripts/merge_registry.py` (stage 16b) |

Copy `approved_segments.EMPTY_TEMPLATE.json` → `approved_segments.json` before the first batch.

## Rules

- **Teaching channels only.** News, commentary and founder-advice channels are excluded, however big (Fireship, Matt Wolfe and Y Combinator were rejected on this basis). So are non-English channels.
- **`career_family_ids` is a ranking hint, not a filter.** Stage 06 searches every catalogue. Most channels are currently tagged `software_engineer` from the first discovery run; re-tag them to the real path families as batches run.
- **No downloads.** `yt-dlp` runs with `--skip-download` only. Visual quality is judged from chapters, thumbnail and transcript cues (README decision 2).
- **Fetched once.** A video already in `catalogue/` is never fetched again, whichever batch or concept wants it.
- Fetching needs `yt-dlp` on PATH. It reads the same public caption data a browser does; it doesn't use the official API, whose caption download only works for your own channel. At volume, pace requests (built in) and rerun on rate limits — cached videos are skipped.
