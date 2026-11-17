from brief_data import DATA
DATA[24][1]=(DATA[24][1][0],'aws_wa_devops_guidance#dl.ads.3-use-staggered-deployment-and-release-strategies.html')
DATA[24][2]=(DATA[24][2][0],'aws_codedeploy_user_guide#deployment-configurations.html')
DATA[29][0]=('Pin the approved provider version with this declaration, substituting the approved version:\nterraform {\n  required_providers {\n    aws = {\n      source = "hashicorp/aws"\n      version = "= APPROVED_VERSION"\n    }\n  }\n}', 'terraform_language#providers/requirements')
DATA[29][1]=(DATA[29][1][0],'terraform_aws_provider#resources/instance#argument-reference')
DATA[37][2]=('To restore an overwritten object, copy the selected prior version to the same key to create a new current version; to undo a simple deletion, remove its delete marker to expose the preceding version.','aws_s3_user_guide#RestoringPreviousVersions.html')
DATA[85][1]=('For each approved account/Region pair, use a named role profile with role_arn and source_profile, verify its caller with aws sts get-caller-identity --profile NAME, and create the supplied stack with that profile and explicit --region REGION.','aws_cli_user_guide#cli-configure-role.html')
DATA[90][2]=('Use aws lambda publish-version --function-name NAME, then aws lambda update-alias --function-name NAME --name ALIAS --function-version VERSION; invoke NAME:ALIAS through the supplied test and roll back by updating the alias to the approved previous version.','aws_lambda_developer_guide#configuration-aliases.html')
DATA[90].insert(2,('Publish-version snapshots the tested code and configuration as a numbered version; production alias references must identify a published version, not the mutable $LATEST version.','aws_lambda_developer_guide#configuration-versions.html'))
# The inserted publication detail overlaps the core definition; retain the executable publication/alias fact instead.
DATA[90].pop(2)
DATA[92][0]=(DATA[92][0][0],'aws_codedeploy_user_guide#deployment-groups-create-blue-green.html')
DATA[100][1]=('Run the supplied unit and integration test commands in workflow steps with run: TEST_COMMAND; set the promotion job’s needs: [UNIT_JOB, INTEGRATION_JOB] to require both test jobs.','github_actions_docs#reference/workflows-and-actions/workflow-syntax')
DATA[101].insert(1,('In the supplied repository workflow, stage the focused files with git add FILES, commit with git commit -m "MESSAGE", push the review branch with git push, and open its supplied pull-request interface to request review.','git_docs#git-commit'))
DATA[103].insert(2,('An S3 bucket must be empty before deletion; remove the exercise bucket’s objects, all object versions and delete markers before deleting that bucket.','aws_s3_user_guide#delete-bucket.html'))
DATA[108][1]=('Run aws cloudtrail validate-logs --trail-arn ARN --start-time TIME --end-time TIME --region REGION against the supplied log/digest interval and inspect validation failures; for an organization trail also provide the required --account-id.','aws_cloudtrail_user_guide#cloudtrail-log-file-validation-cli.html')
DATA[110][2]=('Configure the already-provisioned backend using line-separated HCL arguments:\nterraform {\n  backend "s3" {\n    bucket = "BUCKET"\n    key = "KEY"\n    region = "REGION"\n  }\n}\nUse the supplied bucket, key, Region and protection settings.','terraform_language#backend/s3')
DATA[116][2]=('In the supplied Lambda validation action, call CodePipeline PutJobSuccessResult with the job ID only after a passing smoke check; call PutJobFailureResult on failure so dependent progression remains blocked.','aws_codepipeline_user_guide#actions-invoke-lambda-function.html')
DATA[122][1]=('Set use_lockfile = true in the supplied S3 backend configuration and use the supplied s3:GetObject, s3:PutObject and s3:DeleteObject permissions on the .tflock object.','terraform_language#backend/s3')
# Split independent CLI/provider commands across the appropriate sources.
EXTRA_REFS={
 (0,1):['aws_cli_user_guide#../../../STS/latest/APIReference/API_GetCallerIdentity.html'],
 (14,1):['aws_cli_user_guide#cli-usage-parameters.html'],
 (29,2):['terraform_language#../cli/commands/init','terraform_language#../cli/commands/plan','terraform_language#../cli/commands/apply'],
 (77,1):['terraform_language#../cli/commands/show'],
 (90,2):['aws_lambda_developer_guide#configuration-versions.html'],
 (101,1):['git_docs#git-add','git_docs#git-push'],
 (121,0):['terraform_language#state/sensitive-data'],
 (122,2):['terraform_language#state/locking'],
 (122,3):['terraform_language#state/locking'],
}
MISCONCEPTIONS={
 28:[('Using a security-group ID as an allowed source does not import the referenced group’s rules into the destination group.','aws_vpc_user_guide#security-group-rules.html#security-group-referencing')],
 76:[('Changing bucket default encryption does not re-encrypt objects that already exist; their individual encryption settings still matter.','aws_s3_user_guide#bucket-encryption.html')],
 83:[('Environment variables populated from a ConfigMap do not automatically update inside already-running containers when the ConfigMap changes.','kubernetes_overview#../../tasks/configure-pod-container/configure-pod-configmap/#mounted-configmaps-are-updated-automatically')],
 122:[('Force-unlock is not a safe way to bypass another active state writer; it is reserved for a lock from a failed operation when automatic unlocking failed.','terraform_language#state/locking')],
 123:[('Receiving an approval notification does not itself grant permission to approve the action; approval requires the appropriate authorization.','aws_codepipeline_user_guide#approvals.html')]
}
DATA[24]=[(f,'aws_well_architected_framework#ops04-bp01.html') for f,r in DATA[24]]
DATA[2][1]=(DATA[2][1][0],'aws_eks_user_guide#security.html')
DATA[15][2]=(DATA[15][2][0],'aws_well_architected_framework#ops03-bp02.html')
DATA[5].append(('Interpret the supplied EC2 OS-update report as customer guest-OS work and the supplied RDS parameter-check report as customer-controlled database configuration; RDS parameter groups contain database engine configuration values.','aws_rds_user_guide#USER_WorkingWithParamGroups.html'))
DATA[67][1]=('Set botocore.config.Config(retries={"mode": "standard", "total_max_attempts": APPROVED_ATTEMPTS}) on the supplied Boto3 client to bound requests with the SDK’s backoff; do not wrap terminal errors in an unbounded retry loop.','boto3_guide#retries.html')
DATA[67][2]=('Catch botocore.exceptions.ClientError around the supplied call, inspect its response["Error"]["Code"] and response["Error"]["Message"] and preserve response["ResponseMetadata"]["RequestId"] when present; report the terminal failure or exhausted retry outcome.','boto3_guide#error-handling.html')
