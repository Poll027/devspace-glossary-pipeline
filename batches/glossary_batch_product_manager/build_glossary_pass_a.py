import json, hashlib, re
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter

ROOT=Path('batches/glossary_batch_product_manager')
inputs=['coverage_briefs.json','extracted_concepts.json','depth_classification.json']
doc={name:json.loads((ROOT/name).read_text()) for name in inputs}
briefs=doc['coverage_briefs.json']['briefs']
concepts=doc['extracted_concepts.json']['concepts']
depths={(x['concept_id'],x['path_id']):x for x in doc['depth_classification.json']['classifications']}
bmap={(x['concept_id'],x['path_id']):x for x in briefs}
prose={}
for chunk in re.split(r'^@@', (ROOT/'pass_a_prose.txt').read_text(), flags=re.M)[1:]:
    num,body=chunk.split('\n',1)
    pieces=body.strip().split('\n---\n')
    assert len(pieces)==3,(num,len(pieces))
    prose[int(num)]=pieces
assert set(prose)==set(range(len(concepts)))
# Need reasons describe an instructional visual, not a claim about a candidate.
visual={
3:('MEDIUM','An annotated alternatives comparison would help show how a shared dimension supports a gap or threat judgment.',['data_table_demo']),
6:('MEDIUM','A neutral-prompt interview role-play would help distinguish follow-up questions from leading the participant.',['talking_head_with_visual_support']),
7:('MEDIUM','A worked reframing of a feature request into situation, task, and desired outcome would help with drafting a job statement.',['whiteboard_drawing']),
8:('MEDIUM','A demonstration grouping raw comments into themes would help make recurrence and consequence visible.',['data_table_demo']),
9:('MEDIUM','Revising flawed survey items and checking response options would help learners apply the wording rules.',['slides_with_signaling']),
11:('HIGH','A nested market diagram and worked calculation would show total, geographically reachable, and obtainable revenue boundaries and assumptions.',['whiteboard_drawing','data_table_demo']),
12:('MEDIUM','A worked research-to-persona example would help distinguish recurring evidence from decorative persona details.',['slides_with_signaling']),
13:('HIGH','A simulated task session would show user actions, facilitator restraint, and the distinction between observation and opinion.',['screen_demo','talking_head_with_visual_support']),
14:('HIGH','Annotated retention curves over time would clarify early versus sustained use and contrast stabilization with decline toward zero.',['diagram_animation','data_table_demo']),
16:('MEDIUM','A worked prompt revision and ideation demonstration would help show how wording opens or narrows the solution space.',['whiteboard_drawing']),
17:('MEDIUM','An annotated proposal would help connect intended behavior with scope, exclusions, constraints, and unresolved questions.',['slides_with_signaling']),
19:('MEDIUM','An annotated specification review would help learners find ambiguity across purpose, behavior, scope, and constraints.',['slides_with_signaling']),
22:('MEDIUM','Comparing delivered behavior against concrete criteria would help show what makes a condition testable.',['annotated_ui']),
23:('HIGH','Drawing decision branches and endpoints would make the task sequence and missing routes visible.',['whiteboard_drawing','diagram_animation']),
25:('MEDIUM','An annotated roadmap would help connect goals, prioritized initiatives, audience detail, and the planning horizon.',['slides_with_signaling']),
26:('HIGH','A worked capacity table would show historical average, baseline forecast, and adjustments as distinct planning steps.',['spreadsheet_demo']),
27:('HIGH','Moving work across release windows would help show why prerequisites and capacity constrain grouping.',['whiteboard_drawing']),
28:('HIGH','A dependency diagram would make feasible sequences and dependency-driven changes in order visible.',['diagram_animation','whiteboard_drawing']),
29:('HIGH','A worked forecast and timeline would connect work units to iterations and then to a range on the calendar.',['spreadsheet_demo','whiteboard_drawing']),
30:('MEDIUM','A quarterly planning example would help align goals, initiatives, owners, and milestones with capacity.',['slides_with_signaling']),
32:('HIGH','A provider-output-handoff diagram would show cross-team dependencies and downstream consequences of changes.',['whiteboard_drawing']),
33:('MEDIUM','A worked scope reduction would help distinguish preserving core value from arbitrary feature removal.',['slides_with_signaling']),
34:('HIGH','Placing initiatives on a two-axis matrix would make quadrant relationships and impact-effort tradeoffs visible.',['whiteboard_drawing']),
35:('MEDIUM','An annotated comparison of impact estimates and confidence would help separate predicted magnitude from evidential support.',['data_table_demo']),
36:('HIGH','A worked scoring table would demonstrate proportional confidence and how changed inputs affect RICE rankings.',['spreadsheet_demo']),
37:('MEDIUM','A worked ICE score comparison would help apply the named multiplication convention and avoid reversing ease.',['data_table_demo']),
38:('HIGH','A weighted-score table with changing weights would make contributions and sensitivity of the ranking visible.',['spreadsheet_demo']),
39:('MEDIUM','A worked alternatives comparison would help make opportunity cost and the accepted downside explicit.',['data_table_demo']),
43:('HIGH','Placing stakeholders on a power-interest map would show the two dimensions and corresponding engagement approaches.',['whiteboard_drawing']),
44:('MEDIUM','A cross-functional handoff example would help connect owners, constraints, and communication to a shared outcome.',['whiteboard_drawing']),
45:('MEDIUM','A discussion role-play would help distinguish consent, unanimity, unresolved concerns, and an explicitly changed decision rule.',['talking_head_with_visual_support']),
47:('MEDIUM','An annotated status update would help learners separate actual progress, deviations, owners, and requests.',['slides_with_signaling']),
48:('MEDIUM','A before-and-after update would demonstrate moving the executive decision and key implication ahead of technical detail.',['slides_with_signaling']),
50:('MEDIUM','A roadmap update example would help show how to explain changes and invite input at an audience-appropriate detail level.',['slides_with_signaling']),
51:('MEDIUM','A conflict-resolution role-play would help distinguish observations from blame and move needs toward an explicit tradeoff.',['talking_head_with_visual_support']),
52:('MEDIUM','A negotiation role-play would help reveal the underlying need behind a stated position and compare workable options.',['talking_head_with_visual_support']),
53:('MEDIUM','A worked backlog cleanup would help show how obsolete, unclear, and valuable items lead to a revised order.',['data_table_demo']),
54:('MEDIUM','A planning-poker demonstration would show independent estimates, reveal, discussion, and re-estimation.',['talking_head_with_visual_support']),
55:('MEDIUM','A feasibility conversation would help distinguish a hard constraint from a manageable risk or scope-cost tradeoff.',['talking_head_with_visual_support']),
56:('MEDIUM','A Sprint Planning role example would help separate product briefing from Developer selection and implementation planning.',['talking_head_with_visual_support']),
57:('MEDIUM','A short event and follow-up example would help show how a product question is handled without becoming a management report.',['talking_head_with_visual_support']),
58:('MEDIUM','A review demonstration would help connect completed work, the goal, stakeholder feedback, and next steps.',['screen_demo']),
59:('MEDIUM','A retrospective action-triage example would help assign follow-up without making the PM own every improvement.',['data_table_demo']),
60:('MEDIUM','An item-refinement demonstration would help show clarification, splitting, and revising estimates and ordering.',['data_table_demo']),
61:('MEDIUM','A worked debt-versus-feature comparison would help make future impact and the chosen capacity tradeoff explicit.',['data_table_demo']),
62:('HIGH','A blocker diagram with status changes would show how the missing output, provider, blocked item, and resolution connect.',['whiteboard_drawing']),
63:('HIGH','Moving cards on a board would show workflow state, a full WIP-limited stage, and finishing or unblocking work instead of starting more.',['screen_demo','annotated_ui']),
65:('MEDIUM','A release-plan walkthrough would help link scope and timing with dependencies, readiness, and post-release response.',['slides_with_signaling']),
66:('MEDIUM','A worked value-to-metric diagram would help connect core customer value with a candidate North Star and actionable inputs.',['whiteboard_drawing']),
69:('MEDIUM','An annotated hypothesis revision would help make audience, metric direction, success boundary, and contradictory evidence explicit.',['slides_with_signaling']),
70:('HIGH','An annotated dashboard comparison would show how definitions, periods, and related measures change the reading of an anomaly.',['data_table_demo','annotated_ui']),
71:('MEDIUM','A tracking-plan table walkthrough would help connect questions with event occurrence, ownership, and typed contextual properties.',['data_table_demo']),
72:('HIGH','A stepwise funnel with worked denominators would show conversion and drop-off between steps without implying a cause.',['diagram_animation','data_table_demo']),
73:('HIGH','An annotated cohort table would make relative periods, entry conditions, and return behavior visible across groups.',['data_table_demo']),
74:('HIGH','A diagram of assignment and annotated experiment results would help distinguish a favorable difference from evidence under the reported significance threshold.',['diagram_animation','data_table_demo']),
76:('HIGH','A staged exposure demonstration would show changing rollout fractions, readiness checks, and rollback state.',['diagram_animation','annotated_ui']),
77:('HIGH','A changing-state diagram would show a held-out baseline remaining excluded while eligible exposed users receive specified changes.',['diagram_animation']),
78:('MEDIUM','A worked readiness checklist would help connect evidence and unmet gates to a justified go/no-go recommendation.',['data_table_demo']),
79:('MEDIUM','A launch communication timeline would help sequence audience-specific messages, channels, and owners around introduction.',['whiteboard_drawing']),
80:('MEDIUM','An annotated enablement packet would help check whether representatives can explain value, limitations, answers, and escalation unaided.',['slides_with_signaling']),
81:('MEDIUM','A design-review role example would help separate evidence-based contribution from agreed decision authority.',['talking_head_with_visual_support']),
82:('HIGH','Building a journey map would show actor, phases, actions, thoughts, emotions, and research-grounded pain points together.',['whiteboard_drawing']),
83:('MEDIUM','An annotated design-feedback example would help separate observation, interpretation, and actionable request.',['annotated_ui']),
84:('MEDIUM','A worked findings table would help connect repeated evidence and severity judgments to proposed design changes.',['data_table_demo'])
}
# Focused self-contained explanations for the simpler writing/classification concepts.
low_reasons={
0:'The purpose-and-principles filter is understandable from the two feature comparisons; a simple written comparison suffices.',
1:'The future-state statement and task-list contrast are clear in text; a labeled statement is enough.',
2:'The customer-problem-benefit sentence can be understood and annotated directly in text.',
4:'A labeled positioning sentence and its customer-benefit contrast suffice without a dynamic demonstration.',
5:'The initiative-to-measured-outcome link is clear from a simple written chain.',
10:'The needs-based group comparison is clear in a small static table; dynamic media would mainly repeat the text.',
15:'The user-problem-consequence draft and feature-absence contrast are clear in a labeled paragraph.',
18:'The separate problem and proposal sentences directly demonstrate the distinction.',
20:'The one-page content and purpose can be understood from a short annotated brief without a dynamic demonstration.',
21:'The common story form and worked sentence teach the concept directly; a simple annotation suffices.',
24:'The distinction between metric, benchmark, target, and period is clear in the worked written example.',
31:'The initiative brief and its included/excluded scope can be understood in a static labeled example.',
40:'The satisfaction categories and feedback-based classifications are clear in a small static comparison.',
41:'The three priority buckets and non-date distinction are adequately taught with a simple static layout.',
42:'The four release-scoping categories and consequences of omission fit a static comparison.',
46:'The three audience-specific messages can be compared directly in text while preserving the same facts.',
49:'The benefit-led headline and supporting points are understandable as a labeled written example.',
64:'The shared-completion versus item-specific distinction is clear from the written checklist comparison.',
67:'The objective, measured key results, and activity contrast fit a static annotated example.',
68:'The precursor-versus-realized-outcome classification is clear in the written comparison; moving visuals are unnecessary.',
75:'The two definitions and evidence-context decision example suffice in text; a simple comparison adds little beyond that.'
}
assert set(visual)|set(low_reasons)==set(prose)
assert not set(visual)&set(low_reasons)
entries=[]
for i,c in enumerate(concepts):
    key=(c['concept_id'],c['path_id']); b=bmap[key]; tier=depths[key]['depth_tier']; assert tier=='core'
    ev=b['evidence'];facts=ev['required_facts']; ids=[f['id'] for f in facts]; intro,example,walkthrough=prose[i]
    blocks=[]
    def add(purpose,title,text,refs):
        blocks.append({'id':f'tb{len(blocks)+1}','purpose':purpose,'title':title,'content':text,'fact_ids':refs})
    add('intro',c['concept_name']+' in product work',intro,ids[:2])
    split=2 if len(facts)>3 else 1
    add('definition','The central idea',' '.join(f['statement'] for f in facts[:split]),ids[:split])
    add('mechanism','How to apply it',' '.join(f['statement'] for f in facts[split:]),ids[split:])
    add('example','Worked Product Manager example',example,ids)
    add('walkthrough','Reason through the example',walkthrough,ids)
    if ev['misconceptions']:
        add('misconception','Keep this distinction clear',' '.join(m['statement'] for m in ev['misconceptions']),[m['id'] for m in ev['misconceptions']])
    if i in visual:
        level,reason,modes=visual[i]
    else:
        level,reason,modes='LOW',low_reasons[i],['slides_with_signaling']
    notes=[
        'Teach at beginner-to-job-ready Product Manager depth: product decisions and interpretation, not engineering implementation or advanced statistical modeling.',
        'Keep the explanation within '+c['toc_location']['tile_title']+'; establish the central idea before working through the example.',
        'Focus the learner on this objective: '+b['learning_objective'],
        'The numerical values, product proposals, and organization scenarios in the worked example are illustrative, not claims about an actual company or tool.',
    ]
    if c['blocked_knowledge_ids']:
        notes.append('Do not expand into later concepts: '+', '.join(c['blocked_knowledge_ids'][:3])+'.')
    entries.append({'concept_id':c['concept_id'],'path_id':c['path_id'],'teaching_blocks':blocks,'video_need':{'level':level,'reason':reason,'preferred_visual_modes':modes},'teaching_notes':notes})
