import json,subprocess,concurrent.futures,re,html
from pathlib import Path
root=Path('batches/glossary_batch_flutter_mobile_developer/working/coverage_sources')
p=json.load(open('00_GLOSSARY_PIPELINE_CORE/source_packs/flutter_mobile_developer.source_pack.json'))
def fetch(x):
 id,url=x
 r=subprocess.run(['curl','-sL','--max-time','45',url],capture_output=True,text=True).stdout
 (root/(id+'.html')).write_text(r)
 r=re.sub(r'<(script|style).*?</\1>','',r,flags=re.S)
 r=re.sub(r'</(?:p|div|li|pre|h[1-6]|section|tr)>','\n',r)
 r=html.unescape(re.sub('<[^>]+>','',r));r=re.sub(r'[ \t]+',' ',r);r=re.sub(r'\n\s*\n','\n',r)
 (root/(id+'.txt')).write_text(r)
 return id,len(r)
with concurrent.futures.ThreadPoolExecutor(max_workers=12) as ex:
 for a in ex.map(fetch,[(s['source_id'],s['url_or_citation']) for s in p['sources']]):print(*a)
