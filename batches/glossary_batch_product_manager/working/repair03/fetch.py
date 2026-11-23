import subprocess,concurrent.futures,re,json
from html.parser import HTMLParser
from pathlib import Path
class Text(HTMLParser):
 def __init__(self): super().__init__();self.skip=0;self.out=[]
 def handle_starttag(self,t,a):
  if t in ['script','style']:self.skip+=1
  if t in ['p','h1','h2','h3','h4','li','div','br']:self.out.append('\n')
 def handle_endtag(self,t):
  if t in ['script','style']:self.skip=max(0,self.skip-1)
 def handle_data(self,d):
  if not self.skip:self.out.append(d)
def fetch(pair):
 key,url=pair
 s=subprocess.check_output(['curl','-sL','--max-time','45',url]).decode(errors='replace'); p=Text();p.feed(s);s=re.sub(r'[ \t]+',' ',''.join(p.out));s=re.sub(r'\n\s*\n','\n',s)
 Path('batches/glossary_batch_product_manager/working/repair03/'+key+'.txt').write_text(url+'\n'+s)
 print(key,len(s))
urls={
'values':'https://www.atlassian.com/work-management/strategic-planning/core-values',
'position':'https://www.productplan.com/learn/positioning-statement/',
'jtbd':'https://www.atlassian.com/agile/product-management/jobs-to-be-done',
'market':'https://www.atlassian.com/work-management/strategic-planning/tam-sam-som',
'pmf':'https://amplitude.com/blog/product-market-fit',
'release':'https://www.atlassian.com/agile/product-management/release-planning',
'releasemgmt':'https://www.atlassian.com/agile/software-development/release-management',
'funnel':'https://amplitude.com/blog/funnel-analysis',
'funneldoc':'https://amplitude.com/docs/analytics/charts/funnel-analysis/funnel-analysis-interpret',
'ab':'https://amplitude.com/docs/feature-experiment/workflow/experiment-learnings',
'flags':'https://amplitude.com/docs/feature-experiment/workflow/management-api',
'progressive':'https://www.atlassian.com/continuous-delivery/principles/feature-flags',
'holdout':'https://amplitude.com/docs/feature-experiment/advanced-techniques/holdout-groups-exclude-users',
'daci':'https://www.atlassian.com/team-playbook/plays/daci',
'severity':'https://www.nngroup.com/articles/how-to-rate-the-severity-of-usability-problems/',
'jobold':'https://www.productplan.com/glossary/jobs-to-be-done-framework/',
'ice':'https://www.productplan.com/glossary/ice-scoring-model/'
}
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as e:list(e.map(fetch,urls.items()))
