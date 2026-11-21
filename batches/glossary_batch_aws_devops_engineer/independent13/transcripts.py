import json,sys
b=json.load(open('batches/glossary_batch_aws_devops_engineer/glossary_bundles_draft.json'))['bundles']
for i,x in enumerate(b):
 if not(int(sys.argv[1])<=i<int(sys.argv[2])) or not x['media']:continue
 for s in x['media']['segments']:
  d=json.load(open('00_GLOSSARY_PIPELINE_CORE/video_bank/transcripts/'+s['video_id']+'.json'));words=[]
  for z in d['segments']:
   if z['end_seconds']>s['start_seconds'] and z['start_seconds']<s['end_seconds']:
    w=z['text'].split();n=max([n for n in range(1,min(len(words),len(w))+1) if words[-n:]==w[:n]] or [0]);words+=w[n:]
  print('\n###',i,x['context']['concept_id'],s['start_seconds'],s['end_seconds']);print(' '.join(words));print('MEDIA',json.dumps(x['media'],ensure_ascii=False))
