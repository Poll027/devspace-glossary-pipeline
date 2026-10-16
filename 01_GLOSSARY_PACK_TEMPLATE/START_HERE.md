# Start Here — running a glossary batch

The folders in `01_GLOSSARY_PACK_TEMPLATE/` hold stage **instructions**, read in place and never copied. A batch's **artifacts** all go in one flat folder: `batches/<batch_id>/`. Run everything from the pack root.

## Before the first batch

- Read `00_GLOSSARY_PIPELINE_CORE/README.md` (what this is, the decisions) and `RUNBOOK.md` (batching, rollout, two-runner coordination).
- `00_GLOSSARY_PIPELINE_CORE/PLAYBOOK_v3.md` is the spec. The stage files point you to the sections they implement.

## The loop

You (the main session) are the orchestrator. **Don't do stage work in your own context** — dispatch it, so your context stays small and every evaluator starts fresh. Walk `00_GLOSSARY_PIPELINE_CORE/pipeline_manifest.json` in order. Per stage `kind`:

- **`script`** — run the command in the stage's `RUN.md` with Bash. Exit 0 → record the gate. Non-zero → read the error, fix the input stage it points to, rerun.
- **`generate_evaluate`** — dispatch the `glossary-generator` subagent with the stage id and batch folder. Then dispatch a **new** `glossary-evaluator` subagent with the same stage id and batch folder, and nothing about the generator's reasoning. Evaluators label each defect `BLOCKING` or `ADVISORY` (see `.claude/agents/glossary-evaluator.md`).
    - `VERDICT: FAIL` (at least one blocking): send all findings to a generator repair round, then a **new** evaluator. Stop after 3 failed rounds and report to the user — don't loop forever.
    - `VERDICT: PASS` with advisories: send the advisories to one generator repair round, re-validate the schema, and gate. **No re-evaluation** — advisories don't warrant another full review.
    - **Advisory fixes may only reword, delete, move a fact to optional, or add a citation — never add a new claim.** The generator skips an advisory that would need a new claim (the evaluator judged it non-essential); evaluators must mark a needed new claim BLOCKING, not ADVISORY. (Pilot: 2 of 4 repair-introduced blockers came from advisory edits, which are otherwise never re-checked.)
    - The 3-round limit is for open-ended repairs. A single blocker with evaluator-pinned wording may get one more narrow fix + check.
    - A repair may resume the same generator (it keeps its context, which is cheaper). Evaluators are always new.
    - **Re-evaluation after a blocking FAIL is scoped to what the repair changed**: the new evaluator checks the repaired facts and blocks against their sources, and confirms nothing else changed. A full re-read every round keeps surfacing fresh advisories and never settles — the pilot canary showed this over four rounds. Full evaluation happens once per chunk, on first generation.
  - `08_segment_detection` is evaluated by stage `09`, not by its own evaluator.
- **`evaluator_only`** — dispatch `glossary-evaluator`. It writes the artifact itself.

After every gate decision:

```bash
python3 00_GLOSSARY_PIPELINE_CORE/scripts/update_ledger.py batches/<batch_id> record <stage_id> <artifact> PASS|FAIL \
  --generator <model or none> --evaluator <model or none> --unresolved <n>
```

**Large paths — fan out.** A 150+ concept path is too much for one agent in stages 03, 05, 06, 08, 09, 11 and 13. Split the path into chunks of about 30 concepts along region boundaries, never splitting a tile. Run the first chunk alone as a canary — its evaluator catches instruction problems cheaply — then dispatch the remaining chunks in parallel. Each agent writes `<artifact>.part.<chunk>.json` covering only its chunk (stage 08/09 chunks: the candidate videos of those concepts). Then combine the parts:

```bash
python3 00_GLOSSARY_PIPELINE_CORE/scripts/merge_parts.py batches/<batch_id> <artifact>.json <schema file name>
```

