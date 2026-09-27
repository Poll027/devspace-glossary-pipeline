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
