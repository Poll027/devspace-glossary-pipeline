import json,copy
from pathlib import Path
p=Path('batches/glossary_batch_product_manager/coverage_briefs.part.all.json')
d=json.loads(p.read_text());before=copy.deepcopy(d)
by={b['concept_id'].split('.')[-1]:b['evidence'] for b in d['briefs']}
def ref(s,u,section):return s+'#'+u+' :: '+section
def edit(n,k,i,statement=None,refs=None):
 f=next(f for f in by[n][k] if f['id']==i)
 if statement is not None:f['statement']=statement
 if refs is not None:f['source_refs']=refs
 return f
def add(n,statement,refs):
 facts=by[n]['required_facts'];facts.append({'id':'f'+str(len(facts)+1),'statement':statement,'source_refs':refs})
A='atlassian_agile';P='productplan_glossary';M='amplitude_playbook';N='nngroup_articles'
edit('mission_and_values','required_facts','f2',refs=[ref(A,'https://www.atlassian.com/blog/innovation/company-culture-company-values','What are company values?')])
f=edit('mission_and_values','required_facts','f4',statement='Check a proposed product direction against the organization’s stated purpose.')
by['mission_and_values']['optional_enrichment'].append({'id':'f5','statement':'Draft a mission by identifying the organization’s purpose, audience, and value.','source_refs':copy.deepcopy(f['source_refs'])})
by['value_proposition']['misconceptions']=[m for m in by['value_proposition']['misconceptions'] if m['id']!='m1']
pos='https://www.atlassian.com/agile/product-management/product-positioning'
edit('strategic_positioning','required_facts','f2',statement='A positioning statement typically identifies who the product is for, what problem it solves, what category it competes in, and what makes it different.',refs=[ref(A,pos,'How to create an effective product positioning strategy to make your brand stand out / 3. Craft your positioning message')])
edit('strategic_positioning','required_facts','f3',refs=[ref(A,pos,'Key elements to create strong product positioning'),ref(A,pos,'How to create an effective product positioning strategy to make your brand stand out')])
job='https://www.nngroup.com/articles/personas-jobs-be-done/'
jobref=ref(N,job,'Jobs-to-Be-Done: Focus on User Goals')
edit('jobs_to_be_done_framework','required_facts','f2',refs=[jobref])
edit('jobs_to_be_done_framework','required_facts','f5',statement='Write the job as a sentence describing what the customer needs to accomplish, the relevant situation and why they do it, and what counts as a successful outcome rather than naming a requested feature.',refs=[jobref,ref(P,'https://www.productplan.com/glossary/jobs-to-be-done-framework','How Does the Jobs-to-be-Done Theory Apply to Product Development?')])
tam='https://www.productplan.com/glossary/total-addressable-market'
for i in ['f1','f2','f3','f4']:
 edit('market_sizing','required_facts',i,refs=[ref(P,tam,'What is Total Addressable Market (TAM)?' if i=='f1' else 'How do you calculate total addressable market?')])
samref=ref(P,'https://www.productplan.com/learn/how-to-measure-product-market-fit','Set attainable goals.')
edit('market_sizing','required_facts','f4',statement='Document the customer-count and revenue assumptions and, for the obtainable market, the time horizon and assumptions about willingness to buy, marketing and distribution reach, and competition.',refs=[ref(P,tam,'How do you calculate total addressable market?'),samref])
add('market_sizing','The Serviceable Addressable Market (SAM) is the portion of TAM within geographical reach; estimate its annual revenue by multiplying the reachable potential-customer count by annual revenue per customer.',[samref,ref(P,tam,'How do you calculate total addressable market?')])
add('market_sizing','The Serviceable Obtainable Market (SOM) is the portion of SAM realistically achievable; calculate it as SAM multiplied by an assumed achievable share for the chosen period, treating that share as an estimate rather than guaranteed demand.',[samref])
curve='https://amplitude.com/explore/analytics/retention-curve'
add('product_market_fit','A retention curve that declines initially and then stabilizes at a healthy level supports a judgment of product-market fit, while a curve declining toward zero signals problems with delivered value or onboarding.',[ref(M,curve,'Common retention curve shapes and what they mean')])
add('product_market_fit','Distinguish early from sustained retention when judging fit: early retention can reflect onboarding, whereas later retention shows lasting usage habits, and the curve alone does not explain why users leave.',[ref(M,curve,'How to analyze retention curves')])
add('product_market_fit','Customer word of mouth supports demand-driven growth, but an increase in signups can arise from external publicity rather than from customer recommendations.',[ref(P,'https://www.productplan.com/glossary/product-market-fit','How Do You Measure Product-Market Fit?'),ref(M,'https://amplitude.com/blog/analytics-product-market-fit','When AI falls short: Spikes in user acquisition')])
rel='https://www.productplan.com/learn/product-roadmap-vs-release-plan'
for i in ['f1','f2']:
 edit('release_planning','required_facts',i,refs=[ref(P,rel,'The Release Plan'),ref(P,rel,'The Product Roadmap')])
