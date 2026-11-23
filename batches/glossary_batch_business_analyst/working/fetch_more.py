exec(open('batches/glossary_batch_business_analyst/working/fetch_sources.py').read().split('urls={}')[0])
urls={}
for k in ['stakeholder-engagement','stakeholder-analysis','engaging-reports-presentations','facilitating-ux-workshops-guide','dominating-workshop-participants','workshop-facilitation-101','ux-workshop-agendas','prioritization-methods','prioritization-matrices','draw-wireframe-even-if-you-cant-draw','collaborating-stakeholders','lean-agile-documentation']:
 urls['nn_'+k]='https://www.nngroup.com/articles/'+k+'/'
for path in ['work-management/project-collaboration/stakeholder-mapping','work-management/project-collaboration/communication-plan','work-management/project-collaboration/cross-functional-teams/stakeholder-communication','work-management/strategic-planning/swot-analysis','work-management/strategic-planning/cost-benefit-analysis','work-management/strategic-planning/business-process-reengineering','work-management/project-management/requirements-gathering','work-management/project-management/process-mapping','work-management/project-management/risk-matrix','work-management/project-management/risk-register','agile/product-management/requirements','agile/project-management/lean-process-improvement','team-playbook/plays/stakeholder-communications-plan','work-management/team-management-and-leadership/decision-making/models']:
 urls['atl_'+path.split('/')[-1]]='https://www.atlassian.com/'+path
urls['pbi_star-schema']='https://learn.microsoft.com/en-us/power-bi/guidance/star-schema'
urls['pbi_quick-measures']='https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-quick-measures'
urls['pbi_report-publish']='https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-upload-desktop-files'
# Discover actual Excel help links rather than manufacturing UUIDs.
urls['excel_formulas']='https://support.microsoft.com/en-us/office/overview-of-formulas-in-excel-ecfdc708-9162-49e8-b993-c311f47ca173'
with concurrent.futures.ThreadPoolExecutor(max_workers=12) as ex:results=list(ex.map(fetch,urls.items()))
(P/'index_more.json').write_text(json.dumps(results,indent=2));print('\n'.join(map(str,results)))
import sys
sys.path.insert(0,'batches/glossary_batch_business_analyst/working/lib')
from pypdf import PdfReader
for k in ['bpmn','uml']:
 reader=PdfReader('batches/glossary_batch_business_analyst/working/'+k+'.pdf');(P/(k+'.txt')).write_text('\n'.join('PDF PAGE '+str(i+1)+'\n'+p.extract_text() for i,p in enumerate(reader.pages)))
