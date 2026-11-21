import json
from pathlib import Path
p = Path('batches/glossary_batch_aws_devops_engineer/glossary_pass_a.part.all.json')
d = json.loads(p.read_text())
before = json.loads(p.read_text())
rows = {r['concept_id']: r for r in d['entries']}
def blocks(cid):
    return {b['id']: b for b in rows[cid]['teaching_blocks']}
cid = 'aws_devops.allocate_vpc_and_subnet_cidrs'
b = blocks(cid)
b['tb3']['content'] = ('IPv4 subnet sizes range from /16 to /28. For ordinary AWS-provided IPv4 subnet ranges, AWS reserves the first four addresses and the last address. With BYOIP, you can use all addresses in the brought IPv4 range, including the network and broadcast addresses.\n\nChoose subnet ranges inside the VPC that do not intersect. When checking usable capacity for ordinary AWS-provided IPv4 ranges, allow for the five reserved addresses; do not apply that subtraction to a BYOIP range.\n\nEach subnet resides entirely in one Availability Zone; create separate subnets for workloads in different Availability Zones.')
b['tb4']['content'] = b['tb4']['content'].replace('Take a supplied VPC range of 10.20.0.0/16.', 'For an ordinary AWS-provided IPv4 range, take a supplied VPC CIDR of 10.20.0.0/16.')
b['tb5']['content'] = b['tb5']['content'].replace('Nor does an address count before reservations establish usable capacity.', 'For ordinary AWS-provided IPv4 ranges, an address count before the five reservations does not establish usable capacity. BYOIP permits use of all addresses in the brought range, including network and broadcast addresses.')
cid = 'aws_devops.configure_cloudwatch_alarm_evaluation_and_missing_data_behavior_from_supplied_signals_and_thresholds'
b = blocks(cid)
b['tb3']['content'] += ('\n\nBefore applying a missing-data setting, establish what CloudWatch retrieved. With the default sliding evaluation window, CloudWatch attempts to retrieve more datapoints than EvaluationPeriods. This evaluation range depends on the period and metric resolution. A wall clock evaluation window instead retrieves only the datapoints within its aligned window.\n\nIf the evaluation range contains at least EvaluationPeriods real datapoints, CloudWatch evaluates the most recent EvaluationPeriods real points, using older real points as needed. It ignores the missing-data setting in this case. If fewer real points are retrieved, CloudWatch includes all of them and fills only as many missing points as necessary using the configured treatment.')
b['tb3']['fact_ids'] += ['f5', 'f6', 'f7']
b['tb4']['content'] = b['tb4']['content'].replace('Do not silently treat a gap as a real zero or a real breach: use breaching, notBreaching, ignore or missing as configured.', 'First check the retrieved evaluation range: if it supplies at least three real points, evaluate the most recent three real points and ignore the missing-data setting. Only when too few real points are retrieved should the configured treatment fill the minimum necessary gaps. Do not silently treat a gap as a real zero or a real breach.')
b['tb4']['fact_ids'] += ['f6', 'f7']
rows[cid]['teaching_blocks'].append({'id': 'tb6', 'purpose': 'example', 'title': 'An older breach amid missing points', 'content': 'Partially missing data has an important exception: CloudWatch can enter ALARM even with fewer real datapoints than DatapointsToAlarm if the oldest breaching datapoint in the evaluation range is at least as old as DatapointsToAlarm and every more recent datapoint is breaching or missing. In the source’s three-out-of-three example, EvaluationPeriods and DatapointsToAlarm are both 3, the treatment is missing, and the evaluation range has five points. Read these sequences from oldest to newest: “missing, missing, missing, missing, breach” does not immediately cause ALARM, but “missing, missing, breach, missing, missing” does. The second sequence has an older breach followed only by missing points; the first has only a new breach. Do not infer the state solely by counting the available real breaches.', 'fact_ids': ['f2', 'f8']})
cid = 'aws_devops.protect_recoverable_s3_objects_with_versioning_and_lifecycle_controls'
b = blocks(cid)
b['tb3']['content'] = ('In the S3 console, open the bucket’s Properties > Bucket Versioning > Edit > Enable > Save changes. Check the Bucket Versioning setting to verify it is enabled. Apply the supplied lifecycle JSON with the following command, substituting the approved bucket and policy file:\n\naws s3api put-bucket-lifecycle-configuration --bucket <bucket> --lifecycle-configuration file://<policy.json>\n\nThen retrieve the configuration to verify the configured rules:\n\naws s3api get-bucket-lifecycle-configuration --bucket <bucket>\n\n' + b['tb3']['content'])
b['tb3']['fact_ids'].append('f5')
remove = ['aws_devops.configure_security_groups', 'security.audit_storage_encryption', 'aws_devops.apply_bounded_eks_workload_configuration_and_secrets', 'terraform.state_locking', 'aws_devops.control_environment_promotion_with_a_manual_approval']
for cid in remove:
    assert blocks(cid)['tb6']['purpose'] == 'misconception'
    rows[cid]['teaching_blocks'] = [b for b in rows[cid]['teaching_blocks'] if b['id'] != 'tb6']
b = blocks('aws_devops.apply_bounded_eks_workload_configuration_and_secrets')
b['tb5']['content'] = b['tb5']['content'].replace(' Also, ConfigMap-backed environment variables do not automatically update inside already-running containers after the ConfigMap changes.', '')
b['tb5']['fact_ids'].remove('m1')
b = blocks('aws_devops.control_environment_promotion_with_a_manual_approval')
b['tb5']['content'] = b['tb5']['content'].replace('A notification is not approval authority, and approval of one revision is not the recorded approval of another.', 'Approval of one revision is not the recorded approval of another.')
b['tb5']['fact_ids'].remove('m1')
changed = [r['concept_id'] for old, r in zip(before['entries'], d['entries']) if old != r]
assert set(changed) == set(remove + ['aws_devops.allocate_vpc_and_subnet_cidrs', 'aws_devops.configure_cloudwatch_alarm_evaluation_and_missing_data_behavior_from_supplied_signals_and_thresholds', 'aws_devops.protect_recoverable_s3_objects_with_versioning_and_lifecycle_controls'])
assert before['metadata'] == d['metadata'] and before['batch_id'] == d['batch_id']
for old, new in zip(before['entries'], d['entries']):
    assert {k:v for k,v in old.items() if k != 'teaching_blocks'} == {k:v for k,v in new.items() if k != 'teaching_blocks'}
p.write_text(json.dumps(d, indent=2, ensure_ascii=False) + '\n')
print('Entries:', len(d['entries']), 'Teaching blocks:', sum(len(r['teaching_blocks']) for r in d['entries']), 'Changed entries:', len(changed))
