import runpy,concurrent.futures
from pathlib import Path
m=runpy.run_path(str(Path(__file__).with_name('build_video_candidates.py')))
queries={12:'CORS preflight',25:'HTTPX async client',33:'HTTPX timeout',42:'SSRF prevention',45:'FastAPI use_cache dependency caching',49:'TrustedHostMiddleware',50:'Python logging redact sensitive data',70:'Uvicorn forwarded-allow-ips',81:'Redis cache failure fallback',83:'FastAPI additional responses',85:'HTTPX raise_for_status exception handling',89:'SQLAlchemy selectinload',97:'FastAPI HTTPBearer OpenAPI',98:'FastAPI OpenAPI schema'}
for n,q in queries.items():
 old=m['W']/f'yt_search_{n:03}.json';old.rename(m['W']/f'yt_search_{n:03}_initial.json');pat,_,ids=m['S'][n];m['S'][n]=(pat,q,ids)
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
 results=list(pool.map(m['get_open'],queries))
for n,d in zip(queries,results):
 print('\n',n,d['query'],'RESULTS',len(d['videos']))
 for v in d['videos'][:7]:print(v['video_id'],v['duration_seconds'],v['channel_name'],'|',v['title'])
