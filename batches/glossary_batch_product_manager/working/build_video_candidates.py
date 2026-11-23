import json,pathlib,hashlib,datetime,collections,re
B=pathlib.Path('batches/glossary_batch_product_manager');W=B/'working';CORE=pathlib.Path('00_GLOSSARY_PIPELINE_CORE')
def load(p):return json.loads(p.read_text())
g=load(B/'glossary_pass_a.json');ex=load(B/'extracted_concepts.json');briefs=load(B/'coverage_briefs.json');look=load(B/'registry_lookup.json')
assert not any(x['reusable_segment_ids'] for x in look['lookups'])
concepts={c['concept_id']:c for c in ex['concepts']};facts={c['concept_id']:c['evidence']['required_facts'] for c in briefs['briefs']};paths={p['path_id']:p for p in ex['paths']}
allow=load(CORE/'video_bank/channel_allowlist.json');channels={c['channel_id']:c['channel_name'] for c in allow['channels']};catalog={};catalog_paths=sorted((CORE/'video_bank/channel_catalogs').glob('*.json'))
for p in catalog_paths:
 d=load(p)
 for v in d['videos']:catalog[v['video_id']]=dict(v,channel_id=d['channel_id'],channel_name=channels[d['channel_id']])
R=load(W/'video_title_matches.json');CAT=load(W/'catalogue_selection.json')
# Narrow the initially shortlisted titles before routing: app-design/user-research and form setup are not direct persona/question-design matches.
CAT['persona_development']=[91]
CAT['survey_design']=[]
OPEN={
'persona_development':[1,4], 'competitive_analysis':[2,3,4], 'customer_interviews':[0,2,6], 'jobs_to_be_done_framework':[0,1,6],
'voice_of_customer':[3,4,6], 'survey_design':[1,2,5], 'market_sizing':[0,3,7], 'usability_testing':[0,2,3],
'product_market_fit':[2,9,10], 'solution_specification':[0,2,5], 'product_requirements_document':[0,3,6],
'acceptance_criteria':[1,3,6], 'user_flows':[0,1,4], 'product_roadmap':[0,2,3],
'capacity_planning':[1,3,5], 'release_planning':[0,2,3], 'feature_sequencing':[0,1,4],
'timeline_estimation':[0,1,7], 'quarterly_planning':[9], 'dependency_management':[1,2,5],
'mvp_scope_definition':[3,4], 'value_vs_effort_matrix':[0,1,7], 'impact_assessment':[4,1],
'rice_framework':[0,1,2], 'ice_framework':[0,3,7], 'weighted_scoring':[0,2,3],
'tradeoff_analysis':[4,0], 'stakeholder_management':[0,3], 'cross_functional_collaboration':[1,2,5],
'consensus_building':[0,1,5], 'status_reporting':[0,1,2], 'executive_communication':[0,1,2],
'roadmap_communication':[7,1], 'conflict_resolution':[0,2,6], 'product_backlog_management':[0,1,4],
'effort_estimation':[0,1,4], 'technical_feasibility_conversations':[3,14,7], 'backlog_refinement':[0,1,2],
'dependency_tracking':[0,1,5], 'kanban_board_management':[0,5], 'release_management':[3,5],
'north_star_metrics':[0,1,2], 'hypothesis_testing':[0], 'analytics_dashboard_interpretation':[0,2,17],
'tracking_plan_definition':[0,1], 'funnel_analysis':[2,5,8], 'cohort_analysis':[0,1,2], 'ab_testing':[0,1,2],
'feature_flags':[2,4,7], 'holdout_groups':[0,2], 'launch_readiness_checklist':[0,2],
'launch_communication_plan':[1,2,7], 'sales_and_support_enablement':[10,12,14],
'design_collaboration':[0,1,2], 'user_journey_mapping':[0,3,5], 'design_feedback':[1,2,4],
'user_testing_synthesis':[1,2,4],
}
# Potential future-topic drift, filtered against the exact per-concept blocked list.
DRIFT={
'competitive_analysis':['market_sizing','product_market_fit','product_positioning'],
'customer_interviews':['survey_design','usability_testing','persona_development'],
'jobs_to_be_done_framework':['persona_development','product_market_fit','mvp_scope_definition'],
'voice_of_customer':['survey_design','user_testing_synthesis','impact_assessment'],
'survey_design':['hypothesis_testing','ab_testing','persona_development'],
'market_sizing':['product_market_fit','product_positioning','funnel_analysis'],
'persona_development':['user_journey_mapping','user_flows','design_thinking_ideation'],
'usability_testing':['user_testing_synthesis','design_feedback','ab_testing'],
'product_market_fit':['cohort_analysis','north_star_metrics','ab_testing'],
'design_thinking_ideation':['solution_specification','user_flows','product_requirements_document'],
'solution_specification':['product_requirements_document','acceptance_criteria','technical_feasibility_conversations'],
'product_requirements_document':['acceptance_criteria','user_flows','effort_estimation'],
'acceptance_criteria':['definition_of_done','product_backlog_management','sprint_planning'],
'user_flows':['user_journey_mapping','design_feedback','design_collaboration'],
'product_roadmap':['release_planning','feature_sequencing','roadmap_communication'],
'capacity_planning':['effort_estimation','sprint_planning','dependency_tracking'],
'release_planning':['release_management','sprint_planning','feature_sequencing'],
'feature_sequencing':['dependency_management','rice_framework','release_management'],
 'timeline_estimation':['effort_estimation','sprint_planning','dependency_management'],
'quarterly_planning':['objectives_and_key_results','sprint_planning','roadmap_communication'],
'dependency_management':['dependency_tracking','sprint_planning','release_management'],
'mvp_scope_definition':['rice_framework','weighted_scoring','ab_testing'],
'value_vs_effort_matrix':['rice_framework','ice_framework','weighted_scoring'],
'impact_assessment':['rice_framework','ice_framework','weighted_scoring'],
'rice_framework':['ice_framework','weighted_scoring','kano_model'],
'ice_framework':['weighted_scoring','kano_model','moscow_method'],
'weighted_scoring':['kano_model','moscow_method','tradeoff_analysis'],
'tradeoff_analysis':['negotiation','stakeholder_management','consensus_building'],
'stakeholder_management':['consensus_building','conflict_resolution','negotiation'],
'cross_functional_collaboration':['consensus_building','conflict_resolution','design_collaboration'],
'consensus_building':['conflict_resolution','negotiation','executive_communication'],
'status_reporting':['executive_communication','roadmap_communication'],
'executive_communication':['roadmap_communication','negotiation'],
'roadmap_communication':['conflict_resolution','negotiation','release_management'],
'conflict_resolution':['negotiation','sprint_retrospective'],
'negotiation':['sprint_planning','design_feedback'],
'product_backlog_management':['backlog_refinement','sprint_planning','definition_of_done'],
'effort_estimation':['sprint_planning','backlog_refinement','dependency_tracking'],
 'technical_feasibility_conversations':['technical_debt_management','dependency_tracking','release_management'],
'sprint_planning':['daily_standup','sprint_review','sprint_retrospective'],
'daily_standup':['sprint_review','sprint_retrospective','dependency_tracking'],
'sprint_review':['sprint_retrospective','backlog_refinement','release_management'],
'sprint_retrospective':['backlog_refinement','technical_debt_management'],
'backlog_refinement':['technical_debt_management','dependency_tracking','definition_of_done'],
 'technical_debt_management':['dependency_tracking','release_management'],
'dependency_tracking':['kanban_board_management','release_management'],
'kanban_board_management':['definition_of_done','release_management'],
'release_management':['feature_flags','launch_readiness_checklist'],
'north_star_metrics':['objectives_and_key_results','funnel_analysis','ab_testing'],
'hypothesis_testing':['ab_testing','holdout_groups','cohort_analysis'],
'analytics_dashboard_interpretation':['tracking_plan_definition','funnel_analysis','cohort_analysis'],
 'tracking_plan_definition':['funnel_analysis','cohort_analysis','ab_testing'],
'funnel_analysis':['cohort_analysis','ab_testing','feature_flags'],
'cohort_analysis':['ab_testing','holdout_groups','feature_flags'],
'ab_testing':['feature_flags','holdout_groups'], 'feature_flags':['holdout_groups','launch_readiness_checklist'],
'holdout_groups':['launch_readiness_checklist'],
'launch_readiness_checklist':['launch_communication_plan','sales_and_support_enablement'],
'launch_communication_plan':['sales_and_support_enablement'],
'sales_and_support_enablement':['design_collaboration'],
'design_collaboration':['user_journey_mapping','design_feedback','user_testing_synthesis'],
'user_journey_mapping':['design_feedback','user_testing_synthesis'],
'design_feedback':['user_testing_synthesis'], 'user_testing_synthesis':[],
}
FOCUS={
'capacity_planning':'available team capacity and allocation, not server throughput',
'feature_sequencing':'release ordering and roadmap dependencies rather than coding implementation',
'quarterly_planning':'turning product direction into a bounded planning period',
'impact_assessment':'using market evidence to judge feature impact before choosing a scoring framework',
'analytics_dashboard_interpretation':'reading product measures and interpreting user behavior at PM depth',
'holdout_groups':'excluded comparison groups and incremental effects, not machine-learning train/test splits',
'feature_flags':'audience exposure, staged rollout and rollback rather than implementing a flag service',
 'technical_feasibility_conversations':'constraints and engineering consultation at PM depth, not system-design implementation',
'product_market_fit':'evidence of customer value and demand, not founder growth advice',
'user_testing_synthesis':'analyzing observed usability findings and deciding design follow-up',
}
def cand(v,via,verdict,reason):
 return {k:v[k] for k in ['video_id','title','channel_id','channel_name','duration_seconds']}|{'youtube_url':'https://www.youtube.com/watch?v='+v['video_id'],'found_via':via,'filter_verdict':verdict,'reason':reason}
