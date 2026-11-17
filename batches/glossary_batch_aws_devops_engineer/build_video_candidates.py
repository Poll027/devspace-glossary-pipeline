from review_catalogue_matches import *
from fetch_open_video_searches import fetch
EX=load(B/'extracted_concepts.json'); CB=load(B/'coverage_briefs.json')
G=load(B/'glossary_pass_a.json'); LOOK=load(B/'registry_lookup.json')
assert not any(x['reusable_segment_ids'] for x in LOOK['lookups']), 'Resolve reusable segments first'
choices=load(B/'catalogue_choices.json'); opchoices=load(B/'open_search_choices.json'); op=load(B/'open_search_results.json')
byid={v['video_id']:v for v in catalog}
for k,ids in choices.items():
 for vid in ids:assert vid in byid,(k,vid,'missing catalogue ID')
for k,ids in opchoices.items():
 available={v['video_id']:v for v in op[k]}
 for vid in ids:assert vid in available,(k,vid,'missing real search result')
# Taint/untaint-only instruction is obsolete for the modern replacement-control brief.
choices['111']=['7xngnjfIlK4']
choices['78']=[];opchoices['78']=['yYKJNCTqswE']
# Add a fallback search for replacement controls after dropping the obsolete candidate.
if '111' not in op:
 q='Terraform lifecycle prevent_destroy create_before_destroy replace tutorial'
 (B/'open_search_queries.json').write_text(json.dumps(dict(load(B/'open_search_queries.json'),**{'111':q}),indent=2))
 _,op['111']=fetch(('111',q))
 (B/'open_search_results.json').write_text(json.dumps(op,indent=2))
 print('REPLACEMENT RESULTS')
 for v in op['111'][:10]:print(v['video_id'],v['channel_name'],v['duration_seconds'],v['title'])
 raise SystemExit('Select replacement results then rerun')
ex={(c['concept_id'],c['path_id']):c for c in EX['concepts']}
cb={(c['concept_id'],c['path_id']):c for c in CB['briefs']}
paths={p['path_id']:p for p in EX['paths']}
drift_risks=load(B/'video_drift_risks.json')
index_by_concept={e['concept_id']:str(i) for i,e in enumerate(G['entries'])}
stop=set('aws aws_devops devops a an the for and with using supplied approved established bounded configure execute operate run perform apply define verify from in to of after as by at on resource workload service operational control controls'.split())
def tokens(cid):return set(re.findall(r'[a-z0-9]+',cid.lower()))-stop
def blocked_for(c):
 own=tokens(c['concept_id']); own.update(tokens(c['concept_name']))
 related=[]
 for cid in c['blocked_knowledge_ids']:
  shared=own&tokens(cid)
  score=sum(3 if x in {'iam','ec2','ecs','eks','terraform','cloudformation','cloudwatch','s3','recovery','pipeline','event','alarm','state','artifact','credentials','credential','incident','storage','security','cost','logs'} else 1 for x in shared)
  if score>=2:related.append((score,cid))
 explicit=[G['entries'][i]['concept_id'] for i in drift_risks.get(index_by_concept[c['concept_id']],[])]
 prioritized=[cid for cid in explicit if cid in c['blocked_knowledge_ids']]+[cid for _,cid in sorted(related,key=lambda x:-x[0])]
 return list(dict.fromkeys(prioritized))[:3]
