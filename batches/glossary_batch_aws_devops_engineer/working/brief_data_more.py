from brief_data import put
put(44,'aws_cloudformation_user_guide#using-cfn-stack-drift.html',
 'CloudFormation drift detection compares supported explicitly declared resource properties with their current values.',
 'Run drift detection on the provisioned stack after the supplied out-of-band change, wait for completion and inspect the bucket’s expected and actual property values.',
 'Drift detection reports differences without repairing them; unsupported or undeclared properties may not be checked.')
put(45,'aws_cloudformation_user_guide#using-cfn-updating-stacks-monitor-stack.html',
 'CloudFormation stack events record resource operation status and failure reasons during an update.',
 'After the supplied controlled update failure, inspect the first failing resource event and subsequent rollback events.',
 ('UPDATE_ROLLBACK_COMPLETE indicates rollback to the previous working stack state; UPDATE_ROLLBACK_FAILED requires resolving the rollback failure before continuing.','aws_cloudformation_user_guide#using-cfn-updating-stacks-continueupdaterollback.html'))
put(46,'aws_iam_user_guide#id_roles_use_switch-role-ec2_instance-profiles.html',
 'An instance profile contains one IAM role and provides a way to pass that role to EC2.',
 ('Attach or replace the approved instance profile on the EC2 instance using the instance’s IAM-role setting or associate-iam-instance-profile.','aws_ec2_user_guide#attach-iam-role.html'),
 ('Use the instance’s role credential provider rather than embedded keys, inspect the caller identity and test one allowed and one denied operation under the assigned role’s permissions.','aws_ec2_user_guide#iam-roles-for-amazon-ec2.html'))
put(47,'aws_eks_user_guide#pod-identities.html',
 'EKS Pod Identity associates a Kubernetes service account in a namespace and cluster with an IAM role for application AWS access.',
 ('Create an association for the supplied cluster, namespace, service account and approved role; run the workload with that serviceAccountName.','aws_eks_user_guide#pod-id-association.html'),
 'The Pod Identity agent and supported SDK credential chain supply temporary role credentials to associated Pods; verify allowed access from the intended workload and rejection from an unassociated workload.')
put(48,'github_actions_docs#how-tos/secure-your-work/security-harden-deployments/oidc-in-aws',
 'GitHub Actions OIDC enables a workflow to obtain temporary AWS role credentials without storing AWS access keys.',
 'Configure the GitHub token issuer as an IAM OIDC provider and constrain the role trust policy’s aud and sub claims to the approved audience and repository/branch or environment.',
 'Give the workflow id-token: write permission and configure the AWS credential action to assume the approved role; test that an unapproved repository or branch cannot assume it.')
put(49,'aws_iam_user_guide#id_credentials_temp_use-resources.html',
 'Temporary AWS credentials consist of an access key ID, secret access key and session token and expire after their issued lifetime.',
 ('Call aws sts assume-role with --role-arn, --role-session-name and the approved --duration-seconds, then use all three returned credential fields and inspect Expiration.','aws_iam_user_guide#id_credentials_temp_request.html'),
 ('A role session’s effective permissions are bounded by the role permissions and any session policies, which cannot grant more than the role allows.','aws_iam_user_guide#access_policies.html#policies_session'))
put(50,'aws_eventbridge_user_guide#eb-events-iam-roles.html',
 'EventBridge target execution authority is separate from the event pattern that selects events.',
 'For targets requiring an execution role, grant events.amazonaws.com permission to assume the role and attach permissions scoped to the approved target operation and resource.',
 ('Targets such as SNS and Lambda use resource-based permissions for invocation; use the target’s required authorization model rather than assuming every target uses a role.','aws_eventbridge_user_guide#eb-use-resource-based.html'))
put(51,'aws_config_developer_guide#evaluate-config_use-managed-rules.html',
 'A Config managed rule evaluates supported resource configuration against the rule’s criteria and configured parameters.',
 'Choose the supplied rule, resource scope and parameters, run or inspect its evaluation, and compare compliant and noncompliant sample resources.',
 ('Read each evaluation’s resource ID and compliance result rather than treating the presence of the rule as proof that all resources passed.','aws_config_developer_guide#evaluate-config_view-compliance.html'))
put(52,'aws_cost_management_user_guide#budgets-create.html',
 'An AWS budget compares cost or usage with a configured budget amount over a selected period.',
 ('Create a cost budget with the approved scope, amount and period, then configure an actual or forecast threshold and approved notification recipient.','aws_cost_management_user_guide#budgets-create-notifications.html'),
 'A notification alerts its recipients; stopping resources requires separately configured actions rather than the notification itself.')
put(53,'aws_codebuild_user_guide#build-spec-ref.html',
 'A buildspec is a YAML document describing build commands and artifacts; version: 0.2 supports commands in the same shell environment.',
 'Place supplied commands under phases such as install, pre_build, build and post_build, using commands lists in the needed phases.',
 'Set artifacts.files and, if needed, base-directory to match the generated output, then inspect the build’s phase logs and exported artifact.')
