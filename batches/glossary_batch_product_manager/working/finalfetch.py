exec(open('batches/glossary_batch_product_manager/working/crawl.py').read().split("if __name__")[0])
ls=[]
for f in base.glob('*.links.json'):ls+=json.load(open(f))
names='survey-best-practices personas-archetypes conflict-resolution-tips-product-managers-product-owners how-to-leverage-conflict-in-product-management decision-rules-to-make-better-product-decisions unanimity-based-product-decisions communication-plan stakeholder-communication cross-functional-teams tips-for-presenting-product-roadmaps go-to-market-strategy amplitude-experiment analytics-product-market-fit'.split()
items=[]
for n in names:
 a=next((a for a in ls if a['url'].split('?')[0].rstrip('/').endswith('/'+n) and '#' not in a['url']),None)
 if a:items.append({'source_id':'more_'+n,'url_or_citation':a['url']})
 else:print('MISSING',n)
old=json.load(open(base/'fetch_index.json'));(base/'fetch_index.json').write_text(json.dumps(old+items,indent=2));run(items)
