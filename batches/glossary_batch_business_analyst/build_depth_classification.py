import json
import hashlib
import math
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter, defaultdict

batch = Path('batches/glossary_batch_business_analyst')
names = ['extracted_concepts.json', 'coverage_briefs.json']
inputs = {name: json.loads((batch / name).read_text()) for name in names}
concepts = inputs[names[0]]['concepts']
briefs = {(b['concept_id'], b['path_id']): b for b in inputs[names[1]]['briefs']}
# Reviewed assessment demands, in frozen input order; not a curriculum importance ranking.
actions = '''write a bounded problem statement from a vague complaint
conduct a stakeholder-specific interview yielding testable requirements
design and facilitate a workshop to converge on requirements
write unbiased survey questions and choose an elicitation method
extract explicit and implied requirements from a supplied document
compare observed work with the worker's account using session evidence
diagnose validation versus verification defects in a requirements list
produce a wireframe and elicit corrected requirements from reactions
run a judgment-suspending brainstorming session
moderate a focus group to surface agreement and disagreement
flag delivery, compliance or adoption risks in supplied requirements
assemble elicited requirements into a structured BRD
write precise expected system behavior for a business requirement
write a feature-specific user story and Gherkin acceptance criteria
write a goal-specific use case with main and alternate flows
build traceability links and detect orphaned requirements
apply lifecycle transitions and versioning to a change request
derive and write NFRs implied by a functional requirement
classify project-specific stakeholders by role or type
plot supplied stakeholders on the grid and justify placements
assign RACI roles to tasks without duplicate Accountable owners
match an engagement plan to stakeholder needs
apply a facilitation technique to a meeting problem
apply a conflict-resolution technique to a stakeholder dispute
select BPMN symbols for supplied process steps
produce an as-is diagram from a process walkthrough
produce a to-be diagram incorporating proposed changes
locate and justify bottlenecks in an as-is diagram
propose and justify an improvement for an identified bottleneck
extract implicit business rules from a process description
build a complete, consistent decision table from supplied rules
build a correctly ordered decision tree from sequential rules
infer entities and attributes from a business narrative
identify a valid primary key in supplied table columns
identify a foreign key and an integrity violation in related tables
determine and model a one-to-many relationship between entities
design a junction table for a many-to-many scenario
determine and notate cardinality for supplied related entities
produce an ERD for a business scenario
classify a supplied model as conceptual or logical and justify it
map a business question to the entities and attributes needed
assign dataset facts to appropriate relational tables
write a SELECT statement for a specified data need
write an INNER JOIN for supplied related tables
write a GROUP BY query with correct per-group aggregates
choose WHERE versus HAVING for a supplied filtering requirement
predict NULL behavior and apply IS NULL/COALESCE in a query
write a LEFT JOIN that preserves required unmatched rows
write a RIGHT JOIN that preserves required unmatched rows
write a FULL OUTER JOIN preserving all rows in a scenario
write ORDER BY for specified columns and directions
compose a query pattern answering a business reporting question
import and transform a raw source into report-ready data
connect Tableau to a raw source and prepare an extract/join
produce a current-state capability assessment for a business area
write a measurable future-state vision for a business goal
identify specific gaps between supplied current and future states
categorize business-scenario factors into SWOT quadrants
assign and justify MoSCoW categories for supplied requirements
classify supplied features using Kano and justify the choices
compute weighted option scores and rank the options
score candidate solutions and justify a recommendation
build a quantified business case for a proposed initiative
apply MCDA to a multi-dimensional decision scenario
compute central measures and justify the best choice for a dataset
compute and interpret spread differences between two datasets
rewrite or split a vague story to satisfy INVEST
refine and reorder a messy backlog into a sprint-ready state
sequence a prioritized backlog into releases respecting dependencies
define testable acceptance criteria for a supplied backlog item
turn raw findings into an audience-appropriate report
rewrite a technical statement accurately for a non-technical audience
structure a stakeholder presentation from supplied findings
plan a requirements walkthrough securing explicit sign-off
draw a context diagram from a system description
decompose a supplied top-level function into a hierarchy
apply reference types and aggregate functions in a formula-copy scenario
build a pivot table answering a specified summary question
write a lookup formula for supplied related tables
encode a supplied business rule as a conditional formula
choose and build a chart for a dataset and question
produce a spreadsheet answer to an ad hoc data question
diagnose insufficiently clear items in a candidate sprint backlog
choose the collaboration boundary and action for BA/PO role ambiguity
recognize an appropriate blocker update versus a detailed status report
check a demonstrated increment against its acceptance criteria
identify an actionable retrospective improvement from sprint events
apply Five Whys to a symptom to reach a distinct root cause
build and categorize candidate causes in a fishbone diagram
apply a DoD checklist to an item and flag a failing criterion
design fact and dimension tables for a business reporting process
configure correct relationships among imported BI tables
design a Power BI page for a reporting requirement
design a Tableau dashboard for a reporting requirement
identify and fix a supplied chart's visual design flaw
choose and execute sharing and permissions for a report audience
write a DAX measure for a metric and distinguish a calculated column
write a Tableau calculated expression for a metric requirement
centralize duplicated report calculations into a reusable definition'''.splitlines()
assert len(actions) == len(concepts) == 99
by_path = defaultdict(list)
for c in concepts:
    by_path[c['path_id']].append(c['dependency_graph_centrality'])
