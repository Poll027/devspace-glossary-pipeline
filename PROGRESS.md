# Progress — data_analyst pilot (glossary_batch_001)

Status as of 2026-10-16. Read this first, then `CLAUDE.md` and `01_GLOSSARY_PACK_TEMPLATE/START_HERE.md`.

## What this is

This pack turns a frozen TOC into Glossary Learning Bundles: teaching text plus matched YouTube segments. It follows `00_GLOSSARY_PIPELINE_CORE/PLAYBOOK_v3.md` through the 19 stages in `pipeline_manifest.json`.

The first run is the `data_analyst` path: 168 concepts, in batch folder `batches/glossary_batch_001_data_analyst_pilot/`.

## Done — gated PASS in `glossary_stage_gate_ledger.json`

| Stage | Result |
|---|---|
| 00 preflight | Source pack grew to 130 sources during stage 03; re-gated. |
| 01 extraction, 02 registry lookup | 168 concepts, all new. |
| 03 coverage briefs | `coverage_briefs.json`, 168 briefs. |
| 04 depth classification | 42 core / 86 standard / 40 reference. |
| 05 glossary pass A | `glossary_pass_a.json`, 168 entries — the teaching text. |
| 06 video candidates | `video_candidates.json`, 96 concepts searched (HIGH/MEDIUM only), 310 candidates, 239 kept. |
| 07 transcript sync | 208 unique videos fetched into the shared `video_bank/` (207 catalogue entries, 204 with transcripts). One video permanently failed (429s); its concept has 2 other candidates. |

## In progress — stage 08/09 (segment detection + judgment)

Fanned out by **video**, not by concept (`chunks_08.json`): a 5-video canary plus 6 chunks of ~32–34 videos.

| Chunk | Detection (`segment_proposals.part.<chunk>.json`) | Judgment (`segment_judgments.part.<chunk>.json`) |
|---|---|---|
| c0_canary | done | done |
| c1 | done | done |
| c2 | done | done |
| c3 | done | done |
| c4 | done | done |
| c5 | done (35 proposals, 4 rejected by the detector) | **not started** |
| c6 | **not started** | **not started** |

**Next steps:** judge c5, detect+judge c6, then:
```bash
python3 00_GLOSSARY_PIPELINE_CORE/scripts/merge_parts.py batches/glossary_batch_001_data_analyst_pilot segment_proposals.json segment_proposals.schema.json
python3 00_GLOSSARY_PIPELINE_CORE/scripts/merge_parts.py batches/glossary_batch_001_data_analyst_pilot segment_judgments.json segment_judgments.schema.json
python3 00_GLOSSARY_PIPELINE_CORE/scripts/update_ledger.py batches/glossary_batch_001_data_analyst_pilot record 08_segment_detection segment_proposals.json PASS
python3 00_GLOSSARY_PIPELINE_CORE/scripts/update_ledger.py batches/glossary_batch_001_data_analyst_pilot record 09_segment_judge segment_judgments.json PASS
```
Prompts for both roles are in `batches/glossary_batch_001_data_analyst_pilot/working/sd_prompt.md` (detector) and `sj_prompt.md` (judge) — both carry the accumulated lessons from c0–c4 (don't pre-trim fact-bearing content; verify exact cut timestamps; flag factual errors in the source video, not just gaps).

Across c0–c4, the judge has rejected content for real reasons on **19 of 162** proposals so far — wrong arithmetic, backwards claims, prerequisite leaks, videos that don't actually demonstrate what their title promises. Several concepts now have no approved video (will need text-only coverage): `viz.seaborn_dataframe_plotting`, `capstone.building_dashboard_or_viz`, among others logged in `orchestrator_notes.md`.

## Still to do after stage 09

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
  - Pinned-wording repairs can be verified by script, without spending another full evaluator round.
  - After 3 failed rounds, stop and ask the user. A single blocker with pinned wording may get one more narrow fix + check instead of stopping.
  - **Stage 08/09 is evaluator-only on the judge side** — there is no repair loop. The judge's own `VERDICT: PASS/FAIL` means "did I judge honestly and completely," not "did every proposal pass." Rejected proposals are the stage doing its job.
- **Batching.** Run about 3 agents at a time. Running 6+ at once repeatedly hit session limits.
- **Checklists.** Each stage's `GENERATOR.md` carries a checklist of "mistakes made." Run or trace every snippet/query/formula; verify exact cut-boundary timestamps rather than estimating; a video can state something factually wrong, not just omit a fact.
- **Content.** Teaching channels only. A good video from a bad channel (career-advice/vendor/news) is rejected even if that one video teaches well.
- **Tools.** `00_GLOSSARY_PIPELINE_CORE/scripts/search_catalogs.py` is the keyword search over the 43-channel video allowlist — use it instead of reading catalogue files directly. `fetch_videos.py` has a client-fallback retry (default → android) for one-off 429s.

## Moving to AWS Bedrock (in progress, 2026-10-16)

Hit Claude usage-limit risk; moving the generator role off the Claude Max-plan subscription.
- **Final architecture decision:** GLM 5.3 (via Bedrock) runs the generator role; **Claude (Opus) stays the evaluator** — the generator/evaluator split is unchanged, only the generator's model changes. Claude Code can't run a third-party model directly, so GLM generation needs a standalone script calling Bedrock's API; Claude Code itself is unaffected (billed through the Max subscription, not a usage-limit risk on its own).
- **Evaluator cost control** (added below, 2026-10-16): since GLM generation is cheap/fast, the risk flips to the Opus evaluator over-spending. Six rules are now baked into `01_GLOSSARY_PACK_TEMPLATE/START_HERE.md` (`## Evaluation cost control`) and into the individual stage files (03, 05, 06, 08, 09, 16) — mechanical checks before any evaluator call, generator self-check against its own mistakes checklist, depth scaled to concept tier/stakes, canary-then-sample across a stage's own chunks, an explicit ceiling next to every "at least N" sampling floor, and the evaluator-only `VERDICT` meaning "did I check honestly," not "did everything pass." Stages 13 (leakage) and 15 (cross-artifact review) were deliberately left as-is — already either exhaustive-by-design or tier-sampled.
- AWS CLI/credentials were **not yet configured** in the working environment as of 2026-10-16 — needed before GLM generation can run. The boto3 script for the GLM generator role has not been written yet.

## Known issues logged for later

`orchestrator_notes.md` holds the running list: ~20 TOC conflicts to fix upstream, placeholder objectives, deferred advisories (e.g. the c4 Orders column-letter inconsistency, now fixed within c4 but not cross-checked against other chunks), and content gaps where no video covers a required fact (text already covers these independently — not a defect, see playbook §18).

## Two-account / multi-compute coordination

Only one compute path works on the batch at a time. `git pull` before starting, commit and push when you stop. GitHub: `Poll027/devspace-glossary-pipeline`.
