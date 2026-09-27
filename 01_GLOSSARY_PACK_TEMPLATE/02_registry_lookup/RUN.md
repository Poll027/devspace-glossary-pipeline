# 02_registry_lookup — script, no model

```bash
python3 00_GLOSSARY_PIPELINE_CORE/scripts/registry_lookup.py batches/<batch_id>/extracted_concepts.json \
  batches/<batch_id>/concept_evidence_registry_snapshot.json batches/<batch_id>/approved_segments_snapshot.json \
  batches/<batch_id>/registry_lookup.json
```

Per (concept, path): `new` (this path builds the canonical evidence), `reuse_registry` (an earlier batch built it — copy it), or `shared_in_batch` (another path in this batch builds it). Exact `concept_id` match only — the TOC pipeline already gives a shared concept the same id in every path. Also lists approved segments already in the video bank for each concept.

Gate: `update_ledger.py batches/<batch_id> record 02_registry_lookup registry_lookup.json PASS`
