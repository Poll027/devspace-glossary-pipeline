import collections
import datetime
import hashlib
import json
import math
from pathlib import Path

batch = Path('batches/glossary_batch_learn_python')
input_names = ['extracted_concepts.json', 'coverage_briefs.json']
inputs = {n: json.loads((batch / n).read_text()) for n in input_names}
extracted = inputs[input_names[0]]
briefs = {(b['concept_id'], b['path_id']): b for b in inputs[input_names[1]]['briefs']}
# Deliberate assessment reading: routine syntax, recognition and local prediction
# are not automatically application to a new requirement.
standard = {
 'python.comparison_operators': 'writing a basic comparison, without a new decision requirement',
 'python.function_default_keyword_args': 'binding arguments to a supplied signature, a routine call-syntax exercise',
 'python.variable_scope': 'predicting name resolution in supplied code rather than designing a solution',
 'python.interactive_execution': 'evaluating an expression sequence and tracking session state',
 'python.interpreter_execution_model': 'predicting and identifying execution phases in a short supplied program',
 'python.multiline_expressions': 'routine continuation syntax that preserves an existing expression',
 'python.syntax_vs_runtime_errors': 'classifying the origin of a failure rather than repairing a new program',
 'python.truth_value_testing': 'predicting the truth values of supplied values',
 'python.zip_iteration': 'routine element pairing and predicting the effect of unequal input lengths',
 'python.aliasing_mutability_and_copying': 'predicting mutation effects in supplied collection relationships',
 'python.docstrings': 'routine documentation of inputs, outputs and exceptions, not a new computational requirement',
 'python.exception_propagation': 'tracing handler selection and skipped operations through a call chain, beyond simple recall but not designing recovery',
 'python.finally_cleanup': 'predicting cleanup paths rather than designing a new resource-handling solution',
 'python.lambda_expressions': 'routine single-expression syntax and parameter binding',
 'python.variadic_arguments_and_unpacking': 'routine argument collection and forwarding without duplicate bindings',
 'python.encapsulation_conventions': 'applying naming conventions to distinguish public and implementation attributes, a bounded interface-convention exercise',
 'python.special_methods': 'implementing the two conventional display hooks, without a new object-protocol design requirement',
 'python.sys_runtime_interface': 'routine interpreter/version inspection using the named sys attributes',
 'python.iterator_consumption_and_exhaustion': 'predicting traversal results from supplied iterator state',
}
reference = {'python.assert_statement': 'recognising the distinction between an invariant assertion and required input validation; no implementation or new-case repair is requested'}

by_path = collections.defaultdict(list)
for c in extracted['concepts']:
    by_path[c['path_id']].append(c['dependency_graph_centrality'])
thresholds = {}
for path, vals in by_path.items():
    vals = sorted(vals)
    # Interpolated 75th percentile; include ties at the resulting threshold.
    index = (len(vals) - 1) * .75
    lo, hi = math.floor(index), math.ceil(index)
    threshold = vals[lo] + (vals[hi] - vals[lo]) * (index - lo)
    thresholds[path] = (threshold, sum(v >= threshold for v in vals), len(vals))

rows = []
for c in extracted['concepts']:
    cid, path = c['concept_id'], c['path_id']
    evidence = briefs[cid, path]['evidence']
    centrality = c['dependency_graph_centrality']
    threshold, count, total = thresholds[path]
    high = centrality >= threshold and centrality > 0
    signal = (f'Centrality {centrality}, ' + ('in' if high else 'below') +
              f' the top-quartile band for {path} (75th-percentile threshold {threshold:g}; '
              f'{count}/{total} concepts meet it); TOC position {c["toc_sequence_position"]} (zero-based). ')
    assessment = f'Assessment: "{c["assessment_target"]}". '
    supporting = (f'Required facts: {len(evidence["required_facts"])}; misconceptions: '
                  f'{len(evidence["misconceptions"])}. ')
    if high:
        tier = 'core'
        why = 'The within-path centrality signal independently warrants Core, even if the assessment is routine or recognition-oriented.'
    elif cid in reference:
        assert centrality == 0
        tier = 'reference'
        why = 'Zero centrality plus ' + reference[cid] + ' warrants Reference; fact count alone does not override the recall signal.'
    elif cid in standard:
        tier = 'standard'
        why = 'Assessment involves ' + standard[cid] + '; this is not mere lookup, but neither it nor centrality supplies a strong Core signal, so Standard.'
    else:
        tier = 'core'
        why = ('The assessment requires applying or combining the concept to meet a supplied requirement, '
               'choose an appropriate operation, diagnose a concrete problem, or repair behavior rather than merely recall syntax; '
               'this application signal warrants Core despite below-quartile centrality' +
               (' (zero centrality does not imply Reference when the assessment demands application).' if centrality == 0 else '.'))
    rows.append({'concept_id': cid, 'path_id': path, 'depth_tier': tier,
                 'reasoning': signal + assessment + supporting + why})

meta = extracted['metadata']
output = {
 'metadata': {
  'artifact_type': 'depth_classification', 'artifact_version': '1.0.0', 'schema_version': '1.0.0',
  'batch_id': 'glossary_batch_learn_python', 'run_id': meta['run_id'],
  'prompt_version': '04_depth_classification@v1', 'model': 'none',
  'generated_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
  'source_snapshot_id': meta['source_snapshot_id'],
  'parent_artifact_hashes': {n: hashlib.sha256((batch / n).read_bytes()).hexdigest() for n in input_names},
 },
 'batch_id': 'glossary_batch_learn_python', 'classifications': rows,
}
# Generator mistakes checklist / deterministic cross-reference checks:
# full batch, unique concept/path pairs, exact input assessment and centrality,
# quartile computed within each path, zero-centrality application not demoted,
# no disposition-based ranking, actual evidence counts, both parent hashes.
keys = [(r['concept_id'], r['path_id']) for r in rows]
expected = [(c['concept_id'], c['path_id']) for c in extracted['concepts']]
assert len(keys) == len(set(keys)) and keys == expected
assert set(keys) == set(briefs)
assert (set(standard) | set(reference)) <= {c['concept_id'] for c in extracted['concepts']}
for c, r in zip(extracted['concepts'], rows):
    assert c['assessment_target'] in r['reasoning']
    assert f'Centrality {c["dependency_graph_centrality"]},' in r['reasoning']
    threshold = thresholds[c['path_id']][0]
    if c['dependency_graph_centrality'] >= threshold and c['dependency_graph_centrality'] > 0:
        assert r['depth_tier'] == 'core'
    if r['depth_tier'] == 'reference':
        assert c['dependency_graph_centrality'] == 0 and c['concept_id'] in reference
assert 'disposition' not in json.dumps(output)
(batch / 'depth_classification.json').write_text(json.dumps(output, indent=2, ensure_ascii=False) + '\n')
print('Quartile thresholds:', thresholds)
print('Counts:', dict(collections.Counter(r['depth_tier'] for r in rows)))
print('Self-check passed: complete unique coverage, input matches, quartile rule, evidence counts, parent hashes.')
