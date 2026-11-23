exec(open('batches/glossary_batch_business_analyst/working/discover_videos.py').read().split('short={}')[0])
import urllib.parse
selections=load(B/'working/catalog_selection.json')
selections['53']=['3dtDbmXFJWs','DUNccXcuOOs']; (B/'working/catalog_selection.json').write_text(json.dumps(selections,indent=2))
segments={s['segment_id']:s for s in load(B/'approved_segments_snapshot.json')['segments']};lookup={l['concept_id']:l for l in r['lookups']}
queries={2:'business analysis facilitated requirements workshop tutorial',5:'business analysis observation contextual inquiry techniques tutorial',9:'focus groups moderation techniques tutorial',10:'risk identification probability impact matrix tutorial',15:'requirements traceability matrix tutorial business analyst',16:'requirements lifecycle management Confluence page history tutorial',19:'stakeholder power interest matrix explained',20:'RACI matrix explained tutorial',22:'meeting workshop facilitation techniques tutorial',23:'consensus building conflict resolution facilitation tutorial',24:'BPMN 2.0 tutorial beginner process modeling',25:'as is business process modeling BPMN tutorial',26:'to be business process modeling BPMN tutorial',27:'business process bottleneck analysis tutorial',28:'business process improvement lean six sigma tutorial',30:'business rules decision tables tutorial',31:'business rules decision tree diagram tutorial',35:'one to many database relationships explained',36:'many to many junction table database explained',37:'entity relationship diagrams cardinality explained',38:'entity relationship diagram tutorial beginner',59:'Kano model requirements prioritization explained',60:'weighted scoring decision matrix tutorial',61:'business analyst solution options evaluation decision matrix tutorial',62:'business case development cost benefits tutorial',63:'multi criteria decision analysis weighted scoring tutorial',68:'agile phased delivery release planning story mapping tutorial',72:'stakeholder business presentation structure tutorial',73:'business analyst requirements walkthrough demonstration',74:'business analysis context diagram tutorial',75:'business analysis functional decomposition diagram tutorial',79:'Excel nested IF IFS functions tutorial',85:'sprint review meeting demonstration tutorial',87:'five whys root cause analysis example',88:'fishbone diagram root cause analysis example',93:'Tableau dashboard beginner tutorial',95:'Power BI publish share reports permissions tutorial',98:'Power BI semantic model shared dataset Build permission tutorial'}
tasks=[(15,'requirements traceability matrix tutorial'),(28,'process improvement techniques explained'),(37,'ER diagram cardinality tutorial'),(74,'context diagram business analysis'),(87,'5 whys root cause analysis example'),(73,'requirements walkthrough review meeting business analyst')]
def text(n):return n.get('simpleText','') or ''.join(r.get('text','') for r in n.get('runs',[]))
def fetch(task):
 idx,q=task; dest=B/f'working/open_search_{idx}.html';url='https://www.youtube.com/results?search_query='+urllib.parse.quote(q)
 subprocess.run(['curl','-sL','--max-time','35',url,'-o',str(dest)],check=True)
 s=dest.read_text();m=re.search(r'(?:var )?ytInitialData\s*=\s*',s)
 out=[]
 if m:
  d=json.JSONDecoder().raw_decode(s[m.end():])[0]
  def walk(n):
   if isinstance(n,dict):
    if 'videoRenderer' in n:
     v=n['videoRenderer'];runs=v.get('longBylineText',{}).get('runs',[]);dur=text(v.get('lengthText',{}))
     endpoint=v.get('navigationEndpoint',{}).get('commandMetadata',{}).get('webCommandMetadata',{}).get('url','')
     vid=urllib.parse.parse_qs(urllib.parse.urlparse(endpoint).query).get('v',[''])[0]
     if not vid or not runs or not re.fullmatch(r'\d+(?::\d+){1,2}',dur):return
     cid=runs[0].get('navigationEndpoint',{}).get('browseEndpoint',{}).get('browseId','')
     if not cid:return
     sec=0
     for n2 in dur.split(':'):sec=sec*60+int(n2)
     out.append({'video_id':vid,'title':text(v.get('title',{})),'channel_id':cid,'channel_name':text(v.get('longBylineText',{})),'duration_seconds':sec,'result_url':'https://www.youtube.com'+endpoint})
    for v in n.values():walk(v)
   elif isinstance(n,list):
    for v in n:walk(v)
  walk(d)
 unique={v['video_id']:v for v in out};return str(idx),list(unique.values())[:10]
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool: results=dict(pool.map(fetch,tasks))
prior=load(B/'working/open_results.json'); prior.update(results); results=prior
(B/'working/open_results.json').write_text(json.dumps(results,indent=2))
for idx,q in tasks:
 print('\n',idx,q)
 for v in results[str(idx)][:8]:print(v['video_id'],v['channel_name'],v['duration_seconds'],v['title'])
