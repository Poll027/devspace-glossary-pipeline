import json,glob,re
names={x['channel_id']:x['channel_name'] for x in json.load(open('00_GLOSSARY_PIPELINE_CORE/video_bank/channel_allowlist.json'))['channels']}
pat=r'idempot|http method|type hint|type annot|context manag|decorator|asyncio|virtual env|venv|poetry|requirements|pipenv|python package|python import|python class|pydantic|constraint|cors|lifespan|password hash|bcrypt|ssrf|redact|logging|loguru|structlog|prometheus|observability|webhook|retry|retries|redis|cache.aside|jwt|oauth|openid|nginx|gunicorn|sql injection|indexing|database index|transaction|rollback|health check|readiness|shutdown'
for f in glob.glob('00_GLOSSARY_PIPELINE_CORE/video_bank/channel_catalogs/*.json'):
 d=json.load(open(f));vs=[v for v in d['videos'] if re.search(pat,v['title'],re.I)]
 if vs:
  print('\n'+names.get(d['channel_id'],d['channel_id']))
  for v in vs[:100]: print(v['video_id'],v['duration_seconds'],v['title'])
