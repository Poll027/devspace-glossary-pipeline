import json,glob,re,hashlib,datetime,urllib.request,urllib.parse,concurrent.futures,time
from pathlib import Path
B=Path('batches/glossary_batch_python_fastapi_backend_developer');W=B/'working'
inputs=[B/'glossary_pass_a.json',B/'registry_lookup.json',B/'extracted_concepts.json',B/'coverage_briefs.json',Path('00_GLOSSARY_PIPELINE_CORE/video_bank/channel_allowlist.json')]
catalog_paths=sorted(Path('00_GLOSSARY_PIPELINE_CORE/video_bank/channel_catalogs').glob('*.json'));inputs+=catalog_paths
G=json.load(open(inputs[0]));R=json.load(open(inputs[1]));E=json.load(open(inputs[2]));C=json.load(open(inputs[3]));A=json.load(open(inputs[4]))
channels={x['channel_id']:x['channel_name'] for x in A['channels']};hints={x['channel_id']:x.get('career_family_ids',[]) for x in A['channels']}
cat={}
for p in catalog_paths:
 d=json.load(open(p))
 for v in d['videos']:
  cat[v['video_id']]={**v,'channel_id':d['channel_id'],'channel_name':channels.get(d['channel_id'],d['channel_id'])}
# Tile-ordered search specifications: title regex, fallback query, and explicitly reviewed catalogue preferences.
S={
1:('idempot|http methods','HTTP methods safety idempotency explained','UaKZ4wKytcA w1P7FBBrrig'),
3:('type hint|type annot|python typing','Python type hints tutorial','QORvB-_mbZ0 fM4O9bModsE'),
4:('python.*oop|python.*class|object.oriented.*python','Python classes instances beginner tutorial',''),
5:('context manag','Python context manager cleanup tutorial','-aKFBoZpiqA 14z_Tf3p2Mw'),
6:('asyncio|python asynchronous','Python async await event loop tutorial','oAkLSJNr5zY Qb9s3UiMSTA'),
7:('decorator.*python|python.*decorator','Python decorator wrapper tutorial','FsAPt_9Bf3U 6McU94UMY9M'),
8:('virtual env|venv','Python virtual environments pip tutorial','Y21OR1OPC9A Kg1Yvry_Ydk'),
9:('asgi|uvicorn','ASGI request lifecycle Uvicorn FastAPI explained',''),
10:('password.*hash|hash.*password|bcrypt','Python password hashing verification argon2 tutorial',''),
11:('sqlalchemy.*model|sqlalchemy|fastapi.*database','SQLAlchemy 2 declarative models tutorial','NvOV3ig2tGY V0FUealWanc'),
12:('cors','CORS preflight OPTIONS explained','PNtFSVU-YTI'),
14:('pydantic','Pydantic V2 model validation conversion tutorial','M81pfi64eeM 9GHxnttXxrA'),
15:('poetry|pipenv|package manager|requirements|uv .*python|python.*uv','Python reproducible dependencies lock file tutorial','AMdG7IjgSPM Ji2XDxmXSOM'),
16:('python.*import|python.*package|python.*module','Python packages imports service project structure tutorial',''),
17:('constraint|foreign key|primary key','PostgreSQL integrity constraints tutorial',''),
18:('fastapi.*lifespan|lifespan.*fastapi','FastAPI lifespan startup shutdown tutorial',''),
19:('sqlalchemy|fastapi.*database','SQLAlchemy relationship mapping tutorial','NvOV3ig2tGY aAy-B6KPld8'),
20:('pydantic','Pydantic V2 Field constraints tutorial','M81pfi64eeM 9GHxnttXxrA'),
21:('pydantic','Pydantic V2 nested models tutorial','M81pfi64eeM 9GHxnttXxrA'),
22:('rest.*api|api.*rest|restful|fastapi','REST API resource URLs CRUD design beginner','8TMQcRcBnW8 iWS9ogMPOI0'),
23:('fastapi','FastAPI path operation tutorial','7AMjmCTumuo Fmw1i1cBYq4'),
24:('pydantic.*setting|fastapi.*config|environment.*config','FastAPI pydantic settings environment validation startup',''),
25:('httpx|aiohttp','Python HTTPX async requests tutorial','qAh5dDODJ5k OPyoXx0yA0I'),
26:('pydantic','Pydantic V2 field validator model validator tutorial','M81pfi64eeM'),
27:('fastapi.*error|fastapi.*exception|exception.*fastapi|fastapi.*validation','FastAPI HTTPException error handling tutorial','WRjXIA5pMtk 7MHDDOrDx-w'),
28:('sync vs async|fastapi.*async|async.*fastapi','FastAPI def async def blocking event loop explained','2JPDt-Jp6fM'),
29:('fastapi.*router|fastapi.*project','FastAPI APIRouter modular application tutorial','NkgIHa6KtHg'),
30:('fastapi.*path|fastapi.*query','FastAPI path query parameters tutorial','WRjXIA5pMtk f1zggIOxmJg'),
31:('fastapi.*response|pydantic.*schema','FastAPI response model exclude password tutorial','9GHxnttXxrA'),
32:('fastapi.*depend','FastAPI Depends dependency injection tutorial','TzXQwHBDEPc'),
33:('httpx.*timeout|timeout.*httpx|outbound.*timeout','Python HTTPX timeout connect read write pool tutorial',''),
35:('fastapi.*background|background.*fastapi','FastAPI BackgroundTasks limitations tutorial','4HxjBvZMAg8'),
36:('fastapi.*depend','FastAPI sub dependencies dependency graph tutorial','TzXQwHBDEPc'),
37:('fastapi.*middleware|middleware.*fastapi','FastAPI middleware request response order tutorial',''),
38:('fastapi.*deploy|uvicorn|gunicorn','FastAPI production Uvicorn workers no reload tutorial','eqjngvKfabg wd1wt2d0eus'),
39:('fastapi.*pydantic|pydantic.*schema','FastAPI request body Pydantic tutorial','9GHxnttXxrA M-DzoNzmJI0'),
40:('fastapi.*yield|yield.*depend','FastAPI yield dependencies cleanup tutorial',''),
41:('python.*logging|logging.*python|structlog|loguru','Python structured logging JSON request logs tutorial','pxuXaaT1u3k'),
42:('ssrf','Python prevent SSRF outbound requests tutorial','SC1WEe5-WDA'),
43:('fastapi.*upload|multipart.*fastapi','FastAPI form file upload size limits tutorial','AExumWjfbyo'),
44:('cors','FastAPI CORS origins credentials tutorial','PNtFSVU-YTI'),
45:('fastapi.*depend','FastAPI dependency caching use_cache request scope tutorial',''),
46:('fastapi.*test|test.*fastapi','FastAPI TestClient HTTPX async endpoint tests tutorial','SO7m7nod0ts 9gC3Ot0LoUQ'),
48:('fastapi.*openapi|fastapi.*swagger','FastAPI OpenAPI generation typed routes tutorial',''),
49:('trustedhost|trusted host','FastAPI TrustedHostMiddleware tutorial',''),
50:('log.*redact|redact.*log|sensitive.*log','Python logging redact passwords tokens filter tutorial',''),
51:('sqlalchemy.*async|async.*sqlalchemy|fastapi.*async','SQLAlchemy 2 async session FastAPI dependency lifecycle tutorial','2JPDt-Jp6fM'),
52:('graceful shutdown','FastAPI Uvicorn graceful shutdown SIGTERM tutorial','abUaM6iuElU'),
53:('health check|readiness|liveness','FastAPI health readiness database check tutorial',''),
54:('fastapi.*metadata|fastapi.*openapi|fastapi.*example','FastAPI OpenAPI examples tags summary description tutorial',''),
55:('fastapi.*test|test.*fastapi|fastapi.*depend','FastAPI dependency overrides testing tutorial','9gC3Ot0LoUQ'),
56:('fastapi.*header|fastapi.*cookie','FastAPI Header Cookie parameters tutorial',''),
57:('fastapi.*validation|fastapi.*error','FastAPI RequestValidationError 422 tutorial','WRjXIA5pMtk 9GHxnttXxrA'),
58:('fastapi.*prometheus|prometheus.*fastapi|fastapi.*metric','FastAPI prometheus instrumentator request metrics tutorial',''),
59:('fastapi.*patch|fastapi.*update|pydantic.*update','FastAPI Pydantic partial update exclude_unset PATCH tutorial','VyoGAoxQhxM'),
61:('fastapi.*database|fastapi.*sqlalchemy|sqlalchemy|fastapi.*fetch','SQLAlchemy 2 select retrieve scalar FastAPI tutorial','NvOV3ig2tGY TzXQwHBDEPc'),
62:('transaction|rollback','SQLAlchemy session commit rollback transaction tutorial',''),
63:('fastapi.*auth|bearer.*fastapi','FastAPI HTTPBearer dependency token extraction tutorial','MY0TFMMm9B0'),
64:('cache.aside|redis.*cach','Python Redis cache aside tutorial',''),
65:('alembic','Alembic migrations SQLAlchemy tutorial','e8NnDz8uT7o'),
66:('database index|indexing.*postgres|postgres.*index','PostgreSQL indexes query performance beginner tutorial','-qNSXK7s7_w Jemuod4wKWo'),
68:('fastapi.*exception|exception.*fastapi|fastapi.*error','FastAPI translate domain exceptions database errors tutorial','7MHDDOrDx-w'),
69:('fastapi.*exception|exception.*fastapi|fastapi.*error','FastAPI custom exception handler JSON error response tutorial','7MHDDOrDx-w'),
70:('proxy header|forwarded header','FastAPI Uvicorn proxy headers trusted forwarded IP tutorial',''),
71:('webhook','Python webhook endpoint acknowledgement request validation tutorial','41NOoEz3Tzc yc-gp3PFHEI'),
72:('correlation.*id|request.*id.*log|log.*request.*id','FastAPI request ID correlation logging middleware tutorial',''),
73:('prometheus|service.*metric|request.*metric','Prometheus request rate error rate latency labels explained','h4Sl21AKiDg f4W_eEJC-20'),
74:('fastapi.*pagination|pagination.*fastapi','FastAPI pagination limit offset filters tutorial','f1zggIOxmJg'),
75:('sql injection','Python SQLAlchemy parameterized queries SQL injection prevention','Azo9tDUtC9s'),
76:('fastapi.*database|fastapi.*sqlalchemy|fastapi.*crud','SQLAlchemy 2 insert create resource FastAPI tutorial','NvOV3ig2tGY FN_BvbOwur0'),
77:('fastapi.*delete|fastapi.*crud','SQLAlchemy delete resource FastAPI tutorial','VyoGAoxQhxM XMoK33jsgcs'),
78:('fastapi.*update|fastapi.*crud','SQLAlchemy update resource FastAPI tutorial','VyoGAoxQhxM XMoK33jsgcs'),
79:('jwt','Python PyJWT verify issuer audience expiry signature tutorial',''),
80:('cache.*expir|cache.*invalid|redis.*ttl|caching.*strateg','Redis cache TTL invalidation freshness tutorial',''),
81:('cache.*fail|redis.*fail|cache.*stampede','Redis cache failure fallback Python timeout tutorial',''),
82:('fastapi.*deploy|twelve.factor|12.factor','FastAPI build release run deploy rollback tutorial','eqjngvKfabg wd1wt2d0eus'),
83:('fastapi.*response|fastapi.*openapi','FastAPI additional responses OpenAPI status codes tutorial',''),
84:('fastapi.*exception|exception.*fastapi|fastapi.*error','FastAPI exception handler safe 500 logging tutorial','7MHDDOrDx-w'),
85:('httpx.*error|fastapi.*upstream|fastapi.*exception|exception.*fastapi','FastAPI HTTPX upstream error timeout response translation',''),
86:('webhook.*signature|webhook.*secur|webhook.*verif','Python webhook HMAC signature verification raw body tutorial',''),
87:('python.*logging|logging.*python|fastapi.*debug|debug.*fastapi','FastAPI diagnose errors logs metrics request correlation tutorial','C-bie4ZY_o0'),
88:('fastapi.*rate limit|rate limit.*fastapi|api.*resource','FastAPI rate limiting payload size resource limits tutorial','pZunzLJ1qcQ'),
89:('n.?1.*quer|sqlalchemy.*load|sqlalchemy.*performance','SQLAlchemy N+1 queries selectinload eager loading tutorial',''),
90:('fastapi.*test|test.*fastapi|database.*test','FastAPI pytest database isolation rollback fixtures tutorial','9gC3Ot0LoUQ SO7m7nod0ts'),
91:('fastapi.*clerk|fastapi.*keycloak|fastapi.*oauth|oauth 2.0 course','FastAPI Keycloak authorization code PKCE resource server JWT audience',''),
92:('fastapi.*authoriz|fastapi.*roles|fastapi.*scope','FastAPI endpoint authorization scopes permissions tutorial','MY0TFMMm9B0'),
93:('webhook.*idempot|webhook.*duplic|idempoten','Python webhook idempotency duplicate event handling tutorial','4OuaONkZw1I'),
94:('webhook.*replay|webhook.*timestamp|webhook.*fresh','webhook signature timestamp replay attack prevention Python',''),
95:('retry|retries|idempotent requests','Python HTTP retry backoff bounded idempotent requests tutorial','43vH_lnM7x0 w1P7FBBrrig'),
97:('fastapi.*oauth|fastapi.*bearer|fastapi.*security','FastAPI OpenAPI HTTPBearer authorization code OAuth2 security scheme',''),
98:('fastapi.*openapi|fastapi.*swagger','FastAPI inspect OpenAPI schema sensitive fields security tutorial',''),
99:('fastapi.*test|test.*fastapi|jwt.*test','FastAPI pytest JWT invalid token authorization tests','SO7m7nod0ts 9gC3Ot0LoUQ')}
# Cheap title/channel/duration filter. Do not infer transcript coverage or visual quality.
def rejection(v):
 t=v['title'];ch=v['channel_name']
 if re.search(r'hindi|telugu|tamil|español|portugu[eê]s',t,re.I) or ch in {'CodeWithHarry','Krish Naik'}:return 'Non-English or mixed-language instructional channel/title; English instruction is required.'
 if re.search(r'Pydantic\s*(?:v?1\b)|SQLAlchemy\s*1\.[0-3]',t,re.I):return 'Title signals an obsolete API version for this version-sensitive learning target.'
 if re.search(r'news|podcast|let.s discuss|vs |versus|which.*best|interview|roadmap|CTF|hackthebox|tryhackme|picoctf|minecraft|AI agents|LangChain|LangGraph',t,re.I) and not re.search(r'Sync vs Async',t,re.I):return 'Title signals commentary, comparative advice, unrelated application context, or advanced security exercises rather than the required introductory topic.'
 if re.search(r'advanced|expert|next.level|master class|scalable|distributed|microservices|kubernetes',t,re.I):return 'Title signals advanced scope or infrastructure prerequisites beyond this entry/junior learning target.'
 if v.get('duration_seconds') is None or v['duration_seconds']<90:return 'Duration is missing or too short to plausibly support a self-contained instructional explanation.'
 return None
