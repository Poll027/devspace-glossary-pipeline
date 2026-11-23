import json,hashlib,datetime,pathlib,copy
B=pathlib.Path('batches/glossary_batch_business_analyst');bid=B.name
cs=json.loads((B/'extracted_concepts.json').read_text())['concepts']
lookup={(x['concept_id'],x['path_id']):x for x in json.loads((B/'registry_lookup.json').read_text())['lookups']}
registry={x['concept_id']:x for x in json.loads((B/'concept_evidence_registry_snapshot.json').read_text())['entries']}
D={}
def add(i,*facts):
 # Each tuple contains a verified statement and a source-pack source_id with a navigable locator.
 D[i]=[{'id':'f'+str(n+1),'statement':s,'source_refs':r if isinstance(r,list) else [r]} for n,(s,r) in enumerate(facts)]
def atl(page,section):return 'atlassian_agile#'+page+' — '+section
def nn(page,section):return 'nngroup_articles#articles/'+page+'/ — '+section
def pg(section):return 'postgres_docs#'+section
def pbi(page,section):return 'powerbi_docs#'+page+' — '+section
def tab(page,section):return 'tableau_help#current/pro/desktop/en-us/'+page+'.htm — '+section
req='work-management/project-management/requirements-gathering'
# Tile 01.01.01: shared elicitation and scoping sources.
add(0,
 ('Problem framing clarifies the problem rather than choosing a solution.',atl('team-playbook/plays/problem-framing','2. Set the stage')),
 ('Write a concise problem statement identifying who is affected, what the problem is, why it matters, and where it occurs.',atl('team-playbook/plays/problem-framing','4. State the problem')),
 ('State what work is included and what is excluded to make the scope boundary explicit.',atl('work-management/project-management/project-scope','Define project scope')))
add(1,
 ('A structured interview uses an interview script rather than a flexibly ordered interview guide.',nn('interview-guide','Introduction')),
 ('Define what needs to be learned and prepare questions that address those aims.',nn('interview-guide','Step 1: Write Your Research Questions; Step 4: Fill In for Unaccounted Research Questions')),
 ('Ask concise, open-ended questions that let the participant describe their experience without suggesting the answer.',nn('interview-guide','Step 3: Broaden Your Questions')),
 ('Record the elicited needs in a shared requirements document with links to the supporting interview context.',atl(req,'Step 4: Document requirements in one shared place')))
add(2,
 ('A workshop uses goal-oriented group activities and discussion to produce shared outcomes.',nn('ux-workshop-agendas','The Process')),
 ('Build the agenda by defining goals, identifying questions needed to reach them, and choosing activities that answer those questions.',nn('ux-workshop-agendas','Step 1; Step 2; Step 3')),
 ('Allocate time to each workshop segment and prepare the materials needed to capture discussion.',nn('ux-workshop-agendas','The Output: Sample Workshop Agenda')),
 ('Guide discussion toward the agenda goals and analyze and share the collected outputs after the workshop.',nn('ux-workshop-agendas','Step 4; Step 5')))
# Tile 01.01.02.
add(3,
 ('Surveys are best suited to collecting quantitative attitudinal data rather than detailed accounts of behavior.',nn('survey-best-practices','Don’t Ask Questions that Respondents Can’t Answer Accurately')),
 ('Include questions needed to answer the research aims rather than collecting information simply because it is easy to ask for.',nn('survey-best-practices','Don’t Ask Questions that You Can Find the Answer to')),
 ('Write questions that respondents can answer accurately and avoid language that leads them toward a preferred answer.',nn('survey-best-practices','Don’t Ask Questions that Respondents Can’t Answer Accurately; Avoid Biasing Respondents')))
add(4,
 ('Existing documentation is one channel for gathering requirements.',atl(req,'Step 3: Collect input through the right channels')),
 ('Capture requirements, assumptions, constraints, and open questions in one shared place with links to supporting context.',atl(req,'Step 4: Document requirements in one shared place')),
 ('Confirm the documented requirements with stakeholders before treating them as execution work.',atl(req,'Step 5: Prioritize and validate requirements')))
add(5,
 ('Observation examines what users do in their work context rather than relying solely on their account of what they do.',nn('task-analysis','Stage 1: Gather Information')),
 ('Watch the user perform work, then ask questions about what was observed.',nn('task-analysis','Stage 1: Gather Information — Contextual inquiry')),
 ('Record the tasks performed and analyze their sequence and subtasks to understand how the goal is achieved.',nn('task-analysis','Stage 2: Analyze Tasks')))
add(6,
 ('Validation with stakeholders confirms priorities and agreement about what will be delivered.',atl(req,'Step 5: Prioritize and validate requirements')),
 ('Review documented requirements and open questions with stakeholders before requirements become execution work.',atl(req,'Step 4; Step 5')))
# Tile 01.01.03.
add(7,
 ('A low-fidelity prototype is an inexpensive, relatively simple representation used to explore and test a design.',nn('ux-prototype-hi-lo-fidelity','Low-Fidelity Prototyping')),
 ('Sketch a wireframe by drawing the screen’s main content areas and controls without detailed visual styling.',nn('draw-wireframe-even-if-you-cant-draw','Drawing Your First Wireframe')),
 ('Use a prototype to gather feedback about a design before investing in a fully implemented version.',nn('ux-prototype-hi-lo-fidelity','Introduction; Low-Fidelity Prototyping')))
add(8,
 ('Brainstorming generates alternative ideas for a shared problem.',atl('team-playbook/plays/disruptive-brainstorming','What is disruptive brainstorming?')),
 ('Set a time limit and have participants write down ideas before sharing them.',atl('team-playbook/plays/disruptive-brainstorming','Instructions for running this Play')),
 ('Keep idea generation separate from judging ideas so participants can explore possibilities.',atl('team-playbook/plays/disruptive-brainstorming','Instructions for running this Play')))
add(9,
 ('A focus group is a moderated discussion that gathers participants’ attitudes and opinions.',nn('focus-groups','Introduction')),
 ('Prepare a moderator script with specific issues and goals for the information to be gathered.',nn('focus-groups','Getting Focused')),
 ('Keep discussion on topic, invite all participants to contribute, and prevent one participant from dominating.',nn('focus-groups','Getting Focused')),
 ('Summarize the prevailing opinions and disagreements rather than treating group discussion as evidence of actual product use.',nn('focus-groups','Getting Focused; Introduction')))
add(10,
 ('Gather information about known risks, blockers, and dependencies while eliciting requirements.',atl(req,'Step 3: Collect input through the right channels')),
 ('A risk matrix evaluates a risk using its likelihood and impact.',atl('work-management/project-management/risk-matrix','What is a risk matrix?')),
 ('Assess likelihood and impact for each identified risk and use its matrix position to determine a risk level.',atl('work-management/project-management/risk-matrix','How to create a risk matrix')))
