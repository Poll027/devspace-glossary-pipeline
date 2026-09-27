# Devspace Glossary Pipeline v2

Turns each frozen TOC into **Glossary Learning Bundles**: source-backed teaching text plus, where video genuinely helps, precisely cut YouTube segments. The Final Schema then arranges them into screens. The spec is `PLAYBOOK_v3.md` in this folder.

> **TOC = order. Evidence = truth. Glossary = teaching bank. Video = support. Final Schema = arrangement.**

## How it flows

```text
frozen TOC ─► 01 extraction ─► 02 registry lookup ─► 03 coverage brief (facts + sources)
  ─► 04 depth ─► 05 Glossary Pass A (text first, + video need)
  ─► 06 video candidates ─► 07 transcripts ─► 08 segment detection ─► 09 segment judge ─► 10 media selection
  ─► 11 reconciliation (text ↔ video, summaries, bridges, anchors) ─► 12 clusters ─► 13 leakage check
  ─► 14 assembly ─► 15 validation ─► 15b ledger ─► 16 audit ─► 16b registry merge ─► Final Schema
```

The text is written **before** any video is looked at, then reconciled with the chosen segments. Deriving lessons from transcripts would inherit each creator's gaps, order and mistakes (playbook §1). Every bundle's text teaches on its own, because some learners won't watch.

## What the Final Schema receives

`batches/<batch_id>/path_glossary_bundle.<path_id>.json` — one bundle per concept, in TOC order (`schemas/glossary_learning_bundle.schema.json`):

- **context**: TOC position, depth tier, prerequisites, blocked future concepts
- **coverage**: learning objective, required facts with sources
- **teaching_blocks**: purpose-tagged prose, each citing the facts it teaches
- **media**: segments with `video_id`, `youtube_url`, `review_url`, start/end seconds, Devspace summary, fact ids, transcript ref; plus `bridge_note` before/after. `null` when there's no video.
- **assessment_anchors**, **practice_anchor**, **visual_anchor**: what can be checked, practised and shown — never question wording
- teaching notes, `cluster_ref`, validation flags

Plus `clusters`: adjacent concepts that may share one explanation area. Nothing about screens, rewards or UI styling (playbook §4).

## Decisions on top of the playbook

Where these differ from a playbook section, this list wins.

1. **Allowlist first, open search as fallback.** Candidates come from cached catalogues of allowlisted channels (`video_bank/channel_catalogs/`, one request per channel via `yt-dlp`, no API quota). Open YouTube search only when a concept gets fewer than 2 plausible candidates. YouTube's search API allows about 100 searches a day, and catalogue results are real videos by construction.
2. **Visual quality from chapters and thumbnails, not frames.** Nothing is downloaded. Creator chapter markers and the thumbnail, plus transcript cues, are the evidence for "diagrammatic, cleanly edited".
3. **Summaries, not transcripts, for learners.** Transcripts are internal grounding for matching and judging. Learners get the Devspace-written summary as the read-alternative, which avoids republishing creators' caption text.
4. **No transcript → segment rejected.** Replaces playbook §30's manual-verification path, so the pipeline never waits on a human.
5. **Reuse by exact `concept_id`.** The TOC pipeline already gives a shared concept one id across paths, so reuse is a lookup, not fuzzy matching. Canonical evidence and approved segments are reused; per-path text, examples and anchors are always written fresh (§25).
6. **A segment's identity is concept + video + cut** (`seg_<concept>_<video>_<start>_<end>`). Fact ids are per concept, so one clip serving two concepts is two records.
7. **Depth comes from dependency-graph centrality.** The TOC's `disposition` field is nearly always `immediate_core` and carries no depth.
8. **No human gate.** Fresh-context evaluators are the gates. Humans review afterwards from `batches/<batch_id>/human_spot_check.md` (review links, lowest scores first).
9. **Deterministic stages are scripts** (`scripts/`): extraction, registry lookup, transcript sync, media selection, assembly, mechanical validation, the ledger and the merge. URLs, segment ids and hashes are always computed, never typed by a model.

## Runners

- **Now: Claude agents.** `.claude/agents/glossary-generator.md` (Sonnet) and `glossary-evaluator.md` (Opus), orchestrated by the main Claude Code session per `01_GLOSSARY_PACK_TEMPLATE/START_HERE.md`. Each subagent starts in its own context, which is exactly what the fresh-evaluator rule needs.
- **Later: GLM branch.** Stage instructions are model-agnostic. A GLM runner reads the same `GENERATOR.md` / `EVALUATOR.md` files and calls the same scripts; only the dispatch layer changes. Keep evaluators on the stronger model when mixing — earlier calibration showed GLM misses subtler defects.

## Layout

```text
00_GLOSSARY_PIPELINE_CORE/
  PLAYBOOK_v3.md  README.md  RUNBOOK.md  pipeline_manifest.json
  schemas/        one JSON Schema per artifact
  scripts/        the deterministic stages + schema_check.py
  registry/       concept_evidence_registry.json (canonical facts per concept)
  source_packs/   curated sources per career family
  video_bank/     channel allowlist, channel catalogues, video catalogue, transcripts, approved segments
01_GLOSSARY_PACK_TEMPLATE/   stage instructions (00_preflight … 16b_registry_merge), START_HERE.md
batches/<batch_id>/          every artifact of one batch (created per run)
.claude/agents/              Claude subagent definitions
```
