# 15_final_validation — script, then CROSS_ARTIFACT_REVIEW.md

```bash
python3 00_GLOSSARY_PIPELINE_CORE/scripts/validate_bundles.py batches/<batch_id>
```

Writes `glossary_validation_report.json`. Mechanical checks (playbook §29): every path has a schema-valid bundle; every TOC concept has one; zero leakage blocks; every required fact taught by a teaching block; no teaching block mentions a video; anchors and segments cite only real facts; context prerequisites match the frozen TOC; each segment's `segment_id`, `youtube_url`, `review_url` and `transcript_ref` derive exactly from its video and cut; no overlapping cuts in a media group; clusters stay inside one tile. Clips over 6 minutes are warnings.

A FAIL names the concept and field. Fix the stage that produced it, rerun from there.

Then run `CROSS_ARTIFACT_REVIEW.md` in this folder (evaluator subagent). It amends this same report.

Gate (after the review): `update_ledger.py batches/<batch_id> record 15_final_validation glossary_validation_report.json PASS|FAIL`
