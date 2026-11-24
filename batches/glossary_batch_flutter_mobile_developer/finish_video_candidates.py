import sys,json,re,glob,hashlib,datetime
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from build_video_candidates import P,W,G,E,B,R,C,BR,V,M,Q,fetch
plan=json.loads((W/'video_selection_plan.json').read_text());plan['project_iteration']=[0,1]
# Related concepts commonly introduced by instructional videos on these topics.
risk_groups=[
['project_iteration','widget_composition','stateless_build','state_lifecycle','local_set_state'],
['analyzer_diagnostics','null_safety','exceptions','flutter_runtime_errors','future_results'],
['expressions','conditionals','null_safety','functions','classes'],
['functions','callbacks','interfaces','future_results','async_await'],
['classes','interfaces','json_model_mapping','repository_boundary'],
['widget_composition','stateless_build','widget_element_identity','state_lifecycle','local_set_state','reusable_widgets'],
['layout_constraints','linear_layout','flexible_layout','layered_layout','scrolling_layout','responsive_layout'],
['material_theming','responsive_layout','text_scaling','semantic_labels','interaction_targets'],
['widget_inspector','profile_frame_investigation','unnecessary_rebuilds','resource_lifetime_leaks'],
['typed_collections','iteration','callbacks','json_model_mapping','interfaces'],
['widget_element_identity','list_item_keys','state_lifecycle','provider_lifetime','stream_subscriptions'],
['state_lifecycle','local_set_state','state_ownership','change_notifier_updates','provider_scope','provider_subscription','provider_lifetime'],
['reusable_widgets','form_validation','state_ownership','rest_client_calls','request_state_model'],
['app_responsibility_boundaries','repository_boundary','widget_test_harness','widget_find_assert','widget_test_interaction','async_test_control'],
['exceptions','flutter_runtime_errors','future_results','async_await','stream_subscriptions'],
['rest_client_calls','json_model_mapping','request_state_model','mounted_async_updates','request_recovery','stale_request_results','repository_boundary','async_test_control'],
['navigator_stack','screen_arguments','screen_results','go_router_routes','route_parameters','invalid_routes','deep_link_entry','system_back','auth_route_access'],
['mobile_integration_tests','android_signed_bundle','ios_distribution_build','review_readiness'],
['compatible_dependencies','plugin_configuration','platform_permission_declarations','runtime_permission_request','permission_denial','device_capability_availability','supplied_native_call','platform_channel_errors'],
['supplied_native_call','platform_channel_errors','local_file_io','device_capability_availability'],
['local_file_io','secure_local_storage','local_database_schema','local_database_create','local_database_read','local_database_update','local_database_delete','local_schema_migration','persistence_failures','local_data_lifetime'],
['stream_subscriptions','flutterfire_initialization','firebase_auth_actions','firebase_auth_session','auth_route_access','firestore_documents','service_access_failures','local_data_lifetime'],
['foreground_notifications','notification_open_navigation','deep_link_entry','auth_route_access','privacy_aware_analytics'],
['profile_frame_investigation','unnecessary_rebuilds','bounded_rebuild_fix','resource_lifetime_leaks','stream_subscriptions'],
['application_identifiers','build_environments','android_signed_bundle','ios_distribution_build','review_readiness','store_submission']]
suffix_ids={k.split('.')[-1]:k for k in C}
def blocked(c):
 s=c['concept_id'].split('.')[-1]; choices=[]
 for group in risk_groups:
  if s in group:
   # Nearest related targets are the most likely instructional drift.
   choices.extend(sorted(group,key=lambda t:abs(group.index(t)-group.index(s))))
 result=[]
 for t in choices:
  k=suffix_ids.get(t)
  if k in c['blocked_knowledge_ids'] and k not in result:result.append(k)
  if len(result)==4:break
 return result
source_catalogs={};allow=json.loads(Path('00_GLOSSARY_PIPELINE_CORE/video_bank/channel_allowlist.json').read_text());names={x['channel_id']:x['channel_name'] for x in allow['channels']}
for f in sorted(glob.glob('00_GLOSSARY_PIPELINE_CORE/video_bank/channel_catalogs/*.json')):
 d=json.loads(Path(f).read_text())
 for v in d['videos']:source_catalogs[(d['channel_id'],v['video_id'])]=(v,f)
