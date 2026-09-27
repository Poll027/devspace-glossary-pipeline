# Devspace Glossary Pipeline

This repo turns frozen Devspace TOCs into Glossary Learning Bundles (teaching text + matched YouTube segments) for the Final Schema.

To run or continue a batch, follow `01_GLOSSARY_PACK_TEMPLATE/START_HERE.md` exactly. You are the orchestrator: dispatch stage work to the `glossary-generator` and `glossary-evaluator` subagents and run scripts; don't do stage work in your own context.

The spec is `00_GLOSSARY_PIPELINE_CORE/PLAYBOOK_v3.md`; the decisions that override it are in `00_GLOSSARY_PIPELINE_CORE/README.md`.

Never edit frozen TOC workspaces. Never hand-edit `registry/`, `video_bank/approved_segments.json` or a ledger — scripts own those.
