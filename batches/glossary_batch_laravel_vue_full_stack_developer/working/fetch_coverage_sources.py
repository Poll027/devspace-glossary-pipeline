import json,urllib.request,concurrent.futures
from html.parser import HTMLParser
from pathlib import Path
B=Path('batches/glossary_batch_laravel_vue_full_stack_developer'); D=B/'working/coverage_sources'
class Text(HTMLParser):
 def __init__(self): super().__init__(); self.skip=0;self.parts=[];self.links=[]
 def handle_starttag(self,t,a):
  a=dict(a)
  if t in ['script','style']:self.skip+=1
  if t=='a' and 'href' in a:self.links.append(a['href'])
  if t in ['h1','h2','h3','h4']:self.parts.append('\n\nSECTION '+a.get('id','')+' ')
  if t in ['p','pre','li','div','tr','br']:self.parts.append('\n')
 def handle_endtag(self,t):
  if t in ['script','style']:self.skip=max(0,self.skip-1)
 def handle_data(self,d):
  if not self.skip:self.parts.append(d)
urls={}
for p in ['routing','controllers','requests','responses','validation','middleware','lifecycle','artisan','configuration','deployment','logging','scheduling','migrations','seeding','queues','database','eloquent','eloquent-mutators','eloquent-relationships','eloquent-factories','eloquent-resources','pagination','testing','http-tests','database-testing','container','authentication','session','hashing','authorization','sanctum','queries']:
 urls['laravel_'+p]='https://laravel.com/docs/12.x/'+p
for p in ['introduction','essentials/reactivity-fundamentals','essentials/computed','essentials/watchers','essentials/template-syntax','essentials/conditional','essentials/list','essentials/event-handling','essentials/forms','essentials/lifecycle','essentials/component-basics','components/props','components/events','reusability/composables','scaling-up/state-management','scaling-up/testing','best-practices/security']:
 urls['vue_'+p.replace('/','_')]='https://vuejs.org/guide/'+p+'.html'
for i in range(1,11):urls['vue_tutorial_'+str(i)]='https://vuejs.org/tutorial/#step-'+str(i)
for p in ['functions.arguments','functions.returning-values','language.types','language.types.array','language.variables.basics','language.operators.comparison','language.operators.logical','control-structures.if','control-structures.foreach','language.oop5.basic','language.oop5.decon','language.oop5.interfaces','language.exceptions','language.namespaces.definition','language.namespaces.importing']:
 urls['php_'+p]='https://www.php.net/manual/en/'+p+'.php'
for p in ['01-basic-usage.md','04-schema.md','06-config.md']:
 urls['composer_'+p]='https://getcomposer.org/doc/'+p
for p in ['','env-and-mode','build','static-deploy']:
 urls['vite_'+(p or 'guide')]='https://vite.dev/guide/'+(p+'.html' if p else '')
for p in ['','features','environment','mocking','mocking/requests']:
 urls['vitest_'+(p.replace('/','_') or 'guide')]='https://vitest.dev/guide/'+(p+'.html' if p else '')
for p in ['introduction.html','core-concepts/state.html','core-concepts/actions.html']:
 urls['pinia_'+p.replace('/','_')]='https://pinia.vuejs.org/'+p
for p in ['essentials','essentials/dynamic-matching','essentials/html5-mode','advanced/navigation-guards']:
 urls['router_'+p.replace('/','_')]='https://router.vuejs.org/guide/'+p+'.html'
def get(k,u):
 try:
  raw=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=50).read().decode(); x=Text();x.feed(raw)
  (D/(k+'.txt')).write_text('\n'.join(l.strip() for l in ''.join(x.parts).splitlines() if l.strip()))
  (D/(k+'.links.json')).write_text(json.dumps(x.links));return k,len(raw)
 except Exception as e:return k,str(e)
with concurrent.futures.ThreadPoolExecutor(max_workers=12) as ex:
 for r in ex.map(lambda kv:get(*kv),urls.items()):print(*r)
(D/'urls.json').write_text(json.dumps(urls,indent=2))
