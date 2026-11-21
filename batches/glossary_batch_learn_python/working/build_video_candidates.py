import json,hashlib,datetime,pathlib,re,collections
B=pathlib.Path('batches/glossary_batch_learn_python');CORE=pathlib.Path('00_GLOSSARY_PIPELINE_CORE')
load=lambda p:json.load(open(p))
G=load(B/'glossary_pass_a.json');E=load(B/'extracted_concepts.json');F=load(B/'coverage_briefs.json');L=load(B/'registry_lookup.json')
V={x['video_id']:x for x in load(B/'working/all_catalog_metadata.json')}
S=load(B/'working/curated_selection.json');R=load(B/'working/reuse_video_ids.json');O=load(B/'working/open_search_results.json')
# Only instructional open results survive the metadata filter. Values are indices into real search results.
open_kept={
'variables_assignment':[0], 'type_conversion':[0], 'floating_point_limits':[0,2], 'indentation_and_blocks':[5,2],
'range_iteration':[7], 'statements_and_expressions':[1,7], 'interactive_execution':[9], 'unicode_and_bytes':[2,4],
'diagnostic_printing':[0,7], 'closures_and_enclosing_scope':[0], 'reading_tracebacks':[0], 'debugger_usage':[0],
'safe_mutable_defaults':[1], 'composition':[5], 'custom_exceptions':[0], 'object_introspection':[1,3],
'text_file_encodings':[2], 'binary_files':[0], 'datetime_operations':[3], 'importable_packages':[0],
'argparse_command_line':[2], 'random_vs_secrets':[2], 'unittest_test_cases':[4], 'unittest_execution_and_results':[9],
'unittest_setup_and_teardown':[9,3], 'read_generated_code':[10], 'review_generated_file_operations':[6],
'verify_generated_api_claims':[1], 'review_generated_dependencies':[0], 'accept_repair_or_reject_generated_code':[6]}
# A few genuinely tempting but unsuitable hits are retained as rejected audit rows.
reject_catalog={
'variables_assignment':('BJ-VvGyQxho','Rejected: class variables are an OOP topic blocked at this first assignment lesson.'),
'arithmetic_operators':('K47w0cpRLt4','Rejected: logical operators are a different, later operator family, not arithmetic.'),
'collections_utilities':('GKgpvriuQY8','Rejected: namedtuple is not the required collections.Counter operation.'),
'pip_installation':('AMdG7IjgSPM','Rejected: the title substitutes UV for pip and venv; this lesson targets python -m pip.'),
'generator_functions':('2eiFCQ-YAf4','Rejected: the title explicitly advertises Expert Python, above the introductory yield target.'),
'enumerate_iteration':('4a777yQwj04','Rejected: threading.enumerate concerns threads rather than numbered collection iteration.'),
'regular_expressions':('jSYPHA02OY0','Rejected: network automation, BGP and IOS require professional networking context outside this native re lesson.')}
reject_open={
'object_introspection':(6,'Rejected: Pydantic/FastAPI data validation is a framework topic, not basic object introspection.'),
'review_generated_dependencies':(2,'Rejected: the threat-focused title reads as security commentary rather than a bounded Python dependency-verification demonstration.'),
'verify_generated_api_claims':(0,'Rejected: building a ChatGPT API client is not checking generated claims against Python API documentation.'),
'read_generated_code':(2,'Rejected: building an AI agent is the wrong learning target; this unit reviews supplied Python rather than implementing agents.'),
'accept_repair_or_reject_generated_code':(7,'Rejected: Pytest introduces a different test framework; this unit relies on the already taught unittest checks.'),
'unittest_setup_and_teardown':(11,'Rejected: pytest fixtures are not unittest setUp, tearDown and addCleanup.'),
'random_vs_secrets':(1,'Rejected: the title explicitly says Hindi, whereas English instructional video is required.')}
# Likely topic drift, expressed exclusively with real concept IDs; filtered per row against the frozen blocked list.
drift={
'variables_assignment':'core_data_types arithmetic_operators variable_scope classes_and_instances',
'core_data_types':'type_conversion lists aliasing_mutability_and_copying', 'arithmetic_operators':'comparison_operators logical_operators math_utilities floating_point_limits',
'logical_operators':'conditional_statements truth_value_testing', 'conditional_statements':'while_loops nested_loops',
'while_loops':'for_loops loop_control', 'lists':'tuples sets comprehensions nested_collections sorting_with_key_functions',
'sets':'comprehensions collection_selection', 'dictionaries':'comprehensions nested_collections',
'defining_calling_functions':'parameters_arguments return_values function_default_keyword_args variable_scope',
'parameters_arguments':'function_default_keyword_args variadic_arguments_and_unpacking safe_mutable_defaults',
'return_values':'variable_scope functions_as_values generator_functions', 'variable_scope':'closures_and_enclosing_scope functions_as_values',
'error_handling':'raising_exceptions finally_cleanup custom_exceptions', 'import_statements':'local_modules importable_packages module_search_paths',
'for_loops':'loop_control comprehensions enumerate_iteration', 'iterating_collections':'comprehensions enumerate_iteration zip_iteration',
'file_io':'with_resource_management file_modes binary_files text_file_encodings',
'console_input_output':'diagnostic_printing argparse_command_line', 'enumerate_iteration':'zip_iteration iterables_and_iterators',
'floating_point_limits':'math_utilities', 'math_utilities':'random_vs_secrets',
'nested_collections':'nested_loops aliasing_mutability_and_copying', 'range_iteration':'zip_iteration iterables_and_iterators',
'running_scripts':'main_entry_point virtual_environments argparse_command_line', 'interactive_execution':'interpreter_execution_model',
'string_methods':'regular_expressions unicode_and_bytes', 'unicode_and_bytes':'binary_files text_file_encodings',
'aliasing_mutability_and_copying':'safe_mutable_defaults classes_and_instances', 'collections_utilities':'iterables_and_iterators itertools_utilities',
'diagnostic_printing':'debugger_usage logging', 'exception_hierarchy':'custom_exceptions specific_exception_handlers',
'exception_propagation':'finally_cleanup raising_exceptions specific_exception_handlers', 'finally_cleanup':'with_resource_management',
'functions_as_values':'closures_and_enclosing_scope lambdas sorting_with_key_functions', 'closures_and_enclosing_scope':'classes_and_instances generator_functions',
'pathlib_paths':'pathlib_filesystem_operations file_modes', 'raising_exceptions':'custom_exceptions specific_exception_handlers',
'debugger_usage':'logging', 'safe_mutable_defaults':'classes_and_instances', 'classes_and_instances':'instance_initialization instance_methods inheritance_and_super',
'instance_initialization':'class_and_static_methods inheritance_and_super', 'instance_methods':'class_and_static_methods inheritance_and_super',
'class_and_static_methods':'inheritance_and_super special_methods', 'composition':'inheritance_and_super',
'inheritance_and_super':'special_methods', 'instance_vs_class_attributes':'special_methods object_introspection',
'json_serialization':'file_and_format_errors', 'pathlib_filesystem_operations':'with_resource_management review_generated_file_operations',
'special_methods':'iterables_and_iterators', 'text_file_encodings':'binary_files', 'file_and_format_errors':'with_resource_management',
'with_resource_management':'binary_files', 'local_modules':'importable_packages main_entry_point module_search_paths',
'importable_packages':'module_search_paths pip_installation', 'logging':'os_environment', 'main_entry_point':'argparse_command_line',
'virtual_environments':'pip_installation requirements_files', 'environment_interpreter_selection':'pip_installation requirements_files',
'iterables_and_iterators':'generator_functions generator_expressions iterator_consumption_and_exhaustion',
'generator_functions':'generator_expressions eager_vs_lazy_processing', 'generator_expressions':'iterator_consumption_and_exhaustion eager_vs_lazy_processing',
'iterator_consumption_and_exhaustion':'eager_vs_lazy_processing itertools_utilities', 'eager_vs_lazy_processing':'itertools_utilities map_and_filter',
'unittest_test_cases':'unittest_execution_and_results unittest_setup_and_teardown', 'unittest_execution_and_results':'unittest_setup_and_teardown',
'read_generated_code':'review_generated_file_operations review_untrusted_input_and_execution verify_generated_api_claims',
'review_generated_file_operations':'review_untrusted_input_and_execution', 'verify_generated_api_claims':'review_generated_dependencies accept_repair_or_reject_generated_code',
'review_generated_dependencies':'accept_repair_or_reject_generated_code'}
concepts={(x['concept_id'],x['path_id']):x for x in E['concepts']};briefs={(x['concept_id'],x['path_id']):x for x in F['briefs']};paths={x['path_id']:x for x in E['paths']}
notes={
'exception_hierarchy':'A general exception tutorial is a plausible location for built-in exception relationships, not proof that hierarchy facts are covered.',
'exception_propagation':'A general exception tutorial may contain a call-stack failure example; propagation coverage is not established by its title.',
'reading_tracebacks':'Keep only a traceback-reading or basic error-location section, not later exception design.',
'review_generated_file_operations':'The operational file tutorial is a possible visual aid for tracing copy, rename and delete calls; it does not itself establish generated-code review or safe-path coverage.',
'read_generated_code':'The code-reading tutorial may support a trace-based review of supplied code; Python-specific returns and branches still require segment verification.',
'verify_generated_api_claims':'The title directly targets spotting fake API methods and verification; a Python-specific official-documentation demonstration still needs verification.',
'review_generated_dependencies':'The title targets hallucinated Python imports; distribution identity, index source and standard-library alternatives remain unverified.',
'accept_repair_or_reject_generated_code':'The title directly questions generated Python correctness through code review; bounded behavior tests and unsafe-operation review remain unverified.',
'pip_installation':'Check that the selected cut demonstrates python -m pip in the selected interpreter; a general pip title does not establish that invocation.',
'requirements_files':'A package/environment tutorial is a plausible place for dependency export and recreation; requirements-file commands remain unverified.',
'object_introspection':'Use only basic type/attribute inspection; exclude dynamic mutation examples and later framework/type-hint material.',
'pathlib_paths':'Use a path construction/resolution cut only, deferring filesystem mutation.',
'with_resource_management':'Use the existing with statement for file cleanup; exclude construction of custom context managers.',
'binary_files':'Seek raw bytes read/write modes; exclude pickle and text-decoding detours.'}