put(54,'aws_codedeploy_user_guide#reference-appspec-file.html',
 'For EC2 deployments, appspec.yml maps revision files to destinations and lists scripts for deployment lifecycle hooks.',
 ('Configure the supplied application and deployment group to identify the intended EC2 targets and revision, with the approved service role and installed agent.','aws_codedeploy_user_guide#deployment-groups.html'),
 'Inspect the AppSpec files mapping and hooks, execute the supplied deployment action and verify hook results and application files on the target.')
put(55,'aws_ec2_autoscaling_user_guide#as-scaling-target-tracking.html',
 'Target tracking adjusts Auto Scaling capacity to keep a chosen metric near its target value.',
 'Select the approved metric and target value and configure instance warmup along with the group’s minimum, desired and maximum capacities.',
 'Run the bounded load test and compare metric values and scaling activities with resulting capacity; capacity cannot exceed the group’s configured maximum.')
put(56,'aws_ecr_user_guide#repository-policy-examples.html',
 'An ECR repository policy grants specified principals repository operations such as pulling images or uploading image layers.',
 'Scope the supplied policy’s principals and actions to approved publishers and consumers, then test push and pull and an unapproved principal.',
 'ECR authentication also requires ecr:GetAuthorizationToken through an identity policy; repository permissions alone do not grant that action.')
put(57,'aws_ecr_user_guide#LifecyclePolicies.html',
 'ECR lifecycle policies select images using criteria such as tag status and count or age and expire matching images.',
 'Use rulePriority, selection and action fields to express the supplied retention policy and run a lifecycle preview before applying it.',
 'Check previewed digests against deployed versions; exclude still-needed versions from eligible expiry rather than assuming deployment makes an image immune to lifecycle rules.')
put(58,'aws_elb_user_guide#../application/load-balancer-target-groups.html',
 'An Application Load Balancer listener evaluates routing rules and forwards matching requests to a target group.',
 'Configure the supplied listener protocol and port, forwarding rule and registered target protocol/port, then test the endpoint.',
 ('Configure the health-check path, port and success codes to match the backend and inspect target health reasons when a request path fails.','aws_elb_user_guide#../application/target-group-health-checks.html'),
 ('An ALB normally routes to healthy registered targets, but when every registered target in a target group is unhealthy it fails open and routes to those unhealthy targets.','aws_elb_user_guide#../application/target-group-health-checks.html'))
put(59,'aws_cloudwatch_user_guide#../logs/Working-with-log-groups-and-streams.html',
 'CloudWatch log-group retention controls how long events remain; by default logs are retained indefinitely.',
 'Set the supplied retention interval with put-retention-policy and inspect the log group’s retentionInDays.',
 'Expired events are marked for deletion; physical deletion typically takes up to 72 hours, so expiry is not necessarily immediate disappearance.')
put(60,'aws_rds_user_guide#USER_CreateSnapshot.html',
 'An RDS DB snapshot captures the database instance for later restoration.',
 'Create a manual snapshot for the intended DB instance and wait until its snapshot status is available.',
 ('Restore the snapshot to a new DB instance identifier using the supplied network settings; restoration creates a separate instance rather than overwriting the source.','aws_rds_user_guide#USER_RestoreFromSnapshot.html'),
 ('Wait for the restored instance to become available, connect to its endpoint and run the supplied query to verify the recovery marker.','aws_rds_user_guide#CHAP_CommonTasks.Connect.html'))
put(61,'aws_cloudwatch_user_guide#../logs/iam-access-control-overview-cwl.html',
 'CloudWatch Logs uses IAM policies to authorize log-group and log-stream operations.',
 ('Grant the approved reader the required read actions on the intended log-group resources and remove unnecessary broader grants; some operations require resource scope *.','aws_cloudwatch_user_guide#../logs/iam-identity-based-access-control-cwl.html'),
 'Test the approved and unapproved principals against the intended read operations because collecting logs does not itself grant reader access.')
put(62,'aws_ecs_developer_guide#task_definitions.html',
 'An ECS task definition specifies the image and container runtime settings for tasks.',
 ('Set containerDefinitions entries with name, image, portMappings, cpu and memory settings appropriate to the supplied launch type, and register the task definition.','aws_ecs_developer_guide#task_definition_parameters.html'),
 ('Run the registered task definition with the supplied cluster and network configuration, then inspect task status and container details to verify the image and runtime settings.','aws_ecs_developer_guide#ecs_run_task.html'))
put(63,'aws_iam_user_guide#troubleshoot_access-denied.html',
 'An access-denied diagnosis is specific to the requesting principal, operation, resource and request context.',
 'Inspect the request and applicable policies for an explicit deny, missing allow or unsatisfied condition and use available denial context to localize the cause.',
 ('Resource policies, session policies, permissions boundaries and organization policies can constrain access beyond one identity policy; explicit deny takes precedence.','aws_iam_user_guide#reference_policies_evaluation-logic.html'),
 'Make the smallest approved policy or request correction supported by the evidence and retest the denied operation.')
