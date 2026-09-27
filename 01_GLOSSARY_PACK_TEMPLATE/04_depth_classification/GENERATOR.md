# 04_depth_classification — GENERATOR

Produce `depth_classification.json`: `core`, `standard` or `reference` per (concept, path). This reuses the TOC's own signals; it is not a second curriculum ranking (playbook §8). The TOC's `disposition` field is nearly always `immediate_core`, so it carries no depth information — don't use it.

Signals from `extracted_concepts.json` and `coverage_briefs.json`:
- `dependency_graph_centrality` — how many later concepts build on this one. Compare within the path: top quarter → strong Core signal; zero → strong Reference signal.
- What the `assessment_target` asks for: applying or combining in a new situation → Core; recognising or looking up → Reference.
- Required-fact count and whether there are misconceptions.

Rough rule: **Core** when centrality is in the path's top quarter, or the assessment demands applying the idea in a new situation. **Reference** when centrality is 0 and the assessment is recall or lookup (minor syntax, one-off options). **Standard** otherwise.

`reasoning` cites the actual numbers ("centrality 6, top quartile for data_analyst; assessment requires choosing a join type for a new question → core").
