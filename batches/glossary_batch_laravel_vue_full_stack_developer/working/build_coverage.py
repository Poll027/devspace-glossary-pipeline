import json,hashlib,datetime,copy
from pathlib import Path
B=Path('batches/glossary_batch_laravel_vue_full_stack_developer')
C=json.loads((B/'extracted_concepts.json').read_text())['concepts']; data={}
# Linked prerequisite references are explicit locators under the source that links to them.
JS='vue_docs#introduction/what-is-vue -> linked MDN JavaScript Guide/Language_overview/'
HTML='vue_docs#introduction/what-is-vue -> linked MDN Learn_web_development/Core/Structuring_content/'
CSS='vue_docs#introduction/what-is-vue -> linked MDN Learn_web_development/Core/Styling_basics/'
FETCH=JS+'linked Web/API/Fetch_API/Using_Fetch/'
NPM='vite_docs#getting-started -> linked npm documentation/cli/v11/'
def add(i,ref,*facts):
 assert i not in data,i
 data[i]=[(ref,f) if isinstance(f,str) else f for f in facts]
def L(page,section):return 'laravel_docs#'+page+'/'+section
def V(page,section):return 'vue_docs#'+page+'/'+section
def P(page,section=''):return 'php_manual#'+page+('/'+section if section else '')
add(0,L('controllers','actions-handled-by-resource-controllers'),
 'A CRUD resource interface distinguishes listing a collection, creating a resource, reading one resource, updating one resource and deleting one resource.',
 'For the documented photos resource, GET /photos lists resources and POST /photos creates a resource.',
 'For the documented photos resource, GET /photos/{photo} reads one resource, PUT/PATCH /photos/{photo} updates it and DELETE /photos/{photo} deletes it.',
 'Specify collection and identified-resource URLs with these method-to-operation mappings to make the requested CRUD operation unambiguous.')
add(1,'composer_docs#01-basic-usage.md/installing-from-composerlock',
 'composer.json declares dependencies and version constraints, while composer.lock records resolved exact versions.',
 'Run composer install in a project with composer.lock to restore dependencies using the locked versions in vendor.',
 ('composer_docs#01-basic-usage.md/updating-dependencies-to-their-latest-versions','composer update resolves versions satisfying the manifest constraints and updates composer.lock rather than merely restoring its existing versions.'))
add(2,JS+'objects',
 'An object literal uses braces and property-to-value pairs, and object properties can contain other objects.',
 'Read or assign a property with object.name or object[key]; bracket notation permits a key chosen by a variable.',
 (JS+'data_types','JavaScript null represents a deliberate non-value, while undefined represents an unassigned value.'),
 (JS+'variables','let permits reassignment, whereas const prevents reassignment of its binding but does not prevent changes to an object property.'))
add(3,NPM+'commands/npm-ci/description',
 'npm ci restores a whole project from an existing package-lock.json or npm-shrinkwrap.json without writing the manifest or lockfile.',
 'npm ci fails when the manifest dependencies disagree with the lockfile and removes an existing node_modules before installing.',
 (NPM+'commands/npm-install/description','Run npm install -D package-name to add the chosen package as a development dependency and update the dependency files.'),
 'After committing the changed dependency files, use npm ci to verify that a clean installation can restore the locked project.')
add(4,P('language.variables.basics.php'),
 'A PHP variable is written with a dollar sign and its name, and $name = value assigns a value to it.',
 (P('language.types.intro.php'),'PHP determines a value’s type at runtime; application values include integers, floating-point numbers, strings and booleans.'),
 (P('language.types.null.php'),'The null type has one value, null, which can be assigned to represent a missing application value.'),
 (P('function.var-dump.php'),'Use var_dump($value) to inspect a value together with its type.'))
add(5,'laravel_sanctum#how-it-works-spa-authentication',
 'Sanctum SPA authentication uses Laravel cookie-based sessions rather than API tokens for a first-party SPA.',
 ('laravel_sanctum#how-it-works-api-tokens','Sanctum API tokens authenticate clients through a bearer token in the Authorization header.'),
 ('laravel_sanctum#spa-authentication','Choose cookie session authentication for a first-party SPA sharing the same top-level domain with its API, and API tokens for a mobile or third-party client.'))
add(6,HTML+'Basic_HTML_syntax/anatomy_of_an_html_element',
 'An ordinary HTML element consists of an opening tag, content and a matching closing tag, such as <p>text</p>.',
 (HTML+'Basic_HTML_syntax/attributes','Write attributes inside the opening tag as name="value", separated by spaces; they supply information about the element.'),
 (HTML+'Basic_HTML_syntax/nesting_elements','Nested elements must close in the reverse order in which they open, rather than overlapping their tags.'),
 (HTML+'Basic_HTML_syntax/void_elements','Void elements such as <img> do not wrap content in a closing tag.'))
add(7,JS+'control_structures',
 'Write conditional alternatives as if (predicate) { ... } else if (otherPredicate) { ... } else { ... }.',
 'A matching if branch executes its body instead of its else alternative, allowing an ordered chain of status decisions.',
 (JS+'operators','Use === to compare without converting unlike types, and combine boolean predicates with &&, || and !.'))
add(8,JS+'functions',
 'A function declares parameters and a body, is invoked with arguments, and returns a result with return.',
 (JS+'inner_functions','A nested function can access variables in its enclosing function’s scope while its own local variables remain inside its scope.'),
 (JS+'functions_are_first-class_objects','Functions are values that can be passed as arguments or returned by another function.'),
 (JS+'inner_functions','Define callback helpers inside an enclosing function to let them use its local state without creating global variables.'))
add(9,L('artisan','introduction'),
 'Artisan is Laravel’s project command-line interface; run php artisan list from the project to discover available commands.',
 'Use php artisan help command-name to inspect a command’s arguments and options before invoking it.',
 (L('controllers','basic-controllers'),'php artisan make:controller ControllerName generates a controller artifact.'))
add(10,P('language.types.array.php','Syntax'),
 'A PHP array is an ordered map from keys to values and may contain arrays as its values.',
 'Create keyed data with [key => value] and a list with [value1, value2].',
 (P('language.types.array.php','Accessing array elements with square bracket syntax'),'Use $array[$key] to read a keyed value, including chained bracket access for nested record data.'),
 (P('language.types.array.php','Creating/modifying with square bracket syntax'),'Use $result[$key] = $value to insert or replace a keyed result and $array[] = $value to append a value.'))
add(11,P('language.operators.comparison.php'),
 '=== is true when operands have equal values and equal types, and !== is true when either their values or types differ.',
 '== and != compare after type juggling, unlike the strict comparison operators.',
 'Use <, >, <= and >= to express numeric eligibility boundaries.',
 (P('language.operators.logical.php'),'For boolean predicates, && requires both conditions, || requires at least one, and ! negates a condition; parentheses make the intended grouping explicit.'))
add(12,CSS+'Basic_selectors/class_selectors',
 'A class selector begins with a dot, is case-sensitive, and matches elements that have the named class.',
 (CSS+'Getting_started/adding_a_class','Write a rule as .className { property: value; } and put class="className" on the elements to receive those declarations.'),
 (CSS+'Getting_started/adding_css_to_our_document','Attach an external stylesheet with <link rel="stylesheet" href="styles.css"> and save and refresh the page to check the resulting styling.'))
add(13,HTML+'HTML_forms/making_forms_accessible',
 'Associate a label’s for attribute with the id of its native form control so the control has an accessible label.',
 (HTML+'HTML_forms/the_form_element','A form groups controls for submission, and its action and method determine the destination and submission method.'),
 (HTML+'HTML_forms/the_name_and_value_attributes','A control’s name identifies its submitted value; id serves label association rather than naming the submitted field.'),
 (HTML+'HTML_forms/button_types','Use a submit button to submit the form and type="button" for a button that should not submit it.'))
add(14,JS+'arrays',
 'JavaScript arrays are ordered collections with zero-based index access and a length property.',
 (JS+'linked Reference/Global_Objects/Array/map/description','array.map(callback) builds a new array from each callback result, allowing a derived record list without replacing the source array.'),
 (JS+'linked Reference/Global_Objects/Array/filter/description','array.filter(predicate) builds a new array containing the elements for which the predicate is truthy.'),
 (JS+'linked Reference/Global_Objects/Array/map/description','A new mapped array does not prevent the callback from mutating an object it receives; avoid such writes when the source records must remain unchanged.'))
add(15,JS+'asynchronous_programming',
 'A promise exposes eventual completion rather than an immediately available result; .then handles fulfillment and .catch handles rejection.',
 'Inside an async function, await defers subsequent dependent statements until the awaited operation completes.',
 (FETCH+'handling_the_response','An awaited rejected operation can be caught by try { ... } catch (error) { ... }; leaving it uncaught propagates failure to the caller.'),
 'Return or await the dependent asynchronous work so the caller’s completion tracks that work rather than starting it without waiting.')
add(16,'vite_docs#getting-started -> linked MDN Web/JavaScript/Guide/Modules/exporting_module_features',
 'Export a reusable module binding with export before its declaration, or list exported bindings in export { name }.',
 ('vite_docs#getting-started -> linked MDN Web/JavaScript/Guide/Modules/importing_features_into_your_script','Import a named binding with import { name } from "./module.js"; the path identifies the module and the name must be exported by it.'),
 ('vite_docs#getting-started -> linked MDN Web/JavaScript/Guide/Modules/default_exports_versus_named_exports','A default export is imported without braces and can be assigned a local name, unlike a named import.'))
add(17,'laravel_testing#running-tests',
 'Run ./vendor/bin/phpunit or php artisan test to execute the configured Laravel test suite and inspect the runner’s test results.',
 ('laravel_testing#environment','The phpunit.xml environment settings select the testing configuration and can be edited to correct a testing-environment mismatch.'),
 ('laravel_testing#environment','Run php artisan config:clear before tests when stale cached configuration would prevent the test environment settings from taking effect.'))
add(18,L('configuration','environment-configuration'),
 'Laravel’s config files read environment-specific settings, and external environment variables can override values from .env.',
 'Use placeholder values in .env.example rather than committing real credentials to source control.',
 (L('database','configuration'),'Configure the database connection in config/database.php using the connection, host, port, database and credential settings for the target environment.'),
 (L('deployment','debug-mode'),'Set APP_DEBUG=false in production to avoid exposing sensitive configuration details in public error output.'))
add(19,P('control-structures.if.php'),
 'PHP if (condition) { ... } executes its body when the condition evaluates to true.',
 (P('control-structures.elseif.php'),'Chain elseif (condition) alternatives to execute the first true branch when earlier branches did not match.'),
 (P('control-structures.else.php'),'An else body handles the case where the preceding conditional alternatives do not execute.'))
add(20,P('language.types.declarations.php'),
 'Write typed parameters and returns as function name(int $input): int { return $result; }, using types that match the intended function contract.',
 'PHP type declarations constrain parameter and return values, and ?T permits either a value of type T or null.',
 'Scalar types can be coerced by default; declare(strict_types=1) enables strict scalar typing for calls made from that file, with int accepted for a float declaration.',
 (P('functions.returning-values.php'),'return passes the result to the caller and ends the function; a function without a return value returns null.'))
