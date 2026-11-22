import collections
import datetime
import hashlib
import json
from pathlib import Path

root = Path(__file__).parent
inputs = ['glossary_bundles_draft.json', 'extracted_concepts.json']
data = {name: json.loads((root / name).read_text()) for name in inputs}
extracted = data['extracted_concepts.json']
draft = data['glossary_bundles_draft.json']
concepts = sorted(extracted['concepts'], key=lambda c: (c['path_id'], c['toc_sequence_position']))
by_id = {(c['path_id'], c['concept_id']): c for c in concepts}
bundles = {(b['context']['path_id'], b['context']['concept_id']): b for b in draft['bundles']}
assert set(by_id) == set(bundles)
tiles = collections.defaultdict(list)
for c in concepts:
    tiles[(c['path_id'], c['toc_location']['tile_id'])].append(c)

# All tiles are reviewed. Only these four adjacent runs pass both readiness
# and the shared-idea test; all other concepts remain separate.
selections = [
    ('038_040', 'Interactive execution in the Python runtime',
     ['python.interactive_execution', 'python.interpreter_execution_model'],
     'These adjacent concepts connect investigating expressions in a live interpreter with how the selected runtime evaluates source and binds current values. All declared prerequisites for both are available before this tile starts. Keep interactive-session behavior and the runtime model as distinct sub-concepts, including the CPython-specific bytecode qualification; expression layout remains a separate step.'),
    ('051_053', 'Exception flow and cleanup',
     ['python.exception_hierarchy', 'python.exception_propagation', 'python.finally_cleanup'],
     'These adjacent concepts describe parts of one exception-control-flow story: classifying the failure, following handler matching and propagation, and accounting for cleanup when control leaves the protected operation. All declared prerequisites are available at tile entry. Preserve separate sub-concepts for hierarchy, recovery and cleanup so finally is not presented as catching or recovering from an exception, and ordinary Exception subclasses remain distinct from BaseException termination signals.'),
    ('057_059', 'Signaling and locating a failure',
     ['python.raising_exceptions', 'python.reading_tracebacks'],
     'These adjacent concepts form a failure-reporting workflow: signal a specific invalid operation with meaningful context, then locate the reported failure using its exception message and traceback frames. Both have all declared prerequisites before the tile begins. Keep raising and inspecting a report as distinct steps. Exclude debugger usage because it requires reading_tracebacks, which is not available at tile entry.'),
    ('071_073', 'Collaborators behind an object interface',
     ['python.composition', 'python.encapsulation_conventions'],
     'These adjacent concepts are complementary parts of an object interface: delegate work to a contained collaborator and expose public behavior without making clients manage supporting state. Both require only previously taught initialization and instance methods. Keep delegation and non-public naming conventions as separate sub-concepts, explicitly retaining that an underscore is not enforced access protection. Leave inheritance and super as a separate step to preserve the boundary between containing a collaborator and inheriting behavior.'),
]

# Specific content-based exclusions for all other prerequisite-ready runs.
skip_ready = {
    '015_017': 'Tuple results, argument binding defaults and name scope are distinct mental models, not variants of one operation.',
    '027_028': 'Console interaction and indexed traversal are independent capabilities.',
    '035_037': 'Invoking a saved script and classifying expressions/statements are different tasks; comments additionally lack tile-entry prerequisites.',
    '047_048': 'Shared mutable state/copying and frequency counting with Counter are different operations.',
    '049_050': 'Observing runtime state and documenting a callable interface serve different purposes.',
    '063_064': 'Keep handler dispatch separate from diagnosis of input, implementation and operational failures to foreground the recovery-versus-code-correction boundary.',
}
clusters = []
selected_tiles = set()
for suffix, title, ids, reasoning in selections:
    path_id = 'learn_python'
    tile_id = 'learn_python.tile.' + suffix
    cs = tiles[(path_id, tile_id)]
    positions = [next(i for i, c in enumerate(cs) if c['concept_id'] == cid) for cid in ids]
    assert positions == list(range(positions[0], positions[0] + len(ids)))
    start_allowed = set(cs[0]['allowed_knowledge_ids'])
    for cid in ids:
        c = by_id[(path_id, cid)]
        assert set(c['direct_prerequisite_ids']) <= start_allowed
        assert set(bundles[(path_id, cid)]['context']['prerequisites']) <= start_allowed
        # Check transitive internal prerequisites as well.
        pending = list(c['direct_prerequisite_ids'])
        seen = set()
        while pending:
            dep = pending.pop()
            if dep in seen:
                continue
            seen.add(dep)
            assert dep in start_allowed
            if (path_id, dep) in by_id:
                pending.extend(by_id[(path_id, dep)]['direct_prerequisite_ids'])
    clusters.append(dict(cluster_id='cluster_learn_python_' + suffix,
                         path_id=path_id, tile_id=tile_id, title=title,
                         concept_ids=ids, reasoning=reasoning))
    selected_tiles.add((path_id, tile_id))

# Own mistakes checklist: cover every tile; never cross tiles; no singleton,
# duplicate, reordered or nonadjacent members; no missing tile-entry prereq;
# shared idea rather than mere proximity; important boundaries stay explicit;
# bundles/TOC untouched; exact parent hashes and real UTC metadata.
review = {}
for key, cs in tiles.items():
    if key in selected_tiles:
        review[key] = 'selected adjacent run; other members remain separate'
        continue
    if len(cs) == 1:
        review[key] = 'singleton tile'
        continue
    allowed = set(cs[0]['allowed_knowledge_ids'])
    eligible = [set(c['direct_prerequisite_ids']) <= allowed for c in cs]
    has_ready_pair = any(a and b for a, b in zip(eligible, eligible[1:]))
    suffix = key[1].split('.')[-1]
    if has_ready_pair:
        assert suffix in skip_ready, (key, 'unreviewed eligible run')
        review[key] = skip_ready[suffix]
    else:
        review[key] = 'no two adjacent concepts have every prerequisite at tile entry'
assert len(review) == len(tiles)
assert len({c['cluster_id'] for c in clusters}) == len(clusters)
member_keys = [(c['path_id'], cid) for c in clusters for cid in c['concept_ids']]
assert len(member_keys) == len(set(member_keys))
metadata = dict(draft['metadata'])
metadata.update(artifact_type='clusters', artifact_version='1.0.0', schema_version='1.0.0',
                batch_id='glossary_batch_learn_python', model='none',
                prompt_version='12_cluster_pass@v1',
                generated_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                parent_artifact_hashes={name: hashlib.sha256((root / name).read_bytes()).hexdigest() for name in inputs})
artifact = dict(metadata=metadata, batch_id='glossary_batch_learn_python', clusters=clusters)
(root / 'clusters.json').write_text(json.dumps(artifact, indent=2) + '\n')
print(f'Self-check passed: {len(concepts)} concepts, {len(tiles)} tiles reviewed; {len(clusters)} clusters, {len(member_keys)} clustered concepts; {len(tiles)-len(selected_tiles)} tiles skipped.')