# All catalogues are searched by the concept-specific title regex; manually pinned preferences outrank other matches.
def catalog_search(n):
 pat,q,picks=S[n];ms=[v for v in cat.values() if re.search(pat,v['title'],re.I)]
 picked=[]
 for id in picks.split():
  assert id in cat,id
  assert re.search(pat,cat[id]['title'],re.I),(n,id)
  picked.append(cat[id])
 # Automatic additions only for tightly scoped foundational concepts; narrow backend targets use targeted open fallback.
 if n in {4,16,17}:
  good=[v for v in ms if not rejection(v) and (('Python' in v['title'] or 'python' in v['title']) if n in {4,16} else ('MySQL' in v['title'] or 'PostgreSQL' in v['title']))]
  good.sort(key=lambda v:(not('python_fastapi_backend_developer' in hints.get(v['channel_id'],[])),v['duration_seconds']))
  for v in good:
   if v['video_id'] not in {p['video_id'] for p in picked}:picked.append(v)
   if sum(not rejection(p) for p in picked)>=2:break
 return ms,picked

def get_open(n):
 q=S[n][1];p=W/f'yt_search_{n:03}.json'
 if p.exists():return json.load(open(p))
 url='https://www.youtube.com/results?search_query='+urllib.parse.quote(q)
 result={'query':q,'result_url':url,'videos':[]}
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0','Accept-Language':'en-US,en;q=0.9'})
  text=urllib.request.urlopen(req,timeout=35).read().decode()
  match=re.search(r'var ytInitialData\s*=\s*',text)
  if not match:raise ValueError('No ytInitialData')
  data=json.JSONDecoder().raw_decode(text[match.end():])[0]
  def textof(x):return x.get('simpleText') or ''.join(y.get('text','') for y in x.get('runs',[]))
  def walk(x):
   if isinstance(x,dict):
    if 'videoRenderer' in x:
     v=x['videoRenderer'];owner=v.get('ownerText',{}).get('runs',[{}])[0];cid=owner.get('navigationEndpoint',{}).get('browseEndpoint',{}).get('browseId','');dur=textof(v.get('lengthText',{}));id=v.get('videoId','')
     # Copy ID from the real result's watch endpoint URL, never from memory.
     endpoint=v.get('navigationEndpoint',{});source=endpoint.get('commandMetadata',{}).get('webCommandMetadata',{}).get('url','')
     parsed=urllib.parse.parse_qs(urllib.parse.urlsplit(source).query).get('v',[])
     if not parsed or parsed[0]!=id or not re.fullmatch('[A-Za-z0-9_-]{11}',id) or not cid or not re.fullmatch(r'\d+(?::\d+){1,2}',dur):return
     seconds=0
     for part in dur.split(':'):seconds=seconds*60+int(part)
     result['videos'].append({'video_id':parsed[0],'source_result_url':'https://www.youtube.com'+source,'title':textof(v.get('title',{})),'channel_id':cid,'channel_name':owner.get('text',''),'duration_seconds':seconds})
     return
    for v in x.values():walk(v)
   elif isinstance(x,list):
    for v in x:walk(v)
  walk(data)
 except Exception as ex:result['error']=str(ex)
 p.write_text(json.dumps(result,ensure_ascii=False,indent=2));return result

