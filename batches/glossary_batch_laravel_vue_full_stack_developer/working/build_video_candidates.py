import json, glob, re, hashlib, datetime, subprocess, concurrent.futures, urllib.parse
from pathlib import Path
B=Path('batches/glossary_batch_laravel_vue_full_stack_developer'); CORE=Path('00_GLOSSARY_PIPELINE_CORE')
def load(p): return json.loads(Path(p).read_text())
g=load(B/'glossary_pass_a.json'); ex=load(B/'extracted_concepts.json'); cv=load(B/'coverage_briefs.json'); reg=load(B/'registry_lookup.json')
assert not any(r['reusable_segment_ids'] for r in reg['lookups'])
concepts={c['concept_id']:c for c in ex['concepts']}; briefs={c['concept_id']:c for c in cv['briefs']}; paths={p['path_id']:p for p in ex['paths']}
r=load(B/'working/video_catalog_matches.json')
# Curated title-only matches; adjacent targets reuse broad courses only where the title plausibly supports that target.
M={
'api.crud_endpoint_contracts':[35,36,37,773],
'composer.locked_dependencies':[],
'javascript.application_data':[1013,1073,1075],
'npm.locked_project_dependencies':[54,299,564],
'php.application_values_and_types':[98,149,10],
'web.html_markup_authoring':[1070,1002,1108],
'javascript.application_conditionals':[990],
'javascript.application_functions':[1074,1017,1032],
'laravel.artisan_development':[9,18,482],
'php.application_arrays':[97,139,140],
'php.application_operators':[144,148,94],
'web.css_rule_styling':[1067,1068,1001],
'web.semantic_application_forms':[1069,1051,1018],
'javascript.application_arrays':[993,1048,1053],
'javascript.async_request_flow':[1008,1056,1054],
'laravel.phpunit_execution':[],
'laravel.production_configuration':[],
'php.application_conditionals':[94,145,143],
'php.typed_functions':[135,95],
'laravel.basic_scheduled_task':[],
'laravel.production_logging':[],
'php.application_classes':[76,10,17],
'php.foreach_iteration':[96,964],
'vitest.vue_test_execution':[379,375],
'vue.single_file_components':[224,199,6],
'web.fetch_json_wrapper':[56,318,563],
'laravel.request_lifecycle':[],
'laravel.scheduler_operation':[],
'laravel.schema_migrations':[475,9,18],
'php.application_exceptions':[],
'php.interface_contracts':[],
'vite.spa_dev_server':[273,279],
'vue.lifecycle_cleanup':[167,181],
'vue.reactive_state':[175,176,552],
'vue_router.route_navigation':[554,516],
'web.fetch_response_failures':[318,280,56],
'composer.psr4_autoloading':[],
'eloquent.application_crud':[474,9,18],
'laravel.api_routes':[9,18],
'laravel.basic_queued_job':[],
'vue.computed_derivations':[171,205,204],
'vue.stateful_composables':[163,551],
'vue.template_bindings':[223,221,218],
'eloquent.attribute_casts':[],
'eloquent.filtered_queries':[474,9],
'laravel.database_seeders':[472,9],
'laravel.form_request_validation':[],
'laravel.middleware_boundaries':[422],
'laravel.model_factories':[473,9],
'laravel.production_caches':[],
'laravel.queue_worker_operation':[],
'laravel.related_write_transactions':[],
'laravel.route_model_binding':[460,9],
'vite.api_development_connectivity':[273,279],
'vite.spa_production_build':[273,279],
'vue.bounded_watchers':[169,170,200],
'vue.component_event_handlers':[210,211,173],
'vue.component_props':[165,198,197],
'vue.conditional_rendering':[216,217],
'vue.keyed_list_rendering':[214,215],
'vue.safe_html_rendering':[222,223],
'eloquent.one_to_many_relationships':[466,467],
'eloquent.parameterized_queries':[],
'eloquent.query_scopes':[],
'laravel.api_resource_serialization':[],
'laravel.resource_controllers':[470,9],
'laravel.validated_input':[464,463],
'laravel_vue.request_diagnosis':[],
'sanctum.stateful_spa_configuration':[],
'vue.async_screen_states':[511,513,506],
'vue.component_emits':[164,193,194],
'vue.form_input_binding':[172,208,209],
'vue_router.host_history_fallback':[162,504],
'vue_router.resource_parameters':[554],
'api.backward_compatible_evolution':[],
'api.filter_sort_contracts':[],
'api.paginated_collections':[468],
'eloquent.eager_loading':[],
'eloquent.many_to_many_relationships':[],
'laravel.api_feature_tests':[],
'laravel.controller_dependency_injection':[],
'laravel.session_login':[417,419],
'sanctum.csrf_initialization':[],
'sanctum.personal_access_tokens':[],
'vue.component_interaction_tests':[],
'vue.server_validation_feedback':[],
'vue.state_ownership':[195,500],
'api.relationship_representation':[],
'laravel.database_test_isolation':[],
'laravel.session_logout':[418],
'pinia.store_state':[500,501,494],
'sanctum.credentialed_fetch':[],
'sanctum.protected_api_routes':[],
'vue.mocked_api_state_tests':[],
'laravel.credentialed_cors':[],
'laravel.permission_gates':[],
'laravel.session_fixation_defense':[417],
'pinia.store_actions':[498,496,495],
'vue_router.auth_navigation_guards':[],
'laravel.resource_policies':[],
'sanctum.production_cookie_domains':[],
'vue.mutation_screen_synchronization':[182,507],
'laravel.auth_feature_tests':[],
'laravel_vue.deployment_smoke_check':[],
'vue.session_failure_recovery':[]
}
# Narrow searches for concepts not supported by two credible catalogue titles.
Q={
'composer.locked_dependencies':'PHP Composer install update composer.lock tutorial',
'javascript.application_conditionals':'JavaScript if else strict equality tutorial',
'laravel.phpunit_execution':'Laravel PHPUnit run tests artisan test tutorial',
'laravel.production_configuration':'Laravel production deployment environment configuration tutorial',
'laravel.basic_scheduled_task':'Laravel 11 scheduled tasks tutorial',
'laravel.production_logging':'Laravel logging tutorial log context',
'laravel.request_lifecycle':'Laravel request lifecycle explained tutorial',
'laravel.scheduler_operation':'Laravel scheduler cron schedule run tutorial',
'php.application_exceptions':'PHP exceptions try catch finally tutorial',
'php.interface_contracts':'PHP interfaces implements tutorial',
'composer.psr4_autoloading':'PHP Composer PSR-4 autoloading tutorial',
'laravel.basic_queued_job':'Laravel 11 queues jobs tutorial',
'eloquent.attribute_casts':'Laravel Eloquent attribute casts tutorial',
'laravel.form_request_validation':'Laravel form request validation tutorial',
'laravel.middleware_boundaries':'Laravel 11 middleware tutorial',
'laravel.production_caches':'Laravel production config cache route cache tutorial',
'laravel.queue_worker_operation':'Laravel queue worker supervisor deployment tutorial',
'laravel.related_write_transactions':'Laravel database transactions tutorial',
'eloquent.parameterized_queries':'Laravel query builder parameter binding SQL injection tutorial',
'eloquent.query_scopes':'Laravel Eloquent query scopes tutorial',
'laravel.api_resource_serialization':'Laravel API resources serialization tutorial',
'laravel_vue.request_diagnosis':'Laravel Vue API debugging network requests tutorial',
'sanctum.stateful_spa_configuration':'Laravel 11 Sanctum SPA authentication Vue tutorial',
'vue_router.resource_parameters':'Vue Router 4 dynamic route params tutorial',
'api.backward_compatible_evolution':'REST API versioning backwards compatibility tutorial',
'api.filter_sort_contracts':'REST API filtering sorting query parameters tutorial',
'api.paginated_collections':'Laravel API pagination resources tutorial',
'eloquent.eager_loading':'Laravel eager loading N+1 tutorial',
'eloquent.many_to_many_relationships':'Laravel many to many relationship pivot tutorial',
'laravel.api_feature_tests':'Laravel API feature tests assertJson tutorial',
'laravel.controller_dependency_injection':'Laravel dependency injection controller service container tutorial',
'sanctum.csrf_initialization':'Laravel Sanctum SPA csrf cookie authentication tutorial',
'sanctum.personal_access_tokens':'Laravel 11 Sanctum API token authentication tutorial',
'vue.component_interaction_tests':'Vue 3 Vitest Vue Test Utils component testing tutorial',
'vue.server_validation_feedback':'Vue Laravel form validation errors 422 tutorial',
'api.relationship_representation':'Laravel API resources relationships whenLoaded tutorial',
'laravel.database_test_isolation':'Laravel RefreshDatabase testing factories tutorial',
'laravel.session_logout':'Laravel session logout invalidate regenerateToken tutorial',
'sanctum.credentialed_fetch':'Laravel Sanctum Vue fetch credentials csrf tutorial',
'sanctum.protected_api_routes':'Laravel 11 Sanctum auth sanctum protected routes tutorial',
'vue.mocked_api_state_tests':'Vue Vitest mock API fetch component testing tutorial',
'laravel.credentialed_cors':'Laravel Sanctum CORS credentials tutorial',
'laravel.permission_gates':'Laravel authorization gates tutorial',
'laravel.session_fixation_defense':'Laravel session authentication regenerate session tutorial',
'vue_router.auth_navigation_guards':'Vue Router 4 authentication navigation guards tutorial',
'laravel.resource_policies':'Laravel authorization policies tutorial',
'sanctum.production_cookie_domains':'Laravel Sanctum SPA subdomains production cookies tutorial',
'laravel.auth_feature_tests':'Laravel test authentication authorization actingAs assertForbidden tutorial',
'laravel_vue.deployment_smoke_check':'Laravel Vue deployment testing API tutorial',
'vue.session_failure_recovery':'Vue Pinia authentication 401 session expired logout tutorial'
}
def text(o):
 if not o:return ''
 return o.get('simpleText','') or ''.join(x.get('text','') for x in o.get('runs',[]))
