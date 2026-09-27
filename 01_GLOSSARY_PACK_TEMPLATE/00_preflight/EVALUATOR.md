# 00_preflight — EVALUATOR

Fresh context. Re-check everything the generator claims, on disk.

- **Eligibility:** every `toc_workspace` in `batch_run_context.json` contains `freeze_manifest.json`. `software_engineer` absent. A path failing this is a FAIL.
- **Batching rule** (`RUNBOOK.md`): paths grouped by family, concept-volume estimate justified with a real number, no path included "in advance".
- **Source packs:** each file exists and validates. Open at least a third of the source URLs yourself — a dead link, a job posting, or a source that isn't what its title says is a FAIL for that pack.
- **Snapshots:** `shasum -a 256` of each snapshot equals the live file it was copied from (or the empty template). Any difference is a FAIL.
- **Catalogues:** every allowlisted channel has a catalogue file with at least one video.
- **Prerequisites:** run the two commands yourself.

End your reply with `VERDICT: PASS` or `VERDICT: FAIL` followed by each failing item.
