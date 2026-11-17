from brief_data import DATA, put
# Use current, verified documentation page locators rather than retired page names.
REPLACE={
'aws_cli_user_guide#cli-configure-profiles.html':'aws_cli_user_guide#cli-configure-files.html#cli-configure-files-using-profiles',
'aws_well_architected_framework#rel_withstand_component_failures.html':'aws_well_architected_framework#rel11.html',
'aws_well_architected_framework#rel_adapt_to_changes_in_demand.html':'aws_well_architected_framework#rel07.html',
'aws_well_architected_framework#ops_ops_event_response.html':'aws_well_architected_framework#ops06.html',
'aws_well_architected_framework#ops_ops_model_def_resource_owners.html':'aws_well_architected_framework#fnd01-bp02.html',
'aws_well_architected_framework#ops_dev_integ_deploy_mgmt.html':'aws_well_architected_framework#ops04-bp01.html',
'aws_eventbridge_user_guide#eb-test-event-pattern.html':'aws_eventbridge_user_guide#eb-event-pattern-sandbox.html',
'aws_cost_management_user_guide#cost-alloc-tags.html':'aws_cost_management_user_guide#../../../awsaccountbilling/latest/aboutv2/custom-tags.html',
'aws_cloudwatch_user_guide#Working-with-log-groups-and-streams.html':'aws_cloudwatch_user_guide#../logs/Working-with-log-groups-and-streams.html',
'aws_cloudwatch_user_guide#CWL_AnalyzeLogData-discoverable-fields.html':'aws_cloudwatch_user_guide#../logs/CWL_AnalyzeLogData-discoverable-fields.html',
'linux_man_pages#linux/man-pages/man5/systemd.service.5.html':'linux_man_pages#man5/systemd.service.5.html',
'aws_wa_devops_guidance#dl.ads.1-use-progressive-delivery-to-minimize-risk.html':'aws_wa_devops_guidance#dl.ads.3-use-staggered-deployment-and-release-strategies.html',
'aws_well_architected_framework#ops_event_response_use_runbooks.html':'aws_well_architected_framework#ops05-bp01.html',
'aws_well_architected_framework#ops_event_response_defined_escalation_paths.html':'aws_well_architected_framework#ops06-bp03.html',
'aws_rds_user_guide#USER_DescribeInstance.html':'aws_rds_user_guide#accessing-monitoring.html',
'aws_wa_devops_guidance#continuous-improvement.html':'aws_wa_devops_guidance#dl.cd.6-refine-delivery-pipelines-using-metrics-for-continuous-improvement.html',
'aws_cost_management_user_guide#budgets-create-notifications.html':'aws_cost_management_user_guide#budgets-create.html',
'aws_ecs_developer_guide#ecs_run_task.html':'aws_ecs_developer_guide#standalone-task-create.html',
'aws_systems_manager_user_guide#run-command-tutorial.html':'aws_systems_manager_user_guide#walkthrough-cli.html',
'aws_well_architected_framework#rel_planning_for_recovery.html':'aws_well_architected_framework#rel13-bp02.html',
'aws_systems_manager_user_guide#sysman-patch-compliance.html':'aws_systems_manager_user_guide#patch-manager-view-compliance-results.html',
'aws_eventbridge_user_guide#eb-rule-create.html':'aws_eventbridge_user_guide#eb-create-rule-wizard.html',
'aws_well_architected_framework#rel_testing_resiliency.html':'aws_well_architected_framework#rel12-bp04.html',
'aws_systems_manager_user_guide#automation-working-execution.html':'aws_systems_manager_user_guide#automation-working-executions.html',
'aws_well_architected_framework#cost_right_sizing.html':'aws_well_architected_framework#cost06-bp02.html',
'aws_well_architected_framework#ops11-bp02.html':'aws_well_architected_framework#ops07-bp01.html',
'aws_wa_devops_guidance#dl.ci.1-maintain-small-batch-sizes-for-changes.html':'aws_wa_devops_guidance#dl.ci.2-integrate-code-changes-frequently.html',
'aws_cloudwatch_user_guide#AlarmThatSendsEmail.html':'aws_cloudwatch_user_guide#alarm-evaluation.html',
'github_actions_docs#how-tos/secure-your-work/use-artifact-attestations':'github_actions_docs#how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations',
}
for i,fs in DATA.items():DATA[i]=[(f,REPLACE.get(r,r)) for f,r in fs]
# Distinguish mechanism, configuration syntax and the actual check.
DATA[26][2]=(DATA[26][2][0],'aws_cloudwatch_user_guide#ConsoleAlarms.html')
DATA[26][3]=(DATA[26][3][0],'aws_cloudwatch_user_guide#alarms-and-missing-data.html')
DATA[25][2]=(DATA[25][2][0],'aws_cloudwatch_user_guide#start-CloudWatch-Agent-on-premise-SSM-onprem.html')
DATA[14][1]=(DATA[14][1][0],'aws_cloudwatch_user_guide#publishingMetrics.html#publishingDataPoints')
DATA[15][1]=('Set the supplied allowlist environment variable FLEET_ALLOWED_INSTANCE_IDS to the approved comma-separated IDs and the supplied FLEET_MAX_TARGETS variable to the approved positive integer limit; these are configuration inputs to the supplied validator, not Python language keywords.','python_tutorial#../library/os.html#os.environ')
put(23,'aws_well_architected_framework#ops04-bp01.html',
 'A configuration change needs validation of its intended effect and a defined way to return to the previous working configuration.',
 'Save the prior configuration, change the supplied setting and run the supplied syntax or configuration check before activation.',
 ('Use the service’s supported reload or restart procedure to activate a valid change, then inspect status and the supplied effective-setting check; on failure restore and reactivate the saved configuration.','linux_man_pages#man5/systemd.service.5.html'))