# Tile 01.02.01.
add(11,
 ('Business requirements express the broader business goal or outcome the work should support.',atl(req,'Types of project requirements to gather')),
 ('A requirements document can contain a project summary, goals and success metrics, in-scope and out-of-scope items, requirements, assumptions, and constraints.',atl(req,'Step 4: Document requirements in one shared place')),
 ('Organize the elicited requirements in that shared structure and review them with approvers to agree what will be delivered.',atl(req,'Step 4; Step 5')))
add(12,
 ('Functional requirements state what the deliverable must do.',atl(req,'Types of project requirements to gather')),
 ('Document the expected functions separately from the broader business outcome and from how the solution should perform.',atl(req,'Types of project requirements to gather; Step 4')))
add(13,
 ('A user story describes a desired outcome from a user’s perspective.', 'atlassian_user_stories#What are agile user stories?'),
 ('Write a story as “As a [persona], I [want to], [so that].” to state the user, need, and purpose.', 'atlassian_user_stories#User story template and examples'),
 ('Acceptance criteria describe specific conditions that must be satisfied for the story to be accepted.',atl('agile/project-management/user-stories','How to write user stories')))
add(14,
 ('A use case specifies behavior that provides an observable result of value to an actor or other stakeholder.','uml_spec#18.1.3.1'),
 ('An actor represents a role interacting with the subject and may be a person or another system.','uml_spec#18.1.3.1'),
 ('Describe a use case’s behavior in natural language with relevant preconditions and postconditions.','uml_spec#18.1.3.1'),
 ('Include the basic interaction and relevant variations, exceptional behavior, or error handling.','uml_spec#18.1.3.1'))
add(15,
 ('Requirements traceability connects requirements to related delivery work and tests.',atl('software/jira/templates/requirements-traceability-matrix','What is a requirements traceability matrix template?')),
 ('Link each requirement to relevant tasks or test cases so the relationship can be followed between high-level requirements and specific work.',atl('software/jira/templates/requirements-traceability-matrix','Linking work items')),
 ('When a requirement changes, follow its links to identify affected work items that need updating.',atl('software/jira/templates/requirements-traceability-matrix','Linking work items')))
add(16,
 ('Requirements documentation needs updating as development and learning change the understanding of the work.',atl('agile/product-management/requirements','The challenges product requirements documents')),
 ('Track the current program status and keep requirements linked to current work-item status.',atl('agile/product-management/requirements','Define project specifics; Living stories')),
 ('For a changed requirement, identify and update related work through its traceability links.',atl('software/jira/templates/requirements-traceability-matrix','Linking work items')))
add(17,
 ('Nonfunctional requirements describe how the solution should perform or operate rather than the functions it must provide.',atl(req,'Types of project requirements to gather')),
 ('A measurable nonfunctional requirement states a concrete performance target, such as the source’s requirement that the system load within two seconds.',atl(req,'Types of project requirements to gather')))
# Tile 02.01.01.
add(18,
 ('A stakeholder is someone interested in the work or someone whose involvement is needed to complete it.',nn('stakeholder-analysis','Who’s a Stakeholder?')),
 ('Identify people who use, provide input to, approve, fund, or are affected by the deliverable.',atl(req,'Step 2: Identify stakeholders and decision-makers')),
 ('Classify stakeholders as directly involved or affected, indirectly affected or consulted, and reviewers or approvers, noting that roles can overlap.',atl(req,'Step 2: Identify stakeholders and decision-makers')),
 ('Record each stakeholder’s role and assess their interest and power over the work.',nn('stakeholder-analysis','Who’s a Stakeholder?; Stakeholder Analysis')))
add(19,
 ('Plot stakeholders on a grid with separate low-to-high power and interest axes.',nn('stakeholder-analysis','Stakeholder Analysis')),
 ('Manage high-power, high-interest stakeholders closely.',nn('stakeholder-analysis','Manage Closely')),
 ('Keep high-power, low-interest stakeholders satisfied.',nn('stakeholder-analysis','Keep Satisfied')),
 ('Keep low-power, high-interest stakeholders informed.',nn('stakeholder-analysis','Keep Informed')),
 ('Monitor low-power, low-interest stakeholders with less intensive engagement.',nn('stakeholder-analysis','Monitor')))
add(20,
 ('A RACI chart assigns roles by task to clarify who does work and who owns the outcome.',atl('work-management/project-management/raci-chart','What is a RACI chart?')),
 ('Responsible identifies the person or people doing the work.',atl('work-management/project-management/raci-chart','Responsible')),
 ('Accountable identifies the one person ultimately answerable for a task’s completion.',atl('work-management/project-management/raci-chart','Accountable')),
 ('Consulted identifies people whose input is needed, using two-way communication.',atl('work-management/project-management/raci-chart','Consulted')),
 ('Informed identifies people kept updated, using one-way communication.',atl('work-management/project-management/raci-chart','Informed')),
 ('List tasks against stakeholders and assign the appropriate R, A, C, or I entries, checking that each task has one accountable owner.',atl('work-management/project-management/raci-chart','How to create a RACI chart')))
add(21,
 ('A communication plan turns stakeholder analysis into specific ongoing engagement actions.',nn('stakeholder-analysis','Adding Attitude')),
 ('For each stakeholder group, specify the communication goal, channel, frequency, and owner.',atl('team-playbook/plays/stakeholder-communications-plan','Instructions for running this Play')),
 ('Match communication intensity to stakeholder power and interest and review whether the approach is effective.',nn('stakeholder-analysis','Stakeholder Analysis; Summary')))
# Tile 02.02.01.
add(22,
 ('Facilitation guides a group’s process rather than imposing the facilitator’s preferred content.',nn('workshop-facilitation-101','Workshop-Facilitation Principles')),
 ('Use an agenda whose activities and allotted time support the meeting’s goals.',nn('ux-workshop-agendas','The Output: Sample Workshop Agenda')),
 ('Redirect dominating contributions toward shared goals or invite other participants to balance the discussion.',nn('dominating-workshop-participants','How to Navigate Dominating Behaviors in a Workshop')),
 ('Use silent individual contributions when verbal discussion prevents equitable participation.',nn('dominating-workshop-participants','Tactic #3: Silence the Contributions')))
add(23,
 ('Different stakeholders may have conflicting goals and different measures of success.',nn('collaborating-stakeholders','Introduction')),
 ('Build shared understanding by involving stakeholders in discussion of goals and evidence rather than presenting an isolated solution.',nn('collaborating-stakeholders','Collaborate')),
 ('Forced ranking or dot voting can help a group move toward consensus.',nn('ux-workshop-agendas','Step 3: Pick processes that will answer the questions')))
