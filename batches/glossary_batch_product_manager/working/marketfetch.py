exec(open('batches/glossary_batch_product_manager/working/crawl.py').read().split("if __name__")[0])
x={'source_id':'market_tam-sam-som','url_or_citation':'https://foundationinc.co/lab/tam-sam-som'}
old=json.load(open(base/'fetch_index.json'));(base/'fetch_index.json').write_text(json.dumps(old+[x],indent=2));fetch(x)
