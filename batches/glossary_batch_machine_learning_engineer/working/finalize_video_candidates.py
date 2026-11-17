import importlib.util, json, pathlib, hashlib, datetime, collections, re
B=pathlib.Path('batches/glossary_batch_machine_learning_engineer'); CORE=pathlib.Path('00_GLOSSARY_PIPELINE_CORE')
def module(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=module('build',B/'build_video_candidates.py');sel=module('select',B/'working/video_selection.py')
def load(p):return json.loads(pathlib.Path(p).read_text())
e=load(B/'extracted_concepts.json');g=load(B/'glossary_pass_a.json');briefs=load(B/'coverage_briefs.json');reg=load(B/'registry_lookup.json')
assert not any(x['reusable_segment_ids'] for x in reg['lookups']), 'Reuse route needs resolving before catalogue search'
gby={(x['concept_id'],x['path_id']):x for x in g['entries']};bby={(x['concept_id'],x['path_id']):x for x in briefs['briefs']};rby={(x['concept_id'],x['path_id']):x for x in reg['lookups']}
first=load(B/'working/open_search_results.json');second=load(B/'working/open_search_refined_results.json')
initial_counts={n:len(v) for n,v in m.plans.items()}
# Additional title matches resolved during fallback review, recorded with their real provenance.
m.plans[7]=[24933];m.plans[44]=[28541];m.plans[46]=[20043]
m.plans[80]=[17178,19239];m.plans[82]=[17178,19239];m.plans[86]=[19998]
m.plans[34]=[52480]
# Avoid treating general preprocessing composition as title evidence for imputation.
m.plans[12]=[20592]
CAT_REASON={
0:'The supervised-ML introductory title may explain inputs and target outputs for a prediction task; retain task framing only, not modeling algorithms.',
1:'The NumPy array/shape title offers a plausible concrete axis/shape example for boundary validation; explicit contract checks still need transcript confirmation.',
2:'The NumPy teaching title is plausible for dtype inspection/casting and element-storage examples; precision-loss checks must be verified later.',
3:'The title directly teaches NumPy broadcasting, matching compatible vectorized array operations.',
4:'The pandas file-reading title may supply a concrete dataset read/access example; storage-format/access-pattern tradeoffs need later confirmation.',
5:'The pandas CSV-parameter tutorial may demonstrate bounded reading options; require a chunksize example rather than unbounded loading.',
6:'The pandas exploration title may show dataset structure and aggregate distributions; memory inspection is not established by the title alone.',
7:'The title explicitly demonstrates validating pandas data with Pandera, matching a model-facing schema check.',
8:'The pandas cleaning title may show invalid/missing observations and data-type checks; require an explicit cleaning-policy example rather than blindly dropping rows.',
9:'The technical title covers ML bias/fairness, a possible dataset-representation example; sampling bias must not be conflated with fitting bias.',
11:'The title directly contrasts split/cross-validation strategies, matching the choice of evaluation partitions; deployment/time/group matching must be verified later.',
12:'The missing-data instructional title may show imputation; keep only a training-fitted transform and reject any fit on held-out data at the transcript gate.',
13:'The title directly teaches feature scaling, matching numerical transformations; train-only fitting must be confirmed at segment review.',
14:'The title directly explains categorical encoding, matching concrete category representation; unseen-category policy requires transcript confirmation.',
15:'The title explicitly builds sklearn pipelines, matching reusable fitted preprocessing composition.',
16:'The title is plausible for leakage diagnosis or preprocessing fit boundaries; require an explicit leakage-safe example and exclude later tuning topics.',
17:'The feature-engineering title offers a task-feature example; keep only prediction-time information and verify no outcome leakage.',
18:'The technical ML-environment security title may explain protection of sensitive ML assets; exclude platform provisioning and advanced attack/defense research.',
19:'The title explicitly teaches ML evaluation metrics, matching task-appropriate classification/regression measurement.',
20:'The title directly contrasts false-positive and false-negative priorities, a plausible task-cost rationale for acceptance metrics; numeric acceptance gates are not established yet.',
22:'The title explicitly describes model selection, a plausible validation-evidence decision example; latency/cost comparisons need separate confirmation.',
23:'The practical regression/sklearn-methods title may show the fit/predict estimator workflow; exclude algorithm internals and tuning.',
24:'The title directly concerns binary thresholds or ROC/AUC, a plausible threshold tradeoff illustration; the cut must use validation rather than the protected test.',
25:'The model-selection/cross-validation title may compare validation results between candidates; do not infer a final protected-test result.',
26:'The confusion-matrix title provides a concrete prediction-error breakdown; seek only inspection of failures, not a new metric-selection lesson.',
27:'The technical bias/fairness title may show performance comparisons across groups; concrete slice metrics and denominators still require confirmation.',
28:'The technical fairness title may discuss responses to documented subgroup risks; require practical bounded mitigation rather than general social commentary.',
29:'The MLflow instructional title may show runs, parameter/metric tracking and artifacts; require a short concrete run-logging demonstration, not the entire course.',
31:'The regularization title directly targets overfitting responses; require a validation-based choice and avoid deeper algorithm derivations.',
32:'The sklearn tuning title directly teaches bounded hyperparameter search; require a finite search using validation without protected-test access.',
33:'The model-card title directly concerns model documentation, a plausible limitations/intended-use example; its short duration may cover only part of the required facts.',
34:'The ML evaluation title may support scoring supplied pretrained-task outputs without teaching foundation-model application construction; a task-specific baseline remains unconfirmed.',
35:'The title directly introduces PyTorch tensors, a plausible shape/dtype construction example.',
36:'The title explicitly implements PyTorch DataLoaders/batch training, matching dataset and minibatch-loader mechanics.',
37:'The PyTorch feed-forward/linear-layer title may show nn.Module and task-compatible outputs; exclude training, gradients and optimizer setup from this early model-definition cut.',
38:'The title explicitly demonstrates PyTorch automatic differentiation, matching gradient calculation.',
39:'The title directly teaches cross entropy, a plausible classification loss example; require correct task/output-target compatibility.',
40:'The PyTorch optimizer/training-pipeline title may show optimizer and learning-rate configuration; restrict the cut to configuration rather than the later training loop.',
41:'The PyTorch training-pipeline/code-example title may show forward/backward/step mechanics; select a minibatch loop rather than unrelated network architecture.',
43:'The title explicitly saves and loads PyTorch models, matching persisted weights and restored prediction behavior.',
44:'The title explicitly teaches early stopping, matching validation-observed stopping without protected-test access.',
45:'The title directly explains exploding/vanishing gradients, matching diagnostic patterns in failed neural training; exclude architectural remedies beyond the supplied baseline.',
46:'The title explicitly runs PyTorch code on GPU with CUDA, matching compatible model/tensor placement.',
49:'The title explicitly concerns training data-preprocessing bottlenecks, a plausible input-pipeline profiling example; distributed optimization is outside this bounded tile.',
51:'The title explicitly teaches transfer learning with PyTorch, matching task-specific pretrained-weight fine-tuning; retain the custom-task training workflow.',
52:'The title isolates script setup or the Python __main__ entry point, matching conversion to an executable training script; recorded ML inputs require later confirmation.',
53:'The project title explicitly includes DVC, a plausible frozen dataset/version reference example; require a short versioning cut, not the entire deep-learning project.',
55:'The MLflow instructional course may show reproducible run inputs and rerunning experiments; a self-contained reproduction demonstration is required.',
56:'The MLflow instructional course may contain a registry/version example; tracked-run linkage is not confirmed by the title alone.',
57:'The MLflow/deployment-pipeline title may show packaging a fitted model and dependencies; fitted preprocessing must remain attached to the artifact.',
58:'The model-selection lesson may distinguish final test evaluation from validation choices; require a frozen-choice comparison and do not teach test-set tuning.',
59:'The title explicitly teaches SageMaker/XGBoost training on a managed platform, matching a bounded custom training job without AutoML or new infrastructure ownership.',
60:'The Pydantic request/response validation title directly supports prediction schema checks; restrict to a supplied prediction contract rather than general API design.',
61:'The ML deployment/API title may show calling a loaded custom model for predictions; require fitted-preprocessing reuse and avoid broad API/platform construction.',
64:'The technical Terraform/ML-lifecycle title may show parameterized deployment from an artifact reference; exclude new cloud provisioning and retain existing-runtime configuration only.',
65:'The ML deployment tutorial may show a deployed prediction verification; smoke/contract checks are not yet guaranteed by metadata.',
66:'The FastAPI authentication/authorization title may show enforcement on an existing prediction route; do not expand into designing a new identity system.',
67:'The Prometheus monitoring title may explain observable service signals; require availability/error/latency instrumentation rather than new monitoring-platform provisioning.',
68:'The short K6 performance/load-test title may show endpoint throughput and latency testing; retain measurement and reject unbounded stress testing.',
73:'The Great Expectations data-quality title may show concrete validation checks used as gates; downstream blocking behavior requires transcript verification.',
74:'The FastAPI pytest/fixtures title may show deterministic request/response tests; restrict to inference behavior and avoid general API curriculum.',
75:'The MLflow instructional course may show validation-to-release controls; a fail-closed model acceptance gate must be confirmed, not assumed.',
76:'The SageMaker pipeline title may show stage outputs and dependent inputs, matching artifact dependencies rather than new orchestration architecture.',
77:'The MLflow lifecycle course may show registry-version promotion controls; require accountable approval and preserve quality gates.',
79:'The MLflow lifecycle course may show dataset/run/model records, a plausible lineage audit example; all links require transcript confirmation.',
80:'The monitoring/Evidently title may show input and prediction distribution reports; do not interpret distribution change as proven quality degradation.',
81:'The performance-monitoring technical title may distinguish drift from measured quality change; all three terms need explicit confirmation.',
82:'The monitoring/Evidently title may show data-drift checks; require a declared reference distribution and do not trigger automatic promotion.',
83:'The performance-monitoring technical title may explain quality measurement when outcomes become observable; verify delayed-label cohort alignment.',
86:'The retraining tutorial directly addresses incremental/continuous approaches, a plausible trigger-policy comparison; require authorized retraining rather than automatic release.'}
DRIFT={0:[10,11,16],1:[2,3,35],2:[3,47,48],3:[35,37],4:[5,7,53],5:[49,53],6:[7,8,12],7:[8,73],8:[12,15],9:[27,28],10:[11,16],11:[16,25,32],12:[13,15,16],13:[15,16],14:[15,17],15:[23,57,61],16:[17,25,32],17:[23,25],18:[66],19:[24,25],20:[24,58,75],21:[23,24,32],22:[37,39,51],23:[24,25,32],24:[25,58],25:[32,58],26:[27,28],27:[28,33],28:[33,89],29:[32,55,56],30:[35,38,55],31:[32,44],32:[58,89],33:[34,79],34:[51,58],35:[36,38,46],36:[37,41,47],37:[38,39,40],38:[39,40,41],39:[40,41],40:[41,44],41:[42,43,44],42:[43,44,61],43:[51,57,61],44:[45,58],45:[49,51],46:[47,48,50],47:[48,49,50],48:[49,50],49:[50,59],50:[59],51:[52,59,61],52:[53,54,55],53:[55,79],54:[55,57],55:[56,57],56:[57,72,77],57:[60,61,64],58:[59,75],59:[64,76],60:[61,63,66],61:[63,68,71],62:[69,76],63:[65,67],64:[65,71],65:[68,72],66:[67,84],67:[68,84],68:[69,70,71],69:[70,71],70:[71,91],71:[72,93],72:[77,90],73:[74,75,76],74:[75,76],75:[77,89],76:[77,78,79],77:[78,89],78:[79,88],79:[80,83],80:[81,82,86],81:[82,83,86],82:[83,86,87],83:[84,85,86],84:[85,90],85:[86,87,90],86:[87,88,89],87:[88,89],88:[89,90],89:[90],90:[91,94],91:[92,93],92:[93,94],93:[94],94:[]}
concepts=e['concepts'];ids={x['toc_sequence_position']:x['concept_id'] for x in concepts};levels={p['path_id']:p['learner_scope'] for p in e['paths']}
searches=[];provenance={};audit=[]
for c in concepts:
 n=c['toc_sequence_position'];key=(c['concept_id'],c['path_id']);ge=gby[key]
 if ge['video_need']['level'] not in ['HIGH','MEDIUM']:continue
 assert key in rby and key in bby
 candidates=[];seen=set()
 def add(v,via,verdict,reason,source):
  if v['video_id'] in seen:return
  seen.add(v['video_id'])
  candidates.append({k:v[k] for k in ['video_id','title','channel_id','channel_name','duration_seconds']} | {'youtube_url':'https://www.youtube.com/watch?v='+v['video_id'],'found_via':via,'filter_verdict':verdict,'reason':reason})
  provenance[(c['concept_id'],v['video_id'])]=source
 for idx in m.plans[n]:
  v=m.vs[idx]
  verdict='kept';reason=CAT_REASON[n]
  if n==9:verdict='rejected';reason='The title concerns societal ML bias/fairness, not a bounded sampling/selection-bias lesson.'
  add(v,'allowlist_catalogue',verdict,reason,('catalogue',idx))
 used_open=str(n) in first
 if used_open:
  assert initial_counts[n]<2, 'Fallback cost gate violated'
  for round_,j,verdict,reason in sel.OPEN[n]:
   rows=(first if round_=='f' else second)[str(n)]
   assert 0<=j<len(rows),(n,round_,j)
   v=rows[j]
   # id copied from the source result's URL, never constructed from memory.
   assert '?v='+v['video_id'] in v['result_url']
   add(v,'open_search','kept' if verdict=='k' else 'rejected',reason,(round_,n,j))
 if n==30:
  for j in [2,3]:
   v=second['130'][j]
   add(v,'open_search','kept','The title explicitly explains random_state and reproducible ML code, matching supported sklearn estimator/split random controls; do not imply universal determinism or skip the paired-seed comparison.',('s',130,j))
 # Adjacent slice and mitigation concepts share a concrete fairness evaluation candidate.
 if n==27:
  v=first['28'][1]
  add(v,'open_search','kept','The Fairlearn title explicitly tests models for fairness; seek group-separated metrics for slice evaluation, not mitigation or model retraining.',('f',28,1))
 assert len(candidates)<=5 and sum(x['filter_verdict']=='kept' for x in candidates)<=5,(n,len(candidates))
 blocked=[ids[j] for j in DRIFT[n] if ids[j] in c['blocked_knowledge_ids']][:3]
 searches.append({'concept_id':c['concept_id'],'path_id':c['path_id'],'search_brief':{'concept_name':c['concept_name'],'learner_level':levels[c['path_id']],'required_fact_ids':[x['id'] for x in bby[key]['evidence']['required_facts']],'preferred_visual_modes':ge['video_need']['preferred_visual_modes'],'blocked_concepts_to_avoid':blocked},'search_route':'allowlist_then_open_search' if used_open else 'allowlist_only','candidates':candidates})
 audit.append({'concept_id':c['concept_id'],'tile_id':c['toc_location']['tile_id'],'initial_catalogue_count':initial_counts[n],'kept':sum(x['filter_verdict']=='kept' for x in candidates),'rejected':sum(x['filter_verdict']=='rejected' for x in candidates),'open_search_performed':used_open})
inputs=[B/'glossary_pass_a.json',B/'registry_lookup.json',B/'extracted_concepts.json',B/'coverage_briefs.json',CORE/'video_bank/channel_allowlist.json']+sorted((CORE/'video_bank/channel_catalogs').glob('*.json'))
# Raw web responses/results are candidate provenance, not upstream stage artifacts.
parents={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs}
now=datetime.datetime.now(datetime.timezone.utc)
meta={'artifact_type':'video_candidates','artifact_version':'1.0.0','schema_version':'1.0.0','batch_id':g['batch_id'],'run_id':g['batch_id']+'.06_video_candidates.all.'+now.strftime('%Y%m%dT%H%M%SZ'),'prompt_version':'06_video_candidates@v1','model':'none','generated_at':now.isoformat(),'source_snapshot_id':g['metadata']['source_snapshot_id'],'parent_artifact_hashes':parents}
artifact={'metadata':meta,'batch_id':g['batch_id'],'searches':searches}
out=B/'video_candidates.part.all.json';out.write_text(json.dumps(artifact,indent=2,ensure_ascii=False)+'\n')
# Own mistakes checklist: exhaustive mechanical tests before evaluation.
expected={k for k,v in gby.items() if v['video_need']['level'] in ['HIGH','MEDIUM']}
assert {(r['concept_id'],r['path_id']) for r in searches}==expected
assert len(searches)==len(expected)
for row in searches:
 key=(row['concept_id'],row['path_id']);c=next(x for x in concepts if (x['concept_id'],x['path_id'])==key)
 sb=row['search_brief']
 assert sb['concept_name']==c['concept_name'] and sb['learner_level']==levels[key[1]]
 assert sb['required_fact_ids']==[x['id'] for x in bby[key]['evidence']['required_facts']]
 assert sb['preferred_visual_modes']==gby[key]['video_need']['preferred_visual_modes']
 assert set(sb['blocked_concepts_to_avoid'])<=set(c['blocked_knowledge_ids']) and len(sb['blocked_concepts_to_avoid'])<=3
 assert len(row['candidates'])==len({v['video_id'] for v in row['candidates']})
 for v in row['candidates']:
  assert re.fullmatch('[A-Za-z0-9_-]{11}',v['video_id'])
  assert v['youtube_url']=='https://www.youtube.com/watch?v='+v['video_id']
  source=provenance[(row['concept_id'],v['video_id'])]
  original=m.vs[source[1]] if source[0]=='catalogue' else (first if source[0]=='f' else second)[str(source[1])][source[2]]
  for field in ['video_id','title','channel_id','channel_name','duration_seconds']:assert v[field]==original[field],field
  assert v['duration_seconds']>0 and v['reason'].strip()
  if v['found_via']=='open_search':assert row['search_route']=='allowlist_then_open_search'
assert all(hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()==h for p,h in parents.items())
counts=collections.Counter(v['filter_verdict'] for r in searches for v in r['candidates'])
report={'artifact':str(out),'search_rows':len(searches),'candidate_rows':sum(len(r['candidates']) for r in searches),'verdict_counts':dict(counts),'route_counts':dict(collections.Counter(r['search_route'] for r in searches)),'catalogues_searched':len(list((CORE/'video_bank/channel_catalogs').glob('*.json'))),'reusable_segments':0,'self_check':'PASS','checks':['HIGH/MEDIUM exhaustive coverage, LOW/NONE exclusion','fact ids, exact learner scope, concept names and visual modes','blocked ids are real blocked ids, at most three','every candidate URL computed from a source-grounded real id','catalogue titles/channels/durations byte-matched; open results byte-matched','unique candidate ids, positive integer durations, five-candidate ceiling','fallback only when initial catalogue review yielded fewer than two plausible candidates','explicit reason for every kept and rejected row','no transcript/visual-quality or fact-coverage assertions at cheap filter stage','all parent SHA256 values recomputed'],'uncertainties':['Metadata-only discovery cannot confirm fact coverage, visual mode, captions or exact scope; later transcript/segment gates must verify these.','Some fallback searches yielded broader or partial-support candidates, especially acceptance policy, supplied foundation-model output evaluation, recovery and incident runbooks.','Catalogue review found extra title matches while inspecting fallback results for distribution/drift monitoring; routes retain that open search was actually used.'],'tile_audit':audit}
(B/'video_candidates_self_check.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='tile_audit'},indent=2))
