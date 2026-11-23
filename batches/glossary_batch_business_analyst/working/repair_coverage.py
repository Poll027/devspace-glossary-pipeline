import json,copy
from pathlib import Path
p=Path('batches/glossary_batch_business_analyst/coverage_briefs.part.all.json')
a=json.loads(p.read_text());before=copy.deepcopy(a)
B={b['concept_id']:b for b in a['briefs']}
def ref(i,url,section):return i+'#'+url+' — '+section
def fact(i,s,*r):return {'id':'f'+str(i),'statement':s,'source_refs':list(r)}
def ev(i):return B[i]['evidence']
def append(i,s,*r):
 e=ev(i);n=max(int(f['id'][1:]) for f in e['required_facts']+e['optional_enrichment'])+1;e['required_facts'].append(fact(n,s,*r))
gather='https://www.atlassian.com/work-management/project-management/requirements-gathering'
ac='https://www.atlassian.com/work-management/project-management/acceptance-criteria'
uml='https://www.omg.org/spec/UML/2.5.1/PDF'
bpmn='https://www.omg.org/spec/BPMN/2.0.2/PDF'
rtm='https://www.atlassian.com/software/jira/templates/requirements-traceability-matrix'
hist='https://confluence.atlassian.com/doc/page-history-and-page-comparison-views-139379.html'
workflow='https://www.atlassian.com/software/jira/templates/document-approval'
change='https://www.atlassian.com/itsm/change-management'
i='ba_req.elicitation_validation_verification'
append(i,'Distinguish validation of the intended business need with stakeholders from verification of the written requirements’ quality: stakeholder agreement does not by itself establish that the wording is unambiguous or objectively testable.',ref('atlassian_agile',gather,'Step 5: Prioritize and validate requirements'),ref('atlassian_agile',ac,'Characteristics of good acceptance criteria — Clarity and conciseness; Testability'))
append(i,'Check completeness against the documented goals, success metrics, scope, requirement categories, assumptions, and constraints; record missing information as open questions for resolution.',ref('atlassian_agile',gather,'Step 4: Document requirements in one shared place'))
append(i,'Check ambiguity by asking whether stakeholders can interpret the statement the same way; replace vague wording with plain, outcome-focused language and measurable thresholds where possible.',ref('atlassian_agile',ac,'Characteristics of good acceptance criteria — Clarity and conciseness; Measurability'))
append(i,'Check testability by identifying an executable test and an objective pass/fail result for each stated condition; revise a condition if its satisfaction depends on subjective judgment.',ref('atlassian_agile',ac,'Characteristics of good acceptance criteria — Testability; How to write acceptance criteria — 3. Establish overall testability'))
i='ba_doc.functional_specifications'
ev(i)['required_facts'][2]=fact(3,'Write a detailed functional specification entry with the initiating event and input values, the expected system response, resulting outputs, and applicable preconditions, postconditions, or exception behavior.',ref('uml_spec',uml,'13.2.3.1 — Behaviors; 13.2.3.2 — Behavior Parameters'))
i='ba_doc.requirements_traceability'
ev(i)['required_facts'][0]=fact(1,'Requirements traceability maintains links from initial business needs through design, development, and testing to the work that fulfills the requirements.',ref('atlassian_agile',rtm,'What is a requirements traceability matrix template?'))
ev(i)['required_facts'][1]=fact(2,'Construct an RTM with a row for each requirement identifier and columns for its originating business need or source, related design artifact, and test-case identifiers; populate these with references to the actual artifacts rather than unlinked descriptions.',ref('atlassian_agile',rtm,'What is a requirements traceability matrix template?; How to get started — 2. Define and categorize requirements for easy traceability; 3. Link requirements to related work items'))
append(i,'Review the RTM for missing required links: a requirement without a source link is orphaned from its business justification, and a missing design or test link is a coverage gap when that artifact is required for the stage being reviewed.',ref('atlassian_agile',rtm,'What is a requirements traceability matrix template?; Importance of a requirements traceability matrix template; How to get started — 3. Link requirements to related work items; 5. Track progress with dashboards and reports'))
i='ba_doc.requirements_lifecycle'
append(i,'Use a customized requirement workflow to distinguish draft (under preparation or review), approved (agreed for delivery), change under review (a proposed revision awaiting a decision), and retired (no longer current); make approval, revision review, and retirement explicit status transitions rather than silently overwriting the current requirement.',ref('atlassian_agile',workflow,'Workflows; Easy document management; Progress tracking; Customized workflow'),ref('atlassian_agile',change,'Change management process — Change request; Change request review; Change approval; Change closure'))
append(i,'For a proposed change, record the affected requirement and change request, review its risks and expected outcomes, record the approval decision and status, then document the implemented change and its results.',ref('atlassian_agile',change,'Change management process — Change request; Change request review; Change plan; Change approval; Change implementation; Change closure'))
append(i,'When the requirement is documented on a Confluence page, modifying that page creates a new version; record the current workflow status in the document, and use More options > Page History to inspect version numbers and compare the revision with the preceding version.',ref('atlassian_agile',hist,'Access the page history; View changes made to a page; Compare two versions'),ref('atlassian_agile',workflow,'Progress tracking; Customized workflow'))
append(i,'Preserve the change history when restoring an earlier requirement document: Confluence restoration creates a new current copy of the selected version rather than replacing the historical versions, and lets the user edit the restoration’s change comment.',ref('atlassian_agile',hist,'Restore a previous version'))
i='ba_bpmn.core_notation'
append(i,'Select a thin single-circle start event to show where a process starts, a thin double-circle intermediate event for something occurring between its start and end, and a thick single-circle end event to show where a process path ends.',ref('bpmn_spec',bpmn,'10.5 — Events; 10.5.2 — Start Event; 10.5.3 — End Event; 10.5.4 — Intermediate Event'))
i='ba_dm.relationships_cardinality'
append(i,'Write UML multiplicity as lower..upper: the lower bound is the minimum allowed number of related instances, the upper bound is the maximum, and * denotes an unlimited upper bound.',ref('uml_spec',uml,'7.5.3.2 — Multiplicities; 7.5.4.1 — Multiplicity Element'))
append(i,'Interpret 0..1 as optional with at most one related instance, 1 (equivalently 1..1) as exactly one, 0..* as zero or more, and 1..* as one or more.',ref('uml_spec',uml,'7.5.3.2 — Multiplicities; 7.5.4.1 — Multiplicity Element'))
append(i,'For a binary relationship, translate the business statement about how many instances of one entity can relate to a fixed instance of the other into lower and upper bounds, and place those bounds at the end whose instances are being counted; repeat from the opposite direction to annotate both ends.',ref('uml_spec',uml,'11.5.3.1 — Associations; 7.5.4.1 — Multiplicity Element'))
i='ba_gap.business_case'
e=ev(i)
for fid in ['f3','f5']:
 f=next(f for f in e['required_facts'] if f['id']==fid);e['required_facts'].remove(f);e['optional_enrichment'].append(f)
