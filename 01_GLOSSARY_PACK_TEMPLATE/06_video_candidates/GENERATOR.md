# 06_video_candidates — GENERATOR

Produce `video_candidates.json` for every `glossary_pass_a.json` entry whose `video_need.level` is `HIGH` or `MEDIUM`. Skip the rest. Read playbook §10–12 and the §28.2 prompt. Work tile by tile — adjacent concepts often come from the same video (cost gate 7).

**Search brief** per concept (§10): concept name, the path's `learner_scope` as level, required fact ids, `preferred_visual_modes`, and the handful of blocked concepts a video on this topic would likely drift into.

**Routing — cheapest first:**
1. **Reused segments.** Videos behind `registry_lookup.json` `reusable_segment_ids` → candidates with `found_via: "reused_segment"`.
2. **Allowlist catalogues.** Search every `00_GLOSSARY_PIPELINE_CORE/video_bank/channel_catalogs/*.json` by title (write a small script over the files; don't read them all into context). A channel's `career_family_ids` is a ranking hint, not a filter. `found_via: "allowlist_catalogue"`.
3. **Open search — only when steps 1–2 yield fewer than 2 plausible candidates.** Search YouTube via WebSearch. Every candidate's `video_id` must be copied from a real result URL — never constructed or recalled. Exclude news, commentary, founder-advice and non-English channels. `found_via: "open_search"`. Set `search_route` to show whether open search was used.

**Cheap filter** (§12) from title, channel and duration only: reject wrong topic or level, obvious news/opinion/entertainment, videos whose title signals advanced material the learner hasn't reached, and clearly obsolete versions of version-sensitive tools. Keep at most 5 per concept (cost gate 5). Every candidate — kept or rejected — gets a `reason`.

`youtube_url` is `https://www.youtube.com/watch?v=<video_id>` — build it from the id, don't paste it.

Validate: `schema_check.py video_candidates.schema.json batches/<batch_id>/video_candidates.json`
