import json,concurrent.futures,urllib.request,urllib.parse,hashlib
from pathlib import Path
from html.parser import HTMLParser
root=Path('batches/glossary_batch_aws_devops_engineer/working/coverage_sources')
class Parse(HTMLParser):
 def __init__(self): super().__init__(); self.text=[];self.links=[];self.skip=0
 def handle_starttag(self,t,a):
  if t in ('script','style'):self.skip+=1
  if t=='a':
   d=dict(a)
   if 'href' in d:self.links.append(d['href'])
 def handle_endtag(self,t):
  if t in ('script','style'):self.skip=max(0,self.skip-1)
 def handle_data(self,d):
  if not self.skip and d.strip():self.text.append(d.strip())
def fetch(x):
 sid,url=x; key=sid+'_'+hashlib.sha256(url.encode()).hexdigest()[:12]; target=root/(key+'.json')
 if target.exists():return
 try:
  data=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=35).read().decode('utf-8'); p=Parse();p.feed(data)
  target.write_text(json.dumps({'source_id':sid,'url':url,'text':'\n'.join(p.text),'links':list(dict.fromkeys(urllib.parse.urljoin(url,l) for l in p.links))},ensure_ascii=False));print(sid,len(data),url)
 except Exception as e: print('FAIL',url,str(e))
if __name__=='__main__':
 import sys
 jobs=json.load(open(sys.argv[1])) if len(sys.argv)>1 else [(s['source_id'],s['url_or_citation']) for s in json.load(open('00_GLOSSARY_PIPELINE_CORE/source_packs/aws_devops_engineer.source_pack.json'))['sources']]
 with concurrent.futures.ThreadPoolExecutor(max_workers=12) as ex:list(ex.map(fetch,jobs))