put(64,'terraform_language#../cli/commands/apply',
 'terraform apply PLAN_FILE executes the changes recorded in a saved plan without generating a new plan or prompting for approval.',
 'Use the supplied approved saved plan file rather than an unplanned apply, and retain the apply outcome as execution evidence.',
 ('Inspect terraform show PLAN_FILE and the resulting resource or outputs to check that the created EC2 instance matches the approved plan.','terraform_language#../cli/commands/show'))
put(65,'aws_systems_manager_user_guide#run-command.html',
 'Run Command executes Systems Manager documents on managed nodes under authorized access.',
 ('Use send-command with the supplied document and explicit approved --instance-ids or tag-based --targets and document parameters.','aws_systems_manager_user_guide#run-command-tutorial.html'),
 ('Record the command ID and inspect each invocation’s status and output; the parent command status does not replace per-node result checks.','aws_systems_manager_user_guide#monitor-commands.html'))
put(66,'terraform_language#../cli/commands/validate',
 'terraform validate checks configuration syntax and internal consistency without checking remote service state or provider API success.',
 'Initialize needed providers and modules with terraform init -backend=false before static validation where backend access is not needed.',
 'Run terraform validate as a blocking workflow step; stop on its nonzero exit result, correct the invalid declaration and rerun before the supplied approved apply step.',
 ('terraform fmt -check checks canonical formatting and can be used as an additional blocking configuration check.','terraform_language#../cli/commands/fmt'))
put(67,'boto3_guide#retries.html',
 'AWS SDK retries cover selected transient or throttling errors rather than making every failed request safe to repeat.',
 'Configure a finite retry limit and backoff for the supplied operation, and stop instead of retrying errors classified as terminal.',
 ('In Python, catch the supplied call’s expected exception around a try block, preserve error code, message and request ID when available, and report failure after the retry budget is exhausted.','boto3_guide#error-handling.html'),
 'When configuring Boto3, total_max_attempts includes the initial request, whereas max_attempts in a Config object counts retries after the initial request.')
put(68,'aws_cost_management_user_guide#ce-what-is.html',
 'Cost Explorer analyzes billed cost and usage for selected time intervals and grouping dimensions.',
 ('Filter the supplied period and account, group by service or usage type, and inspect the cost and usage values to identify the supported cost driver.','aws_cost_management_user_guide#ce-filtering.html'),
 'Use the billed usage evidence to justify the avoidable charge rather than equating the existence of a resource with a specific charge.')
put(69,'kubernetes_overview#../workloads/controllers/deployment/',
 'A Deployment manages ReplicaSets to reconcile the requested Pod replicas and Pod template.',
 'Apply the supplied Deployment with kubectl apply -f FILE and inspect kubectl get deployment NAME and the associated Pods.',
 'Delete one controlled test Pod and verify the controller creates a replacement and restores the requested replica count.')
put(70,'aws_well_architected_framework#rel_planning_for_recovery.html',
 'A workload recovery plan must account for dependencies and the recovery capabilities needed to satisfy its objectives.',
 'List the supplied infrastructure, data and service dependencies and place each prerequisite restoration before the steps that depend on it.',
 'Include verification points before dependent services resume so incomplete restoration is not mistaken for usable recovery.')
put(71,'aws_cloudwatch_user_guide#../logs/CWL_QuerySyntax.html',
 'Logs Insights queries select and transform log events using commands connected with pipe characters.',
 ('Select the log group and time window, then use fields @timestamp, @message, REQUEST_FIELD | filter REQUEST_FIELD = "ID" | sort @timestamp asc with the actual supplied request field and identity.','aws_cloudwatch_user_guide#../logs/CWL_QuerySyntax-Filter.html'),
 ('Use shared request identity and event timestamps to reconstruct the supplied symptom’s sequence, retaining the relevant events as evidence.','aws_cloudwatch_user_guide#../logs/CWL_QuerySyntax-Sort.html'))
put(72,'aws_cloudwatch_user_guide#Notify_Users_Alarm_Changes.html',
 'An alarm action can publish state-change notifications to an SNS topic without changing the alarm’s metric evaluation.',
 'Configure the approved topic as the alarm’s notification action and create the approved recipient subscription, confirming it when required.',
 'Verify the recipient receives a test alarm notification containing alarm and workload context; a configured but unconfirmed subscription may not deliver notifications.')
put(73,'aws_lambda_developer_guide#lambda-intro-execution-role.html',
 'A Lambda execution role grants the function permission to access AWS resources during invocation.',
 'Assign the approved execution role whose actions and resources are limited to the supplied operational task.',
 ('Invoke the function with the supplied payload and inspect its returned result and execution logs, distinguishing successful invocation from a successful operational result.','aws_lambda_developer_guide#invocation-sync.html'))
put(74,'aws_guardduty_user_guide#guardduty_findings-summary.html',
 'A GuardDuty finding contains a finding type, severity, affected resource and details of suspicious activity.',
 'Inspect resource identity, activity timestamps and finding details, and preserve the evidence supporting investigation.',
 ('Follow the established investigation and escalation procedure for the finding type rather than taking destructive action from severity alone.','aws_guardduty_user_guide#guardduty_remediate.html'))