add(21,L('scheduling','defining-schedules'),
 'Declare tasks in routes/console.php through the Schedule facade, using Schedule::call(callback) for a callable task.',
 'Chain a frequency method such as ->daily() onto the task declaration to describe its due times.',
 (L('scheduling','schedule-frequency-options'),'->everyMinute() schedules a task every minute, while ->daily() schedules it daily at midnight.'),
 'Run php artisan schedule:list to inspect the scheduled tasks and their next due times.')
add(22,L('logging','configuration'),
 'Set logging channels and options in config/logging.php; the default stack channel combines configured channels.',
 (L('logging','log-levels'),'A channel’s level sets the minimum severity of messages it records, allowing production logging to retain the relevant failures.'),
 (L('deployment','debug-mode'),'Keep APP_DEBUG=false in production so public error pages do not expose sensitive configuration.'),
 (V('best-practices/security','backend-coordination'),'Treat protection of sensitive server-side data as a backend responsibility rather than relying on frontend hiding.'))
add(23,P('language.oop5.basic.php','class'),
 'A PHP class declares properties holding state and methods implementing behavior, and new ClassName(...) creates an instance.',
 (P('language.oop5.decon.php','construct'),'A __construct(...) method runs when an object is created and can initialize its properties from the supplied arguments.'),
 (P('language.oop5.basic.php','class'),'Inside an instance method, $this identifies the current object and $this->property accesses its state.'),
 (P('language.oop5.basic.php','new'),'Use $object->method(...) to invoke instance behavior on the created object.'))
add(24,P('control-structures.foreach.php'),
 'foreach ($array as $value) traverses values, while foreach ($array as $key => $value) supplies both keys and values.',
 'The loop body runs for each traversed element, so initialize an accumulator before the loop and update it in the body to obtain a summary.',
 'The ordinary foreach value form assigns the current value to the loop variable rather than making it a reference to the original element.')
add(25,'vitest_docs#guide/',
 'Run npx vitest in the supplied project to discover and execute its tests, or npx vitest run for a single run.',
 ('vitest_docs#guide/environment','Vitest uses node as its default environment; component DOM tests need a browser-like environment such as jsdom or happy-dom.'),
 ('vue_docs#scaling-up/testing/adding-vitest-to-a-project','Configure Vitest’s test.environment as jsdom in the project configuration for the documented Vue component-testing setup.'),
 ('vitest_docs#guide/','The runner reports passing and failing tests; use the reported failing file and assertion to identify the configuration or behavior under test.'))
add(26,V('introduction','single-file-components'),
 'A Vue single-file component is a .vue file combining component JavaScript, an HTML-like template and optional CSS.',
 (V('essentials/reactivity-fundamentals','script-setup'),'Declare component bindings in <script setup>; its top-level bindings are available to the component template.'),
 'Use <template> for the component’s markup and <style> for its CSS, keeping each block in its own role.')
add(27,FETCH+'making_a_request',
 'Call fetch(url, options) in a shared function and return its asynchronous result so callers can reuse one request interface.',
 (FETCH+'setting_the_method','fetch uses GET by default; set options.method for POST, PUT, PATCH or DELETE operations.'),
 (FETCH+'setting_headers','For JSON data, set the Content-Type header to application/json and serialize the payload with JSON.stringify in options.body.'),
 (FETCH+'setting_a_body','Do not attach a request body to a GET request.'),
 (FETCH+'reading_the_response_body','Use await response.json() to parse a JSON response body before returning its data to a caller.'))
add(28,L('hashing','introduction'),
 'Laravel’s Hash facade supports Bcrypt and Argon2 for storing password hashes rather than plaintext passwords.',
 (L('hashing','hashing-passwords'),'Store the result of Hash::make($password) rather than the input password.'),
 (L('hashing','verifying-that-a-password-matches-a-hash'),'Hash::check($plainText, $storedHash) verifies whether a supplied plaintext password corresponds to the stored hash without needing to recover the original password.'))
add(29,L('lifecycle','first-steps'),
 'Laravel’s HTTP entrypoint creates the application and passes the incoming request into the application’s request-handling process.',
 (L('lifecycle','routing'),'Routing dispatches the request to its route or controller while applying the route’s assigned middleware.'),
 (L('lifecycle','routing'),'Only a request that passes the assigned middleware reaches the handler; the handler’s response returns through that middleware chain.'),
 (L('lifecycle','finishing-up'),'The final response is sent back to the browser, making the entrypoint, request checks, dispatch and response distinct places to locate a failed trace.'))
add(30,L('scheduling','running-the-scheduler'),
 'php artisan schedule:run evaluates scheduled tasks against the current server time and executes those that are due.',
 'For server operation, configure one cron entry to run schedule:run every minute from the project directory.',
 'The documented trigger is * * * * * cd /path-to-your-project && php artisan schedule:run >> /dev/null 2>&1.',
 (L('scheduling','defining-schedules'),'Use php artisan schedule:list to inspect the next due times, then observe schedule:run at a due time to distinguish the schedule declaration from its execution trigger.'))
add(31,L('migrations','migration-structure'),
 'Put schema changes in a migration’s up method and reverse those operations in its down method.',
 'Use Schema::create(tableName, callback) with Blueprint methods such as id() and string(columnName) to declare the resulting table and columns.',
 (L('migrations','foreign-key-constraints'),'A foreign key constraint enforces referential integrity; foreignId("user_id")->constrained() creates the documented posts-to-users reference.'),
 (L('migrations','running-migrations'),'Run php artisan migrate to apply outstanding migrations.'),
 (L('migrations','rolling-back-migrations'),'Run php artisan migrate:rollback to reverse the latest migration batch, which may include several migration files.'))
add(32,P('language.error-handling.throwable.php'),
 'throw interrupts ordinary execution and propagates a throwable through the call stack until a matching catch or the global scope is reached.',
 'Surround the operation with try { ... } catch (ExceptionType $error) { ... } to handle a matching service failure at the caller boundary.',
 'A catch handles a matching throwable type; if no matching catch is reached, an uncaught failure is passed to an exception handler or terminates the program.',
 'A finally block runs as control leaves its try/catch boundary, including during propagation.')
add(33,P('language.oop5.interfaces.php'),
 'An interface specifies public methods that an implementing class must provide with compatible signatures.',
 'Declare the contract with interface Name { public function method(...); } and use class Adapter implements Name to provide its behavior.',
 'Type a caller’s dependency with the interface so different conforming implementation classes can be substituted without changing that caller.')
add(34,P('language.namespaces.definition.php'),
 'A namespace declaration assigns names declared in that file to a namespace.',
 (P('language.namespaces.importing.php'),'use Full\\ClassName as Alias makes Alias resolve to that fully qualified class name within the importing file.'),
 (P('language.namespaces.importing.php'),'An unaliased use Full\\ClassName import makes ClassName available as the short name.'),
 (P('language.namespaces.importing.php'),'A fully qualified name beginning with a backslash is absolute and is not changed by use imports.'))
add(35,'vite_docs#getting-started/manual-installation',
 'Start the development server with npx vite, or npm run dev when the supplied package script runs vite.',
 ('vite_docs#getting-started/index-html-and-project-root','Vite uses index.html in the project root as a development entrypoint rather than treating it as a passive public file.'),
 ('vite_docs#features/hot-module-replacement','Vite’s hot module replacement updates edited modules during development without requiring a full page reload.'),
 'The documented development URL is http://localhost:5173; use the URL actually printed by the running project to check an edit.')
add(36,V('essentials/lifecycle','registering-lifecycle-hooks'),
 'onMounted registers work that runs after the component’s initial rendering and DOM creation.',
 (V('reusability/composables','mouse-tracker-example'),'Pair a listener registered at mount with removal of the same listener in onUnmounted to stop the side effect when the component goes away.'),
 'Register lifecycle hooks synchronously during setup so Vue associates them with the active component instance.')
add(37,V('essentials/reactivity-fundamentals','ref'),
 'import { ref } from "vue" and ref(initialValue) create a reactive value whose script access and updates use .value.',
 'A top-level ref exposed to a template is unwrapped there, so template access does not normally require .value.',
 (V('essentials/reactivity-fundamentals','reactive'),'reactive(object) returns a reactive proxy whose property reads and writes are tracked.'),
 (V('essentials/reactivity-fundamentals','limitations-of-reactive'),'reactive only accepts object types; destructuring a primitive property disconnects that local value, and replacing the reactive object breaks the original connection.'))
add(38,'vue_router_docs#guide/Creating-the-router-instance',
 'Configure routes as path-to-component records passed to createRouter({ history, routes }); RouterView renders the matched component.',
 ('vue_router_docs#guide/Registering-the-router-plugin','Register the router with app.use(router) before mounting the application.'),
 ('vue_router_docs#guide/The-RouterLink-component','Use <RouterLink to="/path"> to navigate without reloading the whole page.'),
 ('vue_router_docs#guide/essentials/navigation','router.push(destination) performs programmatic navigation to a route destination.'))
add(39,FETCH+'handling_the_response',
 'fetch rejects for some transport failures but fulfills with a Response for HTTP errors such as 404.',
 'Check response.ok or response.status before treating the response body as a successful result; ok indicates a 200–299 status.',
 'Use try/catch around awaited fetch and body-reading work to handle rejected network or parsing operations separately from a received non-success HTTP status.',
 'For an expected 422 JSON response, inspect the status and parse its body for the caller rather than classifying it as a rejected network request.')
add(40,'composer_docs#04-schema.md/psr-4',
 'Declare an autoload.psr-4 mapping in composer.json from a namespace prefix ending in a backslash to a project-relative directory.',
 'For the documented Foo\\ prefix mapped to src/, Foo\\Bar\\Baz resolves to src/Bar/Baz.php rather than src/Foo/Bar/Baz.php.',
 ('composer_docs#01-basic-usage.md/autoloading','Run composer dump-autoload after changing the autoload configuration and include vendor/autoload.php to use the generated autoloader.'))
add(41,'laravel_eloquent#mass-assignment',
 'Eloquent models are protected from mass assignment by default; declare protected $fillable = [allowedAttributeNames] to permit only the chosen attributes in create or fill.',
 'Model::create($attributes) inserts and returns a model, while $model->fill($attributes) applies mass-assignable input to an existing instance.',
 ('laravel_eloquent#updates','Use $model->save() to persist changes to an existing model.'),
 ('laravel_eloquent#retrieving-single-models','Model::find($id) retrieves a model by its primary key.'),
 ('laravel_eloquent#deleting-models','Call $model->delete() to remove the model’s stored record.'),
 'Keep protected fields out of $fillable rather than allowing an unexpected submitted field to change them through mass assignment.')