# Tile 03.01.01.
add(24,
 ('An event is something that happens during a process and is drawn as a circle.','bpmn_spec#7.2.1 — Basic BPMN Modeling Elements'),
 ('A task is an atomic activity and is drawn as a rounded rectangle.','bpmn_spec#10.3.3 — Task'),
 ('A gateway controls branching and convergence of sequence flows and is drawn as a diamond.','bpmn_spec#7.2.1 — Basic BPMN Modeling Elements'),
 ('Sequence flow is a solid line with a solid arrowhead indicating the order of activities within a process.','bpmn_spec#8.4.13 — Sequence Flow'),
 ('Message flow is a dashed line with an open arrowhead and open circle showing messages between separate participants.','bpmn_spec#9.4 — Message Flow'),
 ('Draw activities and appropriate events or gateways, connecting execution order with sequence flows and communication between participants with message flows.','bpmn_spec#7.2.1 — Basic BPMN Modeling Elements'))
add(25,
 ('An as-is process map records the current process rather than a proposed redesign.',atl('work-management/project-management/process-mapping','Benefits of process mapping')),
 ('Identify the process’s start and end, collect information about its steps and decisions, and determine their sequence.',atl('work-management/project-management/process-mapping','How to create a process map')),
 ('Represent the observed activities and routing with BPMN tasks, events, gateways, and sequence flows.','bpmn_spec#7.2.1 — Basic BPMN Modeling Elements'),
 ('Review the map with those who perform the process to refine its accuracy.',atl('work-management/project-management/process-mapping','How to create a process map')))
add(26,
 ('A future-state process map shows how the process is intended to work after improvement.',atl('work-management/project-management/process-mapping','Benefits of process mapping')),
 ('Use the current-state map to identify improvements and draw a revised map reflecting the proposed changes.',atl('work-management/project-management/process-mapping','Benefits of process mapping; How to create a process map')),
 ('Use BPMN tasks, events, gateways, and sequence flows to represent the revised activities and routing.','bpmn_spec#7.2.1 — Basic BPMN Modeling Elements'))
# Tile 03.01.02.
add(27,
 ('Process mapping can expose bottlenecks, redundant efforts, and unnecessary steps.',atl('work-management/project-management/process-mapping','Benefits of process mapping')),
 ('Inspect the mapped steps and handoffs for obstacles that impede efficient flow.',atl('work-management/project-management/process-mapping','How to create a process map')),
 ('Compare current-state and future-state maps to identify specific differences and potential efficiency gains.',atl('work-management/project-management/process-mapping','Benefits of process mapping')))
add(28,
 ('Lean process improvement aims to eliminate waste and improve value delivered by a process.',atl('agile/project-management/lean-process-improvement','What is Lean process improvement?')),
 ('Inspect a process for non-value-adding steps and propose a change that removes or reduces the identified waste.',atl('agile/project-management/lean-process-improvement','Lean process improvement principles')))
add(29,
 ('Requirements documentation includes assumptions and constraints that govern the work.',atl(req,'Step 4: Document requirements in one shared place')),
 ('Capture required approvals and operating constraints explicitly when documenting what the deliverable must do.',atl(req,'Types of project requirements to gather; Step 4')))
# Tile 03.01.03. Only source-supported decision logic is retained; source gaps are reported separately.
add(30,
 ('Conditional decision logic associates a condition with a result to use when the condition is true.',pg('9.18.1 — CASE')),
 ('Check which outcomes apply to the specified conditions rather than leaving the decision as an unspecified instruction.',pg('9.18.1 — CASE')))
add(31,
 ('A decision tree represents choices and possible outcomes with branches.',atl('work-management/project-management/decision-tree','What is a decision tree?')),
 ('Start with the initial decision, add branches for the possible answers, and continue with subsequent decisions and their outcomes.',atl('work-management/project-management/decision-tree','How to create a decision tree')))
# Tile 04.01.01.
add(32,
 ('Dimension tables describe business entities, and their non-key columns describe attributes of those entities.',pbi('guidance/star-schema','Understand star schema')),
 ('Identify the business things that need describing and list the descriptive attributes needed for each.',pbi('guidance/star-schema','Understand star schema')))
# Tile 04.01.03.
add(37,
 ('Relationship cardinality expresses how many instances on either side can be related.', 'uml_spec#7.5.3 — Multiplicities'),
 ('A one-to-many relationship has a column with unique values on one side and potentially repeated matching values on the other.',pbi('transform-model/desktop-create-and-manage-relationships','Cardinality')),
 ('A many-to-many relationship permits repeated matching values on both sides.',pbi('transform-model/desktop-create-and-manage-relationships','Cardinality')),
 ('Determine the relationship by checking whether each side permits one or multiple matching instances.',pbi('transform-model/desktop-create-and-manage-relationships','Cardinality')))
add(38,
 ('A model diagram can show entity types, their attributes, and relationships between instances.', ['uml_spec#11.4 — Classes','uml_spec#11.5 — Associations']),
 ('Draw named entity boxes with their relevant attributes and connect related entities, marking the permitted multiplicities.', ['uml_spec#11.4.4 — Notation','uml_spec#11.5.4 — Notation','uml_spec#7.5.4 — Notation']))
add(39,
 ('A model can express business meaning through named entities, descriptive attributes, and relationships.', ['uml_spec#11.4 — Classes','uml_spec#11.5 — Associations']),
 ('The amount of model detail can be chosen to communicate with its intended readers.','uml_spec#18.1.3.1'))
add(40,
 ('Business entities and their descriptive attributes give a model the information used to describe a business domain.',pbi('guidance/star-schema','Understand star schema')),
 ('Choose the entities and attributes needed to support the intended reporting and filtering requirements.',pbi('guidance/star-schema','Star schema relevance to Power BI semantic models')))
# Tile 05.01.01.
add(42,
 ('SELECT retrieves data from a table; the select list names the desired output columns.',pg('2.5 — Querying a Table')),
 ('Write SELECT column1, column2, column3 FROM table_name; to retrieve the named columns.',pg('2.5 — Querying a Table')),
 ('SELECT * FROM table_name; retrieves all columns.',pg('2.5 — Querying a Table')))
