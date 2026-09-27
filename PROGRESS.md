# Progress — data_analyst pilot (glossary_batch_001)

Status as of 2026-09-27. Read this first, then `CLAUDE.md` and `01_GLOSSARY_PACK_TEMPLATE/START_HERE.md`.

## What this is

This pack turns a frozen TOC into Glossary Learning Bundles: teaching text plus matched YouTube segments. It follows `00_GLOSSARY_PIPELINE_CORE/PLAYBOOK_v3.md` through the 19 stages in `pipeline_manifest.json`.

The first run is the `data_analyst` path: 168 concepts, in batch folder `batches/glossary_batch_001_data_analyst_pilot/`.

## Done — gated PASS in `glossary_stage_gate_ledger.json`

| Stage | Result |
|---|---|
| 00 preflight | The source pack grew from 50 to **130** checked sources during stage 03, and 00 was re-gated. |
| 01 extraction, 02 registry lookup | 168 concepts, all new. |
| 03 coverage briefs | `coverage_briefs.json`, 168 briefs. Every chunk needed 2–3 repair rounds. |
| 04 depth classification | 42 core / 86 standard / 40 reference. |

## In progress — stage 05 (Glossary Pass A: the teaching text)

The work is split into chunks (see `chunks.json`). Each chunk writes `glossary_pass_a.part.<chunk>.json`.

| Chunk | Concepts | State | Next step |
|---|---|---|---|
| c0_canary | 5 foundations | **PASS** | none |
| c1 | 26 Python | FAIL, 17 blockers, **not yet repaired** | Repair from `working/findings_05_c1.md` |
| c2 | 30 stats + pandas | FAIL, 7 blockers, **partly repaired** | Diff against `working/pa_c2_round1.json`, finish the remaining fixes |
| c3 | 33 SQL + data modelling | FAIL, 6 blockers, **partly repaired** | Diff against `working/pa_c3_round1.json`, finish the remaining fixes |
| c4 | 32 spreadsheets + experimentation | FAIL, 9 blockers, **not yet repaired** | Repair from `working/findings_05_c4.md` |
| c5 | 30 visualization + stakeholder communication | **not written** (the draft was lost when the run stopped) | Generate with `working/pa_prompt.md` (`{CHUNK}` = c5) |
| c6 | 12 capstone | written, **not yet evaluated** | Evaluate with `working/pa_eval_prompt.md` (`{CHUNK}` = c6) |

Every blocking finding comes with pinned replacement wording. After each repair:
1. Diff the part file against its round-1 snapshot.
2. Confirm the pinned text is present and nothing else changed.
3. Mark the chunk passed.

Once all 7 chunks have passed:

```bash
python3 00_GLOSSARY_PIPELINE_CORE/scripts/merge_parts.py batches/glossary_batch_001_data_analyst_pilot glossary_pass_a.json glossary_pass_a.schema.json
python3 00_GLOSSARY_PIPELINE_CORE/scripts/update_ledger.py batches/glossary_batch_001_data_analyst_pilot record 05_glossary_pass_a glossary_pass_a.json PASS --generator claude-sonnet-5 --evaluator claude-opus-5-5 --unresolved 0
```

## Still to do after stage 05

- **06:** video candidates. Search the allowlisted channel catalogues first.
- **07:** transcript sync (script).
- **08/09:** segment detection and judgement.
- **10:** media selection (script).
- **11:** reconciliation.
- **12:** clusters.
- **13:** leakage check.
- **14:** assembly.
- **15:** validation.
- **15b:** ledger.
- **16:** independent audit.
- **16b:** registry merge.
- **At the end:** write `human_spot_check.md` for the user.

## How we work (rules decided so far)

- **Agents.** `.claude/agents/glossary-generator.md` runs on Sonnet; `glossary-evaluator.md` runs on Opus and always starts in a fresh context.
- **Gate.** Only BLOCKING defects fail a round. ADVISORY findings go to the generator once, with no re-evaluation.
  - Advisory fixes may only reword, delete, move or cite. They must never add a new claim.
  - A re-check after a repair covers only the diff.
  - Pinned-wording repairs can be verified by script.
  - After 3 failed rounds, stop and ask the user.
- **Batching.** Run about 3 agents at a time. Running 6 at once repeatedly hit session limits.
- **Checklists.** Each stage's `GENERATOR.md` carries a checklist of "mistakes made". The most common are prose saying more than its source (upgraded hedges, closed lists, added causes) and code that doesn't run. Run or trace every snippet, and use only syntax the course has already taught.
- **Content.** Teaching channels only (no news or commentary channels). The text must teach on its own and never mention video.

## Known issues logged for later

`orchestrator_notes.md` holds three kinds of issue for later:
- About 20 TOC conflicts to fix upstream in the TOC pipeline, mostly practice tasks that need a concept taught later.
- Placeholder objectives.
- Deferred advisories. One example: the Orders column letters differ between the c4 spreadsheet entries.

## Two-account coordination

Only one account works on the batch at a time. Run `git pull` before starting, and commit and push when you stop.