assert not any(x['reusable_segment_ids'] for x in R['lookups']), 'Reusable segments require first-route inspection.'
provenance={}; searches=[]; empty=[]
for entry in G['entries']:
 if entry['video_need']['level'] not in ['HIGH','MEDIUM']:continue
 cid=entry['concept_id'];suffix=cid.split('.')[-1];c=C[cid];candidates=[];seen=set()
 def add(v,via,verdict='kept',reason=None):
  if v['video_id'] in seen:return
  if verdict=='kept' and sum(x['filter_verdict']=='kept' for x in candidates)>=5:return
  seen.add(v['video_id'])
  if reason is None:
   reason=(f"Title-level match for {c['concept_name']}: '{v['title']}' on {v['channel_name']} ({v['duration_seconds']}s). "
       + ('A broad beginner course is only a fallback source for a focused cut, not a recommendation to watch the whole course. ' if 'Full Course' in v['title'] or 'Full Tutorial' in v['title'] else '')
       + 'Plausible instructional candidate; exact fact coverage, prerequisite boundaries and visual teaching must be verified from the transcript at the segment stages.')
  candidates.append({k:v[k] for k in ['video_id','title','channel_id','channel_name','duration_seconds']} | {'youtube_url':'https://www.youtube.com/watch?v='+v['video_id'],'found_via':via,'filter_verdict':verdict,'reason':reason})
 for idx in M[suffix]:add(V[idx],'allowlist_catalogue')
 route='allowlist_only'
 if len(M[suffix])<2:
  route='allowlist_then_open_search';spec=plan[suffix]
  if isinstance(spec,list):spec={'keep':spec}
  q=spec.get('query',Q[suffix]);_,d=fetch(q)
  provenance[cid]={'catalogue_plausible_count':len(M[suffix]),'queries':[d]}
  for idx in spec.get('keep',[]):
   if idx>=len(d['results']):raise ValueError((cid,q,idx,'missing result'))
   add(d['results'][idx],'open_search')
  for idx,why in spec.get('reject',{}).items():
   if int(idx)<len(d['results']):add(d['results'][int(idx)],'open_search','rejected',why)
  if 'extra_query' in spec:
   _,d2=fetch(spec['extra_query']);provenance[cid]['queries'].append(d2)
   for idx in spec.get('extra_keep',[]):add(d2['results'][idx],'open_search')
  # Record the earlier fallback result sets when a narrower query was necessary.
  if q!=Q[suffix]:
   cache=W/('search_'+hashlib.sha256(Q[suffix].encode()).hexdigest()[:16]+'.json')
   if cache.exists():provenance[cid]['queries'].insert(0,json.loads(cache.read_text()))
 if not any(x['filter_verdict']=='kept' for x in candidates):empty.append(cid)
 path=next(x for x in E['paths'] if x['path_id']==entry['path_id'])
 searches.append({'concept_id':cid,'path_id':entry['path_id'],'search_brief':{'concept_name':c['concept_name'],'learner_level':path['learner_scope'],'required_fact_ids':[x['id'] for x in BR[cid]['evidence']['required_facts']], 'preferred_visual_modes':entry['video_need']['preferred_visual_modes'],'blocked_concepts_to_avoid':blocked(c)},'search_route':route,'candidates':candidates})
inputs=[str(P/n) for n in ['glossary_pass_a.json','registry_lookup.json','extracted_concepts.json','coverage_briefs.json']]+['00_GLOSSARY_PIPELINE_CORE/video_bank/channel_allowlist.json']+sorted(glob.glob('00_GLOSSARY_PIPELINE_CORE/video_bank/channel_catalogs/*.json'))
hashes={(Path(f).name if f.startswith(str(P)+'/') else f):hashlib.sha256(Path(f).read_bytes()).hexdigest() for f in inputs}
meta=dict(G['metadata']);meta.update(artifact_type='video_candidates',artifact_version='1.0.0',schema_version='1.0.0',model='none',prompt_version='06_video_candidates@v1',generated_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),parent_artifact_hashes=hashes)
out={'metadata':meta,'batch_id':P.name,'searches':searches};target=P/'video_candidates.part.all.json';target.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
# Generator mistakes checklist: exact eligibility, unique ids/URLs, title byte matches,
# <=5 kept, route gate, all required facts, learner_scope, modes and blocked references.
expected={(e['concept_id'],e['path_id']) for e in G['entries'] if e['video_need']['level'] in ['HIGH','MEDIUM']}
assert len(searches)==len(expected) and {(s['concept_id'],s['path_id']) for s in searches}==expected
for s in searches:
 cid=s['concept_id'];c=C[cid];b=s['search_brief'];entry=next(e for e in G['entries'] if e['concept_id']==cid)
 assert b['concept_name']==c['concept_name']
 assert b['required_fact_ids']==[f['id'] for f in BR[cid]['evidence']['required_facts']]
 assert b['preferred_visual_modes']==entry['video_need']['preferred_visual_modes']
 assert set(b['blocked_concepts_to_avoid'])<=set(c['blocked_knowledge_ids']) and len(b['blocked_concepts_to_avoid'])<=4
 assert len({v['video_id'] for v in s['candidates']})==len(s['candidates'])
 assert sum(v['filter_verdict']=='kept' for v in s['candidates'])<=5
 if s['search_route']=='allowlist_then_open_search':assert len(M[cid.split('.')[-1]])<2
 for v in s['candidates']:
  assert v['youtube_url']=='https://www.youtube.com/watch?v='+v['video_id'] and v['reason'].strip()
  assert re.fullmatch(r'[A-Za-z0-9_-]{11}',v['video_id'])
  if v['found_via']=='allowlist_catalogue':
   original,_=source_catalogs[(v['channel_id'],v['video_id'])]
   assert all(v[k]==original[k] for k in ['video_id','title','duration_seconds'])
   assert v['channel_name']==names[v['channel_id']]
  else:
   origins=[r for q in provenance[cid]['queries'] for r in q['results'] if r['video_id']==v['video_id']]
   assert origins and any(all(v[k]==o[k] for k in ['title','duration_seconds','channel_id','channel_name']) and o['result_url']==v['youtube_url'] for o in origins)
report={'search_rows':len(searches),'candidate_rows':sum(len(s['candidates']) for s in searches),'kept':sum(v['filter_verdict']=='kept' for s in searches for v in s['candidates']),'rejected':sum(v['filter_verdict']=='rejected' for s in searches for v in s['candidates']),'no_kept_candidates':empty,'self_check':'PASS','open_search_provenance':provenance}
(W/'video_candidates_self_check.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='open_search_provenance'},indent=2))