# Tile 05.01.02.
add(44,
 ('GROUP BY creates one result group for rows with the same grouping-column values.',pg('7.2.3 — The GROUP BY and HAVING Clauses')),
 ('SUM computes a total, COUNT(*) counts rows, and AVG computes an arithmetic mean.',pg('2.7 — Aggregate Functions')),
 ('Write SELECT group_column, SUM(value_column) FROM table_name GROUP BY group_column; for one total per group.',pg('7.2.3 — The GROUP BY and HAVING Clauses')),
 ('Selected columns outside aggregate functions must be grouped unless they are functionally dependent on the grouping columns.',pg('7.2.3 — The GROUP BY and HAVING Clauses')))
add(45,
 ('WHERE selects input rows before grouping and aggregate calculation.',pg('2.7 — Aggregate Functions')),
 ('HAVING selects groups after grouping and aggregate calculation.',pg('2.7 — Aggregate Functions')),
 ('Use SELECT group_column, SUM(value_column) FROM table_name WHERE row_condition GROUP BY group_column HAVING SUM(value_column) > threshold; to apply both kinds of filtering.',pg('7.2.3 — The GROUP BY and HAVING Clauses')),
 ('In comparisons, = means equal, <> means not equal, and < or > means less or greater than.',pg('9.2 — Comparison Functions and Operators')))
add(46,
 ('SQL column types distinguish integers, exact numeric values, text, dates, and Boolean values, among other types.',pg('8 — Data Types, Table 8.1')),
 ('Choose a column type whose value category and range fit the information being stored.',pg('8 — Data Types, Table 8.1')),
 ('NULL represents an unknown value, and ordinary comparisons with NULL yield unknown rather than true or false.',pg('9.2 — Comparison Functions and Operators')),
 ('Use WHERE column_name IS NULL or WHERE column_name IS NOT NULL to test for missing values rather than = NULL.',pg('9.2 — Comparison Functions and Operators')),
 ('COALESCE(value, replacement) returns the first non-NULL argument; use it in the SELECT list to substitute for a missing value.',pg('9.18.2 — COALESCE')),
 ('WHERE retains only rows whose condition is true, so unknown results from NULL comparisons do not pass its filter.',pg('7.2.2 — The WHERE Clause')))
# Tile 05.02.01: join variants use the same authoritative section.
for i,kind,side in [(47,'LEFT','left'),(48,'RIGHT','right')]:
 other='right' if side=='left' else 'left'
 add(i,
  (kind+' OUTER JOIN returns matching combinations and preserves each unmatched '+side+'-table row.',pg('7.2.1.1 — Joined Tables')),
  ('For an unmatched '+side+' row, columns from the '+other+' table are filled with NULL.',pg('7.2.1.1 — Joined Tables')),
  ('Write SELECT a.column_name, b.column_name FROM table_a AS a '+kind+' OUTER JOIN table_b AS b ON a.key_column = b.key_column; with the table to preserve on the '+side+'.',pg('7.2.1.1 — Joined Tables')))
add(49,
 ('FULL OUTER JOIN returns matching combinations and preserves unmatched rows from both tables.',pg('7.2.1.1 — Joined Tables')),
 ('Columns on the missing side of an unmatched row are filled with NULL.',pg('7.2.1.1 — Joined Tables')),
 ('Write SELECT a.column_name, b.column_name FROM table_a AS a FULL OUTER JOIN table_b AS b ON a.key_column = b.key_column; to preserve unmatched rows on either side.',pg('7.2.1.1 — Joined Tables')))
# Tile 05.02.02.
add(50,
 ('Without ORDER BY, a query’s output order is unspecified.',pg('7.5 — Sorting Rows (ORDER BY)')),
 ('ORDER BY column ASC sorts ascending and ORDER BY column DESC sorts descending; ASC is the default.',pg('7.5 — Sorting Rows (ORDER BY)')),
 ('Write ORDER BY first_column ASC, second_column DESC to sort by the first column and break its ties with the second.',pg('7.5 — Sorting Rows (ORDER BY)')),
 ('When not otherwise specified, NULL values sort last for ASC and first for DESC; NULLS FIRST or NULLS LAST overrides that placement.',pg('7.5 — Sorting Rows (ORDER BY)')))
add(51,
 ('For a top-N report, compute the metric per group, order it descending, and limit the output: SELECT group_column, SUM(value_column) AS total FROM table_name GROUP BY group_column ORDER BY total DESC, group_column LIMIT n;', [pg('7.2.3 — The GROUP BY and HAVING Clauses'),pg('7.5 — Sorting Rows (ORDER BY)'),pg('7.6 — LIMIT and OFFSET')]),
 ('A predictable limited result requires an ordering that determines which rows come first.',pg('7.6 — LIMIT and OFFSET')),
 ('LAG(metric) OVER (ORDER BY period_column) retrieves the previous row’s metric for an ordered period comparison; the first row has NULL by default.',pg('9.22 — Window Functions')),
 ('SUM(metric) OVER (ORDER BY period_column ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) computes an ordered running total over the rows through the current row.', [pg('3.5 — Window Functions'),pg('9.22 — Window Functions')]))
# Tile 06.01.01.
add(52,
 ('In Power BI Desktop, Home > Get data selects a connector and connects to a data source.',pbi('fundamentals/desktop-getting-started','Connect to data')),
 ('Choose Transform Data to open Power Query Editor and shape the data before loading it.',pbi('connect-data/desktop-shape-and-combine-data','Shape data')),
 ('Change a column’s data type and remove unnecessary columns using the editor’s column commands; the transformations are recorded as applied steps.',pbi('connect-data/desktop-shape-and-combine-data','Shape data')),
 ('Use Close & Apply to apply the transformations and load the shaped data.',pbi('connect-data/desktop-shape-and-combine-data','Shape data')))
add(53,
 ('Select a connector in Tableau’s Connect pane and provide the source-specific connection information.',tab('basicconnectoverview','Connect to your data')),
 ('To create a physical join, drag the first table to the canvas, double-click it, then drag another table into that join canvas.',tab('joining_tables','Create a join')),
 ('Select the join type and matching fields in the join dialog; inner keeps matches, left or right preserves its named side, and full outer preserves both sides.',tab('joining_tables','Join types; Join Clauses')),
 ('An extract is a saved snapshot of data for analysis; select Extract on the Data Source page and configure the extract before saving it.',tab('extracting_data','Create an extract')))
# Tile 07.01.01.
add(54,
 ('A current-state assessment describes the present situation as a baseline for identifying improvements.',atl('software/confluence/templates/gap-analysis','Assess current state')),
 ('Record detailed notes about the current business situation in a structured current-state column.',atl('software/confluence/templates/gap-analysis','Assess current state')))
add(55,
 ('A desired-state definition states the objectives and situation the business wants to achieve.',atl('software/confluence/templates/gap-analysis','Define the desired state')),
 ('Express the goal using a business outcome and measurable success target.',atl(req,'Step 1: Define the project goal')))
