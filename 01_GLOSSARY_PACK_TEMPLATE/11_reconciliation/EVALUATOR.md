# 11_reconciliation — EVALUATOR

Fresh context.

- **Segment fields untouched:** for every media segment, `segment_id`, `video_id`, both URLs, times, `fact_ids` and `transcript_ref` match `selected_media.json` exactly. Any difference is a FAIL.
- **Text stands alone:** read only the teaching blocks. Every required fact taught? Any reference to a video?
- **Complement, not echo:** open each segment's transcript range. The text shouldn't re-narrate the clip at length, and it mustn't leave out what the clip doesn't cover.
- **Summaries:** accurate to the range, in Devspace's voice, readable without the video, not lifted from the transcript.
- **Bridge notes** are concrete ("watch how the duplicate row inflates the count"), not generic ("watch the video").
- **Anchors:** every anchor cites real fact ids; assessment anchors reflect the `assessment_target`; the practice anchor is doable with taught knowledge and uses no blocked syntax.
- **Validation flags** are honest.

End with `VERDICT: PASS` or `VERDICT: FAIL` and defects as `concept_id@path_id: field → problem → fix`.