It concatenates rows, sums counts, rejects duplicate rows across parts, and schema-validates the result. Evaluate each chunk's part separately (in parallel), and gate the merged artifact.

**Repairs:** fix the earliest stage that owns the problem, then re-run and re-gate every stage downstream of it. `15b` catches anything you forget — it flags every gate whose artifact changed after it was recorded.

## Evaluation cost control

The evaluator is the expensive, high-value part of this loop — don't let it spend on what a script or a cheaper pass could have caught first.

1. **Mechanical checks before any evaluator call.** Run `schema_check.py` and any deterministic cross-reference (duplicate ids, a `blocked_concepts_to_avoid` id checked against the real `blocked_knowledge_ids`, a title byte-matched against its catalogue entry) before dispatching the evaluator. These are free; don't pay evaluator tokens to rediscover what a script already could have.
2. **Generator self-check before submitting.** Every `GENERATOR.md` carries a "mistakes made" checklist built from what evaluators have actually caught. Whatever model is generating should run its own output back through that checklist itself before handing it off — catches the mechanically-obvious errors (a dropped hedge, a formula that's backwards, a claim the source doesn't support) for a fraction of an evaluator call's cost.
3. **Depth tracks stakes, not uniform max rigor.** Full, exhaustive verification (open every source, run every snippet, read every transcript window) for Core concepts and anything a stage's own criteria flag as high-stakes (centrality, HIGH video_need). Lighter, sampled checking is fine for Standard/Reference-tier work, unless a stage's own file says otherwise (13 and 16's text pass are deliberately exhaustive — see those files).
4. **Canary-then-sample across a stage's chunks, not just its first run ever.** Full depth on the first chunk of any new stage, same as always. Once a generator/evaluator combination shows a low, stable defect rate across a few chunks of the *same* stage, later chunks of that stage can move to sampled verification instead of full depth on every single one. Re-upgrade to full depth immediately the moment a sampled chunk turns up a real defect — don't average it away.
5. **State a ceiling, not just a floor, wherever a stage asks for a sample.** "Open at least a third" has repeatedly turned into "opened essentially all of them" in practice, because thoroughness feels safer than the rule requires. Where a stage file says "at least N", also say "and no more than roughly 2N unless something you find gives a specific reason to go further."
6. **An `evaluator_only` stage's own `VERDICT: PASS/FAIL` describes whether it did its job completely, not whether the content turned out good.** Rejecting a large share of what it reviewed, for real stated reasons, is `PASS` — the gate worked. Say `FAIL` only if the evaluator couldn't finish, or realizes it was mirroring the generator's claims instead of checking the source itself.

## Stage kinds at a glance

| Stage | Kind | Files |
|---|---|---|
| 00_preflight | generate_evaluate | GENERATOR / EVALUATOR |
| 01_extraction, 02_registry_lookup | script | RUN |
| 03_coverage_brief, 04_depth_classification, 05_glossary_pass_a, 06_video_candidates | generate_evaluate | GENERATOR / EVALUATOR |
| 07_transcript_sync | script | RUN |
| 08_segment_detection | generator, judged by 09 | GENERATOR |
| 09_segment_judge | evaluator_only | EVALUATOR |
| 10_media_selection | script | RUN |
| 11_reconciliation, 12_cluster_pass | generate_evaluate | GENERATOR / EVALUATOR |
| 13_leakage_check | evaluator_only | EVALUATOR |
| 14_bundle_assembly | script | RUN |
| 15_final_validation | script + evaluator | RUN / CROSS_ARTIFACT_REVIEW |
| 15b_stage_gate_ledger | script | RUN |
| 16_final_audit | evaluator_only | INDEPENDENT_AUDIT |
| 16b_registry_merge | script | RUN |

## Done

A batch is done when `16b` has merged and the result is committed and pushed. Tell the user where `batches/<batch_id>/human_spot_check.md` is — that's their review list.
