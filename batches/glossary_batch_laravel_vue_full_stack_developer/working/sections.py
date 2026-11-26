import sys,re
from pathlib import Path
D=Path('batches/glossary_batch_laravel_vue_full_stack_developer/working/coverage_sources')
for arg in sys.argv[1:]:
 k,_,s=arg.partition(':');t=(D/(k+'.txt')).read_text();m=re.search(r'^SECTION '+re.escape(s)+r'(?: |$)',t,re.M)
 if m:
  start=m.start();end=t.find('\nSECTION ',m.end());z=t[start:end if end!=-1 else len(t)];print('\n'+k+':'+s+'\n'+z[:2600])
 else:print('\nMISSING',arg)