def walk(o):
 if isinstance(o,dict):
  if 'videoRenderer' in o:yield o['videoRenderer']
  elif 'lockupViewModel' in o:
   v=o['lockupViewModel']; md=v.get('metadata',{}).get('lockupMetadataViewModel',{})
   im=md.get('image',{}).get('decoratedAvatarViewModel',{})
   ch=im.get('rendererContext',{}).get('commandContext',{}).get('onTap',{}).get('innertubeCommand',{}).get('browseEndpoint',{}).get('browseId','')
   name=im.get('a11yLabel','').removeprefix('Go to channel ')
   badges=v.get('contentImage',{}).get('thumbnailViewModel',{}).get('overlays',[])
   duration=''
   for ov in badges:
    for badge in ov.get('thumbnailBottomOverlayViewModel',{}).get('badges',[]):
     st=badge.get('thumbnailBadgeViewModel',{}).get('text','')
     if re.fullmatch(r'\d+(?::\d+){1,2}',st):duration=st
   if v.get('contentType')=='LOCKUP_CONTENT_TYPE_VIDEO':
    yield {'videoId':v['contentId'],'title':{'simpleText':md.get('title',{}).get('content','')},'lengthText':{'simpleText':duration},'ownerText':{'runs':[{'text':name,'navigationEndpoint':{'browseEndpoint':{'browseId':ch}}}]}}

  else:
   for v in o.values():yield from walk(v)
 elif isinstance(o,list):
  for v in o:yield from walk(v)
