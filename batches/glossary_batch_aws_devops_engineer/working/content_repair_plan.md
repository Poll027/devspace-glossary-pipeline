# Stage 13 content repair

Affected concept: `aws_devops.perform_an_ec2_blue_green_deployment_with_codedeploy`.

The leakage audit reports a source-support defect, not prerequisite leakage. Assessment and practice anchors require restoration to the original EC2 fleet, although the supplied sources allow termination of original instances and describe rollback as a new deployment of a previous revision. No retained-original-fleet scenario is supplied.

Repair through stage 05/11:
- Rename `assessment_anchors[1].capability` from `verify_rollback_restores_original_fleet_and_known_good_behavior` to `verify_rollback_restores_known_good_revision_and_behavior`.
- Rewrite `practice_anchor.success` to require verified traffic destination, known-good revision, and application behavior according to the supplied rollback/redeployment procedure; do not require the original fleet.
- Preserve all source-support, safety, evaluation and ledger checks. Keep the teaching content's known-good-revision requirement.

Use the pipeline's supported upstream repair/invalidation process to regenerate and re-evaluate the affected stages and downstream artifacts, then rerun the same driver command. Plain reruns currently skip stages 05 and 11 and repeat the stage 13 stop.

Investigation only: no pipeline artifacts or code were changed, and no rerun was performed.
