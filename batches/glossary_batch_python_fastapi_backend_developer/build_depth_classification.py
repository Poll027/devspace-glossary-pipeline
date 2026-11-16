import collections
import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path

batch = Path('batches/glossary_batch_python_fastapi_backend_developer')
input_names = ['extracted_concepts.json', 'coverage_briefs.json']
inputs = {name: json.loads((batch / name).read_text()) for name in input_names}
concepts = inputs['extracted_concepts.json']['concepts']
briefs = inputs['coverage_briefs.json']['briefs']
key = lambda row: (row['concept_id'], row['path_id'])
assert len({key(c) for c in concepts}) == len(concepts)
assert len({key(b) for b in briefs}) == len(briefs)
assert {key(c) for c in concepts} == {key(b) for b in briefs}
brief_by_key = {key(b): b for b in briefs}
by_path = collections.defaultdict(list)
for c in concepts:
    by_path[c['path_id']].append(c)
# Nearest-rank 75th percentile; keep all ties at the boundary rather than
# arbitrarily choosing concepts with identical centrality.
thresholds = {}
for path, rows in by_path.items():
    scores = sorted(c['dependency_graph_centrality'] for c in rows)
    threshold = scores[math.ceil(0.75 * len(scores)) - 1]
    thresholds[path] = (threshold, sum(s >= threshold for s in scores), len(scores))

# Explicit assessment interpretation, keyed to the frozen sequence. These
# annotations distinguish transfer/application from recognition alone; no
# keyword rule promotes all 'identify' targets or treats security as trivia.
application = {
 1: 'predicting repeated-operation effects for an operation',
 3: 'selecting annotations for required, nullable and collection values',
 5: 'predicting cleanup in success and failure cases',
 6: 'predicting immediate continuation, suspension and resumption for an await',
 7: 'tracing which callable results from decoration',
 8: 'demonstrating interpreter and dependency isolation',
 11: 'determining persistent identity and columns for a mapping',
 12: 'evaluating whether a preflight permits a request',
 13: 'choosing statuses for supplied outcomes',
 14: 'determining which values a model accepts and converts',
 15: 'recreating dependencies from committed declarations',
 16: 'resolving package-qualified imports',
 17: 'evaluating which writes violate integrity constraints',
 18: 'assigning startup and shutdown ownership',
 19: 'interpreting the association represented by a relationship',
 20: 'evaluating whether values satisfy constraints',
 21: 'determining validation locations for nested input',
 22: 'mapping operations to item and collection resources',
 23: 'determining handler selection for a method and path',
 26: 'evaluating validity across multiple fields',
 27: 'determining deliberate rejection responses',
 28: 'choosing an execution context for a library call',
 29: 'determining namespaces after router inclusion',
 30: 'determining requiredness and conversion for request parameters',
 31: 'determining which fields are publicly projected',
 32: 'determining the context supplied to a handler',
 33: 'determining an upstream timeout outcome against a budget',
 35: 'deciding between bounded tasks and durable execution needs',
 36: 'determining provider execution order',
 37: 'predicting both directions of traversal through a configured stack',
 39: 'determining how a request body binds',
 40: 'determining cleanup in both success and failure cases',
 42: 'evaluating outbound requests against network-trust boundaries',
 43: 'rejecting unsuitable multipart input while safely binding values and managing files',
 44: 'evaluating origin and credential combinations for safety',
 45: 'predicting dependency reuse within a request',
 46: 'asserting status and payload together with dependency and lifespan behavior',
 47: 'classifying omitted, explicit-null and supplied input cases',
 49: 'evaluating a request against a host allowlist',
 53: 'determining whether a health failure restarts a process or removes traffic',
 54: 'selecting valid examples and metadata for an actual operation contract',
 55: 'determining which provider runs with an override',
 56: 'determining the binding sources for headers and cookies',
 58: 'verifying counters and latency observations across successful, failing and delayed requests',
 59: 'classifying absent, null and supplied update fields',
 61: 'selecting a resource with a bounded query and distinguishing presence from absence',
 62: 'determining commit and rollback effects',
 63: 'evaluating whether a request supplies a usable bearer credential',
 64: 'choosing cache eligibility and recovering a miss from authoritative storage',
 66: 'choosing indexes for frequent queries',
 68: 'mapping a domain or persistence failure to a public outcome',
 69: 'maintaining consistent error bodies without exposing internal exception data',
 70: 'deciding whether forwarded metadata may be trusted',
 71: 'distinguishing acknowledgement timing from completion of side effects',
 73: 'interpreting traffic, error and latency signals with appropriate labels',
 74: 'choosing stable pagination and filtering with bounded responses',
 76: 'persisting an entity and verifying its generated identity',
 77: 'removing the intended resource and verifying its absence',
 78: 'applying supplied changes without overwriting omitted fields',
 80: 'selecting expiry and invalidation for a stated stale-data tolerance',
 81: 'determining whether cache failure changes authoritative outcomes',
 82: 'determining a rollback release',
 85: 'translating a supplied upstream status or transport failure into a local outcome',
 87: 'choosing diagnostic boundaries from service signals',
 91: 'combining issuer-to-API wiring, verifier configuration and real HTTP acceptance/rejection tests',
 92: 'determining permission for an operation',
 93: 'determining the effects of repeated event identifiers',
 94: 'evaluating authenticated event age',
 95: 'deciding whether to retry and when to stop',
 99: 'distinguishing invalid-token, missing-permission and cross-object rejection cases',
}
recognition = {
 0: 'distinguishing browser restrictions from authentication',
 2: 'distinguishing Content-Type from Accept responsibilities',
 4: 'distinguishing class state from instance state',
 9: 'locating server and application responsibilities',
 10: 'recognizing safe password storage and verification designs',
 24: 'recognizing invalid settings before serving',
 25: 'recognizing client-lifetime mistakes',
 34: 'recognizing misplaced logic and protocol coupling',
 38: 'recognizing development-only serving behavior',
 41: 'recognizing insufficient failure logs',
 48: 'recognizing generated input and output schemas',
 50: 'recognizing credentials in diagnostic output',
 51: 'recognizing leaked sessions and unsafe concurrent sharing',
 52: 'recognizing interrupted work and leaked resources at shutdown',
 57: 'locating rejected input and its outcome',
 60: 'recognizing client-breaking contract changes',
 65: 'detecting unintended schema changes',
 67: 'detecting persistence changes that leak into API contracts',
 72: 'recognizing broken cross-service correlation',
 75: 'recognizing unsafe SQL interpolation',
 79: 'recognizing signature, expiry and contextual verification failures',
 83: 'recognizing missing or misleading documented response cases',
 84: 'recognizing internal disclosure in unexpected errors',
 86: 'recognizing invalid byte signatures',
 88: 'recognizing unbounded expensive operations',
 89: 'recognizing repeated relationship queries',
 90: 'detecting persistence leakage between tests',
 96: 'detecting another user\'s object access',
 97: 'detecting security documentation that misrepresents the deployed flow',
 98: 'recognizing contract drift and sensitive examples',
}
assert set(application).isdisjoint(recognition)
assert set(application) | set(recognition) == set(range(100))
assert len(concepts) == 100
classifications = []
for index, c in enumerate(concepts):
    assert c['toc_sequence_position'] == index
    centrality = c['dependency_graph_centrality']
    threshold, top_count, path_count = thresholds[c['path_id']]
    evidence = brief_by_key[key(c)]['evidence']
    facts = len(evidence['required_facts'])
    misconceptions = len(evidence['misconceptions'])
    in_top = centrality >= threshold and centrality > 0
    tier = 'core' if in_top or index in application else 'standard'
    percentile = (
        f"nearest-rank 75th-percentile threshold {threshold}; all boundary ties included, "
        f"{top_count}/{path_count} concepts qualify"
    )
    assessment = c['assessment_target']
    reasoning = (
        f"Centrality {centrality} for {c['path_id']}, "
        f"{'in' if in_top else 'below'} the path's top-quartile band ({percentile}); "
        f"TOC sequence position {c['toc_sequence_position']}. "
        f"Assessment: {json.dumps(assessment, ensure_ascii=False)}. "
    )
    if index in application:
        reasoning += f"This requires applying the idea to a case by {application[index]}, not merely recalling a definition. "
    else:
        reasoning += f"The stated target emphasizes {recognition[index]}, without explicitly requiring implementation or combining the idea in a new situation. "
    reasoning += f"Coverage has {facts} required facts and {misconceptions} recorded misconceptions. "
    if tier == 'core':
        reasoning += ('Top-quartile centrality independently supports Core.' if in_top else 'Application demanded by the assessment supports Core despite lower centrality.')
    else:
        reasoning += 'Standard: below the top-quartile band and no explicit transfer task; the multi-fact diagnostic/conceptual distinction is more than minor syntax or recall/lookup'
        if centrality == 0:
            reasoning += ', so zero centrality alone does not make it Reference'
        reasoning += '.'
    classifications.append({'concept_id': c['concept_id'], 'path_id': c['path_id'], 'depth_tier': tier, 'reasoning': reasoning})