add(42,L('routing','available-router-methods'),
 'Declare method-specific routes with Route::get, Route::post, Route::put, Route::patch or Route::delete and supply a path and handler.',
 (L('controllers','basic-controllers'),'A route handler can be [ControllerClass::class, "action"] to dispatch to that controller method.'),
 (L('routing','api-routes'),'routes/api.php has the /api prefix by default, so a route declared there as /user is addressed as /api/user.'),
 (L('routing','listing-your-routes'),'Run php artisan route:list to verify each configured method, URI and action.'))
add(43,L('queues','generating-job-classes'),
 'php artisan make:job JobName generates a job implementing ShouldQueue, marking it for queued execution.',
 (L('queues','class-structure'),'The job constructor receives its input, and the handle method contains the work to execute.'),
 (L('queues','dispatching-jobs'),'JobName::dispatch($input) passes the input to the job constructor; the sync connection executes immediately instead of leaving asynchronous work pending.'),
 (L('queues','dispatching-to-a-particular-connection'),'Use JobName::dispatch($input)->onConnection(connectionName) to select the supplied asynchronous connection rather than relying on the default.'),
 (L('queues','introduction'),'With an asynchronous connection, queued work can run later outside the request, so check the pending work before allowing a worker to consume it.'))
add(44,'vite_docs#env-and-mode/env-variables',
 'Vite exposes custom environment values through import.meta.env and uses the VITE_ prefix for client-exposed values by default.',
 'Declare a public API address as VITE_API_URL and read import.meta.env.VITE_API_URL in the client.',
 'Custom environment values are read as strings, even when their text looks numeric or boolean.',
 'VITE_ values are embedded in client code at build time and must not contain passwords, private API keys or other secrets.')
add(45,V('essentials/computed','basic-example'),
 'import { computed } from "vue" and computed(() => expression) create a derived ref from reactive values read by the getter.',
 (V('essentials/computed','computed-caching-vs-methods'),'Computed results are cached until their tracked reactive dependencies change.'),
 (V('essentials/computed','getters-should-be-side-effect-free'),'A computed getter should calculate and return a result without mutating source state or making asynchronous requests.'),
 (JS+'control_structures','To calculate a total, initialize a local total, traverse the selected records with for...of, add each required value to it and return that total from the getter.'),
 (JS+'linked Reference/Global_Objects/Array/filter/description','Use records.filter(predicate) to select the records whose values contribute to the derived total.'))
add(46,V('reusability/composables','what-is-a-composable'),
 'A composable is a function that encapsulates reusable stateful behavior using the Composition API.',
 (V('reusability/composables','mouse-tracker-example'),'Export a use-prefixed function containing refs and behavior, return the state and actions, and call it from the consuming component’s setup.'),
 (V('reusability/composables','mouse-tracker-example'),'Refs created inside the composable’s call belong to that call, so separate calls can have isolated state.'),
 (V('scaling-up/state-management','simple-state-management-with-reactivity-api'),'State declared at module scope instead of inside the function can be shared by consumers of that module.'))
add(47,V('essentials/template-syntax','text-interpolation'),
 'Use {{ value }} to interpolate component data as text, which updates when the value changes.',
 (V('essentials/template-syntax','attribute-bindings'),'Use v-bind:attribute="value" or :attribute="value" for a dynamic HTML attribute rather than placing mustaches inside that attribute.'),
 (V('essentials/template-syntax','attribute-bindings'),'A null or undefined bound attribute value removes that attribute from the rendered element.'),
 (V('essentials/template-syntax','boolean-attributes'),'For boolean attributes such as disabled, a truthy value or an empty string includes the attribute, while other falsy values omit it.'))
add(48,L('eloquent-mutators','attribute-casting'),
 'Define protected function casts(): array returning attribute-name-to-cast-type mappings to convert model attributes to application-facing types.',
 'A boolean cast converts the documented stored is_admin integer values 0 and 1 into a boolean when the attribute is accessed.',
 'Attributes whose value is null are not cast.',
 (L('eloquent-mutators','date-casting'),'Use date or datetime casts for date attributes; the application receives date objects and values assigned as supported date representations are converted for database storage.'),
 (L('eloquent-mutators','date-casting'),'A date cast’s serialization format does not itself specify the database storage format.'))
add(49,L('queries','where-clauses'),
 'where(column, operator, value) adds a predicate, while where(column, value) assumes equality.',
 'Chaining ordinary where clauses requires all those predicates to match.',
 (L('queries','ordering'),'orderBy(column, "asc") orders ascending and orderBy(column, "desc") orders descending; ascending is the default.'),
 ('laravel_eloquent#building-queries','Call get() after chaining query constraints to retrieve the matching models rather than retrieving every model first.'))
add(50,L('seeding','writing-seeders'),
 'Generate a seeder with php artisan make:seeder SeederName and put the intended baseline insert operations in its run method.',
 'A seeder’s run method may insert data through DB::table(tableName)->insert($records) or through Eloquent.',
 (L('seeding','calling-additional-seeders'),'Use $this->call([SeederClass::class]) in DatabaseSeeder to include a separate dataset seeder.'),
 (L('seeding','running-seeders'),'Run php artisan db:seed or php artisan db:seed --class=SeederName against the intended development database.'),
 (L('seeding','running-seeders'),'php artisan migrate:fresh --seed drops tables, reapplies migrations and seeds data, so it is a destructive way to rebuild a development database.'))
add(51,L('validation','creating-form-requests'),
 'Generate a form request with php artisan make:request RequestName and return field-to-rule mappings from its rules method.',
 'Type-hint the form request in the controller action to validate the incoming data before the action executes.',
 (L('validation','rule-required'),'required rejects a missing or empty required field.'),
 (L('validation','rule-string'),'string requires the supplied field value to be a string.'),
 (L('validation','rule-max'),'max sets a limit appropriate to the field type, including a maximum character length for strings.'),
 (L('validation','a-note-on-optional-fields'),'nullable permits null for optional fields that would otherwise fail their type rule.'),
 (L('validation','validation-error-response-format'),'When JSON is expected, validation failure returns status 422 with a message and an errors object mapping fields to lists of messages.'))
add(52,L('responses','json-responses'),
 'response()->json($data) serializes the supplied array as JSON and sets Content-Type to application/json.',
 (L('responses','creating-responses'),'Supply an explicit response status to select the HTTP outcome rather than relying on the default 200 status.'),
 (L('responses','other-response-types'),'Use response()->json($data, $status) to pair the required JSON body with the chosen outcome status.'),
 (L('responses','attaching-headers-to-responses'),'Use response headers when the response contract requires metadata outside the JSON body.'))
add(53,L('middleware','defining-middleware'),
 'A middleware handle method examines a request and either returns its own response or calls $next($request) to let handling continue.',
 (L('middleware','assigning-middleware-to-routes'),'Assign middleware to a route with ->middleware(MiddlewareClass::class).'),
 (L('middleware','middleware-groups'),'Use Route::middleware([...])->group(function () { ... }) to apply request checks to every route inside that group.'),
 'A rejected request returns at the middleware boundary instead of reaching the protected handler.')
add(54,L('eloquent-factories','introduction'),
 'A model factory defines a default set of attribute values through definition(): array, using values that suit the model’s data requirements.',
 (L('eloquent-factories','generating-factories'),'Generate the factory with php artisan make:factory FactoryName and associate it with the intended model.'),
 (L('eloquent-factories','instantiating-models'),'Model::factory()->make() creates an unpersisted model instance and permits explicit attribute overrides.'),
 (L('eloquent-factories','persisting-models'),'Model::factory()->create() persists the generated model, and ->count(number)->create() persists several models.'))
add(55,L('deployment','optimization'),
 'php artisan optimize caches production configuration, events, routes and views as part of deployment.',
 (L('deployment','caching-configuration'),'php artisan config:cache combines configuration into one cached file; subsequent .env reads outside configuration files do not work as ordinary environment loading.'),
 (L('deployment','caching-routes'),'php artisan route:cache caches route registrations, so changes to routes require rebuilding that cache.'),
 (L('deployment','caching-views'),'php artisan view:cache precompiles Blade views.'),
 'php artisan optimize:clear removes optimization caches and also clears keys in the default cache driver.')
add(56,L('queues','the-queue-work-command'),
 'Run php artisan queue:work connectionName to consume jobs from the selected asynchronous queue connection.',
 (L('queues','processing-a-single-job'),'Use queue:work --once when verification requires processing one available job and then exiting.'),
 (L('queues','queue-workers-and-deployment'),'Long-lived workers do not notice code changes until restarted; php artisan queue:restart asks them to exit after finishing their current job.'),
 (L('queues','queue-workers-and-deployment'),'A process manager must restart exited workers, and a functioning cache driver is needed for queue restart signals.'))
add(57,L('database','database-transactions'),
 'Wrap related writes in DB::transaction(function () { ... }) to execute them within one database transaction.',
 'If the transaction callback throws an exception, its database changes are rolled back and the exception is rethrown.',
 'If the callback completes successfully, the transaction commits automatically.',
 'Put both writes inside the same transaction callback so a failure in the second does not leave the first write committed independently.')
add(58,L('routing','implicit-binding'),
 'Implicit model binding resolves a type-hinted model parameter when its variable name matches the route segment name.',
 'The documented /users/{user} route with User $user loads the User whose primary key matches the parameter.',
 'When no matching model exists, implicit binding generates a 404 response instead of passing a nonexistent model to the action.',
 (L('routing','customizing-the-default-key-name'),'Use a segment such as {post:slug} when binding must use a specified model column rather than the default key.'))
add(59,'vite_docs#config/server-options/server-proxy',
 'A relative frontend request is addressed through the frontend origin unless a development proxy forwards that path to the API server.',
 'Configure server.proxy with a path prefix and the backend target to forward matching development requests.',
 'Check the proxy target and any rewrite rule against the backend’s real path, because removing or retaining a prefix changes the forwarded URL.',
 (L('routing','listing-your-routes'),'Compare the requested method and endpoint with php artisan route:list to distinguish an API path mismatch from a frontend-server address.'))
add(60,'vite_docs#build/building-for-production',
 'Run npm run build when its script invokes vite build to produce a production bundle from the project’s index.html entrypoint.',
 ('vite_docs#static-deploy/building-the-app','Vite writes deployable output to dist by default.'),
 ('vite_docs#static-deploy/testing-the-app-locally','Run npm run preview when its script invokes vite preview to serve the built dist output for local verification.'),
 ('vite_docs#static-deploy/','vite preview is a local build preview, not a production hosting server.'))
add(61,V('essentials/watchers','watch-source-types'),
 'Use watch(source, callback) with a ref or a getter to run a reactive side effect for a specified source.',
 'To watch one reactive property, pass () => object.property rather than the property’s current primitive value.',
 (V('essentials/watchers','eager-watchers'),'watch is lazy by default; { immediate: true } also runs its callback at registration.'),
 (V('essentials/watchers','basic-example'),'Place the intended persistence operation in the callback rather than a computed getter, keeping the watched source limited to the state that should trigger it.'),
 (V('essentials/watchers','stopping-a-watcher'),'A watcher created synchronously during component setup stops with its component, while the returned stop function permits stopping it explicitly.'))
