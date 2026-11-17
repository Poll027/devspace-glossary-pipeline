import concurrent.futures, hashlib, json, pathlib, re, shutil, subprocess, sys
root = pathlib.Path('.')
batch = root / 'batches/glossary_batch_aws_devops_engineer'
context_path = batch / 'batch_run_context.json'
before = context_path.read_bytes()
context = json.loads(before)
workspace = pathlib.Path(context['paths'][0]['toc_workspace'])
seed = json.loads((workspace / 'source_registry_snapshot.json').read_text())['sources']
exclude = {'aws_cert_devops_pro', 'aws_dop_c02_exam_guide', 'roadmap_sh_devops_job_description', 'roadmap_sh_devops'}
educational = {'dora_capabilities', 'twelve_factor_app'}
sources = []
for s in seed:
    if s['source_id'] in exclude:
        continue
    is_edu = s['source_id'] in educational
    sources.append(dict(source_id=s['source_id'], title=s['name'], source_type='educational' if is_edu else 'official_docs', url_or_citation=s['url_or_citation'], trust_tier='explanation_and_sequencing' if is_edu else 'technical_truth'))
for s in sources:
    if s['source_id'] == 'aws_well_architected_framework':
        s['url_or_citation'] = 'https://docs.aws.amazon.com/wellarchitected/latest/framework/framework.html'
    if s['source_id'] == 'git_docs':
        s['url_or_citation'] = 'https://git-scm.com/docs'
additional = [
('aws_ec2_user_guide', 'Amazon EC2 User Guide', 'https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/concepts.html'),
('aws_s3_user_guide', 'Amazon S3 User Guide', 'https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html'),
('aws_cloudtrail_user_guide', 'AWS CloudTrail User Guide', 'https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-user-guide.html'),
('aws_systems_manager_user_guide', 'AWS Systems Manager User Guide', 'https://docs.aws.amazon.com/systems-manager/latest/userguide/what-is-systems-manager.html'),
('aws_ec2_autoscaling_user_guide', 'Amazon EC2 Auto Scaling User Guide', 'https://docs.aws.amazon.com/autoscaling/ec2/userguide/what-is-amazon-ec2-auto-scaling.html'),
('aws_rds_user_guide', 'Amazon RDS User Guide', 'https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Welcome.html'),
('aws_ecr_user_guide', 'Amazon ECR User Guide', 'https://docs.aws.amazon.com/AmazonECR/latest/userguide/what-is-ecr.html'),
('aws_lambda_developer_guide', 'AWS Lambda Developer Guide', 'https://docs.aws.amazon.com/lambda/latest/dg/welcome.html'),
('aws_eventbridge_user_guide', 'Amazon EventBridge User Guide', 'https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-what-is.html'),
('aws_sns_developer_guide', 'Amazon SNS Developer Guide', 'https://docs.aws.amazon.com/sns/latest/dg/welcome.html'),
('aws_secrets_manager_user_guide', 'AWS Secrets Manager User Guide', 'https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html'),
('aws_config_developer_guide', 'AWS Config Developer Guide', 'https://docs.aws.amazon.com/config/latest/developerguide/WhatIsConfig.html'),
('aws_guardduty_user_guide', 'Amazon GuardDuty User Guide', 'https://docs.aws.amazon.com/guardduty/latest/ug/what-is-guardduty.html'),
('aws_security_hub_user_guide', 'AWS Security Hub User Guide', 'https://docs.aws.amazon.com/securityhub/latest/userguide/what-is-securityhub.html'),
('aws_organizations_user_guide', 'AWS Organizations User Guide', 'https://docs.aws.amazon.com/organizations/latest/userguide/orgs_introduction.html'),
('aws_control_tower_user_guide', 'AWS Control Tower User Guide', 'https://docs.aws.amazon.com/controltower/latest/userguide/what-is-control-tower.html'),
('aws_cost_management_user_guide', 'AWS Cost Management User Guide', 'https://docs.aws.amazon.com/cost-management/latest/userguide/what-is-costmanagement.html'),
('terraform_language', 'Terraform language documentation', 'https://developer.hashicorp.com/terraform/language'),
('terraform_aws_provider', 'Terraform AWS provider documentation', 'https://registry.terraform.io/providers/hashicorp/aws/latest/docs'),
('aws_inspector_user_guide', 'Amazon Inspector User Guide', 'https://docs.aws.amazon.com/inspector/latest/user/what-is-inspector.html'),
]
for sid, title, url in additional:
    sources.append(dict(source_id=sid, title=title, source_type='official_docs', url_or_citation=url, trust_tier='technical_truth'))
def check(s):
    p = subprocess.run(['curl', '-sSL', '--retry', '2', '--max-time', '60', '-w', '\n%{http_code}\n%{url_effective}', s['url_or_citation']], capture_output=True, text=True)
    body, status, effective = p.stdout.rsplit('\n', 2)
    title = re.search(r'<title[^>]*>(.*?)</title>', body, re.S | re.I)
    print(s['source_id'], status, effective, 'TITLE:', re.sub(r'\s+', ' ', title.group(1))[:180] if title else '(no title)', flush=True)
    if p.returncode or status != '200' or len(body) < 100:
        raise RuntimeError('URL verification failed: ' + s['url_or_citation'])
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
    list(pool.map(check, sources))
pack_path = root / '00_GLOSSARY_PIPELINE_CORE/source_packs/aws_devops_engineer.source_pack.json'
assert not pack_path.exists(), 'Do not overwrite an existing source pack'
pack_path.write_text(json.dumps({'career_family_id': context['career_family_id'], 'sources': sources}, indent=2) + '\n')
subprocess.run(['python3', '00_GLOSSARY_PIPELINE_CORE/scripts/schema_check.py', 'source_pack.schema.json', str(pack_path)], check=True)
manifest = {'batch_id': context['batch_id'], 'packs': [{'career_family_id': context['career_family_id'], 'file': str(pack_path), 'source_count': len(sources)}]}
(batch / 'source_pack_manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
for live, snapshot, key, schema in [
('registry/concept_evidence_registry.json', 'concept_evidence_registry_snapshot.json', 'entries', 'concept_evidence.schema.json'),
('video_bank/approved_segments.json', 'approved_segments_snapshot.json', 'segments', 'approved_segment.schema.json')]:
    src = root / '00_GLOSSARY_PIPELINE_CORE' / live
    dst = batch / snapshot
    assert not dst.exists(), 'Do not overwrite an existing frozen snapshot'
    shutil.copyfile(src, dst)
    a = hashlib.sha256(src.read_bytes()).hexdigest()
    b = hashlib.sha256(dst.read_bytes()).hexdigest()
    assert a == b
    sys.path.insert(0, str(root / '00_GLOSSARY_PIPELINE_CORE/scripts'))
    from schema_check import validate
    rows = json.loads(dst.read_text())[key]
    for row in rows:
        validate(row, schema)
    print(snapshot, 'rows:', len(rows), 'live SHA256:', a, 'snapshot SHA256:', b)
# The findings name missing sidecars, not any context field: preserve it byte-for-byte.
assert context_path.read_bytes() == before
print('batch_run_context.json unchanged; paths:', len(context['paths']), '; source count:', len(sources))