add(56,
 ('A gap is a specific difference between the current situation and the desired state.',atl('software/confluence/templates/gap-analysis','Identify gaps')),
 ('Compare the current-state description with the desired-state objectives and list the specific differences keeping the business from those goals.',atl('software/confluence/templates/gap-analysis','Assess current state; Define the desired state; Identify gaps')))
add(57,
 ('SWOT separates strengths, weaknesses, opportunities, and threats in a business situation.',atl('work-management/strategic-planning/swot-analysis','What is a SWOT analysis?')),
 ('Strengths are internal advantages; weaknesses are internal limitations.',atl('work-management/strategic-planning/swot-analysis','Strengths; Weaknesses')),
 ('Opportunities are favorable external possibilities; threats are external factors that could harm success.',atl('work-management/strategic-planning/swot-analysis','Opportunities; Threats')),
 ('Create four labeled quadrants and place each factor according to whether it is internal or external and favorable or unfavorable.',atl('work-management/strategic-planning/swot-analysis','How to conduct a SWOT analysis')))
# Tile 07.02.01.
add(58,
 ('MoSCoW groups requirements as Must have, Should have, Could have, or Will not have for the scope being prioritized.',nn('prioritization-methods','4.A. Overview; 4.C. Process')),
 ('Must-have items are essential: without them the solution would not work or the project would be useless.',nn('prioritization-methods','4.B. Criteria')),
 ('Should-have items are important but the solution can still work without them.',nn('prioritization-methods','4.B. Criteria')),
 ('Could-have items are desirable but nonessential and have a smaller impact if omitted.',nn('prioritization-methods','4.B. Criteria')),
 ('Will-not-have items are not needed within the prioritization scope and can be deprioritized or dropped.',nn('prioritization-methods','4.B. Criteria; 4.C. Process')),
 ('Define the prioritization scope, discuss each item’s importance, and assign the category the group agrees fits it.',nn('prioritization-methods','4.C. Process')))
add(59,
 ('Kano classifies features by how functionality relates to customer satisfaction.',nn('prioritization-methods','5.A. Overview')),
 ('Must-be or basic features are expected; their absence causes dissatisfaction, while their presence adds little satisfaction.',nn('prioritization-methods','5.C. Process — Must-be')),
 ('Performance features produce more satisfaction as their functionality improves.',nn('prioritization-methods','5.C. Process — Performance')),
 ('Attractive or excitement features can delight users who did not expect them and may not notice their absence.',nn('prioritization-methods','5.C. Process — Attractive')),
 ('Use user evidence about satisfaction and the feature’s functionality to classify and discuss the appropriate category.',nn('prioritization-methods','5.C. Process')))
add(60,
 ('A weighted decision matrix compares options on criteria whose weights represent importance.',atl('software/confluence/templates/decision-matrix','Assign weights to each criterion')),
 ('List the criteria and options, assign criterion weights, and score every option against each criterion using a consistent scale.',atl('software/confluence/templates/decision-matrix','Define decision criteria; Assign weights; List the options; Score each option')),
 ('Multiply each criterion score by its weight and add those products for the option’s total weighted score.',atl('software/confluence/templates/decision-matrix','Calculate the weighted scores and make a decision')),
 ('Compare the totals to rank the options; the highest total is typically the best choice under the chosen criteria and weights.',atl('software/confluence/templates/decision-matrix','Calculate the weighted scores and make a decision')))
# Tile 07.02.02.
add(61,
 ('Solution comparison uses defined decision criteria rather than an unstructured preference.',atl('software/confluence/templates/decision-matrix','Define decision criteria')),
 ('Score each candidate solution against the same criteria and multiply the scores by the corresponding importance weights.',atl('software/confluence/templates/decision-matrix','Score each option; Calculate the weighted scores')),
 ('Sum each candidate’s weighted scores, compare the totals, and explain the recommendation in terms of the criteria and scores.',atl('software/confluence/templates/decision-matrix','Calculate the weighted scores and make a decision')))
add(62,
 ('A business case justifies an initiative by describing the problem, possible solutions, expected benefits, and costs.',atl('work-management/project-management/business-case','What is a business case?; Key elements of a business case')),
 ('List and estimate relevant costs and benefits over the period being evaluated, including direct and indirect effects.',atl('work-management/strategic-planning/cost-benefit-analysis','Key components of a cost-benefit analysis')),
 ('Compare the quantified costs and benefits and explain whether the proposed initiative merits the investment.',atl('work-management/strategic-planning/cost-benefit-analysis','How to perform a cost-benefit analysis')),
 ('Present the recommendation with the supporting financial assessment in the business case.',atl('work-management/project-management/business-case','Key elements of a business case')))
add(63,
 ('A decision matrix enables comparison across several criteria using explicit importance weights and scores.',atl('software/confluence/templates/decision-matrix','What is a decision matrix template?')),
 ('Define relevant criteria, establish weights, and score the options consistently against each criterion.',atl('software/confluence/templates/decision-matrix','How to use the decision matrix template')),
 ('Calculate each option’s total as the sum of score times weight across the criteria, then compare totals for a defensible ranking.',atl('software/confluence/templates/decision-matrix','Calculate the weighted scores and make a decision')))
# Tile 08.01.01.
add(66,
 ('A user story states a persona’s need and its purpose using “As a [persona], I [want to], [so that].”','atlassian_user_stories#User story template and examples'),
 ('INVEST stands for Independent, Negotiable, Valuable, Estimable, Small, and Testable.',atl('agile/scrum/backlog-refinement','INVEST')),
 ('Refine oversized backlog items by breaking them into smaller, more precise items with clearer descriptions.', 'scrum_guide#Product Backlog'),
 ('Split larger stories into smaller stories that can be completed within an iteration.', 'atlassian_user_stories#How to write user stories'))
add(67,
 ('A product backlog is an emergent, ordered list of work needed to improve the product.', 'scrum_guide#Product Backlog'),
 ('Refinement breaks items into smaller, more precise items and adds details such as description, order, and size.', 'scrum_guide#Product Backlog'),
 ('Review unclear or oversized items, clarify their details, split them as needed, and keep the backlog ordered.', 'scrum_guide#Product Backlog'),
 ('Items that can be completed within one iteration are ready for selection; refinement usually provides the needed transparency.', 'scrum_guide#Product Backlog'))
add(68,
 ('A roadmap sequences planned work against goals rather than listing disconnected features.',atl('agile/product-management/roadmaps','What is a product roadmap?')),
 ('Sequence work by considering priorities, dependencies, and the resources available for delivery.',atl('agile/product-management/roadmaps','How to create a product roadmap')),
 ('Review the sequence as priorities and information change rather than treating the initial roadmap as fixed.',atl('agile/product-management/roadmaps','Who is responsible for the product roadmap?')))
