import hashlib
import itertools
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path('batches/glossary_batch_business_analyst')
INPUTS = ['glossary_bundles_draft.json', 'extracted_concepts.json']
data = {name: json.loads((ROOT / name).read_text()) for name in INPUTS}
extracted = data['extracted_concepts.json']
draft = data['glossary_bundles_draft.json']
concepts = extracted['concepts']
lookup = {(c['path_id'], c['concept_id']): c for c in concepts}
bundles = {(b['context']['path_id'], b['context']['concept_id']): b for b in draft['bundles']}
assert len(lookup) == len(concepts)
assert len(bundles) == len(draft['bundles'])
assert set(lookup) == set(bundles)

# Reviewed candidates: positions are resolved to the exact input concept IDs.
# Only presentation grouping is proposed; the bundles are never rewritten.
choices = {
    'tile.01.01.02': ([3, 4, 5], 'Gathering requirements evidence',
        'These adjacent concepts are complementary channels for gathering requirements evidence: survey responses, existing documents, and observed work. Problem scoping, their shared prerequisite, is complete before this tile starts. Keep each channel separately labeled so stated attitudes, recorded material, and observed behavior are not treated as interchangeable evidence. Validation remains a separate step because its document-analysis prerequisite is not available at tile start.'),
    'tile.03.02.01': ([32, 33], 'Describing business data and identifying rows',
        'These adjacent concepts belong to the same initial data-description task: identify business entities and their descriptive attributes, then consider which column or columns uniquely identify table rows. Neither concept has a prerequisite in the inputs. Separate sub-concepts preserve the distinction between a descriptive attribute and a primary key with uniqueness and non-null requirements. Foreign keys stay outside this cluster because primary keys are their prerequisite within this tile.'),
    'tile.04.02.01': ([52, 53], 'Connecting BI tools to business data',
        'These adjacent concepts are tool-specific variants of connecting to and preparing a data source for BI work. Their relational-model prerequisite is already complete at tile start. Retain separate Power BI and Tableau sub-concepts and their own preparation commands; grouping does not imply that Power Query transformations and Tableau joins or extracts are the same operation.'),
    'tile.05.01.01': ([54, 55], 'Establishing the current and desired states',
        'These adjacent concepts establish the paired baseline and target for a state comparison. Their respective as-is and to-be modeling prerequisites are both complete before the tile starts. Separate current-state and desired-state labels preserve the essential distinction between the present situation and intended outcomes. Gap identification and SWOT remain separate because they depend on concepts introduced within this tile.'),
    'tile.07.01.01': ([70, 71], 'Writing findings for the audience',
        'These adjacent concepts are complementary parts of one communication task: structure a written report and adapt its detail and terminology to the audience. Neither has a prerequisite in the inputs. Keep report structure and audience adaptation as distinct sub-concepts rather than replacing either with a general communication lesson. Presentations and walkthroughs stay separate because their prerequisites are introduced within this tile.'),
    'tile.11.03.01': ([96, 97], 'Defining business metrics in BI tools',
        'These adjacent concepts are tool-specific variants of deriving business metrics from existing data. Both dashboard-design prerequisites and reporting-query patterns are complete before this tile starts. Preserve distinct Power BI DAX and Tableau calculation sub-concepts, including their own row-level and aggregate or report-context distinctions; no equivalence between their evaluation rules is implied. The semantic layer remains a later step because it requires both calculation concepts.'),
}

# Whole-batch review notes for every tile not selected. These are audit notes in
# the build script, not invented singleton or empty cluster records.
skips = {
    'tile.01.01.01': 'Interviews and workshops require problem scoping taught inside this tile.',
    'tile.01.01.03': 'Keep design feedback, divergent idea generation, moderated opinions, and risk assessment distinct; they are not one workflow or interchangeable operation.',
    'tile.01.02.01': 'Functional specifications require the BRD taught inside the tile.',
    'tile.01.02.02': 'Preserve the boundary between user-story acceptance scenarios and actor interaction specifications.',
    'tile.01.02.03': 'Lifecycle depends on traceability; the two tile-start-ready concepts are not adjacent.',
    'tile.02.01.01': 'The analysis matrices require stakeholder identification within the tile.',
    'tile.02.01.02': 'Facilitation and conflict resolution have intra-tile prerequisites.',
    'tile.03.01.01': 'Process modeling depends on notation, then to-be modeling on as-is modeling.',
    'tile.03.01.02': 'Improvement requires the gap analysis taught inside the tile.',
    'tile.03.01.03': 'Decision representations require rules analysis within the tile.',
    'tile.03.02.02': 'Relationship types and cardinality have intra-tile prerequisites.',
    'tile.03.02.03': 'Model level comparison and information mapping have intra-tile prerequisites.',
    'tile.04.01.01': 'SELECT and inner join depend on earlier concepts inside the tile.',
    'tile.04.01.02': 'Filtering depends on aggregation; the other tile-start-ready concepts are not adjacent.',
    'tile.04.01.03': 'Later outer joins have intra-tile prerequisites; preserve join-type boundaries.',
    'tile.04.01.04': 'Reporting patterns require sorting introduced inside the tile.',
    'tile.05.01.02': 'Preserve separate steps for scope categories, satisfaction classifications, and numerical weighted ranking; their outputs are not interchangeable.',
    'tile.05.01.03': 'Business case requires solution evaluation; the tile-start-ready concepts are not adjacent.',
    'tile.05.02.01': 'Spread requires measures of center within the tile.',
    'tile.06.01.01': 'Backlog management requires story writing within the tile.',
    'tile.06.01.02': 'Release sequencing and item-specific acceptance conditions answer different questions, not variants of one operation.',
    'tile.08.01.01': 'Functional decomposition requires scope modeling within the tile.',
    'tile.09.01.01': 'Pivot tables and lookups require basic formulas introduced in this tile.',
    'tile.09.01.02': 'Conditional formula evaluation and chart construction are different operations; ad hoc reporting has an intra-tile prerequisite.',
    'tile.10.01.01': 'Team collaboration requires sprint planning introduced in this tile.',
    'tile.10.01.02': 'Keep daily coordination and stakeholder outcome inspection distinct; retrospective also requires review within the tile.',
    'tile.10.02.01': 'Fishbone diagrams require Five Whys introduced within this tile.',
    'tile.10.02.02': 'Singleton tile cannot form a cluster.',
    'tile.11.01.01': 'BI model relationships require star-schema design introduced in this tile.',
    'tile.11.02.01': 'Tableau design requires Power BI design introduced in this tile.',
    'tile.11.02.02': 'Stakeholder delivery requires visual design introduced in this tile.',
}

