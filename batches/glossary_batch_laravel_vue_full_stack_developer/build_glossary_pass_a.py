import json, hashlib
from datetime import datetime, timezone
from pathlib import Path
P=Path('batches/glossary_batch_laravel_vue_full_stack_developer')
inputs=['coverage_briefs.json','extracted_concepts.json','depth_classification.json']
briefs=json.loads((P/inputs[0]).read_text())
extracted=json.loads((P/inputs[1]).read_text())
depths=json.loads((P/inputs[2]).read_text())
B={(x['concept_id'],x['path_id']):x for x in briefs['briefs']}
D={(x['concept_id'],x['path_id']):x['depth_tier'] for x in depths['classifications']}
C=extracted['concepts']
custom={}
def add(i, intro, example, contrast, level='HIGH', mode='annotated_code'):
    custom[i]=(intro,example,contrast,level,mode)

add(0,
"Suppose a supplied photo-management brief asks for a gallery, a way to add a photo, and a way to change or remove one chosen photo. Calling every operation ‘photos’ is not enough: the client and API need to agree which operation a request means. A CRUD endpoint contract records that agreement for a resource, an identified application entity.",
"Read the documented photos interface as a set of requests. GET /photos asks for the collection, whereas POST /photos asks to create a resource. Once a photo is identified, GET /photos/{photo} asks to read it, PUT/PATCH asks to update it, and DELETE asks to remove it. The braces mark the identified-resource position in this contract. For each supplied operation, write down the method, the collection or identified-resource URL, and the expected outcome together. Then add the required public success and non-success statuses from the exercise brief. A status in the 200–299 range communicates success, but that range alone does not specify the exact status your contract expects.",
"Do not infer the operation from the URL alone. The collection URL participates in both listing and creation; the method distinguishes those requests. Likewise, a successful status range does not replace an endpoint's specified success and failure outcomes.", 'HIGH','whiteboard_drawing')
add(1,
"You have received an existing Laravel project and need the dependencies its maintainers already resolved. This is a restoration task, not a request to choose newer versions. Composer separates the declaration of acceptable dependencies from the record of the exact versions chosen.",
"Imagine composer.json permits a range for a package and composer.lock records one exact version from that range. Run composer install to restore that locked project into vendor. If the task instead asks you to resolve dependencies again within the declared constraints, composer update changes the lockfile. Before choosing a command, state whether the required outcome is ‘restore these versions’ or ‘resolve versions again’.",
"Install and update are not interchangeable names for restoring a locked project. Update performs resolution and changes composer.lock; the fact that both concern dependencies does not make their outcomes the same.", 'MEDIUM','screen_demo')
add(2,
"A SPA screen needs a record containing a title, a nested owner record and an optional subtitle. A JavaScript object is the keyed container for that data. Understanding what a property contains, and what happens when a property is absent, is more useful here than memorizing a list of value names.",
"Picture an object with title set to ‘Harbour’ and owner containing another object with name set to ‘Mina’. Reading record.title selects the named property; if a variable key contains ‘title’, record[key] selects the same value. A subtitle deliberately assigned null is a different case from a property that has never been assigned: reading the latter gives undefined. Now suppose the record binding was declared with const. Assigning record.title to ‘Harbour at dusk’ changes a property of the existing object, not the binding itself. Assigning a new value to record would be reassignment of that binding. Keep those two actions distinct when tracing a screen's data.",
"Const does not freeze the contents of an object. Also, an absent property is not automatically null. Explicit null and an unassigned property communicate different states in this model.")
add(3,
"A supplied SPA project includes a manifest and lockfile. Your first task is to restore that project, while a later task might add a development tool. npm ci and npm install -D serve those different intentions.",
"For restoration, run npm ci against the existing locked project. If it reports that the manifest and lockfile disagree, treat that disagreement as the problem rather than expecting ci to rewrite them. To add a chosen development package, use npm install -D package-name, substituting the supplied package name. Once the dependency files have been updated, run npm ci to check that a clean restoration succeeds.",
"npm ci is not a way to repair the dependency files by silently rewriting them. It also removes an existing node_modules, so it is a clean-project restoration rather than an incremental addition.", 'MEDIUM','screen_demo')
add(4,
"A Laravel-side record might have a whole-number quantity, a decimal price, a text title, a yes/no flag and a missing optional value. PHP variables hold these values, and their types are determined at runtime. Start by separating the variable's name from the value currently assigned to it.",
"For a supplied item, assign $quantity = 3, $price = 12.5, $title = 'Harbour', $published = false and $subtitle = null. These represent an integer, a floating-point number, a string, a boolean and the null value respectively. Use var_dump($quantity) and var_dump($subtitle) to inspect both the value and its type rather than guessing from how a screen displays it. If you later assign $quantity = '3', the new value is a string: the quoted value differs from the earlier whole number even though their displayed characters can look alike. Each assignment gives the variable a current value; inspect that current value when reasoning about the application's input.",
"A missing value represented by null is not the same example as the string 'null'. Quotes make that example text. Nor should a value's printed appearance be treated as sufficient evidence of its runtime type.")
add(5,
"Before configuring authentication, identify the client. A first-party browser SPA and a third-party client need not use the same Sanctum mechanism. The choice here is between cookie-based Laravel sessions and bearer API tokens, not two names for one credential.",
"Consider a first-party SPA at app.example.test and an API at api.example.test. They share the same top-level domain, so choose Sanctum's cookie session model for this case. Contrast that with a mobile client or a third-party client: choose API tokens, sent as a bearer token in Authorization. Write the client type and chosen authentication model beside each supplied integration requirement. That small decision record helps keep subsequent implementation tasks aligned: the first-party SPA requirement is not a request to issue it a personal API token. This example chooses the model only; it does not yet configure the browser or the server's authentication boundary.",
"Do not assume every API client must use a bearer token simply because it calls an API. Sanctum's first-party SPA mode uses Laravel cookie-based sessions. Conversely, the stated SPA choice depends on the shared-domain requirement.", 'LOW','slides_with_signaling')
add(6,
"A supplied component sketch includes a title, a paragraph and an image. HTML markup expresses those elements and the information attached to them. Begin with the structure before adding framework behavior: opening tags, content, closing tags and attributes have different jobs.",
"For a paragraph, <p>Harbour</p> shows the ordinary opening-content-closing pattern. Attributes belong inside the opening tag, such as an element's class=\"caption\"; separate multiple attributes with spaces. For nested supplied elements, read the openings from the outside inward and close them from the inside outward. If a paragraph contains another ordinary element, that inner element closes before the paragraph does. Then inspect the image separately: <img> is a void element, so do not give it wrapped content and a matching closing tag. When reviewing a supplied page, check each ordinary element's pair, each attribute's position, and each nesting boundary. These checks concern markup structure, not what a later framework will do with the page.",
"Do not apply the matching-closing-tag pattern indiscriminately to void elements. Also, nesting is not merely having all the expected tag names somewhere in the file: overlapping pairs still violate the required structure.", 'MEDIUM','annotated_code')
add(7,
"A SPA has to choose one message from several supplied status cases. A conditional is an ordered decision: evaluate a predicate and run the corresponding branch, rather than running every message whose code appears nearby.",
"Imagine status is the number 200. In an if / else if / else chain, an initial predicate status === 200 selects the success body instead of its else alternatives. If the first predicate does not match, a later predicate can select another status message; else handles the remaining case. Now compare the number 200 with the string '200': === does not convert the unlike types to make that comparison match. For a decision that requires both a ready flag and a selected flag, combine boolean predicates with &&. Use || for alternatives and ! for negation. Trace the predicates in their written order, recording which body is selected for each supplied input, before reasoning about what the message should say.",
"An else-if chain is not a set of independent if statements. A matching if body runs instead of its else alternative. Also, strict equality does not turn a numeric-looking string into a number for comparison.")
add(8,
"A screen needs a reusable helper that works with state belonging to one enclosing operation. Functions provide parameters, local work and a returned result; nested functions can also use the enclosing function's variables. This explains how a callback can retain access to local state without a global variable.",
"Imagine an enclosing function has a local title value ‘Harbour’ and defines a callback helper inside its body. The helper can read that enclosing title. The enclosing function can pass the helper as an argument or return it as its result, because functions are values. A variable created only inside the helper remains in the helper's own scope; it does not become an enclosing variable just because the helper is nested. To trace a callback in supplied code, identify its parameters, then the variables in its own body, then the enclosing variables it reads. Separately identify the arguments passed when it is invoked and the result passed back by return. This keeps invocation inputs and captured local state from being confused.",
"Passing a function as an argument is not the same operation as describing a global variable. A callback can access its enclosing state, but its own local variables remain local to its scope.")
add(9,
"You need a controller artifact in a supplied Laravel project. Artisan is the project's command-line interface, so the first skill is choosing and checking the intended command rather than guessing a command from the artifact's name.",
"From the project, run php artisan list to inspect available commands. For controller generation, inspect php artisan help make:controller to see that command's arguments and options, then run php artisan make:controller PhotoController for the example artifact name. Read this as three separate actions: discover the command, inspect how to invoke it, then request the artifact. The command name identifies the operation, and PhotoController supplies the chosen controller name. When given a different development task, repeat the same discovery-and-help sequence for its command instead of reusing make:controller simply because it worked before. The learning target is command selection and invocation; the generated controller's later implementation belongs to a separate task.",
"Generating a controller artifact is not itself implementing its endpoint behavior. Keep the observable outcome here limited to the artifact the command generates.", 'HIGH','screen_demo')
add(10,
"On the PHP side, a supplied record has named fields and the response work may collect several results. PHP arrays cover both keyed record data and list-like data because an array is an ordered map. A value in that map may itself be another array.",
"Picture $record with 'title' mapped to 'Harbour' and 'owner' mapped to a nested array containing 'name' mapped to 'Mina'. Read the title through $record['title']; nested bracket access selects the owner's name through the outer and inner keys. Build keyed data with the key => value form, and list data with values in brackets. Now consider $result['title'] = 'Dusk': if the key already exists, this replaces its value; otherwise it inserts that keyed result. By contrast, $results[] = $record appends a value to the collection. Trace these as different operations: named lookup, named insertion or replacement, and append. The distinction helps you predict the resulting record or collection without treating every bracket expression as the same action.",
"The empty brackets in an append are not a named-field lookup. Nor does a nested array flatten itself into the outer record; access each level with the corresponding key.")
add(11,
"A supplied eligibility rule says a quantity must be above one boundary and at or below another, with a boolean flag also required. PHP operators turn those conditions into predicates. The important distinctions are the boundary itself, how conditions combine, and whether a comparison considers types.",
"For an example numeric quantity of 5, the conditions quantity > 2 and quantity <= 5 both match. Replacing <= 5 with < 5 changes the boundary case: 5 is no longer included. Use && when the rule requires both predicates, || when either is enough, and ! when a boolean decision must be negated. Parenthesize the intended combination so the grouped decision is explicit. Separately compare integer 5 with string '5'. Strict === requires equal values and types, so these are not strictly equal; !== recognizes a value or type difference. The loose operators == and != compare after type juggling. When tracing an eligibility rule, record the input values and types, check the numeric boundaries, then check the grouped boolean decision.",
"Do not describe === as merely checking whether two values look alike. Also, an inclusive boundary such as <= is not interchangeable with < when the input equals the boundary.")
add(12,
"A supplied page needs its caption elements styled consistently. A CSS class rule connects a named class in HTML to declarations in the stylesheet. The selector chooses the elements; the declarations describe the styling assigned to those matches.",
"Use the supplied class name caption as the connection point. The HTML element gets class=\"caption\", while the stylesheet rule begins .caption and contains the supplied property: value declarations inside braces, each ending in a semicolon. The leading dot belongs to the selector, not the class attribute's value. Class selectors are case-sensitive, so class=\"Caption\" is a different name from caption. Attach the external file with <link rel=\"stylesheet\" href=\"styles.css\">. Save the stylesheet and refresh the page to inspect the result. If the expected element is not styled, compare the class spelling in the markup with the selector before changing unrelated declarations. This example assumes the exercise supplies the desired property and value; choosing a whole visual design is not required here.",
"A rule's presence in a stylesheet does not by itself mean an element matches it. The class name must match, including case, and the external stylesheet must be attached.", 'HIGH','screen_demo')
add(13,
"A supplied form needs a title control and a submit button. Native form markup connects a visible label to its control and names the value that will be submitted. The id and name attributes serve different purposes.",
"For the title control, choose id=\"title-input\" and set the label's for=\"title-input\". Give the control name=\"title\" to identify its submitted value. Configure the form's supplied action and method for its submission destination and method, then use a submit button to submit those controls. Reviewing the form means checking both the label association and the submitted field name, not just whether the text box is visible.",
"Do not use id as a substitute for name. The label-to-control association can be correct while the submitted field still has the wrong name.", 'MEDIUM','annotated_ui')
add(14,
"A SPA receives an ordered list of records and needs a derived list for a screen. JavaScript arrays have zero-based positions and a length, but transforming them also requires understanding what each callback does to each element.",
"Suppose the supplied records have titles Harbour and Market. Index 0 identifies the first record and length reports the collection size. A map callback that returns each record's title produces a new array containing those titles. A filter predicate that matches only the Harbour record produces a new array containing that selected element. The source array need not be replaced to create either derived array. However, inspect the callback itself: if a map callback assigns a new title into the record object it receives, building a new result array has not prevented that object mutation. To keep source records unchanged, avoid such writes. Trace the result array and the source objects as separate things rather than assuming ‘new array’ answers every mutation question.",
"Map and filter do different jobs: one collects callback results, the other selects matching elements. A new mapped array is not proof that objects passed into its callback were left unchanged.")
add(15,
"A request-dependent step needs a result that is not available immediately. A promise represents eventual completion; async/await gives dependent statements a clear place to wait. The goal is to make the caller's completion track the work it actually depends on.",
"Imagine a supplied operation first obtains a record and then uses that record's title. Inside an async function, await the record operation before the dependent title step. If the awaited operation rejects, a surrounding try/catch can handle that failure; without a matching handling boundary, it propagates to the caller. Alternatively, a promise's .then handles fulfillment and .catch handles rejection. Now inspect the outer helper: starting dependent asynchronous work but neither returning nor awaiting it means the caller's completion no longer tracks that work. Trace the order as ‘start, await completion, use the result’, with a separate rejected path. Do not write the success-dependent step as though the promise itself were already the record.",
"Starting asynchronous work is not the same as completing it. Return or await dependent work, and do not treat a rejected operation as a fulfilled result just because the success statements appear next in the file.")
add(16,
"Two SPA modules need the same supplied helper. ES modules let one file export a binding and another import it. Read the export shape and import syntax together rather than treating every imported name as interchangeable.",
"If module.js exports a named binding called helper, a consumer uses import { helper } from \"./module.js\". The braces indicate a named import, and helper must be exported by that module. A default export is imported without braces and may receive a local name. When a supplied import fails to match its module, compare the path, whether the export is named or default, and the exported binding name before changing the helper's behavior.",
"A default import's local name does not make it a named import. Adding braces changes which kind of export the consumer expects.", 'LOW','annotated_code')
add(17,
"A Laravel test run must use the supplied project's testing configuration. Running the suite and diagnosing an environment mismatch are related but distinct tasks: one executes tests, while the other checks the settings those tests receive.",
"Run php artisan test or ./vendor/bin/phpunit and inspect the reported results. If the test environment does not match the exercise, compare the relevant phpunit.xml environment settings with the required testing configuration. Correct the mismatch there. When stale cached configuration would stop those settings from taking effect, run php artisan config:clear before repeating the tests. Use the next runner output to check the result rather than assuming an edited file has already changed the run.",
"A failing test result alone does not establish that the application behavior is wrong; the supplied testing environment may be mismatched. Check configuration evidence instead of guessing.", 'HIGH','screen_demo')
add(18,
"The same Laravel code is being prepared for a target production environment. Configuration selects environment-specific values; it should not turn the repository's example file or public error output into a place for credentials.",
"For a supplied target database, compare the connection, host, port, database and credential settings with config/database.php. Keep .env.example as a template with placeholders, not the target's real password. Remember that external environment variables can override .env values, so a file value alone does not settle which setting wins. Set APP_DEBUG=false for production so public error output does not expose sensitive configuration details. This is a configuration exercise, not a request to invent target credentials.",
"Do not assume .env always has the final say when external environment variables are present. Nor should real credentials be copied into .env.example for convenience.", 'MEDIUM','screen_demo')
add(19,
"A PHP operation needs one of several supplied outcomes. An if / elseif / else chain expresses an ordered choice. Trace it by asking which condition first evaluates to true, not by reading every branch body as work that will run.",
"Suppose the first condition is false and the next elseif condition is true for a supplied record. The elseif body is selected because the earlier branch did not match. If the first condition is true instead, its body runs and the later alternatives are not selected. If none of the preceding conditions is true, else supplies the remaining outcome. For each supplied input, mark the tested conditions and the selected body.",
"Else is not another independent action that always follows if. It handles the case in which the preceding alternatives do not execute.")
add(20,
"A PHP helper should accept a particular kind of input and return a particular kind of result. A typed function makes that contract visible at the parameters and return declaration. Runtime values still matter: a type declaration is not simply documentation that can be ignored.",
"Consider a supplied helper with an int input and an int return contract. Its declaration follows function name(int $input): int, and return passes the result to the caller and ends the function. If the contract allows a missing integer, ?int permits int or null. Now check the file making the call: scalar types can be coerced by default, while declare(strict_types=1) enables strict scalar typing for calls from that file. Preserve the documented exception that an int is accepted for a float declaration. To review a helper, record the input contract, whether null is permitted, the calling file's scalar-typing mode, and the return value. An untyped function with no returned value returns null; that is a different case from a declared int result.",
"Do not claim strict scalar typing means every numeric type combination is rejected: int is accepted for float. Also, return is not merely a label on the result; it ends the function's execution.")
add(21,
"A supplied maintenance task should run on a schedule. The declaration names the work and its due times; inspecting the schedule helps you check whether those due times match the requirement.",
"Declare the callable through Schedule::call(callback) in routes/console.php. For a task intended daily at midnight, chain ->daily(); for one intended every minute, use ->everyMinute(). Run php artisan schedule:list and compare the task's next due time with the supplied requirement. Keep the callback's supplied work separate from the frequency choice so changing the frequency does not obscure which operation is being scheduled.",
"The schedule declaration describes due times. Do not confuse inspecting that declaration with proving the server's execution trigger is operating; that trigger is a separate concept.", 'MEDIUM','screen_demo')
add(22,
"Production needs useful failure evidence without exposing internal details to the user. Laravel logging channels decide where configured messages go, and a channel's level decides the minimum severity it records.",
"For a supplied logging requirement, inspect config/logging.php and identify the selected channels in the default stack. Compare each relevant channel's level with the severity of the failure messages the task requires. Keep APP_DEBUG=false so collecting internal evidence does not turn public errors into sensitive configuration output. If adding contextual information to a message, exclude sensitive data; the same caution applies to exposing internal logging events to users.",
"Turning off public debug output is not a reason to log secrets instead. Logging and public error display are different boundaries, and both can leak sensitive information.", 'MEDIUM','screen_demo')
add(23,
"A PHP collaborator has its own state and behavior. A class describes those properties and methods; creating an instance gives you an object on which to invoke the behavior. Keep the class description, constructor inputs and current instance distinct.",
"Imagine a supplied helper class accepts a title when created with new ClassName(...). Its __construct method can initialize a title property from that argument. Inside an instance method, $this refers to the current object, and $this->title accesses that object's property. Outside the object, $object->method(...) invokes the method on the created instance. Trace a second instance with a different constructor title separately: when its method refers to $this, the current object is that second instance, not the first. To follow collaborating code, locate the creation, note the constructor arguments, then follow the instance method call and the properties it accesses. This connects state initialization to behavior without treating a class name itself as the current object.",
"A constructor argument and a property are not automatically the same variable. The constructor initializes state, and $this identifies the instance whose state an instance method accesses.")
add(24,
"A supplied PHP array contains values that need to contribute to a summary. Foreach visits its elements, letting the loop body update an accumulator. Decide whether the body needs only each value or also its key.",
"For a two-element array with numeric values 2 and 3, initialize a numeric total before the loop. In foreach ($array as $value), the body adds the current value, yielding a total of 5 after both visits. If a result must retain each named key, use foreach ($array as $key => $value) instead. The ordinary value form assigns the current value to the loop variable; it does not make that variable a reference to the original element. Trace the accumulator across visits rather than reinitializing it in the body.",
"Initializing the accumulator inside the body defeats the intended across-element summary. Also, do not read ordinary value iteration as a reference-based update of the source array.")
add(25,
"A supplied Vue test project is ready to run, but component tests require an environment appropriate to DOM work. Learn to read the runner's result and its configuration together.",
"Use npx vitest run for a single execution, or npx vitest to discover and execute the supplied tests. Vitest defaults to node; for the documented component-testing setup, configure test.environment as jsdom. If a test fails, start with the reported file and assertion, then compare the environment with the test's browser-like DOM requirements. The exercise supplies the tests and setup, so do not infer success merely because the runner started.",
"A default node environment is not the same as jsdom. Starting Vitest and obtaining passing component assertions are separate observations.", 'HIGH','screen_demo')
add(26,
"A SPA screen component needs JavaScript bindings, markup and possibly styling. A Vue single-file component keeps these roles in one .vue file without making the three sections interchangeable.",
"In a supplied PhotoCard.vue, place component bindings in <script setup>, markup in <template> and any CSS in <style>. A title declared at the top level of script setup is available to the template. When reviewing the file, follow a supplied title from its script declaration to the template that uses it, while keeping CSS declarations in the style section. This is a file-structure and binding-visibility model; reactive updates and particular template directives have their own explanations.",
"Putting markup into the script section does not give it the template section's role. The file combines distinct blocks rather than erasing the difference between JavaScript, template markup and CSS.", 'MEDIUM','annotated_code')
add(27,
"Several SPA operations need to send JSON through one request interface. A shared fetch wrapper centralizes that request construction and returns asynchronous work that its callers can await. Match the method and body to the supplied endpoint operation.",
"For a supplied read operation, call fetch with the URL and no body; GET is the default method. For a JSON create operation, choose POST, set Content-Type to application/json and serialize the supplied payload with JSON.stringify into options.body. When the response is expected to contain JSON, await response.json() and return the parsed data. Trace the wrapper as request construction, asynchronous response, then expected-body parsing. Its caller should receive the returned asynchronous result rather than a helper that starts work and forgets to return it.",
"Do not attach a request body to GET. Also, parsing an expected JSON body is not an explanation of how every failure is handled; response failure handling is a separate boundary.")
add(28,
"A supplied user record needs password storage and later password verification. Laravel's hashing services separate the input password from the stored hash. Verification compares a candidate password with that hash; it does not need to recover the original password.",
"For an example input password supplied only for the exercise, store Hash::make($password), not the input itself. During verification, pass the candidate plaintext password and the stored hash to Hash::check($plainText, $storedHash). Read the result as whether that candidate corresponds to the stored hash. Laravel supports Bcrypt and Argon2 for this storage task. Keep the stored representation and the submitted candidate distinct when following the data through supplied code.",
"A password hash is not a plaintext password to display later. The verification model does not require recovering the original password from it.", 'LOW','annotated_code')
add(29,
"A browser request failed somewhere between reaching Laravel and receiving the final response. The HTTP lifecycle is a sequence of boundaries for locating that failure, not just a jump straight from URL to controller.",
"Trace a supplied request from the HTTP entrypoint that creates the application into request handling. Routing dispatches it to the route or controller with the assigned middleware applied. If a middleware check rejects it, the handler is not reached. If the request passes those checks, the handler's response travels back through the middleware chain before the final response goes to the browser. Draw those stages for the same request and mark which stage the supplied evidence shows it reached. An observed response may have come from a request check rather than the intended handler, so do not assume every response proves handler execution.",
"A route's existence is not evidence that a particular request passed its middleware. Keep dispatch, request checks and response return distinct when reading a failed trace.", 'HIGH','diagram_animation')
add(30,
"A scheduled task declaration needs a server trigger to evaluate due work. Laravel's schedule runner performs that evaluation against the current server time. Operating the trigger is different from writing the declaration.",
"Use the documented cron entry from the project directory, replacing /path-to-your-project with the supplied path. It invokes schedule:run every minute. First inspect schedule:list for the next due time of the supplied task; then observe schedule:run at a due time. Compare those observations: one establishes the declaration's due time, while the other shows evaluation and execution of due work. The trigger's every-minute invocation does not change a daily task into an every-minute task.",
"Do not confuse how often cron invokes the runner with how often every task is due. schedule:run evaluates the declared schedule against server time.", 'HIGH','screen_demo')
add(31,
"A supplied relational change needs an explicit application step and a reversal. A migration's up and down methods express those operations. Think in terms of the resulting table and relationships rather than treating a migration as an arbitrary script.",
"For the documented posts-to-users reference, foreignId(\"user_id\")->constrained() expresses the foreign key constraint. For a table declaration, Schema::create with a Blueprint callback can include id() and string(columnName). Place the forward schema operations in up and their reversal in down. Run php artisan migrate to apply outstanding migrations. Before using migrate:rollback, identify the latest migration batch: that reversal may cover several files, not just the one you most recently opened. Trace the resulting schema forward and backward against the supplied change specification.",
"Rollback targets the latest batch, not necessarily one migration file. Also, a foreign key constraint is an integrity rule, not merely a similarly named column.", 'HIGH','screen_demo')
add(32,
"A PHP service operation can fail before producing its ordinary result. Exceptions transfer control to a matching caller boundary. Understanding that transfer helps you avoid continuing the success path as though the failed operation had returned normally.",
"Imagine a supplied service call inside try throws an exception. Ordinary execution is interrupted and the throwable moves through callers until a matching catch is reached or it reaches global scope. A catch for the intended exception type handles that failure at the boundary; a catch for a nonmatching type does not. A finally block runs as control leaves its try/catch boundary, including when the throwable continues propagating. Trace the success and thrown paths separately, marking which catch matches and where finally runs. If no matching catch is reached, the uncaught failure goes to an exception handler or terminates the program rather than becoming a normal result.",
"The presence of some catch does not mean every throwable is handled there. Matching the throwable type matters, and finally can run even when failure propagates onward.")
add(33,
"A caller should work with either of two supplied collaborator implementations. A PHP interface names the public behavior both must provide, letting the caller depend on the shared contract rather than a particular class.",
"For a supplied Adapter contract, declare the required public method signatures in an interface. Each implementing class uses implements and provides compatible signatures. Type the caller's dependency with that interface. Now substitute the second conforming adapter: the caller still requests the same interface behavior even though the implementation changes. Review compatibility at the methods and signatures, not merely at whether the two classes have similar names.",
"A class that happens to sound like an adapter is not thereby an implementation of the interface. The declared contract and compatible public methods establish that relationship.", 'MEDIUM','whiteboard_drawing')
add(34,
"A supplied PHP file refers to classes with short names, aliases and absolute names. Namespaces and use imports explain which class each reference means. Resolve names from the file's declarations before deciding that a class is missing.",
"If the file imports Full\\ClassName as Alias, Alias resolves to that fully qualified class in that file. Without the alias, use Full\\ClassName makes ClassName available as the short name. A name beginning with a backslash is already absolute and is not redirected by those imports. Separately, the namespace declaration places names declared in the file inside that namespace. Trace each supplied reference with the file's own namespace and imports; do not copy another file's alias interpretation into it.",
"An alias is a local name-resolution choice in the importing file, not a change to the class's fully qualified name. Absolute names remain absolute despite imports.", 'LOW','annotated_code')
add(35,
"You need to inspect an edit in a supplied standalone SPA during development. Vite provides a development server whose entrypoint is the project's root index.html and whose module updates support the edit-check loop.",
"Run npx vite, or npm run dev when that supplied script invokes vite. Use the URL printed by the running project; http://localhost:5173 is the documented development URL, not a reason to ignore the actual output. Edit a supplied module and inspect the update in the running page. Hot module replacement updates edited modules without requiring a full page reload. Keep this development workflow distinct from producing and hosting a production bundle.",
"Do not treat root index.html as a passive public file in this model. Nor should the documented port replace the URL actually printed by the project.", 'HIGH','screen_demo')
add(36,
"A component registers a listener after its initial DOM exists. That side effect needs a lifetime tied to the component, including cleanup when the component goes away. Vue lifecycle hooks provide those boundaries.",
"Register the supplied listener in onMounted and remove that same listener in onUnmounted. Track the identity of the listener in the supplied scaffold so removal corresponds to what was registered. Register the hooks synchronously during setup, when Vue can associate them with the active component instance. Read the lifetime as setup registration, mounted work, then unmounted cleanup rather than as unrelated calls.",
"Removing a different listener does not express the required pairing. Also, registering lifecycle hooks later is not the stated synchronous-setup pattern.", 'HIGH','diagram_animation')
add(37,
"A Vue screen must keep a changing title or record connected to its template. Reactive state is that connection, but ref and reactive have different access and replacement rules. Choose the representation before tracing an update.",
"For a title ref created with ref('Harbour'), script reads and updates use title.value. A top-level ref exposed to the template is unwrapped there, so ordinary template access uses title without .value. For a record created with reactive(object), tracked property reads and writes go through the returned proxy. Now imagine destructuring its primitive title property into a local variable: that local value is disconnected from the original tracked property. Similarly, replacing the reactive object breaks the original connection. Follow the same screen value through creation, script access, update and template access, and distinguish a tracked property write from a disconnected local assignment.",
"Reactive is not a representation for a primitive value. Also, ref script access and template unwrapping are different contexts; do not remove .value everywhere just because the template normally omits it.")
add(38,
"A SPA has supplied list and detail screens. Vue Router connects route paths to component rendering and allows navigation without reloading the whole page. The router must be installed before that rendering connection is used.",
"Configure the supplied path-to-component records in createRouter({ history, routes }). Install the router with app.use(router) before mounting the application and place RouterView where the matched component should render. A RouterLink whose to is /photos navigates to that destination without a whole-page reload. For a supplied action requiring navigation in code, router.push(destination) performs the programmatic move. Trace one destination from its configured route record to RouterView, then compare clicking a RouterLink with invoking router.push: both express navigation, while the path-to-component configuration determines the matching screen.",
"A route record alone is not the entire setup: the router must be registered and the matched component rendered through RouterView. Host behavior on direct nested URLs is a separate deployment concern.", 'HIGH','screen_demo')
add(39,
"A SPA request may fail to travel successfully, or it may reach the server and receive a non-success HTTP response. Fetch handles those differently. Separating them is essential before the screen treats a body as successful data.",
"Compare two supplied cases. In one, fetch receives a 404 response: the promise fulfills with a Response, so inspect response.status or response.ok before choosing the success path. In another, a transport operation rejects: try/catch around awaited fetch handles that rejected path. Body reading can also reject and belongs inside the relevant boundary. For an expected 422 JSON response, identify the status and parse its error body for the caller; do not relabel it as a rejected network request. Trace the decision as ‘did the operation reject, or did a Response arrive?’, then ‘is the received HTTP outcome successful?’, and finally the expected body handling.",
"A non-success HTTP status does not by itself make fetch reject. Conversely, receiving some response body does not establish success: ok represents the 200–299 status range.")
add(40,
"A supplied PHP class has a namespace and a location under src. Composer's PSR-4 mapping connects the namespace prefix to that directory so the generated autoloader can find the class.",
"Use the documented example: Foo\\ mapped to src/ makes Foo\\Bar\\Baz resolve to src/Bar/Baz.php. The prefix has already been mapped to src, so do not add another Foo directory under it. After changing composer.json's autoload.psr-4 configuration, run composer dump-autoload. Include vendor/autoload.php to use the generated loader. Compare the declared prefix, remaining class-name segments and resulting file path as three parts of one resolution.",
"The mapped namespace prefix is not repeated in the remaining path. Also, changing the mapping and regenerating the autoloader are distinct steps.", 'MEDIUM','annotated_code')
add(41,
"A Laravel operation receives attributes for a stored record. Eloquent supplies create, retrieval, update and deletion operations, but mass assignment also needs an explicit choice about which submitted attributes may be applied.",
"Suppose the supplied record has an editable title and a protected ownership field. Include title in $fillable and keep the protected field out. Model::create($attributes) inserts and returns a model using the permitted mass-assignment attributes. For an existing model retrieved by Model::find($id), fill applies allowed input to the instance and save persists the changes. Calling delete on the model removes its stored record. Trace the update in two stages: the instance receives permitted attributes, then the instance's changes are saved. If the input unexpectedly contains the ownership field, the allowlist should not grant that field permission merely because it arrived in the submitted array.",
"Fill and save are different operations; applying attributes to an instance is not the same step as persisting it. Mass assignment should not include protected fields simply to accommodate unexpected input.")
add(42,
"An endpoint contract needs an actual Laravel route for its method and path. The route declaration connects that request shape to a handler, and route:list gives an observable way to check the registration.",
"For a supplied read operation, choose Route::get and provide its path and handler; use the corresponding method-specific declaration for create, update or delete. A handler can be a controller class and action pair. In routes/api.php, a declaration for /user is addressed as /api/user because of the default prefix. Run php artisan route:list and compare the registered method, URI and action with the supplied contract. Trace the public URL through the prefix and the declared path before changing the controller: a path mismatch can be visible in route registration itself.",
"Do not repeat the default /api prefix as though a route declaration and its public URL were necessarily identical. Also, a correct action name does not compensate for a wrong method or URI.", 'HIGH','screen_demo')
add(43,
"A supplied operation should queue work outside the request rather than run it immediately. A job's structure defines the input and work, while the selected queue connection determines whether dispatch leaves asynchronous work pending.",
"Generate the supplied job with php artisan make:job JobName. The generated ShouldQueue job takes its input through the constructor and performs its work in handle. Dispatch with JobName::dispatch($input)->onConnection(connectionName), using the supplied asynchronous connection. Observe whether dispatch leaves work pending instead of doing it during the request. The sync connection is a useful contrast: it executes immediately. Keep three questions separate when tracing the operation: what input enters the constructor, what work handle contains, and which connection receives the dispatch.",
"A queued-job class does not make the sync connection asynchronous. Verify the selected connection and pending-work outcome instead of inferring deferred execution from the class name.", 'HIGH','diagram_animation')
add(44,
"A standalone SPA needs a public API address selected for its build. Vite exposes appropriately prefixed environment values to client code, so those values must be safe for the client to contain.",
"Declare the supplied address as VITE_API_URL and read import.meta.env.VITE_API_URL. If another custom value contains the text ‘false’ or ‘10’, remember that custom environment values are strings. VITE_ values are embedded at build time; do not put a password or private API key beside the public address. Review each value by asking whether it belongs in delivered client code, not merely whether storing it in an environment file feels private.",
"A VITE_ name is not a secrecy boundary. Nor does numeric-looking or boolean-looking text automatically become a number or boolean.", 'LOW','annotated_code')
add(45,
"A screen needs a total derived from its selected records. Computed state expresses a result calculated from reactive inputs, with caching until tracked dependencies change. The getter's job is calculation, not changing the source or performing a request.",
"Suppose selected records contribute amounts 4 and 6. Inside the computed getter, select the contributing records with filter, initialize a local total, traverse them with for...of, add each amount and return 10. The computed result is a derived ref. If a tracked contributing value changes, the cached result can change with that dependency; unrelated work should not be smuggled into the getter. To review the supplied total, trace selection first, then each addition and the returned result. Keep the local accumulator separate from the source records: calculation should not rewrite the amounts being totaled.",
"Computed is not a place for an asynchronous request or a source-state mutation. Caching also does not mean the result is fixed forever; tracked reactive dependency changes invalidate it.")
add(46,
"Two components need the same pattern of stateful behavior, but not necessarily the same state instance. A composable packages reusable Composition API behavior in a function. Its call boundary matters for ownership.",
"Export a use-prefixed function that creates its refs and behavior, returns state and actions, and is called from each consumer's setup. Imagine two edit panels calling it separately: refs created inside each call can belong to that call, giving the panels isolated state. Trace one panel's returned state and actions separately from the other panel's call. Reuse here means reusing the behavior's definition; it does not by itself require both panels to share every value.",
"A reusable composable is not automatically a global shared store. Refs created inside separate calls can remain isolated.", 'MEDIUM','whiteboard_drawing')
add(47,
"A Vue template needs a changing caption and a changing attribute. Text interpolation and attribute binding connect those different output positions to component values. Use the syntax for the output position you actually need.",
"For a caption, {{ title }} renders text and updates when title changes. For a dynamic attribute, use :attribute=\"value\" or the full v-bind form, not mustaches inside an attribute. If a bound ordinary attribute value is null or undefined, the attribute is removed. For disabled, the boolean-attribute rule includes it for a truthy value or an empty string and omits it for other falsy values. Trace the supplied value through its output rule, checking attribute presence separately from text content.",
"Mustaches inside an HTML attribute are not a replacement for v-bind. Also, boolean-attribute presence has its stated rule; do not generalize it from how a text value looks.")
add(48,
"A stored model value may need a different application-facing representation. Eloquent attribute casts declare that conversion per attribute. Read the application-facing value and database representation as separate concerns.",
"For the documented is_admin field, a boolean cast turns stored 0 and 1 into boolean values when accessed. Define the mapping in casts(): array. If the attribute is null, it is not cast. For a supplied date attribute, date or datetime casts provide date objects to the application and convert supported assigned date representations for storage. When reviewing a date contract, distinguish its serialization format from its storage format: specifying one does not itself specify the other.",
"Do not infer the database date storage format solely from the cast's serialization format. Also, null attributes are not converted by these casts.", 'MEDIUM','data_table_demo')
add(49,
"A Laravel operation needs only matching records in a specified order. Build those constraints on the query before retrieving the collection instead of loading every model and then deciding what was wanted.",
"For a supplied list, add an equality predicate with where(column, value), then another required predicate with where(column, operator, value). Ordinary chained where clauses require both to match. Choose orderBy(column, 'desc') for descending order or 'asc' for ascending order, which is the default. Call get after the constraints. Trace a small supplied set of rows through each predicate, then sort the survivors, to predict the returned models.",
"Chained ordinary where predicates are not alternatives. Also, get is the retrieval step, so putting it before the intended constraints does not express the described constrained query.")
add(50,
"A development database needs a supplied baseline dataset. A seeder describes those insert operations and can be included from DatabaseSeeder. Choose the target database and command before rebuilding data.",
"Generate the dataset seeder, put the intended inserts in run and include it through $this->call([SeederClass::class]) when it belongs in DatabaseSeeder. Run db:seed for the configured seed set or db:seed --class=SeederName for the supplied seeder. If the task explicitly calls for rebuilding the development database, migrate:fresh --seed drops tables, reapplies migrations and seeds data. Treat that destructive rebuild as a different operation from ordinary seeding.",
"migrate:fresh --seed is not a harmless synonym for db:seed. Its table-dropping behavior must match the intended development task.", 'HIGH','screen_demo')
add(51,
"An API create request needs its fields checked before controller work begins. A form request holds the field rules and is injected into the action to perform that validation. Work backward from the supplied field requirements rather than accepting every input shape.",
"For a supplied title that must be present, text and within a character limit, combine required, string and the specified max rule. For an optional field that permits null, nullable handles that permitted value. Generate the request with make:request and return these mappings from rules; type-hint it in the action so validation precedes action execution. If this request handles validation only and authorization is handled elsewhere, return true from authorize or remove that method. For a request expecting JSON, a failure produces 422 with message and field-to-message-list errors. Trace valid and invalid supplied payloads separately: an invalid required title should yield field feedback, not be treated as an accepted action input.",
"Max is interpreted according to the field type, including character length for strings. Do not assume nullable means a required field may simply be omitted; the rules need to match the supplied requirement.")
add(52,
"A Laravel handler must return both the specified JSON data and the specified HTTP outcome. A response contract includes those two parts and may also require headers for metadata outside the body.",
"Build the supplied public body as an array and return response()->json($data, $status). The helper serializes JSON and sets Content-Type to application/json. If the contract calls for a status other than the default 200, supply it explicitly. Review a response by comparing the JSON fields, status and any required headers separately; a correct body does not settle the status.",
"Do not rely on default 200 when the endpoint specifies another outcome. Required response metadata outside the JSON body belongs in headers rather than being assumed from the body's fields.", 'LOW','annotated_code')
add(53,
"A protected route has a request check that should stop unsuitable requests before the handler. Middleware can either return its own response or let the request continue. This is an execution boundary, not merely a label on the route.",
"In the supplied middleware's handle method, trace the rejected case to its own response and the accepted case to $next($request). Assign the middleware to the route, or use Route::middleware([...])->group(...) for several routes needing the same checks. For each route in the group, follow the same acceptance or rejection decision. A response returned at this boundary means the protected handler was not reached. Draw the two paths before interpreting a handler-side observation: only the continuing path reaches that later work.",
"An assigned middleware does not always call the handler. Returning its own rejection response ends handling at that boundary.", 'HIGH','diagram_animation')
add(54,
"A supplied development or test task needs model records with known attributes. Factories define a default attribute set and allow overrides. Choose whether the task needs an instance only or a persisted record.",
"Generate and associate the factory with the intended model, then define defaults that satisfy its data requirements. Model::factory()->make() gives an unpersisted instance, while create persists it. For a case requiring three stored records, count(3)->create() expresses that count. Use explicit overrides for attributes the exercise needs to control, rather than relying on defaults to happen to represent the desired case.",
"Make and create do not have the same persistence outcome. A model instance existing in the test's variables is not proof that its record was stored.", 'MEDIUM','annotated_code')
add(55,
"Deployment can cache Laravel's configuration and registrations. Those caches affect how later configuration and route changes are observed, so deployment work must include the appropriate rebuild or clearing behavior.",
"Use optimize for the documented production optimization caches. If routes change after route:cache, rebuild that route cache. With config:cache, read configuration through the intended configuration files rather than assuming ordinary .env reads elsewhere still load values. view:cache precompiles Blade views; this path notes that operation without teaching full Blade authoring. Before optimize:clear, note that it removes optimization caches and clears keys in the default cache driver too. Match the cache operation to the supplied deployment change.",
"optimize:clear affects more than a route cache alone. Also, cached configuration changes the stated behavior of .env reads outside configuration files.", 'HIGH','screen_demo')
add(56,
"An asynchronous connection contains pending jobs that a worker must consume. Operating a worker includes choosing the connection and accounting for its long-lived process when code changes.",
"Run php artisan queue:work connectionName for the supplied connection. For a verification task that should process one available job and exit, use --once. After a code change, queue:restart asks a long-lived worker to exit after its current job; it does not itself provide the process manager that restarts it. Check that a process manager restarts exited workers and that a functioning cache driver can deliver restart signals. Observe consumption separately from dispatch.",
"A running long-lived worker does not notice new code automatically. Also, asking it to exit and ensuring it is restarted are different operational responsibilities.", 'HIGH','screen_demo')
add(57,
"A supplied operation makes two related database writes that must succeed together. A transaction puts both inside one success-or-failure boundary, preventing the first from being committed independently when the second fails.",
"Wrap both writes in the same DB::transaction callback. Trace two cases: if the callback completes, the transaction commits automatically; if the second write throws, the database changes are rolled back and the exception is rethrown. The important placement is that the first write is also inside the callback. Keeping it outside would not express the stated paired-write guarantee. Follow the supplied records before and after each case rather than treating ‘transaction’ as an unexplained safety label.",
"A transaction rollback does not silently swallow the exception: it is rethrown. Nor does wrapping only the second write protect a first write made outside the shared transaction.", 'HIGH','diagram_animation')
add(58,
"A route identifies one model and the action needs that model instance. Implicit binding links the route segment name to a matching type-hinted action parameter, with a defined missing-model outcome.",
"Read /users/{user} together with User $user: the segment and variable name match, and the parameter resolves the user whose primary key matches the requested value. If no matching user exists, binding returns 404 rather than passing a nonexistent model into the action. For the supplied slug case, {post:slug} selects the specified column instead of the default key. Trace the segment, action parameter and lookup key as one contract.",
"A model type hint alone is not the full implicit-binding condition; the variable name must match the route segment. Binding by slug is an explicit departure from the default key.")
add(59,
"A relative request in a standalone SPA initially targets the frontend origin. A development proxy can forward matching paths to Laravel, but its prefix and rewrite behavior must preserve the backend URL you intend.",
"Suppose the client requests /api/photos. Compare the configured server.proxy prefix and backend target with the registered Laravel path. If a rewrite removes /api while the backend expects it, the forwarded URL no longer matches that route. If the backend expects a path without the prefix, retaining it can cause the opposite mismatch. Check the request method and endpoint against route:list, then inspect the forwarding rule. This follows the actual path transformation instead of assuming a relative URL automatically addresses Laravel.",
"The frontend origin is not automatically the API server. A proxy's target alone is also insufficient evidence of correctness when a rewrite changes the path.", 'HIGH','whiteboard_drawing')
add(60,
"The SPA needs deployable output, not the development server's edit loop. Vite's build starts from index.html and produces a production bundle that can be checked locally before deployment.",
"Run npm run build when the supplied script invokes vite build, then inspect the default dist output. Run npm run preview when its script invokes vite preview to serve that built output locally. Compare the previewed result with the supplied acceptance requirement. Keep ‘produce the bundle’, ‘preview the bundle’ and ‘host production’ as separate activities: preview verifies built dist locally but is not a production hosting server.",
"Do not deploy by treating vite preview as the production server. It is a local preview of the already built output.", 'HIGH','screen_demo')
add(61,
"A particular reactive value should trigger a supplied persistence side effect. Watch lets you name that source and put the side effect in a callback, without mixing persistence into a computed calculation.",
"For a ref, pass the ref as the watch source. For one reactive object's property, pass a getter such as () => object.property, not its current primitive value. Keep the source limited to the state that should trigger persistence. Watch is lazy by default; add immediate: true if the callback should also run at registration. A watcher created synchronously in setup stops with its component, and its returned stop function permits explicit stopping. Trace the initial registration and a later source change separately to check the intended callback timing.",
"Passing a primitive property's current value does not express a getter that follows that property. Also, a lazy watcher does not automatically run its callback at registration.")
add(62,
"A component button should change reactive state when a user acts. An event binding connects the DOM event to the handler; a tracked state update then changes the component value.",
"Bind a supplied click handler with @click=\"handler\" or v-on:click=\"handler\". A named handler receives the native event object. If it updates a ref in script, use .value for that update. For a small template-only update, the documented @click=\"count++\" form is an inline expression. Follow the sequence event, handler, state change rather than assuming the handler ran just because its name appears in the template.",
"A method handler's native event argument is not automatically an application record. Also, script-side ref updates still require .value.", 'MEDIUM','live_code')
add(63,
"A child component displays a title owned by its parent. Props provide readonly input to that child. This preserves a clear direction for data flow even when the parent's value changes.",
"Declare the child input with defineProps in script setup and pass the parent's changing title through :title=\"value\". A literal title attribute supplies a static string instead. Read the prop in the child rather than assuming a local copy of its initial value will follow later parent updates. If a prop is an object or array, its nested references are still exposed; avoid using those references to change parent data from inside the child. Trace ownership from parent value to readonly child input, separating that input from any genuinely local state.",
"Readonly props do not make nested object references disappear. A local copy of an initial prop is also not a subscription to future parent changes.")
add(64,
"A screen should show one of several supplied branches. Vue's v-if family controls whether subtrees exist, whereas v-show keeps an element in the DOM and changes its display. Choose based on the required rendering behavior.",
"Place v-else-if or v-else immediately after its conditional sibling. For an initially false v-if branch, creation is lazy; switching it has higher toggle cost. v-show has higher initial render cost but cheaper toggles because the element remains in the DOM. Trace a supplied flag from false to true and back, noting whether the subtree is created and destroyed or merely hidden and shown.",
"Hidden with v-show is not the same state as an absent v-if subtree. Also, a separated v-else sibling is not the required adjacent branch structure.", 'HIGH','annotated_ui')
add(65,
"A list can reorder while its items contain temporary input or child state. Keys give Vue an item identity for node reuse, rather than leaving that temporary state attached to the wrong position.",
"Render the supplied records with v-for=\"item in items\" and :key=\"item.id\", where each id is unique and stable. Imagine Harbour and Market reverse positions. The keys let Vue reuse and reorder nodes by record identity; default in-place patching without identity keys can leave temporary state with the wrong item. Use primitive string or number keys, not whole record objects. Trace which record owns each temporary input before and after the reorder.",
"A position is not the stable item identity this example needs. Nor should the entire object be used as the key when the stated key types are primitive strings or numbers.", 'HIGH','diagram_animation')
add(66,
"A supplied record contains user-authored text that happens to look like markup. The screen should display that text without treating it as instructions to insert raw HTML or form a component template.",
"Render the untrusted value through {{ value }}. Vue text interpolation escapes HTML content, so markup-like input is treated as text. If supplied code uses v-html for that input, replace raw insertion with interpolation. v-html inserts raw HTML and can expose users to markup injection. Keep the content as data rather than using it as a component template, which permits arbitrary JavaScript execution.",
"Markup-like text is not a reason to enable v-html. Never use untrusted content as a Vue component template.", 'MEDIUM','annotated_ui')
add(67,
"An API form submitted invalid fields and needs structured feedback. Laravel's JSON validation response distinguishes a general message from the errors mapping keyed by field, giving consumers a predictable field-error contract.",
"Enforce the supplied rules with $request->validate($rules). For a request expecting JSON, validation failure returns 422 with message and errors. A title error is an array of messages under its field key; nested field keys use dot notation. If the exercise specifies a custom contract, construct that required mapping and return response()->json($body, 422). Review the status and field-to-message arrays together rather than accepting a generic error string as equivalent.",
"The errors entry for a field is a list of messages, not the same thing as the overall message. A custom body still needs the specified 422 status and mapping.", 'LOW','data_table_demo')
add(68,
"A parent can have several related child records. In an Eloquent one-to-many relationship, the child's foreign key connects each child to its parent, and the model methods describe both directions of access.",
"Use the documented Post and Comment example. A parent method returning hasMany describes its comments, while the child's belongsTo method describes its post. comments.post_id matches posts.id. Accessing $post->comments retrieves the comments related to that post; $comment->post retrieves the parent matching that comment's foreign key. Supply a custom foreign key when conventions do not match the supplied schema. Trace the same comment through its stored foreign key in both directions rather than assuming every comment belongs to every post.",
"The inverse relationship is not another collection of parents for this one-to-many example. It resolves the parent matching the child's foreign key.", 'HIGH','whiteboard_drawing')
add(69,
"A query needs a submitted search value without allowing that value to become query structure. Parameter binding keeps values separate from SQL structure, but it does not provide the same mechanism for column names.",
"Pass a supplied search value to where(column, operator, $value). If raw SQL is necessary, the documented whereRaw(\"column = ?\", [$value]) supplies the value as a separate binding rather than interpolating it. Review the fixed expression and bound value separately. Column names cannot be bound by PDO, so choose those from trusted definitions; do not let arbitrary input dictate them. Raw expressions are SQL strings requiring care, not automatically safe containers for untrusted text.",
"Parameter binding for values is not permission to accept arbitrary column names. A raw expression also does not gain safety merely by being inside a query-builder call.")
add(70,
"Several operations need the same query constraint. A local Eloquent scope gives that constraint one reusable name while letting callers add further constraints before retrieval.",
"For Laravel 12's documented active scope, import the Scope attribute, mark the model method with #[Scope], and have it apply $query->where(\"active\", 1). The method takes a Builder and returns void or that same builder. A caller uses Model::active()->where(...)->get() to combine active with another requirement. Trace the scope as adding the reusable constraint, not as fetching a finished collection inside the method.",
"Retrieving records inside the scope would not express the described composable-constraint pattern. Keep get at the caller's retrieval boundary.", 'MEDIUM','annotated_code')
add(71,
"A stored model contains more than the API should expose. An API resource defines the public representation explicitly, connecting model values to chosen output keys rather than automatically publishing every attribute.",
"Create a JsonResource subclass and list the allowed output fields in toArray(Request $request): array. For a supplied record with title and a protected internal field, expose only the fields the public contract allows. Return new ResourceName($model) from the handler. The outermost resource response uses a data wrapper by default, so check that configured wrapping against the client's expected shape. Trace model attribute, selected public key and outer response shape as three layers of the same output.",
"Choosing explicit fields and choosing wrapping are separate decisions. A field allowlist does not remove the default outer data wrapper by itself.")
add(72,
"A REST resource controller needs bounded actions for the supplied API operations. Laravel's API resource registration maps those actions without adding the create and edit routes used for HTML forms.",
"Register Route::apiResource(resourceName, ControllerClass::class). Read index, store, show, update and destroy as list, create, read, update and delete. In the supplied store action, create the model from accepted attributes through Model::create($attributes). If the contract calls for creation status 201, return its public body through response()->json($body, 201). Trace the action from accepted attributes to created model to public response rather than equating method registration with completed behavior.",
"The store action creates a resource; it is not the omitted create route for an HTML form. The API contract still determines the required response body and status.")
add(73,
"An update can omit an optional field or explicitly supply null, and those cases can mean different things. Validated input should preserve that distinction instead of filling omitted fields with invented defaults.",
"Use validated() for validated data, or safe()->only([...]) for its intended subset. sometimes validates an optional update field only when present; nullable permits an explicitly supplied null, including null produced by default empty-string conversion. Compare two payloads: one omits subtitle, while the other supplies subtitle as null. array_key_exists detects that the second key is present even though isset would not. Apply only the validated attributes that are present through fill, then save. Follow presence and value separately before deciding which model attributes change.",
"Missing and explicitly null are not interchangeable update inputs. An invented default for an omitted field can change data the request did not ask to change.")
add(74,
"A Vue screen reports that a request failed, but the visible screen alone does not locate the failure. Diagnose by comparing the captured request and response with route registration and matching backend log context.",
"Start with the supplied method and URL and compare them with php artisan route:list. Next distinguish a received HTTP status from a rejected fetch operation. Use matching server log messages and request details to establish the backend point reached. If existing evidence is insufficient, add non-sensitive context to the log message, repeat the same request and inspect the new evidence. Keep the diagnosis tied to observations: a path mismatch, received response and matched handler context establish different boundaries.",
"Do not guess the backend stage solely from a screen message. Also, adding diagnostic context is not permission to log sensitive input.", 'HIGH','screen_demo')
add(75,
"The chosen first-party SPA session model needs a server boundary that recognizes first-party browser requests. Sanctum's stateful configuration names those domains, while middleware configuration enables session authentication for the classified API requests.",
"For the supplied SPA origin with a port, include both host and port in config/sanctum.php's stateful domains. The SPA and API must share the same top-level domain; different subdomains are supported. In bootstrap/app.php's withMiddleware callback, call statefulApi. Send Accept: application/json and ensure the browser supplies Referer or Origin. Trace one configured request through its origin evidence and server classification rather than assuming every API request is automatically a first-party SPA request.",
"The port is part of the configuration when it is part of the SPA origin. Also, merely choosing cookie authentication does not replace configuring the stateful request boundary.", 'HIGH','whiteboard_drawing')
add(76,
"A list screen can be waiting, failed, successfully empty or successfully populated. Separate result and error state let it represent those outcomes instead of using one blank screen to mean everything.",
"Set loading before awaiting the supplied request, update data or error according to its outcome, and reset loading in finally. Render the error branch when error is set, the loading branch while work is pending and the success branch when a result arrives. Within successful list rendering, inspect whether the collection has items. A returned empty collection should show its empty-state message, not remain in loading. Trace each outcome using the same request so the screen's messages correspond to pending work, failure or an actual successful result.",
"An empty successful list is not still loading. Also, resetting loading only on success leaves the failed path outside the stated finally cleanup pattern.", 'HIGH','annotated_ui')
add(77,
"A child form wants a parent-owned value to change. Component events let the child communicate that request while the parent remains responsible for its state. They are not a DOM-style bubbling mechanism.",
"Declare the supplied event names with defineEmits at the top of script setup. On the user action, call emit(eventName, payload). The direct parent listens on the child with @event-name=\"handler\" and updates its state in that handler. Trace the payload from child emission to parent handling, keeping the child input readonly throughout. If another ancestor needs notification, do not assume the component event bubbles automatically through the hierarchy.",
"The event asks the parent to handle a change; it is not a reason for the child to mutate its readonly input. A listener on an indirect ancestor does not receive it through automatic component-event bubbling.")
add(78,
"A SPA form should use the user's current field state when constructing its JSON submission. v-model connects controls to JavaScript state, and the submit handler can then send those values without the form's default browser navigation.",
"Bind the title control with <input v-model=\"field\"> and initialize the intended field in JavaScript. v-model uses that state as the source of truth rather than the control's initial value attribute. Bind the form with @submit.prevent=\"onSubmit\". In the supplied handler, serialize the current form values with JSON.stringify for the request body. Trace an edit from control to component field to submitted payload, checking that unrelated component state has not been submitted instead.",
"An initial HTML value attribute does not override v-model's JavaScript source of truth. Preventing default submission also does not decide which values the JSON payload contains; the handler must use the form values.")
add(79,
"In-app navigation succeeds, but directly opening a nested SPA URL also needs host support. With createWebHistory, the host receives that direct URL before Vue Router can render its client route.",
"Configure the supplied host to serve existing static files normally and return SPA index.html for client-route requests without a matching static file. The documented nginx try_files pattern checks $uri and $uri/ before /index.html. Verify the same nested route in three ways: in-app navigation, a direct URL and a reload. Only the latter two exercise the host fallback. A catch-all fallback also serves the SPA for unknown paths, so configure a client not-found route rather than expecting the host's normal 404 page.",
"Passing an in-app navigation check is not proof that the host handles direct nested URLs. A catch-all fallback also changes what happens for unknown routes.", 'HIGH','screen_demo')
add(80,
"A detail route changes from one record identifier to another while matching the same component. Vue Router can reuse the component instance, so loading only at an initial lifecycle boundary does not cover every parameter change.",
"Obtain route through useRoute and watch a getter for route.params.id. Call the supplied loading operation with the new identifier in the callback. Add immediate: true when this watcher should handle the initial record as well as later changes. Trace navigation from record 12 to record 18: the callback's new id selects the new record even though the matched component instance is reused. Compare initial loading and changed-parameter loading explicitly.",
"Do not assume the same-route parameter change always creates a new component instance or reruns every lifecycle hook. Watch the parameter needed for the data load.", 'HIGH','live_code')
add(81,
"A response is gaining a public field while existing consumers still depend on earlier fields and wrapping. Explicit resource output helps bound the change, and tests can check that required existing data remains present.",
"For a supplied resource, add only the intended public field in toArray rather than automatically exposing other model attributes. Keep the required outer wrapping unchanged unless the contract explicitly changes it: consumers access wrapped and unwrapped data differently. Use assertJson($expectedFragment) to check that earlier required data remains present even if additional properties exist. Separately, account for maintenance mode during updates: Laravel disables the application and returns 503. Treat availability during maintenance and response-shape compatibility as distinct checks.",
"Adding a field and changing the outer data wrapper are not equivalent changes for consumers. A fragment assertion checks required data presence, not the absence of all additional properties.", 'MEDIUM','data_table_demo')
add(82,
"A collection endpoint allows selected filter and sort choices. Those options affect query structure, so validate choices and map them to trusted columns instead of copying arbitrary request text into column positions.",
"Suppose the supplied API permits sorting by a public option called title. Validate the option with Rule::in($allowedChoices), then map it to the trusted column and an allowed asc or desc direction before orderBy. For an accepted filter, map its option to the trusted column and pass the submitted value separately to where. Use only validated inputs for this construction. Trace option validation, trusted mapping and value binding as separate steps; binding a filter value does not validate the requested column.",
"PDO binds values, not column names. Therefore a parameterized value does not make an arbitrary sort or filter column safe to accept.")
add(83,
"A collection endpoint should return a bounded page rather than the entire matching list. Pagination combines the query constraints with page selection and returns both records and navigation metadata.",
"Build where and orderBy constraints, then paginate with the supplied per-page limit. The default page query-string argument selects the current page. In JSON, read the records under data and inspect total, per_page, current_page and last_page as metadata rather than record fields. Use next_page_url and prev_page_url for adjacent destinations, checking for null at a boundary. Trace the first and last pages in the supplied dataset so a missing previous or next destination is interpreted as a boundary, not a failed collection request.",
"Pagination metadata is not another resource record. Also, an adjacent-page URL may legitimately be null; do not assume both directions always exist.", 'HIGH','data_table_demo')
add(84,
"A collection needs related data for every parent model. Accessing each relationship lazily can add one query per parent, the N+1 pattern. Eager loading asks for the needed relationship at the collection query boundary.",
"Use the documented books-and-authors example. Book::with(\"author\")->get() uses one books query and one authors query rather than an author query for each book. Compare the query pattern as the supplied book count grows: per-item lazy access grows with the parents, while this documented eager example retrieves authors together. If selecting related columns, retain the related id and required foreign-key columns along with displayed fields. Trace both the query boundary and the identifying columns needed to connect the retrieved data.",
"Do not generalize the documented two-query books-and-authors example into a universal query count for every relationship graph. Selecting only displayed fields can omit required identifying columns.", 'HIGH','diagram_animation')
add(85,
"A model can belong to several related models, each of which can also have several memberships. A many-to-many relationship stores those associations in a pivot table, so changing membership is distinct from deleting a related model.",
"Define belongsToMany with custom pivot-table or key arguments if conventions do not fit the supplied schema. Imagine current related ids are 2 and 4. attach(7) adds membership 7; detach(4) removes that association without deleting either model. sync([2, 7]) makes the membership match that list, removing omitted memberships. If the task instead requires preserving omitted memberships, use syncWithoutDetaching. Trace the identifier set before and after each supplied operation to distinguish addition, removal and replacement of the set.",
"Detach removes pivot membership, not the related model itself. Sync also removes omitted memberships, so it is not interchangeable with an add-without-removal operation.", 'HIGH','whiteboard_drawing')
add(86,
"A supplied API contract needs executable checks for status, JSON data and invalid-field feedback. Laravel feature tests exercise the JSON request boundary and assert those public outcomes independently.",
"Choose the request helper matching the operation, such as postJson for creation or patchJson for an update, with the supplied endpoint and payload. Assert the expected status and JSON fragment; use assertJsonPath for one particular nested field. For an invalid title payload, combine assertUnprocessable with assertJsonValidationErrors(['title']) to check 422 and the field mapping. Trace the valid and invalid cases separately, noting which contract requirement each assertion checks. A status assertion alone does not establish the required body.",
"Checking that a request ran without an exception is not a substitute for the specified public assertions. Invalid-field tests need both the HTTP outcome and field-error evidence.", 'HIGH','live_code')
add(87,
"A controller depends on a collaborator contract, and Laravel's container needs to know which implementation to supply. Interface-based injection links that contract to a registered implementation without making the consumer choose the concrete class itself.",
"Bind the supplied interface to its implementation in a service provider with $this->app->bind. Type-hint the interface in the container-resolved consumer's constructor. Trace resolution from interface dependency to registered class to constructed collaborator. To substitute another conforming service, change the binding while preserving the consumer's interface dependency. Concrete classes with concrete dependencies can often resolve without an explicit binding, but the interface needs the chosen implementation mapping.",
"Do not upgrade ‘can often be resolved’ to a promise that all concrete dependency graphs need no binding. An interface also does not tell the container which implementation to choose without a mapping.", 'HIGH','whiteboard_drawing')
add(88,
"A login endpoint receives validated credentials and must choose a public success or failure response. Auth::attempt checks the stored user and password and establishes authentication when the credentials are accepted.",
"Pass the validated credentials to Auth::attempt and branch on its true or false result. The submitted password remains plaintext input to that check; Auth::attempt compares it with the stored password hash. Return the login contract's JSON body and status for the selected outcome with response()->json. Trace accepted and rejected credentials through that decision, keeping authentication outcome and response construction distinct. This explanation covers the check and response; session identifier regeneration has its own focused treatment.",
"Do not hash the submitted password before Auth::attempt. The service checks plaintext against the stored hash, rather than requiring another submitted hash.")
add(89,
"The cookie-authenticated SPA login flow needs CSRF initialization before credentials are posted. Follow the request order and token handling instead of disabling protection when a later request fails.",
"First request /sanctum/csrf-cookie. It sets XSRF-TOKEN; if the client library does not copy it automatically, URL-decode the cookie value and send it as X-XSRF-TOKEN on subsequent requests. Then POST credentials to /login. Successful login establishes the session cookie for later requests. Trace that sequence separately from a later expiration case, where 401 or 419 may require returning to login. The initialization cookie, CSRF header and authenticated session cookie play different roles in this flow.",
"A CSRF failure is not a reason to turn protection off. Also, preserve the stated ‘may require’ recovery wording for later 401 or 419 responses rather than treating every such response as the same confirmed cause.", 'HIGH','diagram_animation')
add(90,
"A non-SPA client needs a bearer credential. Sanctum personal access tokens support issuance, authentication and revocation, while distinguishing the newly issued plaintext credential from its stored hash.",
"Add HasApiTokens to the user model and create a token with $user->createToken($name). Deliver the returned object's plainTextToken immediately to the intended client, which sends Authorization: Bearer followed by that value. Sanctum stores a SHA-256 hash, not a plaintext value to retrieve later. For selective revocation, delete the stored token matching the intended id; other tokens remain. Deleting the user's entire tokens relationship revokes all their stored tokens. Trace issuance and the two revocation choices with the supplied token ids so the selected scope of deletion is explicit.",
"Selective token deletion is not the same as deleting every token for the user. Also, do not expect to recover the issued plaintext value from the stored hash later.", 'MEDIUM','annotated_code')
add(91,
"A component form should be checked through the interactions and output a consumer can observe. Mount it with supplied props, enter a value through its native control and submit through its public event handling.",
"Await wrapper.get(selector).setValue(value) for the input, then await wrapper.get('form').trigger('submit.prevent'). Inspect wrapper.emitted(eventName)[0][0] with toEqual to check the submitted payload. For visible feedback, inspect the selected element's text with toContain. Follow the same supplied input through entry, submission, emitted payload and rendered output. This tests the component's public behavior rather than relying on private internal state names.",
"A private implementation detail is not a substitute for observed form behavior. Await the supplied user-interaction helpers before making the corresponding output assertion.", 'HIGH','live_code')
add(92,
"An API rejects a form with field validation errors, and the SPA should put those messages beside the relevant fields. A received 422 is an HTTP result to interpret, not a network rejection to wait for in catch.",
"Clear stale request-error state before the next submission. When status is 422, parse the JSON errors mapping and store it reactively. Render each field's messages beside that field when its error entry exists. On another 422, replace the mapping with the new response so old errors do not stand in for current feedback. Trace a title error from the response's title key into the title control's feedback, rather than treating the invalid submission as successful data.",
"Fetch does not reject merely because the status is 422. Also, keeping stale field messages without replacing them can misrepresent the next request's result.", 'HIGH','annotated_ui')
add(93,
"Two views need the same confirmed values, while an edit form also has an unconfirmed draft. State ownership decides which values need a shared boundary and which should remain local.",
"Imagine a list and summary both use a confirmed title. Place that genuinely cross-view value in one shared source of truth covering both consumers rather than maintaining independent copies. Keep the form's edit draft local when other views do not need it. Trace ownership for each value separately: the confirmed shared value is not the same thing as one component's unconfirmed draft. This avoids solving every synchronization issue by moving every local field into a shared store.",
"Shared state is for values genuinely needed across consumers, not all component state. Keeping a component-owned draft local is consistent with sharing confirmed cross-view values.", 'HIGH','whiteboard_drawing')
add(94,
"A public response may include a related identifier, a selected related collection or no related output. Resource serialization must choose those shapes explicitly and coordinate optional inclusion with what the parent query loaded.",
"If the supplied contract needs only a related identifier, return that field instead of the whole model. For an optional included collection, use RelatedResource::collection($this->whenLoaded(relationshipName)). whenLoaded removes the key when the relationship is not loaded, so compare omission with the contract's required shape. Load an included relationship with with at the parent query boundary, avoiding per-item lazy relationship access. Trace loaded and unloaded cases separately: omitted output is not automatically the same as an included empty collection.",
"A related model's presence internally does not mean every related attribute should be public. Also, whenLoaded omission must match the contract rather than being treated as an incidental formatting detail.")
add(95,
"A database feature test should not inherit unintended state from an earlier participating test. RefreshDatabase supplies an isolation pattern, while fixtures and database assertions make the operation's stored effect explicit.",
"Use RefreshDatabase in the feature test class and arrange records with factory()->create($overrides). After the supplied operation, assertDatabaseHas checks the expected matching record, while assertDatabaseMissing checks that a matching record no longer exists. When the schema is current, RefreshDatabase runs the test in a transaction rather than migrating the schema every time. Trace setup, operation and stored outcome, keeping isolation and persistence assertions distinct.",
"Do not say RefreshDatabase always migrates for every test; the current-schema case uses a transaction. Also, a response assertion alone does not establish the database effect.", 'MEDIUM','live_code')
add(96,
"Logging out of a cookie-session application is a server-session operation, not just removing the user's name from a SPA menu. Laravel's recommended sequence removes authentication, invalidates the session and refreshes the CSRF token.",
"Call Auth::logout(), then $request->session()->invalidate(), then regenerateToken(). Invalidation flushes session data and regenerates its identifier, so the old session data and identifier are not continued. Verify the resulting unauthenticated state with assertGuest. Trace that server result separately from the visible navigation: the user label disappearing does not prove the session was invalidated.",
"Clearing a client-side display is weaker than the described server logout. Do not replace invalidate with a visual change and infer that existing session data is gone.")
add(97,
"Several components need to read the same shared confirmed values. A Pinia store supplies a shared instance with reactive state, provided it is installed in the application and consumed without disconnecting state reads.",
"Define the store with a unique id and state: () => ({ ... }), exporting its useStore function. Install createPinia through app.use before mount. Consumers call the exported function and read store.property so both observe the shared value. If they need destructured state or getters, use storeToRefs rather than destructuring those values directly from the store. Trace two consumers reading the same property before and after a state change, preserving the reactive connection in both.",
"Directly destructuring store state breaks its reactive connection. Also, defining a store module does not replace installing Pinia in the application.")
add(98,
"A cookie-authenticated API on another origin needs fetch requests that include the chosen session credentials. Mutations also need the CSRF header; fetch does not automatically copy that token cookie into the header for you.",
"For the configured cross-origin cookie API, use credentials: 'include' instead of fetch's same-origin default. Send Accept: application/json and ensure Referer or Origin accompanies the first-party request. For a mutation, URL-decode XSRF-TOKEN and send the result as X-XSRF-TOKEN. Trace the session credential and CSRF header separately: including cookies does not itself perform that header copy. Keep the request in the cookie-session model instead of substituting a bearer token.",
"Credentials inclusion and CSRF header construction are distinct requirements. A bearer API token is not a substitute for implementing the chosen first-party cookie-session mode.")
add(99,
"The API needs a server authentication boundary for protected operations. auth:sanctum accepts the stated authenticated modes and prevents protected routes from being treated as public.",
"Assign auth:sanctum to the supplied route, or use Route::middleware('auth:sanctum')->group(...) for all protected routes in a group. For first-party SPA requests, the authentication check uses cookie-based sessions rather than requiring a personal access token. In the protected route, $request->user() supplies the authenticated user. Test anonymous JSON access with assertUnauthorized to verify 401. Trace an anonymous request and an authenticated request separately before considering the route's application work.",
"A SPA's chosen session model does not make the API route public. Conversely, auth:sanctum does not require a personal access token for every first-party SPA request.")
add(100,
"A component's asynchronous states need tests with controlled request outcomes. Mock the imported request boundary so each case can specify completion or rejection and then observe the screen at the correct time.",
"Replace the supplied module export with vi.mock and vi.fn. Set mockResolvedValue for a successful result or mockRejectedValue for a rejected operation. After triggering the request, assert loading before flushPromises, then await flushPromises and assert the controlled outcome. Between tests, call vi.resetAllMocks and set the next response anew; this resets histories and implementations. Trace pending and completed observations separately so the test does not skip the loading state or reuse another case's response.",
"Do not assert the completed asynchronous outcome before the component has processed it. Also, resetting mocks and configuring each new case's response are separate parts of the isolation pattern.", 'HIGH','live_code')
add(101,
"The browser must be allowed to read credentialed API responses from the approved SPA origin. Laravel CORS configuration defines that permission; a wildcard origin is not the credentialed-response setting required here.",
"Publish cors configuration and set allowed_origins to the explicit approved origins with supports_credentials true. For the approved origin, verify the preflight for required method and headers and inspect the response permission: a specific Access-Control-Allow-Origin and Access-Control-Allow-Credentials: true. Also verify that a disallowed origin does not receive access permission. Laravel's global HandleCors handles OPTIONS from these settings. Follow the approved and disallowed cases separately rather than testing only that the endpoint itself returns some data.",
"A wildcard origin does not permit browser access to a credentialed cross-origin response. Successful endpoint processing alone is not proof of the required CORS permission.", 'HIGH','screen_demo')
add(102,
"A privileged action needs a permission decision on the server. A named gate holds that decision and can be enforced before the action, rather than relying on whether a frontend control is hidden.",
"Define the supplied ability with Gate::define and place its role or capability predicate in the callback receiving the authenticated user. Enforce it with Gate::authorize before the privileged action; denial produces 403. For an ability without a model instance, can:ability-name middleware can enforce it at the route boundary. Trace permitted and denied users through the same ability so the server decision, not a visual control, determines whether work proceeds.",
"Hiding a button is not enforcement of server permission. Authentication and the supplied ability decision also should not be collapsed into one indistinct ‘allowed’ label.", 'HIGH','whiteboard_drawing')
add(103,
"A successful login should not keep using its pre-login session identifier. Session regeneration after accepted credentials is Laravel's session-fixation defense, while preserving the authenticated session data.",
"Inside the successful Auth::attempt branch, call $request->session()->regenerate(). Compare the identifier before login with the one used after successful login to verify the transition. Keep rejected credentials outside that success branch. Contrast regenerate with invalidate: regeneration changes the identifier while preserving authenticated data, whereas invalidation removes all session data. Trace accepted credentials, regeneration and use of the resulting identifier as an ordered sequence.",
"Do not substitute invalidate for regeneration in this successful-login explanation: it removes all session data. Also, the regeneration belongs after credentials have been accepted.")
add(104,
"Several consumers need the same confirmed shared-state transition. A Pinia action puts that behavior in the store so components call one transition rather than each reproducing it independently.",
"Define the action as a method in an options store's actions object. It receives arguments and uses this.property to update store state. If the action makes a request, it can be async and await the confirmed result before applying it. A consumer calls store.actionName(input). Trace two components reading the shared property: after the action updates it, both observe the store's changed state. Keep the request input, confirmed result and consumer-visible store update distinct.",
"An action that starts asynchronous work should not apply an unconfirmed result as though the request had completed. Nor should each consumer reproduce the same shared transition independently.")
add(105,
"A user requests a protected client screen while signed out. A navigation guard can redirect the client to login and preserve the intended destination, but it does not replace server-side API protection.",
"Register router.beforeEach and inspect to before navigation is confirmed. Return false to cancel, a route location to redirect, or undefined/true to allow. Exclude the login route from the unauthenticated redirect condition so the redirect does not loop. Add query: { redirect: to.fullPath } when preserving the intended destination. Trace the original protected URL into the login redirect and eventual recovery destination. Separately keep authentication checks on the API: the guard controls navigation, not server access.",
"A frontend guard is not an API security boundary. Redirecting every unauthenticated destination including login also defeats the flow by creating a redirect loop.", 'HIGH','diagram_animation')
add(106,
"An update is allowed only for the resource owner. A model policy expresses that user-and-model decision, and Gate::authorize enforces it before the protected action.",
"Use the documented PostPolicy::update comparison $user->id === $post->user_id. The policy method receives the authenticated user and relevant model and returns whether the action is permitted. Generate a model-associated policy with make:policy and the --model option. Laravel discovers policies under its naming and directory conventions; otherwise register the mapping explicitly. Before the update, call Gate::authorize(actionName, $model), which returns 403 on denial. Trace owner and non-owner against the same post rather than checking only whether either user is signed in.",
"Being authenticated does not by itself satisfy the ownership rule. Policy discovery also depends on the stated conventions; a differently placed policy needs the intended explicit mapping.")
add(107,
"The first-party session model must still fit the deployed SPA and API domains. Production cookie configuration combines stateful classification, session scope, credentialed CORS and actual client credential sending.",
"For the supplied HTTPS deployment at different subdomains of the same top-level domain, configure the SPA host in stateful domains and retain a port if it belongs to the deployed origin. Set the session domain to cover the SPA and API subdomains and enable credentialed CORS for the approved origin. Set SESSION_SECURE_COOKIE=true so the browser sends the session cookie only over HTTPS. Ensure the production client sends credentials too. Trace one deployed request across all these requirements; a correctly scoped cookie is not useful if that request omits credentials.",
"Do not assume development-domain settings automatically describe production. Also, the shared top-level-domain requirement still applies; secure cookies do not replace it.", 'HIGH','whiteboard_drawing')
add(108,
"A user saves an edit, and the screen should show what the server confirmed rather than claim an unconfirmed save succeeded. Mutation synchronization ties visible reactive state to the successful request outcome.",
"Await the mutation before applying its successful result. For a record screen, assign the confirmed saved record to reactive record state. For a list, replace the array with a new confirmed list or a mapped replacement for the matching record. Alternatively, re-fetch after success and replace results with the confirmed response. If the mutation fails, record error feedback instead of applying that success update. Trace one saved title from request input to server-confirmed result to visible state, keeping the failure path separate.",
"Submitting an edit is not confirmation that it was saved. Do not apply the success-state update on the failed path or leave the screen showing an unconfirmed result as final.", 'HIGH','annotated_ui')
add(109,
"A failed API request may be unauthenticated, forbidden or missing its resource. The specified failure contract keeps those outcomes distinct in both HTTP status and public JSON body.",
"For anonymous access use 401, for denied Gate::authorize permission use 403, and for missing implicit-bound models use 404. Return the selected contract body with response()->json($body, $status). Verify each applicable failure's status and required JSON fields instead of treating any non-success as the same result. For the 401 case, assertUnauthorized checks that outcome.",
"A 403 is not the same evidence as a missing model's 404 or an anonymous request's 401. Matching a generic error body alone does not verify the correct failure category.", 'LOW','data_table_demo')
add(110,
"The same protected resource should behave differently for its owner, a non-owner and an anonymous caller. Authentication feature tests arrange those identities explicitly and verify the specified public outcome for each.",
"Create owner and non-owner fixtures and a record with its owner attribute fixed. Use actingAs($user) before the JSON request for each authenticated case. Make a separate anonymous request and assertUnauthorized for 401; as the forbidden non-owner, assertForbidden for 403. As the owner, assert the required success status and response JSON. Trace all three against the same ownership rule, keeping fixture ownership explicit so the test actually exercises different decisions.",
"A test that merely avoids an exception does not establish the permitted owner's contract. Also, a non-owner test without explicit record ownership may not represent the intended denied case.", 'HIGH','live_code')
add(111,
"A deployment smoke check should exercise the deployed boundaries, not just show that the SPA opens. Use supplied disposable identities and records so the check can compare real endpoint evidence with the acceptance contract.",
"Begin with the configured health route to check that Laravel boots without exceptions. Log in with the disposable acceptance identity, then use its authenticated session for create, read, update and delete on disposable records. Record each status and required public JSON fields. Include a direct protected-screen URL or reload to test the SPA host fallback as well as in-app navigation. If a step fails, compare its captured request and response with matching server log context to locate the reached boundary. Follow the same disposable workflow from health through CRUD rather than collecting unrelated screenshots.",
"A healthy-looking screen is not enough: endpoint statuses, public JSON and direct-route hosting are separate acceptance evidence. Use matching logs to diagnose failure instead of guessing from appearance.", 'HIGH','screen_demo')
add(112,
"A later protected request may require login recovery, or it may deny a particular action even though repeating login is not the right response. Inspect the status before successful-data parsing so those paths remain distinct.",
"For a later 401 or 419 after session expiration, send the user back through login while preserving the requested destination. For an options auth store whose initial state is signed out, authStore.$reset() restores that state before directing the user to login. For 403, display the forbidden branch instead of repeatedly restarting login or replacing the screen with success data. Trace one request needing authentication and another forbidden action, checking the received HTTP status first in both. This keeps recovery aligned with the actual response rather than treating every failed request as an expired session.",
"A 403 means forbidden, not simply ‘log in again’. Also, preserve the stated possibility of 401 or 419 after expiration rather than asserting that every such status proves the same cause.", 'HIGH','diagram_animation')

