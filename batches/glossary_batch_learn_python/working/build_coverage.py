import json,hashlib,copy,datetime
from pathlib import Path
P=Path('batches/glossary_batch_learn_python')
E=json.loads((P/'extracted_concepts.json').read_text());L=json.loads((P/'registry_lookup.json').read_text());R=json.loads((P/'concept_evidence_registry_snapshot.json').read_text())
lookup={(r['concept_id'],r['path_id']):r for r in L['lookups']};registry={r['concept_id']:r for r in R['entries']};data={}
def add(name,*facts):
 data['python.'+name]=[{'id':f'f{i+1}','statement':s,'source_refs':[ref]} for i,(s,ref) in enumerate(facts)]
def T(page,anchor):return 'python_tutorial#'+page+'.html#'+anchor
def S(page,anchor):return 'python_stdlib_reference#'+page+'.html#'+anchor
def Q(page,anchor):return 'python_language_reference#'+page+'.html#'+anchor
# Work in frozen tile order; earlier registry rows are copied below, not regenerated.
add('collection_selection',
 ('A list is a mutable sequence whose items can be accessed by position.',S('stdtypes','lists')),
 ('A tuple is an immutable sequence whose items can be accessed by position.',S('stdtypes','tuples')),
 ('A set is a mutable, unordered collection of distinct hashable elements and does not support positional indexing.',S('stdtypes','set-types-set-frozenset')),
 ('A dictionary is mutable, maps unique hashable keys to values and preserves insertion order.',S('stdtypes','mapping-types-dict-frozendict')),
 ('Use d[key] to retrieve a dictionary value by its key, rather than a sequence item by its position.',S('stdtypes','mapping-types-dict-frozendict')))
add('console_input_output',
 ('input(prompt) displays the prompt without a trailing newline and returns the entered line as a string with its trailing newline removed.',S('functions','input')),
 ('print(*objects) converts its arguments to strings, separates them with spaces by default and ends with a newline by default.',S('functions','print')),
 ('Store the result of input(prompt) in a name and pass that name alongside greeting text to print to display the entered value.',S('functions','print')))
add('enumerate_iteration',
 ('enumerate(sequence, start=0) yields pairs containing a count and the corresponding value; the count starts at zero by default.',S('functions','enumerate')),
 ('Use for position, value in enumerate(sequence, start=1): followed by the loop body to label entries from one without manually updating a counter.',S('functions','enumerate')))
add('floating_point_limits',
 ('Many decimal fractions cannot be represented exactly as binary floating-point values, so stored values and arithmetic results can be approximations.',T('floatingpoint','floating-point-arithmetic-issues-and-limitations')),
 ('Use math.isclose(actual, expected, rel_tol=..., abs_tol=...) to compare computed floats within chosen relative and absolute tolerances.',S('math','math.isclose')),
 ('math.isclose uses abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol), with defaults rel_tol=1e-9 and abs_tol=0.0.',S('math','math.isclose')),
 ('When comparing a nonzero value to zero with math.isclose, supply a positive abs_tol appropriate to the expected closeness.',S('math','math.isclose')))
add('indentation_and_blocks',
 ('Leading whitespace determines the grouping of statements into blocks.',Q('lexical_analysis','indentation')),
 ('A multiline suite follows its header and colon on indented lines, with statements at the same indentation belonging to the same suite.',Q('compound_stmts','compound-statements')),
 ('Indent a nested header inside the enclosing suite and indent its body further; dedenting ends the nested suite.',Q('lexical_analysis','indentation')),
 ('Mixing tabs and spaces is rejected when the meaning of indentation depends on the worth of a tab in spaces.',Q('lexical_analysis','indentation')))
add('math_utilities',
 ('Import math and call math.sqrt(x) to obtain the square root of x.',S('math','math.sqrt')),
 ('math functions operate on real arguments, and the documented implementation raises ValueError for invalid operations such as sqrt(-1.0).',S('math','module-math')))
add('nested_collections',
 ('Collections can contain other collections, so each subscription selects one level of the structure.',T('datastructures','nested-list-comprehensions')),
 ('Use a list index or dictionary key at each successive level, as in records[i][key][j], to reach a nested value.',T('datastructures','dictionaries')),
 ('Assign to the final subscription, as in records[i][key][j] = value, to replace that nested item.',Q('simple_stmts','assignment-statements')))
add('nested_loops',
 ('For each item of an outer for loop, its body runs, including a complete traversal of any inner loop reached in that body.',T('controlflow','for-statements')),
 ('Traverse a nested list with for row in rows: and an indented for cell in row: whose further-indented body processes each cell.',T('datastructures','nested-list-comprehensions')))
add('range_iteration',
 ('range(stop) starts at zero and uses a step of one, while range(start, stop, step) permits an explicit starting value and stride.',S('stdtypes','ranges')),
 ('For a positive step, range includes values less than stop; for a negative step, it includes values greater than stop.',S('stdtypes','ranges')),
 ('Use for i in range(start, stop, 2): to visit every second integer position within a chosen increasing bound.',S('stdtypes','ranges')),
 ('A range step cannot be zero.',S('stdtypes','ranges')))
add('running_scripts',
 ('Invoke a saved script with the intended Python executable followed by the script path; the interpreter reads and executes that file.',T('interpreter','invoking-the-interpreter')),
 ('A script runs in a new interpreter invocation, rather than inheriting names from a previous interactive session.',T('interpreter','invoking-the-interpreter')),
 ('print writes to standard output by default, which is the script output to inspect for displayed results.',S('functions','print')),
 ('An exit status of zero indicates successful termination, while a nonzero status indicates abnormal termination.',S('sys','sys.exit')))
add('statements_and_expressions',
 ('An expression is evaluated to produce a value; an assignment statement binds its target to the resulting object.',Q('simple_stmts','assignment-statements')),
 ('Trace an assignment by evaluating the right-hand expression before changing the target binding.',Q('expressions','evaluation-order')),
 ('Expressions are evaluated left to right, with operator precedence determining how their parts are grouped.',Q('expressions','evaluation-order')))
