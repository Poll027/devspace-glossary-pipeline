# 00_preflight — GENERATOR

Set up `batches/<batch_id>/` so every later stage runs against a fixed, verified starting state. Report facts you checked on disk, never facts you assume.

1. **Prerequisites.** `yt-dlp --version` and `python3 -c "import jsonschema, referencing"` both succeed. If not, stop and report which is missing.

2. **Batch context.** Copy `01_GLOSSARY_PACK_TEMPLATE/00_inputs/batch_run_context.template.json` to `batches/<batch_id>/batch_run_context.json` and fill every `[[ AUTHOR ]]`. For each path, confirm `freeze_manifest.json` exists in its `toc_workspace` — check the file, not a status note. Apply the batching rule in `00_GLOSSARY_PIPELINE_CORE/RUNBOOK.md`. `software_engineer` is a test path and never enters a batch.

3. **Source packs** (playbook §7). For each career family in the batch, `00_GLOSSARY_PIPELINE_CORE/source_packs/<career_family_id>.source_pack.json` must exist and validate (`python3 00_GLOSSARY_PIPELINE_CORE/scripts/schema_check.py source_pack.schema.json <file>`). If it's missing, build it:
   - Seed from each path's own `<toc_workspace>/source_registry_snapshot.json` — keep the technical references (official docs, specs); leave out job postings and certification pages, which scoped the TOC but don't teach.
   - Add the official documentation the path's concepts actually need (e.g. pandas, SQL dialect, Excel docs for data paths), then trusted educational references.
   - Every source must have a real URL you opened this session. `trust_tier`: official docs → `technical_truth`, educational → `explanation_and_sequencing`, practitioner → `realistic_context`.
   Then write `source_pack_manifest.json`: `{"batch_id", "packs": [{"career_family_id", "file", "source_count"}]}`.

4. **Snapshots.** Copy, byte for byte:
   - `00_GLOSSARY_PIPELINE_CORE/registry/concept_evidence_registry.json` (or its `.EMPTY_TEMPLATE.json` on the very first batch) → `concept_evidence_registry_snapshot.json`
   - `00_GLOSSARY_PIPELINE_CORE/video_bank/approved_segments.json` (or `.EMPTY_TEMPLATE.json`) → `approved_segments_snapshot.json`
   These snapshots are what this batch reads. The live files may change under another runner; the snapshots may not.

5. **Channel catalogues.** Every channel in `video_bank/channel_allowlist.json` must have `video_bank/channel_catalogs/<channel_id>.json`. For any missing, run `python3 00_GLOSSARY_PIPELINE_CORE/scripts/sync_catalogs.py 00_GLOSSARY_PIPELINE_CORE/video_bank <channel_id> ...`.

Do not touch any TOC workspace. This stage reads and copies; it generates no teaching content.
