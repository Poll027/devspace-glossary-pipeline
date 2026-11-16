# Executed in the author's build script namespace.
for section in ['glossary_authored_40_59.py','glossary_authored_60_79.py','glossary_authored_80_99.py']:
    exec(compile((P/section).read_text(), str(P/section), 'exec'))
exec(compile((P/'glossary_deeper_reasoning.py').read_text(),str(P/'glossary_deeper_reasoning.py'),'exec'))
inputs=['coverage_briefs.json','extracted_concepts.json','depth_classification.json']
loaded={n:json.loads((P/n).read_text()) for n in inputs}
briefs=loaded['coverage_briefs.json']['briefs']
concepts=loaded['extracted_concepts.json']['concepts']
classifications=loaded['depth_classification.json']['classifications']
B={(x['concept_id'],x['path_id']):x for x in briefs}
C={(x['concept_id'],x['path_id']):x for x in classifications}
paths={x['path_id']:x for x in loaded['extracted_concepts.json']['paths']}
assert len(D)==len(concepts)==100
# Narrow citations for contrast blocks; the definition/mechanism blocks are exhaustive.
contrast_ids={
0:['f3'],1:['f1','f2','f5'],2:['f1','f2'],3:['f1','f2'],4:['f4'],5:['f2','f3'],6:['f3','f5'],7:['f1','f2'],8:['f3','f4'],9:['f1'],10:['f1','f3'],11:['f1','f2'],12:['f1','f4'],13:['f1','f2'],14:['f2'],15:['f3'],16:['f2'],17:['f2','f5'],18:['f3'],19:['f1','f2'],20:['f1'],21:['f1'],22:['f1'],23:['f3'],24:['f2','f3'],25:['f2','f3'],26:['f4'],27:['f1','f3'],28:['f3'],29:['f2','f3'],30:['f1','f2'],31:['f4'],32:['f2'],33:['f1','f2'],34:['f2','f3'],35:['f3'],36:['f2'],37:['f1','f3'],38:['f2','f3'],39:['f3'],40:['f3'],41:['f3'],42:['f3','f4'],43:['f2','f3','f4'],44:['f3','f4'],45:['f1','f3'],46:['f2','f3'],47:['f1','f2'],48:['f3'],49:['f2','f3'],50:['f2'],51:['f1'],52:['f1','f2','f3'],53:['f1','f2','f4'],54:['f3','f4'],55:['f3'],56:['f1','f2'],57:['f1','f3'],58:['f5'],59:['f1','f3'],60:['f1','f2','f3'],61:['f2','f3'],62:['f3'],63:['f1','f2'],64:['f1','f4'],65:['f3','f5'],66:['f1'],67:['f1','f2','f3'],68:['f1','f2','f3'],69:['f3','f4'],70:['f1','f2'],71:['f2'],72:['f3'],73:['f1','f2','f3'],74:['f2','f3'],75:['f4'],76:['f2','f3','f4'],77:['f2','f3','f4'],78:['f2','f4'],79:['f1','f2'],80:['f3','f4'],81:['f1','f2','f3'],82:['f4'],83:['f2'],84:['f1','f3','f4'],85:['f1','f3','f4'],86:['f1','f2'],87:['f2','f4'],88:['f1'],89:['f1'],90:['f4'],91:['f1','f4','f5'],92:['f1','f3'],93:['f1','f2'],94:['f1','f2','f4'],95:['f1','f4'],96:['f1','f2'],97:['f1','f3','f4','f5'],98:['f3','f4'],99:['f1','f2','f3','f4','f5']}
visual_reasons={
'data_table_demo':'A small comparison table makes the contrasting cases clear; a moving demonstration would mostly repeat the text.',
'annotated_code':'Annotated declarations and their resulting behavior make the input, ownership or contract boundary easier to follow.',
'whiteboard_drawing':'A drawn trace makes the distinct boundaries and direction of effects explicit rather than collapsing them into one step.',
'screen_demo':'A tool demonstration can show the configured boundary and the evidence used to verify it.',
'live_code':'Running controlled success and failure cases makes the observable application boundary and assertions concrete.'}
entries=[]
for i,c in enumerate(concepts):
    key=(c['concept_id'],c['path_id']); brief=B[key]; tier=C[key]['depth_tier']; path=paths[c['path_id']]
    assert path['path_title']=='Python/FastAPI Backend Developer'
    assert 'no prior programming experience' in path['learner_scope']
    facts=brief['evidence']['required_facts']; ids=[f['id'] for f in facts]
    intro,example,misconception,choice=D[i]
    level,mode=choice.split(':')
    blocks=[]
    def block(purpose,title,content,fids):
        blocks.append({'id':f'tb{len(blocks)+1}','purpose':purpose,'title':title,'content':content,'fact_ids':fids})
    block('intro','The situation',intro,[])
    # Facts remain exact, including hedges, defaults and important conditional scope.
    block('definition','The rule and its boundary',facts[0]['statement'],[ids[0]])
    if len(facts)>1:
        block('mechanism','How to use the rule',' '.join(f['statement'] for f in facts[1:]),ids[1:])
    if i in S:
        insight_ids={1:['f1','f2','f3','f4','f5'],3:['f1','f2'],4:['f1','f2','f3','f4'],5:['f1','f2','f3','f4'],6:['f2','f3','f4','f5'],8:['f1','f3','f4'],9:['f1','f2','f3','f4','f5'],11:['f1','f2','f3'],13:['f1','f2','f3','f4','f5'],14:['f1','f2','f3','f4'],18:['f1','f2','f3','f4'],20:['f1','f2','f3','f4'],23:['f1','f2','f3'],24:['f1','f2','f3'],25:['f1','f2','f3'],27:['f1','f2','f3','f4'],30:['f1','f2','f3','f4'],31:['f1','f2','f3','f4'],32:['f1','f2','f3'],39:['f1','f2','f3'],46:['f1','f2','f3','f4'],47:['f1','f2','f3'],48:['f1','f2','f3'],51:['f1','f2','f3','f4'],54:['f1','f2','f3','f4'],59:['f1','f2','f3'],61:['f1','f2','f3','f4'],62:['f1','f2','f3'],79:['f1','f2','f3','f4']}
        block('mental_model','Why the distinction matters',S[i],[f for f in insight_ids[i] if f in ids])
    block('walkthrough' if tier=='core' else 'example','Reason through an example',example,ids)
    block('misconception','Keep this distinction',misconception,contrast_ids[i])
    first=c['central_mental_model']
    if i==94:
        first='An authenticated delivery timestamp bounds delivery freshness, not the original event age'
    entries.append({'concept_id':c['concept_id'],'path_id':c['path_id'], 'teaching_blocks':blocks,
        'video_need':{'level':level,'reason':visual_reasons[mode]+' Focus: '+brief['learning_objective'],'preferred_visual_modes':[mode]},
        'teaching_notes':['Establish this first: '+first+'.',
            'Stay within the current objective: '+c['primary_objective']+'. Avoid extending the example into blocked later concepts.',
            'Use the worked case to support this target: '+c['assessment_target']+'.']})