edit('release_planning','required_facts','f3',refs=[ref(P,'https://www.productplan.com/learn/how-to-quarterly-release-plan','Create a Quarterly Release Plan / Step 1: Identify your strategic objectives; Step 5: Plot out your plan'),ref(A,'https://www.atlassian.com/agile/product-management/product-planning','Develop product roadmap'),ref(A,'https://www.atlassian.com/agile/project-management/project-management-dependencies','How to identify dependencies in a project')])
edit('release_planning','required_facts','f4',refs=[ref(A,'https://www.atlassian.com/agile/project-management/project-management-dependencies','How to identify dependencies in a project; How to manage dependencies in project management')])
edit('ice_framework','misconceptions','m1',statement='ICE inputs remain subjective; shared scale definitions improve consistency but do not eliminate subjectivity.',refs=[ref(P,'https://www.productplan.com/glossary/ice-scoring-model','What are some drawbacks or shortcomings of ICE Scoring?')])
edit('release_management','required_facts','f1',statement='Release management coordinates the tactical and strategic steps involved in preparing a product for launch.',refs=[ref(P,'https://www.productplan.com/glossary/release-management','What Is Release Management?')])
funnel='https://amplitude.com/docs/analytics/charts/funnel-analysis/funnel-analysis-interpret'
for i,sec in [('f1','Interpret your Funnel Analysis chart'),('f2','Conversion'),('f3','Interpret your Funnel Analysis chart; Set your time options'),('f4','Conversion; Conversion over time')]:
 edit('funnel_analysis','required_facts',i,refs=[ref(M,funnel,sec)])
edit('funnel_analysis','required_facts','f5',refs=[ref(M,'https://amplitude.com/blog/funnel-analysis','How to Use Funnel Analysis'),ref(M,'https://amplitude.com/blog/funnel-analysis','What Is Funnel Analysis?')])
edit('ab_testing','required_facts','f4',statement='Treat a favorable metric difference as evidence of improvement only when the reported result is statistically significant under the experiment’s chosen threshold; a Not Significant or Inconclusive result does not establish improvement.',refs=[ref(M,'https://amplitude.com/docs/feature-experiment/workflow/experiment-learnings','Summary card / Statistical significance and Amplitude')])
flag='https://www.atlassian.com/blog/development/tips-for-feature-flagging'
edit('feature_flags','required_facts','f5',statement='Write explicit exposure stages with a success-metric and feedback check before expanding, and a quality rollback trigger such as errors in the logs that calls for switching the flag off until the problem is fixed.',refs=[ref(A,flag,'Tip 1: Understand why you want to use feature flags.'),ref(A,flag,'Tip 2: Measure the success of your feature.')])
edit('feature_flags','misconceptions','m1',refs=[ref(M,'https://amplitude.com/docs/feature-experiment/overview','Best practices / Establish causality')])
f=next(f for f in by['holdout_groups']['required_facts'] if '5–10%' in f['statement'])
f['statement']='Choose the holdout size using both available traffic and the statistical needs of the comparison; Amplitude specifies a configurable range of 1–10%, not a universal requirement.'
f['source_refs']=[ref(M,'https://amplitude.com/docs/feature-experiment/advanced-techniques/holdout-groups-exclude-users','Create a holdout group')]
add('design_collaboration','Agree who makes each design decision and who contributes advice; when the responsible designer is the agreed decision-maker, contributors supply information and recommendations but leave the final call to that designer.',[ref(A,'https://www.atlassian.com/team-playbook/plays/daci','What is the DACI decision-making framework?'),ref(A,'https://www.atlassian.com/team-playbook/plays/daci','3. Assign both Approvers and Contributors'),ref(A,'https://www.atlassian.com/team-playbook/plays/daci','6. Gather input and make decisions')])
edit('user_testing_synthesis','required_facts','f4',statement='Prioritize usability issues by severity, considering how often each occurs, how difficult it is for users to overcome, and whether it repeatedly bothers them; allocate more effort to the most serious problems.',refs=[ref(N,'https://www.nngroup.com/articles/how-to-rate-the-severity-of-usability-problems/','Severity Ratings for Usability Problems / three factors')])
expected={'mission_and_values','value_proposition','strategic_positioning','jobs_to_be_done_framework','market_sizing','product_market_fit','release_planning','ice_framework','release_management','funnel_analysis','ab_testing','feature_flags','holdout_groups','design_collaboration','user_testing_synthesis'}
changed=[]
for old,new in zip(before['briefs'],d['briefs']):
 if old!=new:
  assert old['concept_id'].split('.')[-1] in expected
  assert all(old[k]==new[k] for k in old if k!='evidence')
  changed.append(new['concept_id'])
assert len(changed)==15 and before['metadata']==d['metadata']
Path('batches/glossary_batch_product_manager/working/repair03/before.json').write_text(json.dumps(before,ensure_ascii=False,indent=2)+'\n')
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
print('Changed',len(changed),'briefs of',len(d['briefs']))
print('Facts',sum(len(b['evidence']['required_facts']) for b in d['briefs']),'Misconceptions',sum(len(b['evidence']['misconceptions']) for b in d['briefs']),'Optional',sum(len(b['evidence']['optional_enrichment']) for b in d['briefs']))
