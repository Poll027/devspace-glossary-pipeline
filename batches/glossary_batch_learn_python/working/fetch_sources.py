from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import urllib.request,re
from html import unescape
root=Path('batches/glossary_batch_learn_python/working/sources');root.mkdir(exist_ok=True)
pages={}
for section, names in {'tutorial':['introduction','controlflow','datastructures','inputoutput','errors','modules','classes','interpreter','floatingpoint','venv','stdlib','stdlib2'], 'library':['functions','stdtypes','csv','math','collections','pathlib','exceptions','pdb','json','datetime','logging','argparse','sys','os','random','secrets','re','venv','unittest','itertools','subprocess','ast','dis','codeop'], 'reference':['simple_stmts','compound_stmts','executionmodel','lexical_analysis','expressions','datamodel']}.items():
 for name in names: pages[section+'_'+name]='https://docs.python.org/3/'+section+'/'+name+'.html'
pages['pep8']='https://peps.python.org/pep-0008/'
pages['packaging']='https://packaging.python.org/en/latest/tutorials/installing-packages/'
def fetch(kv):
 name,url=kv
 try:
  data=urllib.request.urlopen(url,timeout=40).read().decode();(root/(name+'.html')).write_text(data)
  data=re.sub(r'<(script|style).*?</\1>','',data,flags=re.S)
  data=re.sub(r'<[^>]+>',' ',data);data=unescape(data);data=re.sub(r'[ \t]+',' ',data);data=re.sub(r'\n\s*\n','\n',data)
  (root/(name+'.txt')).write_text(data);return name,len(data)
 except Exception as e:return name,str(e)
with ThreadPoolExecutor(max_workers=10) as pool:
 for r in pool.map(fetch,pages.items()):print(*r)
