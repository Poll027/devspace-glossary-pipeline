import json,hashlib,datetime,re,sys
from pathlib import Path
root=Path('batches/glossary_batch_aws_devops_engineer')
sys.path.insert(0,str(root/'working'))
from brief_data import DATA
import brief_data_more,brief_fixes
from brief_final_fixes import EXTRA_REFS,MISCONCEPTIONS
cs=json.loads((root/'extracted_concepts.json').read_text())
lookup=json.loads((root/'registry_lookup.json').read_text())
snapshot=json.loads((root/'concept_evidence_registry_snapshot.json').read_text())
manifest=json.loads((root/'source_pack_manifest.json').read_text())
pack_path=Path('00_GLOSSARY_PIPELINE_CORE/source_packs/aws_devops_engineer.source_pack.json')
pack=json.loads(pack_path.read_text())
statuses={x['concept_id']:x for x in lookup['lookups']}
assert set(DATA)==set(range(len(cs['concepts'])))
assert all(x['canonical_status']=='new' for x in lookup['lookups']), 'A reuse/shared record needs evidence copying, not generation'
parents={str(root/n):hashlib.sha256((root/n).read_bytes()).hexdigest() for n in ['extracted_concepts.json','registry_lookup.json','source_pack_manifest.json','concept_evidence_registry_snapshot.json']}
parents[str(pack_path)]=hashlib.sha256(pack_path.read_bytes()).hexdigest()
md=cs['metadata'].copy();md.update(artifact_type='coverage_briefs',artifact_version='1.0.0',schema_version='1.0.0',batch_id='glossary_batch_aws_devops_engineer',prompt_version='03_coverage_brief@v1',model='none',generated_at=datetime.datetime.now(datetime.timezone.utc).isoformat().replace('+00:00','Z'),parent_artifact_hashes=parents)
briefs=[]; placeholders=[]
for i,c in enumerate(cs['concepts']):
 objective=re.split(r' Direct native| Cross-path| Semantic assumption:',c['primary_objective'])[0].strip()
 if any(t in objective for t in ['Understand and use','Given a simple example']):placeholders.append(c['concept_id'])
 facts=[];optional=[]
 for j,(f,r) in enumerate(DATA[i]):
  refs=list(dict.fromkeys([r]+EXTRA_REFS.get((i,j),[])))
  entry={'id':f'f{j+1}','statement':f,'source_refs':refs}
  if i==28 and j==3:optional.append(entry)
  else:facts.append(entry)
 evidence={'concept_id':c['concept_id'],'required_facts':facts,'optional_enrichment':optional,'misconceptions':[{'id':f'm{j+1}','statement':f,'source_refs':[r]} for j,(f,r) in enumerate(MISCONCEPTIONS.get(i,[]))],'created_in_batch_id':md['batch_id'],'used_by_path_ids':[c['path_id']]}
 briefs.append({'concept_id':c['concept_id'],'path_id':c['path_id'],'learning_objective':objective,'canonical_status':statuses[c['concept_id']]['canonical_status'],'evidence':evidence})
artifact={'metadata':md,'batch_id':md['batch_id'],'briefs':briefs}
(root/'coverage_briefs.part.all.json').write_text(json.dumps(artifact,indent=2,ensure_ascii=False)+'\n')
# Deterministic mistakes checklist and input/output cross references.
assert len(briefs)==len(cs['concepts'])
assert len(set((b['concept_id'],b['path_id']) for b in briefs))==len(briefs)
source_ids={s['source_id'] for s in pack['sources']}
for c,b in zip(cs['concepts'],briefs):
 assert c['concept_id']==b['concept_id']==b['evidence']['concept_id']
 assert c['path_id']==b['path_id']
 ev=b['evidence'];allfacts=ev['required_facts']+ev['optional_enrichment']
 assert len({f['id'] for f in allfacts})==len(allfacts)
 assert len({f['statement'] for f in allfacts})==len(allfacts)
 for f in allfacts+ev['misconceptions']:
  for ref in f['source_refs']:
   sid,loc=ref.split('#',1);assert sid in source_ids and loc,ref
 assert ev['used_by_path_ids']==[c['path_id']]
 for term in ['AWS DevOps Engineer career','glossary_batch_','this path','later in the path']:
  assert term not in json.dumps(allfacts)
counts={'briefs':len(briefs),'required_facts':sum(len(b['evidence']['required_facts']) for b in briefs),'optional_enrichment':sum(len(b['evidence']['optional_enrichment']) for b in briefs),'misconceptions':sum(len(b['evidence']['misconceptions']) for b in briefs)}
report={'counts':counts,'placeholder_objective_ids':placeholders,'mechanical_checks':'passed','manual_checklist':['all assessment/practice verbs checked for an actionable form','blocked concept names and inline vocabulary reviewed by tile; no later implementation required for supplied scaffolding','each named assessment variant covered; impactful defaults and exceptions retained','all required facts have valid source-pack ids and section/page locators','no source examples copied from memory or fabricated concrete AWS identifiers','no career/path context inside evidence','required facts distinct; optional security-group exception separated','security, state, approval, rollback and recovery source sections sampled in additional high-stakes review'], 'scaffolding_note':'Supplied wrapper key names and procedures are grounded in the extracted exercise objectives; official Python/operations sources ground the configuration mechanism and validation principles, not an independently published wrapper implementation.'}
(root/'working/coverage_self_check.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
