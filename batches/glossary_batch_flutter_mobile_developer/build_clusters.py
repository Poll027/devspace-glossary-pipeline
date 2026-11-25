import collections
import datetime
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INPUTS = ['glossary_bundles_draft.json', 'extracted_concepts.json']
raw = {name: (ROOT / name).read_bytes() for name in INPUTS}
draft, extracted = (json.loads(raw[name]) for name in INPUTS)
concepts = sorted(extracted['concepts'], key=lambda c: (c['path_id'], c['toc_sequence_position']))
by_key = {(c['path_id'], c['concept_id']): c for c in concepts}
bundles = {(b['context']['path_id'], b['context']['concept_id']): b for b in draft['bundles']}
assert len(by_key) == len(concepts) == len(bundles) == 112
assert set(by_key) == set(bundles)
tiles = collections.defaultdict(list)
for c in concepts:
    tiles[(c['path_id'], c['toc_location']['tile_id'])].append(c)

# Editorial selections after reviewing every tile's objectives and prerequisites.
# All remaining tiles are intentionally skipped. Eligibility alone is insufficient:
# run/edit vs declarations, extraction vs validation, layering vs scrolling,
# read vs subscription vs disposal, interface boundaries vs test harnesses,
# schema migration vs failed writes, and stream/security/service initialization
# retain separate explanations. Tiles with a prerequisite introduced inside the
# tile cannot cluster that dependent concept, even in a later sub-group.
selections = [
    (['flutter.material_theming', 'flutter.bundled_assets'],
     'Apply the screen\'s visual resources',
     'These adjacent concepts are complementary parts of supplying a screen\'s appearance: shared Material styling and a declared bundled image. Both require only widget composition, already taught before this tile. Keep theme inheritance and asset declaration/loading as distinct sub-concepts, not interchangeable mechanisms. The inspector remains a separate diagnostic step.'),
    (['flutter.semantic_labels', 'flutter.interaction_targets'],
     'Make a control identifiable and reachable',
     'These adjacent concepts address two complementary checks on the same accessible control: its accessible name and its interactive area. Widget composition and layout constraints are available at the tile\'s start; neither concept requires the earlier responsive-layout or text-scaling concepts in this tile. Preserve separate naming and target-size checks rather than imply that either alone establishes accessibility.'),
    (['flutter.request_state_model', 'flutter.mounted_async_updates'],
     'Present asynchronous results to a live UI owner',
     'These adjacent concepts are complementary parts of handling an asynchronous completion: choosing its presentation state and checking whether its UI owner can still receive an update. Their Dart asynchronous, conditional and class foundations, notifier updates, State lifecycle and local setState prerequisites are all earlier than this tile. Retain the boundary between what result state to publish and whether an owner is still mounted; request recovery and stale-result handling remain separate later concepts.'),
    (['flutter.package_selection', 'flutter.compatible_dependencies'],
     'Select and resolve a compatible package',
     'These adjacent concepts form a package-adoption workflow: evaluate a candidate against feature and platform requirements, then resolve compatible dependency constraints reproducibly. Selection has no direct prerequisites and package imports precede this tile, so both can be entered at the tile\'s start. Preserve suitability evaluation versus version resolution as distinct checks; platform plugin configuration remains separate because it requires dependency compatibility taught within this tile.'),
    (['flutter.firebase_auth_actions', 'flutter.firebase_auth_session'],
     'Change and observe the sign-in session',
     'These adjacent concepts are the command and observation sides of one authentication workflow: await sign-in/sign-out operations and observe the session stream. FlutterFire initialization, async/await, stream subscriptions and notifier updates are all taught before this tile. Keep operation completion and stream-observed session state explicitly distinct; route access is excluded because it depends on session observation introduced here.'),
    (['flutter.application_identifiers', 'flutter.release_versioning'],
     'Identify the app and its release',
     'These adjacent concepts supply complementary release identifiers: which registered application the build belongs to and which version/build it represents. Both have no direct prerequisites and can be entered at this tile\'s start. Keep application identity distinct from release versioning, and preserve the Android and iOS rules within each concept rather than imply one universal numbering rule. The dated release-requirements check stays separate because it requires both concepts.'),
    (['flutter.store_metadata_assets', 'flutter.store_privacy_disclosures', 'flutter.review_readiness'],
     'Prepare the store review package',
     'These three adjacent concepts are complementary preparation checks for one store review package: accurate listing materials, implementation-matched privacy disclosures, and a working release journey with reviewer access. Their release-requirements, analytics, permissions, security, integration-testing and authentication prerequisites all precede this tile. Preserve each checklist and its separate acceptance criteria; store submission remains a subsequent step because it requires these preparations.'),
]

