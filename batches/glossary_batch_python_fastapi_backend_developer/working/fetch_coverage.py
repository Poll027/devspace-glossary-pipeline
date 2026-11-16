import json,subprocess,concurrent.futures,re
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urljoin
B=Path('batches/glossary_batch_python_fastapi_backend_developer/working/coverage_sources')
class Parse(HTMLParser):
 def __init__(self): super().__init__(); self.text=[];self.links=[];self.skip=0
 def handle_starttag(self,t,a):
  a=dict(a)
  if t in ('script','style'): self.skip+=1
  if t=='a' and 'href' in a:self.links.append(a['href'])
  if t in ('p','h1','h2','h3','h4','li','pre','section','div','br'): self.text.append('\n')
 def handle_endtag(self,t):
  if t in ('script','style'): self.skip=max(0,self.skip-1)
 def handle_data(self,d):
  if not self.skip:self.text.append(d)
def fetch(item):
 name,url=item
 out=B/(name+'.html')
 subprocess.run(['curl','-sL','--max-time','45',url,'-o',str(out)],check=True)
 raw=out.read_text(errors='replace');p=Parse();p.feed(raw)
 text=re.sub(r'\n\s*\n+','\n', ''.join(p.text)) if '<html' in raw[:1000].lower() or '<!doctype' in raw[:100].lower() else raw
 (B/(name+'.txt')).write_text(text)
 links=sorted(set(urljoin(url,l) for l in p.links if l and not l.startswith(('#','javascript:'))))
 (B/(name+'.links.json')).write_text(json.dumps(links,indent=2))
 return name,len(raw)
if __name__=='__main__':
 import sys
 if len(sys.argv)>1: items=json.load(open(sys.argv[1])).items()
 else: items=[(s['source_id'],s['url_or_citation']) for s in json.load(open('00_GLOSSARY_PIPELINE_CORE/source_packs/python_fastapi_backend_developer.source_pack.json'))['sources']]
 with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:
  for r in pool.map(fetch,items): print(r)
