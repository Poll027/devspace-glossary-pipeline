# HANDOFF: full context for a model with no prior history

Read this first, then `PROGRESS.md` (live status) and `batches/glossary_batch_001_data_analyst_pilot/orchestrator_notes.md` (detailed log).

## 1. The product

**Devspace** is an AI learning platform with **64 career paths**: data analyst, business analyst, software, cyber, devops, marketing, and non-coding paths. Each path is taught from three layers, built in this order (playbook v3 is the spec):

1. **TOC.** The frozen, ordered concept sequence per path, built upstream by a separate pipeline.
2. **Glossary Learning Bundles**, built by this pack. Each bundle holds:
   - teaching text written from the TOC plus sourced evidence;
   - the best matching **YouTube segments** (specific timestamp ranges from teaching channels) found *after* the text is written and reconciled with it.

   Text must teach on its own: never "as the video shows", and learners can turn video off. Videos are chosen once and stored in the bundle, never generated at runtime. Learners see summaries, not transcripts.
3. **Final Schema.** The main course content, which arranges the bundles. Video segments live only in the glossaries. Interactive diagrams and code sandboxes belong to the main schema, not here.

Principle: **the TOC gives the order, the evidence gives the truth, the glossary is the teaching bank, video is support, and the Final Schema arranges.**

## 2. Upstream: the TOC pipeline (separate project, frozen inputs)

- Pack: `UNIVERSAL_TOC_PIPELINE_PACK_V2_FINAL`, a sibling folder that is not in this repo. v2 exists because v1 was too loose. It spends maximum rigour on the first 2 "pathfinder" paths and is leaner for paths 3–50 to control cost.
- Each path's frozen output is a workspace such as `04_data_analyst_V2_WORKSPACE`, containing:
  - `ordered_concept_sequence.json` with `sequence_index`;
  - a dependency graph;
  - concept atoms;
  - tiles and regions;
  - per concept: `primary_objective`, `assessment_target`, `practice_objective`, `central_mental_model`, `disposition` (almost always `immediate_core`, so useless for depth).
- **Never edit frozen TOC workspaces.** Log TOC problems in `orchestrator_notes.md` under "For the TOC pipeline" for a later upstream fix.
- `software_engineer` was only a test path and is not one of the 64. Real paths have fine-grained concepts, so the planned "term mining" step was removed.
- Cross-path reuse: data_analyst and business_analyst share 9 concept_ids. Reuse is an exact `concept_id` match through the registry.

## 3. This pack: layout

- `CLAUDE.md` is the orchestrator pointer.
- `.claude/agents/`
  - `glossary-generator.md` (Sonnet): reads the stage's GENERATOR.md, validates with schema_check, never invents ids, URLs or facts. Reads PDFs with `curl -sL url -o /tmp/x.pdf && pdftotext`.
  - `glossary-evaluator.md` (Opus): always a fresh context, never sees the generator's reasoning, classifies each defect as BLOCKING or ADVISORY.
- `00_GLOSSARY_PIPELINE_CORE/`
  - `PLAYBOOK_v3.md` is the spec. §5–7 cover the TOC and coverage brief, §8 Pass A (including the Data Cleaning quality benchmark at about line 705), §9 video need, §10+ YouTube.
  - `README.md` records design decisions. `RUNBOOK.md` covers rollout: phase 1 is data_analyst alone, and two runners coordinate through separate batch folders.
  - `pipeline_manifest.json` (v2.0.0) lists the 19 stages with kind, script, outputs and depends_on.
  - `schemas/`: 26 JSON schemas. `schema_check.py` resolves cross-file `$ref`s.
  - `scripts/`, all tested: `extract_concepts.py`, `registry_lookup.py`, `schema_check.py`, `merge_parts.py` (combines chunk parts and rejects duplicates), `update_ledger.py` (`record` / `verify`; detects stale gates by hash), `fetch_videos.py`, `sync_catalogs.py` (yt-dlp flat playlist, no API key), `select_media.py` (max 3 segments, greedy fact coverage), `assemble_bundles.py`, `validate_bundles.py`, `merge_registry.py` (idempotent).
  - `source_packs/data_analytics.source_pack.json`: 130 sources. Other packs are not built yet.
  - `registry/concept_evidence_registry.json` and `video_bank/approved_segments.json` are live and currently empty. **Only scripts write them.**
  - `video_bank/channel_allowlist.json` (43 channels) and `channel_catalogs/` (43 synced catalogues).
- `01_GLOSSARY_PACK_TEMPLATE/` holds stage instructions only (`GENERATOR.md` / `EVALUATOR.md` / `RUN.md` per stage), read in place. `START_HERE.md` is the orchestration loop.
- `batches/<batch_id>/` is one flat folder holding all of a batch's artifacts.

## 4. The 19 stages

The pipeline runs these stages in order:

1. **00 preflight** (generate/evaluate): run context, source pack, snapshots.
2. **01 extraction** (script).
3. **02 registry lookup** (script): status new, reuse_registry or shared_in_batch.
4. **03 coverage brief** (generate/evaluate): sourced required facts per concept, with `source_id#locator`.
5. **04 depth classification** (generate/evaluate): core, standard or reference, from dependency-graph centrality quartiles plus what the assessment demands.
6. **05 Pass A** (generate/evaluate): teaching blocks written before any video, plus a `video_need` call (HIGH, MEDIUM, LOW or NONE, with preferred_visual_modes).
7. **06 video candidates** (generate/evaluate): searches allowlist catalogues first. Open YouTube API search costs 100 quota units against a 10k/day quota, so it is only a fallback.
8. **07 transcript sync** (script): yt-dlp captions (en-orig/en, json3). No transcript means the segment is rejected.
9. **08 segment detection** (generate): judged by stage 09.
10. **09 segment judge** (evaluator only).
11. **10 media selection** (script). `segment_id = seg_<concept>_<video>_<start>_<end>`, which is concept-scoped to avoid collisions.
12. **11 reconciliation** (generate/evaluate): aligns the text with the chosen segments.
13. **12 cluster pass** (generate/evaluate).
14. **13 leakage check** (evaluator only): nothing may need later concepts.
15. **14 assembly** (script): refuses to run while leakage is blocking.
16. **15 final validation** (script, plus the CROSS_ARTIFACT_REVIEW evaluator).
17. **15b ledger verify** (script).
18. **16 independent audit** (evaluator only): the report must be persisted to disk.
19. **16b registry merge** (script).

There is no human gate. At the end, write `human_spot_check.md` for the user.

## 5. Other design decisions (README)

- Visual quality is judged from chapters and thumbnails. Nothing is downloaded or rehosted.
- Reuse is by exact concept_id.
- Deterministic stages are scripts.
- yt-dlp field names are verified: `chapters` (start_time/end_time/title), `playable_in_embed`, `automatic_captions`, `channel_follower_count`, `channel_id`. Installed: yt-dlp 2026.08.19 and poppler.

## 6. Video channel curation (user rules)

- **Teaching channels only.** Exclude news, commentary and career-advice channels (Fireship, Matt Wolfe, YC). Luke Barousse was rejected because about 69 of his 80 videos are career or hype content. Decide in or out; don't include a channel with caveats.
- Channels on the list the user supplied: Code with Mosh, Bro Code, Web Dev Simplified, Hyperplexed (UI), ByteByteGo (systems), Hayk Simonyan, Dave Ebbelaar (AI engineering), NeetCode and Abdul Bari (DSA), Corbin Brown, Tech With Tim, Andrej Karpathy, sentdex, 3Blue1Brown, StatQuest, CS Dojo, CS50, plus others from their image list.
- Added for data analytics: Leila Gharani, MyOnlineTrainingHub, Chandoo (`@chandoo_`), Excel Campus, Data with Baraa, techTFQ, storytelling with data. Retagged: Alex The Analyst, StatQuest, Corey Schafer, freeCodeCamp.
- Still to do: channel discovery for the other career families (cyber, devops, marketing, and so on).

## 7. How we run stages (orchestration rules, all decided with the user)

- **The orchestrator does no stage work itself.** It dispatches generator and evaluator subagents, verifies their output with scripts, and records gates with `update_ledger.py`.
- **Fan-out.** A path of 150+ concepts is split into chunks of about 30 along region boundaries (`chunks.json`):
  - c0_canary: foundations, 5 concepts;
  - c1: Python, 26;
  - c2: stats + pandas, 30;
  - c3: SQL + data modelling + joins, 33;
  - c4: spreadsheets + experimentation, 32;
  - c5: visualisation + stakeholder communication, 30;
  - c6: capstone, 12.

  The canary runs alone first. Its lessons go into the stage's GENERATOR.md checklist before the rest fan out. Each agent writes `<artifact>.part.<chunk>.json`, then `merge_parts.py` combines them. The merged file comes out in chunk order, which doesn't matter because assembly sorts by TOC position.
