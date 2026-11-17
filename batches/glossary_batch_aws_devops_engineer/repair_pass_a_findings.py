import json
from pathlib import Path
p = Path('batches/glossary_batch_aws_devops_engineer/glossary_pass_a.part.all.json')
text = p.read_text()
expected = json.loads(text)
entries = {r['concept_id']: r for r in expected['entries']}
changes = []
def patch(cid, bid, old, new):
    block = next(b for b in entries[cid]['teaching_blocks'] if b['id'] == bid)
    before = block['content']
    assert old in before, (cid, bid)
    after = before.replace(old, new)
    changes.append((before, after))
    block['content'] = after

patch('aws.cloudformation_change_sets', 'tb4',
      'Inspect additions, modifications, removals and any replacement indicators against the approved scope. For an illustrative review, suppose the preview contains the expected EC2 addition but also a removal the task does not authorize.',
      'Inspect the proposed additions against the approved scope. For an illustrative new-stack review, suppose the preview contains the expected EC2 addition but also an extra addition the task does not authorize.')
patch('aws.ec2_instance_profile', 'tb3',
      'Attach or replace the approved instance profile on the EC2 instance using the instance’s IAM-role setting or associate-iam-instance-profile.',
      'Use associate-iam-instance-profile to attach the approved instance profile to an EC2 instance without an existing association. To replace an existing profile, use the console’s Modify IAM role workflow instead.')
patch('aws.ec2_instance_profile', 'tb4',
      "Use the instance's IAM-role setting or the supplied associate-iam-instance-profile operation to attach or replace the approved profile.",
      'For attachment to an instance without an existing association, use the supplied associate-iam-instance-profile operation. For replacement of an existing profile, use the console’s Modify IAM role workflow to select the approved role.')
patch('aws_devops.reconcile_terraform_ec2_drift', 'tb3',
      'A refresh-only plan updates state and outputs to reflect remote changes; it does not itself change remote infrastructure to restore configuration.',
      'A refresh-only plan proposes state and output updates to reflect remote changes; planning alone does not persist them. Applying the approved refresh-only plan persists those updates without changing remote infrastructure to restore configuration.')
patch('aws_devops.reconcile_terraform_ec2_drift', 'tb4',
      'A refresh-only plan updates state and outputs to reflect remote changes; it does not itself restore remote infrastructure to the configuration.',
      'A refresh-only plan proposes state and output updates to reflect remote changes. Applying the approved refresh-only plan persists them without changing remote infrastructure; planning alone does not persist them or restore remote infrastructure to the configuration.')
patch('aws_devops.reconcile_terraform_ec2_drift', 'tb5',
      'Refresh-only is not remote repair. It updates state and outputs to reflect remote changes.',
      'Refresh-only is not remote repair. Refresh-only planning proposes state and output updates to reflect remote changes; applying the approved refresh-only plan persists them without changing remote infrastructure.')
patch('aws.operator_profiles', 'tb4',
      "Replace NAME with lab-operator in the identity command. Read both the caller ARN and account ID in the result and compare them with the supplied operator context. Then use the configuration-list command with that same profile. Read the effective Region and the origin of the values rather than inferring them from the profile's label.",
      "Run aws sts get-caller-identity --profile lab-operator. Suppose the illustrative result shows Account: [REDACTED_ACCOUNT] and Arn: arn:aws:iam::[REDACTED_ACCOUNT]:user/[REDACTED_OPERATOR]. Compare both values with the supplied operator context: this checks the caller identity and account. Then run aws configure list --profile lab-operator. Suppose its illustrative Region row shows Value: us-west-2, Type: config-file, Location: ~/.aws/config. This checks the effective Region and its configuration origin rather than inferring them from the profile's label.")
patch('aws_devops.verify_availability_across_availability_zones_under_a_controlled_failure', 'tb4',
      'the failure criterion has not been met.', 'the availability criterion has not been met.')
for before, after in changes:
    old_literal = json.dumps(before, ensure_ascii=False)
    new_literal = json.dumps(after, ensure_ascii=False)
    if old_literal not in text:
        old_literal = json.dumps(before, ensure_ascii=True)
        new_literal = json.dumps(after, ensure_ascii=True)
    assert text.count(old_literal) == 1
    text = text.replace(old_literal, new_literal, 1)
assert json.loads(text) == expected
p.write_text(text)
print(f'Patched {len(changes)} teaching blocks; {len(expected["entries"])} entries; {sum(len(r["teaching_blocks"]) for r in expected["entries"])} teaching blocks.')
