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

## Stage 05 chunk status (continued, session resumed 2026-10-01)
- c1: PASS (2026-10-01). Full FAIL 20B → repair → scoped FAIL 1B (return_values recursion bug from an applied advisory) → repair → scoped PASS, no defects.
- c3: PASS (2026-10-01). Full FAIL 6B → repair (2 sessions) → scoped PASS with advisories → advisories applied once.
- c4: PASS (2026-10-01). Full FAIL 9B (10 in practice) → repair → scoped PASS with advisories → advisories applied once.
c3: DONE — all advisories closed.
- c6 05 evaluation: deferred advisory, driver roster/orders data-flow consistency across integrate_sql/integrate_spreadsheet/integrate_python_pandas, similar to the c4 column-layout issue — fix at stage 11/16.
c4: DONE — all advisories closed, 32 entries.
- c2: PASS (2026-10-01). Full FAIL 7B → repair → scoped FAIL 2B (self-contradicting correlation sign, overstated mean-as-typical — both from an applied advisory) → repair → scoped PASS, no defects.
c6: DONE — all advisories closed, 12 entries.

## From c5 05 evaluation — upstream/stage-16 gaps (logged, not fixed here)
- python.import_statements has no fact for the `import X as Y` alias form, needed by every plt/sns/pd example across the whole path.
- viz.pyplot_basic_plotting's central_mental_model (pyplot implicitly acts on the current Figure/Axes) has no backing fact.
- viz.box_plots: no brief anywhere defines a quartile; add a sourced definition (OpenIntro 4th ed.) at stage 16.
- viz.scatter_plots practice asks to "describe the apparent relationship" with no reading-guidance fact.
- stakeholder.anticipating_questions_objections brief f2 itself dropped the source's "Some" hedge — fix at stage 03 or flag for 16.
- c5: PASS (2026-10-01). Full FAIL 11B (undefined vars, unapplied facts, misconception stated as true) → repair → scoped PASS → 3 advisories applied once.

## Stage 05 GATED PASS (2026-10-01)
- glossary_pass_a.json = 7 merged parts, 168 entries. Every chunk: full eval → repair(s) → scoped checks. c1 and c2 each needed 3 rounds (hit new blockers introduced by their own applied advisories); c3, c4, c5, c6 needed 2; c0 needed 2.
- Pattern confirmed again: advisory edits are a real source of new blockers (5 of ~8 second-round failures came from an applied advisory, not the original defect). Keep running a scoped re-check after every advisory batch that touches prose with a factual claim, not just after blocking repairs.
- Deferred to stage 11/16: c4 Orders column layout (now fixed to one layout within c4 itself, but not cross-checked against other chunks); c6 capstone data-source consistency (SQL drivers table vs Excel roster framing in data_retrieval_method_selection).
- Upstream gaps logged for stage 16 / TOC fix: python.import_statements missing the `import X as Y` alias fact; viz.pyplot_basic_plotting central_mental_model unbacked; viz.box_plots missing a quartile definition; viz.scatter_plots missing relationship-reading guidance; stakeholder.anticipating_questions_objections brief dropped a source hedge.

