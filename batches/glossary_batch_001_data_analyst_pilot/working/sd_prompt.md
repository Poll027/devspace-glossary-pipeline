Pack root (run every command from here): `/Users/folajuwon/Downloads/Telegram Desktop/UNIVERSAL_GLOSSARY_PIPELINE_PACK`

Stage `08_segment_detection`: for each video you're assigned, find the best standalone timestamp range for every concept it's a candidate for. There is no evaluator for this stage's own round — `09_segment_judge` independently re-checks every proposal in a fresh context, so propose honestly rather than optimistically; a rejected proposal costs nothing, a bad one that gets approved reaches a learner.

**Read first:**
- `01_GLOSSARY_PACK_TEMPLATE/08_segment_detection/GENERATOR.md`.
- Playbook §14-16 (segment boundaries, duration targets, video-quality rules) and §28.3 (the detector prompt) in `00_GLOSSARY_PIPELINE_CORE/PLAYBOOK_v3.md`, lines ~1073-1175 and ~1715-1752.
- §25 (lines ~1478-1498) if any of your videos came from a reused segment (check `registry_lookup.json` — in this batch everything is `new`, so this won't apply).

**Inputs**, in batch folder `batches/glossary_batch_001_data_analyst_pilot/`:
- `video_candidates.json`: tells you which concepts each video is a kept candidate for.
- `coverage_briefs.json`: each concept's required facts (what `covered_fact_ids` must reference) and sources.
- `extracted_concepts.json`: each concept's `blocked_knowledge_ids` (check by name, not just id — a passing mention the learner can follow is fine; needing to understand it is not) and `allowed_knowledge_ids`.
- `glossary_pass_a.json`: each concept's `video_need` (role hint: the duration targets differ by role) and `teaching_notes`.
- `00_GLOSSARY_PIPELINE_CORE/video_bank/catalogue/<video_id>.json`: chapters, `playable_in_embed`, duration.
- `00_GLOSSARY_PIPELINE_CORE/video_bank/transcripts/<video_id>.json`: the timestamped transcript. **Read this, not just the chapter list** — a prior stage caught an auto-generated chapter list that completely misrepresented a video's actual content.

**Your assigned videos** for chunk `{CHUNK}`: see `batches/glossary_batch_001_data_analyst_pilot/chunks_08.json`, key `{CHUNK}`. For each video_id in that list, look up every concept it's a kept candidate for in `video_candidates.json`.

**For each (video, concept) pair:**
1. Check `catalogue/<video_id>.json`: if `playable_in_embed` is `false`, or there's no matching transcript file, add it to `rejected_videos` with that reason. Don't propose a range.
2. Read the transcript around the video's chapters, and judge whether the video actually covers this concept well enough to propose a range at all. If not, add it to `rejected_videos` with a specific reason (not generic).
3. If it does, find the best standalone range per §14: starts on a new thought (ideally a chapter boundary), explains itself immediately, needs no earlier context, covers the facts it claims, finishes its example, ends before the next topic or any blocked concept.
4. Pick a `role` (mental_model / visual_mechanism / worked_example / live_code_demo / tool_workflow) and keep the range inside its duration band from §15 unless you have a real reason not to.
5. Write the proposal: `proposal_id` (unique, e.g. `prop_<video_id>_<short_concept_name>`), `concept_id`, `path_id` (`data_analyst`), `video_id`, `start_seconds`, `end_seconds` (integers), `label` (what the learner is about to watch, in Devspace terms — not the video's own title), `role`, `covered_fact_ids` (only facts this range actually teaches), `visual_mode` (your inference — chapter titles, thumbnail, transcript cues like "let me draw" or "as you can see"), `chapter_aligned` (true if start sits on a chapter marker), `transcript_evidence` (a real quote copied from inside the range — not paraphrased, not from outside it), `issues` (any doubts; empty array if none).

A long, well-chaptered video can supply ranges for several of its concepts — propose one per concept, not one overall.

**Lessons from the canary:**
- Don't pre-trim a fact-bearing sentence just to stay inside the duration band — if cutting a range short mid-sentence drops a fact the concept needs, extend it (unless that extension would leak a blocked concept) and let the judge decide if it's too long. A canary proposal clipped a video's own sentence completing a required fact, purely to hit the duration target.
- When you say a cut's start/end avoids a specific line ("ends before X is said"), double-check that line's actual timestamp in the transcript — don't estimate. Two canary proposals were off by a few seconds (a referenced line was still inside the claimed-clean cut; trailing music/outro started earlier than claimed).
- If the video itself states something factually wrong or contradicts a required fact (not just omits one), say so explicitly in `issues` — this is different from a coverage gap, and the judge needs to know to reject on accuracy grounds, not just trim.

**Output:** `batches/glossary_batch_001_data_analyst_pilot/segment_proposals.part.{CHUNK}.json`, a full `segment_proposals.schema.json` document. Metadata: batch_id `glossary_batch_001_data_analyst_pilot`, model `claude-sonnet-5`, prompt_version `08_segment_detection@v1`, source_snapshot_id `data_analytics.source_pack`, parent_artifact_hashes = sha256 of `video_candidates.json`, `coverage_briefs.json` and `extracted_concepts.json`, generated_at = real UTC time.

Work through your video list methodically — write the file incrementally with a script as you go, don't hold everything in your head.

Validate: `python3 00_GLOSSARY_PIPELINE_CORE/scripts/schema_check.py segment_proposals.schema.json <your part file>`.

Reply briefly: video count, proposal count, rejected count, which videos needed real transcript reading (not just chapters) to catch a mismatch, anything you were unsure of.
