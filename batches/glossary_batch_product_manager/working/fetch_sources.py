import urllib.request, json, re, concurrent.futures
from pathlib import Path
from html.parser import HTMLParser
B=Path('batches/glossary_batch_product_manager'); D=B/'working'/'sources'; D.mkdir(exist_ok=True)
class Parser(HTMLParser):
 def __init__(self): super().__init__();self.parts=[];self.links=[];self.skip=0
 def handle_starttag(self,t,a):
  if t in ('script','style'):self.skip+=1
  if t in ('h1','h2','h3','h4','p','li','div','br','tr'):self.parts.append('\n')
  if t=='a':
   u=dict(a).get('href');
   if u:self.links.append(u)
 def handle_endtag(self,t):
  if t in ('script','style'):self.skip=max(0,self.skip-1)
 def handle_data(self,d):
  if not self.skip:self.parts.append(d)
def fetch(pair):
 key,url=pair
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
  with urllib.request.urlopen(req,timeout=45) as r:html=r.read().decode('utf8','replace');final=r.url
  p=Parser();p.feed(html);text=re.sub(r'\n\s*\n+', '\n', ''.join(p.parts));text=re.sub(r'[ \t]+',' ',text)
  (D/(key+'.txt')).write_text(text);(D/(key+'.links.json')).write_text(json.dumps({'url':final,'links':list(dict.fromkeys(p.links))},indent=2));print(key,len(text),final)
 except Exception as e:print('ERROR',key,url,str(e))
if __name__=='__main__':
 import sys
 if len(sys.argv)>1:items=json.load(open(sys.argv[1])).items()
 else:items=[(s['source_id'],s['url_or_citation']) for s in json.load(open(B/'product_manager.source_pack.json'))['sources']]
 with concurrent.futures.ThreadPoolExecutor(max_workers=12) as ex:list(ex.map(fetch,items))