add('comments',
 ('A comment starts with # outside a string literal and ends at the end of the physical line; it is ignored by the syntax.',Q('lexical_analysis','comments')),
 ('Keep comments consistent with the code and avoid inline comments that merely state the obvious.', 'pep8_style_guide#comments'),
 ('Use an inline comment sparingly to explain information that the operation itself does not make obvious.', 'pep8_style_guide#inline-comments'))
add('interactive_execution',
 ('Starting the interpreter without a script allows commands to be entered at the interactive prompt.',T('interpreter','interactive-mode')),
 ('Interactive expression statements can display computed results, while assignments do not display the assigned values.',Q('simple_stmts','expression-statements')),
 ('Assignments bind names in the session, so later commands can use those names; restart the interpreter to check an expression without earlier bindings.',T('introduction','numbers')))
add('interpreter_execution_model',
 ('A Python module or interactive command is a code block executed as a unit.',Q('executionmodel','structure-of-a-program')),
 ('CPython compiles Python source into bytecode instructions that its interpreter executes.',S('dis','module-dis')),
 ('Syntax errors occur while parsing source, whereas exceptions can occur when syntactically correct code executes.',T('errors','syntax-errors')),
 ('Trace top-level execution in statement order, evaluating the expressions and updating bindings as each executed statement requires.',Q('simple_stmts','assignment-statements')))
add('multiline_expressions',
 ('Expressions inside parentheses, square brackets or braces can span physical lines without backslashes.',Q('lexical_analysis','implicit-line-joining')),
 ('Reformat a long call by breaking lines inside its argument parentheses while keeping its arguments and operators unchanged.',Q('lexical_analysis','implicit-line-joining')))
add('string_methods',
 ('s.strip() returns a copy with leading and trailing whitespace removed, leaving interior whitespace intact.',S('stdtypes','str.strip')),
 ('s.lower() returns a copy with cased characters converted to lowercase.',S('stdtypes','str.lower')),
 ('s.split(sep) returns a list split on the specified delimiter, including empty fields between consecutive delimiters.',S('stdtypes','str.split')),
 ('s.split() without a separator groups runs of whitespace and omits leading and trailing empty fields.',S('stdtypes','str.split')),
 ('String methods return transformed values rather than modifying the original string, so assign the returned value when retaining a normalized label.',S('stdtypes','string-methods')))
add('syntax_vs_runtime_errors',
 ('A SyntaxError reports a failure to parse source and can occur before the intended code executes.',T('errors','syntax-errors')),
 ('An exception can occur while executing a statement or expression that is syntactically correct.',T('errors','exceptions')),
 ('Use the reported source line and location to repair a syntax failure, then rerun to investigate any execution-time exception.',T('errors','syntax-errors')))
add('truth_value_testing',
 ('False, None, numeric zero and empty built-in sequences or collections test false; nonempty built-in collections test true.',S('stdtypes','truth-value-testing')),
 ('Use if collection: for a nonempty guard or if not collection: for an empty guard instead of comparing the collection to True.',S('stdtypes','truth-value-testing')))
add('none_and_identity',
 ('None is the single object frequently used to represent the absence of a value.',S('constants','None')),
 ('Use value is None or value is not None to check for that object specifically.',Q('expressions','is-not')),
 ('A truth-value test also rejects zero and empty values, whereas an identity check against None distinguishes them from absence.',S('stdtypes','truth-value-testing')))
add('unicode_and_bytes',
 ('str represents Unicode text, whereas bytes represents a sequence of byte values.',S('stdtypes','text-sequence-type-str')),
 ('text.encode("utf-8") produces UTF-8 bytes, and payload.decode("utf-8") reconstructs text from correctly encoded bytes.',S('stdtypes','str.encode')))
add('zip_iteration',
 ('zip(a, b) yields tuples of corresponding elements and by default stops when the shortest input is exhausted.',S('functions','zip')),
 ('Use for left, right in zip(a, b): followed by an indented body to work with paired values.',S('functions','zip')))
add('aliasing_mutability_and_copying',
 ('Assignment binds another name to an object rather than copying that object, so mutations through either alias can affect the same collection.',T('classes','a-word-about-names-and-objects')),
 ('Use list.copy() or a full list slice to create a shallow copy before changing the outer list independently.',T('datastructures','more-on-lists')),
 ('A shallow copy creates a new outer collection but retains references to nested objects, so mutating a shared nested object can still affect the original.',S('copy','module-copy')))
add('collections_utilities',
 ('Import Counter from collections and call Counter(iterable) to count occurrences, with each element as a key and its count as the value.',S('collections','collections.Counter')),
 ('counter.most_common(1) returns a list containing the most frequent element and its count, or an empty list for an empty counter.',S('collections','collections.Counter.most_common')),
 ('Equal counts in most_common are ordered by first encounter, so a tie does not establish a uniquely most frequent element.',S('collections','collections.Counter.most_common')))
add('diagnostic_printing',
 ('Use labeled print output at relevant execution points to compare observed values with the expected behavior.', 'think_python#chap12.html#debugging'),
 ('repr(value) gives a printable representation that can reveal string quotes and escapes obscured by ordinary display.',S('functions','repr')),
 ('Remove temporary diagnostic prints once the problem has been resolved.', 'think_python#chap06.html#incremental-development'))
add('docstrings',
 ('A string literal as the first statement of a function body becomes that function\'s docstring.',T('controlflow','documentation-strings')),
 ('Write a concise summary followed when needed by details of arguments, return values and relevant exceptions, keeping the documentation consistent with the function.', 'pep8_style_guide#documentation-strings'),
 ('Use help(function) to inspect the function\'s documentation.',S('functions','help')))
add('exception_hierarchy',
 ('BaseException is the base class of built-in exceptions, while Exception is the base class for non-system-exiting exceptions.',S('exceptions','BaseException')),
 ('ValueError and OSError are subclasses of Exception, and FileNotFoundError is a subclass of OSError.',S('exceptions','exception-hierarchy')),
 ('KeyboardInterrupt and SystemExit inherit directly from BaseException rather than Exception.',S('exceptions','exception-hierarchy')),
 ('Use the documented hierarchy to place an exception beneath its parent instead of treating all exception types as siblings.',S('exceptions','exception-hierarchy')))
