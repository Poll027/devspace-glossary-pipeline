exec(open('batches/glossary_batch_product_manager/working/crawl.py').read().split("if __name__")[0])
for n in range(3,13):
 ls=json.load(open(base/('pp_page%d.links.json'%(n-1))))
 a=next((a for a in ls if 'page='+str(n) in a['url']),None)
 if not a:break
 fetch({'source_id':'pp_page%d'%n,'url_or_citation':a['url']})
ls=[]
for f in [base/'productplan_glossary.links.json']+list(base.glob('pp_page*.links.json')):ls+=json.load(open(f))
(base/'pp_all_links.json').write_text(json.dumps(ls,indent=2))
print('\n'.join(sorted(set(a['url'] for a in ls if '/glossary/' in a['url'] and '?' not in a['url']))))
