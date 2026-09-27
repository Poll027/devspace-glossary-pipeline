# 13_leakage_check — EVALUATOR (evaluator-only)

Fresh context. You write `leakage_audit_report.json` yourself. A hard gate — assembly refuses to run while `blocking_issue_count` is above 0.

Review **every** bundle in `glossary_bundles_draft.json` — list all of them in `reviewed_bundle_ids` as `concept_id:path_id`. Sampling is a FAIL of this stage.

For each bundle, using its row in `extracted_concepts.json`:
- **Leakage** (playbook §5): read every teaching block, example, misconception, anchor, and — for each media segment — its transcript range. Record any concept from `blocked_knowledge_ids` that a learner would need to understand in order to follow it, with `where` it happens. A blocked term mentioned in passing, not needed for understanding and listed in `forward_preview_ids`, is allowed. Implicit leakage counts: a code example using a later-taught construct without explaining it.
- **Unsupported claims:** any statement the coverage brief's facts and their sources don't support.
- `blocking: true` when either list is non-empty. `blocking_issue_count` is the real total.

When blocking issues exist, the fix goes to the stage that owns the problem (usually 05 or 11; a leaking segment goes back to 09), then everything downstream reruns.

Validate: `schema_check.py leakage_audit_report.schema.json batches/<batch_id>/leakage_audit_report.json`. End with `VERDICT: PASS` (0 blocking) or `VERDICT: FAIL`.