add('exception_propagation',
 ('If an exception is not handled in the current function, handling is sought in surrounding execution contexts and callers.',T('errors','handling-exceptions')),
 ('Once an exception interrupts a try suite, its remaining statements are skipped and the first matching except clause is executed.',T('errors','handling-exceptions')),
 ('Trace a call-chain failure from the raising operation outward to the matching handler; an unhandled exception stops execution with an error report.',T('errors','handling-exceptions')))
add('finally_cleanup',
 ('A finally suite executes as the try statement is left, whether the try suite succeeds or raises an exception.',T('errors','defining-clean-up-actions')),
 ('Place the resource-release operation in finally after a try suite to perform cleanup when leaving that suite.',T('errors','defining-clean-up-actions')),
 ('A return from try runs finally before returning, while an unhandled exception is re-raised after finally finishes normally.',T('errors','defining-clean-up-actions')))
add('functions_as_values',
 ('A function name refers to a function object that can be assigned to another name or passed as an argument.',T('controlflow','defining-functions')),
 ('Pass transform rather than transform(value) when the receiver needs the callable itself, then call transform(value) inside the receiving helper.',T('controlflow','lambda-expressions')))
add('closures_and_enclosing_scope',
 ('A nested function can refer to bindings in an enclosing function scope, retaining access when the nested function is returned.',Q('executionmodel','resolution-of-names')),
 ('Use nonlocal name in the nested function to rebind an existing name in the nearest enclosing function scope.',Q('simple_stmts','the-nonlocal-statement')),
 ('For an independent-state counter factory, initialize the state inside each factory call, define a nested function that updates it using nonlocal, and return that function.',T('classes','python-scopes-and-namespaces')))
add('pathlib_paths',
 ('from pathlib import Path provides path objects with the appropriate concrete path form for the platform.',S('pathlib','concrete-paths')),
 ('Join a base path and a relative child with base / child; an absolute child discards preceding path components.',S('pathlib','operators')),
 ('Relative filesystem paths are interpreted from the current working directory, which Path.cwd() reports.',S('pathlib','pathlib.Path.cwd')),
 ('Build a project-relative output path by starting from the chosen project directory rather than assuming the current working directory is that directory.',S('pathlib','operators')))
add('raising_exceptions',
 ('Use raise ExceptionType(message) to signal a failure explicitly.',T('errors','raising-exceptions')),
 ('ValueError indicates an argument of an appropriate type but an inappropriate value when no more precise exception describes the situation.',S('exceptions','ValueError')),
 ('Put useful failure context in the exception message so the reported exception explains what was rejected.',T('errors','raising-exceptions')))
add('reading_tracebacks',
 ('A traceback shows the execution context leading to an exception, followed by the exception type and explanatory message.',T('errors','exceptions')),
 ('Read the reported file, line and statement for each frame to follow calls toward the failing operation.',T('errors','exceptions')),
 ('Use the final exception description together with the relevant source frame to locate the failure rather than treating the calling line alone as its cause.',T('errors','exceptions')))
add('debugger_usage',
 ('Insert pdb.set_trace() after importing pdb to enter the debugger at the calling frame.',S('pdb','pdb.set_trace')),
 ('Use p expression to examine a value and where to display the stack.',S('pdb','debugger-commands')),
 ('Use step to enter called functions, next to advance within the current function and continue to resume until a breakpoint.',S('pdb','debugger-commands')),
 ('Use break line to stop at a source line, then inspect the condition values that determine the branch.',S('pdb','debugger-commands')))
add('safe_mutable_defaults',
 ('A default argument value is evaluated once at function definition, so a mutable default object can be shared across calls.',T('controlflow','default-argument-values')),
 ('Replace a default list with a None default and create a new list inside the function when the argument is None.',T('controlflow','default-argument-values')))
add('sorting_with_key_functions',
 ('sorted(iterable, key=function) returns a new sorted list, whereas list.sort(key=function) changes the list in place.',S('functions','sorted')),
 ('The key callable receives each item and provides the value used for sorting, so pass a function that derives the required normalized key.',S('functions','sorted')),
 ('Sorting is stable: items with equal keys retain their original relative order.',S('functions','sorted')))
add('lambda_expressions',
 ('lambda parameters: expression creates a function whose result is that expression, without a statement body.',T('controlflow','lambda-expressions')),
 ('Pass key=lambda item: expression to a sorting operation to supply a one-expression key transformation.',T('controlflow','lambda-expressions')))
add('specific_exception_handlers',
 ('An except clause matches its named exception class and subclasses, and the first matching clause handles the exception.',T('errors','handling-exceptions')),
 ('Place except FileNotFoundError: before except OSError: to keep the specific recovery branch reachable for missing files.',S('exceptions','exception-hierarchy')))
add('validation_vs_programming_errors',
 ('int(text) raises ValueError for text that does not represent a valid integer; catch it at the input boundary and report rejection when the contract requires a numeric input.',T('errors','handling-exceptions')),
 ('NameError means a local or global name was not found; a misspelled local name should be corrected in the implementation rather than attributed to malformed numeric input.',S('exceptions','NameError')),
 ('PermissionError indicates inadequate access rights, so a valid path can still require an external-permission failure response rather than input rejection or assuming a coding defect.',S('exceptions','PermissionError')))
add('variadic_arguments_and_unpacking',
 ('A parameter of the form *args collects additional positional arguments into a tuple, while **kwargs collects additional keyword arguments into a dictionary.',T('controlflow','arbitrary-argument-lists')),
 ('Forward collected arguments with target(*args, **kwargs), using * to expand positional values and ** to expand named values.',T('controlflow','unpacking-argument-lists')),
 ('Passing more than one value for the same parameter, including a positional value and a keyword value, raises TypeError.',T('controlflow','keyword-arguments')))
