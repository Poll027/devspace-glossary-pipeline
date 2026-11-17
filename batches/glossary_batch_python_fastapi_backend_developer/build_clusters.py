"""Stage 12 only: full-batch decisions and pre-submission self-checks."""
import collections
import datetime
import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent
inputs = {name: (B / name).read_bytes() for name in (
    'glossary_bundles_draft.json', 'extracted_concepts.json')}
draft = json.loads(inputs['glossary_bundles_draft.json'])
extracted = json.loads(inputs['extracted_concepts.json'])
concepts = extracted['concepts']
bundles = {(b['context']['path_id'], b['context']['concept_id']): b for b in draft['bundles']}
tiles = collections.defaultdict(list)
for c in concepts:
    tiles[c['path_id'], c['toc_location']['tile_id']].append(c)
for cs in tiles.values():
    cs.sort(key=lambda c: c['toc_sequence_position'])

# Chosen ranges are offsets within each tile, not hand-entered concept IDs.
chosen = {
    'tile_015': (0, 2, 'Install and run a service package',
        'These adjacent concepts are complementary steps in preparing a runnable Python service: reconstruct its declared dependencies and organize and execute its importable package. Both require only the isolated-environment foundation already available at tile start. Dependency installation and package identity retain separate sub-concepts and exercises; neither is presented as a substitute for the other.'),
    'tile_020': (0, 2, 'Compose validated request models',
        'Field constraints and nested models are complementary parts of declaring a validated request-data structure. Both build on model construction and type annotations already available at tile start. Keep value restrictions and structural composition as separate, ordered sub-concepts rather than implying that either declaration replaces the other.'),
    'tile_047': (0, 2, 'Declare and inspect an input contract',
        'Input presence, nullability and defaults describe the accepted input contract; OpenAPI generation supplies its inspectable public description. These adjacent concepts fit a declaration-and-inspection workflow, and both have their prerequisites before the tile. Keep executable input behavior distinct from generated documentation, and retain the separate absence, null and concrete-value cases.'),
    'tile_056': (0, 2, 'Bind and validate request metadata',
        'Header and cookie binding and request-validation errors fit the workflow of declaring metadata inputs and checking invalid request outcomes. All prerequisites for both are already available at tile start. Separate source/name binding from validation failure handling, and preserve the distinction between invalid client input and server-side validation bugs.'),
    'tile_059': (0, 2, 'Preserve input intent as contracts evolve',
        'Partial-update extraction and compatible contract changes share the problem of preserving what a client request means. Both can be learned from prerequisites already completed before this tile. Keep omitted fields versus explicit null visible in the update sub-concept, and keep compatibility review as its own broader contract check rather than treating partial-update extraction as proof of compatibility.'),
    'tile_067': (1, 3, 'Translate and format public API errors',
        'The adjacent error-translation and error-envelope concepts are complementary parts of turning recognized internal failures into stable public HTTP responses. Both have all prerequisites at tile start; the earlier model-boundary concept in this tile is not needed by either. Keep choosing an intentional HTTP outcome separate from formatting its body, preserving status, relevant headers and transaction recovery rather than allowing a uniform envelope to erase those boundaries.'),
    'tile_076': (0, 3, 'Commit and verify ORM resource mutations',
        'Creation, deletion and update are variants of one ORM resource-mutation workflow: change mapped state, complete the transaction and verify the durable result independently. Each concept has all prerequisites before the tile, so none needs another mutation introduced here. Preserve TOC order and separate operation labels: creation verifies stored identity and fields, deletion verifies absence, and update verifies changed and preserved fields. The shared explanation does not merge their bundles or exercises.'),
    'tile_080': (0, 2, 'Keep cache-backed reads correct',
        'Freshness and safe cache failure are complementary policies for the already-learned cache-aside read. Both have all prerequisites at tile start. Separate stale-data control through expiry and write invalidation from unavailable-cache handling through bounded waits and primary-store fallback; an expiry policy is not an outage policy, and a fallback does not establish freshness of an existing cached copy.'),
}
# Explicitly review every other multi-concept tile, including dependency exclusions.
skipped = {
    'tile_000': 'Browser access policy, method semantics and representation metadata are different foundational boundaries, not variants of one operation.',
    'tile_003': 'Type annotations and class/instance state require distinct foundational mental models.',
    'tile_005': 'Cleanup scope and cooperative scheduling are distinct execution mechanisms.',
    'tile_012': 'Preflight permission checking and general HTTP status selection are separate concerns.',
    'tile_022': 'Path-operation declarations require the resource-contract concept introduced within this tile.',
    'tile_026': 'Model invariants and intentional endpoint HTTP rejections need a visible boundary.',
    'tile_030': 'URL input binding and public output serialization should retain the input/output boundary.',
    'tile_034': 'Responsibility separation, background execution placement and dependency composition are not one workflow; the related boundary concepts are not adjacent.',
    'tile_037': 'Middleware configuration and production process serving operate at different boundaries.',
    'tile_045': 'Dependency reuse and general HTTP integration testing are not variants of one operation.',
    'tile_052': 'Shutdown verification and restart/traffic-eligibility probe contracts deserve distinct operational checks.',
    'tile_061': 'Identity retrieval and multi-write transaction boundaries teach different operations.',
    'tile_065': 'Schema migration and workload-driven indexing are separate change and performance decisions.',
    'tile_072': 'Request correlation and aggregate signal interpretation use different evidence and mental models.',
    'tile_074': 'Bounded listings and injection prevention are distinct defenses; one does not establish the other.',
    'tile_083': 'Documenting expected responses is not containment of unexpected runtime failures.',
    'tile_091': 'Issuer integration authenticates credentials; endpoint permissions authorize operations. Preserve that security boundary.',
    'tile_093': 'Durable event deduplication, authenticated timestamp freshness and outbound retry safety protect different boundaries.',
    'tile_097': 'Inspection requires security documentation introduced within this tile; documentation and HTTP security testing are nonadjacent.',
}
rows = []
reviewed = []
for (path_id, tile_id), cs in tiles.items():
    if len(cs) == 1:
        reviewed.append((tile_id, 'singleton'))
        continue
    assert (tile_id in chosen) != (tile_id in skipped), tile_id
    if tile_id not in chosen:
        reviewed.append((tile_id, skipped[tile_id]))
        continue
    lo, hi, title, reasoning = chosen[tile_id]
    selected = cs[lo:hi]
    assert len(selected) >= 2
    available = set(cs[0]['allowed_knowledge_ids'])
    for c in selected:
        bundle = bundles[path_id, c['concept_id']]
        assert bundle['context']['toc_location']['tile_id'] == tile_id
        assert set(c['direct_prerequisite_ids']) <= available
        assert set(bundle['context']['prerequisites']) <= available
        assert bundle['coverage']['required_facts'] and bundle['teaching_blocks']
    positions = [c['toc_sequence_position'] for c in selected]
    assert positions == list(range(positions[0], positions[0] + len(selected)))
    rows.append({
        'cluster_id': f'cluster_{path_id}_{tile_id}',
        'path_id': path_id, 'tile_id': tile_id, 'title': title,
        'concept_ids': [c['concept_id'] for c in selected],
        'reasoning': reasoning,
    })
    reviewed.append((tile_id, 'cluster'))

