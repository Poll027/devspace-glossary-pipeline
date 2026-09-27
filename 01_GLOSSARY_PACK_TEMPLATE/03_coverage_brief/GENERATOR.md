# 03_coverage_brief — GENERATOR

Produce `coverage_briefs.json` (`schemas/coverage_briefs.schema.json`): one brief per row of `extracted_concepts.json`. Read playbook §5–7 and the §28.1 prompt first. Work one TOC tile at a time — concepts in a tile share sources and context (cost gate 8).

**By `registry_lookup.json` status:**
- `reuse_registry` — copy the concept's `evidence` object from `concept_evidence_registry_snapshot.json` unchanged. Only `learning_objective` is written fresh.
- `shared_in_batch` — do the owning path's brief first, then copy its `evidence` unchanged.
- `new` — build the evidence below.

**Building evidence (path-neutral — it will be reused by other paths):**
- `required_facts`: the minimum complete set a learner must understand. Derive them from the concept's `primary_objective`, `assessment_target`, `practice_objective` and `central_mental_model`. Test the set: could a learner who knew only these facts do the `assessment_target` and `practice_objective`? If not, a fact is missing. If a fact isn't needed for either, it's `optional_enrichment`, not required.
- **Placeholder objectives.** A few frozen TOC concepts carry template text instead of real objectives ("Understand and use X in a small analysis task", "Given a simple example, correctly identify or apply X"). For those, derive the facts from the concept name, its tile's title and summary, its neighbours in the tile, and the sources. List those concept_ids in your reply so the TOC can be fixed upstream. Don't treat the placeholder text as a real assessment target.
- **If the concept name lists items** ("Ask, inspect, clean, analyze, visualize, communicate"), every listed item gets covered by a fact.
- Each fact is one plain statement, ids `f1, f2, …`, and cites `source_refs` from this batch's source packs. Open the source and confirm it says what the fact says. A fact you can't back is dropped or backed — never left unsupported.
- **Cite with a locator** where the source is long: `source_id#section` (e.g. `openintro_statistics_textbook#1.2.1`), so an evaluator can check it without re-reading a whole book.
- **Say no more than the source.** Don't add "always", "every", "only", ordering ("once X is done") or scope the source doesn't state. "Data is commonly organized as a table" is not "all data is a table".
- **Blocked by meaning, not just by id.** Read the *names* of the `blocked_knowledge_ids` concepts, not only their ids. A fact that mentions averages, histograms or joins is using blocked knowledge if those concepts come later, whatever the wording. Terms in `inline_vocabulary` are usable; `forward_preview_ids` concepts may be mentioned only as an un-required preview.
- `misconceptions`: only ones that would damage later learning (playbook §6). A misconception is a factual claim too — give it `source_refs` when a source addresses it, and don't lean on terms no required fact introduces.
- **Practice must be possible.** If the concept will be practised (see `practice_objective`, or its name for placeholders), include at least one actionable fact — something a learner can *do* — not only a principle.
- No path framing, examples or career context inside `evidence`.

**Mistakes the pilot canary made — check every brief for these before you finish:**
- Blocked knowledge smuggled into a parenthetical or example ("numbers can be summarized (such as averaging)" when averages come later). The boundary applies to every word, not just the main claim.
- A fixing or remedy fact that reaches for a later technique ("group or aggregate the data" when grouping is taught later). Say only what this concept can do.
- A claimed structure the source doesn't have ("visualizing is its own stage" when the source lists four stages without one). Don't invent stages, steps or categories.
- Examples that aren't the source's. Use the source's own example, or none — not a similar one from memory.
- The same claim stated in two facts, or in a fact and a misconception. Each claim appears once.
- A concept-name item with no fact of its own ("datasets" in "rows, columns, and datasets").
- Long sources cited without a `#section` locator.

**Mistakes the first fan-out wave made (37 blockers across 89 briefs) — most common first:**
- **No "how-to" fact.** Every verb in `practice_objective` and `assessment_target` needs a fact giving the form to do it: syntax (`df.loc[rows, cols]`, `WITH name AS (…)`, `if …:` + indented block), the argument that picks the variant (`how=`, `axis=`, `aggfunc=`), what an operator means (`=`/`<>`). Conceptual facts alone ("group by is split-apply-combine") can't be practised. Walk the practice sentence verb by verb.
- **Defaults that change the answer.** If a default silently gives a different result than the practice expects (pivot_table averages; variance divides by n − 1), state it.
- **Every variant the assessment asks the learner to choose between** ("correct join type" → define inner, left, right, outer).
- **The definition behind the objective.** If the objective is "each table represents one entity", a fact must say that; if it's "identify redundancy", say what redundancy is.
- **An example's specifics stated as a rule** ("the foreign key goes on the many side" when the source only shows Customer/Order). Scope it to the example, or find a source that states the rule.
- **Softening dropped.** Keep "roughly", "usually", "can" from the source.
- **Refs that cite the right page but the wrong section** (a claim about dicts cited to a section that only shows Series). Cite the section that says it.
- **Every listed collection or type** in the objective ("lists, dicts, sets and tuples") gets its own behaviour fact.

**Repair rounds:** in the pilot, every repair introduced one new blocker — a fact added to fill a gap that went beyond its source ("so the optional side is the many side", "keep, correct, or exclude"), or a rewrite that deleted the concept's defining rule. Before replying, re-open the cited section for every fact you added or rewrote and check it word by word; and confirm each rewritten brief still states its concept's core rule.

**Path-specific:** `learning_objective` — this path's objective, grounded in its own `primary_objective`.

Validate: `python3 00_GLOSSARY_PIPELINE_CORE/scripts/schema_check.py coverage_briefs.schema.json batches/<batch_id>/coverage_briefs.json`
