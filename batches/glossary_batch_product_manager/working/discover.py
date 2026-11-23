exec(open('batches/glossary_batch_product_manager/working/crawl.py').read().split("if __name__")[0])
ls=[]
for f in base.glob('*.links.json'):ls+=json.load(open(f))
items=[]
for n in ['learn','product-roadmaps','experiment']:
 a=next((a for a in ls if a['url'].rstrip('/').endswith('/'+n) and (('productplan' in a['url']) if n!='experiment' else ('amplitude.com/docs' in a['url']))),None)
 if a:items.append({'source_id':'discover_'+n,'url_or_citation':a['url']})
old=json.load(open(base/'fetch_index.json'));(base/'fetch_index.json').write_text(json.dumps(old+items,indent=2));run(items)
for x in items:
 ls=json.load(open(base/(x['source_id']+'.links.json')))
 print(x['source_id']);print('\n'.join(sorted(set(a['url'] for a in ls if any(w in a['url'] for w in ['now-next','holdout','market-size','roadmap-types','roadmap-examples','feature-experiment'])))))
