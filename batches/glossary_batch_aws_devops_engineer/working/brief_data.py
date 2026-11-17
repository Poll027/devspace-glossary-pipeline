# Evidence specifications: one tile per indexed entry; locators are documentation pages.
DATA = {}
def put(i, ref, *facts):
 DATA[i]=[(f,ref) if isinstance(f,str) else f for f in facts]
put(0,'aws_cli_user_guide#cli-configure-profiles.html',
 'A named AWS CLI profile groups credential and configuration settings; select it with --profile NAME.',
 ('Run aws sts get-caller-identity --profile NAME to inspect the caller ARN and account ID.','aws_cli_user_guide#cli-configure-files.html'),
 ('Run aws configure list --profile NAME to inspect the effective configuration and where its values came from; --region REGION overrides the configured Region for a command.','aws_cli_user_guide#cli-configure-files.html'))
put(1,'aws_vpc_user_guide#subnet-sizing.html',
 'An IPv4 subnet CIDR must be within its VPC CIDR and must not overlap another subnet in that VPC.',
 'IPv4 subnet sizes range from /16 to /28; AWS reserves the first four addresses and the last address of each subnet.',
 'Choose subnet ranges inside the VPC that do not intersect, and allow for the five reserved addresses when checking usable capacity.',
 ('Each subnet resides entirely in one Availability Zone; create separate subnets for workloads in different Availability Zones.','aws_vpc_user_guide#configure-subnets.html'))
put(2,'aws_ecs_developer_guide#Welcome.html',
 'ECS is a managed container orchestration service that schedules container workloads; customers supply and operate their applications.',
 ('Managed EKS runs the Kubernetes control plane; customers retain responsibility for workload configuration and, depending on the compute option, worker nodes.','aws_eks_user_guide#shared-responsibility.html'),
 ('Choose between ECS and EKS by comparing the need for Kubernetes APIs and ecosystem with the team’s willingness to operate Kubernetes workloads.','aws_eks_user_guide#what-is-eks.html'))
put(3,'aws_vpc_user_guide#subnet-route-tables.html',
 'A subnet uses its explicitly associated route table or, without an explicit association, the VPC main route table.',
 ('Among matching destination routes, the most specific destination prefix takes priority.','aws_vpc_user_guide#route-tables-priority.html'),
 ('Associate the subnet with the intended route table and add an IPv4 0.0.0.0/0 route targeting the attached internet gateway for internet-bound destinations not matched by a more specific route.','aws_vpc_user_guide#VPC_Internet_Gateway.html'))
put(4,'aws_wa_devops_guidance#ag.dlm.1-define-recovery-objectives-to-maintain-business-continuity.html',
 'Recovery time objective (RTO) is the maximum acceptable time to restore service after a disruption.',
 'Recovery point objective (RPO) is the maximum acceptable data loss measured in time.',
 'Set recovery objectives from business requirements and use them to choose recovery capabilities that meet the tolerated downtime and data loss.')
put(5,'aws_rds_user_guide#Welcome.html#Welcome.Concepts.SharedResponsibility',
 'With EC2, customers manage the guest operating system, including updates and security patches.',
 'With RDS, AWS manages database infrastructure and operating-system maintenance, while customers manage their data and application use.',
 'Assign duties by the service boundary: AWS manages its infrastructure, while customers retain responsibilities for data, access and customer-controlled configuration.')
put(6,'aws_well_architected_framework#rel_withstand_component_failures.html',
 'Redundant components and multiple locations can keep a workload available when a component fails.',
 ('Capacity must accommodate workload demand; adding or removing resources helps match capacity to changing demand.','aws_well_architected_framework#rel_adapt_to_changes_in_demand.html'),
 'For a component-failure constraint, evaluate independent redundant capacity rather than merely increasing the size of the same component.')
put(7,'aws_well_architected_framework#ops_ops_event_response.html',
 'Operational events need response processes with identified owners and escalation paths.',
 'Assign event-response responsibility and document when and to whom unresolved issues are escalated.',
 ('Identify a team responsible for each resource and process so operators know whom to engage.','aws_well_architected_framework#ops_ops_model_def_resource_owners.html'))
put(8,'aws_iam_user_guide#reference_policies_elements.html',
 'An identity-based policy attaches to an identity and specifies permitted or denied actions on resources.',
 'A statement uses Effect, Action and Resource, with optional Condition tests to scope when it applies.',
 ('For a request, compare action, resource and condition values with applicable statements; explicit deny overrides an allow, and absent an applicable allow the request is implicitly denied.','aws_iam_user_guide#reference_policies_evaluation-logic.html'))
