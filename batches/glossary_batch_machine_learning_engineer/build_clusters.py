import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone
from collections import OrderedDict

B = Path('batches/glossary_batch_machine_learning_engineer')
INPUTS = ['glossary_bundles_draft.json', 'extracted_concepts.json']
draft, extracted = [json.loads((B / f).read_text()) for f in INPUTS]
concepts = sorted(extracted['concepts'], key=lambda c: (c['path_id'], c['toc_sequence_position']))
by_id = {c['concept_id']: c for c in concepts}
bundles = {(b['context']['path_id'], b['context']['concept_id']): b for b in draft['bundles']}
tiles = OrderedDict()
for c in concepts:
    tiles.setdefault((c['path_id'], c['toc_location']['tile_id']), []).append(c)

# Semantic decisions, keyed by the actual tile positions, not inferred from titles.
choices = {
    'mle.tile.012_015': ([12, 13, 14], 'Training-Fitted Feature Transformations',
        'Imputation, numerical scaling and categorical encoding are adjacent variants of the same fit-on-training, reuse-on-validation operation. Each retains its own replacement, scaling or category policy rather than becoming an interchangeable transformation. All prerequisites are available before this tile. Pipeline composition remains a separate later concept because it requires these fitted transformations.'),
    'mle.tile.024_025': ([24, 25], 'Validation-Based Selection Under Task Costs',
        'These adjacent steps apply precommitted validation cost and eligibility rules to freeze a prediction choice before protected testing. Keep their selection objects explicit: threshold selection changes the cutoff for scores, whereas candidate comparison ranks supplied model records against a baseline. Metrics, acceptance criteria and their prerequisites are available at tile start; neither concept requires the other as preparation.'),
    'mle.tile.026_028': ([26, 27], 'Localize Errors Across Validation Groups',
        'Both concepts examine conditional errors within an identified validation group rather than treating the overall score as sufficient. Error analysis investigates recurring failures; slice evaluation compares predefined groups with their counts and representativeness limits. These are complementary views of one diagnostic workflow, with metric prerequisites already available at tile start. Subgroup mitigation stays separate because it requires slice evaluation.'),
    'mle.tile.029_032': ([29, 30], 'Record and Control Training Comparisons',
        'Run logging and random-source control are adjacent parts of a traceable training comparison: record configuration, metrics and artifacts, then make the random settings and observed variability explicit. A recorded run is not itself a guarantee of deterministic reproduction, and seed control does not provide that guarantee either. Both prerequisite sets precede the tile. Regularization remains its own model-selection step; search remains separate and requires the randomness concept.'),
    'mle.tile.041_043': ([41, 42], 'Training Updates and Forward-Only Validation',
        'The minibatch update loop and training/evaluation mode handling are parts of one neural training workflow. The shared explanation must keep parameter-updating training distinct from forward-only validation, including the separate roles of eval mode and disabled gradient recording. Both concepts have all prerequisites before tile start. Weight persistence remains separate because it requires training/evaluation modes.'),
    'mle.tile.049_050': ([49, 50], 'Measure Training Bottlenecks and Capacity',
        'Profiling a bounded workload and comparing authorized CPU/GPU capacity are adjacent evidence-gathering parts of choosing a suitable training runtime. Keep operator/data-loading attribution distinct from the matched runtime, memory and billing comparison; profiling is not a prerequisite for the supplied hardware comparison. All declared prerequisites precede this tile, so neither sub-concept needs knowledge introduced by its neighbor.'),
    'mle.tile.052_055': ([53, 54], 'Capture Dataset and Environment Identity',
        'These adjacent concepts capture complementary immutable inputs to a reproducible training record: the selected dataset generation/hash and the actual code revision, dependency pins and runtime identity. They are parts of one provenance-capture operation, not claims that an environment manifest versions the dataset. Both prerequisite sets are available at tile start. Script conversion stays separate; experiment reproduction follows only after these records and the script exist.'),
    'mle.tile.056_057': ([56, 57], 'Prepare a Traceable Model Release Artifact',
        'Registration and packaging are adjacent parts of preparing an identifiable model deliverable. Registration links the immutable artifact to its originating run; packaging carries fitted preprocessing, model state and compatible inference dependencies and checks reloaded predictions. Keep those distinct responsibilities explicit rather than treating registration as proof of package correctness. Every prerequisite for both concepts precedes the tile.'),
    'mle.tile.064_065': ([64, 65], 'Reproduce and Verify a Model Deployment',
        'These adjacent concepts form a deployment workflow around an immutable artifact and explicit runtime configuration: reproduce the deployment, then inspect its identity and prediction behavior. Configuration validity and successful startup are not substitutes for release verification. Both prerequisite sets are already available at tile start, so the supplied verification task does not depend on first learning its neighboring configuration concept.'),
    'mle.tile.068_071': ([68, 69, 70], 'Measure and Tune Bounded Serving Capacity',
        'Load testing, batching selection and bounded worker concurrency are adjacent parts of checking serving performance under fixed service constraints. Keep endpoint-level throughput and tail latency, request batching limits and actual worker bounds distinct; batching and concurrency are not interchangeable controls. All prerequisites precede the tile. Replica scaling stays separate because it requires the load-test concept introduced here.'),
    'mle.tile.073_075': ([73, 74, 75], 'Fail-Closed Data, Behavior and Release Gates',
        'These adjacent concepts are variants of the same operation: evaluate named requirements, retain failure evidence and stop dependent pipeline or promotion steps on rejection. Preserve separate scopes and evidence: dataset validity before training, packaged inference behavior on fixtures, and candidate acceptance before release. Passing one is not passing the others. All prerequisite sets are available at the beginning of this tile.'),
}

