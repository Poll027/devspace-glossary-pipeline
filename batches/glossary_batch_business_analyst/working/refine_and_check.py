import json,pathlib,re,copy,hashlib,datetime,collections
B=pathlib.Path('batches/glossary_batch_business_analyst');P=B/'coverage_briefs.part.all.json';o=json.loads(P.read_text());rows=o['briefs'];cs=json.loads((B/'extracted_concepts.json').read_text())['concepts']
# Narrow claims, repair source locations, remove unsupported acronym and redirected-page citations,
# and strengthen supported hands-on steps before the initial submission.
def facts(i):return rows[i]['evidence']['required_facts']
def replace(i,n,statement=None,refs=None):
 f=facts(i)[n-1]
 if statement is not None:f['statement']=statement
 if refs is not None:f['source_refs']=refs if isinstance(refs,list) else [refs]
def append(i,s,r):facts(i).append({'id':'pending','statement':s,'source_refs':r if isinstance(r,list) else [r]})
a=lambda path,head:'atlassian_agile#'+path+' — '+head
n=lambda path,head:'nngroup_articles#articles/'+path+'/ — '+head
pb=lambda path,head:'powerbi_docs#'+path+' — '+head
pg=lambda head:'postgres_docs#'+head
req='work-management/project-management/requirements-gathering'
replace(1,1,'A structured interview follows an interview script, unlike a semistructured interview’s flexibly ordered guide.',n('interview-guide','Opening definitions of interview script and interview guide'))
replace(4,2,'Extract the requirements, assumptions, constraints, and open questions found in existing material and record them in one shared document with links to supporting context.',a(req,'Step 3: Collect input through the right channels; Step 4: Document requirements in one shared place'))
replace(6,2,'For the requirements review, present the documented goal, scope, requirements, assumptions, and open questions, then capture stakeholder agreement or requested changes.',a(req,'Step 4: Document requirements in one shared place; Step 5: Prioritize and validate requirements'))
replace(7,2,refs=n('draw-wireframe-even-if-you-cant-draw','The 5-Step Wireframing Process'))
replace(8,1,refs=a('work-management/project-collaboration/brainstorming','What is brainstorming?'))
replace(8,2,'State the session’s problem and goal, set a time limit, choose a facilitator, and record contributed ideas.',a('work-management/project-collaboration/brainstorming/how-to-run-a-brainstorming-session','Step 1. Identify your goal; Step 3. Set a time and place; Step 4. Pick a qualified facilitator'))
replace(8,3,refs=a('work-management/project-collaboration/brainstorming','The importance of brainstorming'))
replace(9,4,'Record the opinions and disagreements expressed in the discussion without treating those stated preferences as evidence of actual product use.',n('focus-groups','Getting Focused; opening distinction between what users say and do'))
append(12,'Create a shared specification by listing the expected functions and separating them from business outcomes and nonfunctional expectations, then review that list with stakeholders.',a(req,'Types of project requirements to gather; Step 4; Step 5'))
replace(17,2,'Make the performance expectation measurable by stating a concrete numerical target rather than a vague request for good performance.',a(req,'Types of project requirements to gather — non-functional requirements'))
replace(21,2,refs=a('team-playbook/plays/stakeholder-communications-plan','3. Fill out the Communications Plan; 4. Review the Communications Plan'))
replace(22,1,'A workshop facilitator supports the group’s process by planning, guiding, and managing collaborative work.',n('workshop-facilitation-101','What Is Workshop Facilitation?'))
append(27,'List the specific steps or handoffs where the map shows delay, redundancy, or missing work, and review these findings with process stakeholders.',a('work-management/project-management/process-mapping','Benefits of process mapping; 6. Review and validate'))
replace(28,2,refs=a('agile/project-management/lean-process-improvement','How to apply Lean process improvement within projects — 1. Determine potential areas for improvement; 2. Identify potential solutions'))
append(28,'Agree an improvement action with the team, implement it, and review its effects to continue improving the process.',a('agile/project-management/lean-process-improvement','How to apply Lean process improvement within projects'))
replace(30,2,'Specify an explicit default outcome for the situation in which none of the listed conditions is true.',pg('9.18.1 — CASE'))
replace(32,1,'An entity is a business thing being described; its attributes are descriptive properties of that thing.',pb('guidance/star-schema','Understand star schema'))
append(38,'Use multiplicity labels such as 1, 0..1, 0..*, or 1..* to state the permitted numbers of related instances.','uml_spec#7.5.4 — Notation')
replace(39,2,'Draw the named entities and connect their relationships to communicate the main things represented in the business domain.',['uml_spec#11.4.4 — Notation','uml_spec#11.5.4 — Notation'])
replace(40,2,'Identify the reporting or filtering information needed and match each item to the entity attributes that can supply it.',pb('guidance/star-schema','Understand star schema; Star schema relevance to Power BI semantic models'))
append(54,'Organize the current-state notes by the business areas being assessed so they can be compared with goals and gaps.',a('software/confluence/templates/gap-analysis','Categorize information and start your analysis; Assess current state'))
append(55,'Write the desired objectives alongside the corresponding business areas in the desired-state column.',a('software/confluence/templates/gap-analysis','Define the desired state'))
replace(62,3,'Calculate net present value as the present value of future benefits minus the present value of future costs, using a consistent discount rate and evaluation period.',a('work-management/strategic-planning/cost-benefit-analysis','Calculate net present value'))
append(62,'A positive net present value supports accepting the initiative on this financial criterion; a negative value argues against it, and zero indicates neither gain nor loss.',a('work-management/strategic-planning/cost-benefit-analysis','Analyze your results'))
# INVEST was not present in the cited page. Keep supported writing and splitting facts only.
del facts(66)[1]
replace(68,2,'Group planned initiatives into a sequence such as Now, Next, and Later, linking the sequence to goals and tracking dependencies.',a('agile/product-management/roadmaps','Who is responsible for the product roadmap?; roadmap examples; Tips and tricks'))
replace(68,3,refs=a('agile/product-management/roadmaps','Tips and tricks'))
replace(69,2,'Discuss what completing the story means, make the acceptance conditions testable, and document that shared understanding.','atlassian_user_stories#How to write user stories — Definition of done; Testable stories')
replace(75,1,'Hierarchical decomposition represents a larger goal as major tasks or functions and breaks them into smaller parts.',n('task-analysis','Stage 2: Analyze Tasks'))
replace(75,2,'Start with the top-level goal, draw its major parts below it, and break each part into relevant subparts.',n('task-analysis','Stage 2: Analyze Tasks'))
replace(79,2,refs='excel_support#en-us/excel/functions/if-function — Simple IF examples — discussion of nesting multiple comparisons')
replace(81,2,refs='excel_support#https://support.microsoft.com/en-us/office/create-a-pivottable-to-analyze-worksheet-data-a9a84538-bfe9-40a9-a8e9-f99134456576 — Working with the PivotTable Fields pane')
append(81,'Select a table or range, insert a PivotTable, place grouping fields in Rows and the metric in Values, and select an aggregation that answers the business question.','excel_support#https://support.microsoft.com/en-us/office/create-a-pivottable-to-analyze-worksheet-data-a9a84538-bfe9-40a9-a8e9-f99134456576 — Insert a PivotTable; Working with PivotTable Values')
replace(82,2,'Review important backlog items collaboratively and select work that can be completed within the iteration.','scrum_guide#Sprint Planning')
replace(88,1,refs=a('software/confluence/templates/fishbone-diagram','What is a fishbone diagram template?'))
replace(88,2,'Write a specific problem statement, select cause categories appropriate to the problem, and brainstorm potential causes with the team.',a('software/confluence/templates/fishbone-diagram','Define the problem; Choose categories; Brainstorm potential causes'))
append(88,'Place each proposed cause under its category branch to expose patterns; then analyze the proposed causes and agree actions addressing the root cause.',a('software/confluence/templates/fishbone-diagram','Organize causes; Analyze the diagram; Develop an action plan'))
replace(96,2,'Use Modeling > New measure and enter MeasureName = SUM(TableName[NumericColumn]) to define a basic total that responds to report context.',pb('transform-model/desktop-measures','Sales projection example; Understanding measures'))
replace(97,3,'For a row-level ratio, divide the two input fields and use IIF(condition, true_result, false_result) to specify what happens when the denominator is zero.','tableau_help#current/pro/desktop/en-us/calculations_calculatedfields_create.htm — Create a calculated field')
replace(98,1,'A Power BI semantic model contains data-model logic that can be used to build reports.',pb('connect-data/service-datasets-understand','Power BI Desktop-developed models'))
replace(98,2,refs=pb('connect-data/service-datasets-across-workspaces','Discover semantic models; Copy a report'))
replace(98,3,refs=[pb('transform-model/desktop-measures','Understanding measures'),pb('connect-data/service-datasets-across-workspaces','Discover semantic models')])
append(98,'Connect a new report to the existing shared semantic model; building content on a shared model requires Build permission.',pb('connect-data/service-datasets-across-workspaces','Discover semantic models; Build permission for semantic models'))
# Chart-type guidance was not in Tableau's formatting page. Cite the verified Power BI overview.
for i in [80,94]:replace(i,1,refs=pb('visuals/power-bi-visualization-types-for-reports-and-q-and-a','Charts for comparison and trends — Bar and column charts; Line charts'))
# Use complete verified URLs in locators when the source-pack entry is a site/section hub.
pgpages={'2.5':'tutorial-select','2.7':'tutorial-agg','7.2':'queries-table-expressions','7.5':'queries-order','7.6':'queries-limit','8':'datatype','9.2':'functions-comparison','9.18':'functions-conditional','9.22':'functions-window','3.5':'tutorial-window'}
def normalize_ref(r):
 sid,loc=r.split('#',1)
 if loc.startswith('https://'):return r
 if sid=='atlassian_agile':loc='https://www.atlassian.com/'+loc
 elif sid=='atlassian_user_stories':loc='https://www.atlassian.com/agile/project-management/user-stories — '+loc
 elif sid=='nngroup_articles':loc='https://www.nngroup.com/'+loc
 elif sid=='powerbi_docs':loc='https://learn.microsoft.com/en-us/power-bi/'+loc
 elif sid=='tableau_help':loc='https://help.tableau.com/'+loc
 elif sid=='excel_support':
  if loc.startswith('en-us/'):loc='https://support.microsoft.com/'+loc
 elif sid=='scrum_guide':loc='https://scrumguides.org/scrum-guide.html — '+loc
 elif sid=='bpmn_spec':loc='https://www.omg.org/spec/BPMN/2.0.2/PDF — '+loc
 elif sid=='uml_spec':loc='https://www.omg.org/spec/UML/2.5.1/PDF — '+loc
 elif sid=='postgres_docs':
  section=loc.split(' — ')[0]
  choices=[k for k in pgpages if section==k or section.startswith(k+'.')]
  k=max(choices,key=len);loc='https://www.postgresql.org/docs/current/'+pgpages[k]+'.html — '+loc
 return sid+'#'+loc
