import json, urllib.request,concurrent.futures
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urljoin
class Parse(HTMLParser):
 def __init__(self):super().__init__();self.text=[];self.links=[];self.skip=0;self.a=None
 def handle_starttag(self,t,attrs):
  if t in ['script','style']: self.skip+=1
  if t=='a':self.a=[dict(attrs).get('href',''),'']
  if t in ['h1','h2','h3','h4','p','li','div','br']:self.text.append('\n')
 def handle_endtag(self,t):
  if t in ['script','style']:self.skip=max(0,self.skip-1)
  if t=='a' and self.a:self.links.append({'text':self.a[1].strip(),'url':self.a[0]});self.a=None
 def handle_data(self,d):
  if not self.skip:self.text.append(d)
  if self.a:self.a[1]+=d
p=Path('batches/glossary_batch_product_manager/working/coverage_sources')
def fetch(s):
 try:
  u=s['url_or_citation'];req=urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'})
  h=urllib.request.urlopen(req,timeout=40).read().decode('utf8','replace'); soup=Parse();soup.feed(h)
  links=[{'text':a['text'],'url':urljoin(u,a['url'])} for a in soup.links]
  (p/(s['source_id']+'.txt')).write_text('\n'.join(x.strip() for x in ''.join(soup.text).splitlines() if x.strip()));(p/(s['source_id']+'.links.json')).write_text(json.dumps(links,indent=2));print(s['source_id'],len(h))
 except Exception as e:print(s['source_id'],e)
with concurrent.futures.ThreadPoolExecutor(max_workers=9) as e:list(e.map(fetch,json.load(open('batches/glossary_batch_product_manager/product_manager.source_pack.json'))['sources']))
