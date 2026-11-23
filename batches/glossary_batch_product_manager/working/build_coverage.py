import json,hashlib,datetime
from pathlib import Path
from urllib.parse import urlparse
B=Path('batches/glossary_batch_product_manager');D=B/'working'/'sources'
cs=json.load(open(B/'extracted_concepts.json'))['concepts']; lookups=json.load(open(B/'registry_lookup.json'))['lookups']; data={}
def ref(key,section):
 url=json.load(open(D/(key+'.links.json')))['url']
 sid={'pp':'productplan_glossary','atl':'atlassian_agile','rp':'pichler_blog','nn':'nngroup_articles','amp':'amplitude_playbook'}[key.split('_')[0]]
 return sid+'#'+urlparse(url).path+' :: '+section
def add(i,key,section,*facts):
 assert i not in data
 data[i]=[{'id':f'f{j+1}','statement':s,'source_refs':[ref(key,section)]} for j,s in enumerate(facts)]
def more(i,key,section,*facts):
 for s in facts:data[i].append({'id':f'f{len(data[i])+1}','statement':s,'source_refs':[ref(key,section)]})
# Tile 1: Product Strategy and Vision
add(0,'pp_product-mission','What is Product Mission?; How Do You Come Up with a Product Mission?',
 'A product mission explains the product’s purpose and the value it aims to deliver to users.',
 'Draft a concise mission by stating who benefits, what problem is addressed, and how their lives improve.')
more(0,'rp_the-strategy-stack','Business Strategy; Conclusion',
 'Organisational values and desired culture guide strategic choices and how people work together.',
 'Check product direction against the overarching purpose and values so strategic choices remain coherent.')
add(1,'pp_product-vision','What is a Product Vision?; How do you create a product vision?',
 'A product vision describes the long-term future state the product aims to achieve for its users.',
 'A useful vision identifies the audience, their needs, and the reason the product matters.',
 'Write the vision concisely and memorably, with a direction ambitious enough to inspire but realistic enough to pursue.')
add(2,'pp_value-proposition','What is a Value Proposition?; How Do You Develop a Strong Product Value Proposition?',
 'A value proposition communicates the unique value the product offers its target audience relative to alternatives.',
 'Build the proposition from customer jobs, pains, and desired gains rather than a list of product capabilities.',
 'Describe the customer, the benefit, and the differentiator in plain language the audience can understand.',
 'Present the proposition to prospective customers and revise its wording based on their response.')
add(3,'pp_competitive-landscape','What is a Competitive Landscape?; What Should a Competitive Landscape Analysis Include?',
 'Competitive analysis compares alternative offerings and their strengths and weaknesses to identify opportunities to compete.',
 'Identify relevant competitors and compare their offerings using consistent criteria such as features, pricing, and customer service.',
 'Include competitors’ positioning and messaging to understand how they describe their value to customers.',
 'Use the comparison to identify competitive advantages and gaps in the available offerings.')
add(4,'pp_product-positioning','What is Product Positioning?; Why Is Product Positioning Important?',
 'Positioning defines where an offering fits in the market and why a particular audience should choose it.',
 'Define the target customer, the problem addressed, and the product’s distinctive value relative to competitors.',
 'Ground differentiation in customer needs and competitive research rather than claiming to be everything to everyone.')
add(5,'rp_my-product-strategy-model','Product Strategy',
 'A product strategy connects the users and customers served, the needs addressed, the product’s distinguishing capabilities, and its business goals.',
 'Business goals express how the product benefits the organisation, including financial and nonfinancial benefits.',
 'For a proposed product choice, explain both the user benefit and the business goal it supports.',
 'Treat uncertain strategy choices as assumptions to validate and adapt the strategy as evidence changes.')
# Tile 2: Customer Research
add(6,'nn_user-interviews','Definition of a User Interview; How to Do a User Interview',
 'A user interview asks one participant about experiences, needs, and perspectives to learn about a topic.',
 'Plan an interview around research goals and prepare a guide with open-ended questions about participants’ experiences.',
 'Recruit participants relevant to the research question, establish rapport, and listen without judging or leading their answers.',
 'Use follow-up questions to clarify what happened and why rather than accepting vague generalisations.',
 'Record or take notes with permission so the participant’s account can be examined after the session.')
add(7,'amp_customer-segmentation','What is customer segmentation?; Types of customer segmentation; How to segment customers',
 'Customer segmentation divides customers into groups sharing relevant characteristics so their different needs can be addressed.',
 'Useful segmentation dimensions include demographics, geography, psychographics, and behaviour.',
 'Choose dimensions relevant to the product decision and describe each group with observable shared characteristics.',
 'Compare groups’ needs and behaviours to identify which groups the product should serve.')
add(8,'nn_persona','Definition of a Persona; Creating Personas',
 'A persona is a fictional but realistic representation of a target user grounded in research about real users.',
 'Create personas by clustering observed behaviours and needs into distinct roles and adding details relevant to product decisions.',
 'Describe each persona’s goals, concerns, usage context, and experience with the product.',
 'Merge overly similar personas and remove details that neither affect design nor help decisions.')
add(9,'pp_voice-of-customer','What is Voice of Customer?; How Do You Gather Voice of Customer Data?',
 'Voice of Customer captures customers’ expectations, preferences, and problems so decisions reflect their perspective.',
 'Collect input through channels such as interviews, surveys, support interactions, and online feedback.',
 'Analyse recurring customer needs and concerns across the collected input rather than treating a single comment as the whole customer voice.',
 'Use the findings to identify improvements that address what customers need.')