put(9,'github_actions_docs#reference/workflows-and-actions/workflow-syntax',
 'Workflow YAML files are stored in .github/workflows; on defines the triggering events.',
 'jobs defines jobs, runs-on selects the runner, and steps lists actions invoked with uses or commands executed with run.',
 ('Inspect a workflow run’s job and step logs to verify which steps ran and which succeeded or failed.','github_actions_docs#how-tos/monitor-workflows/use-workflow-run-logs'))
put(10,'dora_capabilities#guides/dora-metrics/',
 'Deployment frequency measures how often changes are deployed; change lead time measures the elapsed time for a committed change to reach production.',
 'Change fail rate measures the proportion of deployments requiring intervention; failed deployment recovery time measures how long recovery from a failed deployment takes.',
 'Compare throughput and instability measures together over time and within application context rather than using one measure to rank individuals.')
put(11,'aws_eventbridge_user_guide#eb-event-patterns.html',
 'An EventBridge event pattern describes event fields and values that an event must match.',
 'Write a JSON object containing the fields to filter and arrays of acceptable values; fields omitted from the pattern are not required to match.',
 ('Test a pattern against both matching and nonmatching sample events with the EventBridge sandbox or TestEventPattern before using it in a rule.','aws_eventbridge_user_guide#eb-test-event-pattern.html'))
put(12,'aws_ec2_user_guide#ec2-launch-instance-wizard.html',
 'Launching an EC2 instance requires choices such as AMI, instance type and network placement; an AMI supplies the initial software image.',
 'In the launch workflow, use the approved AMI, subnet and supplied IAM instance profile, then inspect the created instance’s ID and settings.',
 ('An instance profile contains an IAM role and attaches it to EC2; applications on the instance can use that role’s temporary credentials.','aws_iam_user_guide#id_roles_use_switch-role-ec2_instance-profiles.html'),
 ('Inspect instance state and status checks to distinguish lifecycle state from reported host or instance health.','aws_ec2_user_guide#monitoring-system-instance-status-check.html'))
put(13,'aws_s3_user_guide#UsingObjects.html',
 'An S3 object consists of data and metadata and is identified within a bucket by its object key.',
 ('Use aws s3 cp LOCAL_FILE s3://BUCKET/KEY --profile NAME --region REGION to upload, and reverse the source and destination to download.','aws_cli_user_guide#cli-services-s3-commands.html'),
 ('A bucket is created in an AWS Region; verify the intended bucket location and caller access when storing or retrieving an object.','aws_s3_user_guide#UsingBucket.html'))
put(14,'aws_cloudwatch_user_guide#publishingMetrics.html',
 'A custom CloudWatch metric is identified by its namespace, name and dimension combination.',
 'Publish a metric with put-metric-data, specifying namespace, metric name, value and the intended dimensions.',
 ('Each distinct dimension combination identifies a distinct metric; query the same combination that was published to select the intended series.','aws_cloudwatch_user_guide#cloudwatch_concepts.html#Dimension'))
put(15,'python_tutorial#../library/os.html#os.environ',
 'Process environment variables provide named string values that a supplied program can read as configuration.',
 'For the supplied validator, set FLEET_ALLOWED_INSTANCE_IDS to the approved comma-separated IDs and FLEET_MAX_TARGETS to the approved positive integer limit in its environment configuration.',
 ('Exercise malformed and out-of-scope inputs and check the supplied validator rejects them before invoking a resource-changing operation.','aws_well_architected_framework#ops_dev_integ_deploy_mgmt.html'))
put(16,'aws_cloudformation_user_guide#using-cfn-updating-stacks-changesets.html',
 'A change set previews proposed stack resource changes without executing them.',
 'Review additions, modifications, removals and replacement indicators before authorizing execution; a preview does not guarantee that execution will succeed.',
 ('For a new stack, create a CREATE change set from the supplied template, wait for creation to complete, inspect it, and execute the approved set to provision the resources.','aws_cloudformation_user_guide#using-cfn-updating-stacks-changesets-create.html'))
put(17,'aws_iam_user_guide#reference_policies_examples_aws_my-sec-creds-self-manage.html',
 'The aws:MultiFactorAuthPresent condition indicates whether qualifying temporary credentials were authenticated with MFA.',
 'A Deny with BoolIfExists on aws:MultiFactorAuthPresent set to false can block non-MFA requests, including requests where the key is absent, subject to the statement’s scoped actions.',
 'Apply the supplied scoped MFA policy and compare an allowed MFA-authenticated request with a denied request without MFA.')
