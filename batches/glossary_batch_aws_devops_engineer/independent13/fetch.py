import json,urllib.parse,subprocess,concurrent.futures,re,pathlib
p=pathlib.Path('batches/glossary_batch_aws_devops_engineer');q=p/'independent13'
s={x['source_id']:x['url_or_citation'] for x in json.load(open('00_GLOSSARY_PIPELINE_CORE/source_packs/aws_devops_engineer.source_pack.json'))['sources']}
refs=sorted({r for b in json.load(open(p/'coverage_briefs.json'))['briefs'] for f in b['evidence']['required_facts'] for r in f['source_refs']})
def go(item):
 i,r=item;a,*z=r.split('#',1);u=s[a];u=u+'/' if '.' not in urllib.parse.urlparse(u).path.rsplit('/',1)[-1] and not u.endswith('/') else u;u=urllib.parse.urljoin(u,z[0].split('#')[0]) if z and z[0].split('#')[0] else u
 
 if a in ['git_docs','github_actions_docs','terraform_aws_provider'] and z:u=s[a].rstrip('/')+'/'+z[0].split('#')[0]
 raw=subprocess.run(['curl','-sL','--max-time','40',u],capture_output=True).stdout.decode(errors='replace');raw=re.sub(r'<script\b.*?</script>|<style\b.*?</style>','',raw,flags=re.S|re.I);raw=re.sub('<[^>]+>',' ',raw);import html;raw=html.unescape(raw);raw=re.sub(r'\s+',' ',raw)
 (q/f's{i}.txt').write_text(u+'\n'+raw);return {'i':i,'ref':r,'url':u,'chars':len(raw)}
with concurrent.futures.ThreadPoolExecutor(max_workers=20) as pool:out=list(pool.map(go,enumerate(refs)))
(q/'sources.json').write_text(json.dumps(out,indent=2));print('FETCHED',len(out));print([o for o in out if o['chars']<500])
