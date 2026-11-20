# Stage 13 content remediation

Classification: content. The leakage audit reports one real source-support defect for `aws_devops.perform_an_ec2_blue_green_deployment_with_codedeploy`, not prerequisite leakage. Repeated driver restarts skip the passed upstream stages and reproduce the unresolved finding; stage 11's subprocess evaluator passed with zero blocking findings.

The audit quotes the unsupported capability `verify_rollback_restores_original_fleet_and_known_good_behavior`. CodeDeploy rollback redeploys a previous revision as a new deployment; original instances may have been terminated. The supplied bundle does not establish a retained-original-fleet scenario. Stage 05 teaching already correctly requires the known-good revision.

Required content correction in the authoritative anchor input used by stage 11:
- For this concept, change `assessment_anchors[1].capability` to `verify_rollback_restores_known_good_revision_and_behavior`.
- Change `practice_anchor.success` to require verification of traffic destination, known-good revision, and application behavior according to the supplied rollback/redeployment procedure; remove the unconditional original-fleet requirement.
- Keep the existing traffic, revision, behavior and health checks. Do not weaken the evaluator, gates, ledger, or checks.

An authorized operator should apply the anchor correction and use the supported upstream/downstream rerun mechanism to regenerate and evaluate affected artifacts through stage 13, then resume the original command. A plain restart currently skips the stages needing correction.

No source artifacts or code were modified and no pipeline rerun was performed: this investigation is read-only except for working/ notes.
