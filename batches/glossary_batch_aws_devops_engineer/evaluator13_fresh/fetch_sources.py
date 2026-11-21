import json,urllib.parse,subprocess,concurrent.futures,pathlib
p=pathlib.Path('batches/glossary_batch_aws_devops_engineer/evaluator13_fresh');f=json.load(open(p.parent/'coverage_briefs.json'))['briefs'];sources={s['source_id']:s['url_or_citation'] for s in json.load(open('00_GLOSSARY_PIPELINE_CORE/source_packs/aws_devops_engineer.source_pack.json'))['sources']}
refs=sorted({r for b in f for x in b['evidence']['required_facts'] for r in x['source_refs']})
def fetch(z):
 i,r=z;sid,_,loc=r.partition('#');base=sources[sid];base=base+'/' if sid in ['github_actions_docs','terraform_language','git_docs','terraform_aws_provider'] and not base.endswith('/') else base;url=urllib.parse.urljoin(base,loc) if loc else base
 if sid=='terraform_docs' and loc:url=urllib.parse.urljoin('https://developer.hashicorp.com/terraform/',loc)
 raw=subprocess.run(['curl','-sL','--max-time','35',url],capture_output=True).stdout
 (p/f'source{i}.html').write_bytes(raw)
 if raw.startswith(b'%PDF'):
  (p/f'source{i}.pdf').write_bytes(raw);text=subprocess.run(['pdftotext',str(p/f'source{i}.pdf'),'-'],capture_output=True).stdout.decode(errors='replace')
 else:
  import re,html
  text=html.unescape(re.sub('<[^>]+>',' ',re.sub(r'<(script|style).*?</\1>','',raw.decode(errors='replace'),flags=re.S)));text=re.sub(r'\s+',' ',text)
 (p/f'source{i}.txt').write_text(text);return {'i':i,'ref':r,'url':url,'length':len(text)}
with concurrent.futures.ThreadPoolExecutor(max_workers=16) as pool:rows=list(pool.map(fetch,enumerate(refs)))
(p/'source_index.json').write_text(json.dumps(rows,indent=2))
print('fetched',len(rows),'empty',sum(x['length']<100 for x in rows))
