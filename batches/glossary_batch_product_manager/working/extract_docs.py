import json,re
from pathlib import Path
p=Path('batches/glossary_batch_product_manager/working/coverage_sources')
t=(p/'amplitude_experiment_index.txt').read_text();docs={}
for part in t.split('='*80):
 m=re.search(r'URL: (https://[^\s]+)',part)
 if m:docs[m[1]]=[part.strip()]
 elif docs:docs[list(docs)[-1]].append(part.strip())
idx=json.load(open(p/'fetch_index.json'))
for slug,key in [('holdout-groups-exclude-users','doc_holdouts'),('define-goals','doc_goals'),('identify-the-problem','doc_hypothesis'),('experiment-estimate-duration','doc_duration')]:
 found=[(u,a) for u,a in docs.items() if u.rstrip('/').endswith('/'+slug)]
 if not found:
  print('missing',slug);continue
 u,a=found[0];(p/(key+'.txt')).write_text('\n\n'.join(a));idx.append({'source_id':key,'url_or_citation':u});print(key,u)
(p/'fetch_index.json').write_text(json.dumps(idx,indent=2))