for row in rows:
 if row['canonical_status']=='new':
  for j,f in enumerate(row['evidence']['required_facts'],1):
   f['id']='f'+str(j);f['source_refs']=[normalize_ref(r) for r in f['source_refs']]
o['metadata']['generated_at']=datetime.datetime.now(datetime.timezone.utc).isoformat()
P.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
# Mistakes-checklist audit: exact pairing, registry preservation, source IDs, ID uniqueness,
# placeholder objectives, duplicate facts, and explicit blocked-name leakage.
look=json.loads((B/'registry_lookup.json').read_text())['lookups'];lk={(x['concept_id'],x['path_id']):x for x in look}
reg={x['concept_id']:x for x in json.loads((B/'concept_evidence_registry_snapshot.json').read_text())['entries']}
assert len(rows)==len(cs)==99
assert {(x['concept_id'],x['path_id']) for x in rows}==set(lk)
pack=json.loads(pathlib.Path('00_GLOSSARY_PIPELINE_CORE/source_packs/business_analyst.source_pack.json').read_text());sids={s['source_id'] for s in pack['sources']}
names={c['concept_id']:c['concept_name'] for c in cs};hits=[];facts_count=0
for c,row in zip(cs,rows):
 assert row['canonical_status']==lk[(c['concept_id'],c['path_id'])]['canonical_status']
 assert row['learning_objective'].startswith('Learner can ')
 assert not re.search(r'Understand and use|Given a simple example|small analysis task',row['learning_objective'],re.I)
 ev=row['evidence'];fs=ev['required_facts'];facts_count+=len(fs)
 assert len({f['id'] for f in fs})==len(fs)
 if row['canonical_status']=='reuse_registry':assert ev==reg[c['concept_id']].get('evidence',reg[c['concept_id']])
 else:
  assert ev['created_in_batch_id']==B.name and ev['used_by_path_ids']==[c['path_id']]
  assert len({f['statement'].strip().lower() for f in fs})==len(fs)
  for f in fs:
   assert f['statement'].strip() and f['source_refs']
   for ref in f['source_refs']:assert ref.split('#',1)[0] in sids
  text=' '.join(f['statement'] for f in fs).lower()
  for blocked in c['blocked_knowledge_ids']:
   if names[blocked].lower() in text:hits.append((c['concept_id'],names[blocked]))