add('classes_and_instances',
 ('Use class Name: followed by an indented body to define a class object.',T('classes','class-definition-syntax')),
 ('Calling a class, as in Name(), creates an instance of that class.',T('classes','instance-objects')),
 ('Two ordinary class-instantiation calls produce distinct instance objects; is compares their identities rather than merely their class.',Q('datamodel','objects-values-and-types')))
add('file_modes',
 ('open(path, "r") opens for reading and is the default mode.',S('functions','open')),
 ('open(path, "w") truncates an existing file, while open(path, "a") appends to the end.',S('functions','open')),
 ('open(path, "x") creates a file exclusively and fails if the destination already exists.',S('functions','open')),
 ('Catch FileExistsError around exclusive creation to handle an existing report destination without truncating it.',S('exceptions','FileExistsError')))
add('instance_initialization',
 ('When a class defines __init__, class instantiation calls it on the new instance with the supplied arguments.',T('classes','class-objects')),
 ('Define def __init__(self, name, quantity): and assign self.name = name and self.quantity = quantity in its body to store each instance\'s initial values.',T('classes','class-and-instance-variables')))
add('instance_methods',
 ('A method called as instance.method(arguments) receives the instance as its first argument, conventionally named self.',T('classes','method-objects')),
 ('Define def method(self, ...): in the class and use self.attribute to read or assign the receiving object\'s stored state.',T('classes','random-remarks')))
add('class_and_static_methods',
 ('An instance method receives the instance, a @classmethod receives the class as its first argument, and a @staticmethod receives no implicit first argument.',S('functions','classmethod')),
 ('Use @classmethod above def constructor(cls, ...): and return cls(...) to provide an alternative constructor tied to the receiving class.',S('functions','classmethod')),
 ('Use @staticmethod above a function that requires neither instance nor class state.',S('functions','staticmethod')))
add('composition',
 ('An instance attribute can refer to another object, making that object a contained collaborator rather than an inherited base.',T('classes','random-remarks')),
 ('Store a collaborator with self.collaborator = collaborator and delegate with self.collaborator.method(...) when its behavior is needed.',T('classes','random-remarks')))
add('encapsulation_conventions',
 ('Prefix an implementation attribute with a single underscore to mark it as a non-public API detail that may change.',T('classes','private-variables')),
 ('Expose intended operations as public methods while accessing supporting state through the implementation; underscore naming is a convention, not enforced access security.',T('classes','private-variables')))
add('inheritance_and_super',
 ('class Derived(Base): defines a subclass that can inherit base-class attributes and override methods by defining them again.',T('classes','inheritance')),
 ('Use super().method(...) in an overriding method to delegate according to the method resolution order rather than hard-coding a parent.',S('functions','super')),
 ('When defining a subclass __init__, call super().__init__(...) to retain the base initialization behavior before adding the subclass\'s state.',S('functions','super')))
add('custom_exceptions',
 ('Define class InvalidRecordError(Exception): with an indented body to create an exception type for a domain failure.',T('errors','user-defined-exceptions')),
 ('Raise InvalidRecordError(message) at the validation failure and catch except InvalidRecordError: where the caller can respond to it.',T('errors','user-defined-exceptions')))
add('instance_vs_class_attributes',
 ('Class variables hold shared attributes, while attributes assigned on self can store data unique to an instance.',T('classes','class-and-instance-variables')),
 ('A mutable list defined in the class body can be shared by instances, so append operations can unexpectedly affect other instances.',T('classes','class-and-instance-variables')),
 ('Initialize self.items = [] inside __init__ to give each instance its own list instead of mutating a shared class list.',T('classes','class-and-instance-variables')))
add('json_serialization',
 ('json.dumps(record) serializes supported Python values to a JSON string and json.loads(text) reconstructs Python values from a JSON string.',S('json','basic-usage')),
 ('JSON objects decode to dict, arrays to list, strings to str, booleans to bool and null to None.',S('json','json.JSONDecoder')),
 ('Python lists and tuples both encode as JSON arrays, so a tuple decodes back as a list.',S('json','json.JSONEncoder')),
 ('JSON object keys are strings, so a dictionary with non-string keys need not equal the dictionary obtained after serialization and reconstruction.',S('json','json.dumps')),
 ('Compare the reconstructed nested values and types with the conversion table rather than assuming round-tripping preserves every Python-specific type.',S('json','json.JSONDecoder')))
add('object_introspection',
 ('type(obj) returns an object\'s type.',S('functions','type')),
 ('isinstance(obj, Class) tests whether the object is an instance of the class or one of its subclasses.',S('functions','isinstance')),
 ('dir(obj) produces a list of attribute names useful for inspection, but its output is not necessarily complete.',S('functions','dir')),
 ('Inspect public candidate attributes by selecting names from dir(obj) that do not start with an underscore.',S('functions','dir')))
add('pathlib_filesystem_operations',
 ('Path.mkdir(parents=True, exist_ok=True) creates a directory and needed parents, allowing an existing directory but not an existing non-directory at that path.',S('pathlib','pathlib.Path.mkdir')),
 ('Path.iterdir() yields the directory\'s child paths in arbitrary order.',S('pathlib','pathlib.Path.iterdir')),
 ('source.rename(target) renames a filesystem entry to the specified target and returns a new path pointing there.',S('pathlib','pathlib.Path.rename')),
 ('A relative rename target is interpreted from the current working directory, and an existing target file is replaced on Unix but raises FileExistsError on Windows.',S('pathlib','pathlib.Path.rename')))
add('special_methods',
 ('__repr__(self) returns a string intended as an information-rich and unambiguous representation, useful for debugging.',Q('datamodel','object.__repr__')),
 ('__str__(self) returns a string intended as a convenient printable representation for str and print.',Q('datamodel','object.__str__')),
 ('Define both methods to return strings when the developer representation and user-facing display should differ.',Q('datamodel','object.__str__')))
add('text_file_encodings',
 ('Open a text file with encoding="utf-8" when its contents are UTF-8, since the unspecified default encoding is platform-dependent.',S('functions','open')),
 ('Use text-mode read and write operations with the matching explicit encoding on both files to preserve non-ASCII text.',T('inputoutput','reading-and-writing-files')),
 ('A UnicodeDecodeError indicates a decoding failure; check whether the chosen encoding matches the file\'s actual bytes.',S('exceptions','UnicodeDecodeError')))
