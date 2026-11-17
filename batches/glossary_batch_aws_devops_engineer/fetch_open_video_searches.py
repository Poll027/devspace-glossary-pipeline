from discover_video_candidates import *
import subprocess,urllib.parse,concurrent.futures
WORK=B/'working/video_search'
WORK.mkdir(parents=True,exist_ok=True)
def text(x):
 return x.get('simpleText') or ''.join(z['text'] for z in x.get('runs',[]))
def walk(x):
 if isinstance(x,dict):
  if 'videoRenderer' in x:yield x['videoRenderer']
  if 'lockupViewModel' in x:yield x['lockupViewModel']
  for v in x.values():yield from walk(v)
 elif isinstance(x,list):
  for v in x:yield from walk(v)
def fetch(item):
 ix,q=item;p=WORK/(ix+'.html')
 if not p.exists():
  url='https://www.youtube.com/results?search_query='+urllib.parse.quote_plus(q)+'&hl=en'
  subprocess.run(['curl','-sL','--max-time','35',url,'-o',str(p)],check=True)
 raw=p.read_text();m=re.search(r'(?:var )?ytInitialData\s*=\s*',raw)
 if m:d=json.JSONDecoder().raw_decode(raw[m.end():])[0]
 else:
  m=re.search(r'<script id="yt-initial-data"[^>]*>',raw)
  if not m:return ix,[]
  d=json.JSONDecoder().raw_decode(raw[m.end():])[0]
 vs=[];ids=set()
 for v in walk(d):
  if v.get('contentType')=='LOCKUP_CONTENT_TYPE_VIDEO':
   md=v['metadata']['lockupMetadataViewModel']; cid=None
   img=md.get('image',{}).get('decoratedAvatarViewModel',{})
   cid=img.get('rendererContext',{}).get('commandContext',{}).get('onTap',{}).get('innertubeCommand',{}).get('browseEndpoint',{}).get('browseId')
   title=md['title']['content']; name=img.get('a11yLabel','').removeprefix('Go to channel ')
   badges=v.get('contentImage',{}).get('thumbnailViewModel',{}).get('overlays',[])
   length=''
   for ov in badges:
    for z in ov.get('thumbnailBottomOverlayViewModel',{}).get('badges',[]):
     length=z.get('thumbnailBadgeViewModel',{}).get('text','')
   if cid and re.fullmatch(r'[0-9:]+',length):
    duration=0
    for z in length.split(':'):duration=duration*60+int(z)
    vid=v['contentId']
    if vid not in ids:
     ids.add(vid);vs.append({'video_id':vid,'title':title,'channel_id':cid,'channel_name':name,'duration_seconds':duration})
   continue
  vid=v.get('videoId');length=text(v.get('lengthText',{}));owner=v.get('ownerText') or v.get('longBylineText',{})
  if not vid or vid in ids or not length or not owner.get('runs'):continue
  ids.add(vid);rn=owner['runs'][0];cid=rn.get('navigationEndpoint',{}).get('browseEndpoint',{}).get('browseId')
  if not cid:continue
  try:
   duration=0
   for x in length.split(':'):duration=duration*60+int(x)
  except ValueError:continue
  vs.append({'video_id':vid,'title':text(v['title']),'channel_id':cid,'channel_name':text(owner),'duration_seconds':duration})
  if len(vs)>=16:break
 return ix,vs
if __name__=='__main__':
 qs=load(B/'open_search_queries.json');choices=load(B/'catalogue_choices.json')
 assert all(len(choices[k])<2 for k in qs)
 with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:results=dict(ex.map(fetch,qs.items()))
 (B/'open_search_results.json').write_text(json.dumps(results,indent=2))
 for ix,vs in results.items():
  print('\n',ix,qs[ix])
  for j,v in enumerate(vs):print(j,v['video_id'],v['channel_name'],v['duration_seconds'],v['title'])