add(62,V('essentials/event-handling','listening-to-events'),
 'Use v-on:event="handler" or @event="handler" to listen for a DOM event such as a button click.',
 (V('essentials/event-handling','method-handlers'),'A named method handler is called when the event occurs and receives the native event object.'),
 (V('essentials/reactivity-fundamentals','ref'),'Inside the handler, update a ref through .value so Vue tracks the state change.'),
 (V('essentials/event-handling','inline-handlers'),'An inline event expression can perform a small update such as @click="count++" directly in the template.'))
add(63,V('components/props','props-declaration'),
 'Declare child input with defineProps([...]) or an object of prop definitions inside <script setup>.',
 (V('components/props','static-vs-dynamic-props'),'Pass a changing parent value with a bound attribute such as :title="value" instead of a literal static string.'),
 (V('components/props','one-way-data-flow'),'Props flow from parent to child and are readonly in the child; copying an initial prop into local state does not track later parent changes.'),
 (V('components/props','mutating-object-array-props'),'An object or array prop still exposes nested references, so avoid changing nested parent data from the child.'))
add(64,V('essentials/conditional','v-if'),
 'v-if="condition" creates its subtree when the condition is truthy; v-else-if and v-else provide adjacent alternatives.',
 (V('essentials/conditional','v-show'),'v-show keeps an element in the DOM and toggles its display rather than creating and destroying it.'),
 (V('essentials/conditional','v-if-vs-v-show'),'v-if is lazy for an initially false branch and has higher toggle cost, while v-show has higher initial render cost but cheaper toggles.'),
 (V('essentials/conditional','v-else'),'Place v-else or v-else-if immediately after its conditional sibling so Vue can recognize the branch.'))
add(65,V('essentials/list','v-for'),
 'Use v-for="item in items" to render a list, with item referring to the current array element.',
 (V('essentials/list','maintaining-state-with-key'),'Bind a unique stable item identifier with :key="item.id" so Vue can reuse and reorder nodes by identity.'),
 (V('essentials/list','maintaining-state-with-key'),'Without identity keys, Vue’s default in-place patching can attach temporary input or child state to the wrong item after reordering.'),
 (V('essentials/list','maintaining-state-with-key'),'Keys should be primitive strings or numbers rather than object values.'))
add(66,V('best-practices/security','html-content'),
 'Vue text interpolation automatically escapes HTML content, treating untrusted markup as text.',
 (V('best-practices/security','html-injection'),'v-html inserts raw HTML and can expose users to markup injection when used with untrusted content.'),
 'Replace raw HTML insertion for untrusted text with {{ value }} so the content is escaped.',
 (V('best-practices/security','rule-no-1-never-use-non-trusted-templates'),'Never use untrusted content as a Vue component template, which permits arbitrary JavaScript execution.'))
add(67,L('validation','validation-error-response-format'),
 'When a validation exception occurs for a request expecting JSON, Laravel returns HTTP 422 with message and errors properties.',
 'The errors object maps each invalid field name to an array of messages, and nested field names use dot notation.',
 (L('validation','quick-writing-the-validation-logic'),'Call $request->validate($rules) to enforce field rules and trigger Laravel’s normal validation failure response.'),
 (L('responses','json-responses'),'If constructing a specified custom error contract, use response()->json($body, 422) with its required field-to-message mapping.'))
add(68,L('eloquent-relationships','one-to-many'),
 'A one-to-many relationship connects a parent model to multiple child records through their foreign key.',
 'Define a parent relationship method returning $this->hasMany(Child::class), supplying a custom foreign key if the convention does not match.',
 (L('eloquent-relationships','one-to-many-inverse'),'Define the child’s inverse method with $this->belongsTo(Parent::class) to resolve its parent.'),
 'In the documented Post and Comment relationship, comments.post_id matches posts.id, and $post->comments retrieves that post’s related comments.',
 (L('eloquent-relationships','one-to-many-inverse'),'Access $comment->post to retrieve the parent that matches that comment’s foreign key.'))
add(69,L('queries','introduction'),
 'Laravel’s query builder uses PDO parameter binding for query values, helping protect against SQL injection.',
 (L('queries','where-clauses'),'Use where(column, operator, $value) to pass a search value separately from the query structure.'),
 (L('queries','raw-methods'),'When raw SQL is necessary, whereRaw("column = ?", [$value]) supplies a separate binding rather than interpolating input into SQL.'),
 (L('queries','raw-expressions'),'Raw expressions are injected as SQL strings and require care to avoid injection vulnerabilities.'),
 (L('queries','where-clauses'),'Column names cannot be bound by PDO, so choose columns from trusted definitions rather than letting arbitrary input dictate them.'))
add(70,'laravel_eloquent#local-scopes',
 'A local scope encapsulates reusable query constraints on a model.',
 'In Laravel 12, import Illuminate\\Database\\Eloquent\\Attributes\\Scope and mark a model method with #[Scope], taking a Builder and returning void or the same builder.',
 'The documented active scope applies $query->where("active", 1) inside the scope method.',
 ('laravel_eloquent#utilizing-a-local-scope','Call Model::active()->where(...)->get() to combine the scope with another query constraint rather than retrieve records inside the scope.'))
add(71,L('eloquent-resources','writing-resources'),
 'An API resource translates a model into an explicit public array through toArray(Request $request): array.',
 'Return an array listing the allowed output keys and their model values instead of automatically including every model attribute.',
 (L('eloquent-resources','concept-overview'),'Create a resource extending JsonResource and return new ResourceName($model) from a handler to expose that transformation.'),
 (L('eloquent-resources','data-wrapping'),'The outermost resource response is wrapped in a data key by default, so include the configured wrapping in the public contract.'))
add(72,L('controllers','actions-handled-by-resource-controllers'),
 'Resource controller index, store, show, update and destroy actions correspond to listing, creating, reading, updating and deleting resources.',
 (L('controllers','api-resource-routes'),'Route::apiResource(resourceName, ControllerClass::class) omits the create and edit routes used for HTML forms.'),
 ('laravel_eloquent#mass-assignment','Implement a store action by creating the model from accepted attributes through Model::create($attributes).'),
 (L('responses','json-responses'),'Return the specified public JSON body and creation status with response()->json($body, 201) when the endpoint contract calls for 201.'))
add(73,L('validation','working-with-validated-input'),
 '$request->validated() returns the validated data, while $request->safe()->only([...]) selects a subset rather than including unvalidated fields.',
 (L('validation','validating-when-present'),'Use sometimes to validate an optional update field only if it is present.'),
 (L('validation','a-note-on-optional-fields'),'Use nullable when an explicitly supplied null is permitted; Laravel’s default empty-string conversion can produce null.'),
 (P('function.array-key-exists.php'),'array_key_exists($key, $validated) detects a present key even when its value is null, unlike isset.'),
 ('laravel_eloquent#mass-assignment','Apply only the validated attributes that are present through $model->fill($validated), then save, so omitted fields are not replaced by invented defaults.'))
add(74,L('routing','listing-your-routes'),
 'Compare the captured request method and URL with php artisan route:list to check whether the expected backend route is targeted.',
 (FETCH+'handling_the_response','Separate a received HTTP status from a rejected fetch operation before locating a failure in request transport or server response handling.'),
 (L('logging','writing-log-messages'),'Use matching server log messages and request details as evidence of the point reached in backend handling rather than guessing solely from the visible screen.'),
 (L('logging','contextual-information'),'Add non-sensitive contextual information to a log message to distinguish the request being diagnosed, then repeat the request after the change to inspect the resulting evidence.'))
add(75,V('components/events','declaring-emitted-events'),
 'Declare emitted events with const emit = defineEmits([eventNames]) at the top level of <script setup>.',
 (V('components/events','event-arguments'),'emit(eventName, payload) notifies the parent with the supplied payload.'),
 (V('components/events','emitting-and-listening-to-events'),'The parent listens with @event-name="handler" on the child component and updates its own state in that handler.'),
 (V('components/events','emitting-and-listening-to-events'),'Component events do not bubble; a parent can listen to its direct child rather than relying on a DOM-style bubbling chain.'),
 (V('components/props','one-way-data-flow'),'Keep the parent-owned input readonly in the child and communicate the requested change through the event instead.'))
add(76,V('essentials/forms','basic-usage'),
 'v-model uses the bound JavaScript state as the source of truth and ignores initial value, checked and selected attributes on controls.',
 (V('essentials/forms','text'),'Use <input v-model="field"> to keep text input and the component’s field state synchronized.'),
 (V('essentials/event-handling','event-modifiers'),'Use <form @submit.prevent="onSubmit"> to invoke a component submit handler without the browser’s default form navigation.'),
 (FETCH+'setting_the_body','Serialize the current form values with JSON.stringify in the request body when submitting a JSON payload, rather than submitting unrelated component state.'))
add(77,FETCH+'sending_data_in_a_get_request',
 'GET request parameters belong in the URL query string; URLSearchParams encodes named filter and sort values for that string.',
 'Create a URLSearchParams object, append the required names and current values, and append its serialized string after ? in the requested URL.',
 (V('essentials/forms','basic-usage'),'Keep filter controls bound to component state through v-model so the request can use the current selections.'),
 (V('essentials/watchers','watch-source-types'),'Watch the relevant selected values or invoke an event handler to rebuild the request parameters and fetch results when those selections change.'))
add(78,'pinia_docs#core-concepts/Defining-a-Store',
 'defineStore(uniqueId, options) defines a store, and calling its exported useStore function returns the shared store instance for consumers.',
 ('pinia_docs#introduction/Basic-example','Put shared values in state: () => ({ ... }) and export the useStore function from the store module.'),
 ('pinia_docs#getting-started/Installation','Create Pinia with createPinia() and install it through app.use(pinia) before the application is mounted.'),
 ('pinia_docs#core-concepts/actions/Actions','Define actions as store methods to centralize state-changing business logic and invoke them through store.actionName(...).'),
 ('pinia_docs#core-concepts/state/Accessing-the-state','Read store.property in each component so both consumers observe the same shared state.'))
add(79,V('scaling-up/state-management','simple-state-management-with-reactivity-api'),
 'Keep a single shared source of truth for values used by multiple component instances rather than independent copies that must be synchronized.',
 'Expose named state-changing operations on the shared state owner so mutation logic is centralized instead of scattered across consumers.',
 (V('components/props','one-way-data-flow'),'Keep local editable state in a component when that component owns the draft, rather than mutating a parent-owned prop.'),
 ('pinia_docs#core-concepts/state/Accessing-the-state','Move cross-view values into a store and have consumers read those store properties instead of maintaining duplicate cross-view values.'))
add(80,V('reusability/composables','async-state-example'),
 'Represent asynchronous fetching with separate reactive result and error values so a component can distinguish success from failure.',
 (V('essentials/watchers','basic-example'),'Set loading before awaiting work, update data or error according to the outcome, and reset loading in finally.'),
 (V('essentials/conditional','v-if'),'Render a failure branch when error is set, a loading branch while work is pending, and a success branch after a result arrives.'),
 (V('essentials/list','v-for'),'Within the successful list branch, test whether the returned collection has any items so an empty result can render a distinct empty-state message instead of remaining in loading.'))
