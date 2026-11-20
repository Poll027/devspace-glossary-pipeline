# Stage 13 content repair

Blocking bundle: `aws_devops.perform_an_ec2_blue_green_deployment_with_codedeploy`.

The audit reports a source-support defect, not prerequisite leakage: assessment and practice anchors require rollback to the original fleet, but the cited CodeDeploy sources describe redeployment of a previous revision as a new deployment and permit termination of original instances. Teaching blocks already correctly require the known-good revision.

Required upstream content repair in stage 05/11:
- Change `assessment_anchors[1].capability` from `verify_rollback_restores_original_fleet_and_known_good_behavior` to `verify_rollback_restores_known_good_revision_and_behavior`.
- Change `practice_anchor.success` to require verified traffic destination, known-good revision, and application behavior according to the supplied rollback/redeployment procedure, not return to the original fleet.
- Preserve all other health, lifecycle, traffic and behavior checks and source-support requirements.

Use the pipeline's supported upstream repair/re-gating procedure so stages 05/11 and affected downstream artifacts are regenerated and re-evaluated; then rerun the original command. Plain reruns currently skip the passed upstream stages and repeat the same stage-13 blocker. Do not bypass or weaken stage 13 or manually falsify the ledger. No code or production artifacts were changed during triage.
