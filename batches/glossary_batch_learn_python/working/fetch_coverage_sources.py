import concurrent.futures, urllib.request, pathlib, re
from html.parser import HTMLParser
root=pathlib.Path('batches/glossary_batch_learn_python/working/coverage_sources');root.mkdir(exist_ok=True)
pages=['tutorial/introduction','tutorial/controlflow','tutorial/datastructures','tutorial/inputoutput','tutorial/errors','tutorial/classes','tutorial/modules','tutorial/interpreter','tutorial/stdlib','tutorial/floatingpoint','reference/executionmodel','reference/lexical_analysis','reference/simple_stmts','reference/compound_stmts','reference/expressions','library/stdtypes','library/functions','library/math','library/collections','library/pdb','library/pathlib','library/exceptions','library/json','library/csv','library/datetime','library/logging','library/argparse','library/os','library/random','library/secrets','library/re','library/sys','library/venv','library/itertools','library/unittest','library/subprocess','library/ast','library/traceback','library/importlib','library/dis']
class Text(HTMLParser):
 def __init__(self):super().__init__();self.out=[];self.skip=0
 def handle_starttag(self,t,a):
  if t in ['script','style']:self.skip+=1
  if t in ['section','dt']:
   for k,v in a:
    if k=='id':self.out.append('\nSECTION '+v+'\n')
  if t in ['p','div','li','pre','h1','h2','h3','dt','dd']:self.out.append('\n')
 def handle_endtag(self,t):
  if t in ['script','style']:self.skip-=1
 def handle_data(self,d):
  if not self.skip:self.out.append(d)
def fetch(pair):
 name,url=pair
 try:
  raw=urllib.request.urlopen(url,timeout=35).read().decode();parser=Text();parser.feed(raw);text=''.join(parser.out);text=re.sub(r'\n\s*\n+', '\n\n',text);(root/(name.replace('/','_')+'.txt')).write_text(url+'\n'+text);return name,len(text)
 except Exception as e:return name,str(e)
urls=[(p,'https://docs.python.org/3/'+p+'.html') for p in pages]+[('pep8','https://peps.python.org/pep-0008/'),('packaging','https://packaging.python.org/en/latest/tutorials/installing-packages/'),('think_index','https://allendowney.github.io/ThinkPython/')]
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:
 for r in pool.map(fetch,urls):print(*r)
