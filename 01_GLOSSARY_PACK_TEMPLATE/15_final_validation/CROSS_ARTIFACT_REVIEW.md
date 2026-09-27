# 15_final_validation — CROSS_ARTIFACT_REVIEW (evaluator)

Fresh context, after `validate_bundles.py`. The script catches structure; you catch what only reading catches. Add findings to `glossary_validation_report.json` — `blocking_errors` or `warnings` — and set `validation_status` to FAIL if you add a blocking error. Don't create a second report.

1. **Read as a learner.** For each path, read ~10 bundles in TOC order across tiers. Does it flow? Does anything feel out of place, repeat, or assume what hasn't been taught?
2. **Shared concepts across paths** (same `concept_id` in two bundles): the evidence may match, but examples and framing must differ by path.
3. **Final Schema readiness** (playbook §32): for a sample of segments, could the Final Schema answer every §32 question — which video, where to start and stop, what it teaches, what to read instead — without another lookup?
4. **Write `batches/<batch_id>/human_spot_check.md`** — the user's after-the-fact review list, not a gate. For each path: 10 Core, 10 Standard and 10 Reference concepts (or all, if fewer — playbook §34), and every segment with `mean_score` below 3.5. Per segment: concept, label, a clickable `review_url`, start–end as mm:ss with duration, and the summary. Put the lowest-scoring first.

End with `VERDICT: PASS` or `VERDICT: FAIL`.
