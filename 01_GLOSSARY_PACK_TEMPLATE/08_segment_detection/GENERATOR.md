# 08_segment_detection — GENERATOR

Produce `segment_proposals.json`. There is no EVALUATOR here — `09_segment_judge` evaluates this output in a fresh context. Read playbook §14–16 and the §28.3 prompt.

**One pass per candidate video**, covering every concept that video is a candidate for. Load its `video_bank/catalogue/<video_id>.json` (chapters, embed flag) and `video_bank/transcripts/<video_id>.json`. Skip into `rejected_videos` when: no transcript (`transcript_available: false`), `playable_in_embed` is false, or the video doesn't actually cover the concept.

**A good range** (§14): starts on a new thought — ideally a creator chapter boundary (`chapter_aligned: true`); explains its subject immediately; needs no earlier context ("as we said earlier", unresolved "this", code whose setup came before); covers the intended facts; finishes its example; ends before the next topic or any blocked concept. Use the shortest range that does the job (§15: mental model 45s–3m, visual mechanism 1–4m, worked example 1.5–5m, live-code or tool demo 2–6m).

**Per proposal:** `label` (what the learner is about to watch, in Devspace terms), `role`, `covered_fact_ids`, and `visual_mode` inferred from chapter titles, thumbnail and transcript cues ("let me draw", "as you can see on screen"). State the visual mode as an inference; the judge weighs it. `transcript_evidence` is a real quote copied from inside the range. List any doubts in `issues`.

**Reuse:** for a candidate that came from a reused segment, re-propose the same range for this path so the judge re-checks this path's prerequisites (§25).

One long, well-chaptered video can legitimately supply ranges for several adjacent concepts (cost gate 7) — propose them all.

Validate: `schema_check.py segment_proposals.schema.json batches/<batch_id>/segment_proposals.json`