# Tile 08.01.02.
add(69,
 ('Acceptance criteria state the conditions used to determine whether a particular user story is satisfied.','atlassian_user_stories#How to write user stories'),
 ('Discuss what completing the story means and document that shared understanding as criteria.','atlassian_user_stories#How to write user stories'),
 ('Refinement adds detail to make backlog items more precise and understandable.','scrum_guide#Product Backlog'))
# Tile 09.01.01.
add(70,
 ('A report should be structured for its readers rather than assuming the findings speak for themselves.',nn('engaging-reports-presentations','Introduction; Structure Your Report for 3 Audiences')),
 ('Put the key message in headlines for readers who only scan, then provide highlights and supporting detail for readers who need more.',nn('engaging-reports-presentations','Structure Your Report for 3 Audiences')),
 ('Write at the level of detail the audience needs and select information that serves the report’s purpose.',nn('lean-agile-documentation','Documentation Throughout Agile Product Development')))
add(71,
 ('The audience determines appropriate detail, terminology, and how information is communicated.',nn('lean-agile-documentation','Documentation Throughout Agile Product Development')),
 ('Use the audience’s language and explain an unfamiliar concept with a familiar analogy when useful.',nn('engaging-reports-presentations','Using Storytelling in Asynchronous Mediums')),
 ('Make the main ideas clear in headlines while preserving supporting detail for readers who need it.',nn('engaging-reports-presentations','Structure Your Report for 3 Audiences')))
# Tile 09.01.02.
add(72,
 ('A presentation needs a narrative that makes findings meaningful to its audience rather than a bare list of data.',nn('engaging-reports-presentations','Introduction')),
 ('Structure the presentation around clear headlines, highlights, and supporting detail appropriate to different reader needs.',nn('engaging-reports-presentations','Structure Your Report for 3 Audiences')),
 ('Use audience-appropriate language and connect findings to the recommendation being communicated.',nn('engaging-reports-presentations','Using Storytelling in Asynchronous Mediums')))
add(73,
 ('Requirements review gives stakeholders and approvers the opportunity to confirm priorities and agree what will be delivered.',atl(req,'Step 5: Prioritize and validate requirements')),
 ('Plan a review around the documented goal, scope, requirements, assumptions, and open questions.',atl(req,'Step 4: Document requirements in one shared place')),
 ('Record decisions in the shared requirements document so agreement and unresolved questions remain visible.',atl(req,'Step 4: Document requirements in one shared place')))
# Tile 10.01.01.
add(74,
 ('A context diagram represents the system as a single element with a boundary separating it from external entities.',atl('work-management/project-management/context-diagram','What is a system context diagram?')),
 ('Define the system’s purpose and boundary and identify its external actors and connected systems.',atl('work-management/project-management/context-diagram','How to create a system context diagram')),
 ('Draw the system centrally, place external entities around it, and use labeled directional arrows to show exchanges.',atl('work-management/project-management/context-diagram','How to create a system context diagram')))
add(75,
 ('Hierarchical task analysis decomposes a goal into major tasks and those tasks into subtasks.',nn('task-analysis','Stage 2: Analyze Tasks')),
 ('Start with the goal, draw the major tasks beneath it, and break each top-level task into its relevant subtasks.',nn('task-analysis','Stage 2: Analyze Tasks')),
 ('Choose the number of decomposition levels according to the complexity and detail needed.',nn('task-analysis','Stage 2: Analyze Tasks')))
# Tile 10.01.02.
def excel(page,section):return 'excel_support#en-us/excel/'+page+' — '+section
add(76,
 ('A spreadsheet formula starts with = and may combine cell references, operators, and functions.',excel('get-started/overview-of-formulas-in-excel','The parts of an Excel formula')),
 ('A relative reference such as A1 changes when the formula is copied to a different position.',excel('get-started/overview-of-formulas-in-excel','Using references in Excel formulas')),
 ('An absolute reference such as $A$1 keeps its row and column fixed when copied; $A1 or A$1 fixes just one part.',excel('switch-between-relative-absolute-and-mixed-references','Relative; Absolute; Mixed references')),
 ('Use =SUM(range) to total values, =AVERAGE(range) for their arithmetic mean, and =COUNT(range) to count numeric cells.',[excel('functions/sum-function','Syntax'),excel('functions/average-function','Syntax'),excel('functions/count-function','Syntax')]),
 ('Copy a formula containing relative and fixed references and inspect how each reference changes according to the destination.',excel('switch-between-relative-absolute-and-mixed-references','Relative; Absolute; Mixed references')),
 ('AVERAGE ignores empty cells and text in a referenced range but includes cells containing zero.',excel('functions/average-function','Remarks')))
add(78,
 ('A lookup retrieves a value associated with a matching key.',excel('functions/xlookup-function','Introduction')),
 ('Use =XLOOKUP(key, lookup_range, return_range) to find a key and return the corresponding value; exact match is the default.',excel('functions/xlookup-function','Syntax')),
 ('Use =VLOOKUP(key, table_range, column_number, FALSE) for an exact match in the first column and a return value from the specified column to its right.',excel('functions/vlookup-function','Syntax; How to get started')),
 ('If VLOOKUP’s final argument is omitted or TRUE, it uses approximate matching and expects the first column sorted.',excel('functions/vlookup-function','Syntax')),
 ('Use =INDEX(return_range, MATCH(key, lookup_range, 0)) to return the value at the exact key’s position.',[excel('functions/index-function','Array form'),excel('functions/match-function','Syntax')]))
add(79,
 ('IF(logical_test, value_if_true, value_if_false) returns one of two results according to the test.',excel('functions/if-function','Syntax')),
 ('Use =IF(test1, result1, IF(test2, result2, result3)) to express three ordered alternatives.',excel('functions/if-function','Use IF to check if a cell is blank; Nested IF')),
 ('IFS(test1, result1, test2, result2, ...) returns the result for the first true condition.',excel('functions/ifs-function','Syntax')),
 ('A final TRUE condition in IFS supplies a default result; without a true condition, IFS returns #N/A.',excel('functions/ifs-function','Remarks')))
add(80,
 ('Choose the visualization according to the question: bars compare categories and lines show trends over time.',tab('visual_best_practices','Choose the right chart type')),
 ('Give the chart a clear title and labels so readers can interpret the intended comparison.',pbi('create-reports/service-dashboards-design-tips','Consider your audience; Tell a story on one screen')))
