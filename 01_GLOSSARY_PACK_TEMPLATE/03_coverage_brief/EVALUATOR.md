# 03_coverage_brief — EVALUATOR

Fresh context. You never saw the generator's reasoning; re-derive, don't skim.

- **Completeness:** one brief per `extracted_concepts.json` row, no extras.
- **Reuse is byte-identical:** for `reuse_registry` / `shared_in_batch`, `evidence` equals the source it was copied from exactly.
- **Sufficiency:** for every new concept, read its `assessment_target` and `practice_objective` and ask whether the required facts alone are enough to do them. Name the missing fact when they aren't.
- **Placeholder objectives:** where the TOC's objective is template text ("Understand and use X…", "Given a simple example, correctly identify or apply X"), judge sufficiency against what the concept name and its tile summary clearly require instead.
- **Minimality:** a "required" fact that neither the assessment nor the practice needs belongs in `optional_enrichment`.
- **Boundary:** no required fact needs the learner to *understand* a `blocked_knowledge_ids` concept — check against the blocked concepts' *names*, not just ids (an example that only works if you know averaging is blocked if descriptive statistics comes later). A passing mention the learner can follow without that knowledge is not blocked.
- **List-shaped names:** every item a concept name lists is covered.
- **Overstatement:** a fact adding "always/every/only", an ordering, or a scope its source doesn't state is a defect. Follow `#locator`s to the exact section.
- **Actionable:** a concept that will be practised has at least one fact a learner can act on.
- **Sources:** open at least a third of the cited sources yourself (all of them for Core-looking concepts with centrality ≥ 3). A source that doesn't support its fact is a FAIL.
- **Neutrality:** `evidence` contains no path-specific framing — it will be reused by other paths.

End with the verdict and defect lines in the BLOCKING/ADVISORY format from your agent file. Unsupported, contradicted or overstated claims, blocked knowledge and missing facts are blocking; repetition, wording, example choice and locators are advisory.
