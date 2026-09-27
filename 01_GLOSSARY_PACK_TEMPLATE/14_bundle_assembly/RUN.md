# 14_bundle_assembly — script, no model

```bash
python3 00_GLOSSARY_PIPELINE_CORE/scripts/assemble_bundles.py batches/<batch_id>
```

Refuses to run while `leakage_audit_report.json` has blocking issues. Splits the draft into one `path_glossary_bundle.<path_id>.json` per path — the files the Final Schema consumes — in TOC order, attaches each concept's `cluster_ref`, and counts concepts, videos, segments and tiers.

Gate: `update_ledger.py batches/<batch_id> record 14_bundle_assembly "path_glossary_bundle.*.json" PASS`
