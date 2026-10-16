Pack root (run every command from here): `/Users/folajuwon/Downloads/Telegram Desktop/UNIVERSAL_GLOSSARY_PIPELINE_PACK`

Stage `06_video_candidates`: find candidate teaching videos for concepts whose text needs visual support.

**Read first:**
- `01_GLOSSARY_PACK_TEMPLATE/06_video_candidates/GENERATOR.md`.
- Playbook §10–12 in `00_GLOSSARY_PIPELINE_CORE/PLAYBOOK_v3.md` (around lines 900–1024): the search brief shape, the search prompt, and the cheap filter rules.

**Inputs**, in batch folder `batches/glossary_batch_001_data_analyst_pilot/`:
- `glossary_pass_a.json`: gated. Only search for concepts whose `video_need.level` is `HIGH` or `MEDIUM`. Skip LOW and NONE entirely — they get no entry in your output at all.
- `extracted_concepts.json`: for blocked_knowledge_ids (pick the few a video on this topic would likely drift into, not the whole list) and the path's `learner_scope`.
- `registry_lookup.json`: all `new` — no reused segments exist yet for this batch. `00_GLOSSARY_PIPELINE_CORE/video_bank/approved_segments.json` is also empty, so skip the "reused segments" routing step entirely; every search_route will be `allowlist_only` or `allowlist_then_open_search`.

**Search tool — use this, don't read catalogue files directly:**
```bash
python3 00_GLOSSARY_PIPELINE_CORE/scripts/search_catalogs.py "<keywords>" --limit 20
```
It searches all 43 allowlisted channels' catalogues (31,766 videos total) by title keyword and prints one JSON line per match, ranked by hit count then channel trust tier. Try 2-3 keyword variations per concept (e.g. the concept name, then a more specific fact-level term) before concluding the allowlist has nothing. `career_family_ids` on a result is a ranking hint, not a filter — a video tagged `software_engineer` can still be the right match for a `data_analytics` concept (e.g. general Python/pandas channels).

**Open search fallback:** only when the allowlist search gives fewer than 2 plausible candidates after trying a few keyword variations. Use WebSearch for `site:youtube.com <query>` or similar, with the field's standard wording for the concept (e.g. "ask prepare process analyze share act" for the data-analysis lifecycle, "data quality dimensions" rather than an invented phrase). Every `video_id` must come from a real result URL you saw — never invent or guess one.

**Before keeping any open-search candidate, check two things beyond the title** (the canary found both of these catch real problems title alone misses):
1. Its description and chapters: `yt-dlp --skip-download --print "%(description)s %(chapters)s" "https://www.youtube.com/watch?v=<id>"`. A title can look right while the description shows the video is actually about something else (e.g. a research-methods course that happens to use the word "analysis").
2. The channel's recent output: `yt-dlp --skip-download --flat-playlist --playlist-end 20 --print "%(title)s" "https://www.youtube.com/channel/<channel_id>/videos"`. **Exclude any channel whose recent uploads are mostly news, industry commentary, founder/career advice, or non-English content** — this is the same teaching-channels-only rule the allowlist itself was built on (Fireship was excluded for news/reporting over depth; Luke Barousse was excluded because about 69 of 80 videos were career advice or hype, even though some were real tutorials). **This check is about the channel, not the one video you found.** A single video with teaching chapters, pulled from a channel whose other uploads are career-change stories, portfolio tips, interview prep or "how AI will change your career" content, still fails this check — that channel is advice-flavored, and this candidate doesn't get an exception for it. Decide, don't caveat.

Every `reason` may only cite what you actually saw in the title, description, chapters or channel check — never a plausible-sounding detail you didn't verify (e.g. don't say "Education-category channel" when yt-dlp shows no category field).

**Output:** `batches/glossary_batch_001_data_analyst_pilot/video_candidates.part.{CHUNK}.json`, a full `video_candidates.schema.json` document covering only the HIGH/MEDIUM concepts in chunk `{CHUNK}` from `chunks.json` ({DESC}). Metadata:
- batch_id `glossary_batch_001_data_analyst_pilot`
- model `claude-sonnet-5`
- prompt_version `06_video_candidates@v1`
- source_snapshot_id `data_analytics.source_pack`
- parent_artifact_hashes = sha256 of glossary_pass_a.json, extracted_concepts.json and registry_lookup.json
- generated_at = real UTC time

For each concept: build the `search_brief` (concept_name, learner_level from path's learner_scope, required_fact_ids from the concept's coverage brief, preferred_visual_modes from glossary_pass_a's video_need, blocked_concepts_to_avoid — the few likely drift targets), run the search, apply the cheap filter (title/channel/duration only — reject wrong topic, wrong level, news/opinion/entertainment, obviously obsolete tool versions), keep at most 5 candidates, give every kept and rejected candidate a specific `reason`. Build `youtube_url` from `video_id`, never paste one. Set `search_route` accurately.

Validate: `python3 00_GLOSSARY_PIPELINE_CORE/scripts/schema_check.py video_candidates.schema.json <your part file>`.

Reply briefly: concept count, candidates found vs. none-found, how many needed open search and why, anything you were unsure of.
