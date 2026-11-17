import json, hashlib, datetime, pathlib, re, subprocess, concurrent.futures, urllib.parse
B=pathlib.Path('batches/glossary_batch_machine_learning_engineer')
CORE=pathlib.Path('00_GLOSSARY_PIPELINE_CORE')
def load(p): return json.loads(pathlib.Path(p).read_text())
vs=load(B/'working/video_catalog_index.json')
# Catalogue title review, tile order. Values are indices into the immutable title index.
plans={
0:[17146],1:[5329,6454],2:[5291,5322],3:[5326,6450],4:[16291,5318],5:[20473],6:[16294,17141],7:[],8:[5314,16293],9:[44318],10:[],11:[20542,19767],12:[20592],13:[20429,20575],14:[20539,52003],15:[19361,20355],16:[19940,19361],17:[20051],18:[44634],19:[52480,20621],20:[19741],21:[],22:[17144],23:[5080,19795],24:[20195,52089],25:[20651,17144],26:[52107],27:[44318],28:[44318],29:[10729,19830],30:[],31:[52112,52496],32:[20619,20354],33:[52414],34:[],35:[30258,28588],36:[30251,28546],37:[30244,28585],38:[30257,28571],39:[30248,52046],40:[28521,30254],41:[30254,28550],42:[],43:[30232,28508],44:[],45:[20562,20563],46:[],47:[],48:[],49:[40898],50:[],51:[30240,28492],52:[28549,16487],53:[19222],54:[],55:[10729],56:[10729],57:[10729,20072],58:[17144],59:[20036,40340],60:[16265,16269],61:[30163,20032],62:[],63:[],64:[331,1801],65:[30163],66:[16258,16259],67:[22522,32569],68:[5286],69:[],70:[],71:[],72:[],73:[17107],74:[16252],75:[10729],76:[43041,40834],77:[10729],78:[],79:[10729],80:[17178],81:[17178],82:[17178],83:[17178],84:[],85:[],86:[],87:[],88:[],89:[],90:[],91:[],92:[],93:[],94:[]}
queries={
0:'machine learning problem framing prediction time target leakage',5:'pandas read csv chunksize memory tutorial',7:'pandera dataframe schema validation tutorial',9:'machine learning sampling selection bias explained',10:'machine learning label quality data labeling validation',12:'sklearn SimpleImputer fit training data tutorial',17:'time series feature engineering prevent data leakage',18:'machine learning data privacy security training data',20:'machine learning model acceptance criteria validation metrics',21:'sklearn DummyClassifier DummyRegressor baseline tutorial',22:'machine learning model selection accuracy latency cost',26:'machine learning error analysis tutorial',27:'machine learning subgroup slice evaluation fairness',28:'machine learning fairness mitigation tutorial fairlearn',30:'pytorch reproducibility random seeds tutorial',33:'model cards machine learning limitations documentation',34:'evaluate pretrained model outputs baseline validation metrics',42:'pytorch model train eval no_grad explained',44:'pytorch early stopping validation loss tutorial',46:'pytorch model tensors to device cuda tutorial',47:'pytorch batch size GPU memory tutorial',48:'pytorch cuda out of memory diagnosis tutorial',49:'pytorch profiler tutorial data loading bottleneck',50:'CPU GPU machine learning training benchmark choose hardware',53:'DVC dataset version control tutorial',54:'machine learning reproducibility pip requirements git environment',55:'MLflow reproduce experiment run tutorial',56:'MLflow model registry register version tutorial',58:'machine learning final test set evaluation baseline',62:'SageMaker batch transform inference tutorial',63:'machine learning model serving readiness health check',65:'machine learning model deployment smoke test',68:'locust load testing API tutorial latency',69:'model inference dynamic batching latency throughput explained',70:'gunicorn machine learning workers concurrency tutorial',71:'SageMaker endpoint autoscaling tutorial',72:'MLflow model registry rollback model version tutorial',73:'great expectations data validation pipeline tutorial',74:'machine learning model testing pytest preprocessing tutorial',75:'MLflow model validation deployment quality gate tutorial',77:'MLflow model registry aliases promotion staging tutorial',78:'SageMaker pipelines retry failed step tutorial',79:'MLflow model lineage data run version tutorial',80:'Evidently AI input prediction distribution monitoring tutorial',81:'data drift concept drift model performance degradation explained',82:'Evidently AI data drift detection tutorial',83:'machine learning monitoring delayed labels performance',84:'Evidently AI monitoring alerts tutorial',85:'machine learning production model monitoring troubleshooting drift',86:'machine learning retraining triggers drift scheduled retraining',87:'SageMaker pipeline scheduled retraining EventBridge tutorial',88:'machine learning pipeline idempotency duplicate retraining execution',89:'machine learning retraining model validation champion challenger',90:'MLOps model incident response runbook rollback',91:'GPU CPU memory utilization monitoring machine learning tutorial',92:'AWS cost allocation tags machine learning SageMaker cost',93:'AWS Budgets tutorial cost alerts',94:'SageMaker delete endpoint cleanup resources tutorial'}

