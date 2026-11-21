import json,re,pathlib
B=pathlib.Path('batches/glossary_batch_learn_python'); C=pathlib.Path('00_GLOSSARY_PIPELINE_CORE/video_bank/channel_catalogs')
channels={x['channel_id']:x['channel_name'] for x in json.load(open(C.parent/'channel_allowlist.json'))['channels']}
V=[]
for f in sorted(C.glob('*.json')):
 d=json.load(open(f))
 V.extend(dict(v,channel_id=d['channel_id'],channel_name=channels[d['channel_id']],catalog_path=str(f)) for v in d['videos'])
json.dump(V,open(B/'working/all_catalog_metadata.json','w'))
queries={
'variables_assignment':r'variables|assignment', 'core_data_types':r'data types|data type|numbers|integers|floats','arithmetic_operators':r'arithmetic|basic operators|numbers|operators',
'logical_operators':r'logical operators|boolean|conditions', 'type_conversion':r'type cast|type conversion|typecasting', 'conditional_statements':r'if.elif|if statements|conditionals|conditional statements', 'while_loops':r'while loop',
'lists':r'lists|list tutorial', 'sets':r'sets|set tutorial', 'dictionaries':r'dictionaries|dictionary', 'defining_calling_functions':r'functions', 'parameters_arguments':r'functions|parameters|arguments', 'return_values':r'return|functions', 'variable_scope':r'scope|global vs local',
'error_handling':r'exception|try.*except|error handling', 'import_statements':r'import|modules', 'for_loops':r'for loops|for loop', 'loop_control':r'break|continue|loop control', 'iterating_collections':r'iteration by item|for loops|for loop', 'comprehensions':r'comprehensions|comprehension', 'file_io':r'file objects|read.*file|writ.*file|file handling', 'console_input_output':r'input|print', 'enumerate_iteration':r'enumerate', 'floating_point_limits':r'floating.point|float.*precision|float.*error', 'indentation_and_blocks':r'indentation|code blocks', 'math_utilities':r'math module|math functions', 'nested_collections':r'nested.*list|nested.*dictionar|2d.*list|2d collection', 'nested_loops':r'nested loop', 'range_iteration':r'range function|range\(\)|range tutorial', 'running_scripts':r'running.*python|run.*script|installation and setup', 'statements_and_expressions':r'statements.*expressions|expressions.*statements', 'interactive_execution':r'interactive|repl|installation and setup', 'string_methods':r'string methods|strings.*textual', 'unicode_and_bytes':r'unicode|encoding.*decoding|bytes', 'zip_iteration':r'zip function|zip\(\)|zip.*iteration', 'aliasing_mutability_and_copying':r'mutable.*immutable|copy|mutability', 'collections_utilities':r'counter|collections', 'diagnostic_printing':r'print debugging|debug.*print|debugging', 'exception_hierarchy':r'exception|error handling', 'exception_propagation':r'exception|error handling', 'finally_cleanup':r'finally|exception', 'functions_as_values':r'first.class functions|functions.*values|higher.order', 'closures_and_enclosing_scope':r'closures|closure', 'pathlib_paths':r'pathlib', 'raising_exceptions':r'rais.*exception|exception', 'reading_tracebacks':r'traceback|error handling', 'debugger_usage':r'debugger|debugging', 'safe_mutable_defaults':r'mutable default', 'sorting_with_key_functions':r'sorting|sorted', 'specific_exception_handlers':r'exception|error handling', 'variadic_arguments_and_unpacking':r'args|kwargs|unpacking', 'classes_and_instances':r'classes.*instances|classes.*objects|oop.*intro|creating classes', 'file_modes':r'file objects|file modes|file handling|read.*writ.*file', 'instance_initialization':r'classes.*instances|creating classes|__init__|constructor', 'instance_methods':r'classes.*instances|self|creating classes', 'class_and_static_methods':r'class methods|static methods|classmethod|staticmethod', 'composition':r'composition', 'inheritance_and_super':r'inheritance|super', 'custom_exceptions':r'custom exception', 'instance_vs_class_attributes':r'class variables|class attributes|instance.*attributes', 'json_serialization':r'json', 'object_introspection':r'introspection|dir\(|getattr|hasattr|object.*type', 'pathlib_filesystem_operations':r'pathlib', 'special_methods':r'special.*method|magic.*method|dunder.*method|repr', 'text_file_encodings':r'encoding|unicode|file objects', 'file_and_format_errors':r'exception|error handling|json', 'with_resource_management':r'context manager|with statement', 'binary_files':r'binary.*file|bytes|file objects', 'datetime_operations':r'datetime', 'local_modules':r'modules|import', 'importable_packages':r'packages|modules', 'logging':r'logging', 'main_entry_point':r'__main__|main.*function|if __name__', 'argparse_command_line':r'argparse', 'module_search_paths':r'import|module.*path', 'os_environment':r'environment variables|os module|dotenv', 'random_vs_secrets':r'secrets|random', 'regular_expressions':r'regular expressions|regex', 'virtual_environments':r'venv|virtual environment', 'environment_interpreter_selection':r'venv|virtual environment|development environment', 'pip_installation':r'pip|install.*packages', 'requirements_files':r'requirements|pip|venv|virtual environment', 'iterables_and_iterators':r'iterators|iterables', 'generator_functions':r'generators|generator|yield', 'generator_expressions':r'generators|generator', 'iterator_consumption_and_exhaustion':r'iterators|iterables|generators', 'eager_vs_lazy_processing':r'lazy|generators|generator', 'itertools_utilities':r'itertools', 'map_and_filter':r'map.*filter|map\(\)|filter\(\)', 'unittest_test_cases':r'unittest|unit testing', 'unittest_execution_and_results':r'unittest|unit testing', 'unittest_setup_and_teardown':r'unittest|unit testing',
'read_generated_code':r'(review|validat|test|debug|read|understand|explain).*(ai.generated|generated code|chatgpt)|(ai.generated|generated code|chatgpt).*(review|validat|test|debug|understand|explain)',
'review_generated_file_operations':r'(ai.generated|generated code|chatgpt).*(file|safe|secur)|(safe|secur|file).*(ai.generated|generated code|chatgpt)',
'review_untrusted_input_and_execution':r'eval|exec\(|untrusted|injection|arbitrary.*code',
'verify_generated_api_claims':r'(ai|llm|chatgpt).*(hallucinat|verif)|(verif|hallucinat).*(ai|llm|chatgpt)',
'review_generated_dependencies':r'(ai|llm|chatgpt).*(dependencies|package.*hallucinat)|(package.*hallucinat).*(ai|llm|chatgpt)',
'accept_repair_or_reject_generated_code':r'(review|validat|test|debug).*(ai.generated|generated code|chatgpt)|(ai.generated|generated code|chatgpt).*(review|validat|test|debug)'
}
priority={'Corey Schafer':35,'Bro Code':30,'Tech With Tim':25,'Patrick Loeber':25,'Telusko':15,'CS Dojo':15,'freeCodeCamp.org':10,'ArjanCodes':5}
bad=r'fastapi|django|flask|pandas|numpy|tensorflow|pytorch|machine learning|web scraping|selenium|pygame|tkinter|discord|trading|interview|leetcode|hindi|#shorts|\bshorts\b|cybersecurity|keylogger|hack|news|roadmap|masterclass|deep dive|advanced|metaclass|decorator|design pattern'
E=json.load(open(B/'extracted_concepts.json'))['concepts'];G={x['concept_id']:x for x in json.load(open(B/'glossary_pass_a.json'))['entries']}
R={}
for c in E:
 cid=c['concept_id'];short=cid.split('.')[1]
 if G[cid]['video_need']['level'] not in ('HIGH','MEDIUM'):continue
 hits=[]
 for v in V:
  t=v['title'].lower()
  if 'python' not in t or not re.search(queries[short],t):continue
  reject=bool(re.search(bad,t)) or v['channel_name']=='CodeWithHarry' or not v.get('duration_seconds')
  score=priority.get(v['channel_name'],0)+20+(10 if 'tutorial' in t else 0)-(20 if (v.get('duration_seconds') or 0)>3600 else 0)
  if short not in ['generator_functions','generator_expressions','iterator_consumption_and_exhaustion','eager_vs_lazy_processing'] and 'intermediate' in t:score-=10
  hits.append((reject,-score,v.get('duration_seconds') or 0,v))
 hits.sort(key=lambda x:x[:3]);selected=[v for rej,s,d,v in hits if not rej][:5]
 R[cid]=[v['video_id'] for v in selected]
 print('\n'+cid)
 for v in selected:print(v['video_id'],v['channel_name'],v['duration_seconds'],v['title'])
json.dump(R,open(B/'working/preliminary_selection.json','w'),indent=2)