put(18,'aws_iam_user_guide#id_roles_create_for-user.html',
 'A role trust policy identifies principals allowed to assume the role and any conditions for assumption.',
 'Set Principal to the approved principal and Action to sts:AssumeRole with the supplied conditions in the role’s trust policy.',
 'For cross-account assumption, the caller also needs permission to call sts:AssumeRole on the role; test approved and unapproved principals.',
 ('A role’s permissions policy controls what an assumed session may do, rather than who may assume it.','aws_iam_user_guide#id_roles.html'))
put(19,'aws_iam_user_guide#root-user-best-practices.html',
 'The AWS account root user has broad account authority and should not be used for routine tasks.',
 'Protect root access with MFA and do not create root access keys; delete existing root access keys when they are no longer needed.',
 'Review root-use and access-key evidence against the root-protection checklist, using non-root identities for routine operations.')
put(20,'aws_cloudtrail_user_guide#view-cloudtrail-events.html',
 'CloudTrail event history exposes recent management events for the selected Region; it does not represent all application activity.',
 'Filter event history by an attribute such as event name, resource name or user name and the relevant time interval.',
 ('Inspect eventTime, eventName, userIdentity and requestParameters or resources to attribute a change to an actor, operation, target and time.','aws_cloudtrail_user_guide#cloudtrail-event-reference-record-contents.html'))
put(21,'aws_cost_management_user_guide#cost-alloc-tags.html',
 'Cost-allocation tags categorize costs by resource-associated tag keys and values after activation for billing.',
 ('Activate the desired cost-allocation tag, then group Cost Explorer costs by that tag for the chosen period.','aws_cost_management_user_guide#ce-filtering.html'),
 'Resources without the relevant active tag can leave spend unallocated to the intended workload category.')
put(22,'aws_cloudwatch_user_guide#Working-with-log-groups-and-streams.html',
 'A log group holds log streams with shared retention and access settings; a stream is a sequence of events from one source.',
 ('Configure the supplied log collector with the application file path, log group and stream name, and verify a known JSON event arrives in that stream.','aws_cloudwatch_user_guide#CloudWatch-Agent-Configuration-File-Details.html'),
 ('CloudWatch Logs Insights can discover fields in JSON log events, so preserving structured event fields makes them queryable.','aws_cloudwatch_user_guide#CWL_AnalyzeLogData-discoverable-fields.html'))
put(23,'linux_man_pages#linux/man-pages/man5/systemd.service.5.html',
 'A service configuration change must be activated through the service’s supported reload or restart mechanism; editing a file alone does not demonstrate the running service uses it.',
 'Save the prior configuration, edit the supplied setting, use the supplied validation command and activate the change only if validation succeeds.',
 'Inspect service status and the supplied effective-setting check; if the checks fail, restore the saved configuration and reactivate it using the supplied procedure.')
put(24,'aws_wa_devops_guidance#dl.ads.1-use-progressive-delivery-to-minimize-risk.html',
 'Rolling delivery replaces portions of the workload progressively rather than replacing all instances simultaneously.',
 'Blue/green delivery maintains separate old and new environments and switches traffic to the new environment.',
 'Canary delivery exposes a new version to a limited share of traffic before broader rollout.',
 'Choose a strategy by comparing traffic exposure, available parallel capacity and the ability to return traffic to a known-good version.')
put(25,'aws_cloudwatch_user_guide#CloudWatch-Agent-Configuration-File-Details.html',
 'The CloudWatch agent collects configured host metrics and logs and sends them to CloudWatch.',
 'In the agent configuration, choose metrics under metrics_collected and append instance-identifying dimensions such as InstanceId.',
 ('Start the agent with amazon-cloudwatch-agent-ctl using fetch-config, the supplied configuration location and -s, then verify the expected metric and instance dimension in CloudWatch.','aws_cloudwatch_user_guide#start-CloudWatch-Agent-on-premise-SSM-onprem.html'))
put(26,'aws_cloudwatch_user_guide#AlarmThatSendsEmail.html',
 'A metric alarm evaluates a statistic over periods against a threshold and has OK, ALARM and INSUFFICIENT_DATA states.',
 'EvaluationPeriods is the number of evaluated periods, and DatapointsToAlarm is the number of breaching datapoints required within that window.',
 'Set the supplied metric, statistic, period, comparison operator and threshold along with the evaluation counts; compare the resulting state with the supplied samples.',
 'Missing-data settings are breaching, notBreaching, ignore (retain current state), and missing (insufficient data when all datapoints are missing); missing is the default.')