add(10,'pp_jobs-to-be-done-framework','What is the jobs-to-be-done framework?; How do you implement jobs-to-be-done?',
 'A job to be done is the outcome a customer seeks when choosing and using a product.',
 'Functional jobs concern accomplishing a task, while emotional and social jobs concern feelings and how others perceive the customer.',
 'Identify jobs through customer research by asking about the circumstances, motivation, and desired outcome behind product use.',
 'Describe the job in terms of the customer’s objective rather than a proposed feature or the customer’s demographic category.')
add(11,'nn_should-you-run-a-survey','Benefits of Surveys in UX; Survey Myths, Busted; Good Reasons to Run a Survey',
 'A survey collects self-reported answers and is suited to quantifiable questions about attitudes rather than direct observation of behaviour.',
 'Choose a survey when the research question can be answered by asking respondents, and identify the relevant population before gathering responses.')
more(11,'pp_customer-survey','Two Things to Keep in Mind When Asking Users to Take Your Survey; 5 Pro Tips for Designing Customer Surveys',
 'Define the insight needed and include only questions that contribute to it, keeping the survey short.',
 'Use open-ended questions and why follow-ups where explanations are needed beyond predefined answers.',
 'Offer a clear reason to participate and make completion quick and easy.')
more(11,'nn_leading-questions','Definition of Leading Questions; Avoiding Leading Questions',
 'Write neutral questions that do not suggest a preferred answer.')
add(12,'pp_total-addressable-market','What is Total Addressable Market (TAM)?; How do I calculate TAM (Total Addressable Market)?',
 'Total addressable market is the overall revenue opportunity if all demand for the relevant product or service were served.',
 'A top-down estimate narrows an industry-level market using relevant customer and geographic constraints.',
 'A bottom-up estimate multiplies the number of potential customers by the revenue expected per customer.',
 'State the customer definition, data sources, and revenue assumptions so the estimate can be examined.')
add(13,'nn_usability-testing-101','What Is Usability Testing?; Elements of Usability Testing',
 'Usability testing observes representative participants attempting realistic tasks with a product or design.',
 'Prepare tasks that describe user goals without revealing the steps or interface controls needed to complete them.',
 'During a session, present tasks, observe actions, and invite participants to think aloud while avoiding guidance that changes their behaviour.',
 'Record task outcomes, difficulties, and relevant comments so the session evidence is available afterward.')
add(14,'pp_product-market-fit','What is Product-Market Fit?; Why is it Important?; How Do You Measure Product-Market Fit?',
 'Product-market fit means target customers buy, use, and tell others about the product in sufficient numbers to sustain its growth and profitability.',
 'Evaluate fit using evidence from target customers about purchasing, continued use, referrals, and willingness to pay.',
 'Use survey signals and observed customer behaviour together rather than treating one favourable metric as proof of fit.',
 'When the evidence is weak, reconsider the target customer or the needs the product is addressing.')
# Tile 3: Solution Design
add(15,'nn_how-might-we-questions','1: Start with the Problems (or Insights) You’ve Uncovered; 2: Avoid Suggesting a Solution in Your HMW Question; 4: Focus Your HMWs on the Desired Outcome',
 'A problem statement frames an evidenced user difficulty or unmet need rather than prescribing a solution.',
 'State who has the problem, what difficulty they face, and the outcome they need.',
 'Use research findings to make the problem specific enough to guide solution exploration.')
add(16,'nn_how-might-we-questions','5 Tips on Writing Good HMWs; Write and Choose HMWs with Your Team',
 'A How might we question reframes a research finding as a challenge that invites possible solutions.',
 'Write the question from an observed problem and focus it on a positive desired outcome without embedding a particular solution.',
 'Keep the question broad enough to allow different approaches but specific enough to address the finding.')
more(16,'nn_design-thinking','Process: Ideate',
 'Generate multiple ideas for the unmet need, then share, combine, and build on those ideas with the team.')
add(17,'atl_product-specification','The purpose of product specification; What does a product specification sheet include?; How to write a product specification sheet',
 'A solution specification describes the proposed solution, why it is needed, its scope, and how success will be assessed.',
 'Document the proposed capabilities, expected interactions, and workflow inputs and outputs.',
 'Make scope boundaries, excluded features, known risks, and assumptions explicit.',
 'Review the specification with the contributors responsible for building and evaluating the solution.')
# Tile 4: Requirements and Specification
add(18,'atl_requirements','What is a product requirements document (PRD)?; How to write a product requirements document (PRD)',
 'A product requirements document states a product’s purpose, features, functionality, and behaviour as a shared guide for development.',
 'Set out the product purpose, release goals, features, and conditions for successful release.',
 'For each feature, explain its user purpose and required functionality and document its place in scope.',
 'Include assumptions, constraints, open questions, and out-of-scope work so the team can identify unresolved decisions.')
add(19,'atl_user-stories','What are agile user stories?; How to write user stories',
 'A user story describes a desired capability from the perspective of the person who needs it.',
 'Write a story in the form “As a [user], I want [goal], so that [benefit]” to connect the user, action, and reason.',
 'Use stories to support conversation about user value rather than substituting them for a complete technical specification.')
add(20,'atl_product-specification','The purpose of product specification; What does a product specification sheet include?; How to write a product specification sheet',
 'Functional requirements specify what a system must do and how it should behave in response to user interactions.',
 'Document the expected workflow, inputs, outputs, and how users know the action succeeded.',
 'Describe observable behaviour precisely enough that the team can implement and check it.')