clusters = []
used = set()
for ids, title, reasoning in selections:
    matches = [c for c in concepts if c['concept_id'] == ids[0]]
    assert len(matches) == 1
    path = matches[0]['path_id']
    cs = [by_key[(path, cid)] for cid in ids]
    tile = cs[0]['toc_location']['tile_id']
    assert all(c['toc_location']['tile_id'] == tile for c in cs)
    seq = [c['toc_sequence_position'] for c in cs]
    assert seq == list(range(seq[0], seq[0] + len(seq)))
    tile_start = tiles[(path, tile)][0]['toc_sequence_position']
    prior = {c['concept_id'] for c in concepts if c['path_id'] == path and c['toc_sequence_position'] < tile_start}
    for c in cs:
        key = (path, c['concept_id'])
        assert key not in used
        used.add(key)
        context = bundles[key]['context']
        assert context['toc_location']['tile_id'] == tile
        prereqs = set(c['direct_prerequisite_ids']) | set(context['prerequisites'])
        assert prereqs <= prior, (key, prereqs - prior)
        # Exhaustively check the transitive prerequisite closure as well.
        pending, seen = list(prereqs), set()
        while pending:
            dep = pending.pop()
            if dep in seen:
                continue
            seen.add(dep)
            assert dep in prior
            pending.extend(by_key[(path, dep)]['direct_prerequisite_ids'])
    clusters.append({
        'cluster_id': f'cluster_{path}_{tile.rsplit(".", 1)[-1]}',
        'path_id': path,
        'tile_id': tile,
        'title': title,
        'concept_ids': ids,
        'reasoning': reasoning,
    })

# Stage self-check: full-batch review, no cross-tile or nonadjacent grouping,
# >=2 distinct concepts, TOC order, prerequisites at TILE start (not cluster
# start), no overlap, explicit preservation of boundaries, no curriculum merge,
# no UI arrangement, invented source or video, and exact input-byte hashes.
assert len({c['cluster_id'] for c in clusters}) == len(clusters)
assert all(len(c['concept_ids']) >= 2 and len(set(c['concept_ids'])) == len(c['concept_ids']) for c in clusters)
metadata = {
    'artifact_type': 'clusters', 'artifact_version': '1.0.0', 'schema_version': '1.0.0',
    'batch_id': extracted['batch_id'], 'run_id': extracted['metadata']['run_id'],
    'prompt_version': '12_cluster_pass@v1', 'model': 'none',
    'generated_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'source_snapshot_id': extracted['metadata']['source_snapshot_id'],
    'parent_artifact_hashes': {name: hashlib.sha256(raw[name]).hexdigest() for name in INPUTS},
}
out = {'metadata': metadata, 'batch_id': extracted['batch_id'], 'clusters': clusters}
(ROOT / 'clusters.json').write_text(json.dumps(out, indent=2, ensure_ascii=False) + '\n')
print(f'Reviewed {len(concepts)} concepts in {len(tiles)} tiles across {len(extracted["paths"])} path(s).')
print(f'Created {len(clusters)} cluster rows covering {len(used)} concepts; skipped {len(tiles) - len(clusters)} tiles.')
print('Self-check passed: ids, adjacency, tile boundaries, TOC order, direct/transitive prerequisites, no overlap, metadata hashes.')