assert not hits,hits
for path,hashvalue in o['metadata']['parent_artifact_hashes'].items():
 src=pathlib.Path(path) if path.startswith('00_') else B/path
 assert hashlib.sha256(src.read_bytes()).hexdigest()==hashvalue
summary={'brief_rows':len(rows),'canonical_status_counts':dict(collections.Counter(x['canonical_status'] for x in rows)),'required_fact_rows':facts_count,'optional_fact_rows':sum(len(x['evidence']['optional_enrichment']) for x in rows),'misconception_rows':sum(len(x['evidence']['misconceptions']) for x in rows),'checklist':'Pair completeness, canonical immutability, source IDs/locators, fact IDs, no duplicate statements, actionable practice steps, no placeholder objectives, blocked-name scan, and metadata input hashes checked. No misconceptions added without a direct and safe paraphrase of misconception support.','source_limitations':['requirements_verification: no direct verification-versus-validation definition in the supplied pack; supported validation workflow retained.','decision_tables: no direct decision-table layout source found in the supplied pack; only supported condition/outcome/default decision logic retained.','conceptual_vs_logical_data_modeling: supplied sources support entities and relationships but not an explicit conceptual-versus-logical distinction.','writing_and_splitting_user_stories: cited sources support stories and splitting, but not the INVEST expansion requested by the upstream mental model.','functional_decomposition: supported with hierarchical task-analysis decomposition; no business-function-specific source in pack.','information_needs_mapping: supported through entity/attribute selection for reporting; no named mapping-grid convention in pack.','business_case_basics: cost-benefit and NPV backed; no direct ROI formula found in pack.','business_rules_documentation: supported constraints and approvals capture; no direct rule-statement syntax found in pack.']}
(B/'working/mistakes_checklist.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
