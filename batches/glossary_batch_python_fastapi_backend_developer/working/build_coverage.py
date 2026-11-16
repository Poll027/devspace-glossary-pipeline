import json,re,hashlib,datetime,uuid
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse
B=Path('batches/glossary_batch_python_fastapi_backend_developer');W=B/'working';S=W/'coverage_sources'
pack=Path('00_GLOSSARY_PIPELINE_CORE/source_packs/python_fastapi_backend_developer.source_pack.json')
sources=json.load(open(pack))['sources']; source_ids={x['source_id'] for x in sources}
urls={x['source_id']:x['url_or_citation'] for x in sources}
for p in W.glob('coverage_fetch*.json'):urls.update(json.load(open(p)))
urls['docker_build']='https://docs.docker.com/reference/dockerfile/'
class Ids(HTMLParser):
 def __init__(self):super().__init__();self.ids=[]
 def handle_starttag(self,t,a):
  a=dict(a)
  if a.get('id'):self.ids.append(a['id'])
ids={}
for p in S.glob('*.html'):
 x=Ids();x.feed(p.read_text(errors='replace'));ids[p.stem]=x.ids

def parse(p):
 out={};current=None
 for l in p.read_text().splitlines():
  if not l.strip():continue
  if l.startswith('@'):current=int(l[1:]);out[current]=[]
  else:
   r,t=l.split(' :: ',1);out[current].append({'statement':t,'aliases':r.split(' + ')})
 return out
facts={}
for n in ['coverage_facts_000_034.txt','coverage_facts_035_069.txt']:facts.update(parse(W/n))
old=parse(W/'coverage_facts_070_099.txt')
remap={70:95,74:77,79:76,80:73,81:79,86:80,89:85,90:83,92:82,93:86,96:89}
for to,fr in remap.items():facts[to]=old[fr]
facts.update(parse(W/'coverage_tail_adjustments.txt'))
facts[93]=facts[93][1:]
# Boundary and source precision adjustments.
facts[24]=facts[24][:3]
facts[34][1]={'statement':'Transport handlers adapt HTTP inputs and outputs, business callables enforce application rules, and persistence adapters access stored state; separate these responsibilities so each can change without embedding the other responsibilities.','aliases':['fa_dependencies#what-is-dependency-injection','fa_bigger-applications#apirouter']}
facts[34][2]={'statement':'Move a business decision from a handler into a plain callable with explicit inputs, keep the HTTP adaptation in the handler, and call a separate persistence adapter for stored state rather than treating separate files alone as a responsibility boundary.','aliases':['fa_dependencies#simple-and-powerful','fa_bigger-applications#apirouter']}
facts[35][2]={'statement':'BackgroundTasks work runs in the application process and cannot guarantee survival or delivery when that process fails.','aliases':['fa_background-tasks#caveat']}
facts[37]=[
 {'statement':'The last middleware added is the outermost wrapper: requests traverse it first, while responses traverse it last.','aliases':['fa_middleware#multiple-middleware-execution-order']},
 {'statement':'Configure each selected maintained middleware with app.add_middleware(MiddlewareClass, option=value), passing the component\'s documented options rather than writing its protocol implementation.','aliases':['starlette_middleware#using-middleware']},
 {'statement':'For two middleware additions, trace the request through the second addition then the first and into the handler, and trace the resulting response through the first addition then the second.','aliases':['fa_middleware#multiple-middleware-execution-order']},
]
facts[9][2]={'statement':'Trace the application receiving http.request events through receive(), then sending http.response.start with status and headers followed by http.response.body through send().','aliases':['asgi_intro#show-me-the-code']}
facts[26].append({'statement':'Verify a cross-field rule with input that passes each individual field\'s validation but violates the model invariant, asserting that model construction raises ValidationError; also verify a consistent input is accepted.','aliases':['pd_validators#model-validators','pydantic_models_docs#error-handling']})
facts[58]=[
 {'statement':'Maintained request instrumentation records request and response counters and a duration histogram around the application boundary rather than requiring each handler to implement its own metrics.','aliases':['starlette_prom_impl#L12-L27']},
 {'statement':'Install the documented PrometheusMiddleware with app.add_middleware(PrometheusMiddleware, filter_unhandled_paths=True) and expose its metrics view with app.add_route("/metrics/", metrics), importing both from starlette_prometheus.','aliases':['starlette_prom#readme']},
 {'statement':'Use bounded nonsensitive labels such as method, matched route template and response status; filter unmatched paths so arbitrary requested paths do not generate unlimited metric series.','aliases':['starlette_prom_impl#L92-L103','starlette_prom#readme','prom_instrument#use-labels']},
 {'statement':'Verify wiring with controlled successful, expected-error and delayed responses, comparing request and response counter changes and the completed responses\' duration observations with those known requests.','aliases':['starlette_prom_impl#L44-L85','fa_testing#using-testclient']},
 {'statement':'Interpret the selected middleware\'s measurement boundary accurately: its response counter is updated even for a raised exception, but its processing-time histogram is observed only when the inner application returns a response.','aliases':['starlette_prom_impl#L60-L85']},
]
facts[51][0]['statement']='AsyncSession maintains mutable state for current database work and is not safe to share across concurrent tasks; use a separate session for each concurrent unit of work.'


