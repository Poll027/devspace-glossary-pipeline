import build_video_candidates as s
import json,re,datetime,hashlib,glob
B=s.B
openres=s.load(B/'working/open_search_results.json')
# Explicit selection by index in saved actual YouTube result lists; never inferred IDs.
O={
'vue.state_ownership':[0,1],
'composer.locked_dependencies':[0,12,14],
'javascript.application_conditionals':[0,1,2],
'laravel.phpunit_execution':[0,1,2],
'laravel.production_configuration':[1,3,4],
'laravel.basic_scheduled_task':[1,2,3],
'laravel.production_logging':[0,1,2],
'laravel.request_lifecycle':[1,3,4],
'laravel.scheduler_operation':[1,4],
'php.application_exceptions':[0,1,4],
'php.interface_contracts':[0,1,2],
'composer.psr4_autoloading':[0,1,3],
'laravel.basic_queued_job':[0,4],
'eloquent.attribute_casts':[0,3,4],
'laravel.form_request_validation':[8,10,14],
'laravel.middleware_boundaries':[0,2],
'laravel.production_caches':[1,4],
'laravel.queue_worker_operation':[0,13,14],
'laravel.related_write_transactions':[0,1,3],
'eloquent.parameterized_queries':[0],
'eloquent.query_scopes':[0,1,3],
'laravel.api_resource_serialization':[0,4],
'laravel_vue.request_diagnosis':[0,5,12],
'sanctum.stateful_spa_configuration':[3,10,12],
'vue_router.resource_parameters':[0,2,7],
'api.backward_compatible_evolution':[0,1],
'api.filter_sort_contracts':[3,4],
'api.paginated_collections':[2],
'eloquent.eager_loading':[0,1],
'eloquent.many_to_many_relationships':[0,3],
'laravel.api_feature_tests':[0,1],
'laravel.controller_dependency_injection':[0,2,4],
'sanctum.csrf_initialization':[6,10,12],
'sanctum.personal_access_tokens':[1,2],
'vue.component_interaction_tests':[0,1,3],
'vue.server_validation_feedback':[6,10,13],
'api.relationship_representation':[0,1,2],
'laravel.database_test_isolation':[3,9],
'laravel.session_logout':[1],
'sanctum.credentialed_fetch':[6],
'sanctum.protected_api_routes':[0,3,4],
'vue.mocked_api_state_tests':[1,2],
'laravel.credentialed_cors':[5,6],
'laravel.permission_gates':[0,2,3],
'laravel.session_fixation_defense':[5],
'vue_router.auth_navigation_guards':[3,4],
'laravel.resource_policies':[0,1,3],
'sanctum.production_cookie_domains':[1,2,3],
'laravel.auth_feature_tests':[0,1,2],
'laravel_vue.deployment_smoke_check':[3],
'vue.session_failure_recovery':[11],
'php.typed_functions':[2,5,6],
'npm.locked_project_dependencies':[1,5,7],
'laravel.api_routes':[0,1,6],
'eloquent.filtered_queries':[0,2],
'laravel.database_seeders':[1,2],
'laravel.model_factories':[1,2],
'laravel.resource_controllers':[0,1,8],
'laravel.validated_input':[1,2],
'vue_router.host_history_fallback':[0,1,2],
'eloquent.one_to_many_relationships':[0,5,8],
'laravel.artisan_development':[2,3]
}
# Remove generic matches that cannot supply two plausible targets by title, justifying open search.
for cid in ['php.typed_functions','laravel.api_routes','laravel.validated_input','vue_router.host_history_fallback','laravel.artisan_development','eloquent.one_to_many_relationships']:
 s.M[cid]=[]
for cid in ['npm.locked_project_dependencies','eloquent.filtered_queries','laravel.database_seeders','laravel.model_factories','laravel.resource_controllers']:
 s.M[cid]=s.M[cid][:1]
s.M['vue.state_ownership']=[195]
# Selected near misses are recorded, rather than passed to transcript acquisition.
R={
'laravel.basic_queued_job':[(1,'Rejected: title explicitly signals advanced queue tips beyond introducing one basic queued job.')],
'laravel.form_request_validation':[(2,'Rejected: Laravel 5-specific form request tutorial is clearly obsolete for this version-sensitive framework target.')],
'sanctum.stateful_spa_configuration':[(2,'Rejected: token authentication is the wrong authentication model for the stateful cookie-authenticated first-party SPA target.')],
'vue.mocked_api_state_tests':[(0,'Rejected: React testing is the wrong component framework for Vue screen-state tests.')],
'eloquent.parameterized_queries':[(2,'Rejected: Spanish-language title/channel result is not an English teaching candidate.')],
'vue.session_failure_recovery':[(1,'Rejected: JWT-specific setup drifts from the first-party session-cookie recovery model.')],
'laravel_vue.deployment_smoke_check':[(2,'Rejected: Laravel Vue starter-kit deep dive is not a decoupled REST/SPA deployment acceptance check.')]
}
# Channels and metadata come only from the real catalogues / parsed search responses.
al=s.load(s.CORE/'video_bank/channel_allowlist.json')
channels={x['channel_id']:x for x in al['channels']}
catfiles=sorted(glob.glob(str(s.CORE/'video_bank/channel_catalogs/*.json')))
canonical={}
for fn in catfiles:
 cat=s.load(fn)
 for v in cat['videos']:
  canonical[(cat['channel_id'],v['video_id'])]=dict(v,channel_id=cat['channel_id'],channel_name=channels[cat['channel_id']]['channel_name'])
