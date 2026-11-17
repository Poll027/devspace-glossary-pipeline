import json
import hashlib
import math
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

BASE = Path('batches/glossary_batch_aws_devops_engineer')
INPUTS = ['extracted_concepts.json', 'coverage_briefs.json']
raw = {name: (BASE / name).read_bytes() for name in INPUTS}
extracted = json.loads(raw[INPUTS[0]])
coverage = json.loads(raw[INPUTS[1]])
concepts = extracted['concepts']
briefs = {(b['concept_id'], b['path_id']): b for b in coverage['briefs']}
by_path = defaultdict(list)
for c in concepts:
    by_path[c['path_id']].append(c)
cutoffs = {}
for path, members in by_path.items():
    scores = sorted((c['dependency_graph_centrality'] for c in members), reverse=True)
    cutoffs[path] = scores[math.ceil(len(scores) / 4) - 1]

# Assessment-specific application signals, independently reviewed against each
# input assessment. Indices refer to the unchanged extracted TOC order.
application = {
    1: 'diagnosing overlap and capacity errors in a supplied topology applies CIDR reasoning to a scenario',
    2: 'assigning responsibilities for a proposed platform choice applies the ownership model to that choice',
    3: 'selecting a destination route and subnet association applies routing to a specific topology',
    5: 'assigning operational duties for a supplied service applies the responsibility boundary to that service',
    6: 'classifying a supplied constraint as scaling or redundancy requires a scenario-specific decision',
    8: 'deciding allow or deny under supplied policy conditions applies policy evaluation to a request',
    11: 'predicting matches for supplied events applies pattern logic to new event examples',
    15: 'rejecting malformed inputs and out-of-scope targets applies safety criteria before mutation',
    16: 'interpreting a change set to identify additions, modifications and replacements applies change-impact reasoning before execution',
    17: 'distinguishing permitted and denied attempts applies the MFA requirement to access evidence',
    18: 'deciding whether a named principal can assume a role applies trust conditions to a request',
    19: 'identifying policy-violating root usage applies the supplied account policy to observed access',
    21: 'grouping tagged charges and identifying unallocated spend interprets supplied cost evidence',
    23: 'validating a service change and restoring the prior configuration on failure combines validation with a conditional recovery response',
    24: 'justifying a delivery strategy for a stated workload applies availability and rollback requirements to a choice',
    26: 'predicting an alarm state combines samples, timing, evaluation count and missing-data policy',
    28: 'determining and enforcing traffic rules applies a supplied security baseline to workload requirements',
    30: 'evaluating resource-policy permission applies policy conditions to a supplied request',
    35: 'identifying a Pod lifecycle failure combines status, events and logs into a diagnosis',
    37: 'recovering a previous object version after overwrite or deletion applies versioning to a recovery scenario',
    42: 'identifying a supported delivery bottleneck requires interpretation of supplied evidence rather than naming metrics',
    43: 'identifying a violated rule, affected resource and safe next action combines evidence with response selection',
    44: 'comparing template and live state applies drift interpretation to a supplied property difference',
    45: 'identifying an update failure while verifying restoration combines failure evidence with recovery-state checks',
    48: 'accepting an approved workflow and rejecting other repositories or branches applies federation restrictions to contrasting requests',
    50: 'selecting the least permissions needed applies authorization reasoning to a particular event target',
    51: 'detecting noncompliance without false positives applies a rule to contrasting supplied configurations',
    58: 'diagnosing a listener, target or health-check mismatch combines request-path evidence',
    63: 'identifying the decisive missing allow, deny or condition requires evidence-based policy diagnosis',
    67: 'classifying retryable versus terminal failures and reporting the outcome applies error handling to failure cases',
    68: 'distinguishing a supported cost driver from a guess requires reasoning from supplied cost evidence',
    70: 'ordering restoration prerequisites applies dependency reasoning to a recovery scenario',
    71: 'finding relevant events for a time window and request identity applies log correlation to a symptom',
    74: 'identifying the affected resource and supported escalation combines finding evidence with response selection',
    76: 'distinguishing object permission from key-use authority applies two authorization layers to an SSE-KMS object',
    77: 'accepting or blocking a plan under approval criteria requires interpretation of destructive impact, including a mandatory destructive case',
    79: 'preserving successes while reporting failed targets applies scoped follow-up to partial failure',
    80: 'recognizing expiry, refreshing an authorized session and retrying safely combines diagnosis with a bounded response',
    86: 'locating a broken connectivity layer combines routing, DNS and connection evidence',
    89: 'connecting an injected fault to alarm state and notification applies the alarm model to a controlled failure',
    90: 'checking release routing and returning an alias to a prior version combines release verification with rollback',
    91: 'restoring a prior deployment revision on a seeded failure applies rollout diagnosis and rollback to a failure scenario',
    92: 'switching traffic only to healthy replacements and returning to the original fleet combines health evidence with safe cutover and rollback',
    93: 'removing temporary resources while preserving preexisting ones applies cleanup boundaries after script failure',
    94: 'choosing restoration of declared state versus a configuration update applies drift reasoning to an out-of-band change',
    96: 'choosing a smaller capacity only when evidence preserves constraints requires a workload-specific decision',
    102: 'testing service usability during an AZ failure applies the redundancy model to a controlled failure scenario',
    103: 'removing only exercise resources in dependency order combines scope control with teardown ordering',
    108: 'detecting tampering or missing evidence interprets supplied validation results',
    111: 'predicting replacement order combines lifecycle configuration with a supplied diff',
    113: 'applying severity and exception criteria to a scan report requires a release decision for that report',
    114: 'identifying the first failing action and a supported correction requires evidence-based pipeline diagnosis',
    115: 'identifying a failing component and verifying correction combines telemetry with diagnostic and recovery reasoning',
    117: 'checking bounded retries and recoverability applies the failure-handling model to a failed event target',
    120: 'identifying continuing billed usage after deletion interprets residual-charge evidence',
    124: 'keeping incident recovery within preconditions and success checks applies a runbook to an incident',
    125: 'comparing restored data age and restoration time with supplied objectives applies both recovery measures to a rehearsal',
    126: 'linking a timeline and demonstrated cause to a justified prevention action requires evidence-based causal reasoning',
}

