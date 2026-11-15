# 07_transcript_sync — script, no model

YouTube blocks cloud IPs, so on the VM this goes through `yt_bridge.py`: videos already in the bank are handled offline; missing ones are posted as a job on the `yt-bridge` branch and a worker on a home-IP machine (`python3 00_GLOSSARY_PIPELINE_CORE/scripts/yt_bridge.py worker`) fetches them with `fetch_videos.py` and posts the result back. The run waits (up to 12 h; exit 4, `AWAITING MAC`). On a machine with a normal IP, `fetch_videos.py` can still be run directly.

```bash
python3 00_GLOSSARY_PIPELINE_CORE/scripts/yt_bridge.py transcripts batches/<batch_id> 00_GLOSSARY_PIPELINE_CORE/video_bank
```

For every kept candidate not already in `video_bank/catalogue/`: fetches metadata with `yt-dlp` (creator chapters, thumbnail, embed flag, language, caption tracks) into `catalogue/<video_id>.json`, and the English transcript (creator-uploaded preferred, auto-captions otherwise) into `transcripts/<video_id>.json`. Never downloads video. Already-cached videos are skipped — a video is fetched once, ever.

Outcomes: `fetched`, `already_cached`, `failed_no_captions` (every segment from that video will be rejected — README decision 4), `failed_fetch_error` (retried once; if many appear, YouTube is rate-limiting — wait and rerun, cached videos are skipped).

Gate: `update_ledger.py batches/<batch_id> record 07_transcript_sync transcript_sync_report.json PASS`
