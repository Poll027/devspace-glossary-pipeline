import concurrent.futures,urllib.request,json,re
from html.parser import HTMLParser
from pathlib import Path
P=Path('batches/glossary_batch_learn_python/working/coverage_sources');P.mkdir(exist_ok=True)
pages=['tutorial/introduction','tutorial/controlflow','tutorial/datastructures','tutorial/modules','tutorial/inputoutput','tutorial/errors','tutorial/classes','tutorial/stdlib','tutorial/stdlib2','tutorial/floatingpoint','tutorial/interpreter','reference/lexical_analysis','reference/executionmodel','reference/expressions','reference/simple_stmts','reference/compound_stmts','reference/datamodel','library/functions','library/stdtypes','library/exceptions','library/math','library/collections','library/pathlib','library/pdb','library/json','library/csv','library/datetime','library/logging','library/argparse','library/os','library/random','library/secrets','library/re','library/sys','library/venv','library/itertools','library/unittest']
class Parser(HTMLParser):
 def __init__(self):super().__init__();self.out=[];self.skip=0
 def handle_starttag(self,t,a):
  a=dict(a)
  if t in ['script','style']:self.skip+=1
  if 'id' in a:self.out.append('\n#'+a['id']+'\n')
  if t in ['p','li','pre','h1','h2','h3','dt','dd','tr']:self.out.append('\n')
 def handle_endtag(self,t):
  if t in ['script','style']:self.skip-=1
  if t in ['p','li','pre','h1','h2','h3','dt','dd','tr']:self.out.append('\n')
 def handle_data(self,d):
  if not self.skip:self.out.append(d)
def fetch(page):
 url='https://docs.python.org/3/'+page+'.html';html=urllib.request.urlopen(url,timeout=45).read().decode();p=Parser();p.feed(html);text=re.sub(r'\n[ \t]*\n+', '\n\n',''.join(p.out));(P/(page.replace('/','_')+'.txt')).write_text(text);return page,len(text)
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:
 for r in ex.map(fetch,pages):print(*r)
for name,url in [('packaging','https://packaging.python.org/en/latest/tutorials/installing-packages/'),('thinkpython','https://allendowney.github.io/ThinkPython/chap21.html')]:
 html=urllib.request.urlopen(url,timeout=45).read().decode();p=Parser();p.feed(html);(P/(name+'.txt')).write_text(''.join(p.out));print(name)
