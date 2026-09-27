Pack root (run every command from here): `/Users/folajuwon/Downloads/Telegram Desktop/UNIVERSAL_GLOSSARY_PIPELINE_PACK`

Stage `05_glossary_pass_a`: you write the actual teaching text learners read.

**Read first:**
- `01_GLOSSARY_PACK_TEMPLATE/05_glossary_pass_a/GENERATOR.md`. Pay close attention to "Accuracy — the prose says no more than the facts" and its list of canary mistakes.
- `EVALUATOR.md` in the same folder, which is what you'll be checked against.
- Playbook §8–9 in `00_GLOSSARY_PIPELINE_CORE/PLAYBOOK_v3.md` (lines ~649–901). This includes the Data Cleaning worked benchmark (~line 705), which is the quality bar, and the "Writing rule for the generation agent" (~line 836).
- The teaching_block, video_need and visual_mode defs in `00_GLOSSARY_PIPELINE_CORE/schemas/glossary_learning_bundle.schema.json#/$defs`.

**Inputs**, in batch folder `batches/glossary_batch_001_data_analyst_pilot/`:
- `coverage_briefs.json`: gated. Each concept's required facts are the truth you teach.
- `extracted_concepts.json`: boundary, allowed/blocked knowledge, tile, objectives, path_title, learner_scope.
- `depth_classification.json`: the tier sets the length guide.

**Reference output:** `glossary_pass_a.part.c0_canary.json` (the canary chunk, which has been evaluated) shows the expected style: one continuous delivery-orders example, blocks that list fact_ids, and prose rather than fragments.

**Fan-out chunk `{CHUNK}`** from `chunks.json` ({DESC}). Write `batches/glossary_batch_001_data_analyst_pilot/glossary_pass_a.part.{CHUNK}.json`. It must be a full `glossary_pass_a.schema.json` document covering exactly those concepts. Metadata:
- batch_id: `glossary_batch_001_data_analyst_pilot`
- model: `claude-sonnet-5`
- prompt_version: `05_glossary_pass_a@v1`
- source_snapshot_id: `data_analytics.source_pack`
- parent_artifact_hashes: sha256 of extracted_concepts.json, coverage_briefs.json and depth_classification.json
- generated_at: the real UTC time

Work tile by tile. Write the file incrementally, for example by building it with a script as you go.

**Hard rules**
- **Accuracy.** Every factual claim, rule, tool behaviour, default, ordering or scope in the prose must come from that concept's coverage-brief facts. Keep each fact's hedges ("commonly", "can", "roughly"). Don't close a list the source leaves open. Don't add causes or purposes the facts don't state. Code in examples must use only syntax and behaviour the facts give. Invented example *data* is fine.
- **Coverage.** Every required fact must be actually explained, not just tagged, by a block that lists its fact_id. Optional-enrichment facts may be skipped.
- **Boundary.** Nothing may require a `blocked_knowledge_ids` concept. Check by name as well as id. Examples use allowed knowledge only. A passing mention is OK. Needing it to follow the text is not.
- **Stands alone.** Never mention a video, clip, or "watch".
- **Examples.** Use one continuous, realistic data-analyst example per concept. A running dataset shared across a tile is good.
- **Length** follows the depth tier.
- **video_need** follows §9. For NONE/LOW, `preferred_visual_modes` must be consistent with the level.
- **TOC conflicts.** If a concept's own practice or assessment needs something taught later (see "For the TOC pipeline" in `orchestrator_notes.md`), teach only what the concept can, and note the conflict in teaching_notes.

Validate with `python3 00_GLOSSARY_PIPELINE_CORE/scripts/schema_check.py glossary_pass_a.schema.json <your part file>`. Then reply briefly with: counts, the video_need distribution, any fact the text needed that the brief lacked, and anything you were unsure of.
