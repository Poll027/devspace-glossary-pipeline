Pack root (run every command from here): `/Users/folajuwon/Downloads/Telegram Desktop/UNIVERSAL_GLOSSARY_PIPELINE_PACK`

**Stage `05_glossary_pass_a`.** Your instructions are in `01_GLOSSARY_PACK_TEMPLATE/05_glossary_pass_a/EVALUATOR.md`.

Also read:
- `GENERATOR.md` in the same folder, especially its "Accuracy" list of mistakes.
- Playbook §8–9 in `00_GLOSSARY_PIPELINE_CORE/PLAYBOOK_v3.md`, lines ~649–901. This includes the Data Cleaning worked benchmark at ~line 705, which is the quality bar.

Batch folder: `batches/glossary_batch_001_data_analyst_pilot/`.

**Scope.** This is a full first evaluation of fan-out chunk `{CHUNK}` ({DESC}). Evaluate only `glossary_pass_a.part.{CHUNK}.json`. Check it against:
- `coverage_briefs.json`: the truth, meaning the required facts and their sources.
- `extracted_concepts.json`: boundary, allowed and blocked knowledge, objectives.
- `depth_classification.json`
- `orchestrator_notes.md`: "For the TOC pipeline", which lists known TOC conflicts. Those conflicts are ADVISORY, not blocking.

`glossary_pass_a.part.c0_canary.json` passed evaluation and shows the expected style.

**Checks.** Do these first, with a script:
- Every required fact and misconception is tagged by some block.
- Every fact_id exists.
- Each video_need's level agrees with its preferred_visual_modes.
- Grep the text for "video", "clip" and "watch".

Then read each entry the way a learner at that point would:
- **Accuracy.** Every claim in the prose must be supported by that concept's coverage-brief facts. It is BLOCKING if the prose adds a new factual claim, rule, tool behaviour, default, "always/only", closed list, cause or ordering, or upgrades a hedge. Code or formulas in examples must behave the way the text says; trace them. A worked number that is wrong is BLOCKING. Invented example *data* is fine.
- **Coverage.** A required fact that is tagged but not actually explained is BLOCKING.
- **Boundary.** Check blocked knowledge by concept name, not just id. If the learner must understand a blocked concept to follow the text, that is BLOCKING. A passing mention is not.
- **Stands alone.** Any mention of a video is BLOCKING.
- **Quality vs the benchmark.** A clear failure is BLOCKING: fragments, filler, no example, or a wall of text. Style preferences are ADVISORY.
- **video_need.** Check it against §9. Misjudged levels are ADVISORY, unless it is HIGH for minor syntax or NONE for a visual mechanism; those are BLOCKING per EVALUATOR.md.

End with `VERDICT: PASS|FAIL`, then one line per defect in the BLOCKING/ADVISORY format from your agent file, written as `concept_id@path_id: block → problem → fix`. **For every BLOCKING defect, give pinned replacement wording**, so the fix can be verified mechanically.

Video modes: NONE requires empty `preferred_visual_modes`; LOW may list one simple mode — that is allowed, not a defect.
