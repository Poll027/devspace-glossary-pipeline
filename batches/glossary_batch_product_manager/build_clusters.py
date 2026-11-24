import collections
import datetime
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parent
inputs = ['extracted_concepts.json', 'glossary_bundles_draft.json']
extracted, draft = [json.loads((root / name).read_text()) for name in inputs]
concepts = sorted(extracted['concepts'], key=lambda c: (c['path_id'], c['toc_sequence_position']))
by_id = {(c['path_id'], c['concept_id']): c for c in concepts}
bundles = {(b['context']['path_id'], b['context']['concept_id']): b for b in draft['bundles']}
tiles = collections.defaultdict(list)
for c in concepts:
    tiles[(c['path_id'], c['toc_location']['tile_id'])].append(c)

# Whole-batch editorial decisions. Positions select consecutive sub-concepts,
# not merged curriculum; every omitted tile is explicitly reviewed below.
selected = {
    'tile.01.01.01': ([0, 1], 'Purpose, principles and product direction',
        'These adjacent concepts are complementary parts of setting product direction: apply the organization\'s purpose and principles, then articulate the product\'s desired future impact. Neither has a prerequisite missing at tile entry. Keep the present organizational mission and guiding values distinct from the future product vision; retain both individual explanations in TOC order.'),
    'tile.03.02.01': ([18, 19], 'Documenting the problem and proposed product',
        'These adjacent concepts belong to one specification-writing workflow: distinguish the user problem from the proposed solution, then document what will be built and why in a PRD. Their shared problem-statement and solution-specification prerequisites precede this tile. Keep problem and solution separately identified within the documentation; exclude the later One-Pager because it requires the PRD concept taught in this tile.'),
    'tile.04.01.02': ([27, 28], 'Sequencing roadmap work into releases',
        'These adjacent concepts are two levels of one sequencing operation: assign roadmap work to release windows and order features so prerequisite outputs are available. Product Roadmap is already available at tile entry for both. Preserve the distinction between release-window grouping and executable feature order rather than treating sequencing as a new prioritization decision.'),
    'tile.04.02.01': ([29, 30], 'Forecasting delivery and planning the quarter',
        'These adjacent concepts support one capacity-aware planning workflow: forecast timing from estimated work and completion rate, then check intended quarterly progress against capacity and dependencies. All prerequisites precede the tile. Keep the forecast and its uncertainty distinct from quarterly goals, owners and milestones; the shared explanation must not turn an estimate into a guaranteed commitment.'),
    'tile.04.02.02': ([31, 32], 'Scoping initiatives and coordinating handoffs',
        'These adjacent concepts are complementary parts of planning a body of work: make its goal, scope and success criteria explicit, then identify provider outputs and handoffs affecting execution. All prerequisites are available at tile entry. Preserve the initiative brief as an outcome-and-scope artifact and the dependency map as a coordination artifact, with separate concept explanations.'),
    'tile.07.03.01': ([62, 63], 'Making blockers visible and managing work flow',
        'Only the final two adjacent concepts share this compact workflow: track a blocked item and its agreed resolution action, then manage visible work stages and WIP limits so existing work can finish or be unblocked. All prerequisites precede the tile. Keep sprint-level dependency coordination distinct from Kanban flow control; a board does not itself resolve a dependency, and the cluster does not equate Scrum with Kanban.'),
    'tile.08.01.01': ([66, 67, 68], 'Customer-value goals and progress indicators',
        'These adjacent concepts form one outcome-monitoring workflow: identify a central customer-value measure, express intended improvement through an objective and measurable key results, and distinguish precursors from realized outcomes when monitoring progress. All prerequisites precede the tile. Retain the boundaries between a North Star metric, an OKR goal-setting structure, and leading/lagging classification; they are not interchangeable metrics or frameworks.'),
    'tile.09.01.01': ([78, 79, 80], 'Preparing a supported product launch',
        'These adjacent concepts are coordinated parts of launch preparation: assess readiness evidence, plan audience-specific communications, and equip sales and support with materials and training. Release management, audience adaptation and product messaging are already available at tile entry wherever required; no member requires another member as a prerequisite. Keep readiness gates, message delivery and team enablement as distinct responsibilities, rather than implying communication alone establishes readiness.'),
    'tile.10.02.01': ([83, 84], 'Evidence-grounded design feedback and decisions',
        'These adjacent concepts are complementary operations in turning usability observations into design action: communicate an observed issue against a user outcome, and synthesize reliable patterns into prioritized design changes. Usability Testing and Success Metrics are already available at tile entry wherever required. Preserve TOC order and distinguish feedback about an observation from synthesis of multiple findings; neither should present an isolated observation as a validated pattern.'),
}
skipped = {
    'tile.01.01.02': 'Positioning has within-tile prerequisites; the eligible proposition and competitor assessment have distinct teaching operations.',
    'tile.02.01.01': 'Both later concepts require the interviews taught in this tile.',
    'tile.02.02.01': 'Survey instrument design, segment definition and market-revenue estimation are distinct methods, not one operation.',
    'tile.02.03.01': 'Research representation and test-session moderation are distinct operations.',
    'tile.02.03.02': 'Singleton tile.',
    'tile.03.01.01': 'Later members require the problem statement taught in this tile.',
    'tile.03.03.01': 'Acceptance Criteria requires User Stories; user flows and success measures are distinct artifacts rather than one operation.',
    'tile.04.01.01': 'Capacity Planning requires Product Roadmap taught in this tile.',
    'tile.05.01.01': 'Hypothesis-testing scope and initiative value/effort comparison have different decision boundaries.',
    'tile.05.02.01': 'Each later scoring concept has within-tile prerequisites.',
    'tile.05.03.01': 'Tradeoff comparison and satisfaction classification are distinct decision methods.',
    'tile.05.03.02': 'Coarse time horizons and single-release scope categories must not be conflated.',
    'tile.06.01.01': 'Later members require Stakeholder Management taught in this tile.',
    'tile.06.02.01': 'All later members require Audience Adaptation taught in this tile.',
    'tile.06.03.01': 'Negotiation requires within-tile Conflict Resolution; roadmap expectation-setting and dispute resolution are distinct operations.',
    'tile.07.01.01': 'Effort Estimation requires within-tile Backlog Management, separating the other eligible members.',
    'tile.07.02.01': 'Later ceremonies have within-tile prerequisites; preserve ceremony boundaries.',
    'tile.07.04.01': 'Release Management requires Definition of Done taught in this tile.',
    'tile.08.02.01': 'Hypothesis formulation, dashboard reading and instrumentation planning are distinct operations.',
    'tile.08.03.01': 'Funnel-stage conversion and cohort retention comparison answer different analytic questions; preserve that boundary.',
    'tile.08.04.01': 'Decisions and Holdouts have within-tile prerequisites; A/B Testing and Feature Flags are not adjacent.',
    'tile.10.01.01': 'Design partnership roles and journey-map construction are distinct operations.',
}
assert set(selected).isdisjoint(skipped)
assert {tile for _, tile in tiles} == set(selected) | set(skipped), 'Every tile needs a reviewed decision'
rows = []
for (path, tile), members in tiles.items():
    if tile not in selected:
        continue
    positions, title, reasoning = selected[tile]
    chosen = [c for c in members if c['toc_sequence_position'] in positions]
    assert [c['toc_sequence_position'] for c in chosen] == positions
    rows.append({
        'cluster_id': 'cluster_' + path + '_' + tile.replace('.', '_'),
        'path_id': path, 'tile_id': tile, 'title': title,
        'concept_ids': [c['concept_id'] for c in chosen], 'reasoning': reasoning,
    })

