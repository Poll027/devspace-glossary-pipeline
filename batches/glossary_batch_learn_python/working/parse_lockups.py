import json,re,pathlib
B=pathlib.Path('batches/glossary_batch_learn_python/working');out=json.load(open(B/'open_search_results.json'))
def objects(x):
 if isinstance(x,dict):
  yield x
  for v in x.values():yield from objects(v)
 elif isinstance(x,list):
  for v in x:yield from objects(v)
for short,d in out.items():
 if d['results']:continue
 h=(B/('search_'+short+'.html')).read_text();m=re.search(r'var ytInitialData\s*=\s*',h);data=json.JSONDecoder().raw_decode(h[m.end():])[0]
 for obj in objects(data):
  if 'lockupViewModel' not in obj:continue
  v=obj['lockupViewModel']
  try:
   title=v['metadata']['lockupMetadataViewModel']['title']['content'];oo=list(objects(v))
   watch=next(z['url'] for z in oo if isinstance(z.get('url'),str) and re.search(r'^/watch\?v=[\w-]{11}',z['url']))
   vid=re.search(r'[?&]v=([\w-]{11})',watch).group(1)
   channel=next(z['a11yLabel'].replace('Go to channel ','') for z in oo if z.get('a11yLabel','').startswith('Go to channel '))
   chid=next(z['browseId'] for z in oo if z.get('browseId','').startswith('UC'))
   duration=next(z['text'] for z in objects(v['contentImage']) if isinstance(z.get('text'),str) and re.fullmatch(r'\d+(?::\d+)+',z['text']))
   secs=0
   for t in duration.split(':'):secs=secs*60+int(t)
   if vid not in [r['video_id'] for r in d['results']]:d['results'].append(dict(video_id=vid,result_url='https://www.youtube.com'+watch,title=title,channel_id=chid,channel_name=channel,duration_seconds=secs))
  except (KeyError,StopIteration):continue
  if len(d['results'])>=12:break
 print('\n'+short)
 for i,v in enumerate(d['results']):print(i,v['video_id'],v['channel_name'],v['duration_seconds'],v['title'])
json.dump(out,open(B/'open_search_results.json','w'),indent=2)