put(75,'aws_s3_user_guide#example-bucket-policies.html',
 'S3 bucket policies can grant or deny object operations to specified principals and resource paths.',
 'Give approved audit writers and readers only their required actions on the intended bucket or object ARNs; inspect other applicable grants and denies.',
 'Test a write and read with approved identities and a read with the unapproved identity; encryption or retention settings do not replace authorization checks.')
put(76,'aws_s3_user_guide#UsingKMSEncryption.html',
 'SSE-KMS encrypts S3 objects with an AWS KMS key, while SSE-S3 uses S3-managed keys.',
 'Reading an SSE-KMS object requires both s3:GetObject permission and kms:Decrypt authority for its key; SSE-S3 does not require KMS key-use permission.',
 'Configure the supplied KMS key as bucket default encryption and test reads with approved object/key authority and with KMS use denied; inspect the object’s encryption metadata.')
put(77,'terraform_language#../cli/commands/plan',
 'A Terraform plan describes proposed additions, updates, deletions and replacements based on configuration, state and observed infrastructure.',
 'Create a saved plan with terraform plan -out=PLAN_FILE and inspect it with terraform show PLAN_FILE; replacement includes destruction and creation, not merely an in-place update.',
 'Compare affected resource identities and every proposed action, including the mandatory deletion case, with the supplied scope and impact criteria and record accept or block with plan evidence; review does not require destructive execution.')
put(78,'aws_systems_manager_user_guide#automation-working-executing.html',
 'An execution preview exposes the targets and anticipated impact of an Automation runbook without running the automation.',
 'Use the supplied preview or dry-run mode and compare listed targets and proposed actions with approved scope before enabling execution.',
 'A successful preview is evidence about proposed execution, not proof that a subsequent execution will succeed.')
put(79,'aws_systems_manager_user_guide#monitor-commands.html',
 'A fleet command has separate invocation results for individual targets, which may differ within one command.',
 'Inspect invocation statuses and outputs and record successful, failed and unresolved targets separately.',
 'Use target-specific results to choose the scoped follow-up rather than blindly repeating the entire operation on already successful targets.')
put(80,'aws_iam_user_guide#id_credentials_temp_use-resources.html',
 'Temporary credentials stop being usable after expiration and must be replaced with a newly authorized session.',
 'On an expired-session error, renew the approved session through its credential provider and use the new access key, secret key and token together.',
 ('Before retrying a resource-changing operation, inspect its known outcome or use the operation’s supported idempotency mechanism so credential renewal does not cause duplicate effects.','aws_ec2_user_guide#ec2-api-idempotency.html'))
put(81,'aws_ecs_developer_guide#task-iam-roles.html',
 'The ECS task role supplies credentials for AWS calls made by the application containers.',
 ('The task execution role authorizes ECS startup work such as pulling an image and publishing logs; it is distinct from application AWS permissions.','aws_ecs_developer_guide#task_execution_IAM_role.html'),
 'Set taskRoleArn to the approved least-privilege application role in the task definition and test allowed and denied application operations from the task.')
put(82,'aws_control_tower_user_guide#how-controls-work.html',
 'A governed account baseline applies standardized organizational controls and configuration to accounts.',
 'Apply the supplied approved control configuration to the sandbox account and inspect each stated control’s deployment or evaluation result.',
 'Distinguish preventive controls that restrict actions from detective controls that report noncompliance when interpreting the baseline checks.')
put(83,'kubernetes_overview#../../tasks/configure-pod-container/configure-pod-configmap/',
 'A ConfigMap supplies nonconfidential configuration separately from the container image.',
 'Reference a ConfigMap with envFrom.configMapRef or env.valueFrom.configMapKeyRef in the supplied Pod template.',
 ('Reference a Secret with env.valueFrom.secretKeyRef or a secret-backed volume and test the consuming workload without printing the secret values.','kubernetes_overview#../configuration/secret/'),
 ('Secrets require access control and appropriate storage protection; base64 encoding is not encryption.','kubernetes_overview#../configuration/secret/'))
put(84,'aws_codepipeline_user_guide#concepts-how-it-works.html',
 'A pipeline has stages containing actions that pass declared input and output artifacts between source, build and deployment operations.',
 ('Configure source output, CodeBuild input/output and CodeDeploy input artifact names so each action receives the intended revision’s output.','aws_codepipeline_user_guide#welcome-introducing-artifacts.html'),
 ('The CodePipeline service role requires trust for codepipeline.amazonaws.com and permissions for its actions and artifact access; this service role is not GitHub OIDC federation.','aws_codepipeline_user_guide#pipelines-create-service-role.html'),
 'Verify action execution evidence carries the intended source revision through deployment and a failed action prevents normal progression to dependent actions.')
