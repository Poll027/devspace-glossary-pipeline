import json,re
from pathlib import Path
B=Path('batches/glossary_batch_python_fastapi_backend_developer/working/coverage_sources')
items={}
def pick(base, name, pattern):
 links=json.load(open(B/(base+'.links.json')))
 matches=[l for l in links if re.search(pattern,l)]
 if not matches:print('MISSING',base,name,pattern);return
 items[name]=min(matches,key=len).split('#')[0]
for p in ['first-steps','path-params','query-params','body','body-fields','body-nested-models','response-model','handling-errors','response-status-code','bigger-applications','background-tasks','middleware','cors','request-files','request-forms-and-files','schema-extra-example','path-operation-configuration','header-params','cookie-params','testing','body-updates','metadata','dependencies','dependencies/sub-dependencies','dependencies/dependencies-with-yield','security/first-steps','security/oauth2-jwt']:
 pick('fastapi_docs_tutorial','fa_'+p.replace('/','_'),'tiangolo.com/tutorial/'+p+'/$')
for p in ['events','settings','testing-dependencies','testing-events','middleware','behind-a-proxy','additional-responses','security/oauth2-scopes','openapi-webhooks','async-tests','opentelemetry','path-operation-advanced-configuration']:
 pick('fastapi_docs_tutorial','fa_'+p.replace('/','_'),'tiangolo.com/advanced/'+p+'/$')
for p in ['classes','errors','modules','venv','controlflow']:
 pick('python_tutorial','py_'+p,'tutorial/'+p+r'\.html$')
for p in ['orm_related_objects','orm_data_manipulation','data_select','metadata','data_update','dbapi_transactions']:
 pick('sqlalchemy_20_tutorial','sa_'+p,'tutorial/'+p+r'\.html$')
for p in ['fields','validators','serialization']:
 pick('pydantic_models_docs','pd_'+p,'concepts/'+p+'/$')
for term in ['unrestricted-resource-consumption','broken-object-level-authorization','broken-authentication','security-misconfiguration','unsafe-consumption','server-side-request-forgery']:
 pick('owasp_api_security_top10_2023','ow_'+term,term+'/?$')
for term in ['config','build-release-run','disposability','logs','backing-services','dev-prod-parity']:
 pick('twelve_factor_app','tf_'+term,'12factor.net/'+term+'$')
pick('redis_docs','redis_py','/clients/redis-py/$')
pick('prometheus_client_python','prom_counter','/counter/$')
pick('prometheus_client_python','prom_histogram','/histogram/$')
pick('prometheus_client_python','prom_labels','/labels/$')
pick('alembic_docs','al_tutorial','/tutorial.html$')
pick('alembic_docs','al_autogenerate','/autogenerate.html$')
for t in ['uvicorn','deployment/manually','deployment/server-workers','deployment/docker','virtual-environments']:
 pick('fastapi_docs_tutorial','fa_'+t.replace('/','_'), t+'/?$')
pick('mdn_http','mdn_cors','/CORS$')
pick('postgresql_docs','pg_constraints','/ddl-constraints.html$')
pick('postgresql_docs','pg_indexes','/indexes.html$')
(B.parent/'coverage_fetch_list.json').write_text(json.dumps(items,indent=2))
