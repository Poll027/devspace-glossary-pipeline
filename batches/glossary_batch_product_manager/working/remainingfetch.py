exec(open('batches/glossary_batch_product_manager/working/crawl.py').read().split("if __name__")[0])
ls=[]
for f in base.glob('*.links.json'):ls+=json.load(open(f))
names='sprint-reviews sprint-planning scope-creep vision-to-values product-critique'.split()
items=[]
for n in names:
 a=next(a for a in ls if a['url'].rstrip('/').endswith('/'+n));items.append({'source_id':'remain_'+n,'url_or_citation':a['url']})
old=json.load(open(base/'fetch_index.json'));(base/'fetch_index.json').write_text(json.dumps(old+items,indent=2));run(items)