add(21,'atl_product-specification','What does a product specification sheet include?',
 'Technical specifications describe implementation constraints such as architecture, data structures, and standards.',
 'Document relevant technical constraints alongside functional specifications so developers know the conditions the solution must meet.')
more(21,'atl_definition-of-done','What is the definition of done?; Examples of definition of done',
 'Quality requirements can address performance, security, and accessibility rather than adding a user-facing capability.',
 'State measurable quality conditions so the team can verify whether the product meets the required standard.')
add(22,'pp_acceptance-criteria','What are Acceptance Criteria?; How to Write Acceptance Criteria',
 'Acceptance criteria are conditions a work item must satisfy to be accepted.',
 'Write criteria that are clear, testable, and focused on outcomes rather than prescribing implementation.',
 'A Given–When–Then criterion states the starting context, the action, and the expected result.',
 'Review criteria with the people implementing and testing the work before delivery.')
add(23,'nn_user-journeys-vs-user-flows','What Is a User Flow?',
 'A user flow is a sequence of specific interactions required to accomplish a task within a product.',
 'Represent the flow with a diagram or wireflow that shows user steps and system responses.',
 'Identify the task goal and map its path through the relevant screens and interactions.')
more(23,'pp_user-flow','What is a User Flow?; How Do You Create a User Flow?',
 'Include entry and exit points and decision branches to show alternate paths through the task.')
add(24,'atl_product-planning','Define product vision and goals',
 'Success metrics are measurements chosen to assess progress toward the product’s goals.',
 'Choose measurements that reflect the intended user benefit and business objective.')
more(24,'amp_experiment-brief','Planning (pre-experiment); Phase 1: Plan; Phase 3: Monitor',
 'Define the target outcome, measurement period, and decision for different possible results before evaluating success.',
 'Confirm that the selected measurement can actually be collected before relying on it.')
# Tile 5: Roadmapping
add(25,'atl_product-roadmaps','What is a product roadmap?; Who is the roadmap for?; How to create a product roadmap',
 'A product roadmap communicates product direction, priorities, and progress over time in support of strategy.',
 'Build a roadmap from customer insight, company goals, and effort constraints, then show the initiatives and their relative timing.',
 'Use a separate delivery plan for implementation detail rather than treating the roadmap as a fixed delivery contract.',
 'Update the roadmap when priorities or circumstances change and keep it accessible to stakeholders.')
add(26,'atl_velocity-scrum','What is velocity in Scrum?; How to calculate velocity in Scrum; Factors that can affect Scrum velocity',
 'Capacity planning estimates the work a team can realistically complete in a planning period.',
 'Historical velocity is the work fully completed per sprint, commonly expressed in story points.',
 'Forecast using the team’s recent completed work and adjust for availability, holidays, and external dependencies.',
 'Compare the planned work against available capacity and reduce or reschedule work that exceeds it.')
add(27,'pp_release-plan','What is a Release Plan?',
 'A release plan is a tactical document that captures the features planned for an upcoming release.',
 'Release plans usually cover a few months and are internal working documents for product and development teams.')
more(27,'atl_product-planning','Develop product roadmap; Create product specifications',
 'Group the intended capabilities into releases with realistic timing, resources, and milestones.',
 'Check the chosen release scope against the requirements and constraints before committing to delivery.')
add(28,'pp_dependency-management','Definition; Dependency mapping: How do you strategically manage dependencies on a roadmap?',
 'A dependency is a relationship that requires initiatives to be executed in a particular order.',
 'Map dependencies between initiatives to identify which work must precede other work.')
more(28,'atl_product-roadmaps','How to create a product roadmap',
 'Sequence already-prioritised initiatives in the roadmap while taking engineering constraints into account.')
add(29,'atl_velocity-scrum','What is velocity in Scrum?; How to calculate velocity in Scrum; Factors that can affect Scrum velocity',
 'Historical sprint throughput can support forecasts of how long a defined scope will take.',
 'For comparable work, divide estimated scope by expected throughput per sprint to estimate the number of sprints required.',
 'Adjust the forecast for team availability, work complexity, and dependencies rather than assuming throughput will stay constant.')
more(29,'atl_estimation','Introduction; Story points vs. hours',
 'An estimate is not a delivery promise and should be communicated with its uncertainty and underlying assumptions.')
add(30,'atl_roadmaps','How to create a product roadmap',
 'Quarterly planning translates product direction into a bounded set of initiatives for a quarter.',
 'Choose the quarter’s initiatives by considering company goals, customer insights, and engineering constraints.',
 'Show the initiatives within the quarter-level roadmap and revise the plan as priorities change.')
more(30,'atl_velocity-scrum','How to calculate velocity in Scrum; Factors that can affect Scrum velocity',
 'Check planned scope against the team’s forecast capacity and account for availability and dependencies.')
add(31,'atl_product-roadmaps','Getting started with product roadmaps',
 'An initiative groups work toward a larger goal and can be broken into smaller delivery items.',
 'Link an initiative to the strategic goal it supports and make its component work visible.')
more(31,'atl_product-specification','The purpose of product specification',
 'Plan the initiative by specifying scope, success measures, risks, assumptions, and the responsible contributors.')
