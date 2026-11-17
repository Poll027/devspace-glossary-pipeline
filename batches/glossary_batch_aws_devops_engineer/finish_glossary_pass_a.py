# Loaded by build_glossary_pass_a.py after its authored rows.
exec((P/'glossary_authored_64_95.py').read_text())
exec((P/'glossary_authored_96_127.py').read_text())
exec((P/'glossary_core_extensions.py').read_text())
assert set(rows)==set(range(128))
vr={}
for line in (P/'glossary_video_rationales.txt').read_text().splitlines():
    i,mode,reason=line.split('|',2)
    vr[int(i)]=(mode,reason)
assert set(vr)==set(rows)
briefmap={(x['concept_id'],x['path_id']):x for x in briefs}
# Rephrase the non-runnable Python scaffolding as prose rather than presenting it as executable syntax.
rewrites={(93,'f2'): 'Use a try block for the supplied failing task and a finally block for the supplied scoped cleanup calls.'}
def fact_text(i,f):
    text=rewrites.get((i,f['id']),f['statement'])
    if i==29 and f['id']=='f1':
        lead,code=text.split('\n',1)
        return lead+'\n\n```hcl\n'+code+'\n```'
    if i==110 and f['id']=='f3':
        lead,code=text.split('\n',1)
        code,tail=code.rsplit('\n',1)
        return lead+'\n\n```hcl\n'+code+'\n```\n\n'+tail
    return text
entries=[]
for i,c in enumerate(concepts):
    key=(c['concept_id'],c['path_id']); b=briefmap[key]; r=rows[i]; tier=depths[key]
    required=b['evidence']['required_facts']; extra=b['evidence']['optional_enrichment']; misconceptions=b['evidence']['misconceptions']
    facts=required+extra+misconceptions
    known={f['id'] for f in facts}
    exids=r['exids'].split(',') if r['exids'] else [f['id'] for f in required]
    coids=r['coids'].split(',') if r['coids'] else [required[-1]['id']]
    assert set(exids+coids)<=known,(i,set(exids+coids)-known)
    blocks=[]
    def block(purpose,title,content,ids):
        blocks.append(dict(id=f'tb{len(blocks)+1}',purpose=purpose,title=title,content=content,fact_ids=ids))
    if tier=='reference':
        block('definition','The operational distinction','\n\n'.join(fact_text(i,f) for f in required),[f['id'] for f in required])
        short={
            10:'If deployment frequency improves while more deployments need intervention, throughput and instability are giving different signals. Compare the measures over time in the same application context, not as a ranking of individuals.',
            42:'Use the supplied records to choose one measured delivery bottleneck. Define the success signal, apply one approved bounded improvement and compare that signal with its baseline. Completing the change is not proof that it helped.',
            97:'For the supplied finding, send its ID, affected resource, observed activity and urgency to the established owner. Preserve the evidence link and describe only what it supports, rather than declaring compromise without evidence.'}
        block('example','Apply it to the supplied evidence',short[i],exids)
    else:
        block('intro','The situation',r['intro'],[])
        block('definition','The operating model',fact_text(i,required[0]),[required[0]['id']])
        if len(required)>1:
            block('mechanism','How the check works','\n\n'.join(fact_text(i,f) for f in required[1:]),[f['id'] for f in required[1:]])
        block('example','Work through one sandbox case',r['example'],exids)
        block('misconception','Do not confuse the evidence',r['contrast'],coids)
    if extra or misconceptions:
        block('misconception','A boundary that changes the interpretation','\n\n'.join(fact_text(i,f) for f in extra+misconceptions),[f['id'] for f in extra+misconceptions])
    notes=[r['note']] if r['note'] else []
    level=r['level']
    medium_overrides={25,31,55,57,62,72,85,87,98,100,105,106,116,118,123,127}
    if i in medium_overrides: level='MEDIUM'
    mode,reason=vr[i]
    entries.append(dict(concept_id=c['concept_id'],path_id=c['path_id'],teaching_blocks=blocks,video_need=dict(level=level,reason=reason,preferred_visual_modes=[] if level=='NONE' else [mode]),teaching_notes=notes))