add(81,L('eloquent-resources','writing-resources'),
 'A resource’s explicit toArray output determines the public field names and values, allowing a new field to be added without automatically exposing unrelated attributes.',
 (L('eloquent-resources','data-wrapping'),'Outermost resource wrapping is part of the response shape; changing whether data is wrapped changes how consumers must access it.'),
 (L('http-tests','testing-json-apis'),'assertJson($expectedFragment) checks that existing required data remains present even when the response contains additional properties.'),
 (L('http-tests','assert-json-path'),'Use assertJsonPath(path, expectedValue) to check retained field paths and values alongside an assertion for the added field.'))
add(82,V('essentials/watchers','basic-example'),
 'Set a reactive pending flag before awaiting submission and reset it in finally so both success and failure end the pending state.',
 'Bind :disabled="pending" on the submit control to prevent further interaction with it while the request is pending.',
 (V('reusability/composables','async-state-example'),'Keep success data separate from request errors and update the appropriate outcome when the awaited submission completes.'),
 (V('essentials/conditional','v-if'),'Render pending, success and error feedback from their corresponding state rather than showing success immediately after starting a request.'))
add(83,FETCH+'including_credentials',
 'fetch defaults to credentials: "same-origin"; use credentials: "include" when the configured cookie-authenticated API is on another origin.',
 ('laravel_sanctum#cors-and-cookies','For a separate-subdomain SPA, configure server CORS supports_credentials=true and a session cookie domain that covers the relevant subdomains.'),
 ('laravel_sanctum#configuring-your-first-party-domains','Configure Sanctum’s stateful domains for the SPA’s origin and include the port when it is part of that origin.'),
 ('laravel_sanctum#how-it-works-spa-authentication','A cookie-authenticated SPA should send its session credentials rather than substituting a bearer API token for its chosen authentication mode.'))
add(84,'vue_router_docs#guide/essentials/dynamic-matching/Reacting-to-Params-Changes',
 'When navigation matches the same route component with a different parameter value, Vue Router reuses its instance and some lifecycle hooks do not run again.',
 'Use const route = useRoute() and watch(() => route.params.id, callback) to respond to a changed route identifier.',
 'Call the data-loading operation with the new identifier inside the callback so the reused view receives the newly selected record.',
 (V('essentials/watchers','eager-watchers'),'Add { immediate: true } when the same watcher should load the initial record as well as subsequent parameter changes.'))
add(85,'vue_router_docs#guide/advanced/navigation-guards/Global-Before-Guards',
 'Register router.beforeEach((to, from) => { ... }) to inspect the destination before navigation is confirmed.',
 'Return false to cancel navigation, a route location to redirect, or undefined/true to allow navigation to proceed.',
 'Redirect an unauthenticated user to the login route while excluding that login route from the redirect condition to avoid a redirect loop.',
 (L('authentication','protecting-routes'),'Protect the API independently with server authentication checks; a frontend route guard only controls client navigation.'))
add(86,L('authentication','authenticating-users'),
 'Pass validated credentials to Auth::attempt($credentials) to check the stored user record and password and establish authentication on success.',
 'Auth::attempt checks the submitted plaintext password against the stored password hash, so do not hash the submitted password before calling it.',
 'Regenerate the session after successful authentication with $request->session()->regenerate() to prevent session fixation.',
 (L('authentication','logging-out'),'Auth::logout() removes the authentication information from the session, and $request->session()->invalidate() invalidates that session.'))
add(87,'laravel_sanctum#protecting-spa-routes',
 'Assign ->middleware("auth:sanctum") to protected API routes to require a stateful authenticated request or a valid API token.',
 ('laravel_sanctum#how-it-works-spa-authentication','For first-party SPA requests, Sanctum checks cookie-based session authentication rather than requiring a personal access token.'),
 ('laravel_sanctum#protecting-spa-routes','Inside a protected route, $request->user() retrieves the authenticated user.'),
 (L('http-tests','assert-unauthorized'),'Check anonymous JSON access with assertUnauthorized(), which asserts a 401 outcome, rather than treating the route as publicly accessible.'))
add(88,'laravel_sanctum#csrf-protection',
 'For Sanctum cookie-based SPA login, first request /sanctum/csrf-cookie to initialize CSRF protection.',
 'That request sets an XSRF-TOKEN cookie; URL-decode its value and send it as X-XSRF-TOKEN on subsequent requests when the client library does not do this automatically.',
 ('laravel_sanctum#logging-in','After CSRF initialization, POST the credentials to /login; successful login establishes the session cookie used on later requests.'),
 ('laravel_sanctum#logging-in','If a later session expires, a 401 or 419 response may require returning the user to login rather than disabling CSRF protection.'))
add(89,L('http-tests','testing-json-apis'),
 'Use getJson, postJson, putJson, patchJson or deleteJson with an endpoint and payload to exercise a JSON API from a Laravel feature test.',
 'assertStatus(expectedStatus) checks the HTTP outcome and assertJson($fragment) checks the expected response data.',
 (L('http-tests','assert-json-path'),'Use assertJsonPath(path, expectedValue) for a particular JSON field or nested field.'),
 (L('http-tests','assert-json-validation-errors'),'For an invalid payload, assertJsonValidationErrors([fieldNames]) checks the response’s field-error mapping.'),
 (L('http-tests','assert-unprocessable'),'assertUnprocessable() verifies the invalid-request 422 status alongside the field-error assertion.'))
add(90,L('database-testing','resetting-the-database-after-each-test'),
 'Use the RefreshDatabase trait in the feature test class so state from an earlier participating test does not interfere with the next one.',
 'When the schema is current, RefreshDatabase runs a test in a transaction rather than migrating the schema for every test.',
 (L('eloquent-factories','persisting-models'),'Arrange persisted test data with Model::factory()->create($overrides) before making the request.'),
 (L('database-testing','assert-database-has'),'assertDatabaseHas(tableName, $attributes) checks that a matching database record exists after the operation.'),
 (L('database-testing','assert-database-missing'),'assertDatabaseMissing(tableName, $attributes) checks that a matching record no longer exists.'))
add(91,L('pagination','paginating-eloquent-results'),
 'Use Model::where(...)->orderBy(...)->paginate(perPage) to apply constraints and return a bounded page instead of loading the whole matching collection.',
 (L('pagination','paginating-query-builder-results'),'paginate reads the current page from the page query-string argument by default and applies the appropriate limit and offset.'),
 (L('pagination','converting-results-to-json'),'Returning the paginator as JSON places records in data and supplies metadata including total, per_page, current_page and last_page.'),
 (L('pagination','converting-results-to-json'),'Use the paginator’s next_page_url and prev_page_url to identify adjacent page destinations, which may be null at a boundary.'))
add(92,L('eloquent-relationships','querying-relationship-existence'),
 'Model::has(relationshipName) restricts results to parents that have related records.',
 'whereHas(relationshipName, function (Builder $query) { ... }) additionally constrains the related records that must exist.',
 'Put the related-record predicate inside that callback and call get() on the outer query to retrieve the matching parent models.',
 (L('eloquent-relationships','querying-relationship-absence'),'doesntHave(relationshipName) selects parents with no related records, while whereDoesntHave applies a predicate to the relationship absence check.'))
add(93,L('authorization','policy-methods'),
 'A policy action method receives the authenticated user and relevant model and returns whether that user may perform the action on that model.',
 'The documented PostPolicy::update compares $user->id === $post->user_id to grant only the owner’s update.',
 (L('authorization','generating-policies'),'Generate a model-associated policy with php artisan make:policy PolicyName --model=ModelName.'),
 (L('authorization','policy-discovery'),'Laravel discovers policies following its model and policy naming and directory conventions; otherwise register the intended model-to-policy mapping explicitly.'),
 (L('authorization','via-the-gate-facade'),'Call Gate::authorize(actionName, $model) before a protected action to enforce the relevant policy and return 403 on denial.'))
add(94,L('authorization','introduction'),
 'Being authenticated does not itself grant permission to act on a particular resource; authorization determines whether that action is allowed.',
 (L('authorization','via-middleware'),'Apply ->middleware("can:update,post") or ->can("update", "post") to authorize the action for the model bound to the route parameter before the handler runs.'),
 (L('authorization','via-middleware'),'The can middleware returns 403 when the user is not permitted to perform the specified action.'),
 (L('authorization','via-the-gate-facade'),'Alternatively call Gate::authorize(actionName, $model) in the controller before carrying out the protected action.'))
add(95,L('authorization','writing-gates'),
 'Define a named authorization ability with Gate::define(abilityName, callback); the callback receives the authenticated user and returns the permission decision.',
 'Put the role or capability predicate for the privileged action in that callback rather than relying on a hidden frontend control.',
 (L('authorization','authorizing-or-throwing-exceptions'),'Enforce the ability before the privileged action with Gate::authorize(abilityName), which produces 403 when the ability is denied.'),
 (L('authorization','middleware-actions-that-dont-require-models'),'Use ->middleware("can:ability-name") to enforce an ability that does not require a model instance at a route boundary.'))
add(96,L('http-tests','session-and-authentication'),
 'Use $this->actingAs($user) before a JSON request to make that request as a chosen authenticated user.',
 (L('eloquent-factories','persisting-models'),'Create owner and non-owner user fixtures and a record with an explicit owner attribute so the test cases exercise different ownership decisions.'),
 (L('http-tests','assert-unauthorized'),'Make a separate anonymous JSON request and assertUnauthorized() to verify a 401 outcome.'),
 (L('http-tests','assert-forbidden'),'Make a request as the forbidden non-owner and assertForbidden() to verify a 403 authorization denial.'),
 (L('http-tests','testing-json-apis'),'For the permitted owner, assert the specified success status and expected response JSON rather than merely checking that no exception escaped.'))
add(97,L('eloquent-relationships','eager-loading'),
 'Lazy access to a relationship for each model in a collection can execute one extra query per model, creating the N+1 query pattern.',
 'Use Model::with(relationshipName)->get() to load the needed relationship while retrieving the parent collection.',
 'The documented Book::with("author")->get() uses one books query and one authors query instead of one author query for each book.',
 (L('eloquent-relationships','eager-loading-specific-columns'),'When selecting related columns, retain the related id and required foreign-key columns as well as the displayed fields.'),
 (L('eloquent-resources','conditional-relationships'),'A resource can use whenLoaded(relationshipName) to include already-loaded related data without forcing that relationship to load during serialization.'))
add(98,V('components/props','one-way-data-flow'),
 'Readonly props carry parent-owned state into the child; assigning a prop in the child is not a supported update path.',
 (V('components/events','event-arguments'),'Emit a named event with the proposed value so the parent can decide how to update its state.'),
 (V('essentials/forms','basic-usage'),'Bind an editable local draft through v-model when the child owns the draft rather than binding directly to a parent-owned prop.'),
 (V('components/props','mutating-object-array-props'),'Avoid editing nested fields of an object prop, since those nested references still point into the parent’s data.'),
 (V('components/events','emitting-and-listening-to-events'),'Listen for the child event in the parent and update the parent-owned value there.'))