append(i,'For a monetary-return estimate, calculate projected net return = total projected monetary benefits over the evaluation period − project cost, including the cost of the project itself rather than reporting gross savings alone.',ref('nngroup_articles','https://www.nngroup.com/articles/calculating-roi-design-projects/','Step 3: Convert Your UX Metric to a KPI; Step 4: Report the Results — Example: Health-Insurance Website'))
append(i,'Interpret a positive projected monetary return as estimated benefits exceeding cost over that period, and report the assumptions and time horizon because the return is an estimate, not a promised financial outcome.',ref('nngroup_articles','https://www.nngroup.com/articles/calculating-roi-design-projects/','Step 4: Report the Results'))
i='spreadsheet.data_visualization'
x='https://support.microsoft.com/en-us/excel/get-started/create-a-chart-from-start-to-finish'
append(i,'In Excel for the web, select the worksheet range containing the data, then use Insert > Charts to choose a suitable chart type.',ref('excel_support',x,'1. Create a chart'))
append(i,'Right-click the chart and choose Select Data; in Data > Setup assign the category-cell range to Horizontal Axis > Horizontal Field and add the value-cell range under Vertical Axis > Add Field, checking that the fields occupy the intended axes.',ref('excel_support',x,'2. Edit the Data — Add, remove or modify a data series; Swap vertical and horizontal axis'))
append(i,'Check the source range and plotted series in the chart task pane, correcting series names or ranges as needed, then use Format to check the chart title, axis titles, and displayed data labels.',ref('excel_support',x,'2. Edit the Data; 3. Customize your chart — Add, remove or modify the title; Add, remove or modify the titles of your axis; Add, remove or modify data labels'))
i='ba_bi.tableau_design'
append(i,'Build a worksheet bar chart by dragging a category dimension to Rows and a numeric measure to Columns (or vice versa), using Bar as the mark type; these field placements create the category/value view that can be placed on the dashboard.',ref('tableau_help','https://help.tableau.com/current/pro/desktop/en-us/buildexamples_bar.htm','Build a Bar Chart — introductory field arrangements'))
# Place worksheet instruction before the existing dashboard assembly instruction without changing its fact id.
e=ev(i);f=e['required_facts'].pop();e['required_facts'].insert(1,f)
i='ba_bi.tableau_calculated_fields'
ev(i)['required_facts'][2]=fact(3,'The source’s Discount Ratio calculation is IIF([Sales] !=0, [Discount]/[Sales],0): it returns Discount divided by Sales when Sales is nonzero, and zero otherwise.',ref('tableau_help','https://help.tableau.com/current/pro/desktop/en-us/calculations_calculatedfields_create.htm','Create a calculated field — Discount Ratio example'))
# Advisory changes: reword/cite/move only; no optional new claims.
i='ba_prio.kano'
B[i]['learning_objective'] += ' This lesson focuses on the three named categories: basic, performance, and excitement.'
i='ba_agile.acceptance_criteria'
ev(i)['required_facts'][1]['source_refs']=[ref('atlassian_user_stories','https://www.atlassian.com/agile/project-management/user-stories','How to write user stories — Definition of done; What should a user story include?')]
allowed=set(json.load(open('/tmp/repair_ids.json')))
changed=[]
for b,old in zip(a['briefs'],before['briefs']):
 if b!=old:
  assert b['concept_id'] in allowed
  changed.append(b['concept_id'])
assert a['metadata']==before['metadata'] and len(a['briefs'])==len(before['briefs'])
p.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n')
print('Changed',len(changed),changed)
print('Rows',len(a['briefs']),'required facts',sum(len(b['evidence']['required_facts']) for b in a['briefs']),'optional facts',sum(len(b['evidence']['optional_enrichment']) for b in a['briefs']))