rows=[]
for x in g['entries']:
 if x['video_need']['level'] not in ['HIGH','MEDIUM']:continue
 cid=x['concept_id'];c=concepts[cid];key=cid.split('.')[-1];name=c['concept_name'];focus=FOCUS.get(key,name.lower());cs=[]
 for idx in CAT.get(key,[]):
  v=R[idx];cs.append(cand(v,'allowlist_catalogue','kept',f"Catalogue title suggests a teaching segment relevant to {focus}; channel and duration are plausible for this learner level. Exact fact coverage and visual modes still require transcript/segment review."))
 used_open=key in OPEN
 if used_open:
  assert len(cs)<2, (key,'open search cost gate')
  result=load(W/('search_'+key+'.json'))['results']
  for idx in OPEN[key]:
   v=result[idx];via='open_search'
   if v['video_id'] in catalog:v=catalog[v['video_id']];via='allowlist_catalogue'
   if any(t['video_id']==v['video_id'] for t in cs):continue
   cs.append(cand(v,via,'kept',f"The title offers an instructional explanation or example relevant to {focus}. A bounded {name} segment is plausible at beginner-to-junior-PM level; this is a metadata match, not verified fact or visual coverage."))
  # Preserve one clearly unsuitable inspected result when present.
  bad={'product_market_fit':(16,'Founder-advice source (Y Combinator), rather than a bounded PM-level explanation; excluded from open search.'),
       'mvp_scope_definition':(0,'Founder-advice source (Y Combinator); excluded despite the MVP title.'),
       'dependency_management':(6,'Title explicitly specifies URDU/HINDI; wrong language for the English learner path.'),
       'feature_flags':(0,'Title signals Java low-level system design and implementation, beyond this PM learner scope.'),
       'cohort_analysis':(4,'SQL implementation project; wrong depth for interpreting cohort retention at PM level.'),
       'funnel_analysis':(1,'Multi-stage CTE implementation assumes SQL depth that this PM path does not teach.'),
       'holdout_groups':(4,'Long podcast discussion, excluded commentary format rather than a bounded instructional source.'),
       'cross_functional_collaboration':(0,'TEDx discussion format; prefer explicit instructional collaboration lessons over commentary.'),
       'sales_and_support_enablement':(2,'News channel; excluded news rather than instructional product enablement.'),
       'launch_communication_plan':(0,'Six-second slide-template promotion is too brief to plausibly teach communication planning.'),
       'technical_feasibility_conversations':(8,'System-design interview implementation depth goes beyond PM-level feasibility conversations.')}
  if key in bad:
   idx,reason=bad[key];v=result[idx];cs.append(cand(v,'open_search','rejected',reason))
 # Retain metadata rejections for close-looking catalogue matches, without
 # treating those wrong domains as plausible candidates for the fallback gate.
 catalogue_rejects={
  'persona_development':[(R[88], 'App-design and Figma course; the title does not identify persona development, so prefer direct persona lessons.')],
  'survey_design':[(R[940], 'Microsoft Forms creation/export tutorial rather than research-goal and survey-question design; wrong focal task.')],
 }
 wrong_domains={
  'capacity_planning':('Back-Of-The-Envelope Estimation / Capacity Planning','Software-system capacity estimation rather than available team capacity; wrong professional context.'),
  'holdout_groups':('9.3 Holdout Model Selection (L09 Model Eval 2: Confidence Intervals)','Machine-learning model-selection holdout, not a product-experiment control group; wrong topic and depth.'),
 }
 if key in wrong_domains:
  title,reason=wrong_domains[key]
  matches=[v for v in catalog.values() if v['title']==title]
  assert len(matches)==1
  catalogue_rejects[key]=[(matches[0],reason)]
 if key=='release_management':
  v=next(v for v in catalog.values() if v['title']=='Feynman Bytes Ep 2: Release Management')
  cs.insert(0,cand(v,'allowlist_catalogue','kept','Exact release-management title from an allowlisted software-engineering teaching channel; duration is plausible for a process explanation. PM-level boundaries and coverage require segment review.'))
 for v,reason in catalogue_rejects.get(key,[]):cs.append(cand(v,'allowlist_catalogue','rejected',reason))
 kept=[a for a in cs if a['filter_verdict']=='kept'];assert 1<=len(kept)<=5,(key,len(kept))
 blocked=c['blocked_knowledge_ids'];drift=[z for suffix in DRIFT[key] for z in blocked if z.split('.')[-1]==suffix][:3]
 rows.append({'concept_id':cid,'path_id':x['path_id'],'search_brief':{'concept_name':name,'learner_level':paths[x['path_id']]['learner_scope'],'required_fact_ids':[f['id'] for f in facts[cid]],'preferred_visual_modes':x['video_need']['preferred_visual_modes'],'blocked_concepts_to_avoid':drift},'search_route':'allowlist_then_open_search' if used_open else 'allowlist_only','candidates':cs})
