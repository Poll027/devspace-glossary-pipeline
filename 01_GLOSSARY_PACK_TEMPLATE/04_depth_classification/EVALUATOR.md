# 04_depth_classification — EVALUATOR

Fresh context.

- Every (concept, path) classified once.
- Recompute the path's centrality quartiles from `extracted_concepts.json` yourself and check each `reasoning` cites real numbers. A made-up or wrong number is a FAIL.
- Consistency: two concepts with similar centrality and similar assessment demands shouldn't land in different tiers without a stated reason.
- Sanity: minor syntax isn't Core; a concept 8+ later concepts depend on isn't Reference.

End with `VERDICT: PASS` or `VERDICT: FAIL` and the defective rows.