add(81,
 ('Start by clarifying the business outcome or question the analysis should address.',atl(req,'Step 1: Define the project goal')),
 ('A spreadsheet pivot table can summarize source data with fields placed in Rows, Columns, and Values.', 'excel_support#Create a PivotTable to analyze worksheet data — Build out your PivotTable'),
 ('Present the answer prominently and include enough supporting detail for the audience to understand it.',nn('engaging-reports-presentations','Structure Your Report for 3 Audiences')))
# Tile 10.02.01.
add(82,
 ('Sprint Planning collaboratively establishes the work for the iteration.', 'scrum_guide#Sprint Planning'),
 ('The Product Owner prepares discussion of important backlog items; Developers select work through that discussion.', 'scrum_guide#Sprint Planning'),
 ('Inspect candidate items for clear descriptions and sufficient detail, and refine uncertain items before selection.', 'scrum_guide#Sprint Planning; Product Backlog'),
 ('Selection considers the Developers’ capacity and past performance rather than an externally imposed commitment.', 'scrum_guide#Sprint Planning'))
add(83,
 ('The Product Owner is accountable for maximizing product value and effective backlog management.', 'scrum_guide#Product Owner'),
 ('The Product Owner may delegate backlog-management work but remains accountable for it.', 'scrum_guide#Product Owner'),
 ('Developers are responsible for sizing the work and deciding how selected work is performed.', 'scrum_guide#Product Backlog; Sprint Planning'),
 ('Clarify backlog items collaboratively while respecting the Product Owner’s ordering accountability and the Developers’ delivery decisions.', 'scrum_guide#Product Owner; Product Backlog; Sprint Planning'))
add(84,
 ('The Daily Scrum is a 15-minute event for Developers focused on progress toward the Sprint Goal and an actionable plan.', 'scrum_guide#Daily Scrum'),
 ('Participation by other Scrum accountabilities as Developers depends on actively working on iteration backlog items.', 'scrum_guide#Daily Scrum'),
 ('Give an update that identifies an impediment or needed coordination affecting the goal and the next work plan.', 'scrum_guide#Daily Scrum'),
 ('Move detailed replanning discussion outside the Daily Scrum rather than extending the event.', 'scrum_guide#Daily Scrum'))
add(85,
 ('The Sprint Review inspects the outcome with stakeholders and determines future adaptations; it is a working session rather than just a presentation.', 'scrum_guide#Sprint Review'),
 ('Acceptance criteria provide the story-specific conditions used to judge whether delivered behavior satisfies the need.', 'atlassian_user_stories#How to write user stories'),
 ('Compare the demonstrated behavior with those conditions and discuss differences with the stakeholders.', ['scrum_guide#Sprint Review','atlassian_user_stories#How to write user stories']))
add(86,
 ('The Sprint Retrospective plans ways to improve quality and effectiveness.', 'scrum_guide#Sprint Retrospective'),
 ('Review what went well, what problems occurred, and how they were or were not solved, considering interactions, processes, and tools.', 'scrum_guide#Sprint Retrospective'),
 ('Identify a concrete change that would improve effectiveness and arrange to address the most helpful improvements promptly.', 'scrum_guide#Sprint Retrospective'))
# Tile 10.02.02.
add(87,
 ('Five Whys traces a problem’s cause by repeatedly asking why the previous explanation occurred.',atl('team-playbook/plays/5-whys','Instructions for running this Play')),
 ('Write the problem, ask why it happened, record the answer, and ask why that answer happened to extend the causal chain.',atl('team-playbook/plays/5-whys','Instructions for running this Play')),
 ('Five is a guide rather than a required stopping point; use the chain to reach an underlying cause rather than restating the symptom.',atl('team-playbook/plays/5-whys','Instructions for running this Play')))
add(88,
 ('A fishbone diagram organizes possible causes of a problem to support root cause analysis.',atl('work-management/project-management/root-cause-analysis','Common root cause analysis techniques')),
 ('Group potential causes by categories to explore different contributing factors rather than assuming the visible symptom is the root cause.',atl('work-management/project-management/root-cause-analysis','Common root cause analysis techniques; What is a root cause analysis?')))
add(89,
 ('The Definition of Done describes the state of an increment when it meets the required quality measures.', 'scrum_guide#Commitment: Definition of Done'),
 ('The Scrum Team follows a shared Definition of Done, at least as rigorous as any organizational standard.', 'scrum_guide#Commitment: Definition of Done'),
 ('An item that does not meet the Definition of Done cannot be released or presented at the Sprint Review.', 'scrum_guide#Commitment: Definition of Done'),
 ('Check the completed work against the defined quality criteria and identify any unmet criterion before calling it done.', 'scrum_guide#Commitment: Definition of Done'),
 ('Story acceptance criteria specify completion conditions for that particular story rather than replacing the shared quality standard.', ['atlassian_user_stories#How to write user stories','scrum_guide#Commitment: Definition of Done']))
# Tile 11.01.01.
add(90,
 ('A star schema separates tables describing business entities from tables storing observations or events.',pbi('guidance/star-schema','Understand star schema')),
 ('Dimension tables describe entities and their attributes; their key columns identify rows.',pbi('guidance/star-schema','Understand star schema')),
 ('Fact tables store observations or events with dimension keys and often numeric measures.',pbi('guidance/star-schema','Understand star schema')),
 ('Choose the fact table’s grain so its rows describe a consistent level of detail.',pbi('guidance/star-schema','Understand star schema')),
 ('Connect dimension tables to the central fact table through one-to-many relationships using the dimension’s unique key.',pbi('guidance/star-schema','Star schema relevance to Power BI semantic models')))
add(91,
 ('Model relationships propagate filters between related tables so a visual can use fields from multiple tables.',pbi('transform-model/desktop-create-and-manage-relationships','Understanding relationships')),
 ('Use Modeling > Manage relationships > New and choose the two tables and their matching columns.',pbi('transform-model/desktop-create-and-manage-relationships','Create a relationship manually')),
 ('Set cardinality according to the uniqueness of values on each side and check the active relationship setting.',pbi('transform-model/desktop-create-and-manage-relationships','Configure more options')),
 ('Choose cross-filter direction deliberately: Single propagates filters in one direction and Both allows propagation in both directions.',pbi('transform-model/desktop-create-and-manage-relationships','Cross filter direction')))
