import urllib.request,concurrent.futures,json,re, pathlib
from html.parser import HTMLParser
P=pathlib.Path('batches/glossary_batch_business_analyst/working/sources');P.mkdir(exist_ok=True)
class Text(HTMLParser):
 def __init__(self):super().__init__();self.out=[];self.skip=0
 def handle_starttag(self,t,a):
  if t in ['script','style']:self.skip+=1
  if t in ['p','h1','h2','h3','h4','li','tr','pre']:self.out.append('\n')
 def handle_endtag(self,t):
  if t in ['script','style']:self.skip=max(0,self.skip-1)
 def handle_data(self,s):
  if not self.skip:self.out.append(s)
def fetch(item):
 k,u=item
 try:
  r=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=40);h=r.read().decode();t=Text();t.feed(h);txt=re.sub(r'[ \t]+',' ',''.join(t.out));txt=re.sub(r'\n\s*\n','\n',txt);(P/(k+'.txt')).write_text(txt);return k,u,r.status,len(txt)
 except Exception as e:return k,u,str(e),0
urls={}
a='https://www.atlassian.com/work-management/project-management/'
for k in ['business-requirements','functional-requirements','non-functional-requirements','requirements-traceability-matrix','requirements-management','stakeholder-analysis','stakeholder-mapping','stakeholder-engagement','raci-chart','gap-analysis','swot-analysis','decision-tree','decision-table','weighted-scoring-model','kano-model','moscow-prioritization','business-case','cost-benefit-analysis','multi-criteria-decision-analysis','process-improvement','business-process-mapping','root-cause-analysis','fishbone-diagram','five-whys','functional-decomposition','context-diagram','use-case','risk-assessment','project-scope','executive-summary','project-report','communication-plan','project-proposal']:
 urls['atl_'+k]=a+k
for k in ['brainstorming','problem-framing','project-poster','roles-and-responsibilities','stakeholder-communications','trade-offs','dac','5-whys','disruptive-brainstorming']:
 urls['play_'+k]='https://www.atlassian.com/team-playbook/plays/'+k
for k in ['project-management/requirements','project-management/acceptance-criteria','project-management/user-stories','project-management/product-backlog','scrum/backlog-refinement','product-management/prioritization-framework','product-management/roadmaps','scrum/sprint-planning','scrum/standups','scrum/sprint-reviews','scrum/retrospectives']:
 urls['agile_'+k.replace('/','_')]='https://www.atlassian.com/agile/'+k
for k in ['interview-guide','stakeholder-interviews','discovery-workshops','surveys','survey-best-practices','contextual-inquiry','field-studies','focus-groups','wireframes','ux-prototype-hi-lo-fidelity','facilitating-ux-workshops','conflict-ux','ux-research-cheat-sheet','data-dashboards','data-visualization','presenting-to-stakeholders','documenting-ux-decisions']:
 urls['nn_'+k]='https://www.nngroup.com/articles/'+k+'/'
urls['scrum']='https://scrumguides.org/scrum-guide.html'
for k in ['tutorial-select','tutorial-agg','queries-table-expressions','datatype','functions-comparison','functions-conditional','queries-order','queries-limit','tutorial-window']:
 urls['pg_'+k]='https://www.postgresql.org/docs/current/'+k+'.html'
for k in ['fundamentals/desktop-getting-started','connect-data/desktop-shape-and-combine-data','transform-model/desktop-star-schema','transform-model/desktop-create-and-manage-relationships','visuals/power-bi-report-add-visualizations','create-reports/service-dashboards-design-tips','collaborate-share/service-share-dashboards','transform-model/desktop-measures','transform-model/desktop-calculated-columns','connect-data/service-datasets-understand','connect-data/desktop-data-sources']:
 urls['pbi_'+k.split('/')[-1]]='https://learn.microsoft.com/en-us/power-bi/'+k
for k in ['basicconnectoverview','joining_tables','extracting_data','dashboards_create','dashboards_best_practices','calculations_calculatedfields_create','calculations_calculatedfields_formulas','dm_relationships','datasource_datamodel','publish_workbooks_howto','visual_best_practices']:
 urls['tab_'+k]='https://help.tableau.com/current/pro/desktop/en-us/'+k+'.htm'
with concurrent.futures.ThreadPoolExecutor(max_workers=12) as ex: results=list(ex.map(fetch,urls.items()))
(P/'index.json').write_text(json.dumps(results,indent=2))
for r in results:print(*r)
