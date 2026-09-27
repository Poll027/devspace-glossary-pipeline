# 06_video_candidates — EVALUATOR

Fresh context.

- **Coverage:** exactly the HIGH/MEDIUM concepts have a search; none of the others do.
- **Real videos only:** every allowlist or reused candidate's `video_id` appears in its catalogue file or in `approved_segments_snapshot.json`. For open-search candidates, confirm each exists: `yt-dlp --skip-download --get-title https://www.youtube.com/watch?v=<id>`. An invented or unresolvable id is a FAIL.
- **Routing:** open search was used only where the allowlist genuinely came up short. Check a few of those concepts' catalogues yourself for an obvious miss.
- **Filter quality:** kept candidates plausibly contain this concept at this level; nothing kept is news or commentary; rejection reasons are specific.
- **Not popularity-driven:** a big channel's loosely related video mustn't outrank a precise match.

End with `VERDICT: PASS` or `VERDICT: FAIL` and the defects.
