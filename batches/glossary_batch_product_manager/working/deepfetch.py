exec(open('batches/glossary_batch_product_manager/working/crawl.py').read().split("if __name__")[0])
ls=[]
for f in base.glob('*.links.json'):ls+=json.load(open(f))
names='finalize-statistical-preferences Working-with-feature-flags-and-feature-rollouts Analyze-A-B-test-results-in-Amplitude event-taxonomy quarterly-planning goal-alignment cost-benefit-analysis go-to-market-strategy'.split()
items=[]
for n in names:
 a=next((a for a in ls if a['url'].split('?')[0].rstrip('/').endswith(n) and '#' not in a['url'] and ('atlassian.com' in a['url'] if n=='go-to-market-strategy' else True)),None)
 if a:items.append({'source_id':'deep_'+n,'url_or_citation':a['url']})
 else:print('MISSING',n)
old=json.load(open(base/'fetch_index.json'));(base/'fetch_index.json').write_text(json.dumps(old+items,indent=2));run(items)