clusters = []
reviewed = set()
used = set()
for path in extracted['paths']:
    pid = path['path_id']
    ordered = sorted((c for c in concepts if c['path_id'] == pid), key=lambda c: c['toc_sequence_position'])
    assert len(ordered) == path['concept_count']
    for tile, group in itertools.groupby(ordered, key=lambda c: c['toc_location']['tile_id']):
        rows = list(group)
        assert tile not in reviewed
        reviewed.add(tile)
        assert (tile in choices) != (tile in skips), tile
        if tile not in choices:
            continue
        positions, title, reasoning = choices[tile]
        selected = [c for c in rows if c['toc_sequence_position'] in positions]
        assert [c['toc_sequence_position'] for c in selected] == positions
        assert len(selected) >= 2
        indexes = [ordered.index(c) for c in selected]
        assert indexes == list(range(indexes[0], indexes[0] + len(indexes)))
        available = {c['concept_id'] for c in ordered if c['toc_sequence_position'] < rows[0]['toc_sequence_position']}
        for c in selected:
            ctx = bundles[(pid, c['concept_id'])]['context']
            assert ctx['toc_location']['tile_id'] == tile
            # Check transitive prerequisites too, using both artifacts.
            pending = list(set(c['direct_prerequisite_ids']) | set(ctx['prerequisites']))
            visited = set()
            while pending:
                prerequisite = pending.pop()
                if prerequisite in visited:
                    continue
                visited.add(prerequisite)
                assert prerequisite in available, (tile, c['concept_id'], prerequisite)
                pc = lookup[(pid, prerequisite)]
                pb = bundles[(pid, prerequisite)]['context']
                pending.extend(set(pc['direct_prerequisite_ids']) | set(pb['prerequisites']))
            assert (pid, c['concept_id']) not in used
            used.add((pid, c['concept_id']))
        clusters.append({
            'cluster_id': 'cluster_' + pid + '_' + tile.replace('.', '_'),
            'path_id': pid, 'tile_id': tile, 'title': title,
            'concept_ids': [c['concept_id'] for c in selected],
            'reasoning': reasoning,
        })
assert reviewed == set(choices) | set(skips)
assert len({c['cluster_id'] for c in clusters}) == len(clusters)

# Self-check / mistakes checklist: entire batch and every tile reviewed; no
# singleton, cross-tile, nonadjacent, reordered or duplicate membership; all
# prerequisites available at TILE start (not merely cluster start); semantic
# boundaries explicitly retained; bundles and TOC untouched; no UI prescription;
# exact source IDs and computed parent hashes; real UTC generation timestamp.
metadata = {
    'artifact_type': 'clusters', 'artifact_version': '1.0.0',
    'schema_version': '1.0.0', 'batch_id': extracted['batch_id'],
    'run_id': extracted['metadata']['run_id'],
    'prompt_version': '12_cluster_pass@v1', 'model': 'none',
    'generated_at': datetime.now(timezone.utc).isoformat(),
    'source_snapshot_id': extracted['metadata']['source_snapshot_id'],
    'parent_artifact_hashes': {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in INPUTS},
}
output = {'metadata': metadata, 'batch_id': extracted['batch_id'], 'clusters': clusters}
(ROOT / 'clusters.json').write_text(json.dumps(output, indent=2) + '\n')
print(f'Self-check PASS: {len(concepts)} concepts, {len(reviewed)} tiles, {len(extracted["paths"])} paths reviewed; {len(clusters)} clusters, {len(used)} clustered concepts, {len(skips)} skipped tiles.')