## Stage 06 — first live run (2026-10-01)
- Built 00_GLOSSARY_PIPELINE_CORE/scripts/search_catalogs.py: keyword search over the 43-channel/31,766-video catalogue, with exact-phrase ranking boost. Generators must use this instead of reading catalogue files directly.
- 96 of 168 concepts need a video search (35 HIGH, 61 MEDIUM); the other 72 (LOW/NONE) get no stage 06 entry at all.
- Allowlist content gap: the 43 channels skew tool-tutorial and career-advice, with thin coverage for pre-tool/conceptual concepts (e.g. data.data_quality_basics, data.analysis_workflow — both positions 2-3, before Python/SQL/pandas/Excel are introduced). Both canary concepts needed open search. Expect this pattern to recur for other early-foundations and stakeholder-communication concepts.
- c0_canary: generated, 2/2 HIGH concepts searched, all 9 video_ids independently re-resolved via yt-dlp before being kept — now under evaluation.
- search_catalogs.py fixed: full-term matches now rank before single-word noise (score 100+ vs 1-2); exact-phrase gets a smaller secondary bonus. Re-verified "data quality" still has no genuine allowlist match after the fix, confirming the content-gap finding.
- 06 GENERATOR.md prompt updated: open-search candidates now require a description/chapters check and a last-20-uploads channel check before being kept, with the same teaching-channels-only rule used for the allowlist itself. Reasons may only cite what was actually verified.
- c0_canary (stage 06): PASS (2026-10-01). Full FAIL 2B → repair → scoped FAIL 1B (new candidate from a career-advice channel) → repair → mechanically verified (pinned fix, 3rd round). Fixed search_catalogs.py ranking and strengthened 06 GENERATOR.md: channel check overrides a single good video; open-search candidates need description/chapters + last-20-uploads checks.
- 06 c1/c2/c3 generated: c1 10 searches/50 cands (allowlist_only throughout), c2 24 searches/51 cands (11 needed open search), c3 17 searches/43 cands (allowlist_only throughout). All schema-valid, exact HIGH/MEDIUM coverage confirmed.
- c2 generator substituted `yt-dlp ytsearchN:` for WebSearch after hitting a WebSearch rate limit — still real, verifiable results, same video_id guarantee. Acceptable; evaluator should verify the candidates it sourced this way like any other open-search candidate.
- c1 (stage 06): PASS (2026-10-01). Full FAIL 1B (retyped emoji) + 6 recall-gap advisories → repair → scoped PASS, no defects.
- 06 pattern: generators sometimes give up on allowlist search after 2-3 keyword tries and fall back to open search when a precise allowlist match exists under a different keyword (e.g. "str_accessor_cleaning" needed "strip"/"replace" not "string methods"). Try chapter/transcript-level keywords, not just the concept name, before falling back.
- search_catalogs.py bug fixed: the tokenizer dropped single-letter tokens, so "A/B" testing queries lost both "a" and "b" and couldn't require them together (contributed to missing precise A/B-testing matches in c4). Now normalizes "a/b" -> "ab" before tokenizing, in query, title and phrase-bonus check. Re-verified "a/b testing" now surfaces the precise matches first.
- c3 (stage 06): PASS (2026-10-01), closed by coordinator after round 3 (final). Full FAIL 3B -> repair -> scoped FAIL 2B -> repair -> scoped FAIL 2B (new candidates didn't fit on transcript inspection) -> final repair with transcript-level verification throughout -> coordinator spot-checked 5OpBjU-OWh8's transcript independently (confirmed "multiple columns to join", duplicate-row bug) and closed without another evaluator round. composite_join_conditions ends with 1 honest kept candidate rather than a padded weak fit.
- c4 (stage 06): PASS (2026-10-01). Full FAIL 2B (ab_test_structure missing precise matches due to the A/B tokenizer bug; business_conclusion searched by concept name instead of facts) -> repair -> coordinator fixed one minor search_route/found_via inconsistency directly (ab_test_structure: allowlist_only -> allowlist_then_open_search, since open search was genuinely attempted) rather than spending another round.
- c2 (stage 06): PASS (2026-10-01). Full FAIL 7B -> repair -> scoped FAIL 2B -> repair -> scoped FAIL 2B (Hindi video slipped through; a route/found_via mismatch) -> coordinator fixed both plus 6 mechanical advisory labels directly (no more agent rounds), found codebasics drifts into AI-hype/career content via a manual channel check and rejected it, kept Analytics School as melt_reshaping's sole verified replacement.
- 06 c5 evaluation found a systematic bug: blocked_concepts_to_avoid populated with allowed-knowledge/prerequisite ids instead of real blocked_knowledge_ids, across 6 of 12 concepts. This would make stage 13 leakage-check wrongly reject good segments if not caught here. Worth a spot-check of other already-passed chunks (c0-c4, c6) at stage 16 audit, since this generator mistake may be systemic rather than c5-specific.
- c6 (stage 06): PASS (2026-10-02). Full FAIL 2B -> repair -> scoped PASS (verified via actual transcripts, including a Hindi-only one retrieved via youtube-transcript-api after yt-dlp 429s) -> 1 wording advisory applied directly by coordinator.
- c5 (stage 06): PASS (2026-10-02), closed by coordinator after round 3. Full FAIL 10B (6 were a systematic blocked_concepts_to_avoid bug: allowed-knowledge/prerequisite ids used instead of real blocked ids) -> repair -> scoped FAIL 2B (two new candidates overclaimed content on reason text) -> coordinator fixed both plus 5 advisories directly (pure text/fact-mapping, no new verification needed) and removed a stray fact_ids field it introduced. All 7 stage 06 chunks now done.

## Stage 06 GATED PASS (2026-10-02)
- video_candidates.json = 7 merged parts, 96 concept searches (HIGH/MEDIUM only), 310 candidates (239 kept, 71 rejected), zero concepts with no kept candidate.
- First live run of this stage. Fixed/built along the way: search_catalogs.py (new tool, then ranking fix for full-term vs single-word noise, then "a/b" tokenizer fix).
- Recurring failure patterns across chunks, now folded into working/vc_prompt.md and vc_eval_prompt.md for the next batch:
  - Title/chapter name alone is not enough — must check actual description/transcript before keeping a candidate.
  - A good video from a bad channel (career-advice/vendor-marketing/news) must still be rejected — channel check overrides a single good video.
  - Search the concept's actual required facts, not just its name, before concluding the allowlist has nothing.
  - blocked_concepts_to_avoid must be checked against real blocked_knowledge_ids — generators default to "next N concepts in chunk order" if not pushed.
  - Auto-generated chapter lists can be wrong/misleading; pull the transcript when a rejection or a key claim hinges on content.
  - Copy every title field verbatim via script; several chunks had emoji/whitespace corrupted by retyping.

## Stage 07 GATED PASS (2026-10-02)
- fetch_videos.py run on 208 unique kept video_ids from video_candidates.json. Outcomes: 204 fetched, 3 failed_no_captions, 1 failed_fetch_error (z-Zg39LzcW8, persistent 429 on captions even after a client-fallback retry).
- Added a client-fallback (android) to fetch_videos.py's second retry attempt, since one video's 429 was specific to the default client and a different client fetched it manually. Kept as a general improvement for future runs, not just this video.
- z-Zg39LzcW8 (datamodel.foreign_keys_referential_integrity) still fails after the fix — accepted as a single genuine failure (not "many", per the script's own guidance). Its concept has 2 other kept candidates already fetched, so no concept is left without a usable video.
- failed_no_captions (3 videos): every segment from these will be rejected at stage 08/09 per README decision 4 — expected behavior, not a defect.
- video_bank/catalogue: 207 entries. video_bank/transcripts: 204 entries. Both shared across future batches/paths — never re-fetched.

## Stage 08/09 canary (2026-10-02)
- c0_canary PASS: 5 proposals, 4 approved (with tightened cuts), 1 rejected (video falsely claims "open() only has two arguments", contradicting f7's newline= usage — couldn't be trimmed out since it sits at the start).
- Lessons folded into working/sd_prompt.md and sj_prompt.md before fan-out:
  1. Detector shouldn't pre-trim a fact-bearing clause just to stay inside the duration band (it cut off pandas.creating_dataframes' default-index sentence mid-way for this reason) — propose honestly, let the judge trim.
  2. Detector's claimed "line X ends before timestamp Y" needs double-checking against the actual transcript line, not estimated — two cuts were off by a few seconds (a trailing reference still inside the cut; outro music starting earlier than claimed).
  3. Judge must also flag when the video itself states something false/contradicting the concept's facts (not just omissions) — this is a technical_accuracy failure, not just coverage.
- python.file_io has 3 more kept candidates landing in chunks c2, c3, c5 — the canary's reject doesn't leave this concept uncovered overall.
- Per-fact video gaps (sql.select_fundamentals f2, sql.clause_execution_order f2, datamodel.one_to_many f2, pandas.creating_dataframes f2) are expected/normal — Pass A text already covers every required fact independent of video (playbook §18 rule 5/6), so a missing video for one fact is not a pipeline defect.

## Stage 08/09 c1: DONE (2026-10-02)
- 29 proposals, 23 approved (20 with tightened cuts, 13 with fewer confirmed facts than proposed), 6 rejected for real content problems: 1E7NU-uWalY (variance taught as population 1/n, contradicts n-1 fact), 3hyKQZYe1HY (says WHERE runs after GROUP BY — backwards), 3Xc3CA655Y4 (box plot described as showing max/mean instead of median/IQR), 5OpBjU-OWh8 (depends on blocked LEFT JOIN + prior context), 3SRyslGSMW4 (generic groupby re-teach, not capstone integration), 0djtjjy12fI (5 min of mostly tangents, conflates symmetric with normal, doesn't teach the fact).
- Clarified sj_prompt.md: the judge's VERDICT: PASS/FAIL describes whether it did its own job completely (every proposal judged honestly), not whether the proposals turned out good. A judge rejecting many proposals for real reasons is doing its job (PASS), not failing.
- Advisory note raised by the judge: open-search candidates can come from channels not in channel_allowlist.json (e.g. IBM, a channel used for data.data_quality_basics) — this is expected and correct; open search exists precisely to go beyond the allowlist. No action needed.
- 6 concepts now need either a re-sourced video (another of their other kept candidates, if any, landing in a different chunk) or text-only coverage: stats.measures_of_spread, sql.having, viz.box_plots, sql.composite_join_conditions, capstone.integrate_python_pandas, viz.distribution_shape. Check at merge time whether any of these got an approved segment from a different chunk before concluding they need text-only.
- python.file_io: facts f4/f6/f7 (csv module: DictReader/DictWriter/newline="") are uncovered across all candidate videos seen so far (canary, c2, c3). May need a dedicated csv-focused video search, or rely on text-only for these 3 facts.

## Stage 08/09 c2: DONE (2026-10-02)
- 36 proposals, 32 approved (most cuts tightened), 4 rejected for real problems: GvftKv9uctk (wrong mean arithmetic, median/mode mislabeled), K1WeoKxLZ5o (CTE depends on unexplained PARTITION BY from "a previous video" + end_seconds past video length), K47w0cpRLt4 (logical_operators demo depends on if/elif and int(input()), both taught later), KFMs_ZZNgmo (teaches the 2x2 multi_panel_figures grid instead of single-Axes figure/axes basics).
- 2 label-text errors caught (axis='rows' vs 'columns'; pivot_table "sum default" vs actual "mean default") — fix at media-selection/reconciliation.
- FTpmwX94_Yo and KZe0C0Qq4p0 (both A/B testing) are the same recording word-for-word — use one as primary, one as fallback only, not both in the media group.

## Stage 08/09 c3: DONE (2026-10-02)
- 35 proposals, 30 approved (23 with a tightened range, 11 with fewer facts than proposed), 5 rejected for real problems: O5v4NrSCw_A (results built on blocked plotting setup), P90mCSsGE1c (relies on blocked .corr()/.describe(), overstates "92% correlated"), TqOeMYtOc1w (restates the exact p-value misreading its own concept's fact warns against), V6V5aR0wrkY (weak visual, talking-head-only, no modelling stage), VtVB-XsooiM (skips the delimiter/destination steps the concept actually teaches).
- Flagged for downstream text: SfX8IIxoJwQ says a list "is no longer a variable" (wrong); VRmXto2YA2I's groupby .mean() on string columns raises TypeError in pandas 2.x.

## Stage 08/09 c4: DONE (2026-10-02)
- 34 proposals, 32 approved (many with tightened cuts, 9 with fewer facts than proposed), 2 rejected: XezfbWlEVwE/viz.seaborn_dataframe_plotting (narration contradicts the mean-estimator fact, calling bar height "total"/"maximum"), XFZRVnP-MTU/capstone.building_dashboard_or_viz (the claimed 2x2 dashboard code is commented out on screen, nothing is actually drawn).
- Facts needing re-sourcing or text-only coverage: viz.seaborn_dataframe_plotting (no video now), capstone.building_dashboard_or_viz (no video now), pandas.loc_iloc_selection f2 (.loc inclusive-slice rule never stated explicitly), spreadsheet.aggregation_functions (only SUM covered, not AVERAGE/COUNTA/COUNT), sql.outer_joins (only FULL covered, not LEFT/RIGHT).

## PAUSED by user (2026-10-07) — cost/strategy discussion in progress
- c0-c4 fully done (detection+judgment). c5: proposals done (35, 4 rejected), judgment was in progress when stopped on request — not resumed, no partial file. c6: detection was in progress when stopped on request — no file written yet.
- Resume by re-dispatching: Stage 09 judge for c5 (prompt: working/sj_prompt.md, CHUNK=c5, same re-check list as before), then stage 08 detection for c6 (prompt: working/sd_prompt.md, CHUNK=c6), then stage 09 judge for c6.
- User asked to STOP generation and not restart until told — do not auto-resume on a future "continue" without an explicit instruction to resume this specific pipeline.

## Stage 08/09 close-out (2026-10-16)
- c5 judged: 28 approved / 7 rejected (logical_operators has no usable video at all; file_io, groupby_aggregation, subquery_in_where need prior context; junction_tables and one box-plot clip inaccurate; null_handling off topic).
- c6 detected by Sonnet 4.6 via Bedrock, judged: 25 approved / 4 rejected (normalization_basics x2, correlation, er_diagram_reading). Note: the judge's prose said 24/5; the file says 25/4 — file is authoritative.
- Text must carry (thin or no video): logical_operators; outer_joins (LEFT only); lookups (XLOOKUP only); capstone data retrieval (no SQL); pivot_tables (no Columns/Filters); frequency_distribution (f1 only); pyplot f1; histogram f2/f3; sets f4; FK f2/f3; one_to_many f2; many_to_many f3; significance f2/f4/f5; loc/iloc f2/f3; concat f3.
- Detector-rejections worth reconsidering as partial-coverage proposals (judge's note): q7Bo line_plots (f2), rP4p0luqvR8 while_loops (f1), v7dOXTgT2YU bar_charts (f2,f3 at 20-141).
- loc_iloc f2: zmdjNSmRXF4 Slicing chapters are allowed (reading_data is earlier in the TOC).
- Stage 10: 85 selected / 72 no_video_needed / 11 no_segment_found.
