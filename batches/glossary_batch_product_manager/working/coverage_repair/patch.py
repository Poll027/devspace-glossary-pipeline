import json, copy
from pathlib import Path
p=Path('batches/glossary_batch_product_manager/coverage_briefs.part.all.json')
d=json.loads(p.read_text()); before=copy.deepcopy(d)
by={b['concept_id'].split('.')[-1]:b for b in d['briefs']}
def fact(n,i):
    return next(f for f in by[n]['evidence']['required_facts'] if f['id']==i)
def replace(n,i,s,refs=None):
    f=fact(n,i);f['statement']=s
    if refs is not None:f['source_refs']=refs
replace('product_requirements_document','f3','Construct a specification with purpose, user needs, functional and technical requirements, scope, and constraints.', ['atlassian_agile#https://www.atlassian.com/agile/product-management/product-specification :: What does a product specification sheet include? / How to write a product specification sheet'])
replace('executive_communication','f3','Put the main decision or ask at the start of a written executive update, specifying whether you seek approval, strategic buy-in, or strategic direction, and leave supporting detail afterward.', ['nngroup_articles#https://www.nngroup.com/articles/inverted-pyramid/ :: How to Write in the Inverted Pyramid Style', 'productplan_glossary#https://www.productplan.com/learn/executive-roadmap :: 8. Remember your objective', 'productplan_glossary#https://www.productplan.com/learn/nail-product-roadmap-presentation :: 3. Burying the lede in the details.'])
replace('technical_feasibility_conversations','f4','Use a shared specification to identify roadblocks and align with engineering on features, requirements, and test plans.', ['atlassian_agile#https://www.atlassian.com/agile/product-management/product-specification :: Why is product specification important for product teams? / How do product specifications enhance collaboration?'])
replace('ab_testing','f6','In Amplitude’s Duration Estimator, select Estimate Duration, add a traffic event and conversion success metric (or manually enter total daily traffic and baseline conversion), set the relative minimum detectable effect and confidence level, and read the estimated days and users per day; for a plan exposing all that traffic, multiply days by users per day to estimate the total sample, or half that total per variant for an equal two-variant allocation, treating these as approximate traffic-based sample estimates rather than a separate sample-size output from the tool.', ['amplitude_playbook#https://help.amplitude.com/docs/en/feature-experiment/workflow/experiment-estimate-duration :: Open the duration estimator / Set up your estimate / Understand your results / How to read the table / Increase rollout percentage / Reduce number of variants'])
replace('holdout_groups','f1','A holdout group excludes a subset of users from specified experiments to provide a comparison baseline.')
replace('holdout_groups','f4','In Amplitude, set a holdout percentage between 1% and 10% when creating the group; withholding more traffic can extend experiment duration, and the percentage cannot be changed after creation.', ['amplitude_playbook#https://amplitude.com/docs/feature-experiment/advanced-techniques/holdout-groups-exclude-users :: Create a holdout group'])
replace('sales_and_support_enablement','f5','Prepare sales collateral such as pitch decks, demos, and battle cards, along with sales playbooks and training materials.', ['atlassian_agile#https://www.atlassian.com/agile/product-management/product-launch-checklist :: Sales and distribution'])
moves={'mission_and_values':'f5','product_vision_statement':'f4','jobs_to_be_done_framework':'f4','persona_development':'f4','usability_testing':'f5','solution_specification':'f4','product_requirements_document':'f4','one_pager':'f4','user_stories':'f4','acceptance_criteria':'f4','product_roadmap':'f4','quarterly_planning':'f5','roadmap_communication':'f4','effort_estimation':'f5','objectives_and_key_results':'f4','launch_communication_plan':'f4'}
for n,i in moves.items():
    ev=by[n]['evidence']
    if any(f['id']==i for f in ev['optional_enrichment']):
        continue
    f=fact(n,i);ev['required_facts'].remove(f);ev['optional_enrichment'].append(f)
f=fact('weighted_scoring','f5'); old=copy.deepcopy(f)
f['statement']='Compare totals to rank the options.'
old['id']='f6';old['statement']='Check how changes in priorities or assumptions would affect the ranking.'
by['weighted_scoring']['evidence']['optional_enrichment'].append(old)
changed=[b['concept_id'] for b,old in zip(d['briefs'],before['briefs']) if b!=old]
assert len(changed)==21,changed
assert all(b==old or b['concept_id'].split('.')[-1] in set(moves)|{'weighted_scoring','executive_communication','technical_feasibility_conversations','ab_testing','holdout_groups','sales_and_support_enablement'} for b,old in zip(d['briefs'],before['briefs']))
assert d['metadata']==before['metadata']
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
print('Changed briefs:',len(changed))
print('Briefs:',len(d['briefs']))
print('Required facts:',sum(len(b['evidence']['required_facts']) for b in d['briefs']))
print('Optional facts:',sum(len(b['evidence']['optional_enrichment']) for b in d['briefs']))
print('Misconceptions:',sum(len(b['evidence']['misconceptions']) for b in d['briefs']))
