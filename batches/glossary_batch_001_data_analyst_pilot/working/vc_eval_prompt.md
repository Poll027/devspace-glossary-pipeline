Pack root (run every command from here): `/Users/folajuwon/Downloads/Telegram Desktop/UNIVERSAL_GLOSSARY_PIPELINE_PACK`

Stage `06_video_candidates`. Your instructions are in `01_GLOSSARY_PACK_TEMPLATE/06_video_candidates/EVALUATOR.md`. Also read `GENERATOR.md` in the same folder and playbook §10-12 (`00_GLOSSARY_PIPELINE_CORE/PLAYBOOK_v3.md`, ~lines 900-1024).

Batch folder: `batches/glossary_batch_001_data_analyst_pilot/`. Evaluate `video_candidates.part.{CHUNK}.json` ({DESC}) against:
- `glossary_pass_a.json`: confirm the chunk's output covers exactly the concepts whose video_need.level is HIGH or MEDIUM in this chunk, and no others.
- `extracted_concepts.json`

**Real videos only.** For every allowlist candidate, confirm the video_id exists in its channel's catalogue file (`00_GLOSSARY_PIPELINE_CORE/video_bank/channel_catalogs/<channel_id>.json`) — write a small script, don't eyeball it. For every open-search candidate, confirm it resolves: `yt-dlp --skip-download --get-title "https://www.youtube.com/watch?v=<id>"`. An id that doesn't resolve, or isn't in its catalogue, is BLOCKING.

**Routing.** Open search should only appear where the allowlist genuinely came up short — spot-check a few of those concepts yourself with `search_catalogs.py` using different keywords than the generator tried, to see if it missed an obvious allowlist match.

**Filter quality.** Kept candidates should plausibly contain this concept at this level from their title/channel/duration alone. Nothing kept should be news, commentary or entertainment. Rejection reasons should be specific, not boilerplate. A big channel's loosely-related video must not outrank a precise smaller-channel match — check this isn't happening.

**Search brief quality.** `required_fact_ids` should match the concept's actual coverage-brief facts. `blocked_concepts_to_avoid` should be a short, specific list, not padding.

End with `VERDICT: PASS|FAIL` and one line per defect in the BLOCKING/ADVISORY format from your agent file.