def get_search(n,q):
 p=B/'working'/f'open_search_{n:02d}.html'
 url='https://www.youtube.com/results?search_query='+urllib.parse.quote(q)
 if not p.exists():
  r=subprocess.run(['curl','-sL','--max-time','35','-A','Mozilla/5.0',url,'-o',str(p)],capture_output=True)
 text=p.read_text() if p.exists() else ''
 m=re.search(r'var ytInitialData = (.*?);</script>',text)
 if not m:return n,[]
 data=json.loads(m.group(1));out=[]
 def walk(x):
  if isinstance(x,dict):
   if 'lockupViewModel' in x and x['lockupViewModel'].get('contentType')=='LOCKUP_CONTENT_TYPE_VIDEO':
    v=x['lockupViewModel'];vid=v.get('contentId');md=v['metadata']['lockupMetadataViewModel']
    title=md.get('title',{}).get('content','')
    avatar=md.get('image',{}).get('decoratedAvatarViewModel',{})
    by=avatar.get('rendererContext',{}).get('commandContext',{}).get('onTap',{}).get('innertubeCommand',{})
    cid=by.get('browseEndpoint',{}).get('browseId');channel=avatar.get('a11yLabel','').removeprefix('Go to channel ')
    cmd=v.get('rendererContext',{}).get('commandContext',{}).get('onTap',{}).get('innertubeCommand',{})
    if not cmd:cmd=v.get('itemPlayback',{}).get('inlinePlayerData',{}).get('onSelect',{}).get('innertubeCommand',{})
    result_url=cmd.get('commandMetadata',{}).get('webCommandMetadata',{}).get('url','')
    dur=''
    for ov in v.get('contentImage',{}).get('thumbnailViewModel',{}).get('overlays',[]):
     for badge in ov.get('thumbnailBottomOverlayViewModel',{}).get('badges',[]):
      txt=badge.get('thumbnailBadgeViewModel',{}).get('text','')
      if re.fullmatch(r'[0-9]+(?::[0-9]+)+',txt):dur=txt
    if vid and cid and dur and '/watch?v='+vid in result_url:
     seconds=0
     for t in dur.split(':'):seconds=seconds*60+int(t)
     out.append(dict(video_id=vid,title=title,channel_id=cid,channel_name=channel,duration_seconds=seconds,result_url='https://www.youtube.com'+result_url,query=q))
   if 'videoRenderer' in x:
    v=x['videoRenderer'];vid=v.get('videoId');by=v.get('ownerText',{}).get('runs',[{}])[0]
    title=''.join(z.get('text','') for z in v.get('title',{}).get('runs',[]));dur=v.get('lengthText',{}).get('simpleText','')
    # URL supplied by real search navigation, verified rather than remembered.
    result_url=v.get('navigationEndpoint',{}).get('commandMetadata',{}).get('webCommandMetadata',{}).get('url','')
    if not vid or not dur or '/watch?v='+vid not in result_url:return
    parts=dur.split(':')
    if not all(t.isdigit() for t in parts):return
    seconds=0
    for t in parts:seconds=seconds*60+int(t)
    cid=by.get('navigationEndpoint',{}).get('browseEndpoint',{}).get('browseId')
    if cid:out.append(dict(video_id=vid,title=title,channel_id=cid,channel_name=by.get('text',''),duration_seconds=seconds,result_url='https://www.youtube.com'+result_url,query=q))
   for v in x.values():walk(v)
  elif isinstance(x,list):
   for v in x:walk(v)
 walk(data)
 seen=set();out=[v for v in out if not (v['video_id'] in seen or seen.add(v['video_id']))]
 return n,out[:8]

if __name__=='__main__':
 jobs=[(n,queries[n]) for n in plans if len(plans[n])<2]
 assert all(n in queries for n in plans if len(plans[n])<2)
 results=dict(concurrent.futures.ThreadPoolExecutor(max_workers=6).map(lambda z:get_search(*z),jobs))
 (B/'working/open_search_results.json').write_text(json.dumps(results,indent=2))
 for n,rows in sorted(results.items()):
  print('\nCONCEPT',n,queries[n])
  for j,v in enumerate(rows):print(j,'|',v['channel_name'],'|',v['duration_seconds'],'|',v['title'])