add('file_and_format_errors',
 ('FileNotFoundError indicates a requested file or directory does not exist; handle it separately from failures in the file\'s contents.',S('exceptions','FileNotFoundError')),
 ('UnicodeDecodeError identifies bytes that could not be decoded, so report the decoding problem rather than labeling the file missing.',S('exceptions','UnicodeDecodeError')),
 ('csv.reader(file, strict=True) raises csv.Error on bad CSV input; use except csv.Error: and reader.line_num when reporting the failure location.',S('csv','csv.Dialect.strict')),
 ('A CSV parser returns fields as strings by default; check len(row) and required field values against the input contract and handle ValueError from invalid numeric conversion separately.',S('csv','csv.reader')))
add('with_resource_management',
 ('A with statement enters a context manager before the suite and invokes its exit operation when the suite finishes or raises.',Q('compound_stmts','the-with-statement')),
 ('Use with open(path, mode) as file: followed by an indented processing suite to close the file automatically on exit.',T('inputoutput','reading-and-writing-files')))
add('binary_files',
 ('Open files with "rb" for binary reading and "wb" for binary writing; these operations handle bytes rather than text strings.',T('inputoutput','reading-and-writing-files')),
 ('Read the payload from the binary source and pass those bytes directly to the binary destination\'s write method without decoding or encoding.',T('inputoutput','methods-of-file-objects')))
add('datetime_operations',
 ('datetime.strptime(text, format) parses a date-time string according to a supplied format; %Y-%m-%d specifies a four-digit year, month and day.',S('datetime','datetime.datetime.strptime')),
 ('Subtract compatible datetime values to obtain a timedelta representing their difference.',S('datetime','datetime-objects')),
 ('Use delta.days to obtain the day component of a timedelta; for parsed midnight calendar dates it represents their whole-day difference.',S('datetime','timedelta-objects')))
add('local_modules',
 ('A module is a file containing Python definitions and statements, with its module name normally derived from its .py filename.',T('modules','modules')),
 ('Put a helper definition in helper_module.py and use import helper_module followed by helper_module.helper(...) from a sibling script.',T('modules','modules')),
 ('A module has its own namespace; its executable top-level statements run on its first import in a session.',T('modules','more-on-modules')))
add('importable_packages',
 ('A regular package uses a directory containing __init__.py and its related module files.',T('modules','packages')),
 ('Import a helper module with import package.module and call package.module.helper(...) to use its qualified name.',T('modules','packages')),
 ('The __init__.py file can be empty or execute package initialization code.',T('modules','packages')))
add('logging',
 ('Use logger = logging.getLogger(__name__) after importing logging to obtain a module-named logger.',S('logging','module-logging')),
 ('Emit events with logger.debug, info, warning, error or critical according to their severity; events below the effective logging level are not processed.',S('logging','logging.Logger.setLevel')),
 ('Configure logging once for the application, for example with logging.basicConfig(level=logging.INFO), rather than adding a handler on each helper call.',S('logging','logging.basicConfig')),
 ('Attaching handlers to both a logger and its ancestors can emit the same event multiple times because propagation is enabled by default.',S('logging','logging.Logger.propagate')))
add('main_entry_point',
 ('A module executed as the top-level program has __name__ equal to "__main__", while an imported module has its module name.',T('modules','executing-modules-as-scripts')),
 ('Place command-interface invocation under if __name__ == "__main__": so imports define the helper without running that invocation.',T('modules','executing-modules-as-scripts')))
add('argparse_command_line',
 ('Create argparse.ArgumentParser(), register arguments with add_argument and call parse_args() to obtain an object holding parsed values.',S('argparse','module-argparse')),
 ('add_argument("input_path") declares a positional argument that is required by default, while add_argument("--verbose", action="store_true") declares an optional boolean flag.',S('argparse','argparse.ArgumentParser.add_argument')),
 ('Use args.input_path and args.verbose from the parsed object to drive the script\'s processing and verbosity.',S('argparse','module-argparse')),
 ('parse_args reports invalid invocations such as missing required arguments and exits with status 2 by default.',S('argparse','invalid-arguments')))
add('module_search_paths',
 ('Python resolves imports using its module search path; the script directory or current directory can precede installed standard-library modules.',T('modules','the-module-search-path')),
 ('Inspect sys.path to see search locations and module.__file__ to see the file used for a file-backed imported module.',S('sys','sys.path')),
 ('Rename a local file that shadows a standard-library module and retry in a fresh interpreter so an earlier cached import does not conceal the correction.',T('modules','the-module-search-path')))
add('os_environment',
 ('os.environ is a mapping of the process\'s environment variables to string values.',S('os','os.environ')),
 ('Use os.environ.get("SETTING", fallback) to retrieve a nonsecret configuration value with a fallback when absent.',S('os','os.getenv')),
 ('For a required setting, retrieve it without a fallback and explicitly reject None rather than silently continuing with a missing value.',S('os','os.getenv')))
add('random_vs_secrets',
 ('random generates pseudo-random values for modeling and simulation, not security-sensitive purposes.',S('random','module-random')),
 ('Initialize random.Random(seed) and use its methods for a repeatable simulation sequence with the same seed and compatible generator behavior, without concurrent threads changing its state.',S('random','notes-on-reproducibility')),
 ('Use secrets.token_hex(nbytes) or secrets.token_urlsafe(nbytes) for security-sensitive tokens rather than random.',S('secrets','generating-tokens')))
add('regular_expressions',
 ('Square brackets specify a character class, ranges such as [a-z] specify allowed characters, and * permits zero or more repetitions while + requires one or more.',S('re','regular-expression-syntax')),
 ('Use re.fullmatch(pattern, text) to require the entire text to match; it returns a match object on success and None otherwise.',S('re','re.fullmatch')),
 ('Construct an identifier-like pattern from a character class for allowed initial characters followed by a character class for allowed remaining characters repeated with *; use a raw string for the pattern.',S('re','regular-expression-syntax')))
