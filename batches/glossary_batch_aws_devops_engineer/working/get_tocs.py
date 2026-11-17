import json,urllib.request,urllib.parse,concurrent.futures
from pathlib import Path
p=Path('batches/glossary_batch_aws_devops_engineer/working/coverage_sources')
sources=json.load(open('00_GLOSSARY_PIPELINE_CORE/source_packs/aws_devops_engineer.source_pack.json'))['sources']
def go(s):
 if not s['url_or_citation'].startswith('https://docs.aws.amazon.com/'):return
 u=urllib.parse.urljoin(s['url_or_citation'],'toc-contents.json')
 try:
  d=json.load(urllib.request.urlopen(u,timeout=25));(p/(s['source_id']+'.toc.json')).write_text(json.dumps(d))
 except Exception as e:print(e)
with concurrent.futures.ThreadPoolExecutor(max_workers=12) as ex:list(ex.map(go,sources))