# Mistakes checklist: whole batch, real IDs, adjacency/order, tile containment,
# prerequisites at TILE start (not cluster start), no duplicate membership,
# preserved semantic boundaries, no curriculum/UI merge, exact input hashes.
assert len(reviewed) == len(tiles)
assert len(bundles) == len(concepts) == 100
assert len({r['cluster_id'] for r in rows}) == len(rows)
members = [(r['path_id'], cid) for r in rows for cid in r['concept_ids']]
assert len(set(members)) == len(members)
assert all(key in bundles for key in members)
metadata = extracted['metadata']
artifact = {
    'metadata': {
        'artifact_type': 'clusters', 'artifact_version': '1.0.0',
        'schema_version': '1.0.0', 'batch_id': extracted['batch_id'],
        'run_id': metadata['run_id'], 'prompt_version': '12_cluster_pass@v1',
        'model': 'none',
        'generated_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'source_snapshot_id': metadata['source_snapshot_id'],
        'parent_artifact_hashes': {n: hashlib.sha256(raw).hexdigest() for n, raw in inputs.items()},
    },
    'batch_id': extracted['batch_id'], 'clusters': rows,
}
(B / 'clusters.json').write_text(json.dumps(artifact, indent=2) + '\n')
print(f'Self-check PASS: {len(concepts)} concepts, {len(tiles)} tiles reviewed; '
      f'{len(rows)} clusters, {len(members)} clustered concepts, '
      f'{len(concepts) - len(members)} unclustered concepts.')
