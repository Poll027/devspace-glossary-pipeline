import json, hashlib, math
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter, defaultdict

root = Path('batches/glossary_batch_flutter_mobile_developer')
inputs = ['extracted_concepts.json', 'coverage_briefs.json']
e, b = [json.loads((root / name).read_text()) for name in inputs]
key = lambda x: (x['concept_id'], x['path_id'])
briefs = {key(x): x for x in b['briefs']}
assert len(briefs) == len(b['briefs'])
assert len({key(x) for x in e['concepts']}) == len(e['concepts'])
assert set(briefs) == {key(x) for x in e['concepts']}
by_path = defaultdict(list)
for x in e['concepts']:
    by_path[x['path_id']].append(x['dependency_graph_centrality'])
# Rank-based upper quarter; include all concepts tied at the boundary.
cutoffs = {p: sorted(values, reverse=True)[math.ceil(len(values)/4)-1]
           for p, values in by_path.items()}
# Assessment interpretation for lower-centrality concepts: transfer through
# diagnosis, choosing a design, transformation, or coordinating conditions.
# Other lower-centrality targets ask bounded execution of supplied procedures,
# not recall/lookup, so they receive Standard rather than Reference.
application = {
    'flutter.analyzer_diagnostics', 'dart.strings', 'flutter.widget_inspector',
    'dart.iteration', 'flutter.widget_element_identity', 'flutter.reusable_widgets',
    'flutter.form_validation', 'flutter.flexible_layout', 'flutter.layered_layout',
    'flutter.scrolling_layout', 'flutter.responsive_layout', 'flutter.text_scaling',
    'flutter.interaction_targets', 'flutter.list_item_keys', 'flutter.state_ownership',
    'flutter.provider_subscription', 'flutter.provider_lifetime',
    'flutter.app_responsibility_boundaries', 'flutter.widget_test_harness',
    'flutter.widget_find_assert', 'flutter.widget_test_interaction',
    'flutter.flutter_runtime_errors', 'flutter.rest_client_calls',
    'flutter.json_model_mapping', 'flutter.mounted_async_updates',
    'flutter.request_recovery', 'flutter.stale_request_results', 'dart.interfaces',
    'flutter.repository_boundary', 'flutter.async_test_control',
    'flutter.screen_results', 'flutter.route_parameters', 'flutter.invalid_routes',
    'flutter.deep_link_entry', 'flutter.system_back', 'flutter.package_selection',
    'flutter.compatible_dependencies', 'flutter.permission_denial',
    'flutter.device_capability_availability', 'flutter.storage_choice',
    'flutter.local_database_read', 'flutter.local_database_update',
    'flutter.local_database_delete', 'flutter.local_schema_migration',
    'flutter.persistence_failures', 'flutter.client_security_boundary',
    'flutter.firebase_auth_actions', 'flutter.firebase_auth_session',
    'flutter.auth_route_access', 'flutter.firestore_documents',
    'flutter.service_access_failures', 'flutter.local_data_lifetime',
    'flutter.notification_open_navigation', 'flutter.privacy_aware_analytics',
    'flutter.profile_frame_investigation', 'flutter.unnecessary_rebuilds',
    'flutter.bounded_rebuild_fix', 'flutter.resource_lifetime_leaks',
    'flutter.current_release_requirements', 'flutter.store_privacy_disclosures',
    'flutter.review_readiness',
}
assert application <= {x['concept_id'] for x in e['concepts']}
rows = []
for x in e['concepts']:
    c = x['dependency_graph_centrality']
    p = x['path_id']
    cutoff = cutoffs[p]
    evidence = briefs[key(x)]['evidence']
    nf, nm = len(evidence['required_facts']), len(evidence['misconceptions'])
    high = c >= cutoff and c > 0
    applied = x['concept_id'] in application
    tier = 'core' if high or applied else 'standard'
    signal = (f'top quartile for {p} (rank-based cutoff {cutoff}, boundary ties included)'
              if high else f'below the top-quartile cutoff {cutoff} for {p}')
    if high:
        decision = 'Core follows from the path-relative dependency signal; the assessment also requires practical execution, not mere recognition.'
    elif applied:
        decision = 'Core follows from applying or combining the idea to satisfy this concrete scenario (a correction, design choice, transformation, or coordinated outcome), despite low centrality.'
    else:
        decision = 'Standard: this target is bounded execution/configuration of a supplied operation or workflow, rather than transfer through diagnosis or a new design choice. It is not recall/lookup, so zero centrality alone would not justify Reference.'
    reasoning = (f'Centrality {c}, {signal}; TOC sequence position {x["toc_sequence_position"]}. '
                 f'Assessment target: "{x["assessment_target"]}" '
                 f'Required facts {nf}; misconceptions {nm}. {decision} '
                 'Fact count informs explanation breadth but does not independently override these depth signals.')
    rows.append(dict(concept_id=x['concept_id'], path_id=p, depth_tier=tier, reasoning=reasoning))
meta = dict(e['metadata'])
meta.update(artifact_type='depth_classification', artifact_version='1.0.0', schema_version='1.0.0',
            batch_id='glossary_batch_flutter_mobile_developer', model='none',
            prompt_version='04_depth_classification@v1', generated_at=datetime.now(timezone.utc).isoformat(),
            parent_artifact_hashes={name: hashlib.sha256((root/name).read_bytes()).hexdigest() for name in inputs})
out = dict(metadata=meta, batch_id=meta['batch_id'], classifications=rows)
(root/'depth_classification.json').write_text(json.dumps(out, indent=2, ensure_ascii=False)+'\n')
# Own mistakes checklist: exact whole-batch keys; no duplicates; actual input
# centrality/position/assessment and fact/misconception counts in every rationale;
# path-relative quartile with explicit tie treatment; no disposition-based ranking;
# no zero-centrality Reference for application/procedural assessments; exact hashes.
assert len(rows) == len(e['concepts']) == 112
assert len({key(x) for x in rows}) == len(rows)
assert {key(x) for x in rows} == set(briefs)
for x, r in zip(e['concepts'], rows):
    ev = briefs[key(x)]['evidence']
    assert f'Centrality {x["dependency_graph_centrality"]},' in r['reasoning']
    assert x['assessment_target'] in r['reasoning']
    assert f'Required facts {len(ev["required_facts"])}; misconceptions {len(ev["misconceptions"])}.' in r['reasoning']
    assert 'disposition' not in r['reasoning']
    if x['dependency_graph_centrality'] >= cutoffs[x['path_id']] and x['dependency_graph_centrality'] > 0:
        assert r['depth_tier'] == 'core'
for name in inputs:
    assert meta['parent_artifact_hashes'][name] == hashlib.sha256((root/name).read_bytes()).hexdigest()
print('cutoffs:', cutoffs)
print('counts:', dict(Counter(x['depth_tier'] for x in rows)))
print('Self-check passed: exact coverage, unique keys, source signals, tier rules, metadata hashes.')