add(99,L('validation','validation-error-response-format'),
 'A JSON validation error has status 422 and an errors object whose field keys map to arrays of validation messages.',
 (FETCH+'handling_the_response','Check for status 422 and parse the response JSON instead of expecting fetch itself to reject for validation errors.'),
 (V('essentials/reactivity-fundamentals','ref'),'Store the returned errors mapping in reactive component state so updated errors appear in the form.'),
 (V('essentials/conditional','v-if'),'Render a field’s messages beside that field when its error entry exists, rather than treating all field errors as a successful submission.'))
add(100,V('scaling-up/testing','component-testing'),
 'Mount the component with input props and inspect its rendered public output rather than its private internal implementation.',
 'Use wrapper.find(selector).text() with expect(...).toContain(expectedText) to check the output rendered for the chosen input.',
 'await wrapper.find(selector).trigger("click") performs a user-like interaction before checking the resulting render.',
 (V('scaling-up/testing','component-testing'),'Assert the rendered update or emitted event after the interaction so the test fails when the component’s public behavior regresses.'))
add(101,'vue_docs#scaling-up/testing/mounting-libraries -> linked vuejs/test-utils documentation/guide/essentials/forms/',
 'Mount the form, select its native input, and await wrapper.get(selector).setValue(value) to simulate the user entering a value.',
 'Use await wrapper.get("form").trigger("submit.prevent") to submit the mounted form through its public event handling.',
 'Inspect wrapper.emitted(eventName) to check that submission produced the expected event payload.',
 (V('scaling-up/testing','component-testing'),'For a form that displays validation feedback, assert the visible field-error output after the invalid submission rather than testing only private validation state.'))
add(102,'vitest_docs#guide/mocking/mock-an-exported-function',
 'Use vi.mock(modulePath, () => ({ exportedName: vi.fn() })) to replace the imported request boundary with a controlled mock.',
 ('vitest_docs#guide/mocking/functions','Use mockResolvedValue(result) and mockRejectedValue(error) on the mock to exercise fulfilled and rejected asynchronous request paths.'),
 ('vue_docs#scaling-up/testing/mounting-libraries -> linked vuejs/test-utils documentation/guide/advanced/http-requests/','Call await flushPromises() after the mocked asynchronous request to let the component process its response before asserting the result.'),
 ('vue_docs#scaling-up/testing/component-testing','Assert loading and error UI for their controlled outcomes, then the rendered successful data for the successful outcome.'),
 ('vitest_docs#guide/mocking/mocking','Clear or restore mocks between tests so one test’s controlled responses and recorded calls do not leak into another.'))
add(103,L('deployment','server-configuration'),
 'Configure the web server to send Laravel requests to public/index.php and use public as the web root rather than exposing the project root.',
 (L('deployment','directory-permissions'),'Give the web-server process write access to storage and bootstrap/cache for application operation.'),
 (L('deployment','debug-mode'),'Set APP_DEBUG=false for production so error pages do not reveal sensitive configuration.'),
 (L('deployment','caching-configuration'),'Cache the intended production configuration and use config values in application code rather than reading .env directly after configuration is cached.'),
 (L('deployment','health-route'),'Request the configured health route to check that the deployed application boots without throwing exceptions.'))
add(104,'vite_docs#build/public-base-path',
 'Set Vite’s base option to the deployed public base path when serving the built app beneath a nested URL path.',
 'vite build rewrites asset paths according to base, including JavaScript imports, CSS URLs and asset references in HTML.',
 ('vite_docs#static-deploy/building-the-app','Build the application and serve the generated dist directory rather than relying on the development server.'),
 ('vue_router_docs#guide/essentials/history-mode/HTML5-Mode','A createWebHistory router needs the production server to fall back to the app’s index.html for client routes that do not identify a static file.'),
 ('vue_router_docs#guide/essentials/history-mode/HTML5-Mode','Verify a client route through a direct URL request as well as in-app navigation, since a missing fallback can produce a server 404 on the direct request.'))
add(105,L('container','binding-interfaces-to-implementations'),
 'Bind an interface to an implementation with $this->app->bind(InterfaceName::class, ImplementationName::class) in a service provider.',
 'Type-hint the interface in a container-resolved consumer’s constructor so the container injects the registered implementation.',
 (L('container','zero-configuration-resolution'),'Concrete classes whose dependencies are concrete can often be resolved without an explicit binding, whereas the container needs a mapping for the chosen interface implementation.'),
 'Change the implementation binding to substitute another conforming service without changing the consumer’s interface dependency.')
add(106,V('scaling-up/testing','testing-composables'),
 'A composable using only reactivity APIs can be tested by calling it directly and asserting the returned state and methods.',
 'Call a returned action, then use expect(resultRef.value).toBe(expectedValue) to verify its observable state change.',
 'A composable using lifecycle hooks needs a mounted host component in the test so those hooks run.',
 'Mount a host whose setup invokes the composable, retain its result, and unmount the host when checking teardown behavior.',
 'Create separate composable calls or host instances when verifying that call-local state is isolated.')
add(107,L('queues','dealing-with-failed-jobs'),
 'An asynchronous job that exceeds its permitted attempts is recorded as a failed job rather than retried indefinitely.',
 'Set a finite job $tries value or queue:work --tries=number to bound attempts; absent that worker option or a job override, the worker attempts a job once.',
 'Set a job $backoff or worker --backoff value to delay retries after an exception; the default retry release is immediate.',
 (L('queues','viewing-failed-jobs'),'Run php artisan queue:failed to inspect recorded failures and php artisan queue:retry id to retry a selected failed job.'),
 (L('queues','timeout-and-failure'),'Set a job $timeout or worker --timeout to bound execution time; the job-level timeout takes precedence.'),
 (L('queues','worker-timeouts'),'Keep worker timeout shorter than retry_after to reduce the risk of the same job being processed twice.'))
add(108,L('queries','upserts'),
 'Use a stable identifying column or columns for a repeated operation instead of treating each retry as a new unrelated insert.',
 'upsert($rows, $uniqueBy, $updateColumns) inserts missing records and updates matching records identified by the chosen uniqueness columns.',
 'Except on SQL Server, the identifying upsert columns must have a primary or unique index; MySQL and MariaDB use the table’s primary and unique indexes rather than the uniqueBy argument.',
 (L('migrations','creating-indexes'),'Declare the operation’s durable uniqueness rule with $table->unique(columnName) or a composite unique index in a migration.'),
 (L('queues','worker-timeouts'),'Since a queue job may be processed twice when retry timing and timeouts overlap, make repeated database application of the operation target that same stable identity.'))
add(109,L('logging','writing-log-messages'),
 'Write server-side diagnostic messages with Log::info(message, context) or another appropriate level through the Log facade.',
 (L('logging','contextual-information'),'Attach a request identifier as log context so messages for one request can be distinguished from others.'),
 (L('logging','contextual-information'),'Log::withContext(["request-id" => $requestId]) adds that identifier to subsequent messages on the channel.'),
 (L('logging','contextual-information'),'The documented request-id middleware also sends Request-Id in the response, allowing captured response evidence to be matched to server logs.'),
 (L('logging','log-levels'),'Choose a level and channel threshold that record the required failure evidence in the deployed environment.'))
add(110,L('scheduling','running-the-scheduler'),
 'A deployed scheduler needs a recurring server trigger, normally one cron entry that runs php artisan schedule:run every minute in the application directory.',
 'schedule:run evaluates due tasks against the server’s current time; declaring a schedule alone does not supply this recurring trigger.',
 (L('scheduling','defining-schedules'),'Use php artisan schedule:list to inspect configured tasks and next due times before checking an actual due run.'),
 (L('scheduling','timezones'),'Confirm the configured task timezone as well as server time when the observed due time differs from the expected schedule.'))
add(111,L('deployment','optimization'),
 'After deploying the intended code and environment configuration, rebuild production optimization caches with php artisan optimize.',
 (L('deployment','caching-configuration'),'A cached configuration prevents ordinary .env loading, so environment changes require rebuilding the configuration cache.'),
 (L('queues','queue-workers-and-deployment'),'Restart long-lived queue workers with php artisan queue:restart so they load the deployed code, with a process manager to start their replacements.'),
 (L('logging','writing-log-messages'),'If verification fails, inspect server logs and the captured response to distinguish a configuration failure from an old running worker or route behavior.'),
 (L('deployment','health-route'),'Request the configured health route to check that the application boots after deployment, then verify the release’s intended request behavior.'))
add(112,V('scaling-up/testing','component-testing'),
 'Verify a complete change through its public UI behavior by interacting as a user and checking the resulting visible output.',
 (L('http-tests','testing-json-apis'),'Use a JSON feature request with status and JSON assertions to verify the same change’s backend endpoint contract.'),
 (L('database-testing','assert-database-has'),'Check persisted effects with assertDatabaseHas(tableName, expectedAttributes) instead of assuming a successful screen proves correct stored data.'),
 (L('http-tests','assert-json-validation-errors'),'Include an invalid request and assert its field errors to verify the failure contract as well as the successful workflow.'),
 (V('scaling-up/testing','why-test'),'When the existing test catches a regression, fix the responsible behavior and rerun it to verify the correction.'))
