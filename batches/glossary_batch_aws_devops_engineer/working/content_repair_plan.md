# Stage 13 content repair

Affected concept: `aws_devops.perform_an_ec2_blue_green_deployment_with_codedeploy`.

The leakage audit reports one blocking source-support defect, not prerequisite leakage. Assessment and practice anchors require rollback to the original fleet, but the cited CodeDeploy documentation describes rollback as a new deployment of a previous revision and allows termination of original instances. The stage 05 teaching text already correctly requires the known-good revision without promising restoration of the original fleet.

Apply this source-aligned content repair through stage 05/11:
- Rename `assessment_anchors[1].capability` from `verify_rollback_restores_original_fleet_and_known_good_behavior` to `verify_rollback_restores_known_good_revision_and_behavior`.
- Rewrite `practice_anchor.success` to require verification of traffic destination, known-good revision, and application behavior according to the supplied rollback/redeployment procedure; do not require restoration of the original fleet.
- Keep the traffic, revision, and behavior verification requirements intact; do not weaken any evaluator, gate, ledger, or check.

Use the supported stage-repair/invalidation workflow to regenerate affected artifacts and rerun downstream stages and their gates, then rerun the original driver command. A plain rerun currently skips stages 05 and 11 and reproduces the same blocking finding.

Investigation only: no production artifacts or code were changed and no pipeline was rerun; writes are restricted to this working folder.
