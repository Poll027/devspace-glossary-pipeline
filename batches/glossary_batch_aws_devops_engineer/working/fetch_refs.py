import json,sys,urllib.parse
sys.path.insert(0,'batches/glossary_batch_aws_devops_engineer/working')
from brief_data import DATA
import brief_data_more
import brief_fixes
import brief_final_fixes
from fetch_coverage import fetch
from concurrent.futures import ThreadPoolExecutor
ss={s['source_id']:s['url_or_citation'] for s in json.load(open('00_GLOSSARY_PIPELINE_CORE/source_packs/aws_devops_engineer.source_pack.json'))['sources']}
def url(ref):
 sid,loc=ref.split('#',1); base=ss[sid]
 if sid in ['terraform_language','terraform_aws_provider','github_actions_docs','git_docs']:base+='/'
 return sid,urllib.parse.urljoin(base,loc).split('#')[0]
 
if __name__=='__main__':
 jobs=set(url(ref) for fs in DATA.values() for _,ref in fs)
 from brief_final_fixes import EXTRA_REFS, MISCONCEPTIONS
 jobs.update(url(r) for refs in EXTRA_REFS.values() for r in refs)
 jobs.update(url(r) for fs in MISCONCEPTIONS.values() for _,r in fs)
 with ThreadPoolExecutor(max_workers=15) as ex:list(ex.map(fetch,jobs))