# Review corrections: remove future ownership instruction from the composable introduction,
# and keep queue production machinery out of the dispatch-only objective.
data[46]=data[46][:3]
data[43][-1]=(L('queues','introduction'),'With an asynchronous connection, queued work can run later outside the request, so verify that dispatch leaves the work pending instead of executing it in that request.')
data[22][-1]=('owasp_top10#2025/A09_2025-Security_Logging_and_Alerting_Failures/description','Do not log sensitive information or expose internal logging events to users, since either can leak sensitive data.')
data[0].append((FETCH+'handling_the_response','HTTP success statuses are in the 200–299 range; specify the expected success and non-success statuses as part of each endpoint contract.'))
data[20][-1]=(P('functions.returning-values.php'),'return passes the result to the caller and ends the function; an untyped function without a return value returns null.')
data[27][-1]=(FETCH+'reading_the_response_body','When the response contains the expected JSON body, use await response.json() to parse it before returning the data to a caller.')
data[83].append(('laravel_sanctum#spa-authentication','Send Accept: application/json and ensure a Referer or Origin header accompanies the first-party SPA request.'))
data[83].append((FETCH+'including_credentials','For a cross-origin credentialed request, the server must allow the specific client origin rather than use an Access-Control-Allow-Origin wildcard.'))
data[87].insert(0,('laravel_sanctum#sanctum-middleware','Call $middleware->statefulApi() inside bootstrap/app.php’s withMiddleware callback so first-party SPA requests can authenticate through Laravel session cookies.'))
data[102][1]=('vitest_docs#api/mock/mockresolvedvalue + mockrejectedvalue','Use mockResolvedValue(result) and mockRejectedValue(error) on the mock to exercise fulfilled and rejected asynchronous request paths.')
data[102][-1]=('vitest_docs#api/vi/vi-resetallmocks','Call vi.resetAllMocks() between tests and set each test’s response anew to reset call histories and mock implementations.')
data[107][4]=(L('queues','timeout'),'Set a job $timeout or worker --timeout to bound execution time; the job-level timeout takes precedence, and job timeouts require the PCNTL PHP extension.')
# Resolve observed live-documentation anchor names, not guessed anchors.
replacements={
 'state-management/why-do-we-need-state-management':'state-management/what-is-state-management',
 'vue_router_docs#guide/The-RouterLink-component':'vue_router_docs#guide/RouterView-and-RouterLink',
 'vue_router_docs#guide/essentials/navigation':'vue_router_docs#guide/essentials/navigation/Navigate-to-a-different-location',
 'vitest_docs#guide/environment':'vitest_docs#guide/environment/test-environment',
 'deployment/caching-configuration':'deployment/optimizing-configuration-loading',
 'deployment/caching-routes':'deployment/optimizing-route-loading',
 'deployment/caching-views':'deployment/optimizing-view-loading',
 'deployment/health-route':'deployment/the-health-route',
 'queues/processing-a-single-job':'queues/processing-a-specified-number-of-jobs',
 'queues/viewing-failed-jobs':'queues/retrying-failed-jobs',
 'queues/timeout-and-failure':'queues/timeout',
 'HTML_forms/making_forms_accessible':'HTML_forms/explicit_and_implicit_form_labels',
 'HTML_forms/the_name_and_value_attributes':'HTML_forms/input_elements',
 'HTML_forms/button_types':'HTML_forms/the_button_element',
 'Modules/exporting_module_features':'Modules/named_exports',
 'Modules/importing_features_into_your_script':'Modules/named_imports',
 'Modules/default_exports_versus_named_exports':'Modules/default_exports_and_imports',
}
def normalize(ref):
 for old,new in replacements.items():ref=ref.replace(old,new)
 # Fully explicit, fetched linked-reference locators, retaining the batch source ID.
 ref=ref.replace(JS,'vue_docs#introduction/what-is-vue -> linked https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Language_overview#')
 ref=ref.replace(HTML,'vue_docs#introduction/what-is-vue -> linked https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Structuring_content/')
 ref=ref.replace(CSS,'vue_docs#introduction/what-is-vue -> linked https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/')
 ref=ref.replace(NPM,'vite_docs#getting-started -> linked https://docs.npmjs.com/cli/v11/')
 ref=ref.replace('https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Language_overview#linked Web/API/Fetch_API/Using_Fetch/','https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch#')
 ref=ref.replace('https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Language_overview#linked Reference/Global_Objects/Array/','https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/')
 ref=ref.replace('vite_docs#getting-started -> linked MDN Web/JavaScript/Guide/Modules/','vite_docs#getgetting-started -> linked https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules#')
 ref=ref.replace('vite_docs#getgetting-started','vite_docs#getting-started')
 for page in ['Basic_HTML_syntax','HTML_forms','Getting_started','Basic_selectors','map','filter']:
  ref=ref.replace('/'+page+'/', '/'+page+'#')
 for page in ['npm-ci','npm-install']:
  ref=ref.replace('/'+page+'/description','/'+page+'#description')
 ref=ref.replace('vuejs/test-utils documentation/guide/','https://github.com/vuejs/test-utils -> documentation https://test-utils.vuejs.org/guide/')
 return ref
misconceptions={
 32:[(P('control-structures.finally.php','Interaction between a finally block and a return statement'),'A return from finally can override an earlier return from try or catch, rather than merely run cleanup while preserving that earlier result.')],
 63:[(V('components/props','prop-validation'),'A prop default does not replace an explicitly passed null; the default applies when the resolved prop value is undefined.')],
 107:[(L('queues','max-attempts'),'--tries=0 means unlimited attempts, not zero work, so it is not a finite retry budget.')]
}
# Align by the actual input concept order, not an assumed curriculum after row 74.
old=data
mapping={75:77,76:78,78:97,79:93,80:76,81:81,83:98,84:80,85:105,86:88,87:99,88:89,89:86,90:95,91:83,93:106,95:102,96:110,97:84,99:92,100:91,102:100,105:87}
data={i:copy.deepcopy(old[i]) for i in range(75)}
for previous,current in mapping.items():data[current]=copy.deepcopy(old[previous])
add(75,'laravel_sanctum#configuring-your-first-party-domains',
 'Sanctum classifies first-party SPA requests using the stateful domains configured in config/sanctum.php.',
 'Include the SPA host and its port in the stateful configuration when the SPA origin includes that port.',
 ('laravel_sanctum#spa-authentication','The first-party SPA and API must share the same top-level domain; different subdomains are supported.'),
 ('laravel_sanctum#sanctum-middleware','Call $middleware->statefulApi() inside bootstrap/app.php’s withMiddleware callback to let first-party SPA requests use Laravel session authentication.'),
 ('laravel_sanctum#spa-authentication','Send Accept: application/json and ensure the browser request supplies a Referer or Origin header so the SPA request boundary can be classified.'))
add(79,'vue_router_docs#guide/essentials/history-mode/HTML5-Mode',
 'createWebHistory uses normal-looking URLs, but a direct request to a nested client route reaches the host before Vue Router starts.',
 'Configure the host to return the SPA index.html for a requested client route that does not match a static file.',
 'For the documented nginx setup, try_files $uri $uri/ /index.html preserves existing files before falling back to the SPA entrypoint.',
 'Verify a direct nested URL and a reload as well as in-app navigation, since client-side navigation alone does not test the host fallback.',
 ('vue_router_docs#guide/essentials/history-mode/Caveat','A catch-all host fallback also serves the SPA for unknown routes; configure a client not-found route instead of assuming the host still returns a normal 404 page.'))
add(82,L('queries','where-clauses'),
 'PDO binds query values, not column names, so filter and sort columns must come from trusted choices rather than arbitrary user input.',
 (L('validation','rule-in'),'Validate a requested filter or sort choice with Rule::in($allowedChoices) so unsupported input is rejected before it is used in query construction.'),
 (L('validation','working-with-validated-input'),'Use the validated filter and sort inputs instead of copying unvalidated request fields into query structure.'),
 (L('queries','where-clauses'),'Map an accepted filter option to a trusted column and apply its submitted value with where(column, operator, value).'),
 (L('queries','ordering'),'Map an accepted sort option to a trusted column and an allowed asc or desc direction before passing it to orderBy.'))
add(85,L('eloquent-relationships','many-to-many-table-structure'),
 'A many-to-many association uses an intermediate pivot table containing a foreign key for each related model, allowing both models to have multiple memberships.',
 (L('eloquent-relationships','many-to-many-model-structure'),'Define a relationship method returning $this->belongsToMany(Related::class), with pivot-table and key arguments when the conventions do not match.'),
 (L('eloquent-relationships','attaching-detaching'),'$model->relationship()->attach($id) inserts a pivot membership, while ->detach($id) removes that membership without deleting either related model.'),
 (L('eloquent-relationships','syncing-associations'),'->sync($ids) makes the pivot membership match the supplied identifier list and removes existing memberships absent from that list.'),
 (L('eloquent-relationships','syncing-associations'),'Use ->syncWithoutDetaching($ids) when omitted existing memberships should be retained rather than removed.'))
# Login precedes logout and fixation defense: do not teach those later boundaries here.
data[88]=data[88][:2]
data[88].append((L('authentication','authenticating-users'),'Auth::attempt returns true for accepted credentials and false for rejected credentials; use that result to select the login endpoint’s specified success or failure response.'))
data[88].append((L('responses','json-responses'),'Return the login contract’s JSON body and status with response()->json($body, $status) after checking the authentication result.'))
add(90,'laravel_sanctum#issuing-api-tokens',
 'Add Laravel\\Sanctum\\HasApiTokens to the user model to support Sanctum personal access tokens.',
 '$user->createToken($name) returns a NewAccessToken object, whose plainTextToken is the newly issued credential sent to the non-SPA client.',
 'Sanctum stores a SHA-256 hash of the token; deliver its plaintext value immediately after issuance rather than expecting to retrieve it from the stored hash later.',
 'The client sends Authorization: Bearer followed by the token value to authenticate its API requests.',
 ('laravel_sanctum#revoking-tokens','$user->tokens()->where("id", $tokenId)->delete() revokes a selected token by removing its stored credential; tokens not deleted by that selection remain present.'),
 ('laravel_sanctum#revoking-tokens','$user->tokens()->delete() revokes every stored token belonging to that user.'))
# The input's component-test practice is specifically input-and-submit.
data[91]=[old[100][0],old[101][0],old[101][1],old[101][2],old[100][-1]]
data[92].append((V('reusability/composables','accepting-reactive-state'),'Clear stale request-error state before starting the next request, then replace it with the new response’s field mapping on a 422 outcome.'))
# State ownership precedes Pinia mechanics; use only the approved shared-boundary vocabulary.
data[93]=[
 (V('scaling-up/state-management','why-do-we-need-state-management'),'When multiple views depend on the same state, independent copies or prop chains can make synchronization difficult; place that shared state at a boundary covering its consumers.'),
 (V('scaling-up/state-management','simple-state-management-with-reactivity-api'),'Use one shared source of truth for values genuinely needed by multiple components rather than duplicating those values in each view.'),
 (V('components/props','one-way-data-flow'),'Keep a component-owned edit draft local when other views do not need that unconfirmed value.'),
 (V('scaling-up/state-management','simple-state-management-with-reactivity-api'),'Separate each component’s local state from the shared values used across component instances; only the cross-view values need the shared store boundary.')]
add(94,L('eloquent-resources','writing-resources'),
 'Define related output explicitly in a resource’s toArray result so the relationship contract chooses which keys and related fields are public.',
 'When the contract requires only a related identifier, return that identifier field rather than serializing the whole related model.',
 (L('eloquent-resources','conditional-relationships'),'Use RelatedResource::collection($this->whenLoaded(relationshipName)) for a related collection that should be included only when the controller has loaded it.'),
 (L('eloquent-resources','conditional-relationships'),'whenLoaded removes that output key when the relationship is not loaded, so check the contract’s omitted-versus-included requirement.'),
 (L('eloquent-relationships','eager-loading'),'Load the chosen included relationship through with(relationshipName) at the parent query boundary rather than triggering per-item lazy relationship queries.'))
add(96,L('authentication','logging-out'),
 'Call Auth::logout() to remove the authenticated user information from the session.',
 'Invalidate the session with $request->session()->invalidate() so its existing data and session identifier are no longer used.',
 'Regenerate the CSRF token with $request->session()->regenerateToken() after logout as recommended by Laravel.',
 (L('session','deleting-data'),'invalidate flushes the session data and regenerates the session ID, making it stronger than merely clearing a client-side user display.'),
 (L('http-tests','available-assertions'),'After logout, verify an unauthenticated state with assertGuest() rather than inferring logout from the visible navigation alone.'))
