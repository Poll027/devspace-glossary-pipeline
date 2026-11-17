import json,hashlib,re
from pathlib import Path
from datetime import datetime,timezone
P=Path('batches/glossary_batch_machine_learning_engineer')
a=json.loads((P/'coverage_briefs.part.all.json').read_text())
c=json.loads((P/'extracted_concepts.json').read_text())['concepts']
l=json.loads((P/'registry_lookup.json').read_text())['lookups']
packs=json.loads((P/'source_pack_manifest.json').read_text())['packs']
sources={s['source_id'] for p in packs for s in json.loads(Path(p['file']).read_text())['sources']}
assert a['batch_id']==P.name
assert len(a['briefs'])==len(c)==95
keys=lambda rows:{(x['concept_id'],x['path_id']) for x in rows}
assert keys(a['briefs'])==keys(c)==keys(l)
assert len(keys(a['briefs']))==95
look={(x['concept_id'],x['path_id']):x for x in l}
for b in a['briefs']:
 assert b['canonical_status']==look[(b['concept_id'],b['path_id'])]['canonical_status']=='new'
 e=b['evidence'];assert e['concept_id']==b['concept_id']
 assert e['created_in_batch_id']==P.name and e['used_by_path_ids']==[b['path_id']]
 assert len(e['required_facts'])>0
 assert e['optional_enrichment']==e['misconceptions']==[]
 assert [f['id'] for f in e['required_facts']]==[f'f{i+1}' for i in range(len(e['required_facts']))]
 assert len({f['statement'] for f in e['required_facts']})==len(e['required_facts'])
 for f in e['required_facts']:
  assert f['source_refs'] and all(r.split('#',1)[0] in sources and '#' in r for r in f['source_refs'])
  assert not re.search(r'\b(TODO|TBD|placeholder|machine_learning_engineer|Devspace)\b',f['statement'],re.I)
  assert not re.search(r'https?://',f['statement']) # Real URLs belong in locators, not invented examples.
 for field in ['learning_objective']:
  assert b[field].strip()
m=a['metadata'];assert m['batch_id']==P.name and m['model']=='none' and m['prompt_version']=='03_coverage_brief@v1'
inputs=[P/x for x in ['extracted_concepts.json','registry_lookup.json','concept_evidence_registry_snapshot.json','source_pack_manifest.json']]+[Path(p['file']) for p in packs]
assert m['parent_artifact_hashes']=={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs}
assert datetime.fromisoformat(m['generated_at'].replace('Z','+00:00')).utcoffset().total_seconds()==0
report={'checked_at':datetime.now(timezone.utc).isoformat(),'status':'PASS','briefs':len(a['briefs']),'required_facts':sum(len(b['evidence']['required_facts']) for b in a['briefs']),'automated_checks':['whole-batch keyed coverage','canonical status','evidence ownership','sequential scoped fact IDs','within-concept duplicate facts','nonempty specific source references with registered source IDs','placeholder/path-brand exclusion','metadata and input SHA-256 identities','UTC timestamp'],'manual_mistakes_checklist':['Reviewed all 95 full practice objectives and assessment targets, not only the primary objective.','Corrected risk-record placement and expanded executable YAML, event/gate, runtime, file-handle, credential, probe, lifecycle and recovery boundaries.','Checked stated variants and arithmetic, including conditional probabilities, expected cost, numeric means/spreads, memory shape estimates, chain-rule/SGD references, tails, delayed-label coverage and shared-charge handling.','Kept protected-test selection and supplied identity/coordinator policy boundaries intact.','Kept coordinator implementation out of the run-admission wrapper and preserved accepted/duplicate/busy plus restart/terminal cases.','Removed unneeded cloud launch requirements from local manifest/reproduction placements and resolved replacement-readiness ordering.','Source locators use fetched real documentation; provider adapters remain conditional on the supplied platform/contracts.','Schema validation passed; no input, other stage, TOC or registry artifacts edited.']}
(P/'working/coverage_self_check.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'status':report['status'],'briefs':report['briefs'],'required_facts':report['required_facts']}))
