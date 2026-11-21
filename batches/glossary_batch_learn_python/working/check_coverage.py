import json,re,hashlib
from pathlib import Path
P=Path('batches/glossary_batch_learn_python');C=P/'working/coverage_sources'
o=json.loads((P/'coverage_briefs.part.all.json').read_text());e=json.loads((P/'extracted_concepts.json').read_text());l=json.loads((P/'registry_lookup.json').read_text());reg={x['concept_id']:x for x in json.loads((P/'concept_evidence_registry_snapshot.json').read_text())['entries']}
assert len(o['briefs'])==len(e['concepts']);assert {(b['concept_id'],b['path_id']) for b in o['briefs']}=={(b['concept_id'],b['path_id']) for b in e['concepts']}
look={(x['concept_id'],x['path_id']):x for x in l['lookups']};sources={s['source_id'] for s in json.loads(Path('00_GLOSSARY_PIPELINE_CORE/source_packs/learn_python.source_pack.json').read_text())['sources']}
missing=[];review=[]
for b,c in zip(o['briefs'],e['concepts']):
 assert b['canonical_status']==look[(b['concept_id'],b['path_id'])]['canonical_status']
 if b['canonical_status']=='reuse_registry':assert b['evidence']==reg[b['concept_id']].get('evidence',reg[b['concept_id']]);continue
 assert [f['id'] for f in b['evidence']['required_facts']]==[f'f{i+1}' for i in range(len(b['evidence']['required_facts']))]
 review.append('\nCONCEPT '+b['concept_id']+'\nASSESS '+c['assessment_target']+'\nPRACTICE '+c['practice_objective']+'\nBLOCKED '+', '.join(x['concept_name'] for x in e['concepts'] if x['concept_id'] in c['blocked_knowledge_ids']))
 for f in b['evidence']['required_facts']:
  review.append('\n'+f['id']+' '+f['statement'])
  for ref in f['source_refs']:
   sid,loc=ref.split('#',1);assert sid in sources
   if sid=='python_packaging_user_guide':
    if loc.startswith('discussions/'):fn='packaging_names';anchor=loc.split('#',1)[1]
    else:fn='packaging';anchor=loc
   elif sid=='pep8_style_guide':
    if 'linked PEP 257#' in loc:fn='pep257';anchor=loc.split('linked PEP 257#')[1]
    else:fn='pep8';anchor=loc
   else:
    page,anchor=loc.split('#',1)
    prefix={'python_tutorial':'tutorial_','python_stdlib_reference':'library_','python_language_reference':'reference_','think_python':'think_'}[sid]
    fn=prefix+page.removesuffix('.html')
   t=(C/(fn+'.txt')).read_text();i=t.find('\n#'+anchor+'\n')
   if i<0:missing.append((b['concept_id'],f['id'],ref))
   review.append('REF '+ref+'\n'+(t[i:i+1400] if i>=0 else 'MISSING'))
(P/'working/coverage_source_review.txt').write_text('\n'.join(review))
print('Missing locators:',missing)
print('All 116 row identities/statuses checked; registry evidence unchanged; new fact ids contiguous; source ids valid.')
for k,v in o['metadata']['parent_artifact_hashes'].items():assert hashlib.sha256((P/k if not k.startswith('00_') else Path(k)).read_bytes()).hexdigest()==v
print('Parent hashes verified.')