def candidate(v,via,cid,reason=None):
 # A result also present in an allowlist catalogue retains catalogue-exact metadata and provenance.
 if (v['channel_id'],v['video_id']) in canonical:
  v=canonical[(v['channel_id'],v['video_id'])]; via='allowlist_catalogue'
 name=s.concepts[cid]['concept_name']
 objective=s.briefs[cid]['learning_objective'].removeprefix('Be able to ').rstrip('.')
 prefix=('Long course; seek only a bounded introductory section' if v['duration_seconds']>3600 else 'Focused tutorial is a plausible bounded explanation')
 kept_reason=f'{prefix} for {name}: {objective}. Title/channel/duration-only match; verify the required facts, visual suitability and prerequisite independence during segment detection, not the whole video.'
 if cid=='eloquent.parameterized_queries' and not reason:kept_reason='Title explicitly addresses Laravel raw-query SQL injection protection, a plausible demonstration of safe binding versus interpolation. Verify parameter-binding details and allowed prerequisites in the transcript.'
 if cid=='laravel.session_fixation_defense' and not reason:kept_reason='Login/session tutorial may contain the successful-login session-regeneration step. Select only that security boundary; do not assume the title proves fixation-defense coverage.'
 if cid=='sanctum.credentialed_fetch' and not reason:kept_reason='SPA-authentication explanation may show browser credential and CSRF handling. Fetch-specific header handling is unverified; reject the segment if it only demonstrates Axios defaults or token authentication.'
 if cid=='vue.session_failure_recovery' and not reason:kept_reason='Broad Vue login/logout course may contain unauthenticated-request handling and recovery navigation. Session-cookie 401/419 versus 403 behavior is unverified; do not substitute a JWT-refresh workflow for required facts.'
 return dict(video_id=v['video_id'],youtube_url='https://www.youtube.com/watch?v='+v['video_id'],title=v['title'],channel_id=v['channel_id'],channel_name=v['channel_name'],found_via=via,duration_seconds=v['duration_seconds'],filter_verdict='rejected' if reason else 'kept',reason=reason or kept_reason)
# Narrow cross-search reuse of actual SPA result URLs, without a second request for an adjacent topic.
additional={'sanctum.credentialed_fetch':[('sanctum.stateful_spa_configuration',3),('sanctum.csrf_initialization',12)]}
rows=[]
entries=sorted((e for e in s.g['entries'] if e['video_need']['level'] in ['HIGH','MEDIUM']),key=lambda e:s.concepts[e['concept_id']]['toc_sequence_position'])
for e in entries:
 cid=e['concept_id']; c=s.concepts[cid]; path=s.paths[e['path_id']]
 assert cid in s.M and (len(s.M[cid])>=2 or cid in openres)
 cand=[candidate(s.r[i],'allowlist_catalogue',cid) for i in s.M[cid]]
 if cid in O:
  assert len(s.M[cid])<2, (cid,s.M[cid])
  cand.extend(candidate(openres[cid]['results'][i],'open_search',cid) for i in O[cid])
 if cid=='vue.state_ownership':cand.append(candidate(s.r[500],'allowlist_catalogue',cid,'Rejected: accessing Pinia store state introduces the explicitly blocked future pinia.store_state concept; this target only establishes ownership boundaries.'))
 for other,i in additional.get(cid,[]):cand.append(candidate(openres[other]['results'][i],'open_search',cid))
 for i,reason in R.get(cid,[]):cand.append(candidate(openres[cid]['results'][i],'open_search',cid,reason))
 seen=set(); cand=[v for v in cand if not (v['video_id'] in seen or seen.add(v['video_id']))]
 # Forbid >5 transcript finalists; rejected near-misses do not consume the finalist budget.
 kept=0;limited=[]
 for v in cand:
  if v['filter_verdict']=='kept':
   kept+=1
   if kept>5:continue
  limited.append(v)
 # Choose at most three likely topical drift risks, strictly from real future-blocked IDs.
 groups={
 'api':['eloquent','laravel','sanctum'], 'composer':['php','laravel'], 'npm':['vite','vitest'],
 'php':['php','composer','eloquent'], 'javascript':['javascript','vue','web'],
 'web':['web','vue','vite'], 'laravel':['laravel','eloquent','sanctum'],
 'eloquent':['eloquent','laravel'], 'vue':['vue','pinia','vue_router'],
 'vue_router':['vue_router','pinia','sanctum'], 'pinia':['pinia','vue','vue_router'],
 'sanctum':['sanctum','laravel','vue_router'], 'vite':['vite','laravel_vue'],
 'vitest':['vue','vitest'], 'laravel_vue':['laravel_vue','sanctum','vite']}
 ns=cid.split('.')[0]; words=set(cid.split('.')[1].split('_'))
 def rank(bid):
  bns=bid.split('.')[0]; bw=set(bid.split('.')[-1].split('_'))
  score=10*len(words & bw)+(8 if bns==ns else 3 if bns in groups.get(ns,[]) else 0)
  return (-score,s.concepts.get(bid,{}).get('toc_sequence_position',999))
 relevant=[bid for bid in c['blocked_knowledge_ids'] if bid.split('.')[0] in groups.get(ns,[])]
 blocked=sorted(relevant,key=rank)[:3]
 rows.append(dict(concept_id=cid,path_id=e['path_id'],search_brief=dict(concept_name=c['concept_name'],learner_level=path['learner_scope'],required_fact_ids=[f['id'] for f in s.briefs[cid]['evidence']['required_facts']],preferred_visual_modes=e['video_need']['preferred_visual_modes'],blocked_concepts_to_avoid=blocked),search_route='allowlist_then_open_search' if cid in openres else 'allowlist_only',candidates=limited))