if __name__=='__main__':
 eligible=[e for e in E['concepts'] if next(g for g in G['entries'] if g['concept_id']==e['concept_id'])['video_need']['level'] in {'HIGH','MEDIUM'}]
 assert set(S)=={e['toc_sequence_position'] for e in eligible}
 # Reuse is always checked first. No lookup in this batch exposes a reusable segment.
 assert all(not r['reusable_segment_ids'] for r in R['lookups'])
 searches={};need=[]
 for e in eligible:
  n=e['toc_sequence_position'];ms,picked=catalog_search(n);searches[n]=(ms,picked)
  if sum(not rejection(v) for v in picked)<2:need.append(n)
 print('Eligible',len(eligible),'catalogue videos',len(cat),'open fallback concepts',len(need),flush=True)
 with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
  opens=dict(zip(need,pool.map(get_open,need)))
 # Save compact inspection report before final selection.
 report=[]
 for e in eligible:
  n=e['toc_sequence_position'];ms,picked=searches[n];report.append(f"\n{n} {e['concept_id']} | {e['concept_name']} (catalogue title matches: {len(ms)})")
  for v in picked:report.append('CAT '+v['video_id']+' '+v['title']+' | '+str(rejection(v)))
  if n in opens:
   if opens[n].get('error'):report.append('ERROR '+opens[n]['error'])
   for v in opens[n]['videos'][:8]:report.append('OPEN '+v['video_id']+' '+v['channel_name']+' | '+str(v['duration_seconds'])+' | '+v['title']+' | '+str(rejection(v)))
 (W/'selection_review.txt').write_text('\n'.join(report))
 print('Wrote selection_review.txt; failed searches:',[(n,r.get('error')) for n,r in opens.items() if r.get('error')],flush=True)
