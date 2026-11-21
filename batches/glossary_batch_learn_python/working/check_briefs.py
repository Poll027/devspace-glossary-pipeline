import json,re,hashlib
from pathlib import Path
from html import unescape
B=Path('batches/glossary_batch_learn_python'); a=json.loads((B/'coverage_briefs.part.all.json').read_text());c=json.loads((B/'extracted_concepts.json').read_text())['concepts'];l=json.loads((B/'registry_lookup.json').read_text())['lookups'];packs=json.loads((B/'source_pack_manifest.json').read_text())['packs']; ids={s['source_id'] for p in packs for s in json.loads(Path(p['file']).read_text())['sources']}
assert len(a['briefs'])==len(c)
assert {(b['concept_id'],b['path_id']) for b in a['briefs']}=={(b['concept_id'],b['path_id']) for b in c}
assert len({(b['concept_id'],b['path_id']) for b in a['briefs']})==len(c)
lookup={(b['concept_id'],b['path_id']):b for b in l}
for b in a['briefs']:
 assert b['canonical_status']==lookup[(b['concept_id'],b['path_id'])]['canonical_status']
 assert b['evidence']['concept_id']==b['concept_id']
 fs=b['evidence']['required_facts'];assert len({f['statement'] for f in fs})==len(fs)
 assert [f['id'] for f in fs]==[f'f{i+1}' for i in range(len(fs))]
for n,h in a['metadata']['parent_artifact_hashes'].items():
 p=Path(n) if '/' in n else B/n;assert hashlib.sha256(p.read_bytes()).hexdigest()==h
seen=set();missing=[];out=[]
for b in a['briefs']:
 for f in b['evidence']['required_facts']:
  for ref in f['source_refs']:
   sid,loc=ref.split('#',1);assert sid in ids
   if sid=='pep8_style_guide':
    if loc.startswith('https://peps.python.org/pep-0257/'):name='pep257';anchor=loc.rsplit('#',1)[1]
    else:name='pep8';anchor=loc
   elif sid=='python_packaging_user_guide':name='packaging';anchor=loc
   else:
    page,_,anchor=loc.partition('#');name=({'python_tutorial':'tutorial','python_stdlib_reference':'library','python_language_reference':'reference','think_python':'think'}[sid])+'_'+page.removesuffix('.html')
   text=(B/'working/sources'/f'{name}.html').read_text()
   m=re.search(r'<[^>]+id="'+re.escape(anchor)+'"[^>]*>',text) if anchor else None
   if anchor and not m:missing.append((b['concept_id'],f['id'],ref))
   if ref not in seen:
    seen.add(ref);start=m.start() if m else text.find('<main');end=text.find('<section ',m.end()) if m else start+5000
    if end<0:end=start+6000
    t=unescape(re.sub('<[^>]+>',' ',text[start:end]));t=re.sub(r'\s+',' ',t)
    out.append(ref+'\n'+t[:5000]+'\n')
(B/'working/cited_sections.txt').write_text('\n'.join(out))
print('Rows and statuses and hashes match; source ids valid; duplicate statements and ids absent')
print('Missing anchors:',missing)
print('Unique source sections:',len(seen))
for i,b in enumerate(a['briefs']):
 if i>45:break
 text=' '.join(f['statement'] for f in b['evidence']['required_facts'])
 suspects=[]
 terms={'comprehensions':'comprehension','variable_scope':'local','error_handling':'except','truth_value_testing':'truthy','none_and_identity':'is None','aliasing_mutability_and_copying':'shallow copy','lambda_expressions':'lambda','sorting_with_key_functions':'sorted','generator_functions':'yield','iterables_and_iterators':'iterator','classes_and_instances':'instance','file_modes':'exclusive','enumerate_iteration':'enumerate','zip_iteration':'zip','finally_cleanup':'finally','docstrings':'docstring','logging':'logging','math_utilities':'math.sqrt'}
 for suffix,term in terms.items():
  if 'python.'+suffix in c[i]['blocked_knowledge_ids'] and re.search(r'\b'+re.escape(term)+r'\b',text):suspects.append(term)
 if suspects:print('Boundary review',i,b['concept_id'],suspects)
placeholder=[v['concept_id'] for v in c if re.search(r'Understand and use .*small analysis task|Given a simple example, correctly identify or apply',v['primary_objective']+' '+v['assessment_target'])]
print('Placeholder objectives:',placeholder)
