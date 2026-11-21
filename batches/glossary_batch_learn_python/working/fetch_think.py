exec(open('batches/glossary_batch_learn_python/working/fetch_coverage_sources.py').read().split('with concurrent')[0])
def get(n):
 url=f'https://allendowney.github.io/ThinkPython/chap{n:02d}.html';p=Parser();p.feed(urllib.request.urlopen(url).read().decode());(P/f'think_chap{n:02d}.txt').write_text(''.join(p.out))
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:list(ex.map(get,range(19)))
for f in sorted(P.glob('think_chap*.txt')):
 t=f.read_text();paras=t.split('\n\n')
 for i,v in enumerate(paras):
  if re.search(r'(?i)hallucin|generated code|verify|trust|skepti|correct.*code|code.*correct|test.*requirement',v):print(f.name, v.strip()[:1800])
