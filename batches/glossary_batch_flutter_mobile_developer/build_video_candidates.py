import json,glob,re,hashlib,datetime,urllib.request,urllib.parse,concurrent.futures
from pathlib import Path
P=Path('batches/glossary_batch_flutter_mobile_developer'); W=P/'working'
def load(n):return json.loads((P/n).read_text())
G=load('glossary_pass_a.json'); E=load('extracted_concepts.json'); B=load('coverage_briefs.json'); R=load('registry_lookup.json')
C={x['concept_id']:x for x in E['concepts']}; BR={x['concept_id']:x for x in B['briefs']}
V=load('working/flutter_catalog_matches.json')
# Explicit title-screened catalogue matches, reviewed in TOC tile order.
M={
'project_iteration':[136], 'analyzer_diagnostics':[],
'expressions':[68,13], 'functions':[66,13], 'classes':[62,125],
'widget_composition':[51,49], 'stateless_build':[49,136], 'layout_constraints':[48,43], 'linear_layout':[45,46],
'material_theming':[50], 'widget_inspector':[], 'conditionals':[64,110], 'null_safety':[],
'typed_collections':[60,65,63], 'iteration':[64,40], 'callbacks':[122,66],
'widget_element_identity':[], 'state_lifecycle':[119,41], 'local_set_state':[41,127], 'reusable_widgets':[39,123], 'form_validation':[23,33,34],
'flexible_layout':[43,129], 'layered_layout':[], 'scrolling_layout':[109,155,156], 'responsive_layout':[], 'text_scaling':[], 'semantic_labels':[], 'interaction_targets':[], 'list_item_keys':[],
'state_ownership':[], 'change_notifier_updates':[], 'provider_scope':[100], 'provider_subscription':[100], 'provider_lifetime':[],
'app_responsibility_boundaries':[], 'widget_test_harness':[], 'widget_find_assert':[], 'widget_test_interaction':[],
'exceptions':[114,13], 'flutter_runtime_errors':[], 'future_results':[59,118], 'async_await':[59,118],
'rest_client_calls':[58,116,117], 'json_model_mapping':[115], 'request_state_model':[111,93], 'mounted_async_updates':[], 'request_recovery':[], 'stale_request_results':[],
'interfaces':[61,62,13], 'repository_boundary':[], 'async_test_control':[], 'navigator_stack':[120,154], 'screen_results':[],
'go_router_routes':[], 'route_parameters':[], 'invalid_routes':[], 'deep_link_entry':[], 'system_back':[], 'mobile_integration_tests':[],
'compatible_dependencies':[], 'plugin_configuration':[], 'runtime_permission_request':[], 'permission_denial':[], 'device_capability_availability':[], 'supplied_native_call':[], 'platform_channel_errors':[],
'local_file_io':[], 'secure_local_storage':[], 'local_database_schema':[], 'local_database_create':[], 'local_database_read':[], 'local_database_update':[], 'local_database_delete':[], 'local_schema_migration':[], 'persistence_failures':[],
'stream_subscriptions':[101], 'flutterfire_initialization':[21], 'firebase_auth_actions':[20,24,19], 'firebase_auth_session':[17,18], 'auth_route_access':[], 'firestore_documents':[91,92], 'service_access_failures':[], 'local_data_lifetime':[],
'foreground_notifications':[], 'notification_open_navigation':[], 'privacy_aware_analytics':[], 'profile_frame_investigation':[], 'unnecessary_rebuilds':[], 'bounded_rebuild_fix':[], 'resource_lifetime_leaks':[],
'application_identifiers':[], 'build_environments':[], 'android_signed_bundle':[], 'ios_distribution_build':[], 'review_readiness':[], 'store_submission':[]}
# Search by tile-related topics only after the title-screened reusable/catalogue gate.
Q={
'project_iteration':'Flutter hot reload hot restart tutorial',
'stream_subscriptions':'Dart StreamSubscription listen cancel tutorial',
'analyzer_diagnostics':'Flutter Dart analyzer errors warnings IDE tutorial',
'material_theming':'Flutter Material 3 ThemeData ColorScheme tutorial', 'widget_inspector':'Flutter DevTools widget inspector tutorial',
'null_safety':'Dart null safety nullable types tutorial', 'widget_element_identity':'Flutter widgets elements keys explained',
'layered_layout':'Flutter Stack Positioned tutorial', 'responsive_layout':'Flutter LayoutBuilder MediaQuery responsive layout tutorial',
'text_scaling':'Flutter accessibility text scaling TextScaler tutorial', 'semantic_labels':'Flutter accessibility Semantics widget tutorial', 'interaction_targets':'Flutter accessibility tap target size tutorial', 'list_item_keys':'Flutter keys reorder list state tutorial',
'state_ownership':'Flutter local shared state state management tutorial', 'change_notifier_updates':'Flutter ChangeNotifier notifyListeners tutorial',
'provider_scope':'Flutter Provider ChangeNotifierProvider tutorial', 'provider_subscription':'Flutter Provider Consumer Selector watch tutorial', 'provider_lifetime':'Flutter Provider create value dispose tutorial',
'app_responsibility_boundaries':'Flutter app architecture UI repository service tutorial',
'widget_test_harness':'Flutter widget testing pumpWidget tutorial', 'widget_find_assert':'Flutter widget testing find expect tutorial', 'widget_test_interaction':'Flutter widget testing tap enterText pump tutorial',
'flutter_runtime_errors':'Flutter common runtime errors debugging tutorial', 'json_model_mapping':'Flutter Dart JSON fromJson toJson model tutorial',
'mounted_async_updates':'Flutter mounted setState after dispose async tutorial', 'request_recovery':'Flutter HTTP timeout retry error handling tutorial', 'stale_request_results':'Flutter cancel stale async search requests tutorial',
'repository_boundary':'Flutter repository pattern tutorial', 'async_test_control':'Flutter testing async Completer pump tutorial',
'screen_results':'Flutter Navigator pop return data previous screen tutorial',
'go_router_routes':'Flutter go_router navigation tutorial', 'route_parameters':'Flutter go_router pathParameters queryParameters tutorial', 'invalid_routes':'Flutter go_router errorBuilder unknown route tutorial', 'deep_link_entry':'Flutter go_router deep linking tutorial', 'system_back':'Flutter PopScope Android predictive back tutorial', 'mobile_integration_tests':'Flutter integration_test tutorial',
'compatible_dependencies':'Flutter pubspec dependency version constraints pub outdated tutorial', 'plugin_configuration':'Flutter plugin Android iOS configuration tutorial',
'runtime_permission_request':'Flutter permission_handler request permission tutorial', 'permission_denial':'Flutter permission_handler permanentlyDenied openAppSettings tutorial', 'device_capability_availability':'Flutter camera availableCameras error handling tutorial',
'supplied_native_call':'Flutter MethodChannel invokeMethod native tutorial', 'platform_channel_errors':'Flutter MethodChannel PlatformException MissingPluginException tutorial',
'local_file_io':'Flutter path_provider file read write tutorial', 'secure_local_storage':'Flutter flutter_secure_storage tutorial',
'local_database_schema':'Flutter sqflite SQLite database tutorial', 'local_database_create':'Flutter sqflite SQLite CRUD tutorial', 'local_database_read':'Flutter sqflite SQLite CRUD tutorial', 'local_database_update':'Flutter sqflite SQLite CRUD tutorial', 'local_database_delete':'Flutter sqflite SQLite CRUD tutorial', 'local_schema_migration':'Flutter sqflite database migration onUpgrade tutorial', 'persistence_failures':'Flutter sqflite transaction rollback exception tutorial',
'flutterfire_initialization':'Flutter Firebase initializeApp FlutterFire CLI tutorial', 'auth_route_access':'Flutter go_router Firebase authentication redirect tutorial', 'service_access_failures':'Flutter Firebase permission denied error handling tutorial', 'local_data_lifetime':'Flutter clear local user data logout tutorial',
'foreground_notifications':'Flutter Firebase messaging onMessage foreground notification tutorial', 'notification_open_navigation':'Flutter Firebase messaging getInitialMessage onMessageOpenedApp navigation tutorial', 'privacy_aware_analytics':'Flutter Firebase Analytics consent tutorial',
'profile_frame_investigation':'Flutter DevTools performance profile frames tutorial', 'unnecessary_rebuilds':'Flutter DevTools track widget rebuilds tutorial', 'bounded_rebuild_fix':'Flutter optimize widget rebuilds performance tutorial', 'resource_lifetime_leaks':'Flutter DevTools memory leaks dispose tutorial',
'application_identifiers':'Flutter change applicationId bundle identifier Android iOS tutorial', 'build_environments':'Flutter flavors dart define environment tutorial', 'android_signed_bundle':'Flutter sign Android app bundle release tutorial', 'ios_distribution_build':'Flutter iOS Xcode archive signing TestFlight tutorial', 'review_readiness':'Flutter App Store review test account submission tutorial', 'store_submission':'Flutter publish Google Play App Store tutorial'}
# Shared search results are cached and used by related targets, not repeated network calls.
def text(x):
 if isinstance(x,str):return x
 return x.get('simpleText','') or ''.join(t.get('text','') for t in x.get('runs',[]))