def candidate(v,via,short,verdict='kept',reason=None):
 if reason is None:
  name=next(c['concept_name'] for c in E['concepts'] if c['concept_id']=='python.'+short)
  reason=f'Kept provisionally: title "{v["title"]}" suggests an instructional segment relevant to {name}; {v["duration_seconds"]} seconds permits a bounded excerpt rather than whole-video assignment. '+notes.get(short,'Required-fact coverage, visual mode and prerequisite leakage must be checked from the transcript and segment evidence; title metadata alone does not establish them.')
  if via=='reused_segment':reason='Kept: exact-concept registry lookup points to an approved segment in this source. Recheck the cut against this path\'s required facts and blocked future knowledge; approval on another path is not full local coverage. '+reason.removeprefix('Kept provisionally: ')
 return {k:v[k] for k in ['video_id','title','channel_id','channel_name','duration_seconds']}|{'youtube_url':'https://www.youtube.com/watch?v='+v['video_id'],'found_via':via,'filter_verdict':verdict,'reason':reason}
searches=[]
for g in G['entries']:
 if g['video_need']['level'] not in ('HIGH','MEDIUM'):continue
 cid=g['concept_id'];short=cid.split('.')[1];key=(cid,g['path_id']);c=concepts[key];f=briefs[key]
 candidates=[]
 for vid in S.get(short,[]):candidates.append(candidate(V[vid],'reused_segment' if vid in R.get(cid,[]) else 'allowlist_catalogue',short))
 pre_open_count=len(candidates)
 if short in O:
  assert pre_open_count<2,(short,pre_open_count)
  for i in open_kept.get(short,[]):
   v=O[short]['results'][i]
   if v['video_id'] not in [x['video_id'] for x in candidates]:candidates.append(candidate(V[v['video_id']] if v['video_id'] in V else v,'allowlist_catalogue' if v['video_id'] in V else 'open_search',short))
 if short in reject_catalog:
  vid,reason=reject_catalog[short];candidates.append(candidate(V[vid],'allowlist_catalogue',short,'rejected',reason))
 if short in reject_open:
  i,reason=reject_open[short];v=O[short]['results'][i];candidates.append(candidate(V[v['video_id']] if v['video_id'] in V else v,'allowlist_catalogue' if v['video_id'] in V else 'open_search',short,'rejected',reason))
 blocked=[x for x in ['python.'+s for s in drift.get(short,'').split()] if x in c['blocked_knowledge_ids']][:4]
 searches.append({'concept_id':cid,'path_id':g['path_id'],'search_brief':{'concept_name':c['concept_name'],'learner_level':paths[g['path_id']]['learner_scope'],'required_fact_ids':[x['id'] for x in f['evidence']['required_facts']],'preferred_visual_modes':g['video_need']['preferred_visual_modes'],'blocked_concepts_to_avoid':blocked},'search_route':'allowlist_then_open_search' if short in O else 'reused_segments_only' if candidates and all(x['found_via']=='reused_segment' for x in candidates) else 'allowlist_only','candidates':candidates})