put(85,'aws_cloudformation_user_guide#Welcome.html#welcome-quickly-replicate-your-infrastructure',
 'The same CloudFormation template can provision equivalent resource declarations in multiple approved target environments.',
 ('For each approved account/Region pair, assume its approved role, verify the caller account, and create the supplied stack with that session and explicit Region.','aws_cli_user_guide#cli-configure-role.html'),
 ('Inspect stack outputs and S3 bucket identity and location in every intended target and check the supplied unapproved targets received no stack.','aws_cloudformation_user_guide#cfn-console-view-stack-data-resources.html'))
put(86,'aws_vpc_user_guide#vpc-network-acls.html',
 ('Diagnose connectivity by checking endpoint DNS resolution, subnet route association and destination route, then required protocol/port rules and return traffic.','aws_vpc_user_guide#vpc-reachability.html'),
 'Network ACLs are stateless subnet rules, so permitted requests also require permitted return traffic.',
 ('Use the supplied connection evidence and reachability analysis to identify the broken component, make the approved correction and retest the endpoint.','aws_vpc_user_guide#vpc-reachability.html'))
put(87,'aws_systems_manager_user_guide#patch-manager.html',
 'Patch Manager uses patch baselines and managed-node targets to scan or install patches and report compliance.',
 ('Use the established maintenance-window task with the approved target set, patch document parameters, concurrency and error limits.','aws_systems_manager_user_guide#sysman-maintenance-assign-tasks.html'),
 ('Inspect task execution and per-node patch compliance results to verify which approved instances were patched and which require follow-up.','aws_systems_manager_user_guide#sysman-patch-compliance.html'))
put(88,'kubernetes_overview#../services-networking/service/',
 'A Kubernetes Service provides a stable network endpoint for a changing set of selected Pods.',
 'Set spec.selector to match the intended Pod labels and ports.port and ports.targetPort to map the Service port to the application’s container port.',
 'Apply the supplied Service, inspect its EndpointSlices or endpoints and test the Service address from the supplied client to verify selected Pods receive traffic.')
put(89,'aws_wa_devops_guidance#qa.nt.6-experiment-with-failure-using-resilience-testing-to-build-recovery-preparedness.html',
 'Controlled failure experiments test how a system behaves under disruption rather than merely inspecting its configuration.',
 'Define the approved fault, limited scope, expected signals and abort conditions before injecting the sandbox failure.',
 ('Observe alarm state history and receipt of the expected notification during the fault, then remove the fault and verify recovery.','aws_cloudwatch_user_guide#Notify_Users_Alarm_Changes.html'))
put(90,'aws_lambda_developer_guide#configuration-versions.html',
 'A published Lambda version is an immutable snapshot of function code and most configuration.',
 ('A Lambda alias points to a published version and can be updated to direct invocations to a different version.','aws_lambda_developer_guide#configuration-aliases.html'),
 ('Publish the tested version with publish-version, set the supplied alias with update-alias --function-version VERSION, test invocation through the alias and roll back by repointing it to the prior version.','aws_lambda_developer_guide#configuration-aliases.html'))
put(91,'kubernetes_overview#../workloads/controllers/deployment/',
 'Changing a Deployment’s Pod template creates a new rollout revision; scaling alone does not create a new template revision.',
 'Use kubectl set image deployment/NAME CONTAINER=IMAGE to update the supplied image and kubectl rollout status deployment/NAME to monitor rollout.',
 'On the controlled failure, inspect rollout history and use kubectl rollout undo deployment/NAME --to-revision=REVISION to restore the approved prior revision and verify readiness.')
put(92,'aws_codedeploy_user_guide#deployment-configurations.html',
 ('An EC2 blue/green deployment installs a revision on replacement instances before rerouting traffic from the original instances.','aws_codedeploy_user_guide#deployments-create.html'),
 ('Use the supplied blue/green deployment group, replacement fleet and load balancer configuration and verify lifecycle and health evidence before the approved traffic rerouting.','aws_codedeploy_user_guide#deployment-groups-create-blue-green.html'),
 ('Use the supplied rollback configuration or redeployment procedure and verify traffic and application behavior return to the known-good revision.','aws_codedeploy_user_guide#deployments-rollback-and-redeploy.html'))
put(93,'python_tutorial#errors.html#defining-clean-up-actions',
 'A Python finally block runs cleanup when control leaves its try block, including when an exception is raised.',
 'Wrap the supplied failing task in try: ... finally: ... and put the supplied scoped cleanup calls in finally.',
 'Track resources created by the exercise and clean up only those resources, then verify their removal and preservation of preexisting resources.')
put(94,'terraform_language#../cli/commands/plan',
 'Terraform normally refreshes tracked resources before planning, revealing out-of-band changes relevant to the proposed actions.',
 'After the supplied drift, compare observed instance settings with configuration and decide whether to restore the declaration or update it to reflect an approved intended change.',
 'Generate and inspect a new plan, run the supplied approval/apply workflow and verify live instance settings match the chosen declaration.',
 'A refresh-only plan updates state and outputs to reflect remote changes; it does not itself change remote infrastructure to restore configuration.')