# Nearest-rank 75th percentile; include all concepts tied at the cutoff.
cutoffs = {p: sorted(v)[math.ceil(.75 * len(v)) - 1] for p, v in by_path.items()}
rows = []
for c, action in zip(concepts, actions):
    path = c['path_id']
    centrality = c['dependency_graph_centrality']
    cutoff = cutoffs[path]
    evidence = briefs[(c['concept_id'], path)]['evidence']
    facts = len(evidence['required_facts'])
    misconceptions = len(evidence['misconceptions'])
    high = centrality > 0 and centrality >= cutoff
    signal = ('at/above' if high else 'below')
    reason = (f'Centrality {centrality}, {signal} the {path} top-quartile cutoff {cutoff} '
              f'(75th-percentile nearest rank; ties included; {len(by_path[path])} concepts). '
              f'Coverage has {facts} required facts and {misconceptions} misconceptions. ')
    if c['concept_id'] == 'ba_dm.conceptual_vs_logical':
        tier = 'standard'
        reason += (f'Assessment asks the learner to {action}. This is model-type recognition with an explicit justification, '
                   'not model construction or combining ideas to solve a new business problem; justification warrants more '
                   'than recall/lookup despite zero downstream dependencies, so standard.')
    elif c['concept_id'] == 'ba_agile.daily_standup':
        tier = 'reference'
        reason += (f'Assessment asks the learner to {action}. This checks recognition of the update format, '
                   'not conducting a standup or resolving a blocker; zero downstream dependencies and a recognition-only '
                   'target support reference, despite the four supporting facts.')
    else:
        tier = 'core'
        reason += (f'Assessment requires the learner to {action}; this applies the idea to supplied situational '
                   'evidence rather than merely recalling a definition or looking up syntax, so core')
        if high:
            reason += ', also supported by top-quartile centrality.'
        elif centrality == 0:
            reason += '; zero downstream dependencies do not override the applied assessment.'
        else:
            reason += ' despite centrality below the top quartile.'
    rows.append({'concept_id': c['concept_id'], 'path_id': path, 'depth_tier': tier, 'reasoning': reason})

now = datetime.now(timezone.utc).isoformat()
meta = inputs[names[0]]['metadata']
artifact = {
    'metadata': {
        'artifact_type': 'depth_classification', 'artifact_version': '1.0.0', 'schema_version': '1.0.0',
        'batch_id': batch.name, 'run_id': meta['run_id'], 'prompt_version': '04_depth_classification@v1',
        'model': 'none', 'generated_at': now, 'source_snapshot_id': meta['source_snapshot_id'],
        'parent_artifact_hashes': {n: hashlib.sha256((batch / n).read_bytes()).hexdigest() for n in names}
    },
    'batch_id': batch.name, 'classifications': rows
}
# Own mistakes checklist: full pair coverage, no duplicates, actual numeric signals,
# per-path cutoff with explicit tie policy, no disposition ranking, applied zero-centrality
# cases not automatically Reference, recognition exceptions reviewed, exact input hashes.
expected = {(c['concept_id'], c['path_id']) for c in concepts}
actual = {(r['concept_id'], r['path_id']) for r in rows}
assert actual == expected and len(actual) == len(rows)
assert set(briefs) == expected
for c, r in zip(concepts, rows):
    assert r['concept_id'] == c['concept_id'] and r['path_id'] == c['path_id']
    assert f"Centrality {c['dependency_graph_centrality']}," in r['reasoning']
    assert 'disposition' not in r['reasoning']
for n, h in artifact['metadata']['parent_artifact_hashes'].items():
    assert hashlib.sha256((batch / n).read_bytes()).hexdigest() == h
out = batch / 'depth_classification.json'
out.write_text(json.dumps(artifact, indent=2, ensure_ascii=False) + '\n')
print(out)
print('Rows:', len(rows), 'Tiers:', dict(Counter(r['depth_tier'] for r in rows)), 'Cutoffs:', cutoffs)
print('Self-check passed: full batch, unique pairs, numerical signals, reviewed assessment demands, hashes.')
