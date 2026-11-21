import json
from pathlib import Path
p = Path('batches/glossary_batch_aws_devops_engineer/coverage_briefs.part.all.json')
data = json.loads(p.read_text())
before = json.loads(p.read_text())
rows = {r['concept_id']: r['evidence'] for r in data['briefs']}
def evidence(s): return rows['aws_devops.' + s]
e = evidence('allocate_vpc_and_subnet_cidrs')
e['required_facts'][1]['statement'] = 'IPv4 subnet sizes range from /16 to /28; for ordinary AWS-provided IPv4 subnet ranges, AWS reserves the first four addresses and the last address, but with BYOIP you can use all addresses in the brought IPv4 range, including the network and broadcast addresses.'
e['required_facts'][2]['statement'] = 'Choose subnet ranges inside the VPC that do not intersect, and allow for the five reserved addresses in ordinary AWS-provided IPv4 subnet ranges when checking usable capacity.'
e = evidence('centralize_structured_application_logs_in_cloudwatch_logs')
e['required_facts'][1]['source_refs'] = ['aws_cloudwatch_user_guide#CloudWatch-Agent-Configuration-File-Details.html', 'aws_cloudwatch_user_guide#../logs/Working-with-log-groups-and-streams.html']
e['required_facts'][2]['statement'] = 'Check that collected JSON log events preserve the application’s structured event fields.'
e = evidence('configure_cloudwatch_alarm_evaluation_and_missing_data_behavior_from_supplied_signals_and_thresholds')
ref = ['aws_cloudwatch_user_guide#alarms-and-missing-data.html']
additions = [
 'For the default sliding evaluation window, CloudWatch attempts to retrieve more datapoints than EvaluationPeriods; this evaluation range depends on the period and metric resolution, while a wall clock evaluation window retrieves only the datapoints in its aligned window.',
 'If the evaluation range contains at least EvaluationPeriods real datapoints, CloudWatch evaluates the most recent EvaluationPeriods real datapoints, using older real datapoints as needed and ignoring the missing-data setting.',
 'If fewer than EvaluationPeriods real datapoints are retrieved, CloudWatch includes all retrieved real datapoints and uses the configured missing-data treatment to fill only as many missing datapoints as necessary.',
 'With partially missing data, CloudWatch can enter ALARM even when fewer than DatapointsToAlarm real datapoints are available if the oldest breaching datapoint in the evaluation range is at least as old as DatapointsToAlarm and every more recent datapoint is breaching or missing; for the source’s three-out-of-three example with missing treatment and a five-point evaluation range, four missing points followed by a new breach do not immediately cause ALARM, whereas two missing points, a breach, and two more missing points do.'
]
for i, statement in enumerate(additions, 5):
 e['required_facts'].append({'id': f'f{i}', 'statement': statement, 'source_refs': ref.copy()})
e = evidence('protect_recoverable_s3_objects_with_versioning_and_lifecycle_controls')
e['required_facts'].append({'id': 'f5', 'statement': 'Enable versioning in the S3 console under the bucket’s Properties > Bucket Versioning > Edit > Enable > Save changes, and check its Bucket Versioning setting; apply the supplied lifecycle JSON with aws s3api put-bucket-lifecycle-configuration --bucket <bucket> --lifecycle-configuration file://<policy.json>, then retrieve it with aws s3api get-bucket-lifecycle-configuration --bucket <bucket> to verify the configured rules.', 'source_refs': ['aws_s3_user_guide#manage-versioning-examples.html', 'aws_s3_user_guide#how-to-set-lifecycle-configuration-intro.html']})
e = evidence('gate_infrastructure_changes_with_configuration_validation')
f = e['required_facts'].pop(3)
f['statement'] = 'As optional supporting practice, terraform fmt -check checks canonical formatting and can be used as an additional blocking configuration check.'
e['optional_enrichment'].append(f)
changed = [a['concept_id'] for a,b in zip(data['briefs'],before['briefs']) if a != b]
assert len(changed) == 5, changed
p.write_text(json.dumps(data, indent=2) + '\n')
print('Brief rows:', len(data['briefs']))
print('Required fact rows:', sum(len(r['evidence']['required_facts']) for r in data['briefs']))
print('Optional fact rows:', sum(len(r['evidence']['optional_enrichment']) for r in data['briefs']))
print('Changed brief rows:', len(changed))
