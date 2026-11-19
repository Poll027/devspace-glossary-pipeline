import json, pathlib, hashlib, datetime, re, collections
p=pathlib.Path('batches/glossary_batch_learn_python'); batch=p.name
cs=json.loads((p/'extracted_concepts.json').read_text())['concepts']; ls={(x['concept_id'],x['path_id']):x for x in json.loads((p/'registry_lookup.json').read_text())['lookups']}; reg={x['concept_id']:x for x in json.loads((p/'concept_evidence_registry_snapshot.json').read_text())['entries']}
data={}; key=None
for line in (p/'working/coverage_facts.txt').read_text().splitlines():
 if line.startswith('['):key='python.'+line[1:-1];assert key not in data;data[key]=[]
 elif line.strip():
  ref,statement=line.split(' >> ',1);data[key].append({'id':'f'+str(len(data[key])+1),'statement':statement,'source_refs':ref.split(' ;; ')})
briefs=[];owners={}
for c in cs:
 status=ls[(c['concept_id'],c['path_id'])]['canonical_status']
 if status=='reuse_registry':
  e=reg[c['concept_id']];e=e.get('evidence',e)
 elif status=='shared_in_batch':e=owners[c['concept_id']]
 else:
  e={'concept_id':c['concept_id'],'required_facts':data[c['concept_id']],'optional_enrichment':[],'misconceptions':[],'created_in_batch_id':batch,'used_by_path_ids':sorted({x['path_id'] for x in cs if x['concept_id']==c['concept_id']})}
  owners[c['concept_id']]=e
 briefs.append({'concept_id':c['concept_id'],'path_id':c['path_id'],'learning_objective':c['primary_objective'],'canonical_status':status,'evidence':e})
inputs=['extracted_concepts.json','registry_lookup.json','concept_evidence_registry_snapshot.json','source_pack_manifest.json']
pack=json.loads((p/'source_pack_manifest.json').read_text())['packs'];paths={n:p/n for n in inputs};paths.update({x['file']:pathlib.Path(x['file']) for x in pack})
out={'metadata':{'artifact_type':'coverage_briefs','artifact_version':'1.0.0','schema_version':'1.0.0','batch_id':batch,'run_id':batch,'prompt_version':'03_coverage_brief@v1','model':'none','generated_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_snapshot_id':batch,'parent_artifact_hashes':{n:hashlib.sha256(f.read_bytes()).hexdigest() for n,f in paths.items()}},'batch_id':batch,'briefs':briefs}
(p/'coverage_briefs.part.all.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
assert len(briefs)==len(cs)==len({(b['concept_id'],b['path_id']) for b in briefs})
assert set(data)=={c['concept_id'] for c in cs if ls[(c['concept_id'],c['path_id'])]['canonical_status']=='new'}
print('Rows',len(briefs),'status',collections.Counter(b['canonical_status'] for b in briefs),'facts',sum(len(b['evidence']['required_facts']) for b in briefs))
sourceids={s['source_id'] for x in pack for s in json.loads(pathlib.Path(x['file']).read_text())['sources']}
missing=[]
for b in briefs:
 if b['canonical_status']=='reuse_registry':
  assert b['evidence']==reg[b['concept_id']].get('evidence',reg[b['concept_id']]);continue
 assert len({f['statement'] for f in b['evidence']['required_facts']})==len(b['evidence']['required_facts'])
 for f in b['evidence']['required_facts']:
  for ref in f['source_refs']:
   sid,loc=ref.split('#',1);assert sid in sourceids
   if sid.startswith('python_') and sid!='python_packaging_user_guide':
    cat={'python_tutorial':'tutorial','python_stdlib_reference':'library','python_language_reference':'reference'}[sid];page,section=loc.split('.html#');file=cat+'_'+page
   elif sid=='think_python':page,section=loc.split('.html#');file='think_'+page
   elif sid=='pep8_style_guide' and 'linked PEP 257' in loc:section='multi-line-docstrings';file='pep257'
   else:section=loc;file={'pep8_style_guide':'pep8','python_packaging_user_guide':'packaging'}[sid]
   path=p/'working/coverage_sources'/f'{file}.txt'
   if not path.exists() or 'SECTION '+section+'\n' not in path.read_text():missing.append((b['concept_id'],ref,file))
print('MISSING LOCATORS',missing)