# Metadata-only plausibility: these notes state intended support, not verified coverage.
support={
 '0':'Inspect explicit CLI configuration/profile selection; require the clip to distinguish identity from Region.',
 '1':'Illustrate VPC/subnet boundaries and nonoverlapping address allocation; retain only AWS-specific parts after external CIDR preparation.',
 '3':'Illustrate subnet route-table paths to internet gateways/NAT, avoiding later endpoint and security-group detail.',
 '8':'Inspect policy statements and a requested action/resource, not user creation as the lesson.',
 '9':'Inspect workflow triggers, jobs and runner execution; isolate this from application test or container authoring.',
 '11':'Inspect event patterns and rule matching, avoiding timer-only scheduler explanations.',
 '12':'Show instance state transitions and operating actions on a supplied instance.',
 '13':'Show bucket/object operations, not application development or Object Lambda.',
 '14':'Inspect metrics, namespaces and dimensions; avoid dashboard construction.',
 '15':'Check account identity and AWS configuration before an automation mutation; generic Boto3 programming is out of scope.',
 '16':'Inspect a proposed stack update through a change set before execution.',
 '17':'Inspect MFA setup/enforcement; exclude unrelated identity administration.',
 '18':'Inspect trust versus permissions and the caller assuming a role.',
 '20':'Inspect recorded API events to attribute a change; do not infer identity from a resource label.',
 '21':'Inspect tags/cost allocation as spend attribution, not a workload estimate.',
 '22':'Inspect log groups/streams and centralized ingestion; require structured-field support before selecting a cut.',
 '23':'Inspect service configuration validation and reload; exclude general Linux preparation and boot-start policy.',
 '24':'Compare release traffic patterns and rollback tradeoffs; do not teach a new orchestration platform.',
 '25':'Inspect host agent configuration and collected metrics/logs.',
 '26':'Inspect alarm evaluation and missing-data states; avoid composite/anomaly-detection configuration.',
 '27':'Inspect Identity Center access and permission sets for temporary human sessions.',
 '28':'Inspect inbound/outbound group rules and permitted traffic; avoid enterprise policy automation.',
 '29':'Inspect AWS provider configuration and an EC2 resource; require provider-pinning support in the transcript.',
 '30':'Inspect bucket/resource policy versus identity permissions for a concrete request.',
 '31':'Inspect an established account-factory/onboarding flow, not design a landing-zone architecture.',
 '32':'Inspect isolated Python dependency environments; only the environment mechanics support this native AWS execution target.',
 '33':'Inspect CLI JSON/query/pagination controls; exclude DynamoDB data-model or capacity instruction.',
 '35':'Inspect supplied-cluster access and basic pod commands; exclude cluster provisioning.',
 '36':'Inspect managed database operating status/endpoints; exclude database application development.',
 '37':'Inspect object lifecycle/retention rules; version recovery still needs explicit transcript confirmation.',
 '38':'Inspect image tagging/authentication and pushing into ECR.',
 '39':'Inspect build outputs and artifact identity/versioning, not package application development.',
 '40':'Inspect standard template parameters/resources; isolate S3-compatible template mechanics from DynamoDB details.',
 '41':'Inspect secret retrieval by an authorized workload; managed rotation is blocked.',
 '43':'Inspect Config compliance findings and evidence, not governance-platform design.',
 '44':'Inspect stack drift detection and differences from template state.',
 '45':'Inspect rollback status/events and recovery from a failed stack update.',
 '46':'Inspect EC2 role/profile attachment and credential use without long-lived keys.',
 '47':'Inspect pod/workload IAM identity; avoid identity-provider installation and cluster security architecture.',
 '48':'Inspect GitHub OIDC trust and temporary AWS pipeline credentials.',
 '49':'Inspect STS AssumeRole sessions and temporary credential boundaries.',
 '50':'Inspect invocation roles and target permissions; scheduler payload mechanics alone do not cover authorization.',
 '51':'Inspect automated Config compliance evaluation; avoid multi-account governance architecture.',
 '52':'Inspect threshold notifications and email alert configuration, not a hard spending cap.',
 '53':'Inspect buildspec phases and configured build outputs for a supplied application.',
 '54':'Inspect EC2 CodeDeploy action/appspec mechanics; keep application authoring outside the cut.',
 '55':'Inspect target-tracking/group response to bounded load; exclude ECS/RDS scaling.',
 '56':'Inspect authenticated artifact repository use/access; package development is outside scope.',
 '57':'Inspect repository image lifecycle/retention; preserve traceable releases needed for rollback.',
 '58':'Inspect listener, target registration and health-check configuration; isolate these from later ECS deployment.',
 '59':'Inspect log-group retention settings, not query authoring.',
 '60':'Inspect managed backups/snapshots and restoration; do not teach database schema or capacity design.',
 '61':'Inspect log resource scope and IAM policy mechanics; general policy explanation is only partial support.',
 '62':'Inspect task definition/image configuration for ECS; desired-count operation comes later.',
 '63':'Inspect policy simulation and denied-request evidence; do not equate a simulation with live authorization.',
 '64':'Inspect plan review and apply for a supplied EC2 configuration, excluding module/state/advanced material.',
 '65':'Inspect a scoped Run Command/Systems Manager operational action.',
 '66':'Inspect configuration validation and plan controls before infrastructure changes; no pipeline-platform authoring.',
 '67':'Inspect Boto3 exceptions and error reporting; retries must be bounded, not unconditional loops.',
 '68':'Inspect cost/usage filtering to identify avoidable charges; forecasting is not the target.',
 '69':'Inspect Kubernetes Deployment state and desired replicas on supplied EKS access; exclude cluster setup.',
 '70':'Inspect compute/storage restoration context; dependency ordering must be confirmed rather than inferred from a DR title.',
 '71':'Inspect log filtering and queries that correlate a concrete symptom.',
 '72':'Inspect alarm-to-SNS notification wiring and a verified receiving owner.',
 '73':'Inspect a small Python Lambda operating action, not serverless application architecture.',
 '74':'Inspect sample GuardDuty finding details and evidence; avoid attack-chain deep dives.',
 '75':'Inspect public-access/resource-policy controls for storage access evidence.',
 '76':'Inspect S3/KMS encryption settings and evidence; avoid data-lake architecture.',
 '77':'Inspect destroy/plan review for the bounded AWS resources; do not adopt automatic teardown.',
 '78':'Inspect explicit dry-run/safe-delete behavior; do not imply a dry-run reserves capacity or proves success.',
 '79':'Inspect AWS SDK exceptions/reporting as partial support for per-target failures; the batch-success distinction must be confirmed.',
 '80':'Inspect temporary session credential use; require expiration/refresh behavior before selecting a cut.',
 '81':'Inspect task role versus execution role for ECS.',
 '82':'Inspect enabled managed-account guardrails/controls; exclude independent security architecture.',
 '83':'Inspect ConfigMap/Secret injection and workload references; exclude secret-store provisioning and advanced CSI drivers.',
 '84':'Inspect source/build/deploy action flow and artifact handoff, not CDK application authoring.',
 '85':'Inspect cross-account/Region stack deployment mechanics; exclude autonomous organization-wide administration.',
 '86':'Inspect VPC routes and security-group evidence for connectivity diagnosis; no advanced hybrid network design.',
 '87':'Inspect fleet patch execution/status through Systems Manager; avoid authoring a new fleet orchestration system.',
 '88':'Inspect Service selectors and exposure of supplied Kubernetes workloads.',
 '89':'Inspect controlled alarm triggering/testing and state/notification evidence.',
 '90':'Inspect published Lambda versions and aliases, isolating rollback from application authoring.',
 '91':'Inspect Deployment rolling updates and rollback with supplied EKS cluster access.',
 '92':'Inspect EC2 CodeDeploy blue/green traffic switching; ECS blue/green is a different target.',
 '93':'Inspect explicit AWS cleanup actions as partial support after script failure; require error/ownership guards in the cut.',
 '94':'Inspect drift/refresh-only versus configuration reconciliation for supplied EC2 infrastructure.',
 '95':'Inspect module use from a supplied EC2 configuration; exclude designing modules from scratch.',
 '96':'Inspect baseline-informed cost/EC2 optimization decisions; exclude Spot architecture and workload price estimation.',
 '97':'Inspect Security Hub findings and owner-directed notifications, not autonomous remediation.',
 '98':'Inspect event target routing to an owner or established Systems Manager action.',
 '99':'Inspect ECS service/task reconciliation; exclude load-driven desired-count changes.',
 '100':'Inspect test execution and failure blocking in a workflow; test authoring is external preparation.',
 '101':'Inspect a small Terraform/Git change workflow and reviewable configuration; no enterprise platform design.',
 '102':'Inspect compute/network resilience across zones; actual controlled-failure evidence still requires transcript verification.',
 '103':'Inspect owned-resource cleanup and retained dependencies; broad delete-all advice is unsafe for this bounded target.',
 '104':'Inspect backup/restore role and assumable permissions as credential-readiness support, not proof of a successful restore.',
 '105':'Inspect restore testing and restored-resource isolation; third-party recovery tooling is outside scope.',
 '106':'Inspect established automation/runbook steps as partial support; approval and stop boundaries need explicit transcript evidence.',
 '107':'Inspect auditable API events and caller attribution for operational response evidence.',
 '108':'Inspect CloudTrail log-file integrity validation, distinct from who can read the logs.',
 '109':'Inspect immutable retention/Object Lock settings and governance/compliance boundaries.',
 '110':'Inspect a supplied remote/backend state configuration; exclude managing an enterprise Terraform platform.',
 '111':'Inspect lifecycle/replacement controls and a reviewed plan; prefer modern -replace to deprecated taint workflows.',
 '112':'Inspect template-based restoration mechanics for a supplied environment; only isolate EC2-compatible infrastructure sections.',
 '113':'Inspect automated vulnerability scans as blocking pipeline evidence; ignore unrelated secret-scanning setup.',
 '114':'Inspect failed build/action evidence and the stage/action flow; avoid unrelated CI platforms.',
 '115':'Inspect ECS health-check/log evidence to diagnose a failure, not tracing/dashboard construction.',
 '116':'Inspect deployed-service smoke checks and release-quality gates; exclude writing a full test framework.',
 '117':'Inspect EventBridge delivery failures, retry/DLQ boundaries and failure capture.',
 '118':'Inspect ECS service deployment/update mechanics and rollback; exclude load-driven service scaling.',
 '119':'Inspect artifact identity and cross-environment delivery mechanics; require evidence of promoting the same version rather than rebuilding.',
 '120':'Inspect cost/usage after cleanup; exclude forecasts or claiming deletion immediately erases historical charges.',
 '121':'Inspect remote S3 state access isolation and IAM/security controls; exclude deprecated DynamoDB-only locking guidance.',
 '122':'Inspect modern native S3 lockfile acquisition and locking; deprecated DynamoDB-only guidance is not a match.',
 '123':'Inspect a manual pipeline approval gate before environment promotion.',
 '124':'Inspect stepwise incident runbook operation; exclude provisioning an independent incident-management platform.',
 '125':'Inspect restored compute/storage and recovery evidence; RTO/RPO measurement must be confirmed, not assumed from a DR overview.',
 '126':'Inspect evidence-based postmortem learning/actions; exclude workplace-safety investigation or opinion-only discussion.',
 '127':'Inspect DNS failover/health checks as cutover support, not application network architecture.'}