now=datetime.now(timezone.utc)
metadata={'artifact_type':'glossary_pass_a','artifact_version':'1.0.0','schema_version':'1.0.0',
'batch_id':loaded['coverage_briefs.json']['batch_id'],'run_id':loaded['coverage_briefs.json']['batch_id']+'__05_glossary_pass_a__'+now.strftime('%Y%m%dT%H%M%SZ'),
'prompt_version':'05_glossary_pass_a@v1','model':'none','generated_at':now.isoformat(),'source_snapshot_id':loaded['coverage_briefs.json']['metadata']['source_snapshot_id'],
'parent_artifact_hashes':{str(P/n):hashlib.sha256((P/n).read_bytes()).hexdigest() for n in inputs}}
out={'metadata':metadata,'batch_id':metadata['batch_id'],'entries':entries}
artifact=P/'glossary_pass_a.part.all.json'
artifact.write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
# Deterministic self-check: coverage, order, citations, IDs, provenance and media gate.
assert [(e['concept_id'],e['path_id']) for e in entries]==[(c['concept_id'],c['path_id']) for c in concepts]
assert len(set((e['concept_id'],e['path_id']) for e in entries))==100
for e in entries:
    key=(e['concept_id'],e['path_id']); valid={f['id'] for f in B[key]['evidence']['required_facts']}
    taught=set()
    assert [b['id'] for b in e['teaching_blocks']]==[f'tb{j+1}' for j in range(len(e['teaching_blocks']))]
    for b in e['teaching_blocks']:
        assert set(b['fact_ids'])<=valid
        taught.update(b['fact_ids'])
        assert not any(word in b['content'].lower() for word in ['the video','the clip','watch this'])
        assert '```' not in b['content'] # Declaration notation only, no runnable snippets.
    assert valid<=taught
    if e['video_need']['level']=='NONE': assert not e['video_need']['preferred_visual_modes']
assert set(metadata['parent_artifact_hashes'])=={str(P/n) for n in inputs}
from collections import Counter
print('entries',len(entries),'blocks',sum(len(e['teaching_blocks']) for e in entries),'tiers',Counter(x['depth_tier'] for x in classifications))
print('video',Counter(e['video_need']['level'] for e in entries))
for tier in ['core','standard']:
    words=[sum(len(b['content'].split()) for b in e['teaching_blocks']) for e in entries if C[(e['concept_id'],e['path_id'])]['depth_tier']==tier]
    print(tier,'words min/mean/max',min(words),round(sum(words)/len(words)),max(words))
