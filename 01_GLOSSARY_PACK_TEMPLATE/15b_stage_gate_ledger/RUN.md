# 15b_stage_gate_ledger — script, no model

```bash
python3 00_GLOSSARY_PIPELINE_CORE/scripts/update_ledger.py batches/<batch_id> verify \
  00_preflight 01_extraction 02_registry_lookup 03_coverage_brief 04_depth_classification 05_glossary_pass_a \
  06_video_candidates 07_transcript_sync 08_segment_detection 09_segment_judge 10_media_selection \
  11_reconciliation 12_cluster_pass 13_leakage_check 14_bundle_assembly 15_final_validation
```

The ledger was written one row per stage as each gate passed (`update_ledger.py record`). This re-hashes every gated artifact and exits 1 if any gate is missing, FAIL, or **stale** — the artifact changed after it was gated, so the gate no longer covers what's on disk. Re-gate the stale stage and anything downstream of it.
