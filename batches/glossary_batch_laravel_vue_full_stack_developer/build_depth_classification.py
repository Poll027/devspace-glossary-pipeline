import collections
import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path

p = Path('batches/glossary_batch_laravel_vue_full_stack_developer')
inputs = ['extracted_concepts.json', 'coverage_briefs.json']
a, b = [json.loads((p / name).read_text()) for name in inputs]
concepts = a['concepts']
briefs = {(x['concept_id'], x['path_id']): x for x in b['briefs']}
assert len(briefs) == len(b['briefs'])
assert {(x['concept_id'], x['path_id']) for x in concepts} == set(briefs)
by_path = collections.defaultdict(list)
for c in concepts:
    by_path[c['path_id']].append(c['dependency_graph_centrality'])
# Nearest-rank 75th percentile, inclusive of ties: positive centrality only.
thresholds = {path: sorted(vals)[math.ceil(.75 * len(vals)) - 1] for path, vals in by_path.items()}

# Assessment readings: routine recognition/interpretation does not itself
# demonstrate transfer; application to supplied inputs, failure evidence,
# access cases, or state changes does. These exceptions are keyed by real IDs.
standard = {
 'composer.locked_dependencies': 'routine distinction between installation and dependency resolution, not scenario-based dependency selection',
 'npm.locked_project_dependencies': 'routine distinction between restoring and changing dependency versions',
 'web.semantic_application_forms': 'checking the taught label and submission conventions, rather than combining them in a new design',
 'laravel.phpunit_execution': 'interpreting runner environment and pass/fail output, rather than designing tests',
 'laravel.basic_scheduled_task': 'routine interpretation of when a declared schedule is due',
 'vitest.vue_test_execution': 'recognition of runner environment and output',
 'laravel.password_hashing': 'recognition of hashing versus plaintext or encoding, not implementation of an authentication flow',
 'php.namespaces_and_imports': 'routine interpretation of a use statement and its class name',
 'vite.spa_dev_server': 'recognition of the development entrypoint and hot-update behavior',
 'composer.psr4_autoloading': 'routine application of the namespace-to-path convention, not resolving a new autoloading failure',
 'laravel.basic_queued_job': 'recognition of the queued input and documented execution boundaries',
 'vue.computed_derivations': 'recognition of derived versus mutable source state',
 'vite.spa_production_build': 'recognition of production artifacts versus development-server output',
 'vue_router.host_history_fallback': 'explaining the taught direct-navigation mechanism, rather than diagnosing a supplied deployment',
 'sanctum.csrf_initialization': 'explaining the taught rejection mechanism, rather than designing or repairing a request flow',
 'api.failure_contracts': 'routine interpretation of the three statuses under an already supplied contract'
}
reference = {
 'laravel.scheduler_operation': 'recall of task declaration versus the external trigger',
 'laravel.queue_worker_operation': 'recall of worker consumption and restart requirements',
 'api.paginated_collections': 'recognition of items and navigation metadata in a page',
 'laravel.controller_dependency_injection': 'recognition of how a declared dependency is resolved'
}
assert set(standard) | set(reference) <= {c['concept_id'] for c in concepts}
rows = []
for c in concepts:
    key = c['concept_id'], c['path_id']
    evidence = briefs[key]['evidence']
    cent = c['dependency_graph_centrality']
    threshold = thresholds[c['path_id']]
    top = cent > 0 and cent >= threshold
    facts, misconceptions = len(evidence['required_facts']), len(evidence['misconceptions'])
    numeric = (f"centrality {cent}; path 75th-percentile cutoff {threshold} "
               f"(nearest-rank, ties included) for {c['path_id']}; "
               f"{'in' if top else 'outside'} the top quartile. "
               f"Assessment: {c['assessment_target']!r}. "
               f"Required facts {facts}; misconceptions {misconceptions}. ")
    if top:
        tier = 'core'
        rationale = 'Positive top-quartile dependency centrality is a sufficient Core signal, regardless of whether this particular assessment is routine.'
    elif c['concept_id'] in reference:
        assert cent == 0
        tier = 'reference'
        rationale = reference[c['concept_id']] + '; zero dependents and a recall/recognition assessment support Reference. Fact count alone does not require Core.'
    elif c['concept_id'] in standard:
        tier = 'standard'
        rationale = standard[c['concept_id']] + '; outside the top quartile, this supports Standard rather than Core.'
        if cent == 0:
            rationale += ' The assessment still requires interpreting a concrete naming convention, not merely recalling an option, so zero centrality does not alone make it Reference.'
    else:
        tier = 'core'
        rationale = ('The assessment requires applying the taught rule to concrete inputs, state changes, contracts, access cases or diagnostic evidence, rather than recalling syntax or an option; this application signal supports Core even outside the top quartile.')
    if misconceptions:
        rationale += ' The recorded misconception additionally warrants explicit corrective teaching.'
    rows.append(dict(concept_id=c['concept_id'], path_id=c['path_id'], depth_tier=tier, reasoning=numeric + rationale))
meta = a['metadata']
result = {
 'metadata': {
  'artifact_type': 'depth_classification', 'artifact_version': '1.0.0', 'schema_version': '1.0.0',
  'batch_id': a['batch_id'], 'run_id': meta['run_id'],
  'prompt_version': '04_depth_classification@v1', 'model': 'none',
  'generated_at': datetime.now(timezone.utc).isoformat(),
  'source_snapshot_id': meta['source_snapshot_id'],
  'parent_artifact_hashes': {name: hashlib.sha256((p / name).read_bytes()).hexdigest() for name in inputs}
 },
 'batch_id': a['batch_id'], 'classifications': rows
}
(p / 'depth_classification.json').write_text(json.dumps(result, indent=2) + '\n')
# Own mistakes checklist: full pair coverage, no duplicate pairs, numeric
# evidence and assessment copied faithfully, path-relative positive quartile,
# reference never substitutes zero centrality for recall, no disposition use,
# actual required-fact/misconception counts, exact hashes and real timestamp.
assert len(rows) == len(concepts) == len(set((r['concept_id'], r['path_id']) for r in rows))
for c, r in zip(concepts, rows):
    assert repr(c['assessment_target']) in r['reasoning']
    if c['dependency_graph_centrality'] > 0 and c['dependency_graph_centrality'] >= thresholds[c['path_id']]:
        assert r['depth_tier'] == 'core'
    if r['depth_tier'] == 'reference':
        assert c['dependency_graph_centrality'] == 0 and c['concept_id'] in reference
assert len(result['metadata']['parent_artifact_hashes']) == 2
print('Rows:', len(rows), 'tiers:', dict(collections.Counter(r['depth_tier'] for r in rows)), 'cutoffs:', thresholds)
