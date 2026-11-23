exec(open('batches/glossary_batch_product_manager/working/fetch_sources.py').read().split('with concurrent')[0])
base=Path('batches/glossary_batch_product_manager/working/coverage_sources')
def run(items):
 with concurrent.futures.ThreadPoolExecutor(max_workers=12) as e:list(e.map(fetch,items))
if __name__=='__main__':
 links=json.load(open(base/'atlassian_agile.links.json'))
 names=['product-vision','product-strategy','product-specification','requirements','product-brief','product-planning','product-roadmaps','product-release','product-launch-checklist','product-launch-timeline','product-manager','product-design','prioritization-framework','minimum-viable-product','product-metrics','product-analytics','product-management-kpis','user-stories','velocity-scrum','estimation','project-management-dependencies','status-report','epics-stories-themes','risk-analysis','definition-of-done','backlog-refinement','wip-limits','boards','burndown-charts']
 items=[]
 for n in names:
  a=next((a for a in links if a['url'].rstrip('/').endswith('/'+n)),None)
  if a:items.append({'source_id':'atl_'+n,'url_or_citation':a['url']})
 for s,ns in [('nngroup_articles',['user-interviews','journey-mapping-101','usability-testing-101','affinity-diagram','how-might-we-questions','user-journeys-vs-user-flows','raw-data-vs-synthesized-data']),('pichler_blog',['product-vision-board','the-persona-template','offering-constructive-feedback-a-framework-for-product-people','product-vision-and-strategy','product-roadmap','stakeholder-management']),('amplitude_playbook',['product-north-star-metric','data-driven-data-informed-data-inspired','customer-cohort-analysis-vs-user-cohort-analysis','product-launch'])]:
  ls=json.load(open(base/(s+'.links.json')))
  for n in ns:
   a=next((a for a in ls if a['url'].rstrip('/').endswith('/'+n)),None)
   if a:items.append({'source_id':s.split('_')[0]+'_'+n,'url_or_citation':a['url']})
 items.append({'source_id':'pp_page2','url_or_citation':next(a['url'] for a in json.load(open(base/'productplan_glossary.links.json')) if 'page=2' in a['url'])})
 (base/'fetch_index.json').write_text(json.dumps(items,indent=2));run(items)
