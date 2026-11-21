import json,sys
p='batches/glossary_batch_aws_devops_engineer/'
b=json.load(open(p+'glossary_bundles_draft.json'))['bundles'];e=json.load(open(p+'extracted_concepts.json'))['concepts'];c=json.load(open(p+'coverage_briefs.json'))['briefs']
for i in range(int(sys.argv[1]),int(sys.argv[2])):
 x=b[i];r=e[i];print('\n###',i,r['concept_id']);print('INLINE',[(z['term'],z['definition']) for z in r['inline_vocabulary']]);print('PREVIEW',r['forward_preview_ids']);print('FACTS',[(z['id'],z['statement'],z['source_refs']) for z in c[i]['evidence']['required_facts']]);
 for t in x['teaching_blocks']:
  if t['content'] not in [z['statement'] for z in c[i]['evidence']['required_facts']]:print(t['id'],t['content'])
 for k in ['assessment_anchors','practice_anchor','visual_anchor','teaching_notes']:print(k,json.dumps(x[k],ensure_ascii=False))
 if x['media']:print('MEDIA',json.dumps(x['media'],ensure_ascii=False))
 assert set(r['blocked_knowledge_ids'])==set(x['context']['blocked_future_concepts'])
 assert set(r['allowed_knowledge_ids'])==set(z['concept_id'] for z in e[:i])
