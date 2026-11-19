import json
import hashlib
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime, timezone

root = Path(__file__).resolve().parent
inputs = ['glossary_bundles_draft.json', 'extracted_concepts.json']
draft, extracted = [json.loads((root / name).read_text()) for name in inputs]
batch_id = 'glossary_batch_aws_devops_engineer'
bundles = {(b['context']['path_id'], b['context']['concept_id']): b for b in draft['bundles']}
concepts = sorted(extracted['concepts'], key=lambda c: (c['path_id'], c['toc_sequence_position']))
tiles = defaultdict(list)
positions = {}
for c in concepts:
    tiles[(c['path_id'], c['toc_location']['tile_id'])].append(c)
    positions[(c['path_id'], c['concept_id'])] = c['toc_sequence_position']

# Every multi-concept tile receives a considered decision. Singleton tiles cannot cluster.
decisions = {
    'aws_devops.tile.032': None,  # Python environment preparation and CLI pagination are different operations.
    'aws_devops.tile.036': None,  # Database operation is not the same idea as S3 version recovery.
    'aws_devops.tile.038': ('Publishing exact release content',
        'These adjacent concepts are two forms of publishing and retrieving exact release content: a container image in ECR and a provenance-linked build file. All recorded prerequisites precede the tile; required external Docker, shell and workflow preparation must also be complete before entry. Keep the ECR digest and authentication procedure separate from GitHub artifact immutability and attestation verification: shared presentation compares publication workflows, not interchangeable tools or guarantees.'),
    'aws_devops.tile.044': None,  # Drift detection versus failed-update rollback is an important boundary.
    'aws_devops.tile.046': None,  # Four identity mechanisms have materially different trust/provider boundaries.
    'aws_devops.tile.053': ('From supplied build commands to EC2 deployment',
        'These adjacent concepts cover consecutive delivery responsibilities: selecting CodeBuild phase commands and exported output, then configuring the supplied EC2 CodeDeploy revision, mappings and hooks. Every recorded prerequisite is available before the tile; required external shell, testing and configuration preparation remains an entry condition. The build export and target deployment remain separate steps with separate evidence, and the deployment concept does not require learning the buildspec concept first.'),
    'aws_devops.tile.056': ('Safe ECR repository operation',
        'Access and retention are complementary controls on the same already-published ECR images: identify who may publish or retrieve them, then preview which digests may expire. Their recorded prerequisites all precede tile entry. Preserve the boundary between identity/repository authorization tests and lifecycle-expiry checks; permission to pull does not establish that a still-needed image survives retention.'),
    'aws_devops.tile.071': None,  # Log query analysis and SNS delivery setup are distinct operations.
    'aws_devops.tile.074': None,  # Finding triage and audit-storage controls are not one workflow step.
    'aws_devops.tile.078': ('Before-and-after fleet execution checks',
        'Both concepts apply to a scoped fleet operation: inspect proposed targets and actions before mutation, then classify target-specific outcomes before selecting follow-up. Their shared remote-command prerequisite is earlier than the tile, and required external fleet/shell preparation must already be complete. Preserve the distinction between limited dry-run permission evidence and actual invocation results; neither concept must be learned to satisfy the other\'s entry prerequisites.'),
    'aws_devops.tile.090': None,  # Lambda alias, Kubernetes revision and EC2 traffic rollback boundaries matter.
    'aws_devops.tile.104': ('Recovery rehearsal readiness',
        'These adjacent checks prepare one bounded recovery rehearsal: verify the approved session\'s identity, lifetime and access, then verify the isolated restoration destination and client traffic. All recorded prerequisites precede the tile, with required external preparation still binding at entry. Session authorization and environmental isolation remain independent readiness checks; neither substitutes for the other and neither depends on learning its neighbor first.'),
    'aws_devops.tile.106': ('Controlled and evidenced operational response',
        'Approval/stop controls and execution evidence are complementary parts of the same bounded response workflow. Their recorded prerequisites, including action authorization and CloudTrail attribution, are all available before this tile. Keep preventing or stopping an operation distinct from recording what actually executed: the audit record includes failed outcomes and cannot be inferred from approval or intended actions.'),
    'aws_devops.tile.108': None,  # Tamper detection and retention prevention warrant distinct learning steps.
    'aws_devops.tile.110': None,  # State-backend migration and resource replacement are different operations.
    'aws_devops.tile.114': None,  # Delivery-action and runtime-health diagnosis have different evidence boundaries.
}

clusters = []
reviewed = Counter()
for (path_id, tile_id), members in tiles.items():
    if len(members) < 2:
        reviewed['singleton_tiles'] += 1
        continue
    assert tile_id in decisions, ('Unreviewed multi-concept tile', tile_id)
    decision = decisions[tile_id]
    if decision is None:
        reviewed['skipped_multi_concept_tiles'] += 1
        continue
    title, reasoning = decision
    start = members[0]['toc_sequence_position']
    for c in members:
        b = bundles[(path_id, c['concept_id'])]
        assert b['context']['toc_location']['tile_id'] == tile_id
        prereqs = set(c['direct_prerequisite_ids']) | set(b['context']['prerequisites'])
        assert all((path_id, p) in positions and positions[(path_id, p)] < start for p in prereqs), (tile_id, prereqs)
    clusters.append({
        'cluster_id': f'cluster_{path_id}_{tile_id.rsplit(".", 1)[1]}',
        'path_id': path_id,
        'tile_id': tile_id,
        'title': title,
        'concept_ids': [c['concept_id'] for c in members],
        'reasoning': reasoning,
    })
    reviewed['clustered_tiles'] += 1

# Generator mistakes checklist: full-batch review; IDs and bundles exist; unique membership;
# at least two adjacent concepts, TOC order, one tile/path; prerequisites at tile start;
# preserve pedagogical boundaries and independent bundles; no UI/curriculum merging;
# real UTC and byte-level input hashes. Semantic decisions above were checked against facts/anchors.
assert set(decisions) == {t for (_, t), cs in tiles.items() if len(cs) >= 2}
assert set(bundles) == set(positions)
seen = set()
assert len({c['cluster_id'] for c in clusters}) == len(clusters)
for cluster in clusters:
    ids = cluster['concept_ids']
    assert len(ids) >= 2 and len(ids) == len(set(ids))
    seq = [positions[(cluster['path_id'], cid)] for cid in ids]
    assert seq == list(range(seq[0], seq[0] + len(seq)))
    for cid in ids:
        key = (cluster['path_id'], cid)
        assert key not in seen
        seen.add(key)

meta = extracted['metadata']
artifact = {
    'metadata': {
        'artifact_type': 'clusters', 'artifact_version': '1.0.0', 'schema_version': '1.0.0',
        'batch_id': batch_id, 'run_id': meta['run_id'],
        'prompt_version': '12_cluster_pass@v1', 'model': 'none',
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'source_snapshot_id': meta['source_snapshot_id'],
        'parent_artifact_hashes': {name: hashlib.sha256((root / name).read_bytes()).hexdigest() for name in inputs},
    },
    'batch_id': batch_id,
    'clusters': clusters,
}
(root / 'clusters.json').write_text(json.dumps(artifact, indent=2, ensure_ascii=False) + '\n')
print(json.dumps({'concepts_reviewed': len(concepts), 'tiles_reviewed': len(tiles), 'clusters': len(clusters), 'clustered_concepts': len(seen), **reviewed}, indent=2))
