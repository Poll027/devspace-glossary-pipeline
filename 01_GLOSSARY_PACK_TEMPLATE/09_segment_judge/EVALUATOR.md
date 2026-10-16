# 09_segment_judge — EVALUATOR (evaluator-only)

Fresh context, no access to the detector's reasoning. You write `segment_judgments.json` yourself. **You are the video quality gate** — no human reviews a segment before a learner sees it, so judge the way that person would. Read playbook §14–16.

For **every** proposal in `segment_proposals.json`:

1. Open `video_bank/transcripts/<video_id>.json` and read the range yourself, plus about 30 seconds either side. Open the catalogue's chapters. The 30-second margin is for Core/HIGH-video_need concepts; for Standard/Reference proposals with no flagged `issues`, a tighter margin (10-15s) is fine unless something there makes you widen it.
2. **Hard rejections** (§16): contradicts the concept's evidence → `rejected_inaccurate`; understanding it needs a `blocked_knowledge_ids` concept → `rejected_prerequisite_leak`; opens mid-thought or leans on earlier parts → `rejected_needs_prior_context`; not about this concept → `rejected_off_topic`; not embeddable → `rejected_not_embeddable`; no transcript → `rejected_no_transcript`; cut starts or ends badly and can't be fixed → `rejected_bad_boundaries`; longer than its role needs with no reason → `rejected_too_long`; teaches facts other than the ones claimed → `rejected_fact_mismatch`.
3. **Visual value:** weigh chapters, thumbnail and transcript cues. A pure talking head (`talking_head_only`) is `rejected_weak_visual` unless the concept is genuinely conceptual and the explanation is exceptionally clear.
4. If the content is right but the cut is off, **tighten it** — set `final_start_seconds`/`final_end_seconds` to the range you'd actually use and approve.
5. `confirmed_fact_ids`: only the facts the range really teaches. This can be fewer than proposed.
6. Score all seven dimensions 1–5. `reasoning` cites what you read in the transcript, not the detector's summary.

If your verdicts closely mirror the proposals across the board — every one approved, every fact confirmed — stop and re-read: that pattern usually means you checked the detector's claims instead of the source.

Validate: `schema_check.py segment_judgments.schema.json batches/<batch_id>/segment_judgments.json`, then end your reply with `VERDICT: PASS` (every proposal judged, with reasons) or `VERDICT: FAIL`.

`VERDICT` describes whether you judged every proposal completely and honestly from the transcript — not whether the proposals were good. Rejecting most or all of them, for real stated reasons, is still `VERDICT: PASS`. Only say `FAIL` if you couldn't finish, or you catch yourself mirroring the detector's claims instead of checking the source (see the self-check above).
