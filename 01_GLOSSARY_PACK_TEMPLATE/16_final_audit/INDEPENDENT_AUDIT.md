# 16_final_audit — INDEPENDENT_AUDIT (evaluator-only)

Fresh context, no access to any earlier stage's reasoning. You write `glossary_independent_audit_report.json`. This is the last check before `16b_registry_merge` makes this batch's evidence and segments permanent and reusable by every later batch.

`reviewed_bundle_ids` lists every `concept_id:path_id` in every path bundle.

Re-derive from the source files, not from earlier reports:
- **Exhaustive, text:** every bundle's teaching blocks against its required facts (all taught?) and its boundary (anything blocked needed?). Cheap relative to video — do all of them.
- **Sampled, video:** re-judge at least 20% of segments, plus every segment with `mean_score` below 3.5 — and no need to exceed roughly a third of segments overall unless your sample starts disagreeing with 09. Read their transcript ranges as `09_segment_judge` would. If your sample disagrees with 09 more than occasionally, say so and widen the re-judge — that means 09 is miscalibrated, and the batch needs a wider check, not a pass.
- **New canonical evidence** (coverage briefs with `canonical_status: new`): open a sample of sources and confirm they back the facts. This evidence is about to be reused by other paths.
- **Ledger:** `update_ledger.py verify` exits 0.

Severity: `BLOCKER` for a wrong or leaked fact reaching a learner, or bad evidence about to be reused. `HIGH` for a segment that doesn't really teach its concept. `MEDIUM`/`LOW` for real but non-blocking issues.

Verdict: `PASS` with no issues; `PASS_WITH_NONBLOCKING_CHANGES` when every issue is MEDIUM or LOW; `FAIL` otherwise.

Validate: `schema_check.py glossary_independent_audit_report.schema.json batches/<batch_id>/glossary_independent_audit_report.json`, then end with `VERDICT: <verdict>`.