rows = []
for i, c in enumerate(concepts):
    key = (c['concept_id'], c['path_id'])
    e = briefs[key]['evidence']
    cent = c['dependency_graph_centrality']
    cutoff = cutoffs[c['path_id']]
    facts = len(e['required_facts'])
    misconceptions = len(e['misconceptions'])
    central_core = cent > 0 and cent >= cutoff
    tier = 'core' if central_core or i in application else 'standard'
    if central_core:
        signal = (f'within the top-quarter centrality band for {c["path_id"]} '
                  f'(cutoff {cutoff}; include ties at the 32nd of 128 ranks)')
    else:
        signal = f'below the top-quarter cutoff {cutoff} for {c["path_id"]}'
    reason = f'Centrality {cent}, {signal}; assessment: "{c["assessment_target"]}". '
    if i in application:
        reason += application[i][0].upper() + application[i][1:] + ' -> core. '
    elif central_core:
        reason += 'Graph dependence supplies the Core signal even for this bounded assessment -> core. '
    else:
        reason += ('The target is bounded operational verification or a conceptual distinction, '
                   'not explicit selection/combination for a new problem; it is also not minor syntax or lookup -> standard. ')
    reason += f'{facts} required facts; {misconceptions} documented misconceptions'
    if misconceptions:
        reason += '; the misconception adds explanatory need but does not alone imply a new-situation assessment'
    reason += '.'
    rows.append({'concept_id': key[0], 'path_id': key[1], 'depth_tier': tier, 'reasoning': reason})

metadata = {
    'artifact_type': 'depth_classification',
    'artifact_version': '1.0.0',
    'schema_version': '1.0.0',
    'batch_id': 'glossary_batch_aws_devops_engineer',
    'run_id': extracted['metadata']['run_id'],
    'prompt_version': '04_depth_classification@v1',
    'model': 'none',
    'generated_at': datetime.now(timezone.utc).isoformat(),
    'source_snapshot_id': extracted['metadata']['source_snapshot_id'],
    'parent_artifact_hashes': {name: hashlib.sha256(raw[name]).hexdigest() for name in INPUTS},
}
artifact = {'metadata': metadata, 'batch_id': metadata['batch_id'], 'classifications': rows}
(BASE / 'depth_classification.json').write_text(json.dumps(artifact, indent=2, ensure_ascii=False) + '\n')

# Stage self-check / cost-control mistakes checklist: complete and unique pairs;
# within-path graph cutoff (ties preserved); never use disposition; no forced
# Reference tier for terminal operational assessments; actual targets/counts;
# exact byte hashes of both named inputs; UTC timestamp; no unrelated edits.
keys = [(r['concept_id'], r['path_id']) for r in rows]
assert len(keys) == len(set(keys)) == len(concepts) == 128
assert set(keys) == set(briefs)
assert set(keys) == {(c['concept_id'], c['path_id']) for c in concepts}
assert cutoffs == {'aws_devops_engineer': 3}
for c, r in zip(concepts, rows):
    assert c['assessment_target'] in r['reasoning']
    assert f'Centrality {c["dependency_graph_centrality"]},' in r['reasoning']
    e = briefs[(c['concept_id'], c['path_id'])]['evidence']
    assert f'{len(e["required_facts"])} required facts' in r['reasoning']
    assert f'{len(e["misconceptions"])} documented misconceptions' in r['reasoning']
    if c['dependency_graph_centrality'] >= 3:
        assert r['depth_tier'] == 'core'
    assert 'disposition' not in r['reasoning']
for name in INPUTS:
    assert hashlib.sha256((BASE / name).read_bytes()).hexdigest() == metadata['parent_artifact_hashes'][name]
assert datetime.fromisoformat(metadata['generated_at']).utcoffset().total_seconds() == 0
print('Self-check PASS; rows:', len(rows), '; tiers:', dict(Counter(r['depth_tier'] for r in rows)))
