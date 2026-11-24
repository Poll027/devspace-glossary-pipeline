import json
from pathlib import Path
p=Path('batches/glossary_batch_flutter_mobile_developer/coverage_briefs.part.all.json')
d=json.loads(p.read_text())
before=json.loads(p.read_text())
rows={r['concept_id']:r['evidence'] for r in d['briefs'] if r['path_id']=='flutter_mobile_developer'}
def fact(cid,fid):return next(f for f in rows[cid]['required_facts'] if f['id']==fid)
def replace(cid,fid,statement,refs):
 f=fact(cid,fid);f['statement']=statement;f['source_refs']=refs
replace('flutter.layout_constraints','f4',
 'Bound a child with `ConstrainedBox(constraints: const BoxConstraints(minWidth: 70, minHeight: 70, maxWidth: 150, maxHeight: 150), child: child)`; these are additional bounds within the parent constraints, not replacements for them: with a parent permitting that range an oversized child is limited to 150, but tight parent constraints can force a size outside the requested range.',
 ['flutter_docs#ui/layout/constraints:Example-9','flutter_docs#ui/layout/constraints:Example-11'])
rows['flutter.provider_scope']['required_facts'].append({
 'id':'f5','statement':'Expose the supplied existing model with `Provider<Model>.value(value: suppliedModel, child: consumerSubtree)`, where Model is its type and consumerSubtree contains the intended consumers.',
 'source_refs':['provider_docs#Exposing-a-value:Reusing-an-existing-object-instance']})
replace('dart.future_results','f4',
 'Future completion and callback execution are distinct: when `then` is registered on an already-completed Future, its callback is scheduled in a later microtask rather than called immediately, so a callback not yet having run does not mean the Future is still uncompleted.',
 ['dart_language#api.dart.dev/dart-async/Future/then.html'])
fact('flutter.request_state_model','f3')['source_refs']=['dart_language#api.dart.dev/dart-core/Iterable/isEmpty.html']
rows['dart.interfaces']['required_facts'].append({
 'id':'f5','statement':'Declare `class Subclass extends Superclass` to inherit the superclass implementation; subclasses can override instance methods, getters, and setters, marking intentional overrides with `@override`, and an overriding method must accept the same number of positional parameters, use the same or broader parameter types and the same or narrower return type, and match whether the method is generic.',
 'source_refs':['dart_language#extend','dart_language#extend:Overriding-members']})
replace('flutter.local_database_schema','f2',
 "Open the supplied database with `await openDatabase(path, version: 1, onCreate: (db, version) async { await db.execute('CREATE TABLE tableName (id INTEGER PRIMARY KEY, fieldName TEXT)'); })`: path identifies the database file, 1 is the initial schema version, and onCreate is the creation callback that creates its tables; substitute the supplied schema's table names, column names, and column types.",
 ['sqflite_docs#Open-read-write-close'])
for cid,fid in [('flutter.list_item_keys','f3'),('dart.exceptions','f5')]:
 f=fact(cid,fid);rows[cid]['required_facts'].remove(f);rows[cid]['optional_enrichment'].append(f)
for fid in ['f2','f3','f4']:
 fact('flutter.flutterfire_initialization',fid)['source_refs']=['firebase_flutter#Step-3-Initialize-Firebase-in-your-app']
allowed=set(rows)&{'flutter.layout_constraints','flutter.provider_scope','dart.future_results','flutter.request_state_model','dart.interfaces','flutter.local_database_schema','flutter.list_item_keys','dart.exceptions','flutter.flutterfire_initialization'}
changed=[]
for old,new in zip(before['briefs'],d['briefs']):
 if old!=new:
  assert new['concept_id'] in allowed
  assert {k:v for k,v in old.items() if k!='evidence'}=={k:v for k,v in new.items() if k!='evidence'}
  changed.append(new['concept_id'])
p.write_text(json.dumps(d,indent=2)+'\n')
print('changed',changed)
print('briefs',len(d['briefs']),'required facts',sum(len(r['evidence']['required_facts']) for r in d['briefs']),'optional facts',sum(len(r['evidence']['optional_enrichment']) for r in d['briefs']))