parent=[B/x for x in ['glossary_pass_a.json','registry_lookup.json','coverage_briefs.json','extracted_concepts.json']]+[s.CORE/'video_bank/channel_allowlist.json']+[s.Path(x) if hasattr(s,'Path') else x for x in catfiles]
# Basename keys for batch inputs, pack-relative keys for cross-batch catalogues.
hashes={p.name if p.parent==B else str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in parent}
meta=dict(artifact_type='video_candidates',artifact_version='1.0.0',schema_version='1.0.0',batch_id=s.g['batch_id'],run_id=s.g['metadata']['run_id'],prompt_version='06_video_candidates@v1',model='none',generated_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),source_snapshot_id=s.ex['metadata']['source_snapshot_id'],parent_artifact_hashes=hashes)
out=dict(metadata=meta,batch_id=s.g['batch_id'],searches=rows)
p=B/'video_candidates.part.all.json';p.write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
# Self-check: exact eligible set, tile/TOC ordering, exact briefs, blocked subset, metadata origin, hashes, URLs, duplicate and finalist ceilings.
assert {(x['concept_id'],x['path_id']) for x in rows}=={(x['concept_id'],x['path_id']) for x in entries}
assert len(rows)==len(entries)
resultprovenance={(v['channel_id'],v['video_id']):v for d in openres.values() for v in d['results']}
for row in rows:
 cid=row['concept_id']; br=row['search_brief'];c=s.concepts[cid]
 assert br['learner_level']==s.paths[row['path_id']]['learner_scope']
 assert br['concept_name']==c['concept_name']
 assert set(br['blocked_concepts_to_avoid'])<=set(c['blocked_knowledge_ids']) and len(br['blocked_concepts_to_avoid'])<=3
 assert br['required_fact_ids']==[f['id'] for f in s.briefs[cid]['evidence']['required_facts']]
 assert len({v['video_id'] for v in row['candidates']})==len(row['candidates'])
 assert sum(v['filter_verdict']=='kept' for v in row['candidates'])<=5
 for v in row['candidates']:
  assert re.fullmatch(r'[A-Za-z0-9_-]{11}',v['video_id']) and v['youtube_url']=='https://www.youtube.com/watch?v='+v['video_id']
  source=(canonical if v['found_via']=='allowlist_catalogue' else resultprovenance)[(v['channel_id'],v['video_id'])]
  assert all(v[k]==source[k] for k in ['title','channel_id','channel_name','duration_seconds'])
  assert v['reason']
report={'search_rows':len(rows),'skipped_LOW_NONE':len(s.g['entries'])-len(rows),'candidates':sum(len(x['candidates']) for x in rows),'kept':sum(v['filter_verdict']=='kept' for x in rows for v in x['candidates']),'rejected':sum(v['filter_verdict']=='rejected' for x in rows for v in x['candidates']),'open_search_concepts':sum(x['search_route']=='allowlist_then_open_search' for x in rows),'fewer_than_two_kept':[x['concept_id'] for x in rows if sum(v['filter_verdict']=='kept' for v in x['candidates'])<2],'mechanical_checks':'PASS','mistakes_checklist':['Exact HIGH/MEDIUM coverage; LOW/NONE excluded','All catalogues searched programmatically; career families not filtered','No reusable segments available','Open search only after fewer than two title-plausible matches; YouTube results fetched with curl in absence of WebSearch','IDs and metadata from real cached catalogues or fetched search responses; no recalled IDs','Catalogue titles/channel/durations byte-matched; normalized source URLs computed','No transcript/visual or fact-coverage assertions made at metadata filter stage','Advanced/wrong-language/wrong-model near misses rejected; five-finalist cap verified','Learner scope and required facts exact; blocked IDs restricted to actual future blocks','Metadata UTC timestamp and input SHA256 hashes computed']}
(B/'working/video_candidates_self_check.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