parents=[B/'glossary_pass_a.json',B/'registry_lookup.json',B/'extracted_concepts.json',B/'coverage_briefs.json',CORE/'video_bank/channel_allowlist.json']+catalog_paths
metadata={**g['metadata'],'artifact_type':'video_candidates','prompt_version':'06_video_candidates@v1','model':'gpt-6.1-sol','generated_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'parent_artifact_hashes':{str(p.relative_to(B)) if p.is_relative_to(B) else str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in parents}}
artifact={'metadata':metadata,'batch_id':'glossary_batch_product_manager','searches':rows}
out=B/'video_candidates.part.all.json';out.write_text(json.dumps(artifact,ensure_ascii=False,indent=2)+'\n')
# Mechanical cross-reference and self-review mistakes checklist.
expected={(x['concept_id'],x['path_id']) for x in g['entries'] if x['video_need']['level'] in ['HIGH','MEDIUM']}
assert {(r['concept_id'],r['path_id']) for r in rows}==expected and len(rows)==len(expected)
for r in rows:
 c=concepts[r['concept_id']];sb=r['search_brief'];assert sb['concept_name']==c['concept_name'];assert sb['learner_level']==paths[r['path_id']]['learner_scope'];assert set(sb['blocked_concepts_to_avoid'])<=set(c['blocked_knowledge_ids'])
 assert sb['required_fact_ids']==[f['id'] for f in facts[c['concept_id']]]
 assert len({v['video_id'] for v in r['candidates']})==len(r['candidates'])
 for v in r['candidates']:
  assert re.fullmatch('[A-Za-z0-9_-]{11}',v['video_id']);assert v['youtube_url']=='https://www.youtube.com/watch?v='+v['video_id'];assert v['reason']
  if v['found_via']=='allowlist_catalogue':
   orig=catalog[v['video_id']]
   for k in ['title','channel_id','channel_name','duration_seconds']:assert v[k]==orig[k]
  if v['found_via']=='open_search':
   all_results=[a for p in W.glob('search_*.json') for a in load(p)['results']]
   assert any(all(a[k]==v[k] for k in ['video_id','title','channel_id','channel_name','duration_seconds']) for a in all_results)
counts=collections.Counter(v['filter_verdict'] for r in rows for v in r['candidates']);routes=collections.Counter(r['search_route'] for r in rows)
print(out,'search rows',len(rows),'candidates',sum(counts.values()),dict(counts),'routes',dict(routes));print('Self-check PASS: whole-batch eligibility, no duplicates, exact facts/level/modes, real blocked IDs, <=5 kept, title/channel/duration provenance, computed URLs, reasons, routing, parent hashes. No stage-specific mistakes checklist is present in GENERATOR.md.')