# Tile 11.02.01.
add(92,
 ('A Power BI report page contains visuals that communicate information from the model; a service dashboard is a separate collection of tiles.',pbi('create-reports/service-dashboards-design-tips','Dashboard design best practices')),
 ('In report view, choose fields from the Data pane and a visual type from Visualizations to add a visual to the canvas.',pbi('visuals/power-bi-report-add-visualizations','Add visualizations to a Power BI report')),
 ('Arrange important information prominently and keep the page focused on the audience’s question.',pbi('create-reports/service-dashboards-design-tips','Consider your audience; Tell a story on one screen')),
 ('Choose comparisons and trends appropriate to the need, avoid clutter, and keep display choices consistent.',pbi('create-reports/service-dashboards-design-tips','Use the right visualization for the data')))
add(93,
 ('A Tableau dashboard combines views from worksheets in one place.',tab('dashboards_create','Create a dashboard')),
 ('Select New Dashboard and drag sheets from the dashboard pane onto the canvas.',tab('dashboards_create','Create a dashboard')),
 ('Choose a dashboard size suited to how the audience will view it, and arrange the most important view prominently.',tab('dashboards_best_practices','Set an appropriate size; Place the most important view at the top-left')),
 ('Limit the number of views to keep the dashboard focused and readable.',tab('dashboards_best_practices','Limit the number of views')))
# Tile 11.02.02.
add(94,
 ('Use chart types that fit the question: bars support category comparisons and lines support trends over time.',tab('visual_best_practices','Choose the right chart type')),
 ('Place important information where readers are likely to notice it and keep the layout focused.',pbi('create-reports/service-dashboards-design-tips','Tell a story on one screen')),
 ('Use color consistently and avoid unnecessary variety or decoration that distracts from the data.',pbi('create-reports/service-dashboards-design-tips','Use the right visualization for the data')),
 ('Reduce unnecessary views and labels so the intended comparison remains readable.',tab('dashboards_best_practices','Limit the number of views; Make it easy to read')))
add(95,
 ('Publish a Desktop report with Home > Publish and choose a destination workspace in the Power BI service.',pbi('create-reports/desktop-upload-desktop-files','Publish semantic models and reports from Power BI Desktop')),
 ('Select Share for a report or dashboard and specify recipients or an appropriate sharing link.',pbi('collaborate-share/service-share-dashboards','Share a report or dashboard')),
 ('Choose whether recipients can reshare or build on the underlying data and grant only the permissions the audience needs.',pbi('collaborate-share/service-share-dashboards','Manage permissions; Share a report')),
 ('Sharing and access depend on license and capacity; sharing generally requires Pro or PPU, and free recipients require eligible Premium or Fabric capacity.',pbi('collaborate-share/service-share-dashboards','License requirements')))
# Tile 11.03.01.
add(96,
 ('A DAX measure calculates a result that changes with the current report filtering and selection context.',pbi('transform-model/desktop-measures','Understanding measures')),
 ('Use Modeling > New measure and write a named expression such as the source’s Projected Sales = SUM(\'Reseller Sales\'[Last Years Sales])*1.06.',pbi('transform-model/desktop-measures','Sales projection example')),
 ('A calculated column uses a DAX expression to calculate a value for each row rather than the measure’s report-context result.',pbi('transform-model/desktop-calculated-columns','Introduction')),
 ('Use New Column and write column_name = expression; the formula is applied across the table’s rows.',pbi('transform-model/desktop-calculated-columns','Let’s look at an example')),
 ('In standard Import mode, calculated-column values are materialized and refreshed when the underlying data is refreshed.',pbi('transform-model/desktop-calculated-columns','Materialization and performance')))
add(97,
 ('A Tableau calculated field derives new data from existing fields without changing the original source.',tab('calculations_calculatedfields_create','Why use calculated fields')),
 ('Choose Analysis > Create Calculated Field, name the field, enter an expression, and select OK.',tab('calculations_calculatedfields_create','Create a calculated field')),
 ('The source’s IIF([Sales] !=0, [Discount]/[Sales],0) computes a discount ratio when sales are nonzero and returns zero otherwise.',tab('calculations_calculatedfields_create','Create a calculated field')),
 ('A basic calculation may operate at the row level or at the visualization’s aggregate level, depending on its expression.',tab('calculations_calculatedfields_create','Types of calculations')),
 ('Numeric calculated fields can be summed automatically when added to a view; change the aggregation if the intended metric requires a different one.',tab('calculations_calculatedfields_create','Use a calculated field in the view')))
add(98,
 ('A Power BI semantic model represents data prepared for reporting and visualization.',pbi('connect-data/service-datasets-understand','Semantic models')),
 ('Reports can reuse an existing published semantic model rather than each creating separate data and calculation definitions.',pbi('connect-data/service-datasets-understand','Semantic models')),
 ('Define the shared business calculation as a measure in the common model and use that model for reports that need the same calculation.', [pbi('transform-model/desktop-measures','Understanding measures'),pbi('connect-data/service-datasets-understand','Semantic models')]))
# Assembly preserves reused canonical evidence byte-for-byte structurally.
briefs=[]
for c in cs:
 key=(c['concept_id'],c['path_id']);lk=lookup[key];status=lk['canonical_status'];i=c['toc_sequence_position']
 if status=='reuse_registry':
  entry=registry[c['concept_id']]
  evidence=copy.deepcopy(entry.get('evidence',entry))
 elif status=='shared_in_batch':
  evidence=copy.deepcopy(next(x['evidence'] for x in briefs if x['concept_id']==c['concept_id'] and x['path_id']==lk['evidence_built_by_path_id']))
 else:
  evidence={'concept_id':c['concept_id'],'required_facts':D[i],'optional_enrichment':[],'misconceptions':[], 'created_in_batch_id':bid,'used_by_path_ids':[c['path_id']]}
 objective=c['primary_objective'];objective='Learner can '+objective[0].lower()+objective[1:]
 briefs.append({'concept_id':c['concept_id'],'path_id':c['path_id'],'learning_objective':objective,'canonical_status':status,'evidence':evidence})
parents={}
for f in ['extracted_concepts.json','registry_lookup.json','concept_evidence_registry_snapshot.json','source_pack_manifest.json']:
 parents[f]=hashlib.sha256((B/f).read_bytes()).hexdigest()
manifest=json.loads((B/'source_pack_manifest.json').read_text())
for pack in manifest['packs']:parents[pack['file']]=hashlib.sha256(pathlib.Path(pack['file']).read_bytes()).hexdigest()
out={'metadata':{'artifact_type':'coverage_briefs','artifact_version':'1.0.0','schema_version':'1.0.0','batch_id':bid,'run_id':bid,'prompt_version':'03_coverage_brief@v1','model':'none','generated_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_snapshot_id':bid,'parent_artifact_hashes':parents},'batch_id':bid,'briefs':briefs}
(B/'coverage_briefs.part.all.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print('briefs',len(briefs),'required_facts',sum(len(x['evidence']['required_facts']) for x in briefs))