def search(item):
 cid,q=item; file=B/'working'/('search_'+cid+'.html')
 if not file.exists(): subprocess.run(['curl','-sL','--max-time','35','https://www.youtube.com/results?search_query='+urllib.parse.quote_plus(q),'-o',str(file)])
 html=file.read_text() if file.exists() else ''; found=[]
 mat=re.search(r'(?:var ytInitialData\s*=|window\["ytInitialData"\]\s*=)\s*',html)
 if mat:
  try:data=json.JSONDecoder().raw_decode(html[mat.end():])[0]
  except ValueError:data={}
  for v in walk(data):
   dur=text(v.get('lengthText')); by=v.get('ownerText',v.get('longBylineText',{})); runs=by.get('runs',[])
   chid=next((x.get('navigationEndpoint',{}).get('browseEndpoint',{}).get('browseId','') for x in runs),'')
   if not re.fullmatch(r'\d+(?::\d+){1,2}',dur) or not chid:continue
   sec=0
   for n in dur.split(':'):sec=sec*60+int(n)
   found.append({'video_id':v['videoId'],'title':text(v.get('title')),'channel_id':chid,'channel_name':text(by),'duration_seconds':sec})
 # Preserve actual result URLs alongside parsed metadata as provenance.
 return cid,{'query':q,'result_url':'https://www.youtube.com/results?search_query='+urllib.parse.quote_plus(q),'results':[dict(v,youtube_url='https://www.youtube.com/watch?v='+v['video_id']) for v in found]}
if __name__=='__main__':
 todo=[(cid,Q.get(cid,concepts[cid]['concept_name']+' tutorial')) for cid in M if len(M[cid])<2]
 with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:out=dict(pool.map(search,todo))
 (B/'working/open_search_results.json').write_text(json.dumps(out,indent=2))
 for cid,d in out.items():
  print('\n'+cid)
  for i,v in enumerate(d['results'][:5]):print(i,v['channel_name'],v['duration_seconds'],v['title'])
