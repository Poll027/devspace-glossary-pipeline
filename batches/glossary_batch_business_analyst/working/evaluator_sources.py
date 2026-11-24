import json,re,pathlib,subprocess,concurrent.futures,html
from html.parser import HTMLParser
p=pathlib.Path('batches/glossary_batch_business_analyst');s=p/'working/sources'; dest=p/'working/evaluator_sources';dest.mkdir(exist_ok=True)
m=json.load(open(p/'working/evaluator_source_map.json'))
alias={'requirements-traceability-matrix':'rtm','requirements':'product-requirements','decision-matrix':'decision-matrix','gap-analysis':'gap-analysis','fishbone-diagram':'fishbone-diagram','stakeholder-communications-plan':'atl_stakeholder-communications-plan','data-modeling':'ibm_models','desktop-upload-desktop-files':'pbi_report-publish','service-datasets-across-workspaces':'pbi_reuse-models','power-bi-visualization-types-for-reports-and-q-and-a':'pbi_visual-types','buildexamples_bar.htm':'tab_line','switch-between-relative-absolute-and-mixed-references':'excel_refs','overview-of-formulas-in-excel':'excel_formulas'}
for n in ['if','ifs','count','sum','average','index','match','vlookup','xlookup']:alias[n+'-function']='excel_'+n
sp={}
for pack in pathlib.Path('00_GLOSSARY_PIPELINE_CORE/source_packs').glob('*.json'):
 for x in json.load(open(pack))['sources']:sp[x['source_id']]=x['url_or_citation']
sp['openintro_statistics_textbook']='https://www.openintro.org/book/os/'
briefs=json.load(open(p/'coverage_briefs.json'))['briefs'];urls=set()
for b in briefs:
 for f in b['evidence']['required_facts']:
  for r in f['source_refs']:
   a=re.search(r'https?://\S+',r);u=(a[0] if a else sp.get(r.split('#')[0],'' )).split('#')[0].rstrip(';');urls.add(u)
for u in urls:
 slug=u.rstrip('/').split('/')[-1]; candidates=[alias.get(slug,''), 'atl_'+slug,'nn_'+slug,'pg_'+slug,'pbi_'+slug,'tab_'+slug.replace('.htm','')]
 if u not in m:
  for c in candidates:
   if c and (s/(c+'.txt')).exists():m[u]=str(s/(c+'.txt'));break
class Parser(HTMLParser):
 def __init__(self):super().__init__();self.t=[];self.skip=0
 def handle_starttag(self,t,a):
  if t in ['script','style']:self.skip+=1
 def handle_endtag(self,t):
  if t in ['script','style']:self.skip=max(0,self.skip-1)
 def handle_data(self,d):
  if not self.skip and d.strip():self.t.append(d.strip())
def fetch(u):
 if not u:return
 if u in m:return
 f=dest/(str(len(u))+'_'+re.sub('[^a-zA-Z0-9]','_',u[-90:])+'.txt')
 try:
  if '/PDF' in u or '.pdf' in u:
   subprocess.run(['curl','-sL','--max-time','35',u,'-o',str(f)+'.pdf']);subprocess.run(['pdftotext',str(f)+'.pdf',str(f)])
  else:
   raw=subprocess.check_output(['curl','-sL','--max-time','35',u]);a=Parser();a.feed(raw.decode('utf8','replace'));f.write_text('\n'.join(a.t))
  if f.exists():m[u]=str(f)
 except Exception as e:print('FETCH ERROR',u,str(e))
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:list(ex.map(fetch,urls))
json.dump(m,open(p/'working/evaluator_source_map.json','w'));print('SOURCES',len(urls),'mapped',len(m),'missing',urls-m.keys())
# Per concept/source: select actual source passages, not artifact statements, using shared distinctive words.
stop=set('the a an of to in and is are for or with by on that be as from each it this can should when which how into than does not use using only one'.split())
for i,b in enumerate(briefs):
 out=[f"SOURCE REVIEW {i} {b['concept_id']}"]
 for f in b['evidence']['required_facts']:
  for r in f['source_refs']:
   a=re.search(r'https?://\S+',r);u=(a[0] if a else sp.get(r.split('#')[0],'' )).split('#')[0].rstrip(';');fn=m.get(u)
   if not fn:out.append('MISSING '+r);continue
   lines=pathlib.Path(fn).read_text().splitlines();words=set(re.findall('[a-z]+',f['statement'].lower()))-stop
   scored=sorted(enumerate(lines),key=lambda z:len(words & set(re.findall('[a-z]+',z[1].lower()))),reverse=True)
   for n,line in scored[:1]:
    if len(line)>25:out.append(f"{f['id']} {u} LINE {n+1}: "+line[:650])
 (p/'working'/f'source_review_{i}.txt').write_text('\n'.join(out))