facts[63]=[
 {'statement':'A bearer extraction dependency reads a credential from Authorization: Bearer token; receiving the credential does not itself establish that it is valid.','aliases':['fa_security_ref#fastapi.security.HTTPBearer']},
 {'statement':'Declare Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())] on a handler input and read its scheme and credentials fields to obtain the supplied bearer credential.','aliases':['fa_security_ref#fastapi.security.HTTPBearer']},
 {'statement':'With HTTPBearer\'s default auto_error=True, absent credentials or a non-bearer scheme are rejected instead of supplied to the handler; verify absent and malformed Authorization headers separately.','aliases':['fa_security_ref#fastapi.security.HTTPBearer']},
]
facts[65].append({'statement':'Review an autogenerated drop-and-add pair for a possible rename before applying it; dropping a column deletes the data stored in that column, so an apparent reversal may not recover that data.','aliases':['al_autogenerate#what-does-autogenerate-detect-and-what-does-it-not-detect','pg_alter#DDL-ALTER-REMOVING-A-COLUMN']})
facts[74][1]['aliases']=['pg_query_limit#QUERIES-LIMIT']
facts[17][0]['statement']='Declare a column as TYPE NOT NULL to reject nulls independently of whether a write came through an application.'
facts[17][1]['statement']='Declare UNIQUE (columns) to reject duplicate combinations; PostgreSQL treats nulls as distinct by default unless NULLS NOT DISTINCT is specified.'
facts[17][2]['statement']='Declare PRIMARY KEY (columns) for unique non-null row identity; a primary key can contain more than one column.'
facts[17][3]['statement']='Declare FOREIGN KEY (columns) REFERENCES target (columns) so non-null referencing values must match referenced rows.'
facts[23][0]['statement']='Create a FastAPI instance and register a handler with @app.get("/path"), @app.post("/path"), @app.put("/path") or @app.delete("/path") for the intended method and path.'
facts[36][2]={'statement':'A sub-dependency can declare typed query inputs of its own; those inputs are extracted from the request before its returned value is supplied to the dependent provider.','aliases':['fa_dependencies_sub-dependencies#first-dependency-dependable','fa_dependencies_sub-dependencies#second-dependency-dependable-and-dependant']}
facts[41][2]={'statement':'Emit logger.error(message, extra=event_fields) with the standard logging library to attach structured fields to the LogRecord, and configure the existing formatter or collection pipeline to preserve those field names; custom keys must not collide with reserved LogRecord attributes.','aliases':['py_logging#logging.Logger.debug','ow_Logging_Cheat#event-collection']}
facts[53][0]['aliases']=['kube_probes#']
facts[57][1]['aliases']=['fa_path-params#data-validation','fa_handling-errors#override-request-validation-exceptions']
facts[61][2]['aliases']=['sa_selectable#sqlalchemy.sql.expression.GenerativeSelect.limit']
facts[74][0]['aliases'].append('sa_selectable#sqlalchemy.sql.expression.GenerativeSelect.limit')
facts[74][2]={'statement':'OFFSET skips the requested number of result rows and LIMIT caps the number returned afterward; use the same filter and unique ordering for the page selections.','aliases':['pg_query_limit#QUERIES-LIMIT','sa_selectable#sqlalchemy.sql.expression.GenerativeSelect.offset']}
facts[76][3]['statement']='Verify the generated identity and committed field values with await fresh_session.get(Entity, identity) in an independent session rather than checking only that a Python object was constructed.'
facts[78][3]['statement']='Reload the committed entity in an independent session and verify both the changed supplied fields and the unchanged omitted fields, rather than inspecting only the request model.'
facts[80][3]={'statement':'Inspect ttl(key): it reports remaining seconds, -1 for a key without expiry and -2 for an absent key; change the primary record and verify that invalidation makes the next read return the changed value.','aliases':['redis_ttl#','redis_cache_code#inspect-cached-entries-directly-in-redis']}
facts[89][3]['statement']='Compare emitted SQL before and after the loading change with engine echo=True logging enabled, confirming both reduced relationship queries and unchanged returned entity data.'
facts[93][1]['aliases']+=['pg_constraints#ddl-constraints-unique','sa_test_tx#managing-transactions']
facts[94][2]={'statement':'Keep the receiver clock synchronized so comparing an authenticated timestamp with the local clock enforces the intended freshness window rather than a window distorted by clock drift.','aliases':['ow_Webhook_Security#replay-attack-protection']}
facts[84][4]['aliases'].append('starlette_testclient#testclient')
# Match cited headings to their canonical ids. Numeric RFC sections remain conventional section locators.
fix={
 'rfc_9700_oauth2_security_bcp':'ietf_rfc9700',
}
groups={
 'starlette_prom':'fastapi_docs_advanced','starlette_prom_impl':'fastapi_docs_advanced','asgi_intro':'fastapi_docs_advanced','starlette_middleware':'fastapi_docs_advanced','starlette_requests':'fastapi_docs_advanced','starlette_exceptions':'fastapi_docs_advanced','starlette_testclient':'fastapi_docs_advanced',
 'httpx':'fastapi_docs_advanced','httpx_async':'fastapi_docs_advanced','httpx_timeouts':'fastapi_docs_advanced','httpx_exceptions':'fastapi_docs_advanced',
 'uvicorn':'fastapi_docs_tutorial','uv_settings':'fastapi_docs_tutorial','uv_behavior':'fastapi_docs_tutorial',
 'jwt_install':'fastapi_docs_tutorial','jwt_usage':'fastapi_docs_tutorial','jwt_api':'fastapi_docs_tutorial',
 'stripe_webhooks':'owasp_api_security_top10_2023', 'kube_probes':'fastapi_docs_tutorial','oauth_core':'ietf_rfc9700','pg_query_limit':'postgresql_docs',
}
anchor_overrides={}
if (W/'coverage_anchor_fixes.json').exists():anchor_overrides=json.load(open(W/'coverage_anchor_fixes.json'))
issues=[];audit=[]
def citation(a):
 name,anchor=a.split('#',1);name=fix.get(name,name)
 if name=='fa_middleware':name='fa_tutorial_middleware'
 anchor=anchor_overrides.get(a,anchor)
 if name in source_ids:
  group=name;url=urls[name]
 elif name in groups:group=groups[name];url=urls[name]
 else:
  url=urls.get(name)
  if not url:raise RuntimeError('Unknown source '+name)
  if name.startswith('fa_'):group='fastapi_docs_tutorial' if '/tutorial/' in url or '/deployment/' in url or '/virtual-environments/' in url else 'fastapi_docs_advanced'
  elif name.startswith('py_'):group='python_tutorial'
  elif name.startswith('pd_'):group='pydantic_models_docs'
  elif name.startswith('sa_'):group='sqlalchemy_20_tutorial'
  elif name.startswith('pg_'):group='postgresql_docs'
  elif name.startswith('al_'):group='alembic_docs'
  elif name.startswith('ow_'):group='owasp_api_security_top10_2023'
  elif name.startswith('tf_'):group='twelve_factor_app'
  elif name.startswith('redis_'):group='redis_docs'
  elif name.startswith('prom_'):group='prometheus_client_python'
  elif name.startswith('otel_'):group='opentelemetry_python_docs'
  elif name.startswith('docker_'):group='docker_docs'
  elif name.startswith('pytest_'):group='pytest_getting_started'
  elif name.startswith('mdn_'):group='mdn_http'
  else:raise RuntimeError('Unknown source group '+name)
 if name not in ids:issues.append({'alias':a,'reason':'not opened','url':url})
 elif anchor and not re.fullmatch(r'(?:\d+(\.\d+)*|L\d+-L\d+)',anchor) and anchor not in ids[name]:
  low=anchor.lower();match=[i for i in ids[name] if i.lower()==low]
  if match:anchor=match[0]
  else:issues.append({'alias':a,'reason':'locator missing','url':url,'available':ids[name]})
 audit.append({'alias':a,'source_id':group,'url':url,'section':anchor})
 return group+'#'+url.split('#')[0]+('#'+anchor if anchor else '')