# Every nonselected tile is deliberately considered; omissions are not missing coverage.
skips = {
 'mle.tile.000_000': 'Singleton tile.',
 'mle.tile.001_003': 'Dtype selection and vectorization require array shapes introduced in this tile.',
 'mle.tile.004_006': 'Chunked ingestion requires the first ingestion concept; the two start-ready concepts are nonadjacent.',
 'mle.tile.007_008': 'Cleaning policy requires schema validation introduced in this tile.',
 'mle.tile.009_011': 'Keep population representativeness and keyed label integrity as separate boundaries; split selection additionally requires label integrity introduced here.',
 'mle.tile.016_017': 'Safe feature derivation requires leakage detection introduced in this tile.',
 'mle.tile.018_018': 'Singleton tile.',
 'mle.tile.019_020': 'Acceptance criteria require metric selection introduced in this tile.',
 'mle.tile.021_023': 'Keep the simple reference rule, supplied approach decision and fitted classical estimator separate so a reference is not mistaken for a learned candidate or an approach decision for implementation.',
 'mle.tile.033_033': 'Singleton tile.',
 'mle.tile.034_034': 'Singleton tile.',
 'mle.tile.035_037': 'Loader and model definition require the input tensors introduced in this tile.',
 'mle.tile.038_040': 'Loss and optimizer configuration require autograd introduced in this tile.',
 'mle.tile.044_045': 'Validation-patience stopping and fault diagnosis have different decisions and evidence; keep separate to avoid treating a training failure as an early-stopping condition.',
 'mle.tile.046_048': 'Batch sizing and memory diagnosis require device placement introduced in this tile; memory diagnosis also requires batch sizing.',
 'mle.tile.051_051': 'Singleton tile.',
 'mle.tile.058_058': 'Singleton tile.',
 'mle.tile.059_059': 'Singleton tile.',
 'mle.tile.060_063': 'Online prediction requires schema validation, and readiness requires online prediction, introduced here; start-ready schema validation and batch inference are nonadjacent.',
 'mle.tile.066_067': 'Authentication/authorization and service observability are different responsibilities; successful telemetry does not establish access control.',
 'mle.tile.072_072': 'Singleton tile.',
 'mle.tile.076_079': 'Artifact dependency wiring is distinct from accountable promotion authorization; recovery depends on dependency wiring introduced here, leaving lineage audit nonadjacent to the other start-ready concepts.',
 'mle.tile.080_082': 'Preserve the important distinction between unlabeled distribution observations and evidence for drift or quality degradation; drift detection also requires the preceding concepts introduced here.',
 'mle.tile.083_085': 'Matured-label quality measurement and alert routing/configuration have distinct evidence and outputs; regression diagnosis requires delayed-label quality introduced here.',
 'mle.tile.086_089': 'Execution requires trigger policy and idempotency requires execution introduced here; start-ready policy and candidate validation are nonadjacent.',
 'mle.tile.090_090': 'Singleton tile.',
 'mle.tile.091_094': 'Keep resource utilization separate from bill attribution: low utilization does not determine billed expenditure. Guardrails require attribution introduced here, and cleanup is nonadjacent to the other start-ready concepts.',
}
assert set(choices).isdisjoint(skips)
assert {t for _, t in tiles} == set(choices) | set(skips)
assert len(by_id) == len(concepts)
assert set(bundles) == {(c['path_id'], c['concept_id']) for c in concepts}

