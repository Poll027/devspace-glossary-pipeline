Pack root (run every command from here): `/Users/folajuwon/Downloads/Telegram Desktop/UNIVERSAL_GLOSSARY_PIPELINE_PACK`. Python with jsonschema: `~/ai-env/bin/python` (system python3 lacks it).

Stage `11_reconciliation`: you assemble full Glossary Learning Bundles, one per concept, by reconciling Pass A teaching text with the selected, judge-approved video segments.

**Read first:**
- `01_GLOSSARY_PACK_TEMPLATE/11_reconciliation/GENERATOR.md` and `EVALUATOR.md` (what you'll be checked against).
- Playbook §18-23 and the §28.4 prompt in `00_GLOSSARY_PIPELINE_CORE/PLAYBOOK_v3.md` (the §8 Data Cleaning "video match" table is the model).
- `00_GLOSSARY_PIPELINE_CORE/schemas/glossary_bundles_draft.schema.json` and `glossary_learning_bundle.schema.json`.

**Inputs**, in batch folder `batches/glossary_batch_001_data_analyst_pilot/`: `glossary_pass_a.json`, `selected_media.json`, `coverage_briefs.json`, `depth_classification.json`, `extracted_concepts.json`, `segment_judgments.json` (the judge's `reasoning` per segment records what each final cut does and does not teach, read it), and transcripts in `00_GLOSSARY_PIPELINE_CORE/video_bank/transcripts/<video_id>.json` for the selected ranges.

**Chunk `{CHUNK}`** from `chunks.json` ({DESC}). Write `batches/glossary_batch_001_data_analyst_pilot/glossary_bundles_draft.part.{CHUNK}.json`: a full `glossary_bundles_draft.schema.json` document covering exactly that chunk's concepts. Metadata: batch_id `glossary_batch_001_data_analyst_pilot`, model `claude-sonnet-5-5`, prompt_version `11_reconciliation@v1`, source_snapshot_id `data_analytics.source_pack`, parent_artifact_hashes = sha256 of `glossary_pass_a.json`, `selected_media.json`, `coverage_briefs.json`, `depth_classification.json`, `extracted_concepts.json`; generated_at real UTC. Build the file with a script, copying segment fields mechanically from `selected_media.json` (never retype them).

**Hard rules** (lessons from stages 05/09):
- The text must teach EVERY required fact on its own. The judge approved many cuts that cover FEWER facts than the detector proposed, and several concepts have thin video coverage (see `orchestrator_notes.md`, "Stage 08/09 close-out"): wherever the segment's `fact_ids` omit a required fact, the text must fully carry it. Never rely on the clip for a fact it doesn't list.
- No mention of any video, clip or "watch" inside teaching blocks; that language belongs only in `bridge_note`.
- Keep Pass A's accuracy discipline: prose says no more than the facts; keep hedges; example code uses only allowed syntax; nothing needing a blocked concept.
- Bridge notes: concrete (what to watch for / the takeaway or the gap Devspace fills). If a clip uses a synonym or a blocked tool, say so in the bridge.
- Practice anchors must be doable with taught knowledge only; assessment anchors reflect the TOC `assessment_target` and cite real fact ids. Known TOC conflicts are logged in `orchestrator_notes.md`: handle them, don't paper over them.
- Set the four `validation` flags honestly.

**Self-check before finishing** (cost control): run `~/ai-env/bin/python 00_GLOSSARY_PIPELINE_CORE/scripts/schema_check.py glossary_bundles_draft.schema.json <part file>`, then script-check that every segment field equals the `selected_media.json` value, every required fact id appears in some teaching block's `fact_ids`, and no teaching block contains the words video/clip/watch/footage.

Reply briefly: concept count, segments count, anything you were unsure of.

**Lessons from the c0 canary evaluation (apply from the start):**
- `bridge_note.before`/`after` must be SHORT (~30-40 words each; §19 says "one small bridge_note"): one watch-for line plus any term caveat. No long walkthroughs.
- Describe each clip's visuals/claims only as the transcript range actually supports (e.g. don't say "a table of records" if the clip shows slides). State what a clip lacks (e.g. a misconception it never states) precisely, and don't claim it lacks something it actually says.
- Don't introduce a `blocked_knowledge_ids` concept's name (e.g. "outliers", "sample size") in `summary` or `bridge_note`; use the wording the teaching text uses.
- Segment `fact_ids` copied from `selected_media.json` may include optional-enrichment ids that aren't in `required_facts`; copy them anyway. Don't try to fix this.
