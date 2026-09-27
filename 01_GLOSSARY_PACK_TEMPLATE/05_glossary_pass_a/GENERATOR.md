# 05_glossary_pass_a — GENERATOR

Produce `glossary_pass_a.json`: the Devspace explanation for every (concept, path), written **before any video is considered** (playbook §8), plus the video-need call (§9). Read playbook §8 in full first, including the Data Cleaning benchmark — that is the quality bar for every sentence you write. Work tile by tile.

**Inputs per concept:** its coverage brief, its `extracted_concepts.json` row (boundary, tile, objectives), its depth tier, and the path's `path_title` and `learner_scope`.

**Teaching blocks** (`schemas/glossary_learning_bundle.schema.json#/$defs/teaching_block`):
- Use the purposes the concept needs: `intro`, `definition`, `mental_model`, `mechanism`, `syntax`, `example`, `walkthrough`, `workflow`, `misconception`, `practical_context`, `takeaway`. Core concepts usually need an example and a misconception; Reference concepts may need only a definition and one contextual example.
- Every required fact is taught by at least one block, and each block lists the `fact_ids` it teaches.
- Follow the §8 writing logic where it helps: concrete situation → problem → plain definition → how it works → example → why it matters. Write coherent teaching prose — not slide fragments, and not a textbook. One continuous example beats several unrelated ones.
- Examples come from this path's real work (a delivery-orders dataset for Data Analyst, a stakeholder requirement for Business Analyst), using only allowed knowledge.
- Length guide, not a hard rule: Core ~400–700 words across all blocks, Standard ~150–300, Reference ~40–100.
- **The text must teach on its own.** Learners may have video turned off. Never mention a video, a clip, or "watch".

**`video_need`** (§9): `HIGH` when understanding benefits from diagrams, animation, changing state, running code, tool demos or before/after; `MEDIUM` when a demo helps but the text mostly suffices; `LOW`/`NONE` when a paragraph or a simple visual does the job (minor syntax, definitions). Give a reason and the `preferred_visual_modes`. Only HIGH and MEDIUM get a YouTube search.

**Accuracy — the prose says no more than the facts.** Explaining, connecting and example *data* are yours; every factual claim, rule, tool behaviour, ordering or scope is the brief's. Mistakes the pilot canary made:
- Hedges upgraded: the fact says "commonly", the prose says "almost always". Keep the fact's hedge.
- Closed lists: "this is exactly the four checks from before" when the source has more. Say "checks such as…".
- Added purpose or cause: "to make a dataset usable, it's organized as a table" — no fact says why.
- Absolutes in explanation: "never a mix of kinds in one column". State the rule as the fact does.
- Example choice that fights the concept (a unique ID as the first example of a category). Pick example data that shows the idea cleanly.
- Code that doesn't run as the text says (a one-line `for …: if …:` is a SyntaxError; a variable reused across entries under a different shape). Run every Python/pandas snippet; trace every SQL/Excel example on the example data.
- Syntax the learner was never taught (`lambda`, `x if c else y`, `CREATE TABLE`). Examples use only constructs some allowed concept's facts teach.
- `video_need` NONE with non-empty `preferred_visual_modes` (NONE → `[]`; LOW may list one simple mode such as `data_table_demo`), or MEDIUM for a two-definition classification.

**`teaching_notes`:** what to keep short, what to avoid (later concepts), what the learner should grasp first.

Validate: `schema_check.py glossary_pass_a.schema.json batches/<batch_id>/glossary_pass_a.json`
