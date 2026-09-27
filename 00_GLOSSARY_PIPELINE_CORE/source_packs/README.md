# Source Packs

One `<career_family_id>.source_pack.json` per career family (`../schemas/source_pack.schema.json`), built once in `00_preflight` and reused by every batch in that family (playbook §7, cost gate 1). Coverage briefs (stage 03) may cite only sources listed here.

**Seeding:** each frozen TOC workspace has a `source_registry_snapshot.json` of sources the TOC pipeline already approved. Keep its technical references (official docs, specs). Leave out the job postings and certification pages — they scoped the curriculum but don't teach it. Then add the official documentation the concepts actually need, and trusted educational references.

| `source_type` | `trust_tier` | Backs |
|---|---|---|
| `official_docs` | `technical_truth` | definitions, syntax, mechanisms |
| `educational` | `explanation_and_sequencing` | mental models, misconceptions |
| `practitioner` | `realistic_context` | practical use, realistic examples |

Every source needs a real URL that someone opened. Extend a pack when a new concept needs a source it lacks; don't rebuild it per batch.