add('sys_runtime_interface',
 ('sys.executable normally gives the absolute path of the running interpreter executable, but can be empty or None if Python cannot retrieve it.',S('sys','sys.executable')),
 ('sys.version is a string containing the Python version and additional build information.',S('sys','sys.version')),
 ('Import sys and print labeled sys.executable and sys.version values to identify the actual running runtime.',S('sys','sys.executable')))
add('virtual_environments',
 ('A virtual environment provides its own interpreter entry points and, by default, packages isolated from other environments.',S('venv','module-venv')),
 ('Create an environment with python -m venv .venv using the selected base interpreter.',S('venv','creating-virtual-environments')),
 ('Use .venv/bin/python on POSIX or .venv\\Scripts\\python.exe on Windows, or activate the environment to put its executables on PATH.',S('venv','how-venvs-work')),
 ('Verify the running executable with sys.executable and inspect installed packages with the environment interpreter\'s -m pip list command.',T('venv','managing-packages-with-pip')))
add('environment_interpreter_selection',
 ('An environment\'s Python executable can be invoked directly without activation; activation changes PATH to select it for shell commands.',S('venv','how-venvs-work')),
 ('Inspect sys.executable in the running program to verify which interpreter a terminal or editor actually selected.',S('sys','sys.executable')),
 ('When an editor runs the wrong interpreter, select the intended environment\'s executable in its run configuration and rerun the diagnostic.',S('venv','how-venvs-work')))
add('pip_installation',
 ('Use the intended interpreter with python -m pip install PackageName to install into that interpreter\'s environment.', 'python_packaging_user_guide#installing-from-pypi'),
 ('Use python -m pip show PackageName or python -m pip list with the same interpreter to inspect the installed package.',T('venv','managing-packages-with-pip')),
 ('Verify the documented import with that environment\'s interpreter; an installed distribution name and its import name need not be identical.', 'python_packaging_user_guide#installing-packages'))
add('requirements_files',
 ('A requirements file lists packages to install; PackageName==version pins a specific version.', 'python_packaging_user_guide#installing-from-pypi'),
 ('Use the target environment\'s python -m pip install -r requirements.txt to install the listed requirements.', 'python_packaging_user_guide#requirements-files'),
 ('Use the same environment\'s python -m pip list and documented imports to check that the recreated environment has the intended dependencies.',T('venv','managing-packages-with-pip')))
add('assert_statement',
 ('assert condition raises AssertionError if the condition is false; assert condition, message supplies an explanatory value.',Q('simple_stmts','the-assert-statement')),
 ('Use assert for an internal invariant that should hold during development, not for required public-input validation.',Q('simple_stmts','the-assert-statement')),
 ('Assertions may be omitted when Python is run with optimization, so enforce required input checks with explicit conditionals and exceptions.',Q('simple_stmts','the-assert-statement')))
add('iterables_and_iterators',
 ('An iterable can supply an iterator through iter(iterable); an iterator maintains traversal state and next(iterator) returns its next item.',S('stdtypes','iterator-types')),
 ('next(iterator) raises StopIteration after the items are exhausted unless a default is supplied.',S('functions','next')),
 ('Two calls to iter(a_list) create independent traversal states, while iter(an_iterator) returns the iterator itself.',S('stdtypes','iterator-types')),
 ('Store two list iterators in separate names and call next on each to advance their positions independently.',S('functions','iter')))
add('generator_functions',
 ('A function containing yield produces a generator iterator when called rather than running its body to completion immediately.',T('classes','generators')),
 ('yield value suspends the function and retains local state, resuming after that yield when the next item is requested.',T('classes','generators')),
 ('To yield valid records lazily, loop over the input and yield each record inside the required validity condition.',T('classes','generators')),
 ('Returning or reaching the end of the generator function ends iteration.',T('classes','generators')))
add('generator_expressions',
 ('A generator expression uses (expression for item in iterable if condition) to transform and optionally filter items lazily.',T('classes','generator-expressions')),
 ('Pass a generator expression to sum, as in sum(transform(item) for item in records if condition(item)), to accumulate values without creating an intermediate list.',T('classes','generator-expressions')))
add('iterator_consumption_and_exhaustion',
 ('Each next call consumes one iterator item, so later traversal continues from its current position rather than restarting.',S('stdtypes','iterator-types')),
 ('An exhausted iterator must continue to raise StopIteration on later requests.',S('stdtypes','iterator-types')),
 ('To repeat traversal, obtain a new iterator from a reusable iterable or retain items in a collection before consuming the iterator.',S('functions','iter')))
add('eager_vs_lazy_processing',
 ('A list comprehension constructs a list eagerly, whereas a generator expression supplies values during iteration.',T('classes','generator-expressions')),
 ('Prefer a generator expression for a one-pass aggregation when retaining an intermediate list is unnecessary.',T('classes','generator-expressions')),
 ('Materialize with list(iterable) when retained values are needed for repeated traversal, accepting the memory cost of storing them.',S('stdtypes','lists')))
add('itertools_utilities',
 ('itertools.chain(*iterables) yields all elements from the first input, then the next inputs in sequence, without constructing a concatenated list.',S('itertools','itertools.chain')),
 ('Import chain from itertools and traverse chain(first, second), or pass it to the aggregation, to combine sources in one lazy traversal.',S('itertools','itertools.chain')))
add('map_and_filter',
 ('map(function, iterable) returns an iterator applying the function to each item.',S('functions','map')),
 ('filter(function, iterable) returns an iterator of items whose predicate result tests true; filter(None, iterable) keeps truthy items.',S('functions','filter')),
 ('Use [transform(item) for item in iterable if predicate(item)] for a readable eager transformation and filtering operation, or parentheses for a lazy generator expression.',T('datastructures','list-comprehensions')),
 ('Passing an existing callable to map or filter avoids a wrapper expression; a comprehension can state the equivalent transformation and condition together.',T('datastructures','list-comprehensions')))