def ancestors(cid, visiting=None):
    visiting = set() if visiting is None else visiting
    assert cid not in visiting, ('prerequisite cycle', cid)
    if cid not in by_id:
        return set()
    visiting = visiting | {cid}
    result = set(by_id[cid]['direct_prerequisite_ids'])
    for p in by_id[cid]['direct_prerequisite_ids']:
        result |= ancestors(p, visiting)
    return result

clusters = []
review = []
used = set()
for (path_id, tile_id), cs in tiles.items():
    if tile_id not in choices:
        review.append({'path_id': path_id, 'tile_id': tile_id, 'decision': 'skip', 'reason': skips[tile_id], 'concept_count': len(cs)})
        continue
    positions, title, reasoning = choices[tile_id]
    selected = [c for c in cs if c['toc_sequence_position'] in positions]
    assert [c['toc_sequence_position'] for c in selected] == positions
    assert len(selected) >= 2
    assert positions == list(range(positions[0], positions[-1] + 1)), ('nonadjacent cluster', tile_id)
    start = cs[0]['toc_sequence_position']
    for c in selected:
        cid = c['concept_id']
        assert cid not in used
        used.add(cid)
        assert bundles[(path_id, cid)]['context']['prerequisites'] == c['direct_prerequisite_ids']
        assert bundles[(path_id, cid)]['context']['toc_location']['tile_id'] == tile_id
        for p in ancestors(cid):
            if p in by_id:
                assert by_id[p]['path_id'] == path_id
                assert by_id[p]['toc_sequence_position'] < start, ('prerequisite unavailable at tile start', cid, p)
    row = {'cluster_id': 'cluster_' + path_id + '_' + tile_id.split('.')[-1] + '_' + str(positions[0]) + '_' + str(positions[-1]),
           'path_id': path_id, 'tile_id': tile_id, 'title': title,
           'concept_ids': [c['concept_id'] for c in selected], 'reasoning': reasoning}
    clusters.append(row)
    review.append({'path_id': path_id, 'tile_id': tile_id, 'decision': 'cluster', 'concept_count': len(cs), 'clustered_concept_ids': row['concept_ids']})

meta = {k: draft['metadata'][k] for k in ['artifact_version', 'schema_version', 'batch_id', 'run_id', 'source_snapshot_id']}
meta.update(artifact_type='clusters', model='gpt-6.1-sol', prompt_version='12_cluster_pass@v1',
            generated_at=datetime.now(timezone.utc).isoformat(),
            parent_artifact_hashes={f: hashlib.sha256((B / f).read_bytes()).hexdigest() for f in INPUTS})
output = {'metadata': meta, 'batch_id': 'glossary_batch_machine_learning_engineer', 'clusters': clusters}
assert len({r['cluster_id'] for r in clusters}) == len(clusters)
(B / 'clusters.json').write_text(json.dumps(output, indent=2, ensure_ascii=False) + '\n')
checks = {'input_concept_count': len(concepts), 'input_bundle_count': len(bundles), 'tiles_reviewed': len(tiles),
          'cluster_count': len(clusters), 'clustered_concept_count': len(used), 'unclustered_concept_count': len(concepts)-len(used),
          'skipped_tile_count': len(skips),
          'mistakes_checklist': {
              'whole_batch_all_tiles_considered': True, 'no_cross_tile_or_cross_path_clusters': True,
              'at_least_two_concepts_per_cluster': True, 'contiguous_toc_order_without_gaps': True,
              'no_duplicate_cluster_or_concept_ids': True, 'bundle_and_extraction_references_match': True,
              'direct_and_transitive_local_prerequisites_available_at_tile_start': True,
              'semantic_cohesion_and_important_boundaries_reviewed': True,
              'individual_bundles_and_curriculum_unchanged': True,
              'input_hashes_computed_not_typed': True, 'no_new_sources_video_ids_or_teaching_claims': True},
          'tile_decisions': review}
(B / 'clusters_self_check.json').write_text(json.dumps(checks, indent=2, ensure_ascii=False) + '\n')
print(json.dumps({k: v for k, v in checks.items() if k not in ['tile_decisions', 'mistakes_checklist']}, indent=2))
