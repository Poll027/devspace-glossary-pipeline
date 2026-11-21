import json,re,sys
p='batches/glossary_batch_aws_devops_engineer/';b=json.load(open(p+'glossary_bundles_draft.json'))['bundles'];e=json.load(open(p+'extracted_concepts.json'))['concepts'];c=json.load(open(p+'coverage_briefs.json'))['briefs']
for i in range(int(sys.argv[1]),int(sys.argv[2])):
 x=b[i];r=e[i];print('\n###',i,r['concept_id']);print('inline:',', '.join(z['term'] for z in r['inline_vocabulary']));print('facts:', ' | '.join(z['statement'] for z in c[i]['evidence']['required_facts']));
 for t in x['teaching_blocks']:
  if t['purpose'] in ['example','walkthrough','syntax']:print(t['id'],t['content'])
 print('anchors:',json.dumps([x['assessment_anchors'],x['practice_anchor'],x['visual_anchor']],ensure_ascii=False))
