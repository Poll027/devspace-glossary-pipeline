exec(open('batches/glossary_batch_product_manager/working/crawl.py').read().split("if __name__")[0])
ls=[]
for f in base.glob('*.links.json'):ls+=json.load(open(f))
names='experiment-estimate-duration define-goals create-tracking-plan funnel-analysis experiment-learnings make-decision-experiment key-terms dashboard-reporting'.split()
items=[]
for n in names:
 a=next((a for a in ls if a['url'].split('?')[0].rstrip('/').endswith('/'+n) and '#' not in a['url']),None)
 if a:items.append({'source_id':'last_'+n,'url_or_citation':a['url']})
old=json.load(open(base/'fetch_index.json'));(base/'fetch_index.json').write_text(json.dumps(old+items,indent=2));run(items)