cs=json.load(open(B/'extracted_concepts.json'))['concepts'];lookups=json.load(open(B/'registry_lookup.json'))['lookups']
lookup={(x['concept_id'],x['path_id']):x for x in lookups}
assert set(facts)==set(range(len(cs)))
briefs=[];owners={}
for c in cs:
 i=c['toc_sequence_position'];cid=c['concept_id'];pid=c['path_id'];status=lookup[cid,pid]['canonical_status']
 assert status=='new',status
 fs=[{'id':f'f{j+1}','statement':f['statement'],'source_refs':[citation(a) for a in f['aliases']]} for j,f in enumerate(facts[i])]
 ev={'concept_id':cid,'required_facts':fs,'optional_enrichment':[],'misconceptions':[],'created_in_batch_id':B.name,'used_by_path_ids':[pid]}
 # Each objective is written for the path using its exact goal and concrete practice.
 objective=c['primary_objective'].rstrip('. ')+': '+c['practice_objective'][0].lower()+c['practice_objective'][1:].rstrip('. ')+'.'
 briefs.append({'concept_id':cid,'path_id':pid,'learning_objective':objective,'canonical_status':status,'evidence':ev})
parents=[B/'extracted_concepts.json',B/'registry_lookup.json',B/'concept_evidence_registry_snapshot.json',B/'source_pack_manifest.json',pack]
now=datetime.datetime.now(datetime.timezone.utc)
metadata={'artifact_type':'coverage_briefs','artifact_version':'1.0.0','schema_version':'1.0.0','batch_id':B.name,'run_id':B.name+'__03_coverage_brief__'+now.strftime('%Y%m%dT%H%M%SZ'),'prompt_version':'03_coverage_brief@v1','model':'none','generated_at':now.isoformat(timespec='seconds').replace('+00:00','Z'),'source_snapshot_id':json.load(open(B/'extracted_concepts.json'))['metadata']['source_snapshot_id'],'parent_artifact_hashes':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in parents}}
artifact={'metadata':metadata,'batch_id':B.name,'briefs':briefs}
(B/'coverage_briefs.part.all.json').write_text(json.dumps(artifact,ensure_ascii=False,indent=2)+'\n')
(W/'coverage_citation_audit.json').write_text(json.dumps(audit,indent=2))
(W/'coverage_source_issues.json').write_text(json.dumps(issues,indent=2))
print('briefs',len(briefs),'facts',sum(len(b['evidence']['required_facts']) for b in briefs),'citation issues',len(issues))
print('unique citation issues',len({x['alias'] for x in issues}))