# Generator mistakes checklist: schema, IDs, unique membership, same tile,
# true adjacency in full TOC, TOC order, entry prerequisites (including their
# transitive prerequisites), and no UI decisions or curriculum/bundle edits.
seen = set()
for row in rows:
    members = tiles[(row['path_id'], row['tile_id'])]
    entry_allowed = set(members[0]['allowed_knowledge_ids'])
    earlier = {c['concept_id'] for c in concepts if c['path_id'] == row['path_id'] and c['toc_sequence_position'] < members[0]['toc_sequence_position']}
    cs = [by_id[(row['path_id'], cid)] for cid in row['concept_ids']]
    positions = [c['toc_sequence_position'] for c in cs]
    assert positions == list(range(positions[0], positions[0] + len(cs)))
    assert len(cs) >= 2
    for c in cs:
        key = (row['path_id'], c['concept_id'])
        assert key not in seen
        seen.add(key)
        assert c['toc_location']['tile_id'] == row['tile_id']
        bundle = bundles[key]
        assert bundle['context']['toc_location']['tile_id'] == row['tile_id']
        pending = list(set(c['direct_prerequisite_ids']) | set(bundle['context']['prerequisites']))
        checked = set()
        while pending:
            prerequisite = pending.pop()
            if prerequisite in checked:
                continue
            checked.add(prerequisite)
            assert prerequisite in entry_allowed and prerequisite in earlier, (row['tile_id'], prerequisite)
            pending.extend(by_id[(row['path_id'], prerequisite)]['direct_prerequisite_ids'])
assert len({r['cluster_id'] for r in rows}) == len(rows)
metadata = {
    'artifact_type': 'clusters', 'artifact_version': '1.0.0', 'schema_version': '1.0.0',
    'batch_id': 'glossary_batch_product_manager',
    'run_id': extracted['metadata']['run_id'],
    'prompt_version': '12_cluster_pass@v1', 'model': 'gpt-6.1-sol',
    'generated_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'source_snapshot_id': extracted['metadata']['source_snapshot_id'],
    'parent_artifact_hashes': {name: hashlib.sha256((root / name).read_bytes()).hexdigest() for name in inputs},
}
output = {'metadata': metadata, 'batch_id': metadata['batch_id'], 'clusters': rows}
(root / 'clusters.json').write_text(json.dumps(output, indent=2, ensure_ascii=False) + '\n')
print(f'Reviewed {len(concepts)} concepts in {len(tiles)} tiles; {len(rows)} clusters, {len(seen)} clustered concepts, {len(skipped)} skipped tiles.')