put(95,'terraform_language#modules/syntax',
 'A module packages resource declarations behind input variables and output values.',
 'Configure module "NAME" with the supplied source and named input arguments; reference its output as module.NAME.OUTPUT.',
 ('Initialize the module, inspect the input values and planned instance settings, apply through the approved workflow and verify the created instance and declared outputs.','terraform_language#../cli/run'))
put(96,'aws_well_architected_framework#cost_right_sizing.html',
 'Rightsizing matches resource type and size to workload performance and capacity requirements rather than simply choosing the smallest instance.',
 'Compare supplied load, utilization and performance evidence with service constraints and recommend a smaller instance only when those constraints remain satisfied.',
 'Account for peak and changing demand in the baseline rather than using one low-utilization sample as sufficient evidence.')
put(97,'aws_guardduty_user_guide#guardduty_findings-summary.html',
 'A finding’s resource identity, severity and activity details provide context needed by the accountable responder.',
 ('Route the supplied finding ID or evidence link, affected resource, observed activity and urgency to the responsible owner and apply the established escalation path.','aws_well_architected_framework#ops06-bp03.html'),
 'Preserve the finding evidence rather than replacing it with an unsupported claim that the resource is compromised.')
put(98,'aws_eventbridge_user_guide#eb-rule-create.html',
 'An EventBridge rule pairs an event pattern with one or more targets to receive matching events.',
 'Set the supplied event bus and pattern and add only the approved SNS or Systems Manager target and required target parameters.',
 ('Configure the target’s required permissions, then send matching and nonmatching test events and inspect the approved target’s execution or notification evidence.','aws_eventbridge_user_guide#eb-events-iam-roles.html'))
put(99,'aws_ecs_developer_guide#ecs_services.html',
 'An ECS service maintains the desired number of tasks and replaces tasks that stop or fail.',
 ('Create the service with the supplied cluster, task definition, network settings and desiredCount.','aws_ecs_developer_guide#service_definition_parameters.html'),
 'Remove one task in the controlled exercise and inspect service events and running/pending task counts until the desired count is restored.')
put(100,'github_actions_docs#how-tos/create-and-publish-actions/set-exit-codes',
 'A nonzero command exit status reports failure to a pipeline step, while zero reports success.',
 ('Run the supplied unit and integration test commands as required steps and make promotion depend on their successful jobs.','github_actions_docs#reference/workflows-and-actions/workflow-syntax'),
 ('Do not set continue-on-error on the blocking test steps; demonstrate a failing supplied test prevents the dependent promotion.','github_actions_docs#reference/workflows-and-actions/workflow-syntax'))
put(101,'aws_wa_devops_guidance#dl.ci.1-maintain-small-batch-sizes-for-changes.html',
 'Small coherent changes reduce review complexity and make delivery feedback easier to act on.',
 ('Submit a focused infrastructure pull request with its intent, coherent diff and saved plan evidence showing the affected EC2 resource.','terraform_language#../cli/commands/plan'),
 ('After the supplied approval, execute the supplied CI apply using the approved saved plan and attach the execution and resource-verification evidence to the change record.','terraform_language#../cli/commands/apply'))
put(102,'aws_well_architected_framework#rel_testing_resiliency.html',
 'Resilience testing deliberately introduces failures to verify the workload can meet its availability requirements.',
 'Limit the approved failure to the supplied AZ components, define abort criteria, and monitor client-visible service behavior during the experiment.',
 ('Check that the remaining independent capacity and request path maintain the required service behavior rather than inferring availability from surviving instance count alone.','aws_well_architected_framework#rel11.html'))
put(103,'aws_cloudformation_user_guide#cfn-console-delete-stack.html',
 'Resource deletion must respect dependencies; CloudFormation uses resource relationships when deleting a stack.',
 'Identify only the supplied exercise resources by stack membership or approved tags, remove dependent resources before their prerequisites and verify deletion results.',
 'Retained resources and failed deletions need explicit inspection and approved follow-up; a completed deletion operation is not billing verification.')
put(104,'aws_iam_user_guide#id_credentials_temp_use-resources.html',
 'Recovery execution needs a valid, unexpired session with the permissions required for backup access and resource creation.',
 'Establish the approved recovery session, inspect its identity and expiry, and test the supplied backup-read and recovery-resource operations before rehearsal.',
 'A valid credential lifetime does not prove sufficient authorization; verify both access outcomes and lifetime.')
put(105,'aws_well_architected_framework#rel_testing_resiliency.html',
 'Recovery testing should use a controlled environment that limits the experiment’s effects.',
 'Prepare the supplied isolated account and network target and check restoration destinations and client test traffic do not point to production.',
 'Record the approved scope and stop conditions before provisioning recovery resources or directing test traffic.')
put(106,'aws_systems_manager_user_guide#automation-action-approve.html',
 'An aws:approve Automation step pauses execution pending approval or rejection by the designated approvers.',
 'Put the approval step before the protected operation and use the supplied branching or failure path to prevent that operation on rejection or stop.',
 ('Stop an Automation execution with the approved stop operation when a stop condition occurs and inspect execution state before allowing further actions.','aws_systems_manager_user_guide#automation-working-executing.html'))