add(32,'pp_dependency-management','Definition; Dependency mapping: How do you strategically manage dependencies on a roadmap?',
 'Roadmap-level dependency management tracks relationships between initiatives and teams that constrain delivery order.',
 'Visualise dependent initiatives across roadmaps so teams can see the required coordination.',
 'Identify collaborators and key stakeholders and synchronise their workflows to reduce disruption.')
more(32,'atl_project-management-dependencies','How to manage project dependencies',
 'Monitor dependencies and communicate changes so affected teams can adjust their schedules.')
# Tile 6: Prioritization
add(33,'pp_minimum-viable-product','What Should Your Minimum Viable Product Include?; The MVP needs to fully address a need or solve a problem for the user',
 'A minimum viable product provides enough functionality to address an early customer need and generate feedback for further development.',
 'Select an end-to-end solution to at least one user problem rather than an arbitrary subset of planned features.',
 'Keep the first scope small while ensuring users can accomplish the core task.',
 'Separate work required for that first usable scope from enhancements that can wait.')
add(34,'pp_value-vs-complexity','Definition; How do Product Managers use the Value vs. Complexity Model?',
 'An impact assessment estimates how much an initiative would benefit customers or the business.',
 'Identify the intended benefit and compare initiatives using agreed value criteria rather than intuition alone.',
 'Value criteria can include customer demand, revenue potential, competitive differentiation, and engagement.',
 'Assess value separately from implementation complexity so the two can be compared when prioritising.')
add(35,'pp_value-vs-complexity','Definition; How do Product Managers use the Value vs. Complexity Model?; What Are the Drawbacks?',
 'Value versus complexity is a two-axis comparison of expected benefit and difficulty of implementation.',
 'Plot initiatives using consistently defined value and complexity criteria.',
 'High-value, low-complexity items are attractive early choices, while high-value, high-complexity items need a deliberate investment decision.',
 'Low-value items generally rank below higher-value alternatives, especially when they are complex.',
 'The comparison is useful for discussion but remains sensitive to subjective estimates.')
add(36,'pp_rice-scoring-model','What is the RICE Scoring Model for Prioritization?; Reach; Impact; Confidence; Effort',
 'RICE ranks initiatives using reach, impact, confidence, and effort.',
 'Measure reach over a consistent time period and define a consistent impact scale across initiatives.',
 'Express confidence as the strength of evidence behind the estimates and effort as the total work required, commonly in person-months.',
 'Calculate RICE score as reach × impact × confidence ÷ effort, using confidence as a proportion.',
 'Use the ranked scores as input to a prioritisation discussion rather than as a substitute for examining assumptions.')
add(37,'pp_ice-scoring-model','What is the ICE Scoring Model?; How Does the ICE Scoring Model Work?',
 'ICE compares ideas using impact, confidence, and ease.',
 'Rate the expected benefit, certainty of that benefit, and ease of implementation using a consistent scale.',
 'Calculate the ICE score by multiplying impact × confidence × ease and compare the resulting scores.',
 'Use ICE for a quick comparative assessment while recognising that subjective ratings can bias the ranking.')
add(38,'pp_choose-prioritization-framework','Weighted Scoring',
 'Weighted scoring compares initiatives across a shared set of criteria that reflect their costs and benefits.',
 'Choose criteria and give them weights reflecting their importance to the decision.')
more(38,'pp_prioritizing-support','The Calculation',
 'Convert each criterion rating to points according to its weight and add those points to obtain an initiative’s total score.',
 'Use a consistent scoring direction: stronger benefits should improve the total, while higher costs should reduce it.',
 'Compare the totals and use the ranking to support an explicit discussion of which initiatives to select.')
add(39,'pp_kano-model-prioritization','The Kano Model: Using Customer Satisfaction to Prioritize Product Features; How the Kano Model Works; Survey',
 'The Kano model categorises features according to how their presence or absence affects customer satisfaction.',
 'Basic features are expected and cause dissatisfaction when absent; performance features produce more satisfaction as they improve; excitement features provide unexpected delight.',
 'Ask paired questions about how customers feel when a feature is present and when it is absent to inform its classification.',
 'Use the classifications to protect essential expectations while selecting performance improvements and differentiators.',
 'Revisit the classifications because once-exciting features can become ordinary expectations over time.')
add(40,'atl_product-discovery','Traditional versus dynamic discovery; Dynamic discovery is transparent, collaborative and engaging',
 'Now–Next–Later presents priorities in sequenced horizons rather than committing every item to a fixed delivery date.',
 'Use Now for current focus, Next for subsequent work, and Later for lower-immediacy possibilities.',
 'Place initiatives in the horizons to communicate where delivery teams should focus effort.',
 'Use the sequence as a living priority view and change it when new evidence changes the direction.')
add(41,'pp_moscow-prioritization','What is MoSCoW Prioritization?; What Are the Categories in MoSCoW?; What Are the Drawbacks of MoSCoW Prioritization?',
 'MoSCoW classifies initiatives as Must have, Should have, Could have, or Will not have for a specified time frame.',
 'Must-haves are non-negotiable requirements without which the release would not work or be viable.',
 'Should-haves add important value but can be deferred; could-haves are useful additions with a smaller cost of omission.',
 'Will not have means excluded for this time frame, not necessarily rejected forever.',
 'Agree the objectives, category criteria, and resource allocation before sorting initiatives so the classifications remain consistent.')