m=doc['extracted_concepts.json']['metadata'].copy()
m.update(artifact_type='glossary_pass_a',artifact_version='1.0.0',schema_version='1.0.0',batch_id='glossary_batch_product_manager',model='none',prompt_version='05_glossary_pass_a@v1',generated_at=datetime.now(timezone.utc).isoformat(),parent_artifact_hashes={n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in inputs})
out={'metadata':m,'batch_id':'glossary_batch_product_manager','entries':entries}
(ROOT/'glossary_pass_a.part.all.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
# Self-check mechanics and the canary checklist. No executable snippets are used.
assert len(entries)==85 and len({(e['concept_id'],e['path_id']) for e in entries})==85
assert set(bmap)=={(e['concept_id'],e['path_id']) for e in entries}==set(depths)
for e in entries:
    ev=bmap[(e['concept_id'],e['path_id'])]['evidence']
    known={f['id'] for cat in ['required_facts','misconceptions','optional_enrichment'] for f in ev[cat]}
    used={f for t in e['teaching_blocks'] for f in t['fact_ids']}
    assert used<=known and {f['id'] for f in ev['required_facts']}<=used
    assert all(t['fact_ids'] for t in e['teaching_blocks'])
    text=' '.join(t['content'] for t in e['teaching_blocks'])
    assert not re.search(r'\b(video|clip|watch|youtube)\b',text,re.I)
    assert e['video_need']['level']!='NONE' or not e['video_need']['preferred_visual_modes']
    # Required facts, including their hedges and boundaries, stay intact in the dedicated teaching prose.
    for f in ev['required_facts']: assert f['statement'] in text
assert 10000*120==1200000 and 4000*120==480000 and 480000*.05==24000 and 480000*.02==9600
assert 48/4==12 and 12*3==36 and 60/15==4 and 60/12==5 and 60/20==3
assert 1000*2*.8/4==400 and 800*3*.5/2==600 and 800*3*.25/2==300
assert 6*8*9==432 and 9*4*5==180
assert round(5*.6+2*.4,2)==3.8 and round(3*.6+5*.4,2)==3.8
assert round(5*.8+2*.2,2)==4.4 and round(3*.8+5*.2,2)==3.4
assert 400/800==600/1200==.5
assert 600/1000==.6 and 300/600==.5 and 300/1000==.3
wc=[sum(len(t['content'].split()) for t in e['teaching_blocks']) for e in entries]
print('entries',len(entries),'blocks',sum(len(e['teaching_blocks']) for e in entries),'video_need',dict(Counter(e['video_need']['level'] for e in entries)))
print('words min/mean/max',min(wc),round(sum(wc)/len(wc)),max(wc))
print('All coverage, fact-id, hedge-preservation, standalone-text, calculation, and video-need checks passed.')
