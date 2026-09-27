# Runbook

## Rollout (playbook §34)

1. **Phase 1 — one path.** Run `data_analyst` alone. Its concepts are fine-grained, tool-heavy and video-friendly, so it tests the video half properly. Before going further, review from `human_spot_check.md`: is the text too long, does video add value, do segments feel standalone, are summaries useful, do clusters feel natural, could the Final Schema build screens without inventing anything?
2. **Phase 2 — five paths.** Record the metrics below per batch, and tune `MAX_SEGMENTS`, the candidate cap and the video-need rules from real numbers.
3. **Phase 3 — scale** to the remaining frozen TOCs once the thresholds and failure modes hold steady.

`software_engineer` is a test path, not one of the 64. It never enters a batch.

## Batch composition

- **Eligibility:** a path enters only if its `toc_workspace` has `freeze_manifest.json`, checked on disk each time. List each path's workspace explicitly, because they don't all live in one folder.
- **Group by career family**, so shared concepts and videos get reused inside the batch (e.g. `data_analyst` with `business_analyst`, which share 9 concepts).
- **Cap by concept volume, not path count.** State the estimate in `batch_run_context.json`.
- **Never batch across the eligibility boundary.** Unfrozen paths wait.

## Two runners, one repo

Each account runs a different batch folder — never two runners on one `batches/<batch_id>/`. Prefer different career families, so the two batches rarely build the same concept at once. The only shared writes are `registry/` and `video_bank/` (through `sync_catalogs.py`, `fetch_videos.py` and `merge_registry.py`):
- Pull before `00_preflight`, so snapshots start from the latest registry.
- Pull again right before `16b`, merge, then commit and push immediately.
- If both batches built evidence for the same concept, the merge keeps whichever landed first and never overwrites. Only the second batch's registry write is skipped — its own bundles keep their facts.
- `video_bank/catalogue/` and `transcripts/` only ever gain new files keyed by `video_id`, so they don't conflict.

## Repairs

Fix the earliest stage that owns the problem, then re-run and re-gate everything downstream. Never patch an artifact downstream of where the problem started. `15b` flags every gate whose artifact changed after it was recorded.

## Cost gates → where they live

| Playbook gate | Implemented by |
|---|---|
| 1 cached source packs | `source_packs/`, built once per career family in 00 |
| 2 variable depth | 04 tiers, which shape 05's length and blocks |
| 3 video-need gate | 05 `video_need`; only HIGH/MEDIUM reach 06 |
| 4 metadata filter | 06 cheap filter, ≤5 kept per concept |
| 5 analyse finalists only | 07 fetches only kept candidates; 08/09 read only those transcripts |
| 6 cache processed videos | `video_bank/catalogue/` + `transcripts/` (fetched once, ever) + `judged_ranges` |
| 7 exploit long videos | 06/08 work tile by tile; one video can serve several adjacent concepts |
| 8 batch by tile | every generator stage works tile by tile |

Plus: reuse via exact `concept_id` (02), deterministic stages as scripts (no model tokens), and video sampling rather than exhaustive re-judging in the final audit.

## Metrics to record per batch (Phase 2)

All derivable from the batch's artifacts: concepts; video-need rate (HIGH+MEDIUM ÷ all); `no_segment_found` rate; candidates per searched concept; approved ÷ proposed segments; open-search rate; transcript availability (`transcript_sync_report`); segment reuse rate and evidence reuse rate (`registry_lookup`); leakage blocks found at 13; evaluator repair rounds per stage; and model usage per stage from your Claude account's usage view.