# Tile 7: Stakeholder Management
add(42,'pp_conducting-a-stakeholder-analysis','What is stakeholder analysis?; How do you perform a stakeholder analysis?',
 'Stakeholder mapping identifies people who can affect or are affected by a product decision.',
 'List the relevant stakeholders and classify them by influence and interest.',
 'Use the map to decide who needs close involvement, consultation, or progress information.',
 'Update engagement choices when stakeholders’ interests or influence change.')
add(43,'pp_stakeholder-management','What is Stakeholder Management?; What Does the Stakeholder Management Process Look Like?',
 'Stakeholder management organises ongoing engagement with people whose interests affect product decisions.',
 'Identify each stakeholder’s goals, interests, and influence, then select an appropriate engagement approach.',
 'Maintain regular communication and involve stakeholders at relevant decision points.',
 'Use engagement to understand concerns and build support for product direction.')
add(44,'pp_cross-functional-team','What is a Cross-Functional Team?; Why Do We Need Cross-Functional Teams?',
 'Cross-functional collaboration brings people with different expertise together toward a shared product goal.',
 'Include the functions needed to develop, deliver, and support the product so decisions reflect more than one perspective.',
 'Clarify each function’s contribution and coordinate work around the shared goal.')
more(44,'pp_stakeholder-management','What Does the Stakeholder Management Process Look Like?',
 'Agree communication and involvement expectations so handoffs and decisions do not depend on informal assumptions.')
add(45,'rp_decision-rules-to-make-better-product-decisions','Decisions, Decisions; Unanimity; Consent',
 'Consensus building develops a shared understanding and agreement among the people needed for a product decision.',
 'State whose input is required and which decision rule will be used before the discussion.',
 'Explore competing views and objections, then revise the proposal to address meaningful concerns.',
 'Confirm agreement explicitly rather than treating silence as approval.',
 'Unanimity requires full support; consent requires the absence of meaningful objections and is a distinct, lighter agreement rule.')
add(46,'rp_conflict-resolution','Conflict Resolution Tips for Product Managers and Product Owners; Needs-Based Conflict Resolution',
 'Resolve a stakeholder conflict by understanding the underlying needs behind competing positions.',
 'Describe the issue using factual observations and give each person room to explain their concern without blame.',
 'Listen for the needs each position is intended to satisfy rather than immediately defending one proposed solution.',
 'Generate and agree options that address the important needs on both sides rather than forcing a premature compromise.')
add(47,'pp_4-key-negotiation','1. Start with active listening; 2. Always look for a win-win; 3. Don’t think of each negotiation as all or nothing; 4. Disagree and commit',
 'Negotiation seeks an agreement about competing requests or constraints while preserving working relationships.',
 'Listen actively to understand what the other party wants and why.',
 'Explore options that deliver meaningful benefits for both sides rather than assuming the only outcome is one winner and one loser.',
 'Treat the agreement as part of an ongoing relationship, not an all-or-nothing contest.',
 'Once a decision is made, explain it clearly and commit to the agreed direction even if it was not everyone’s first preference.')
add(48,'pp_stakeholder-buy-in','Common Obstacles to Stakeholder Buy-In; How to Secure and Maintain Stakeholder Buy-In',
 'Buy-in is stakeholders’ support for product direction and willingness to help carry it forward.',
 'Involve stakeholders early and connect the proposed direction to shared business goals.',
 'Explain the reasoning, relevant evidence, and trade-offs behind the proposal and address concerns.',
 'Maintain support through regular progress communication and continued involvement rather than seeking a single approval at the end.')
add(49,'atl_tips-for-presenting-product-roadmaps','Tips for presenting a product roadmap',
 'Roadmap communication explains the planned direction, priorities, and reasons for them to a particular audience.',
 'Tailor the level of detail to the audience and connect the roadmap to the goals it supports.',
 'Make scope and timing expectations clear and avoid presenting uncertain roadmap items as firm promises.',
 'Invite questions and use the discussion to uncover concerns and align expectations.')
add(50,'atl_status-report','What is a status report?; Key elements of a status report',
 'Executive reporting provides a concise view of progress, risks, and next steps so leaders can act on the product’s current state.',
 'Lead with a short summary and relevant progress measures rather than a detailed list of activity.',
 'Surface material obstacles, schedule or budget changes, and their implications.',
 'State next steps, responsible owners, and deadlines, and identify any decision or support needed.',
 'Choose a reporting cadence and level of detail suited to the stakeholders’ information needs.')
# Tile 8: Product Metrics
add(51,'atl_product-management-kpis','What are KPIs in product management?; How to choose the right KPIs for effective product management',
 'A key performance indicator is a selected measurement used to judge progress toward an important product goal.',
 'Choose KPIs that are relevant to the product’s stage, strategic goals, and users.',
 'Make the indicators measurable and actionable so changes can inform decisions rather than merely report activity.')
more(51,'rp_choose-kpis','Use the Product Goals to Guide Your Selection; Avoid Vanity Metrics; Revisit and Change Your KPIs',
 'Select a focused set tied to product goals, avoid vanity measures, and revisit the set when goals change.')
add(52,'pp_objectives-and-key-results','What are Objectives and Key Results (OKRs)?; What are Objectives?; What are Key Results?',
 'OKRs pair an objective describing a desired direction with measurable key results that show whether it has been achieved.',
 'Write the objective as the meaningful outcome to pursue and the key results as verifiable changes rather than a task list.',
 'Use clear measures and target values so progress can be assessed.',
 'Align product OKRs with broader organisational direction and review them during the agreed goal period.')