now = datetime.now(timezone.utc)
metadata = {
    'artifact_type': 'depth_classification', 'artifact_version': '1.0.0',
    'schema_version': '1.0.0', 'batch_id': batch.name,
    'run_id': f'{batch.name}__04_depth_classification__{now.strftime("%Y%m%dT%H%M%SZ")}',
    'prompt_version': '04_depth_classification@v1', 'model': 'none',
    'generated_at': now.isoformat(),
    'source_snapshot_id': inputs['extracted_concepts.json']['metadata']['source_snapshot_id'],
    'parent_artifact_hashes': {str(batch / name): hashlib.sha256((batch / name).read_bytes()).hexdigest() for name in input_names},
}
output = {'metadata': metadata, 'batch_id': batch.name, 'classifications': classifications}
(batch / 'depth_classification.json').write_text(json.dumps(output, ensure_ascii=False, indent=2) + '\n')
# Stage-local mistakes checklist / deterministic cross-references:
# complete unique concept/path coverage; within-path quartiles with declared ties;
# actual assessment/centrality/fact counts; no disposition-based ranking;
# all top-band and transfer targets Core; zero alone never forces Reference;
# hashes cover exactly the two named inputs and metadata uses actual UTC.
assert len(classifications) == len(concepts)
assert len({key(r) for r in classifications}) == len(classifications)
assert {key(r) for r in classifications} == {key(c) for c in concepts}
for c, r in zip(concepts, classifications):
    assert json.dumps(c['assessment_target'], ensure_ascii=False) in r['reasoning']
    assert f"Centrality {c['dependency_graph_centrality']} " in r['reasoning']
    assert 'disposition' not in r['reasoning']
    if c['dependency_graph_centrality'] >= thresholds[c['path_id']][0] and c['dependency_graph_centrality'] > 0:
        assert r['depth_tier'] == 'core'
assert set(metadata['parent_artifact_hashes']) == {str(batch / n) for n in input_names}
print('Thresholds:', thresholds)
print('Rows:', len(classifications), 'Tiers:', dict(collections.Counter(r['depth_tier'] for r in classifications)))
print('Self-check: PASS')