- **Blocking/advisory gate** (the user's choice, after a fully strict evaluator failed the canary 3 rounds running at about 700k tokens):
  - BLOCKING means an unsupported, contradicted or overstated claim; a missing required fact; later knowledge the learner must *understand*; or a data-integrity break. Only blocking defects fail a round.
  - ADVISORY findings go to the generator **once, with no re-evaluation**. Advisory fixes may **only reword, delete, move or cite, never add a new claim**. The generator skips any advisory that would need a new claim; the evaluator must mark a needed claim BLOCKING.
  - After a blocking FAIL, snapshot the file, send the findings for repair (resuming the same generator is cheaper), then run a **scoped re-check covering only the diff**. When the evaluator has pinned the exact replacement wording, verify by script instead of paying for another evaluator: check the pinned text is present and nothing else changed.
  - **Stop after 3 failed rounds and ask the user.** The user approved "apply the pinned fix plus one narrow check" when the last blocker has pinned wording.
- **Evaluators must give pinned replacement wording for every blocker.** This made repairs converge fast.
- **Concurrency.** Run about 3 agents at once. Running 6 hit session usage limits repeatedly. When an agent dies on a limit or network error, check the file state, then resume it with SendMessage; it keeps its context.
- **Source pack edits are append-only.** Re-read the pack before writing, because parallel chunks append concurrently, and bump `source_count` in the batch's `source_pack_manifest.json`. After a change, re-gate 00, since the ledger marks it stale.

## 8. Lessons learned (folded into the GENERATOR.md checklists)

**Stage 03 (facts):**
- Missing "how-to" facts: every verb in the practice or assessment needs syntax or a procedure.
- Undefined variants the learner must choose between.
- Defaults that change the answer, such as pivot_table averaging and variance dividing by n−1.
- An example's specifics stated as a general rule, such as "the foreign key goes on the many side".
- Dropped hedges.
- The right page cited at the wrong section.
- Wrong editions: **OpenIntro is the 4th edition; use 4th-edition section numbers.**
- Marketing pages used as the only source (the Optimizely glossary). Prefer neutral sources.
- **Every repair round introduced a new blocker**, so repairs must re-open the source for every new or changed fact.

**Stage 05 (prose):**
- Upgraded hedges ("commonly" becoming "almost always").
- Closed lists ("exactly these four checks").
- Added causes or purposes.
- Absolutes.
- **Code that doesn't run**: a one-line `for …: if …:`, a wrong claim about UnboundLocalError, a pivot on the wrong variable, `describe()` said to show "range".
- **Untaught syntax**: `lambda`, conditional expressions, CREATE TABLE.
- Invented tool behaviour (Excel tables auto-updating, approximate VLOOKUP results).
- Statistics misreadings ("significance means probably not chance").

Fixes now in the checklist: run every Python or pandas snippet, trace every SQL or Excel example on the example data, and use only syntax from allowed concepts.

**Video-need rules:** NONE takes an empty `preferred_visual_modes`; LOW may list one simple mode.

Generators still repeat the fact sentence and then add code after a colon. It reads stiffly, but it is advisory.

## 9. Where we are (data_analyst pilot, batch `glossary_batch_001_data_analyst_pilot`)

- **Stages 00–04: gated PASS.**
  - 03: 168 briefs.
  - 04: 42 core, 86 standard, 40 reference; top-quartile centrality is ≥3.
  - Source pack: grew from 50 to 130 sources.
- **Stage 05 (Pass A), by chunk:**
  - **c0_canary: PASS.**
  - **c1:** FAIL with 17 pinned blockers, not yet repaired.
  - **c2:** FAIL with 7, partly repaired.
  - **c3:** FAIL with 6, partly repaired.
  - **c4:** FAIL with 9, not repaired.
  - **c5:** not written; its draft was lost.
  - **c6:** written, not evaluated.

  Findings, round-1 snapshots and the shared prompts are in `batches/…/working/`:
  - `pa_prompt.md` is the generator prompt. Substitute `{CHUNK}` and `{DESC}`.
  - `pa_eval_prompt.md` is the evaluator prompt.

  For c2 and c3, diff the current part against `pa_cN_round1.json` and apply whatever pinned fixes are missing. Then merge and gate 05 (commands in `PROGRESS.md`).
- **Carry-forward items for later stages** (full list in `orchestrator_notes.md`):
  - About 20 TOC conflicts.
  - 10 placeholder objectives: all 5 foundations concepts plus sql string/date/type_casting/coalesce/union.
  - Name/objective conflicts in pandas.creating_dataframes and stats.distribution_shape.
  - The c4 Orders column letters are inconsistent; fix at stage 11 or 16.
  - One ERD wording advisory for stage 16.
  - opentextbc.ca (the database textbook) blocks curl, so read it through the Wayback Machine.
  - The Aqua Book URL is now `gov.uk/guidance/the-aqua-book`.

## 10. What's left

1. Finish stage 05, then run stages 06–16b for data_analyst and write `human_spot_check.md`.
2. The 06–10 video stages have **never run live**. Expect a canary round to shake out instruction bugs.
3. Upstream TOC fixes: send the logged conflicts to the TOC pipeline.
4. Roll out to the other 63 paths (RUNBOOK phases), including source packs and channel discovery for each career family.
5. **Cost.** Claude Max usage is tight: a 168-concept path takes several sessions. The plan is a cheaper **GLM branch** (via OpenRouter) using the same stage files once credits exist. Use Claude for the first run and for evaluation.
6. **Two accounts share this repo.** Only one works at a time: `git pull` before starting, commit and push when stopping.

## 11. User preferences

- Wants the process AI-heavy, with the user doing a final pass only.
- Decide, don't caveat.
- Keep reports brief.
- Persist audit reports to disk.
- Don't loop forever: report after 3 failed rounds.