# Store state is distinct from the later actions concept.
data[97]=[old[78][0],old[78][1],old[78][2],old[78][4]]
data[97].append(('pinia_docs#core-concepts/Destructuring-from-a-Store','Destructuring state directly from a store breaks its reactive connection; use storeToRefs(store) when destructuring state or getters into local refs.'))
data[98].append(('laravel_sanctum#csrf-protection','For a cookie-authenticated mutation, URL-decode the XSRF-TOKEN cookie value and send it as X-XSRF-TOKEN when using fetch, which does not automatically copy that cookie into a CSRF header.'))
data[99]=old[87][1:]
data[99].append((L('routing','route-groups'),'Use Route::middleware("auth:sanctum")->group(function () { ... }) to apply the authentication boundary to every API route inside the group.'))
add(101,L('routing','cors'),
 'Laravel’s global HandleCors middleware handles CORS OPTIONS requests from the configured CORS settings.',
 'Run php artisan config:publish cors to create config/cors.php for the application’s CORS configuration.',
 ('laravel_docs#routing/cors -> published config/cors.php/allowed_origins (framework 12.x config/cors.php)','Set allowed_origins to the explicit approved origins and supports_credentials to true for credentialed API access, rather than retaining the wildcard origin default.'),
 ('laravel_docs#routing/cors -> linked https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS#requests_with_credentials','A credentialed cross-origin response must return a specific Access-Control-Allow-Origin and Access-Control-Allow-Credentials: true; a wildcard origin does not permit browser access to that response.'),
 ('laravel_docs#routing/cors -> linked https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS#preflighted_requests','Verify the allowed origin’s preflight for the required method and headers, and verify that a disallowed origin does not receive permission to access the response.'))
add(103,L('authentication','authenticating-users'),
 'Regenerate the session after a successful Auth::attempt to prevent session fixation.',
 'Call $request->session()->regenerate() inside the successful authentication branch, after credentials have been accepted.',
 (L('session','regenerating-the-session-id'),'Session ID regeneration changes the session identifier while preserving authenticated session data, unlike invalidate which removes all session data.'),
 (L('session','regenerating-the-session-id'),'Verify that the successful login uses the regenerated session identifier instead of continuing with the pre-login identifier.'))
add(104,'pinia_docs#core-concepts/actions/Actions',
 'Define actions as methods in an options store’s actions object to encapsulate shared state transitions.',
 'An action accesses the store through this, so assign this.property inside it to update consumer-visible shared state.',
 'Actions can take arguments and can be asynchronous, awaiting a request before applying its confirmed result to the store.',
 'Call store.actionName(input) from a consumer rather than independently reproducing the shared transition in each component.',
 ('pinia_docs#core-concepts/state/Accessing-the-state','Components reading the same store properties observe the action’s updated shared state.'))
data[105].append(('vue_router_docs#guide/advanced/navigation-guards/Global-Before-Guards','A redirect location can include query: { redirect: to.fullPath } to preserve the intended destination for the login flow instead of losing the protected route the user requested.'))
add(107,'laravel_sanctum#spa-authentication',
 'Sanctum’s first-party SPA cookie model requires the SPA and API to share the same top-level domain, even if they use different subdomains.',
 ('laravel_sanctum#configuring-your-first-party-domains','Configure the deployed SPA host in Sanctum’s stateful domains, retaining a port when it is part of the deployed origin.'),
 ('laravel_sanctum#cors-and-cookies','Set the session domain to cover the deployed SPA and API subdomains and enable credentialed CORS for the approved SPA origin.'),
 ('laravel_docs#session/configuration -> config/session.php/secure (framework 12.x config/session.php)','For an HTTPS deployment, set SESSION_SECURE_COOKIE=true so the browser only sends the session cookie over an HTTPS connection.'),
 ('laravel_sanctum#cors-and-cookies','Ensure the production client sends credentials so a correctly scoped session cookie is actually included in requests.'))
add(108,V('essentials/watchers','basic-example'),
 'Await the mutation before applying its successful result to the visible screen so the UI does not claim that an unconfirmed save completed.',
 (V('essentials/reactivity-fundamentals','ref'),'Assign the confirmed saved record to the screen’s reactive record state so bindings reflect the server result.'),
 (V('essentials/list','replacing-an-array'),'For a reactive record list, replace the stored array with the new confirmed list or a mapped replacement for the matching saved record.'),
 (V('reusability/composables','accepting-reactive-state'),'Alternatively re-fetch the relevant data after successful mutation and replace the screen’s result with that confirmed response.'),
 (V('essentials/watchers','basic-example'),'On a failed mutation, record error feedback instead of applying the success-state update.'))
add(109,L('http-tests','assert-unauthorized'),
 'Use 401 for an unauthenticated request under the specified API failure contract; assertUnauthorized() verifies that status.',
 (L('authorization','via-the-gate-facade'),'A denied authorization enforced by Gate::authorize returns 403, distinguishing lack of permission from lack of authentication.'),
 (L('routing','implicit-binding'),'An implicit model binding that cannot find the requested model returns 404, distinguishing a missing resource from an authorization denial.'),
 (L('responses','json-responses'),'Return the contract’s JSON error body with its selected 401, 403 or 404 status through response()->json($body, $status).'),
 (L('http-tests','testing-json-apis'),'Verify each applicable failure outcome with its status and required JSON fields rather than treating every failed request as the same error.'))
add(111,L('deployment','the-health-route'),
 'Begin a deployment smoke check with the configured health route to verify that Laravel boots without throwing exceptions.',
 (L('authentication','authenticating-users'),'Check login with the disposable acceptance identity and use the resulting authenticated session for the protected workflow.'),
 (L('controllers','actions-handled-by-resource-controllers'),'Exercise create, read, update and delete for disposable records through the deployed resource interface so the smoke check covers each CRUD operation.'),
 (L('http-tests','testing-json-apis'),'Record the HTTP status and public JSON fields for each endpoint outcome against the acceptance contract, not just the screen’s appearance.'),
 (L('logging','contextual-information'),'If a step fails, compare its request and response evidence with matching server log context to identify the deployment boundary reached.'),
 ('vue_router_docs#guide/essentials/history-mode/HTML5-Mode','Include a direct protected-screen URL or reload to verify the deployed SPA host fallback as well as in-app navigation.'))
add(112,'laravel_sanctum#logging-in',
 'A later SPA request may receive 401 or 419 after the session expires, and the frontend should send the user back through login.',
 (L('authorization','via-the-gate-facade'),'A 403 response means the action is forbidden, not simply that the session needs another login.'),
 (FETCH+'handling_the_response','Inspect the received HTTP status before parsing it as successful data so the recovery flow can distinguish unauthenticated and forbidden outcomes.'),
 ('vue_router_docs#guide/advanced/navigation-guards/Global-Before-Guards','Redirect a user needing authentication to login while preserving the requested destination for recovery.'),
 (V('essentials/conditional','v-if'),'Display a forbidden-state branch for 403 rather than repeatedly restarting login or replacing the protected screen with success data.'))
# Final knowledge-boundary and practice checks against the extracted row names.
# Minimum protocol and logging details stay in their own objectives.
data[96][3]=(L('session','regenerating-the-session-id'),data[96][3][1])
data[100][3]=('vue_docs#scaling-up/testing/mounting-libraries -> linked vuejs/test-utils documentation/guide/advanced/http-requests/#Asserting-loading-state','After triggering the request, assert the loading indicator before flushPromises; then await flushPromises() and assert the controlled successful or failed outcome.')
data[84]=data[84][:4]
data[98]=[data[98][j] for j in [0,3,4,6]]
data[91][1]=(data[91][1][0].replace('#Triggering-events','#Setting-element-values'),data[91][1][1])
data[91][3]=('vue_docs#scaling-up/testing/mounting-libraries -> linked vuejs/test-utils documentation/guide/essentials/forms/','Use expect(wrapper.emitted(eventName)[0][0]).toEqual(expectedPayload) to check the submitted payload emitted by the form.')
data[91][-1]=(V('scaling-up/testing','component-testing'),'Use expect(wrapper.find(selector).text()).toContain(expectedText) to verify the visible output after the awaited user interaction.')
data[105][-1]=('vue_router_docs#guide/advanced/meta/Route-Meta-Fields','A guard’s redirect can include query: { redirect: to.fullPath } to preserve the intended destination for the login flow instead of losing the protected route the user requested.')
data[112].append(('pinia_docs#core-concepts/state/Resetting-the-state','For an options auth store whose initial state is signed out, authStore.$reset() restores that initial state before directing an unauthenticated user back to login.'))
misconceptions={k:v for k,v in misconceptions.items() if k==32}

assert set(data)==set(range(len(C)))
R=json.loads((B/'registry_lookup.json').read_text())['lookups'];R={(x['concept_id'],x['path_id']):x for x in R}
rows=[]
for i,c in enumerate(C):
 lookup=R[(c['concept_id'],c['path_id'])];assert lookup['canonical_status']=='new'
 facts=[{'id':f'f{j}','statement':statement,'source_refs':([normalize('vitest_docs#api/mock/mockresolvedvalue'),normalize('vitest_docs#api/mock/mockrejectedvalue')] if ref=='vitest_docs#api/mock/mockresolvedvalue + mockrejectedvalue' else [normalize(ref)])} for j,(ref,statement) in enumerate(data[i],1)]
 mc=[{'id':f'm{j}','statement':statement,'source_refs':[normalize(ref)]} for j,(ref,statement) in enumerate(misconceptions.get(i,[]),1)]
 evidence={'concept_id':c['concept_id'],'required_facts':facts,'optional_enrichment':[],'misconceptions':mc,'created_in_batch_id':B.name,'used_by_path_ids':[c['path_id']]}
 objective=c['primary_objective'].rstrip('.');objective='Be able to '+objective[0].lower()+objective[1:]+'.'
 rows.append({'concept_id':c['concept_id'],'path_id':c['path_id'],'learning_objective':objective,'canonical_status':lookup['canonical_status'],'evidence':evidence})
inputs=['extracted_concepts.json','registry_lookup.json','concept_evidence_registry_snapshot.json','laravel_vue_full_stack_developer.source_pack.json']
meta={'artifact_type':'coverage_briefs','artifact_version':'1.0.0','schema_version':'1.0.0','batch_id':B.name,'run_id':B.name,'prompt_version':'03_coverage_brief@v1','model':'none','generated_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_snapshot_id':B.name,'parent_artifact_hashes':{name:hashlib.sha256((B/name).read_bytes()).hexdigest() for name in inputs}}
output={'metadata':meta,'batch_id':B.name,'briefs':rows}
(B/'coverage_briefs.part.all.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
print(len(rows),'briefs;',sum(len(r['evidence']['required_facts']) for r in rows),'required facts;',sum(len(r['evidence']['misconceptions']) for r in rows),'misconceptions')
