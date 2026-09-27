# Orchestrator notes — glossary_batch_001_data_analyst_pilot

Carry-forward items for later stages, so they survive context loss.

## For 05_glossary_pass_a
- `data.analysis_workflow`: present **visualize** as its own step (showing data or findings in graphics), distinct from **analyze** (examining prepared data to answer the question). Don't merge analyzing into "making charts". (Advisory from the canary's final 03 check.)

## For the TOC pipeline (upstream fix, not this batch)
- 10 data_analyst concepts have placeholder objectives in the frozen TOC ("Understand and use X…", "Given a simple example, correctly identify or apply X"): all 5 in region_data_analysis_foundations (`data.dataset_rows_columns`, `data.categorical_numeric_types`, `data.data_quality_basics`, `data.analysis_workflow`, `data.ethics_privacy_basics`) and 5 in region_sql_fundamentals (`sql.string_functions`, `sql.date_time_functions`, `sql.type_casting`, `sql.coalesce`, `sql.union`).

- Name vs. objective conflicts in the frozen TOC (fix the name or the objective upstream): `pandas.creating_dataframes` is named "…from dicts/lists/files" but its objective says "rather than loading it from a file" (file loading is `pandas.reading_data`); `stats.distribution_shape` names "outliers" but its central_mental_model scopes outliers out to `stats.outlier_reasoning`.

## Source pack notes
- `opentextbc.ca` (the BCcampus Database Design textbook) blocks curl/WebFetch with a Cloudflare challenge; c3 read it via Wayback Machine snapshots. Future evaluators need the same route.

## Process learned in the canary (already folded into the pack)
- 03 canary took 4 full evaluations + 2 scoped checks on 5 concepts. Fixes: GENERATOR.md canary-mistakes checklist; BLOCKING/ADVISORY gate; scoped re-checks after repairs (START_HERE.md).

- From the c1 03 evaluation: `python.core_data_types` assessment target asks how types behave in arithmetic/comparison (both taught later); `python.tuples` practice returns a tuple from a function (functions taught later).
- From the c2 03 evaluation (TOC objectives needing later concepts): `stats.descriptive_measures_of_center` assessment/practice need skew (later: `stats.distribution_shape`); `stats.distribution_shape` practice says "Given a histogram" (later: `stats.frequency_distribution_reading`); `pandas.reading_data` and `pandas.creating_dataframes` practices verify shape (later: `pandas.inspecting_dataframes`); `pandas.merge_join` objective mirrors SQL joins (later).

## Stage 03 chunk status
- c1: PASS (full eval FAIL 14B → repair → scoped FAIL 2B → repair → scoped PASS).
- c2: hit the 3-failed-round limit (full FAIL 12B → scoped FAIL 1B outlier → scoped FAIL 1B). Last blocker: `pandas.dataframe_series_model` f3 default-index clause over-generalised to dict/scalar (introduced by an advisory fix). Held for user decision.
- Pattern: every repair round introduced a new blocker, 2 of 4 from ADVISORY fixes. Advisory fixes applied after a PASS are never re-checked — risk to flag.

