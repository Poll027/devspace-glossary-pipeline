exec(open('batches/glossary_batch_product_manager/working/crawl.py').read().split("if __name__")[0])
ls=json.load(open(base/'pp_all_links.json'))
names='product-mission product-vision value-proposition competitive-landscape product-positioning product-strategy voice-of-customer total-addressable-market product-market-fit product-specs product-requirements-document acceptance-criteria user-flow release-plan dependency-management 2x2-prioritization-matrix rice-scoring-model ice-scoring-model weighted-scoring kano-model now-next-later-roadmap moscow-prioritization stakeholder-analysis stakeholder-management product-enablement technical-debt feature-flag a-b-test objectives-and-key-results leading-indicator lagging-indicator market-segmentation jobs-to-be-done'.split()
items=[]
for n in names:
 a=next((a for a in ls if a['url'].rstrip('/').endswith('/'+n)),None)
 if a:items.append({'source_id':'pp_'+n,'url_or_citation':a['url']})
 else:print('MISSING',n)
ls=json.load(open(base/'pichler_product-vision-and-strategy.links.json'))
for n in ['the-strategy-stack','my-product-strategy-model','how-to-choose-the-right-kpis-for-your-product','leading-through-shared-goals']:
 a=next(a for a in ls if a['url'].rstrip('/').endswith('/'+n));items.append({'source_id':'pichler_'+n,'url_or_citation':a['url']})
old=json.load(open(base/'fetch_index.json'));(base/'fetch_index.json').write_text(json.dumps(old+items,indent=2));run(items)
