import json,glob,sys,re
from pathlib import Path
sys.path.insert(0,'batches/glossary_batch_aws_devops_engineer/working')
from brief_data import DATA
import brief_data_more,brief_fixes
from fetch_refs import url
cache={d['url']:d for f in glob.glob('batches/glossary_batch_aws_devops_engineer/working/coverage_sources/*_*.json') if not f.endswith('.toc.json') for d in [json.load(open(f))]}
stop=set('the a an and or to of for in with from by is are that this as be supplied approved intended inspect verify use configuration'.split())
for i in [int(x) for x in sys.argv[1:]]:
 print('\nTILE',i)
 for fact,ref in DATA[i]:
  if ref.startswith('terraform_aws_provider#website'):
   text=Path('batches/glossary_batch_aws_devops_engineer/working/coverage_sources/terraform_instance.md').read_text()
  else:
   u=url(ref)[1];text=cache.get(u,{}).get('text','')
  if len(text)<100: print('BAD',ref);continue
  sentences=[s for s in re.split(r'(?<=[.!?])\s+|\n',text) if len(s)>35]
  words=set(re.findall(r'[a-zA-Z][a-zA-Z_]{2,}',fact.lower()))-stop
  ranked=sorted(sentences,key=lambda s:len(words & set(re.findall(r'[a-zA-Z][a-zA-Z_]{2,}',s.lower()))),reverse=True)
  print('FACT',fact);print('REF',ref,'EVID', ' / '.join(ranked[:2])[:650])