def walk(x):
 if isinstance(x,dict):
  if 'videoRenderer' in x:yield x['videoRenderer']
  for v in x.values():yield from walk(v)
 elif isinstance(x,list):
  for v in x:yield from walk(v)
def fetch(q):
 f=W/('search_'+hashlib.sha256(q.encode()).hexdigest()[:16]+'.json')
 if f.exists():return q,json.loads(f.read_text())
 url='https://www.youtube.com/results?search_query='+urllib.parse.quote_plus(q)
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
  html=urllib.request.urlopen(req,timeout=45).read().decode()
  m=re.search(r'(?:var ytInitialData|window\["ytInitialData"\])\s*=\s*',html)
  if not m:raise ValueError('no ytInitialData')
  data=json.JSONDecoder().raw_decode(html[m.end():])[0]; rows=[]; seen=set()
  for v in walk(data):
   vid=v.get('videoId','');dur=text(v.get('lengthText',{}))
   owner=v.get('ownerText',{}).get('runs',[])
   if not re.fullmatch(r'[\w-]{11}',vid) or vid in seen or not re.fullmatch(r'\d+(?::\d+){1,2}',dur) or not owner:continue
   secs=0
   for t in dur.split(':'):secs=secs*60+int(t)
   cid=owner[0].get('navigationEndpoint',{}).get('browseEndpoint',{}).get('browseId','')
   if not cid:continue
   rows.append(dict(video_id=vid,title=text(v.get('title',{})),channel_id=cid,channel_name=text(v.get('ownerText',{})),duration_seconds=secs,result_url='https://www.youtube.com/watch?v='+vid))
   seen.add(vid)
   if len(rows)>=10:break
  out={'query':q,'search_url':url,'results':rows}
 except Exception as ex:out={'query':q,'search_url':url,'results':[],'error':str(ex)}
 f.write_text(json.dumps(out,indent=2));return q,out
if __name__=='__main__':
 need=[x for x in G['entries'] if x['video_need']['level'] in ['HIGH','MEDIUM']]
 qs=sorted({Q[x['concept_id'].split('.')[-1]] for x in need if len(M[x['concept_id'].split('.')[-1]])<2})
 with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:results=dict(ex.map(fetch,qs))
 for q,d in results.items():
  print('\nQUERY',q)
  for i,v in enumerate(d['results'][:6]):print(i,v['channel_name'],v['duration_seconds'],v['title'])
  if d.get('error'):print('ERROR',d['error'])