put(27,'aws_iam_user_guide#id_roles_providers_saml.html',
 ('IAM Identity Center permission sets define permissions made available through assignments to users or groups in specified AWS accounts.','aws_iam_user_guide#id_roles_providers.html'),
 ('Use the supplied Identity Center assignment workflow to assign the approved user or group, account and permission set, then sign in to that account and test the intended access.','aws_cli_user_guide#cli-configure-sso.html'),
 ('Configure a named SSO profile with aws configure sso and establish a session with aws sso login --profile NAME rather than storing long-lived IAM user keys.','aws_cli_user_guide#cli-configure-sso.html'))
put(28,'aws_vpc_user_guide#vpc-security-groups.html',
 'Security groups contain allow rules for traffic evaluated at associated network interfaces; they have no explicit deny rules.',
 'Security groups are stateful: response traffic for an allowed connection is allowed regardless of rules in the response direction.',
 ('Add inbound rules specifying the required protocol, port range and approved source, remove unnecessary ingress, and test the required connections and their responses.','aws_vpc_user_guide#security-group-rules.html'),
 'Security groups do not filter traffic to Amazon-provided DNS or EC2 instance metadata services.')
put(29,'terraform_language#providers/requirements',
 'Declare the AWS provider under terraform { required_providers { aws = { source = "hashicorp/aws", version = "= APPROVED_VERSION" } } } to require an exact approved version.',
 ('Declare resource "aws_instance" "NAME" with ami, instance_type and subnet_id set to the supplied values.','terraform_aws_provider#resources/instance'),
 ('Run terraform init to install providers, terraform plan to inspect intended changes, and the approved terraform apply step to create the instance; verify the instance settings.','terraform_language#../cli/run'))
put(30,'aws_iam_user_guide#access_policies_identity-vs-resource.html',
 'A resource-based policy is attached to a resource and specifies the principals, actions and resources covered by its statements.',
 'For an S3 bucket policy, compare Principal, Action, Resource and Condition with the caller’s request; bucket and object ARNs identify different resource scopes.',
 ('Same-account identity and resource permissions can contribute allows, but applicable explicit denies override them; cross-account access generally requires permission on both sides.','aws_iam_user_guide#reference_policies_evaluation-logic.html'))
put(31,'aws_control_tower_user_guide#account-factory.html',
 'Account Factory provisions and enrolls accounts into a governed landing zone using standardized account settings.',
 ('Execute the established provisioning workflow with the approved account inputs and inspect the account’s enrollment and organizational-unit placement.','aws_control_tower_user_guide#methods-of-provisioning.html'),
 ('Verify the supplied baseline checkpoints against the account’s applied controls; creating an account alone does not demonstrate governance completion.','aws_control_tower_user_guide#how-controls-work.html'))
put(32,'python_tutorial#venv.html',
 'A virtual environment isolates the Python interpreter context and installed packages used by an application.',
 'Create one with python -m venv ENV_DIR and activate it using the platform’s activation command, such as source ENV_DIR/bin/activate on Unix.',
 'Install supplied dependencies with python -m pip install -r requirements.txt inside the environment, inspect them with python -m pip list, and run the supplied script with that interpreter.',
 ('Confirm the approved AWS profile and Region through the supplied credential configuration before running AWS automation.','boto3_guide#credentials.html'))
put(33,'aws_cli_user_guide#cli-usage-pagination.html',
 'The AWS CLI automatically follows service-side pagination for supported commands unless automatic pagination is disabled.',
 'Use an explicit --profile and --region with --output json for structured inventory and avoid --no-paginate when the full listing is required.',
 '--page-size changes service-call page size rather than the total output count; --max-items limits output and a returned NextToken must be resumed with --starting-token when manually collecting the remainder.')
put(34,'aws_well_architected_framework#ops_event_response_use_runbooks.html',
 'A runbook documents procedures for a known operational outcome and should be usable by the operator performing the task.',
 'Write the task’s preconditions, ordered actions and expected results so execution can be checked rather than inferred.',
 ('Include failure-handling and escalation instructions identifying when routine execution must stop and who takes over.','aws_well_architected_framework#ops_event_response_defined_escalation_paths.html'))
put(35,'kubernetes_overview#../workloads/pods/pod-lifecycle/',
 'A Pod groups containers with shared networking and storage and has a lifecycle distinct from the controller that may replace it.',
 'Pod phases include Pending, Running, Succeeded, Failed and Unknown; phase alone is not a complete diagnosis of container health.',
 ('Use kubectl get pod NAME, kubectl describe pod NAME and kubectl logs NAME -c CONTAINER to inspect status, scheduling or runtime events and container output.','kubernetes_overview#../../tasks/debug/debug-application/debug-pods/'))
