import json,re,sys,collections,pathlib
p=pathlib.Path('batches/glossary_batch_aws_devops_engineer');q=p/'independent13'
b=json.load(open(p/'glossary_bundles_draft.json'))['bundles'];e=json.load(open(p/'extracted_concepts.json'))['concepts'];c=json.load(open(p/'coverage_briefs.json'))['briefs'];si={o['ref']:o for o in json.load(open(q/'sources.json'))}
tok=lambda s:set(re.findall(r'[a-z][a-z0-9_-]{3,}',s.lower()))
alltext=[' '.join(t['content'] for t in x['teaching_blocks']) for x in b];df=collections.Counter(t for s in alltext for t in tok(s))
for i in range(int(sys.argv[1]),int(sys.argv[2])):
 x=b[i];r=e[i];facts=c[i]['evidence']['required_facts'];ev=' '.join((q/f"s{si[z]['i']}.txt").read_text() for f in facts for z in f['source_refs']);ft=' '.join(f['statement'] for f in facts);known=tok(ev+' '+ft)
 print('\n###',i,r['concept_id']);print('FACTS',' | '.join(f['statement'] for f in facts))
 # Read every block/anchor, retain technical assertions and novel words for human inspection.
 for t in x['teaching_blocks']:
  if t['purpose']=='example':
   sentences=re.split(r'(?<=[.!?])\s+|\n+',t['content'])
   selected=[s for s in sentences if re.search(r'\d|--|\b(?:command|API|JSON|YAML|HCL|policy|allow|deni|permission|encrypt|bucket|role|state|version|target|parameter|retry|retri|lock|secret|image|digest|ARN|status|rule|deploy)',s,re.I)]
   print(t['id'],' '.join(selected))
  elif t['purpose'] not in ['definition','mechanism']:
   print(t['id'],t['content'])
  else:
   extra=tok(t['content'])-tok(ft)
   if extra:print(t['id'],t['content'])
 ta=' '.join(t['content'] for t in x['teaching_blocks']);
 for k in ['assessment_anchors','practice_anchor','visual_anchor','teaching_notes']:
  val=json.dumps(x[k],ensure_ascii=False);extra=sorted(t for t in tok(val)-tok(ta) if df[t]<3 and t not in ['type','purpose','success','objective','capability','fact_ids','field_selection','tool_simulation','data_table','matching','diagram','comparison','annotated_screenshot'])
  if extra:print(k,'NEW',extra)
 print('SCOPE inline',','.join(z['term'] for z in r['inline_vocabulary']),'preview',r['forward_preview_ids'])
 assert set(r['blocked_knowledge_ids'])==set(x['context']['blocked_future_concepts'])
 assert set(r['allowed_knowledge_ids'])==set(z['concept_id'] for z in e[:i])
 assert x['coverage']['required_facts']==facts
