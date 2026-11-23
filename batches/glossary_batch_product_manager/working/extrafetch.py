exec(open('batches/glossary_batch_product_manager/working/crawl.py').read().split("if __name__")[0])
ls=[]
for f in base.glob('*.links.json'):ls+=json.load(open(f))
names=['mission-and-vision','jobs-to-be-done-framework','leading-lagging-indicators','customer-surveys','formal-vs-quick-usability-reports','leading-questions','should-you-run-a-survey','now-next-later','product-mission']
items=[]
for n in names:
 a=next((a for a in ls if a['url'].split('?')[0].rstrip('/').endswith('/'+n) and ('/learn/' in a['url'] if n=='product-mission' else True)),None)
 if a:items.append({'source_id':'extra_'+n,'url_or_citation':a['url']})
 else:print('MISSING',n)
# additional discovered pages, not generated URLs
for s,names in [('amplitude_playbook',['blog','funnels','track']),('nngroup_articles',['research-methods','personas','ux-ideation'])]:
 l=json.load(open(base/(s+'.links.json')))
 for n in names:
  a=next((a for a in l if a['url'].rstrip('/').endswith('/'+n)),None)
  if a:items.append({'source_id':'extra_'+s+'_'+n,'url_or_citation':a['url']})
old=json.load(open(base/'fetch_index.json'));(base/'fetch_index.json').write_text(json.dumps(old+items,indent=2));run(items)
