Run this occasionally — when a career family has no allowlisted channel yet, or coverage feels thin — not as part of every glossary batch. Produces proposed additions to `channel_allowlist.json` (`../schemas/channel_allowlist.schema.json`).

For the target career family, research real, currently-active YouTube channels known for high-quality, high-engagement programming/technical education content relevant to it — general-audience channels (freeCodeCamp, Code with Mosh, W3Schools) and, where useful, narrower ones for a specific framework or tool this career family leans on. Use actual web research, not just recalled names — channel activity and standing change over time, and a channel that was prominent two years ago may be inactive now.

For each proposed channel, provide:
- `channel_id` — the real YouTube channel ID (not a guessed or constructed one — verify it resolves to the actual channel).
- `channel_name`, `career_family_ids`.
- A `trust_tier` recommendation (`high` for well-established, long-track-record channels; `standard` otherwise) — this is a recommendation for the evaluator to check, not a self-certified fact.
- Your own reasoning for why this channel fits: content quality, relevance, and real engagement signals you found (subscriber count, upload consistency), cited to where you found them.

Do not fabricate a subscriber count or engagement figure — if you cite a number, it must come from something you actually looked up this session, not from memory. The evaluator re-verifies every number independently regardless, but a knowingly made-up number in your own reasoning is worse than admitting you didn't check.
