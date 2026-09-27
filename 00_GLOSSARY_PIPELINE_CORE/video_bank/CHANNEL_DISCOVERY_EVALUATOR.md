Run in a fresh context. Independently verify every proposed channel before it's allowed into `channel_allowlist.json` — this is the only human-judgment-adjacent gate in the entire video system, so it has to be real verification, not a rubber stamp.

**Channel identity.** Confirm each `channel_id` actually resolves to the named channel, not a similarly-named impersonator or a dead/renamed channel.

**Verified stats — look them up yourself, independently.** Do not accept the generator's cited subscriber count or engagement figures at face value, even if they look plausible. Look up the channel's real current stats yourself (YouTube Data API `channels.list`, or a direct check) and write what you actually found into `verified_stats`. A generator-cited number that turns out to be stale, wrong, or invented is a rejection of that channel, not a minor correction.

**Content quality and relevance.** Spot-check a few of the channel's actual video titles/descriptions against the claimed `career_family_ids` — a channel that's nominally relevant but whose real catalog is mostly unrelated content is a rejection.

**Trust tier.** Confirm the recommended `trust_tier` is reasonable given the real verified stats and track record — don't just copy the generator's recommendation.

For every channel that passes, write its entry into `channel_allowlist.json` with `review_state.review_status: "evaluator_verified"` and real `verified_stats`. For anything rejected, state why — this doesn't need its own report file, just don't add it, and note the rejection reason back to whoever is reviewing this maintenance run.