## RESUME HERE (usage limit hit 2026-09-26)
- User decisions: (1) c2 gets the pinned fix + one narrow check; (2) advisory fixes limited to reword/delete/move/cite (now in START_HERE.md).
- c1: PASS.
- c2: TODO resume generator ac0685a28d0a33a5d with: dataframe_series_model f3 → "...a dict, or a scalar value. When built from a list (or other array-like data) with no index passed, the index defaults to 0, 1, ..., len(data) - 1; when built from a dict, the dict's keys become the index." (refs pandas_docs_series_api, pandas_docs_dsintro#series). Then one narrow re-check of that fact.
- c3: round 3 FAIL, 1 blocker, same rule applies: er_diagram_reading f3 → restore round-2 f3 text (scratchpad/c3_round2.json) and drop the #ch9-Relationship Types ref (or state line style = identifying/non-identifying in optional). Advisory: drop "(see the example in §7.2.2)" from sql.subquery_in_where f2. Generator a065e4ead20b4fa88. Then one narrow check.
- c4: generator ae0e593de00b514bb died (network) while updating manifest count — check part file exists/valid, source pack + manifest count, then resume it.
- c5: generated (30 briefs, VALID) — needs full first evaluation. Sourcing gap flagged: stakeholder.precise_finding_statement "specific number" not sourced.
- c6: generated (12, VALID); its evaluator died (network) — relaunch full evaluation.
- Source pack: uk_gov_aqua_book url_or_citation should point to https://www.gov.uk/guidance/the-aqua-book (locators §5.2.x, §6.x, §9.x live there).
- Then: merge_parts.py coverage_briefs.json, record 03 gate; re-record 00 gate (source pack grew 50→~120).
- c3: PASS (2026-09-26). Pinned fix verified mechanically: er_diagram_reading f3 restored byte-identical to round-2 text (cleared by the round-3 evaluator as non-blocking), subquery_in_where f2 lost only the parenthetical; nothing else changed. Residual advisory (not applied): "ERD shows relationships as lines" isn't in ch8 Types of Relationships — revisit at stage 16.
- c2: PASS (2026-09-26). Pinned fix = evaluator's exact wording; checked against live dsintro (default index under "From ndarray"; dict example shows keys as index). Only that fact changed.
- From c4 generation (TOC objectives needing later concepts): `spreadsheet.grid_model` assessment needs cross-sheet refs (later: `spreadsheet.cross_sheet_references`); `spreadsheet.cell_references_ranges` practice "sums a range" needs formula syntax/SUM (later); `spreadsheet.named_ranges` practice uses a lookup formula (later: `spreadsheet.vlookup_xlookup`).
- From c6 03 evaluation: `capstone.independent_execution` assessment says "across SQL/spreadsheet/Python/BI" but the TOC has no BI-tool concept.
- From c5 03 evaluation: `viz.pyplot_basic_plotting` practice asks for a line chart (later: `viz.line_plots`); `viz.figure_size_layout` practice fixes overlapping labels (later: `viz.labeling_annotation`) and precedes any plotting concept; `viz.seaborn_themes_palettes` practice applies a theme "to an existing plot" (set_theme only affects later plots); `stakeholder.chart_type_to_point_matching` needs pie charts, which no viz concept teaches.
- From c4 03 evaluation: `spreadsheet.structured_tables` and `spreadsheet.named_ranges` assessments have the learner write formulas, but `spreadsheet.formula_syntax` comes later; `spreadsheet.formula_syntax` practice "percentage change" overlaps later `stats.lift_interpretation`.
- OpenIntro edition: the pack's `openintro_statistics_textbook` is the **4th edition** (openintro.org/book/os/). c4's first draft cited 3rd-edition section numbers. All locators must use 4th-edition numbering.
- c6: PASS (2026-09-26). Full FAIL 6B → repair → scoped PASS → 3 wording-only advisory edits (verified by diff; the 4th, a citation, was already present).
- From c5 re-check: `stakeholder.framing_analytical_question` central_mental_model says a measurable question names a "timeframe"; no reputable source states this for analytical questions — consider dropping "timeframe" from the TOC wording.
- c5: PASS (2026-09-27). Full FAIL 20B → repair → scoped FAIL 3B (all pinned) → repair → verified by diff: every change matches pinned wording, nothing else changed. Added asa_gaise_ii (pack 130).
- c4: PASS (2026-09-27). Full FAIL 23B (OpenIntro 3rd-ed locators, missing Excel how-tos) → repair → scoped FAIL 2B (pinned) → repair → verified by diff. Pack at 130.

## Stage 03 GATED PASS (2026-09-27)
- coverage_briefs.json = 7 merged parts, 168 briefs. Every chunk: full eval → repairs → scoped checks (pinned-wording rounds verified by diff).
- 00_preflight re-recorded PASS: source pack grew 50 → 130 during stage 03; every added source was opened and confirmed by a stage 03 evaluator.
- Carry-forward advisories for stage 16: c3 `datamodel.er_diagram_reading` f3 ("ERD shows relationships as lines" not literally in ch8 Types of Relationships).
- Stage 04 GATED PASS (2026-09-27): 42 core / 86 standard / 40 reference. First-pass PASS; advisories applied once; numbers re-verified by script.

## Stage 05 chunk status
- c0_canary: PASS (2026-09-27). Full FAIL 2B (one-word overclaims, pinned) → repair → verified by script. Lessons folded into 05 GENERATOR.md "Accuracy" list.
- From 05 c3: `sql.aliasing` practice ("multi-table join query using aliases") needs `sql.inner_join`, taught later.
- 05 c4 advisory deferred: Orders column letters differ between spreadsheet entries (A/B/C mean different fields). Fix at stage 11 reconciliation or 16 audit with one fixed layout.

## RESUME HERE — stage 05 (stopped by user 2026-09-27)
Findings files + round-1 snapshots are in the session scratchpad (findings_05_cN.md, pa_cN_round1.json); if the scratchpad is gone, re-run the evaluator for that chunk.
- c0_canary: PASS.
- c1: FAIL 17B (pinned) — repair was mid-apply when stopped (generator agent a0793a74cd25f38c1).
- c2: FAIL 7B (pinned) — repair nearly done, was re-verifying (a81299e5c411c1391).
- c3: FAIL 6B (pinned) — repair in progress (a7d6d6af10ce2b269).
- c4: FAIL 9B (pinned) — repair just started (a680f360d0c0e4e72).
- c5: generation almost done, part file not yet written (a9ba469d12b5e8309).
- c6: written; first evaluation was in progress — re-run it.
After each repair: diff vs round-1 snapshot, check pinned text present, then gate. Then merge_parts glossary_pass_a.json, record 05.
- File state at stop: c2 and c3 part files already contain some repair edits (may be partial — resume the same generator or diff against the round-1 snapshot); c1 and c4 unchanged; c5 file not written.
- MOVED TO GITHUB (2026-09-27): findings_05_cN.md, pa_cN_round1.json snapshots and the shared prompts (pa_prompt.md, pa_eval_prompt.md) are now in `batches/glossary_batch_001_data_analyst_pilot/working/`. Agent ids above don't carry to another account — start fresh generators with the findings file for each chunk's repair.
