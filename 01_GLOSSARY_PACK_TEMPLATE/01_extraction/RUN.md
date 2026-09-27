# 01_extraction — script, no model

```bash
python3 00_GLOSSARY_PIPELINE_CORE/scripts/extract_concepts.py batches/<batch_id>/batch_run_context.json batches/<batch_id>/extracted_concepts.json
```

Copies each concept's TOC position, tile, prerequisites, allowed/blocked knowledge, dependency centrality and objectives (`primary_objective`, `assessment_target`, `practice_objective`, `central_mental_model`) out of the frozen TOC. Schema-validated before writing. A non-zero exit means a TOC workspace is incomplete — fix the input, never hand-edit the output.

Gate: `update_ledger.py batches/<batch_id> record 01_extraction extracted_concepts.json PASS`
