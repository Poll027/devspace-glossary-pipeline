import json,glob,urllib.parse,sys
from pathlib import Path
sys.path.insert(0,'batches/glossary_batch_aws_devops_engineer/working')
from brief_data import DATA
p=Path('batches/glossary_batch_aws_devops_engineer/working')
ss={s['source_id']:s['url_or_citation'] for s in json.load(open('00_GLOSSARY_PIPELINE_CORE/source_packs/aws_devops_engineer.source_pack.json'))['sources']}
index=json.load(open(p/'source_index.json')); available={}
for sid,title,h in index: available.setdefault(sid,set()).add(urllib.parse.urljoin(ss[sid],h).split('#')[0])
for f in glob.glob(str(p/'coverage_sources/*.json')):
 if f.endswith('.toc.json'):continue
 d=json.load(open(f));available.setdefault(d['source_id'],set()).update(l.split('#')[0] for l in d['links'])
jobs=[]
for i,fs in DATA.items():
 for fact,ref in fs:
  sid,loc=ref.split('#',1); u=urllib.parse.urljoin(ss[sid],loc).split('#')[0]
  if u not in available.get(sid,set()):print('UNDISCOVERED',i,ref)
  else:jobs.append((sid,u))
json.dump(list(set(jobs)),open(p/'fetch_jobs.json','w'))