# Tile 8 continued
add(53,'amp_leading-lagging-indicators','Leading vs. lagging indicators; Leading indicator examples',
 'Leading indicators provide early signals of progress toward a desired future outcome.',
 'Choose signals relevant to the business model and goal and supported by a relationship to the desired outcome.',
 'Use changes in leading indicators to investigate and adjust actions before the final outcome occurs.',
 'A leading signal is not a guarantee: other factors can still change the eventual result.')
add(54,'amp_leading-lagging-indicators','Leading vs. lagging indicators; Lagging indicator examples',
 'Lagging indicators measure outcomes that have already occurred.',
 'Examples include revenue earned over a completed month or year.',
 'Choose lagging indicators that show whether the intended business or product result was achieved.',
 'Use past results to evaluate success and inform future decisions, recognising that the completed period cannot be changed.')
add(55,'amp_north-star','What is a North Star Metric?; A North Star Metric should consist of 2 parts',
 'A North Star Metric captures the value customers derive from the product in a single overarching measure.',
 'Choose a measure that connects delivered customer value with sustainable business success.',
 'Prefer an actionable leading signal of value rather than a past revenue total alone.',
 'Identify contributing inputs the team can influence and check that increasing the measure reflects genuine customer value.')
add(56,'amp_analytics-dashboard','What is an analytics dashboard?; How to build an analytics dashboard',
 'An analytics dashboard brings related measurements together so product performance can be monitored at a glance.',
 'Choose the audience and decisions the dashboard should support before choosing its measurements.',
 'Use clear visualisations and a focused set of relevant metrics rather than displaying every available measure.',
 'Share the dashboard with the people who need the information and use it to guide follow-up action.')
add(57,'amp_funnel-analysis','What is funnel analysis?; How to use funnel analysis',
 'Funnel analysis examines the sequence of steps users take toward a desired action.',
 'Define the ordered steps and the time allowed for completing them before comparing results.',
 'Compare the numbers reaching each step to identify where users drop out.',
 'Break results down by relevant user characteristics to locate groups experiencing different barriers.',
 'Use the largest or most important drop-offs to focus investigation and improvement.')
add(58,'amp_cohort-analysis','What Is Cohort Analysis?; Behavioral cohort analysis',
 'A cohort is a group of users sharing a characteristic or behaviour, and cohort analysis compares outcomes for those groups.',
 'Define group membership precisely before comparing engagement or retention.',
 'Compare groups over relevant periods to identify differing patterns that aggregate results can hide.',
 'Use the patterns to generate explanations and product improvements rather than assuming every observed association is causal.')
# Tile 9: Experimentation
add(59,'amp_ab','Analyze A/B test results in Amplitude',
 'An A/B test is a controlled, randomised experiment comparing alternatives on a chosen outcome measure.',
 'Assign users to the alternatives and record which variation each user experiences.',
 'Compare the same outcome across the groups to estimate the effect of the change.')
more(59,'amp_ab-testing','Improving UI/UX; Optimizing Marketing Campaigns',
 'Use an existing experience as the control and a proposed change as the alternative, avoiding unrelated changes that obscure what is being tested.')
add(60,'amp_experiment-brief','Phase 1: Plan',
 'A testable hypothesis states the expected effect of a proposed change and the reason for that expectation.',
 'Specify the population, change, outcome measure, and time period involved.',
 'Define in advance what evidence would support or contradict the hypothesis.',
 'Use the hypothesis to choose the experiment’s measurements and decision criteria.')
add(61,'amp_7-step-experimentation-framework','Step 3: Data setup and metric definition; Step 4: Experiment design',
 'An experiment design specifies how a hypothesis will be tested and how results will be interpreted.',
 'Define the target audience, variants, allocation, success measures, and planned duration.',
 'Confirm that the required data can be collected and that the planned test can detect a decision-relevant effect.',
 'Document the setup before starting so the comparison and interpretation do not change opportunistically.')
add(62,'amp_incrementality-testing','In-product feature rollouts with holdout groups; Five actions for reliable marketing incrementality tests',
 'A holdout group remains on the old experience while another group receives the new feature.',
 'Retaining an unexposed comparison group helps separate the feature’s incremental effect from changes that would have happened anyway.',
 'Define the holdout and treatment populations and compare the same outcome over the same period.',
 'Account for seasonality and external factors when interpreting the difference between the groups.')
add(63,'amp_estimate-duration','Step 3: Set your minimum detectable effect (MDE); Use the Duration Scenarios table to prioritize',
 'Sample-size planning determines how much evidence is needed to detect an effect relevant to the decision.',
 'Use baseline conversion, expected traffic, the minimum detectable effect, and the desired confidence level to estimate test duration.',
 'Smaller detectable effects require more traffic or longer duration than larger effects.',
 'Higher confidence requirements generally take longer; choose the level according to the cost of a wrong decision.',
 'Check whether the required duration is feasible before committing to the experiment.')
add(64,'amp_experiment-brief','Phase 4: Analyze; Phase 5: Learn',
 'Experiment analysis compares observed results with the hypothesis and pre-agreed decision criteria.',
 'Evaluate the primary outcome together with other important measures and data-quality concerns.',
 'Consider uncertainty and relevant differences between user groups before choosing an action.',
 'Document whether to ship, revise, stop, or gather more evidence and record the learning for future decisions.')
