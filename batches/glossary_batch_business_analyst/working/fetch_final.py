exec(open('batches/glossary_batch_business_analyst/working/fetch_sources.py').read().split('urls={}')[0])
urls={k:'https://www.atlassian.com/software/confluence/templates/'+k for k in ['gap-analysis','decision-matrix','data-flow-diagram']}
urls['rtm']='https://www.atlassian.com/software/jira/templates/requirements-traceability-matrix'
# Confirm links in the real Excel page and official help search landing.
u='https://support.microsoft.com/en-us/office/overview-of-formulas-in-excel-ecfdc708-9162-49e8-b993-c311f47ca173'
h=urllib.request.urlopen(u).read().decode()
for link in set(re.findall(r'href="([^"]+)"',h)):
 if any(x in link.lower() for x in ['sum-function','average-function','count-function','if-function','vlookup','xlookup','index-function','match-function','ifs-function','create-a-chart','absolute']):
  if link.startswith('/'):link='https://support.microsoft.com'+link
  if link.startswith('https://support.microsoft.com'):urls['excel_'+link.split('/')[-1]]=link
# Additional official pages are followed from the Excel documentation hub/search results.
for k,u in list(urls.items()):pass
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:results=list(ex.map(fetch,urls.items()))
(P/'index_final.json').write_text(json.dumps(results,indent=2));print('\n'.join(map(str,results)))