searches=[]
for ix,e in enumerate(G['entries']):
 if e['video_need']['level'] not in ['HIGH','MEDIUM']:continue
 k=str(ix);key=(e['concept_id'],e['path_id']);c=ex[key];brief=cb[key]
 candidates=[];seen=set()
 def add(v,via,verdict='kept',why=None):
  vid=v['video_id']
  if vid in seen:return
  seen.add(vid)
  reason=why or ('Title/metadata makes this a plausible '+('partial-support ' if k in {'32','50','61','70','79','93','102','104','106','119','125'} else '')+'candidate for '+c['concept_name']+'. '+support[k]+' Coverage and a self-contained visual cut are unverified until transcript/segment review.')
  candidates.append({'video_id':vid,'youtube_url':'https://www.youtube.com/watch?v='+vid,'title':v['title'],'channel_id':v['channel_id'],'channel_name':v['channel_name'],'found_via':via,'duration_seconds':v.get('duration_seconds') or 0,'filter_verdict':verdict,'reason':reason})
 for vid in choices[k]:add(byid[vid],'allowlist_catalogue')
 if k in opchoices:
  available={v['video_id']:v for v in op[k]}
  for vid in opchoices[k]:
   v=available[vid]
   raw=(B/'working/video_search'/f'{k}.html').read_text()
   assert ('/watch?v='+vid) in raw,(k,vid,'ID lacks source result URL')
   # Catalogue provenance takes precedence when a search rediscovers a bank video.
   if vid in byid:add(byid[vid],'allowlist_catalogue')
   else:add(v,'open_search')
 # Show at most two informative cheap rejections from the metadata shortlist.
 rejected=[]
 specific_rejections={'28':[('noJ7XXtcvHY','Introduces Terraform, a later blocked tool target, instead of basic security-group operating rules.')],'47':[('FdCJVvYr5BI','Specialist IRSA-evolution/any-cluster solution exceeds supplied-cluster workload identity operation.')],'58':[('esISkPlnxL0','ECS/Fargate service deployment is a later blocked workload target, not bounded ALB configuration.'),('o7s-eigrMAI','ECS/Fargate deployment context assumes later blocked task/service operations.')]}
 for vid,why in specific_rejections.get(k,[]):rejected.append((byid[vid],'allowlist_catalogue',why))
 if k=='92':
  v=next(v for v in op[k] if v['video_id']=='UtwPl6glP94')
  rejected.append((v,'open_search','Generic EC2 application deployment title does not establish the requested blue/green release and rollback mechanics.'))
 for v in sorted([v for v in catalog if re.search(patterns[k],v['title'],re.I)],key=lambda v:-score(v,patterns[k])):
  why=reject(v)
  if v['video_id'] not in seen and why:rejected.append((v,'allowlist_catalogue',why))
 if k=='111':rejected.insert(0,(byid['IdJBLpjcS4w'],'allowlist_catalogue','Obsolete replacement workflow: title teaches taint/untaint rather than current reviewed -replace/lifecycle controls.'))
 if k in op:
  for v in op[k]:
   why=reject(v)
   if v['duration_seconds']<90:why='Too brief for the requested bounded operational demonstration; short-form overview, not a usable instructional cut.'
   if k=='92' and re.search(r'\bECS\b',v['title']):why='Wrong target: ECS blue/green instead of EC2 CodeDeploy.'
   if v['video_id'] not in seen and why:rejected.append((v,'open_search',why))
 for v,via,why in rejected[:2]:add(v,via,'rejected',why)
 searches.append({'concept_id':e['concept_id'],'path_id':e['path_id'],'search_brief':{'concept_name':c['concept_name'],'learner_level':paths[e['path_id']]['learner_scope'],'required_fact_ids':[f['id'] for f in brief['evidence']['required_facts']],'preferred_visual_modes':e['video_need']['preferred_visual_modes'],'blocked_concepts_to_avoid':blocked_for(c)},'search_route':'allowlist_then_open_search' if k in opchoices else 'allowlist_only','candidates':candidates})
inputs=[B/'glossary_pass_a.json',B/'registry_lookup.json',B/'extracted_concepts.json',B/'coverage_briefs.json',ROOT/'video_bank/channel_allowlist.json',*sorted((ROOT/'video_bank/channel_catalogs').glob('*.json'))]
meta={'artifact_type':'video_candidates','artifact_version':'1.0.0','schema_version':'1.0.0','batch_id':G['batch_id'],'run_id':G['metadata']['run_id'],'prompt_version':'06_video_candidates@v1','model':'none','generated_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_snapshot_id':G['metadata']['source_snapshot_id'],'parent_artifact_hashes':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs}}
out={'metadata':meta,'batch_id':G['batch_id'],'searches':searches}
P=B/'video_candidates.part.all.json';P.write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
print('Wrote',P,'searches',len(searches),'kept',sum(v['filter_verdict']=='kept' for s in searches for v in s['candidates']),'rejected',sum(v['filter_verdict']=='rejected' for s in searches for v in s['candidates']))