put(36,'aws_rds_user_guide#USER_DescribeInstance.html',
 'An RDS DB instance has an identifier, engine, endpoint and operational status that can be inspected in the console or through describe-db-instances.',
 'Inspect the intended DB instance and verify its engine and status before attempting the supplied database connection.',
 ('Connect using the supplied endpoint, database client and approved credentials, then run the supplied query to check the data marker; instance status alone does not verify application data.','aws_rds_user_guide#CHAP_CommonTasks.Connect.html'))
put(37,'aws_s3_user_guide#Versioning.html',
 'S3 versioning retains multiple versions of an object, including versions displaced by overwrites.',
 'In a versioning-enabled bucket, a simple delete ordinarily creates a delete marker rather than removing prior versions; deleting a specified version permanently removes it.',
 ('Enable bucket versioning and retrieve a prior object using its version ID, or remove the relevant delete marker to expose the preceding version.','aws_s3_user_guide#RestoringPreviousVersions.html'),
 ('Inspect noncurrent-version expiration and other lifecycle rules so required recoverable versions remain for the required window.','aws_s3_user_guide#intro-lifecycle-rules.html'))
put(38,'aws_ecr_user_guide#docker-push-ecr-image.html',
 'ECR stores container images in repositories and assigns image digests that identify image content.',
 'Authenticate Docker with aws ecr get-login-password --region REGION piped to docker login --username AWS --password-stdin REGISTRY.',
 'Tag the already-built image with REGISTRY/REPOSITORY:TAG and run docker push with that reference.',
 ('Use docker pull REGISTRY/REPOSITORY@sha256:DIGEST to retrieve the exact image and verify publisher and consumer access with their approved identities.','aws_ecr_user_guide#docker-pull-ecr-image.html'))
put(39,'github_actions_docs#how-tos/secure-your-work/use-artifact-attestations',
 'An artifact attestation binds provenance such as source repository, revision and build workflow to an artifact digest.',
 'Generate provenance for the supplied output using an attestation step whose subject identifies the output file or image digest.',
 ('Publish the output under a version that cannot be overwritten and verify its digest and provenance before using it for deployment.','aws_ecr_user_guide#image-tag-mutability.html'))
put(40,'aws_cloudformation_user_guide#template-anatomy.html',
 'A CloudFormation template’s Resources section declares resources by logical ID, Type and Properties.',
 ('An S3 bucket declaration uses Type: AWS::S3::Bucket; Ref on its logical ID returns its bucket name.','aws_cloudformation_user_guide#aws-resource-s3-bucket.html'),
 ('Modify the supplied declared property and references, validate with aws cloudformation validate-template --template-body file://TEMPLATE, and create the sandbox stack from the approved template.','aws_cloudformation_user_guide#using-cfn-validate-template.html'),
 ('Inspect stack events and outputs and the bucket’s live property to confirm the declaration was deployed.','aws_cloudformation_user_guide#cfn-console-view-stack-data-resources.html'))
put(41,'aws_secrets_manager_user_guide#retrieving-secrets.html',
 'Secrets Manager stores protected secret values and returns them to authorized consumers at runtime.',
 'Retrieve a secret through GetSecretValue using the supplied secret identifier and approved runtime identity, with secretsmanager:GetSecretValue permission.',
 'Use the retrieved value in the runtime consumer without writing it into source code or logs; verify success through the consumer’s safe result rather than displaying the value.')
put(42,'aws_wa_devops_guidance#continuous-improvement.html',
 'Continuous improvement uses feedback and measured outcomes to identify and address delivery friction.',
 'Identify a bottleneck supported by the supplied delivery evidence and propose one bounded change with a measurable expected outcome.',
 'Compare the success signal before and after the change to determine whether the intervention improved the intended outcome.')
put(43,'aws_config_developer_guide#evaluate-config.html',
 'AWS Config rules evaluate recorded resource configuration against desired conditions and report compliance results.',
 ('Open the rule’s noncompliant resources and inspect the affected resource, evaluation result and rule parameters to identify the configuration mismatch.','aws_config_developer_guide#evaluate-config_view-compliance.html'),
 ('Choose the established remediation or escalation path from the governing policy rather than treating a compliance result as proof of an attack.','aws_config_developer_guide#remediation.html'))
