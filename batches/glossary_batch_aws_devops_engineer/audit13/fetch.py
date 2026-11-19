import json,urllib.parse,concurrent.futures,subprocess,os,re
from html.parser import HTMLParser
p='batches/glossary_batch_aws_devops_engineer/';b=json.load(open(p+'glossary_bundles_draft.json'))['bundles'];pack={x['source_id']:x for x in json.load(open('00_GLOSSARY_PIPELINE_CORE/source_packs/aws_devops_engineer.source_pack.json'))['sources']}
refs={(r if isinstance(r,str) else r['source_ref']) for x in b for f in x['coverage']['required_facts'] for r in f['source_refs']}
def url(ref):
 id,_,loc=ref.partition('#');base=pack[id]['url_or_citation']
 if loc and (re.search(r'\.(html|md|pdf)',loc) or not base.startswith('https://docs.aws')):return urllib.parse.urljoin(base if base.endswith('/') or re.search(r'\.(html|pdf)$',base) else base+'/',loc).split('#')[0]
 return base.split('#')[0]
urls=sorted({url(r) for r in refs});json.dump({r:url(r) for r in refs},open(p+'audit13/refurls.json','w'))
class Parser(HTMLParser):
 def __init__(self):super().__init__();self.out=[];self.skip=0
 def handle_starttag(self,t,a):
  if t in ['script','style','nav']:self.skip+=1
  if t in ['p','li','h1','h2','h3','div','pre','tr']:self.out.append('\n')
 def handle_endtag(self,t):
  if t in ['script','style','nav']:self.skip=max(0,self.skip-1)
 def handle_data(self,s):
  if not self.skip:self.out.append(re.sub(r"\s+", " ", s))
def get(z):
 i,u=z;raw=subprocess.run(['curl','-sL','--max-time','25',u],capture_output=True).stdout
 if '.pdf' in u:
  open(p+f'audit13/source{i}.pdf','wb').write(raw);raw=subprocess.run(['pdftotext',p+f'audit13/source{i}.pdf','-'],capture_output=True).stdout;txt=raw.decode(errors='replace')
 else:
  a=Parser();a.feed(raw.decode(errors='replace'));txt='\n'.join(re.sub(r'\s+',' ',l).strip() for l in ''.join(a.out).splitlines() if l.strip())
 open(p+f'audit13/source{i}.txt','w').write(txt);return(u,i,len(txt))
with concurrent.futures.ThreadPoolExecutor(max_workers=16) as ex:results=list(ex.map(get,enumerate(urls)))
json.dump(results,open(p+'audit13/fetched.json','w'));print('fetched',len(results),'chars',sum(x[2] for x in results));print('empty',[x for x in results if x[2]<200])