put(107,'aws_systems_manager_user_guide#automation-working-execution.html',
 'Automation execution details include an execution identifier, step statuses, inputs, outputs and failure information.',
 'Record execution ID, acting role, target identities, start/end times and per-step outcomes for the supplied response.',
 ('Use CloudTrail request identity and operation evidence to attribute the underlying AWS actions; success and failure outcomes both belong in the response record.','aws_cloudtrail_user_guide#cloudtrail-event-reference-record-contents.html'))
put(108,'aws_cloudtrail_user_guide#cloudtrail-log-file-validation-intro.html',
 'CloudTrail log-file integrity validation uses signed digest files and hashes to detect modification or deletion of delivered log files.',
 ('Run aws cloudtrail validate-logs --trail-arn ARN --start-time TIME --end-time TIME against the supplied log/digest interval and inspect reported validation failures.','aws_cloudtrail_user_guide#cloudtrail-log-file-validation-cli.html'),
 'Digest validation supplies tamper evidence but does not itself prevent unauthorized access or deletion.')
put(109,'aws_s3_user_guide#object-lock.html',
 'S3 Object Lock applies retention to object versions using governance or compliance mode and a retain-until date.',
 ('Apply the supplied default retention duration and mode on the prepared Object Lock bucket and inspect individual audit-object version retention.','aws_s3_user_guide#object-lock-managing.html'),
 'Compliance mode prevents deletion or shortening of retention during the retention period even by root; governance mode permits bypass only with the necessary bypass authorization and request.')
put(110,'terraform_language#backend/s3',
 'The S3 backend stores Terraform state in a specified bucket and key, separate from the configuration that declares managed resources.',
 'Provision the protected backend bucket with the supplied local-state bootstrap configuration before selecting it as the backend.',
 'Set terraform { backend "s3" { bucket = "BUCKET"; key = "KEY"; region = "REGION" } } using normal HCL line-separated arguments and the approved settings.',
 ('Run terraform init -migrate-state after changing the backend, approve the supplied migration and verify state is at the intended bucket/key.','terraform_language#../cli/commands/init'))
put(111,'terraform_language#meta-arguments/lifecycle',
 'By default Terraform destroys an object before creating its replacement; create_before_destroy requests the reverse order where supported.',
 'prevent_destroy rejects a plan that would destroy the protected resource while that lifecycle rule remains in its configuration.',
 'Set the supplied lifecycle argument in the resource block, introduce the controlled replacement-triggering change, and inspect the plan’s replacement order or prevention error before the approved permitted apply.',
 'Lifecycle settings constrain replacement mechanics but do not replace scope and impact approval.')
put(112,'aws_cloudformation_user_guide#cfn-console-create-stack.html',
 'Creating a stack from a template provisions its declared resources under the target account’s execution authority and selected Region.',
 'Use the supplied restoration template, approved recovery credentials, explicit isolated target and required parameters to create the replacement EC2 stack.',
 ('Monitor stack events until creation completes, inspect resource IDs and outputs, and run the supplied instance and service recovery-ready checks.','aws_cloudformation_user_guide#cfn-console-view-stack-data-resources.html'))
put(113,'aws_inspector_user_guide#findings-understanding.html',
 'Inspector findings report vulnerability evidence, affected resources and severity that can inform release decisions.',
 'Compare the supplied scan report with the stated severity threshold and documented exception policy to decide whether a finding is actionable.',
 ('Make the scan-policy check return failure for an actionable unexcepted finding and require its success before promotion; retain the report and policy decision as evidence.','github_actions_docs#how-tos/create-and-publish-actions/set-exit-codes'))
put(114,'aws_codepipeline_user_guide#troubleshooting.html',
 'Pipeline execution and action history identify failed actions and their error details.',
 ('Find the first failing action in the selected execution, inspect its input artifact revision and linked service logs, and use the error evidence to identify the correction.','aws_codepipeline_user_guide#pipelines-view-console.html'),
 'Retest after the approved correction and verify that action succeeds before investigating later dependent actions that did not run.')
put(115,'aws_ec2_user_guide#monitoring-system-instance-status-check.html',
 'EC2 system status checks concern underlying AWS host issues, while instance checks concern the instance’s software and networking.',
 ('Use the supplied metric and log time window to identify the affected workload, then inspect the component’s service status, events and logs rather than assuming the symptom proves its cause.','aws_well_architected_framework#ops06-bp01.html'),
 ('For a container, inspect container state, exit status and recent logs; apply the evidence-supported correction and repeat the supplied health check.','aws_ecs_developer_guide#stopped-task-errors.html'))
put(116,'aws_codepipeline_user_guide#actions-invoke-lambda-function.html',
 'A post-deployment validation action checks live application behavior rather than merely whether a deployment operation completed.',
 'Run the supplied smoke-check action against the deployed endpoint and verify the expected response for the deployed revision.',
 'Report action success only on a passing check and failure otherwise so dependent release progression remains blocked on failed live behavior.')