add('unittest_test_cases',
 ('Define a subclass of unittest.TestCase with methods whose names begin with test to express individual checks.',S('unittest','basic-example')),
 ('Use self.assertEqual(actual, expected) for equality checks and self.assertTrue(condition) for truth checks.',S('unittest','basic-example')),
 ('Use with self.assertRaises(ExceptionType): around the tested call to check that supplied invalid input raises the expected exception.',S('unittest','unittest.TestCase.assertRaises')))
add('unittest_execution_and_results',
 ('Run python -m unittest test_module for a named module or python -m unittest discover to find tests.',S('unittest','command-line-interface')),
 ('Discovery looks for test*.py by default and loads matching test cases; inspect the reported test count so zero discovered tests is not mistaken for executed checks.',S('unittest','test-discovery')),
 ('A failure is a failed assertion, whereas an error is an unexpected exception from a test.',S('unittest','unittest.TestResult.errors')),
 ('Read the FAIL or ERROR entry, traceback and final counts to locate a failing test and distinguish it from successful checks.',S('unittest','basic-example')))
add('unittest_setup_and_teardown',
 ('setUp runs before each test method, so create fresh mutable fixture state there instead of sharing state between tests.',S('unittest','unittest.TestCase.setUp')),
 ('Register resource release with self.addCleanup(function, *args, **kwargs); cleanup functions run in reverse registration order.',S('unittest','unittest.TestCase.addCleanup')),
 ('tearDown runs after a test when setUp succeeded, while registered cleanups still run if setUp fails.',S('unittest','unittest.TestCase.addCleanup')))
add('read_generated_code',
 ('Read the implementation line by line and check that it matches the intended behavior rather than assuming its apparent plausibility establishes correctness.', 'think_python#chap12.html#debugging'),
 ('Trace the values and branches for a supplied valid and invalid input, comparing the observed return or exception with the stated requirement.', 'think_python#chap12.html#debugging'),
 ('Test code obtained from a virtual assistant instead of relying on the response alone.', 'think_python#chap18.html#exercises'))
add('review_generated_file_operations',
 ('Opening an existing file with "w" truncates it, so inspect write modes before executing code that must preserve existing contents.',S('functions','open')),
 ('Path.unlink removes a file or symbolic link and Path.rmdir removes an empty directory, so inspect deletion calls and their targets before running a cleanup helper.',S('pathlib','pathlib.Path.unlink')),
 ('Relative paths depend on the current working directory; inspect the resolved target to identify unintended filesystem locations.',S('pathlib','pathlib.Path.resolve')),
 ('Remove an unintended deletion call rather than executing it to discover its effect.',S('pathlib','pathlib.Path.unlink')))
add('review_untrusted_input_and_execution',
 ('eval evaluates Python expressions and exec executes Python code; passing user-supplied input to either can execute arbitrary code.',S('functions','eval')),
 ('For numeric input, use explicit conversion such as int(text) and handle ValueError rather than evaluating the text as Python code.',S('functions','int')),
 ('When explicitly invoking a shell, shell metacharacters and whitespace in untrusted input must be accounted for to avoid shell injection; prefer an argument sequence without shell=True.',S('subprocess','security-considerations')))
add('verify_generated_api_claims',
 ('Check the claimed API in its official reference entry, including the documented parameter signature and return-value description.',S('functions','help')),
 ('Compare the generated call with that entry\'s positional and keyword argument rules, defaults and supported inputs rather than inferring them from its name.',S('functions','help')),
 ('Use help(object) to inspect available documentation, then test the documented behavior with the interpreter version used by the project.',S('functions','help')))
add('review_generated_dependencies',
 ('Distinguish a distribution package installed by pip from the import package used in Python; the names can differ.', 'python_packaging_user_guide#installing-packages'),
 ('Before installation, compare the suggested distribution name and version with the project\'s documented dependency requirement and package source rather than treating a plausible name as sufficient.', 'python_packaging_user_guide#installing-from-pypi'),
 ('pip can install from PyPI, other indexes or specified sources, so check which source the proposed installation command actually uses.', 'python_packaging_user_guide#installing-from-other-indexes'),
 ('Decline to install a suggested package whose identity or required use cannot be established from those checks.', 'python_packaging_user_guide#installing-packages'))
add('accept_repair_or_reject_generated_code',
 ('Treat generated code as an implementation to read and test against the intended behavior, not as established correctness.', 'think_python#chap18.html#exercises'),
 ('For acceptance, cite the supplied checks of required behavior and the resolved safety findings rather than relying on how plausible the implementation looks.', 'think_python#chap18.html#debugging'),
 ('Choose repair for an identified correctable defect, then rerun the relevant checks before reconsidering acceptance.', 'think_python#chap12.html#debugging'),
 ('For rejection, identify the unresolved failed requirement or unsafe operation and record that finding as the reason, rather than claiming the implementation is correct.',S('functions','eval')))
# Complementary source sections for claims with more than one documented component.
def cite(name,index,*refs):
 data['python.'+name][index-1]['source_refs'].extend(refs)
