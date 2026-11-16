import sys,re
from pathlib import Path
from fetch_coverage import Parse
B=Path('batches/glossary_batch_python_fastapi_backend_developer/working/coverage_sources')
for arg in sys.argv[1:]:
 name,anchor=arg.split(':',1);s=(B/(name+'.html')).read_text(errors='replace')
 m=re.search(r'<(?:h[1-4]|section)[^>]*id="'+re.escape(anchor)+r'"[^>]*>',s)
 if not m:print('NOT FOUND',arg);continue
 start=m.start();nexthead=re.search(r'<h[1-4]\b',s[m.end():])
 # Section with id has heading immediately after start; skip it first.
 if m[0].startswith('<section'):
  first=re.search(r'</h[1-4]>',s[m.end():]);endstart=m.end()+first.end() if first else m.end()
 else:endstart=m.end()
 nxt=re.search(r'<h[1-4]\b',s[endstart:]);end=endstart+nxt.start() if nxt else min(len(s),start+18000)
 p=Parse();p.feed(s[start:end]);text=re.sub(r'\n\s*\n+','\n',''.join(p.text));print('\n###',arg,'\n',text[:4200])