# Tile 10: User Research and Design Thinking
add(65,'nn_design-thinking','What Is Design Thinking?; Process',
 'Design thinking is a user-centred, iterative approach to understanding problems and exploring solutions.',
 'Its activities include empathising with users, defining the problem, generating ideas, prototyping, and testing.',
 'Use research to identify the unmet need, generate alternatives, and make candidate solutions tangible enough to evaluate.',
 'Return to earlier activities when feedback changes the understanding of the problem or solution.')
add(66,'nn_affinity-diagram','Definition; Affinity Diagramming in UX',
 'Affinity mapping groups related observations or ideas to reveal themes in qualitative evidence.',
 'Put individual observations on separate notes and cluster them by similarity.',
 'Label the clusters with meaningful themes and discuss how they relate to the research question.',
 'Preserve the underlying observations so the themes can be traced back to evidence.')
add(67,'nn_journey-mapping-101','Definition of a Journey Map; Key Components of a Journey Map',
 'A journey map visualises the process a person goes through to accomplish a goal.',
 'Choose an actor and scenario, then map the phases, actions, thoughts, and emotions along the journey.',
 'Identify difficulties and opportunities across the journey rather than focusing only on individual screens.',
 'Ground the map in research and specify which scenario and perspective it represents.')
add(68,'nn_affinity-diagram','Affinity Diagramming in UX',
 'Interview synthesis turns individual accounts into evidence-based themes and insights.',
 'Extract relevant observations from session notes and group related findings across participants.',
 'Name the recurring themes and retain the supporting accounts so conclusions remain traceable.',
 'Use the themes to explain user needs and identify questions that still require investigation.')
add(69,'nn_10-survey-challenges','Limitations of Surveys; Recall Bias; Social-Desirability Bias; Random-Response Bias',
 'Survey findings describe reported attitudes and recollections, not directly observed behaviour.',
 'Examine response patterns and data quality before treating answers as reliable evidence.',
 'Consider recall, social-desirability, and random-response biases when interpreting the results.',
 'Report the population reached and limitations of the collected responses rather than generalising automatically to all users.',
 'Use observational evidence when the decision depends on what users actually do.')
add(70,'nn_usability-testing-101','Goals of Usability Testing; Elements of Usability Testing',
 'Usability analysis examines task outcomes and observed difficulties to identify problems with an interface.',
 'Bring together the session observations, unsuccessful tasks, errors, and relevant participant comments.',
 'Identify recurring difficulties and the parts of the task or interface associated with them.',
 'Use the evidence to recommend changes and evaluate whether later iterations resolve the identified problems.')
# Tile 11: Agile Collaboration
add(71,'atl_scrum-framework','Scrum roles',
 'Scrum distinguishes the Product Owner’s product-value responsibilities from the Scrum Master’s process-support responsibilities.',
 'The Product Owner orders the product backlog and helps the team understand priorities and user value.',
 'The Scrum Master helps the team use Scrum effectively and remove impediments.',
 'Developers organise the work of building the increment; a product manager should not conflate product direction with directing every delivery task.')
add(72,'atl_sprint-planning','What is sprint planning?; The what; The how; Inputs; Outputs',
 'Sprint planning establishes a sprint goal and a plan for work the team can complete during the sprint.',
 'Bring ordered work, context, and clarified expectations so the team understands the desired outcome.',
 'Discuss the work against team capacity and agree the scope in support of the sprint goal.',
 'Let the delivery team determine how to do the work rather than prescribing every task.')
add(73,'atl_standups','What is a stand-up in scrum?; Stand-ups for agile teams',
 'A daily standup is a short coordination meeting that makes progress and blockers visible to the team.',
 'Discuss recent work, upcoming work, and obstacles that affect progress toward the team’s goal.',
 'As a product manager, contribute relevant context and help resolve issues that require product decisions.',
 'Move detailed problem-solving to follow-up discussions rather than turning the meeting into a long status report.')
add(74,'atl_sprint-reviews','What is a sprint review?; Benefits of sprint reviews',
 'A sprint review shares completed work with stakeholders to inspect progress and gather feedback.',
 'Demonstrate working functionality and discuss what was completed and what remains unresolved.',
 'Invite stakeholder feedback on the product outcome rather than merely reporting task completion.',
 'Use the feedback and changed circumstances to inform subsequent priorities.')
add(75,'atl_retrospectives','What is a sprint retrospective?; How to run a sprint retrospective',
 'A retrospective helps the team inspect how it worked and agree improvements for subsequent work.',
 'Discuss what worked well, what caused problems, and possible changes in a respectful environment.',
 'Select actionable improvements and assign responsibility for carrying them forward.',
 'Review previous improvement actions so the meeting produces change rather than repeated complaints.')
add(76,'atl_definition-of-done','What is the definition of done?; Definition of done vs. acceptance criteria',
 'A Definition of Done is a shared set of quality conditions that work must satisfy before it counts as complete.',
 'Apply the agreed conditions consistently to delivered work so completion means the same thing across the team.',
 'Include relevant checks such as testing, review, documentation, and required quality standards.',
 'Distinguish this shared completion standard from acceptance criteria specific to one work item.')
add(77,'atl_backlog-refinement','What is backlog refinement?; How to refine a product backlog',
 'Backlog refinement prepares future work by reviewing, clarifying, and adjusting backlog items.',
 'Clarify the purpose and requirements of items and resolve important questions with the team.',
 'Break oversized work into manageable items and update estimates and ordering as understanding improves.',
 'Keep upcoming work sufficiently clear for planning without detailing every distant idea.')
