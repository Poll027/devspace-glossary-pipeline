import json,urllib.request,urllib.parse,concurrent.futures,re,pathlib
from html.parser import HTMLParser
P=pathlib.Path('batches/glossary_batch_machine_learning_engineer/working/coverage_sources')
class Parse(HTMLParser):
 def __init__(self):super().__init__();self.text=[];self.links=[];self.skip=0
 def handle_starttag(self,t,a):
  if t in ['script','style']:self.skip+=1
  if t=='a':
   h=dict(a).get('href');
   if h:self.links.append(h)
  if t in ['h1','h2','h3','h4','p','div','li','pre','tr']:self.text.append('\n')
 def handle_endtag(self,t):
  if t in ['script','style']:self.skip=max(0,self.skip-1)
 def handle_data(self,d):
  if not self.skip:self.text.append(d)
def fetch(item):
 sid,url=item
 name=re.sub('[^a-zA-Z0-9._-]','_',sid)
 try:
  html=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=45).read().decode(errors='replace');p=Parse();p.feed(html)
  text=re.sub(r'\n\s*\n+','\n',''.join(p.text));(P/(name+'.txt')).write_text(text);(P/(name+'.links.json')).write_text(json.dumps([urllib.parse.urljoin(url,h) for h in p.links]));return sid,url,len(text)
 except Exception as e:return sid,url,str(e)
if __name__=='__main__':
 import sys
 items=json.load(open(sys.argv[1]))
 with concurrent.futures.ThreadPoolExecutor(max_workers=12) as ex:
  for r in ex.map(fetch,items):print(*r)