put(78,'aws_ec2_user_guide#ec2-api-permissions.html',
 'For EC2 API operations that support DryRun, the dry-run request checks permissions without executing the operation; DryRunOperation indicates sufficient permission and UnauthorizedOperation indicates insufficient permission.',
 ('Use the supplied fleet wrapper’s preview mode, inspect its proposed targets and actions and compare them with approved scope without enabling mutation.','aws_well_architected_framework#ops04-bp01.html'),
 'Dry-run permission success does not guarantee later operation success or provide a universal preview of every AWS service’s changes.')
put(86,'aws_vpc_user_guide#VPC_Route_Tables.html',
 'The subnet’s route table must contain a matching destination route to a usable target for the required network path.',
 ('Check DNS resolution and the intended endpoint address using the supplied tools, then inspect route association, required protocol/port rules and response traffic to localize the failing layer.','aws_vpc_user_guide#vpc-security-groups.html'),
 ('Network ACLs are stateless, so required requests and responses need permitted traffic in their respective directions.','aws_vpc_user_guide#vpc-network-acls.html'),
 'Make the approved correction supported by the failing layer’s evidence and repeat the endpoint connection test.')
DATA[80][2]=('Before retrying a resource-changing operation, inspect its known outcome and use a supported idempotency token where the supplied operation offers one to avoid duplicate effects.','aws_ec2_user_guide#ec2-api-idempotency.html')
# Paths with more precise documentation sections.
DATA[41][1]=(DATA[41][1][0],'aws_secrets_manager_user_guide#retrieving-secrets-python.html')
DATA[41][2]=(DATA[41][2][0],'aws_secrets_manager_user_guide#best-practices.html')
DATA[109][2]=(DATA[109][2][0],'aws_s3_user_guide#object-lock.html#object-lock-retention-modes')
DATA[127][2]=(DATA[127][2][0],'aws_well_architected_framework#../../../Route53/latest/DeveloperGuide/resource-record-sets-values-basic.html#rrsets-values-basic-ttl')
# Terraform Registry page is script-rendered; cite the provider's linked repository documentation through a section locator.
DATA[29][1]=(DATA[29][1][0],'terraform_aws_provider#website/docs/r/instance.html.markdown')
for i,fs in DATA.items():
 DATA[i]=[(f, r.replace('aws_ec2_user_guide#ec2-api-idempotency.html','aws_ec2_user_guide#../../../ec2/latest/devguide/ec2-api-idempotency.html').replace('aws_wa_devops_guidance#dl.ci.2-integrate-code-changes-frequently.html','aws_wa_devops_guidance#dl.ci.1-integrate-code-changes-regularly-and-frequently.html')) for f,r in fs]
for i,fs in DATA.items():
 DATA[i]=[(f,r.replace('dora_capabilities#guides/dora-metrics/','dora_capabilities#../guides/dora-metrics/').replace('aws_ec2_user_guide#ec2-api-permissions.html','aws_ec2_user_guide#../../../AWSEC2/latest/APIReference/API_StartInstances.html').replace('aws_systems_manager_user_guide#automation-working-executions.html','aws_systems_manager_user_guide#../../../systems-manager/latest/APIReference/API_GetAutomationExecution.html')) for f,r in fs]
DATA[27][0]=(DATA[27][0][0],'aws_iam_user_guide#../../../singlesignon/latest/userguide/permissionsetsconcept.html')
DATA[27][1]=(DATA[27][1][0],'aws_iam_user_guide#../../../singlesignon/latest/userguide/assignusers.html')
DATA[106][2]=(DATA[106][2][0],'aws_systems_manager_user_guide#../../../systems-manager/latest/APIReference/API_StopAutomationExecution.html')
DATA[24][1]=(DATA[24][1][0],'aws_codedeploy_user_guide#deployment-steps.html')
DATA[24][2]=(DATA[24][2][0],'aws_wa_devops_guidance#dl.ads.1-gradually-shift-traffic-for-safer-deployments.html')
