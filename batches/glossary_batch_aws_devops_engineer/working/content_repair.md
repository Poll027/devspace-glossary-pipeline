# Stage 13 content repair

Class: content. The audit reports a source-support defect, not prerequisite leakage, for `aws_devops.perform_an_ec2_blue_green_deployment_with_codedeploy`. Rollback redeploys a previous revision as a new deployment; original instances may have been terminated. The current anchors incorrectly require restoration to the original fleet without establishing a retained-original-fleet scenario.

Apply through the stage 11 content repair workflow:
- Change assessment_anchors[1].capability from `verify_rollback_restores_original_fleet_and_known_good_behavior` to `verify_rollback_restores_known_good_revision_and_behavior`.
- Change practice_anchor.success to: "Verify the traffic destination, known-good revision, and application behavior according to the supplied rollback configuration or redeployment procedure."
- Preserve all traffic, revision, behavior, source-support and prerequisite checks. Teaching content already describes the known-good revision correctly; no segment repair is needed.

Re-evaluate repaired stage 11 content and rerun dependent stages including 12 and 13 using the supported stage-repair/restart procedure. A plain rerun currently skips gated upstream stages and repeats the same blocking audit. Do not bypass or manually mark any gate PASS.

Investigation only: this file proposes a content correction; production artifacts and code were not modified and no pipeline rerun was executed.
