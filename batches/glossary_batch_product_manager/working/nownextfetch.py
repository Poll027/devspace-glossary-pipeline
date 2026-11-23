exec(open('batches/glossary_batch_product_manager/working/crawl.py').read().split("if __name__")[0])
a=next(a for a in json.load(open(base/'gaps_blog-customer-feature-requests.links.json')) if 'invented-now-next-later' in a['url'])
x={'source_id':'extra_now-next-later','url_or_citation':a['url']};old=json.load(open(base/'fetch_index.json'));(base/'fetch_index.json').write_text(json.dumps(old+[x],indent=2));fetch(x)