put(117,'aws_eventbridge_user_guide#eb-rule-retry-policy.html',
 'EventBridge retries retryable target-delivery failures within configured maximum event age and retry-attempt limits.',
 'Configure the target RetryPolicy MaximumRetryAttempts and MaximumEventAgeInSeconds to the approved finite budget.',
 ('Configure DeadLetterConfig with the approved SQS queue ARN and required queue permissions, then inspect a seeded exhausted delivery failure in that queue.','aws_eventbridge_user_guide#eb-rule-dlq.html'),
 'Some nonretryable delivery failures go directly to failure capture; retry configuration does not guarantee every failure receives retries.')
put(118,'aws_ecs_developer_guide#deployment-type-ecs.html',
 'An ECS rolling deployment replaces service tasks according to minimumHealthyPercent and maximumPercent relative to desiredCount.',
 'Register the supplied new image version in a task-definition revision and update the service to that revision.',
 'Inspect service events, running task revisions and health until the supplied steady-state criteria are met; a service-update request alone is not proof of a healthy rollout.')
put(119,'twelve_factor_app#build-release-run',
 'The build stage produces a build artifact; release combines that build with environment configuration, and run executes the release.',
 'Promote the same immutable artifact reference or digest to the next environment while supplying that environment’s configuration rather than rebuilding the source.',
 ('Compare the deployed artifact digests in staging and production and their recorded build provenance to verify the tested output is the promoted output.','github_actions_docs#how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations'))
put(120,'aws_cost_management_user_guide#ce-what-is.html',
 'Cost Explorer data is refreshed at least once every 24 hours and some data can take longer to appear.',
 ('Inspect the supplied teardown interval with account and service or usage-type filters and compare usage timestamps with resource-deletion evidence.','aws_cost_management_user_guide#ce-filtering.html'),
 'Distinguish charges for usage before deletion from evidence of continuing usage and repeat the check after the billing data refresh rather than declaring zero cost from resource absence.')
put(121,'terraform_language#backend/s3',
 'S3 backend access needs permissions for the selected state bucket and object key; state can contain sensitive values.',
 'Scope approved readers and writers to the required ListBucket prefix and GetObject/PutObject state object operations, with supplied locking permissions configured separately.',
 'Initialize the supplied backend, provision the separate exercise bucket through the approved identity, and test that an unapproved identity cannot read or overwrite state.',
 'State access isolation prevents unauthorized access; it is separate from the mechanism that coordinates concurrent authorized writers.')
put(122,'terraform_language#backend/s3',
 'The S3 backend supports lock-file locking when use_lockfile = true; locking is opt-in.',
 'Enable use_lockfile in the supplied backend configuration and provide the supplied GetObject, PutObject and DeleteObject permissions on the .tflock object.',
 'During the controlled state-changing operation that holds the lock, attempt a competing operation and verify it cannot acquire the lock or change state; do not disable locking to bypass the test.',
 'Locking coordinates concurrent state writers; it is not an authorization boundary against identities that can directly change state objects.')
put(123,'aws_codepipeline_user_guide#approvals.html',
 'A manual approval action stops pipeline progression until an authorized approver approves; rejection or expiration fails the action.',
 'Place an approval action between staging and production with the supplied review link or revision context and authorized approver permissions.',
 'Verify the pipeline stops at approval and advances only after approval of the intended execution and revision.')
put(124,'aws_well_architected_framework#ops05-bp01.html',
 'A runbook describes known procedures and their expected operational outcomes.',
 'Verify the established runbook’s preconditions, execute only the approved actions and check each expected result before advancing.',
 ('On a supplied stop condition or an outcome outside the runbook’s bounds, stop routine execution and escalate with the observed evidence.','aws_well_architected_framework#ops06-bp03.html'))
put(125,'aws_wa_devops_guidance#ag.dlm.1-define-recovery-objectives-to-maintain-business-continuity.html',
 'Recovery verification must test both restoration time against RTO and recoverable data loss against RPO.',
 'Using the supplied timestamps, measure elapsed time from the defined disruption start to passing service-readiness checks and compare it with RTO.',
 'Using the supplied recovery markers, measure the gap between the disruption point and the latest recovered data point and compare it with RPO; a running service alone does not prove either objective was met.')
put(126,'aws_well_architected_framework#ops11-bp02.html',
 'Post-incident analysis documents the incident’s impact, events, contributing causes and actions to reduce recurrence.',
 'Write a timeline from supplied evidence and distinguish direct observations from causal conclusions supported by the verified fix.',
 'Record one preventive action justified by the demonstrated cause, with an accountable owner and a way to verify completion.')
put(127,'aws_well_architected_framework#rel13-bp02.html',
 'Recovery procedures include restoring service and directing clients to the recovered environment.',
 'Confirm the restored target’s supplied readiness checks pass, perform the approved DNS or application endpoint switch and verify clients reach the restored target.',
 'For DNS cutover, account for cached answers and TTL when testing client convergence rather than assuming every client immediately uses the new endpoint.')
