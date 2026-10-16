Pack root (run every command from here): `/Users/folajuwon/Downloads/Telegram Desktop/UNIVERSAL_GLOSSARY_PIPELINE_PACK`

Stage `09_segment_judge`: you are the only quality gate a video segment passes through before a learner would see it — no human reviews it first. Judge accordingly.

**Read first:**
- `01_GLOSSARY_PACK_TEMPLATE/09_segment_judge/EVALUATOR.md`.
- Playbook §14-16 in `00_GLOSSARY_PIPELINE_CORE/PLAYBOOK_v3.md` (lines ~1073-1175), the same sections the detector worked from.

**Batch folder:** `batches/glossary_batch_001_data_analyst_pilot/`. You're judging `segment_proposals.part.{CHUNK}.json` ({DESC}).

**For every proposal in your chunk's file** (ignore its own `rejected_videos` list — that's the detector's calls, not yours to re-litigate unless something there looks wrong):
1. Open `00_GLOSSARY_PIPELINE_CORE/video_bank/transcripts/<video_id>.json` and read the proposed range yourself, plus about 30 seconds either side. Open the catalogue's chapters too.
2. Check the coverage brief's required facts for `concept_id` (in `coverage_briefs.json`) and the concept's `blocked_knowledge_ids` (in `extracted_concepts.json`, checked by name).
3. Apply the hard rejections from §16: contradicts the concept's evidence (`rejected_inaccurate`); needs a blocked concept to understand (`rejected_prerequisite_leak`); opens mid-thought or leans on earlier context (`rejected_needs_prior_context`); not really about this concept (`rejected_off_topic`); not embeddable (`rejected_not_embeddable`); no transcript (`rejected_no_transcript`); bad boundaries you can't fix (`rejected_bad_boundaries`); longer than its role needs with no reason (`rejected_too_long`); teaches different facts than claimed (`rejected_fact_mismatch`).
4. Weigh visual value: a pure talking-head segment is `rejected_weak_visual` unless the concept is genuinely conceptual and the explanation is exceptionally clear.
5. If the content is right but the cut is off, tighten it yourself — set `final_start_seconds`/`final_end_seconds` to what you'd actually use, and approve.
6. `confirmed_fact_ids`: only the facts the range actually teaches — this can be fewer than what was proposed.
7. Score all seven `scores` keys 1-5, exactly as the schema names them: `technical_accuracy`, `fact_coverage`, `prerequisite_safety`, `standalone_clarity`, `visual_teaching_value`, `pacing`, `boundary_quality`. (Accessibility/reliability is the embeddability check above, folded into the hard-rejection pass, not a separate score.)
8. `reasoning` must cite what you actually read in the transcript — not the detector's label or summary. If your verdicts end up mirroring the proposals across the board (everything approved, every fact confirmed), stop and re-read: that pattern usually means you checked the detector's claims instead of the source.

**Output:** `batches/glossary_batch_001_data_analyst_pilot/segment_judgments.part.{CHUNK}.json`, a full `segment_judgments.schema.json` document covering every proposal in your assigned part file. Metadata: batch_id `glossary_batch_001_data_analyst_pilot`, model `claude-opus-5-5`, prompt_version `09_segment_judge@v1`, source_snapshot_id `data_analytics.source_pack`, parent_artifact_hashes = sha256 of `segment_proposals.part.{CHUNK}.json`, `coverage_briefs.json` and `extracted_concepts.json`, generated_at = real UTC time.

Validate: `python3 00_GLOSSARY_PIPELINE_CORE/scripts/schema_check.py segment_judgments.schema.json <your part file>`.

**Note on your closing verdict:** `VERDICT: PASS` or `VERDICT: FAIL` describes whether *you did your job completely* — every proposal judged with a real reason, no rubber-stamping — not whether the videos turned out good. Rejecting half the proposals for real reasons is still `VERDICT: PASS`; it means the gate worked. Say `VERDICT: FAIL` only if you couldn't finish, or if you realize partway through that you were mirroring the detector's claims instead of checking the source yourself. Either way, list your rejections and their reasons in your reply so the coordinator knows which concepts need a re-sourced video or text-only coverage.
