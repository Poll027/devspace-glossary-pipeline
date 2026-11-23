exec(open('batches/glossary_batch_product_manager/working/crawl.py').read().split("if __name__")[0])
ls=[]
for f in base.glob('*.links.json'):ls+=json.load(open(f))
items=[]
for n in ['backlogs','daily-stand-ups','retrospectives','trade-off-analysis','product-discovery-articles']:
 a=next((a for a in ls if a['url'].rstrip('/').endswith('/'+n)),None)
 if a:items.append({'source_id':'new_'+n,'url_or_citation':a['url']})
old=json.load(open(base/'fetch_index.json'));(base/'fetch_index.json').write_text(json.dumps(old+items,indent=2));run(items)