import runpy
walkthroughs=runpy.run_path(str(P/'pass_a_walkthroughs.py'))['walkthroughs']
# Index-aligned citations for the custom examples and misconception contrasts.
# Introductions are framing; required factual claims have explicit citations in
# the definition/mechanism blocks and worked examples.
citation_rows="""
1234 23
1234 24
1234 34
1234 23
1234 14
1234 34
1234 34
1234 23
1234 34
1234 4
1234 34
1234 12
1234 24
1234 34
1234 234
1234 34
123 23
123 23
1234 12
123 3
1234 34
1234 24
1234 34
1234 23
123 23
1234 23
123 3
12345 45
123 3
1234 23
1234 14
12345 35
1234 34
123 23
1234 24
1234 24
123 23
1234 124
1234 12
1234 12
123 23
123456 136
1234 34
12345 345
1234 34
12345 23
123 3
1234 24
12345 35
1234 24
12345 45
12345678 56
1234 24
1234 14
1234 34
12345 25
1234 34
1234 24
1234 14
1234 123
1234 4
12345 23
1234 23
1234 34
1234 234
1234 234
1234 234
1234 24
12345 345
12345 45
1234 4
1234 24
1234 24
12345 345
1234 34
12345 235
1234 24
12345 45
1234 14
12345 45
1234 12
1234 23
12345 15
1234 34
1234 34
12345 345
12345 245
1234 34
1234 2
1234 24
123456 356
12345 15
12345 25
1234 34
12345 124
12345 24
12345 24
12345 135
1234 24
12345 245
12345 345
12345 345
1234 24
1234 23
12345 234
12345 345
12345 123
12345 15
1234 134
1234 123
12345 345
12345 235
1234 234
""".strip().splitlines()
assert len(citation_rows)==113
reference_examples={
30:'For the supplied task, inspect schedule:list for its next due time, then observe schedule:run at a due time. Cron invokes the evaluator every minute; the task declaration determines whether the task is due.',
56:'For the supplied asynchronous connection, run queue:work with --once when verification should consume one available job and exit. After changed code, queue:restart requests worker exit; the process manager must restart it.',
83:'For a supplied first or last page, read records in data and metadata separately. Check next_page_url and prev_page_url for null at a boundary instead of assuming both adjacent destinations exist.',
87:'Bind the supplied interface to its implementation, then type-hint that interface in the container-resolved consumer. Substituting the implementation changes the binding, not the consumer contract.'}
assert len(custom)==len(C)==113
entries=[]
for i,c in enumerate(C):
    key=(c['concept_id'],c['path_id'])
    b=B[key]; facts=b['evidence']['required_facts']; ids=[f['id'] for f in facts]
    intro,example,contrast,level,mode=custom[i]
    # Each required claim is retained with its original qualification. Teaching
    # examples explain the same claims, with invented example data only.
    split=max(1,len(facts)//2)
    groups=[facts[:split],facts[split:]]
    example_ids,contrast_ids=([f'f{n}' for n in part] for part in citation_rows[i].split())
    example_ids=[f for f in example_ids if f in ids]
    contrast_ids=[f for f in contrast_ids if f in ids]
    blocks=[{'id':'tb1','purpose':'intro','content':intro,'fact_ids':[]}]
    for group,purpose in zip(groups,['definition','mechanism']):
        if group:
            blocks.append({'id':f'tb{len(blocks)+1}','purpose':purpose,
                           'content':' '.join(f['statement'] for f in group),
                           'fact_ids':[f['id'] for f in group]})
    blocks.append({'id':f'tb{len(blocks)+1}','purpose':'example','content':example,'fact_ids':example_ids})
    blocks.append({'id':f'tb{len(blocks)+1}','purpose':'misconception','content':contrast,'fact_ids':contrast_ids})
    if D[key]=='core' and i in walkthroughs:
        blocks.insert(-1,{'id':'walkthrough','purpose':'walkthrough',
                          'content':walkthroughs[i],'fact_ids':example_ids})
    if i==32:
        blocks[-1]['content'] += ' A return from finally can override an earlier return from try or catch; do not assume finally only performs cleanup while preserving that earlier result.'
        # m1 is a sourced misconception correction, not an extra required fact.
    if D[key]=='reference':
        blocks=[t for t in blocks if t['purpose'] in ('definition','mechanism')]
        blocks.append({'id':'reference_example','purpose':'example','content':reference_examples[i],'fact_ids':example_ids})
    for j,t in enumerate(blocks,1):
        t['id']=f'tb{j}'
    reasons={
        'HIGH':{
            'annotated_code':'Following the supplied code and its values step by step makes the mechanism and changed result concrete.',
            'screen_demo':'An end-to-end tool demonstration makes the command or configuration change and its observable verification easier to follow.',
            'live_code':'Running the supplied interaction or code while tracking inputs and outputs clarifies the changing behavior.',
            'diagram_animation':'A changing-state or control-flow diagram clarifies the distinct paths and their order.',
            'whiteboard_drawing':'Drawing the relationships and following one example through them clarifies the boundaries and mappings.',
            'annotated_ui':'A before-and-after interface demonstration clarifies how state and outcomes affect what the learner sees.',
            'data_table_demo':'Following a small collection and its resulting output makes the transformation and boundary cases concrete.'},
        'MEDIUM':'An annotated example or short demonstration can reinforce the supplied distinction, but the prose and worked example carry the explanation.',
        'LOW':'The bounded definition or distinction is adequately taught in prose; a small static annotated example suffices without a demonstration.'}
    reason=reasons[level][mode] if level=='HIGH' else reasons[level]
    reason=c['concept_name']+': '+reason
    blocked=c.get('blocked_knowledge_ids',[])
    notes=['First establish the distinction illustrated in the worked example; keep the explanation focused on '+c['primary_objective'].rstrip('.').lower()+'.',
           'Use supplied exercise material and scaffolding; do not assume the learner can author unrelated setup. Keep optional enrichment outside this required-fact explanation.']
    if blocked:
        names={x['concept_id']:x['concept_name'] for x in C}
        avoid=[names.get(x,x) for x in blocked[:2]]
        notes.append('Do not expand into blocked later concepts here: '+ '; '.join(avoid)+'.')
    entries.append({'concept_id':key[0],'path_id':key[1],'teaching_blocks':blocks,
                    'video_need':{'level':level,'reason':reason,'preferred_visual_modes':[mode] if level!='NONE' else []},
                    'teaching_notes':notes})
meta=dict(extracted['metadata'])
meta.update(artifact_type='glossary_pass_a',artifact_version='1.0.0',schema_version='1.0.0',
            batch_id=P.name,model='none',prompt_version='05_glossary_pass_a@v1',
            generated_at=datetime.now(timezone.utc).isoformat().replace('+00:00','Z'),
            parent_artifact_hashes={f:hashlib.sha256((P/f).read_bytes()).hexdigest() for f in inputs})
out={'metadata':meta,'batch_id':P.name,'entries':entries}
(P/'glossary_pass_a.part.all.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
# Deterministic pre-evaluation checks.
assert set(B)==set(D)=={(c['concept_id'],c['path_id']) for c in C}
assert len({(e['concept_id'],e['path_id']) for e in entries})==113
for e in entries:
    key=e['concept_id'],e['path_id']; required={f['id'] for f in B[key]['evidence']['required_facts']}
    assert required=={f for t in e['teaching_blocks'] for f in t['fact_ids']}
    assert all(set(t['fact_ids'])<=required for t in e['teaching_blocks'])
    assert len({t['id'] for t in e['teaching_blocks']})==len(e['teaching_blocks'])
    assert 'video' not in ' '.join(t['content'] for t in e['teaching_blocks']).lower()
    assert e['video_need']['level']!='NONE' or e['video_need']['preferred_visual_modes']==[]
print('entries',len(entries),'blocks',sum(len(e['teaching_blocks']) for e in entries))
from collections import Counter
print('depth',Counter(D.values()),'video need',Counter(e['video_need']['level'] for e in entries))
print('required fact references',sum(len(B[(e['concept_id'],e['path_id'])]['evidence']['required_facts']) for e in entries))
for tier in sorted(set(D.values())):
    lengths=[sum(len(t['content'].split()) for t in e['teaching_blocks']) for e in entries if D[(e['concept_id'],e['path_id'])]==tier]
    print(tier,'words min/mean/max',min(lengths),round(sum(lengths)/len(lengths)),max(lengths))