now=datetime.now(timezone.utc).isoformat()
metadata=dict(artifact_type='glossary_pass_a',artifact_version='1.0.0',schema_version='1.0.0',batch_id='glossary_batch_aws_devops_engineer',run_id='glossary_batch_aws_devops_engineer',prompt_version='05_glossary_pass_a@v1',model='none',generated_at=now,source_snapshot_id=extracted['metadata']['source_snapshot_id'],parent_artifact_hashes={f:hashlib.sha256((P/f).read_bytes()).hexdigest() for f in inputs})
artifact=dict(metadata=metadata,batch_id=metadata['batch_id'],entries=entries)
out=P/'glossary_pass_a.part.all.json'
out.write_text(json.dumps(artifact,ensure_ascii=False,indent=2)+'\n')
# Cheap mechanical/cross-reference and mistakes-checklist checks before submission.
assert len(entries)==len(concepts)==len(briefs)==len(depths)==128
assert len({(e['concept_id'],e['path_id']) for e in entries})==128
assert {(e['concept_id'],e['path_id']) for e in entries}==set(briefmap)==set(depths)
covered=0
for e in entries:
    b=briefmap[(e['concept_id'],e['path_id'])]
    known={f['id'] for typ in ['required_facts','optional_enrichment','misconceptions'] for f in b['evidence'][typ]}
    taught={f for block in e['teaching_blocks'] for f in block['fact_ids']}
    assert taught<=known
    assert {f['id'] for f in b['evidence']['required_facts']}<=taught
    covered+=len(b['evidence']['required_facts'])
    assert [x['id'] for x in e['teaching_blocks']]==[f'tb{i+1}' for i in range(len(e['teaching_blocks']))]
    text='\n'.join(x['content'] for x in e['teaching_blocks'])
    assert not re.search(r'\b(video|clip|watch)\b',text,re.I)
    assert not re.search(r'https?://',text)
    assert text.count('```')%2==0
    assert not (e['video_need']['level']=='NONE' and e['video_need']['preferred_visual_modes'])
# Every required source statement is preserved except the explicit non-runnable scaffolding rewrite.
for i,e in enumerate(entries):
    text='\n'.join(x['content'] for x in e['teaching_blocks'])
    for f in briefs[i]['evidence']['required_facts']:
        assert fact_text(i,f) in text,(i,f['id'])
# Trace hypothetical examples that rely on arithmetic or data flow.
import ipaddress
vpc=ipaddress.ip_network('10.20.0.0/16'); a=ipaddress.ip_network('10.20.1.0/24'); b=ipaddress.ip_network('10.20.2.0/24')
assert a.subnet_of(vpc) and b.subnet_of(vpc) and not a.overlaps(b)
assert a.num_addresses-5==251 and a.overlaps(ipaddress.ip_network('10.20.1.128/25'))
assert ipaddress.ip_address('10.20.2.10') in vpc and ipaddress.ip_address('198.51.100.8') not in vpc
assert [True,False,True].count(True)==2
assert 3-1==2 # total attempt budget includes the initial request
assert 18<=20 and 4<=5 and 10>5 # RTO/RPO rehearsal examples
# Execute the Python dictionary-access syntax on supplied-shaped safe mock error data.
response={'Error':{'Code':'EXAMPLE','Message':'example message'},'ResponseMetadata':{'RequestId':'example-request'}}
assert response['Error']['Code']=='EXAMPLE' and response['Error']['Message']=='example message'
assert response['ResponseMetadata']['RequestId']=='example-request'
# Execute the Config constructor expression with a local test double; no AWS API calls or new learner syntax are introduced.
class Config:
    def __init__(self,**kwargs):self.options=kwargs
APPROVED_ATTEMPTS=3
config=eval('Config(retries={"mode": "standard", "total_max_attempts": APPROVED_ATTEMPTS})')
assert config.options['retries']['total_max_attempts']==3
# Verify the finally behavior with a finite local task and scoped resource identities.
resources={'preexisting','exercise-created'}
try:
    try:raise RuntimeError('controlled test')
    finally:resources.remove('exercise-created')
except RuntimeError:pass
assert resources=={'preexisting'}
# Trace the supplied fields/filter/sort query on a deterministic in-memory fixture.
events=[{'@timestamp':2,'@message':'failure','request_id':'orders-7'},{'@timestamp':1,'@message':'received','request_id':'orders-7'},{'@timestamp':3,'@message':'unrelated','request_id':'orders-8'}]
matched=sorted((x for x in events if x['request_id']=='orders-7'),key=lambda x:x['@timestamp'])
assert [x['@message'] for x in matched]==['received','failure']
summary={'entries':len(entries),'teaching_blocks':sum(len(e['teaching_blocks']) for e in entries),'required_facts_covered':covered,'depths':dict(collections.Counter(depths.values())),'video_need':dict(collections.Counter(e['video_need']['level'] for e in entries)),'generated_at':now}
for tier in ['core','standard','reference']:
    counts=[sum(len(x['content'].split()) for x in e['teaching_blocks']) for e in entries if depths[(e['concept_id'],e['path_id'])]==tier]
    summary[tier+'_word_counts']={'min':min(counts),'max':max(counts),'mean':round(sum(counts)/len(counts))} if counts else None
print(json.dumps(summary,indent=2))
