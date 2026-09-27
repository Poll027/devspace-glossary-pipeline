# 11_reconciliation — GENERATOR

Produce `glossary_bundles_draft.json`: one full Glossary Learning Bundle (`schemas/glossary_learning_bundle.schema.json`) per (concept, path). Read playbook §18–23 and the §28.4 prompt; the §8 Data Cleaning "video match" table is the model for this stage.

**Start from** the concept's Pass A entry and its `selected_media.json` row. For concepts with media, open each selected segment's transcript range.

**Reconcile text and video** (§18). Build the coverage matrix in your head, per fact: text covers it / video covers it / action. Then:
- Approved evidence beats the video. If the creator uses a valid synonym, keep Devspace's term and bridge it.
- Where the video demonstrates something well, trim repeated prose — but the text must still teach every required fact on its own, because some learners won't watch.
- Fill every gap the video leaves. Never leave a required fact uncovered.
- Keep Pass A's quality: coherent prose at the §8 benchmark, no mention of any video.

**Media group** (§17, §19–20), only when `media_status` is `selected`:
- Copy every segment field from `selected_media.json` exactly: `segment_id`, `video_id`, `youtube_url`, `review_url`, `start_seconds`, `end_seconds`, `fact_ids`, `transcript_ref`. Never retype, round, or "fix" them.
- Write each segment's `summary` in Devspace's voice: an accurate read-alternative of that range that makes sense alone. Don't copy the transcript.
- `label` may be sharpened into Devspace terms. Write a `group_title`, and a `bridge_note` with `before` (why this clip, what to watch for) and `after` (the takeaway, or the gap Devspace fills).
- `media: null` for `no_video_needed` and `no_segment_found`.

**Anchors** (§21–23) — define what can be checked and practised; never write question text:
- `assessment_anchors` from the TOC's `assessment_target`, each tied to fact ids, with a snake_case `capability`.
- `practice_anchor` from `practice_objective`, typed to the concept (`live_code` for coding paths, with `allowed_syntax`/`blocked_syntax` drawn from the boundary; `spreadsheet`, `ordering`, `field_selection`, etc. elsewhere). Achievable with taught knowledge only.
- `visual_anchor`: what must become visible (a messy data table, a join diagram, a UI state), or null.

**Context and coverage** come from `extracted_concepts.json` and the coverage brief — copied, not rewritten. `cluster_ref: null` (set at assembly). Set the four `validation` flags honestly; `ready_for_final_schema: true` only when you believe all checks pass.

Validate: `schema_check.py glossary_bundles_draft.schema.json batches/<batch_id>/glossary_bundles_draft.json`