inputs=[B/x for x in ['glossary_pass_a.json','registry_lookup.json','extracted_concepts.json','coverage_briefs.json','approved_segments_snapshot.json']]+[CORE/'video_bank/channel_allowlist.json']+sorted((CORE/'video_bank/channel_catalogs').glob('*.json'))
hashes={p.name if p.parent==B else str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs}
m=G['metadata'].copy();m.update(artifact_type='video_candidates',prompt_version='06_video_candidates@v1',model='none',generated_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),parent_artifact_hashes=hashes)
artifact={'metadata':m,'batch_id':B.name,'searches':searches};json.dump(artifact,open(B/'video_candidates.part.all.json','w'),indent=2,ensure_ascii=False)
# Deterministic mistakes checklist: full coverage, no duplicates, IDs from real sources, byte-matched catalogues,
# exact fact/mode/level copying, real blocked references, threshold routing, kept cap, URLs and parent hashes.
expected={(g['concept_id'],g['path_id']) for g in G['entries'] if g['video_need']['level'] in ('HIGH','MEDIUM')}
assert len(searches)==len(expected)==len({(s['concept_id'],s['path_id']) for s in searches})
for s in searches:
 key=(s['concept_id'],s['path_id']);c=concepts[key];f=briefs[key];g=next(x for x in G['entries'] if (x['concept_id'],x['path_id'])==key)
 assert set(s['search_brief']['blocked_concepts_to_avoid'])<=set(c['blocked_knowledge_ids'])
 assert s['search_brief']['required_fact_ids']==[x['id'] for x in f['evidence']['required_facts']]
 assert s['search_brief']['preferred_visual_modes']==g['video_need']['preferred_visual_modes']
 assert s['search_brief']['learner_level']==paths[s['path_id']]['learner_scope']
 assert len({x['video_id'] for x in s['candidates']})==len(s['candidates'])
 assert sum(x['filter_verdict']=='kept' for x in s['candidates'])<=5
 for x in s['candidates']:
  assert x['youtube_url']=='https://www.youtube.com/watch?v='+x['video_id']
  assert re.fullmatch(r'[A-Za-z0-9_-]{11}',x['video_id']) and x['reason']
  if x['found_via'] in ('allowlist_catalogue','reused_segment'):
   assert all(x[k]==V[x['video_id']][k] for k in ['title','channel_id','channel_name','duration_seconds'])
   if x['found_via']=='reused_segment':assert x['video_id'] in R[s['concept_id']]
  else:
   source=next(v for v in O[s['concept_id'].split('.')[1]]['results'] if v['video_id']==x['video_id'])
   assert re.search(r'[?&]v='+re.escape(x['video_id']),source['result_url'])
   assert all(x[k]==source[k] for k in ['title','channel_id','channel_name','duration_seconds'])
counts=collections.Counter(x['filter_verdict'] for s in searches for x in s['candidates'])
check={'all_checks_passed':True,'search_rows':len(searches),'candidate_rows':sum(counts.values()),'filter_counts':dict(counts),'route_counts':dict(collections.Counter(s['search_route'] for s in searches)),'unique_videos':len({x['video_id'] for s in searches for x in s['candidates']}),'catalogues_searched':len(list((CORE/'video_bank/channel_catalogs').glob('*.json'))),'catalogue_rows_searched':len(V),'checklist':['whole HIGH/MEDIUM batch, LOW/NONE excluded','exact source titles/channels/durations and real URL provenance','registry reuse first','open routing only below two curated catalogue/reused candidates','max five kept and distinct video IDs per concept','blocked IDs checked against real blocked_knowledge_ids','required fact IDs, learner_scope and preferred modes copied exactly','metadata hashes and real UTC timestamp','no claims of transcript, visual or full fact coverage; rejected hits carry reasons']}
json.dump(check,open(B/'working/video_candidates_self_check.json','w'),indent=2);print(json.dumps(check,indent=2))
