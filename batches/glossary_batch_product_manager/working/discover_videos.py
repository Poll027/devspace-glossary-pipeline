import json,pathlib,re,subprocess,concurrent.futures,urllib.parse
B=pathlib.Path('batches/glossary_batch_product_manager');W=B/'working';g=json.loads((B/'glossary_pass_a.json').read_text());e={x['concept_id']:x for x in json.loads((B/'extracted_concepts.json').read_text())['concepts']}
# Explicit title-level catalogue matches; all catalogue files were scanned before this selection.
CAT={
'persona_development':[91,88], 'design_thinking_ideation':[920,929,921,933],
'mvp_scope_definition':[87], 'negotiation':[849,918],
'sprint_planning':[93,94], 'daily_standup':[93,94], 'sprint_review':[93,94], 'sprint_retrospective':[93,94],
'product_backlog_management':[96], 'technical_debt_management':[769,774],
'kanban_board_management':[90], 'hypothesis_testing':[791], 'ab_testing':[904],
'design_feedback':[922], 'stakeholder_management':[936], 'survey_design':[940],
}
QUERY={
'competitive_analysis':'competitive analysis product management tutorial',
'customer_interviews':'customer interviews user research how to conduct tutorial',
'jobs_to_be_done_framework':'jobs to be done framework explained examples',
'voice_of_customer':'voice of customer analysis themes tutorial',
'survey_design':'survey design neutral questions research tutorial',
'market_sizing':'TAM SAM SOM market sizing calculation example tutorial',
'usability_testing':'usability testing how to conduct session tutorial',
'product_market_fit':'product market fit retention curve explained tutorial',
'solution_specification':'product solution specification document example requirements tutorial',
'product_requirements_document':'product requirements document PRD example tutorial',
'acceptance_criteria':'acceptance criteria given when then examples tutorial',
'user_flows':'UX user flow diagram tutorial example',
'product_roadmap':'product roadmap beginner tutorial example',
'capacity_planning':'agile team capacity planning calculation example',
'release_planning':'agile release planning roadmap tutorial',
'feature_sequencing':'product roadmap sequencing dependencies features tutorial',
'timeline_estimation':'project timeline estimation dependencies tutorial',
'quarterly_planning':'quarterly product planning roadmap tutorial',
'dependency_management':'project roadmap dependency management tutorial',
'mvp_scope_definition':'minimum viable product scope prioritization tutorial',
'value_vs_effort_matrix':'value effort matrix prioritization example tutorial',
'impact_assessment':'product prioritization impact assessment example',
'rice_framework':'RICE prioritization framework calculation example',
'ice_framework':'ICE prioritization framework calculation example',
'weighted_scoring':'weighted scoring prioritization matrix example tutorial',
'tradeoff_analysis':'product management trade off analysis example tutorial',
'stakeholder_management':'stakeholder mapping power interest grid tutorial',
'cross_functional_collaboration':'cross functional collaboration product management tutorial',
'consensus_building':'consensus building team decision making tutorial',
'status_reporting':'project status report tutorial example',
'executive_communication':'executive communication project update tutorial',
'roadmap_communication':'communicating product roadmap stakeholders tutorial',
'conflict_resolution':'conflict resolution workplace techniques tutorial',
'product_backlog_management':'product backlog management prioritization tutorial',
'effort_estimation':'agile effort estimation story points planning poker tutorial',
 'technical_feasibility_conversations':'product management technical feasibility assessment tutorial',
'backlog_refinement':'scrum backlog refinement tutorial',
'dependency_tracking':'scrum dependency management blockers tutorial',
'kanban_board_management':'kanban board WIP limits tutorial',
'release_management':'software release management checklist tutorial',
'north_star_metrics':'north star metric product management examples tutorial',
'hypothesis_testing':'product experiment hypothesis testing explained beginner',
'analytics_dashboard_interpretation':'interpreting analytics dashboards product metrics tutorial',
'tracking_plan_definition':'analytics tracking measurement plan tutorial',
'funnel_analysis':'funnel analysis conversion rate example tutorial',
'cohort_analysis':'cohort retention analysis explained example',
'ab_testing':'A B testing explained beginner significance tutorial',
'feature_flags':'feature flags percentage rollout rollback explained tutorial',
'holdout_groups':'holdout groups product experimentation explained',
'launch_readiness_checklist':'product launch readiness checklist tutorial',
'launch_communication_plan':'product launch communication plan tutorial',
'sales_and_support_enablement':'product enablement sales support training tutorial',
'design_collaboration':'product manager designer collaboration tutorial',
'user_journey_mapping':'user journey mapping example tutorial',
'design_feedback':'giving design feedback critique tutorial',
'user_testing_synthesis':'usability testing findings synthesis severity tutorial',
}
R=json.loads((W/'video_title_matches.json').read_text())
(W/'catalogue_selection.json').write_text(json.dumps(CAT,indent=2))
def walk(o):
 if isinstance(o,dict):
  if 'videoRenderer' in o:yield o['videoRenderer']
  for v in o.values():yield from walk(v)
 elif isinstance(o,list):
  for v in o:yield from walk(v)
def text(o):return o.get('simpleText') or ''.join(x.get('text','') for x in o.get('runs',[]))
def fetch(key,q):
 url='https://www.youtube.com/results?search_query='+urllib.parse.quote(q)
 p=W/('search_'+key+'.json')
 html=subprocess.check_output(['curl','-sL','--max-time','45',url]).decode()
 m=re.search(r'(?:var ytInitialData|window\["ytInitialData"\])\s*=\s*',html)
 if not m:return key,[],'no initial data'
 data=json.JSONDecoder().raw_decode(html[m.end():])[0]; rows=[];seen=set()
 for v in walk(data):
  vid=v.get('videoId');owner=v.get('ownerText',{}).get('runs',[{}])[0];dur=text(v.get('lengthText',{}));parts=dur.split(':')
  if not vid or vid in seen or not all(x.isdigit() for x in parts):continue
  sec=0
  for n in parts:sec=sec*60+int(n)
  cid=owner.get('navigationEndpoint',{}).get('browseEndpoint',{}).get('browseId','')
  if not cid:continue
  seen.add(vid); rows.append({'video_id':vid,'youtube_url':'https://www.youtube.com/watch?v='+vid,'title':text(v.get('title',{})),'channel_id':cid,'channel_name':owner.get('text',''),'duration_seconds':sec,'result_url':url})
 p.write_text(json.dumps({'query':q,'url':url,'results':rows},ensure_ascii=False,indent=2));return key,rows,None
jobs=[]
for x in g['entries']:
 if x['video_need']['level'] not in ['HIGH','MEDIUM']:continue
 key=x['concept_id'].split('.')[-1]
 if len(CAT.get(key,[]))<2:jobs.append((key,QUERY.get(key,e[x['concept_id']]['concept_name']+' tutorial')))
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
 for key,rows,err in pool.map(lambda a:fetch(*a),jobs):print(key,len(rows),err,flush=True)