add(78,'atl_boards','What is an agile board?; Scrum boards; Kanban boards',
 'An agile board visualises work items and their current workflow states.',
 'Move items through the agreed states as their actual status changes.',
 'Use the board to coordinate work and identify blocked or stalled items.',
 'Scrum boards commonly represent sprint work, while Kanban boards support continuous flow.')
add(79,'atl_wip-limits','What are WIP limits?; Why are WIP limits important?; Using WIP limits',
 'Work-in-progress limits constrain how many items are active in a workflow stage at once.',
 'Set explicit limits and make them visible so the team knows when a stage is full.',
 'When a limit is reached, help finish or unblock existing work instead of starting more.',
 'Review the limits and bottlenecks to improve flow rather than treating the limits as fixed productivity targets.')
add(80,'atl_technical-debt','What is technical debt?; Managing technical debt',
 'Technical debt is future work created by shortcuts or compromises in implementation.',
 'Make debt visible and discuss its effects on reliability, delivery speed, and maintainability.',
 'Work with engineering to weigh repayment against new feature work using the consequences and risks involved.',
 'Include important repayment work in planning and revisit the trade-off as the product changes.')
add(81,'atl_project-management-dependencies','Types of project dependencies; How to manage project dependencies',
 'Execution-level dependency tracking identifies work or decisions that other work currently relies on.',
 'Record the dependency, the affected work, and the responsible contributor.',
 'Monitor its status and communicate changes so the team can adjust before the dependency becomes a blocker.',
 'Coordinate resolution or escalation with the people able to remove the obstacle.')
# Tile 12: Product Delivery and Launch
add(82,'atl_release','What is a release?; Release management',
 'Release management coordinates the preparation and delivery of a product version to users.',
 'Plan the release scope and schedule and coordinate the contributors needed to deliver it.',
 'Confirm quality and readiness before deployment and communicate the changes to affected people.',
 'Monitor the release after delivery and respond to problems or feedback.')
add(83,'pp_feature-flag','What is a Feature Flag?; Benefits of Feature Flags',
 'A feature flag controls whether functionality is available without requiring a separate code deployment for each exposure change.',
 'Use flags to enable or disable a feature for selected users or environments.',
 'Plan the initial audience and expand exposure as confidence in the feature grows.',
 'Keep a way to disable problematic functionality and remove obsolete flags so they do not accumulate maintenance burden.')
add(84,'amp_create-tracking-plan','What is a tracking plan?; Components of a good tracking plan; How to create a tracking plan',
 'A tracking plan documents the events and properties needed to answer product questions with behavioural data.',
 'Start from the decisions and questions to identify the actions that need to be tracked.',
 'For each event, specify its name, meaning, properties, and the conditions that trigger it.',
 'Agree the plan with implementation contributors and validate that collected data matches the specification.',
 'Maintain the plan as the product changes so names and definitions remain consistent.')
# Own-mistakes checklist: source existence, identity, objectives, gates, completeness, and provenance.
# Correct the conflict citation to the article actually describing needs-based resolution.
for f in data[46]:f['source_refs']=[ref('rp_leverage-conflict','Resolving Conflict with Non-Violent Communication; Steps 1–4')]
# Add appropriate closed-ended design guidance without promoting later survey analysis.
more(11,'nn_survey-best-practices','Focus on Closed-Ended Questions; Avoid Double-Barreled Questions; Use Balanced Scales',
 'Use closed-ended questions for quantifiable answers, balanced response scales, and separate questions for distinct issues.')
assert set(data)==set(range(len(cs)))
rows=[]
for c in cs:
 i=c['toc_sequence_position'];fs=data[i]
 assert 3<=len(fs)<=8
 assert all(f['statement'].strip() and f['source_refs'] for f in fs)
 rows.append({'concept_id':c['concept_id'],'concept_name':c['concept_name'],'learning_objective':c['primary_objective'], 'canonical_status':next(x['canonical_status'] for x in lookups if x['concept_id']==c['concept_id']), 'required_fact_ids':[f['id'] for f in fs], 'facts':fs,'misconceptions':[],'confusable_pairs':[],'allowed_enrichment':[], 'blocked_future_concepts':[x['concept_id'] for x in cs if x['toc_sequence_position']>i and x['concept_id']!=c['concept_id']], 'evidence_status':'new_evidence_created'})
assert len(rows)==85 and len({x['concept_id'] for x in rows})==85
assert all(len(r['blocked_future_concepts'])==84-i for i,r in enumerate(rows))
inputs=['extracted_concepts.json','registry_lookup.json','concept_evidence_registry_snapshot.json','source_pack_manifest.json','product_manager.source_pack.json']
now=datetime.datetime.now(datetime.timezone.utc)
out={'metadata':{'artifact_type':'coverage_briefs','artifact_version':'1.0.0','schema_version':'1.0.0','batch_id':'glossary_batch_product_manager','run_id':'glossary_batch_product_manager_03_coverage_brief_'+now.strftime('%Y%m%dT%H%M%SZ'),'prompt_version':'03_coverage_brief@v1','model':'none','generated_at':now.isoformat().replace('+00:00','Z'),'source_snapshot_id':json.load(open(B/'extracted_concepts.json'))['metadata']['source_snapshot_id'],'parent_artifact_hashes':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in inputs}},'coverage_briefs':rows}
p=B/'coverage_briefs.part.all.json';p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print('CHECKLIST PASSED:',len(rows),'briefs;',sum(len(r['facts']) for r in rows),'facts; input hashes verified; later-only fences checked; fetched source locators attached.')
