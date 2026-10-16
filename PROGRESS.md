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

## Done — stage 08/09/10 (gated PASS 2026-10-16)

- **08/09:** all 7 chunks merged. 203 proposals, 174 approved, 29 rejected (inaccurate 9, prerequisite leak 5, needs prior context 4, fact mismatch 4, off topic 2, weak visual 2, no transcript 2, too long 1). 34 detector-side rejected videos.
- **Detectors:** c0–c5 Claude Sonnet 5 subagent; c6 Claude Sonnet 4.6 via Bedrock (`scripts/glm_generate.py`). Judge: Opus for all chunks. The judge changed the cut on most approvals — detector ranges run long (sponsor reads, mid-sentence ends).
- **ztHopE5Wnpc:** its transcript timing is broken past ~17800s (cues 1s-spaced, no longer match video time). Don't source from it past ~17400s.
- **10 media selection:** `selected_media.json` — 85 selected, 72 `no_video_needed`, 11 `no_segment_found` (text-only).
- `datamodel.normalization_basics` has no approved video (both proposals rejected); the judge suggests re-sourcing from 314s onward in `rBPQ5fg_kiY`.

## Still to do after stage 10

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
- **Bedrock status (2026-10-16):** a Bedrock API key works (`AWS_BEARER_TOKEN_BEDROCK`, `AWS_REGION`, `GLM_MODEL_ID` in the gitignored `.env`). GLM 5.3, every OpenAI GPT-5.x/6.x and Claude >= 4.7 return AccessDenied "not available for this account" (account/billing-level; AWS Support case needed). Working: Claude 4.x (Sonnet 4.6, Opus 4.6...) and `gpt-oss-*`. gpt-oss-120b detection was too conservative; Sonnet 4.6 was close to Sonnet 5. Run the script with `~/ai-env/bin/python` (boto3, jsonschema live there). `glm_generate.py` covers stage 08 only.

## Known issues logged for later

`orchestrator_notes.md` holds the running list: ~20 TOC conflicts to fix upstream, placeholder objectives, deferred advisories (e.g. the c4 Orders column-letter inconsistency, now fixed within c4 but not cross-checked against other chunks), and content gaps where no video covers a required fact (text already covers these independently — not a defect, see playbook §18).

## Two-account / multi-compute coordination

Only one compute path works on the batch at a time. `git pull` before starting, commit and push when you stop. GitHub: `Poll027/devspace-glossary-pipeline`.
