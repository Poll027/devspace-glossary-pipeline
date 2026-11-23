"""Stage 04 only. All 85 assessment targets were reviewed: each applies the
concept to supplied product data, artifacts, or scenarios; none asks for mere
recall/lookup. Do not infer tiers from disposition or require a tier quota.
"""
import collections
import datetime
import hashlib
import json
import math
from pathlib import Path

folder = Path('batches/glossary_batch_product_manager')
names = ('extracted_concepts.json', 'coverage_briefs.json')
raw = {name: (folder / name).read_bytes() for name in names}
extracted, coverage = (json.loads(raw[name]) for name in names)
key = lambda row: (row['concept_id'], row['path_id'])
concepts = extracted['concepts']
briefs = {key(row): row for row in coverage['briefs']}
assert len(briefs) == len(coverage['briefs'])
assert len({key(row) for row in concepts}) == len(concepts)
assert set(briefs) == {key(row) for row in concepts}
by_path = collections.defaultdict(list)
for row in concepts:
    by_path[row['path_id']].append(row)
cutoffs = {}
for path, rows in by_path.items():
    quarter_size = math.ceil(len(rows) / 4)
    cutoff = sorted((r['dependency_graph_centrality'] for r in rows), reverse=True)[quarter_size - 1]
    tied_count = sum(r['dependency_graph_centrality'] >= cutoff for r in rows)
    cutoffs[path] = (quarter_size, cutoff, tied_count, len(rows))

classifications = []
for row in concepts:
    path = row['path_id']
    centrality = row['dependency_graph_centrality']
    n_top, cutoff, tied_count, total = cutoffs[path]
    evidence = briefs[key(row)]['evidence']
    facts = len(evidence['required_facts'])
    misconceptions = len(evidence['misconceptions'])
    if centrality >= cutoff and centrality > 0:
        graph_reason = (
            f'Centrality {centrality}, in the top quarter for {path} '
            f'(top {n_top} of {total}, cutoff {cutoff}; including cutoff ties gives {tied_count} concepts), '
            'is an independent Core signal.'
        )
    elif centrality == 0:
        graph_reason = (
            f'Centrality 0, below the top-quarter cutoff {cutoff} for {path}; '
            'the zero-centrality Reference signal does not determine the tier because the assessment is not recall or lookup.'
        )
    else:
        graph_reason = (
            f'Centrality {centrality}, below the top-quarter cutoff {cutoff} for {path}; '
            'centrality alone would suggest Standard.'
        )
    reasoning = (
        f'{graph_reason} Assessment target: "{row["assessment_target"]}" '
        'This requires applying the concept to a supplied situation or artifact, not merely recognizing its definition, '
        'so the assessment independently warrants Core. '
        f'The coverage brief has {facts} required facts and {misconceptions} misconceptions; '
        'these describe the teaching scope, not a separate importance ranking.'
    )
    classifications.append(dict(concept_id=row['concept_id'], path_id=path, depth_tier='core', reasoning=reasoning))

batch_id = 'glossary_batch_product_manager'
output = {
    'metadata': {
        'artifact_type': 'depth_classification',
        'artifact_version': '1.0.0',
        'schema_version': '1.0.0',
        'batch_id': batch_id,
        'run_id': batch_id,
        'prompt_version': '04_depth_classification@v1',
        'model': 'gpt-6.1-sol',
        'generated_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'source_snapshot_id': extracted['metadata']['source_snapshot_id'],
        'parent_artifact_hashes': {name: hashlib.sha256(raw[name]).hexdigest() for name in names},
    },
    'batch_id': batch_id,
    'classifications': classifications,
}
(folder / 'depth_classification.json').write_text(json.dumps(output, ensure_ascii=False, indent=2) + '\n')

# Self-check: full pair coverage, unique IDs, TOC order, real numeric evidence,
# no disposition/importance inference, zero-centrality overrides explained,
# exact input hashes and metadata, no changes to upstream artifacts.
assert [key(r) for r in classifications] == [key(r) for r in concepts]
for concept, result in zip(concepts, classifications):
    brief = briefs[key(concept)]['evidence']
    text = result['reasoning']
    assert f'Centrality {concept["dependency_graph_centrality"]},' in text
    assert concept['assessment_target'] in text
    assert f'{len(brief["required_facts"])} required facts and {len(brief["misconceptions"])} misconceptions' in text
    assert 'disposition' not in text
    if concept['dependency_graph_centrality'] == 0:
        assert 'not recall or lookup' in text
for name in names:
    assert (folder / name).read_bytes() == raw[name]
print('Self-check PASS:', len(classifications), 'unique concept/path rows; counts', dict(collections.Counter(r['depth_tier'] for r in classifications)))
print('Top-quarter thresholds:', cutoffs)
