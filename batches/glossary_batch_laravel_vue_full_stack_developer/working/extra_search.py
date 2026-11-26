import build_video_candidates as s
import concurrent.futures,json
extra={
'sanctum.credentialed_fetch':'Laravel Sanctum fetch API authentication credentials include',
'vue.session_failure_recovery':'Vue authentication handle 401 unauthorized logout',
'php.typed_functions':'PHP 8 function parameter return type declarations tutorial',
'npm.locked_project_dependencies':'npm ci package-lock npm install explained',
'laravel.api_routes':'Laravel 12 API routes tutorial',
'eloquent.filtered_queries':'Laravel Eloquent where orderBy queries tutorial',
'laravel.database_seeders':'Laravel database seeders tutorial',
'laravel.model_factories':'Laravel model factories tutorial',
'laravel.resource_controllers':'Laravel API resource controller tutorial',
'laravel.validated_input':'Laravel validated safe input request tutorial',
'vue_router.host_history_fallback':'Vue Router history mode deployment server fallback',
'eloquent.one_to_many_relationships':'Laravel one to many hasMany belongsTo tutorial',
'laravel.artisan_development':'Laravel Artisan commands make controller tutorial'
}
# Keep the first search in provenance if a query has already been made.
d=s.load(s.B/'working/open_search_results.json')
for cid in extra:
 f=s.B/'working'/('search_'+cid+'.html')
 if f.exists(): f.rename(s.B/'working'/('search_initial_'+cid+'.html'))
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
 for cid,res in pool.map(s.search,extra.items()):
  d[cid]=res
  print('\n'+cid)
  for i,v in enumerate(res['results'][:9]):print(i,v['channel_name'],v['duration_seconds'],v['title'])
(s.B/'working/open_search_results.json').write_text(json.dumps(d,indent=2))
