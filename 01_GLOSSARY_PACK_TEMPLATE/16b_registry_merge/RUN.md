# 16b_registry_merge — script, no model

Pull the latest shared repo first — another runner may have merged since your preflight.

```bash
python3 00_GLOSSARY_PIPELINE_CORE/scripts/merge_registry.py batches/<batch_id> 00_GLOSSARY_PIPELINE_CORE
```

Refuses unless the audit verdict is PASS or PASS_WITH_NONBLOCKING_CHANGES and every gated stage is PASS and not stale. Then:
- adds this batch's **new** canonical evidence to `registry/concept_evidence_registry.json`, and records which paths use each concept;
- adds every shipped segment to `video_bank/approved_segments.json`, or records the new path against a segment that's already there;
- appends every judged range to its video's catalogue entry, so no later batch re-judges the same cut for the same concept.

Existing registry entries are never overwritten. Re-running is safe. Commit and push right after, so the next batch's preflight snapshots the richer registry — that's what makes it cheaper.