PACK_NAMES='python_packaging_user_guide#discussions/distribution-package-vs-import-package/#what-are-the-links-between-distribution-packages-and-import-packages'
data['python.pip_installation'][2]['source_refs'].append(PACK_NAMES)
data['python.review_generated_dependencies'][0]['source_refs'].append(PACK_NAMES)
data['python.review_generated_dependencies'][1]['source_refs'].append(PACK_NAMES)
data['python.review_generated_dependencies'][3]['statement']='Do not install a distribution merely because its name matches a generated import: indexes do not enforce that relationship, and a blind installation can select an unintended or malicious package. Confirm its documented identity and intended use first.'
data['python.review_generated_dependencies'][3]['source_refs']=[PACK_NAMES]
data['python.docstrings'][1]['source_refs'].append('pep8_style_guide#documentation-strings -> linked PEP 257#multi-line-docstrings')
cite('collection_selection',1,S('stdtypes','common-sequence-operations'))
cite('collection_selection',2,S('stdtypes','common-sequence-operations'))
cite('collection_selection',4,S('stdtypes','dict'))
cite('collection_selection',5,S('stdtypes','dict'))
cite('console_input_output',3,S('functions','input'))
cite('nested_collections',1,Q('expressions','subscriptions'))
cite('nested_collections',2,Q('expressions','subscriptions'))
cite('nested_loops',2,T('controlflow','for-statements'))
cite('statements_and_expressions',3,Q('expressions','operator-precedence'))
cite('interpreter_execution_model',3,T('errors','exceptions'))
cite('interactive_execution',3,Q('simple_stmts','assignment-statements'),T('interpreter','invoking-the-interpreter'))
cite('none_and_identity',2,Q('expressions','identity-comparisons'))
data['python.none_and_identity'].append({'id':'f4','statement':'Use mapping.get(key) for an optional lookup; it returns None for a missing key when no other default is supplied, then test the result with is None to preserve a legitimate zero.','source_refs':[S('stdtypes','dict.get'),Q('expressions','identity-comparisons')]})
cite('unicode_and_bytes',1,S('stdtypes','binary-sequence-types-bytes-bytearray-memoryview'))
cite('unicode_and_bytes',2,S('stdtypes','bytes.decode'))
cite('aliasing_mutability_and_copying',2,S('stdtypes','common-sequence-operations'))
data['python.diagnostic_printing'][1]['source_refs']=[T('inputoutput','fancier-output-formatting')]
cite('exception_hierarchy',1,S('exceptions','Exception'))
cite('closures_and_enclosing_scope',1,Q('datamodel','function.__closure__'))
cite('closures_and_enclosing_scope',3,Q('simple_stmts','the-nonlocal-statement'))
cite('specific_exception_handlers',2,T('errors','handling-exceptions'))
cite('variadic_arguments_and_unpacking',1,T('controlflow','keyword-arguments'))
cite('class_and_static_methods',1,S('functions','staticmethod'))
cite('class_and_static_methods',2,S('functions','staticmethod'))
cite('composition',1,T('classes','instance-objects'))
cite('inheritance_and_super',3,Q('datamodel','object.__init__'))
cite('json_serialization',1,S('json','json.dumps'),S('json','json.loads'))
cite('json_serialization',3,S('json','json.JSONDecoder'))
cite('json_serialization',4,S('json','json.dump'))
cite('object_introspection',4,T('classes','private-variables'),S('functions','dir'))
cite('file_and_format_errors',3,S('csv','csv.csvreader.line_num'),S('csv','examples'))
cite('file_and_format_errors',4,S('functions','int'),S('exceptions','ValueError'))
cite('datetime_operations',1,S('datetime','strftime-and-strptime-format-codes'))
cite('datetime_operations',3,S('datetime','datetime.timedelta.days'))
cite('module_search_paths',2,Q('datamodel','module.__file__'))
cite('module_search_paths',3,T('modules','more-on-modules'))
cite('os_environment',2,S('stdtypes','dict.get'))
cite('os_environment',3,S('stdtypes','dict.get'))
cite('random_vs_secrets',2,S('random','random.Random'))
cite('regular_expressions',3,S('re','module-re'))
cite('virtual_environments',4,S('sys','sys.executable'))
cite('iterables_and_iterators',3,T('classes','iterators'))
cite('generator_functions',1,S('stdtypes','generator-types'))
cite('generator_functions',4,S('stdtypes','generator-types'))
cite('map_and_filter',3,T('classes','generator-expressions'))
cite('map_and_filter',4,S('functions','filter'),S('functions','map'))
cite('unittest_execution_and_results',3,S('unittest','unittest.TestResult.failures'))
cite('review_generated_file_operations',2,S('pathlib','pathlib.Path.rmdir'))
cite('review_untrusted_input_and_execution',1,S('functions','exec'))
cite('review_untrusted_input_and_execution',2,S('exceptions','ValueError'))
cite('accept_repair_or_reject_generated_code',2,S('functions','eval'))
cite('accept_repair_or_reject_generated_code',4,'think_python#chap12.html#debugging')

# Build file, with exact registry evidence reuse and owner-first evidence identity.
briefs=[];owners={};placeholders=[]
for c in sorted(E['concepts'],key=lambda c:(c['path_id'],c['toc_sequence_position'])):
 cid=c['concept_id'];pid=c['path_id'];status=lookup[(cid,pid)]['canonical_status']
 if status=='reuse_registry':ev=copy.deepcopy(registry[cid].get('evidence',registry[cid]))
 elif status=='shared_in_batch':ev=copy.deepcopy(owners[cid])
 else:
  ev={'concept_id':cid,'required_facts':data[cid],'optional_enrichment':[],'misconceptions':[],'created_in_batch_id':E['batch_id'],'used_by_path_ids':sorted({x['path_id'] for x in E['concepts'] if x['concept_id']==cid})};owners[cid]=ev
 primary=c['primary_objective']
 if 'small analysis task' in primary or 'Given a simple example, correctly identify or apply' in c['assessment_target']:placeholders.append(cid)
 objective='Be able to '+primary[0].lower()+primary[1:]
 briefs.append({'concept_id':cid,'path_id':pid,'learning_objective':objective,'canonical_status':status,'evidence':ev})
inputs=['extracted_concepts.json','registry_lookup.json','concept_evidence_registry_snapshot.json','source_pack_manifest.json']
parents={n:hashlib.sha256((P/n).read_bytes()).hexdigest() for n in inputs}
pack='00_GLOSSARY_PIPELINE_CORE/source_packs/learn_python.source_pack.json';parents[pack]=hashlib.sha256(Path(pack).read_bytes()).hexdigest()
meta={'artifact_type':'coverage_briefs','artifact_version':'1.0.0','schema_version':'1.0.0','batch_id':E['batch_id'],'run_id':E['metadata']['run_id'],'prompt_version':'03_coverage_brief@v1','model':'none','generated_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_snapshot_id':E['metadata']['source_snapshot_id'],'parent_artifact_hashes':parents}
out={'metadata':meta,'batch_id':E['batch_id'],'briefs':briefs}
(P/'coverage_briefs.part.all.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
print('briefs',len(briefs),'facts',sum(len(b['evidence']['required_facts']) for b in briefs),'placeholders',placeholders)
