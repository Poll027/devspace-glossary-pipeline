exec((P/'working/completeness.py').read_text())
exec((P/'working/completeness_late.py').read_text())
# Final source/scope corrections.
E[11][1]=(R['split'],'Keep observations from a common evaluation group entirely on one side of the boundary, and keep time-ordered training observations earlier than the intended later evaluation observations.')
E[81][1]=('google_ml_crash_course#production-ml-systems/static-vs-dynamic-training — Table 1: Primary advantages and disadvantages','A changing relationship between features and labels can invalidate a previously useful model even when monitoring only input marginals does not reveal that relationship change.')
E[81][-1]=('google_ml_crash_course#production-ml-systems/static-vs-dynamic-training — Table 1; scikit_learn_user_guide#modules/model_evaluation.html — Classification metrics','Input marginals describe P(X), conditional-target evidence describes P(Y|X), and matched-label errors describe observed quality; changing one does not logically establish changes in all three.')
for i in [52,55]:
 E[i]=[(R['shell'] if ('Redirect shell output' in t or 'output redirection' in t) else ref,t) for ref,t in E[i]]
add(61,('http','For the bounded fixture, construct HTTPServer((host, port), Handler) with the declared handler and serve_forever(), using the configured host/port and the existing runtime rather than creating a new platform.'))
# Short learning objectives: one outcome, written freshly for each placement.
objectives='''Define an unambiguous prediction record with its unit, target, decision time, horizon and permitted inputs.
Accept or reject a numerical input against a declared rank and batch/feature-axis contract.
Choose a numerical representation by checking its value preservation and element-memory cost.
Implement shape-correct array arithmetic and verify agreement with a bounded reference.
Retrieve and inspect an authorized dataset using the declared format and column types.
Process a dataset stream in chunks whose numerical allocations fit the declared memory bound.
Produce a reproducible dataset-readiness summary of structure, types, memory and feature statistics.
Implement and test a dataset column, type and value contract.
Apply an explicit retain, repair or reject policy to repeated and invalid observations.
Diagnose sample coverage using empirical inclusion proportions and numeric summaries.
Verify keyed label correspondence and the declared label-availability boundaries.
Implement a split that matches the evaluation scenario’s group and time dependencies.
Learn missing-value replacements on training rows and prove validation reuses that state.
Learn feature scaling from training data and check unchanged validation transformation parameters.
Freeze a categorical representation and test its known, unseen and missing-value behavior.
Assemble one fitted feature/model pipeline and verify its reuse for held-out inference.
Find and repair one evaluation-information leak without changing the evaluation boundary.
Compute a prediction-time feature using only records available at that time.
Enforce an existing permitted-field and credential-exposure policy in diagnostic records.
Choose an evaluation measure whose conditioning population and error consequences match the task.
Precommit measurable cost, predictive and operating limits for accepting a model.
Train and freeze a simple reference, then evaluate its declared validation quantities.
Select a supplied modeling approach from matched quality, operating and ownership evidence.
Fit a bounded classical estimator and compare its validation predictions with the fixed reference.
Select and freeze a classification cutoff under precommitted validation cost constraints.
Rank eligible candidate records using a common expected-cost and operating-limit rule.
Explain a localized model failure with conditional error and feature-summary evidence.
Compare predefined validation slices without hiding their counts or representativeness limits.
Choose a supported subgroup mitigation using population-weighted harm and validation evidence.
Create and verify a keyed run record linking parameters, metrics, artifacts and actual code revision.
Assess paired-run variability with numeric summaries and an empirical candidate-win proportion.
Select a regularization setting from matched train/validation gaps and expected-cost evidence.
Execute a budgeted validation search with resolved defaults and protected-test isolation.
Write a model risk record that preserves the existing access policy and supported limitations.
Compare supplied pretrained task outputs with the fixed baseline under declared acceptance rules.
Convert aligned feature/target arrays into tensors with explicitly checked shape and dtype.
Implement a dataset/loader that preserves sample identity and minibatch alignment.
Build a minimal module whose layer widths, nonlinearity and output shape satisfy the task.
Verify parameter gradients against the corresponding matrix-shaped derivative reference.
Choose a task-compatible loss and verify its output, target and gradient contracts.
Implement and test one plain-SGD update from the current gradients.
Execute a parameterized minibatch training loop and verify its gradient/update wiring.
Separate training behavior from forward-only validation behavior in a tested loop.
Save and reload model state through file handles and verify state and prediction agreement.
Implement a validation-patience controller that returns the best retained model state.
Localize and correct one evidence-supported neural training failure.
Verify consistent tensor/model placement on an authorized instance and restore its stopped state.
Choose a minibatch size using matrix-memory estimates, observed peak memory and completed-work evidence.
Diagnose a reproduced out-of-memory failure from simultaneous allocations and runtime measurements.
Profile a bounded training workload and verify one bottleneck-oriented improvement.
Choose between authorized CPU/GPU instances using matched runtime, memory and billing evidence.
Adapt a pretrained supervised task head and verify its contract, learning signal and validation result.
Replace notebook-global execution with a committed, parameterized script whose clean-shell output is verified.
Create and re-retrieve a hashed immutable dataset version despite an overwrite of latest.
Serialize and verify the actual revision, dependency pins and runtime identity in one manifest.
Re-execute a recorded experiment in a clean process using its recorded source, inputs and environment.
Register and verify an artifact’s immutable object version, hash and originating run.
Package fitted preprocessing and model state with dependencies and verify container-reloaded predictions.
Evaluate the frozen selected candidate on protected test observations without retuning.
Invoke a bounded managed job from parsed settings and verify its consumed inputs, output and terminal state.
Implement and test structured request/response checks for prediction inputs and outputs.
Serve bounded predictions through the fitted inference path and a validated JSON contract.
Write keyed batch predictions with bounded reading and explicit file operations.
Make readiness accurately reflect initialized model/preprocessor state and verify it over HTTP.
Version, apply and recreate an existing deployment from parsed runtime configuration.
Verify a referenced serving artifact through real runtime inspection and prediction fixtures.
Adapt and test the existing service’s runtime-injected authorization configuration.
Instrument handler behavior and report a reconciled external client-availability probe.
Measure the highest feasible stable-throughput load point under fixed error and tail-latency constraints.
Select a batching limit from matched end-to-end latency traces.
Apply and verify a configured worker bound under supplied request load.
Verify a bounded replica policy from demand evidence and restore the original runtime settings.
Restore the previous approved serving artifact and retire the faulty release only after verification.
Wire a fail-closed data-quality function into an existing commit-triggered pipeline.
Connect behavior assertions to a pipeline gate that blocks dependent stages on failure.
Implement a fail-closed, event-triggered candidate release gate from fixed validation and operating evidence.
Encode and verify immutable artifact dependencies between pipeline stages.
Gate an existing staging-to-production handoff on artifact-specific approval, quality and protected identity.
Recover an injected stage failure through verified artifact boundaries without bypassing gates.
Audit the served artifact’s registry, run, input, revision and configuration lineage.
Summarize aligned reference and production input/output distributions over a defined window.
Distinguish input shift, changed target relationship and label-supported quality degradation.
Detect a defined feature-distribution difference using aligned proportions and numeric summaries.
Evaluate a matured, keyed prediction cohort with explicit label-coverage limits.
Configure and replay an actionable alert against baseline variability and a known breach.
Reproduce and triage a model-service regression using a tested, evidence-supported hypothesis.
Trace authorized investigated retraining triggers through existing gates and separate promotion authority.
Invoke authorized retraining on a verified immutable input and inspect its actual consumption.
Use the supplied durable admission and executor contracts to prevent duplicate or overlapping logical runs.
Test whether a retrained candidate may proceed under unchanged validation and promotion criteria.
Recover an injected nonproduction service fault through the authorized runbook and instance lifecycle.
Summarize CPU/memory utilization for the correctly matched instance, process and workload window.
Attribute direct and shared workload charges to verified lifecycle intervals and reconcile totals.
Test an existing workload budget notification and authorized safe-stop response, documenting residual exposure.
Remove only verified exclusively retired resources while preserving active service, artifacts and secret-safe records.'''.splitlines()
assert len(objectives)==len(cs)==95
# Scope pruning: remove generic comparison conditions not consumed by a placement.
# A declared tail percentile need not always be both 95 and 99.
for i in [68,71]:
 E[i]=[(ref, 'Compute the declared tail-latency percentile with np.percentile(completed_latency_values, declared_percentile), retaining its convention, sample count and time unit.' if ref==R['percentile'] else text) for ref,text in E[i]]
# Config authoring/inspection uses a verified safe YAML parser.
for i in [64,66,70,71,73,74,75,76,77,78,84,87,88,93]:
 add(i,('python_tutorial#https://pyyaml.org/wiki/PyYAMLDocumentation — Reference: safe_load; safe_dump','With the declared PyYAML dependency, import yaml; write a mapping/list configuration with yaml.safe_dump(config, file_handle), reload it with yaml.safe_load(file_handle), and inspect the required resolved fields before submitting it to the existing runtime. Safe loading accepts standard YAML tags, not arbitrary Python object constructors.'))
add(56,('registryworkflow','Import the registry dependency with from mlflow import MlflowClient, construct MlflowClient(), and use the resulting client for create_model_version, get_model_version and set_model_version_tag.'))
add(54,('python_tutorial#../library/sys.html — sys.version; sys.executable','Use import sys to record sys.version and sys.executable as actual Python runtime details alongside the supplied runtime identity.'))
E[64]=[(ref+"; git-merge — DESCRIPTION" if "merge the branch" in text else ref,text) for ref,text in E[64]]
# Remove redundant ownership explanation and preserve rollback readiness ordering.
E[22]=[x for x in E[22] if not x[1].startswith('Custom classical and custom neural approaches')]
E[51]=[(ref,text.replace('For a supervised vision example,','For a supervised image-classification task,')) for ref,text in E[51]]
E[72]=[(ref,'Use the recorded previous immutable image reference for the approved replacement container.' if ref==R['digest'] else text) for ref,text in E[72] if ref!=R['config']]
for i in E:
 E[i]=[(ref,text.replace('np.mean(values','np.mean(numeric_values').replace('np.std(values','np.std(numeric_values').replace('each feature column is summarized over rows','each selected numeric feature column is summarized over rows').replace('over the selected observations','over the selected numeric observations')) for ref,text in E[i]]
# No invented facts, empty reuse, or unsupported source identifiers.
manifest=json.loads((P/'source_pack_manifest.json').read_text())
source_paths=[pack['file'] for pack in manifest['packs']]
source_ids={s['source_id'] for path in source_paths for s in json.loads(Path(path).read_text())['sources']}
placements=[]
for i,c in enumerate(cs):
 key=(c['concept_id'],c['path_id']); l=lookup[key]
 assert l['canonical_status']=='new' and c['concept_id'] not in registry
 facts=[]; seen=set()
 for ref,text in E[i]:
  assert ref.split('#',1)[0] in source_ids, (i,ref)
  assert '#' in ref and text.strip()
  if text not in seen:
   facts.append({'statement':text,'source_ref':ref});seen.add(text)
 facts=[{'id':f'f{j+1}','statement':f['statement'],'source_refs':re.split(r'; (?=[A-Za-z_]+#)',f['source_ref'])} for j,f in enumerate(facts)]
 evidence={'concept_id':c['concept_id'],'required_facts':facts,'optional_enrichment':[],'misconceptions':[],'created_in_batch_id':B,'used_by_path_ids':[c['path_id']]}
 placements.append({'concept_id':c['concept_id'],'path_id':c['path_id'],'learning_objective':objectives[i],'canonical_status':l['canonical_status'],'evidence':evidence})
now=datetime.now(timezone.utc)
inputs=[P/'extracted_concepts.json',P/'registry_lookup.json',P/'concept_evidence_registry_snapshot.json',P/'source_pack_manifest.json']+[Path(p) for p in source_paths]
parents={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs}
metadata={'artifact_version':'1.0.0','schema_version':'1.0.0','artifact_type':'coverage_briefs','batch_id':B,'generated_at':now.isoformat().replace('+00:00','Z'),'model':'none','prompt_version':'03_coverage_brief@v1','source_snapshot_id':json.loads((P/'extracted_concepts.json').read_text())['metadata']['source_snapshot_id'],'parent_artifact_hashes':parents,'run_id':B+'.03_coverage_brief.all.'+now.strftime('%Y%m%dT%H%M%SZ')}
output={'metadata':metadata,'batch_id':B,'briefs':placements}
(P/'coverage_briefs.part.all.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
print('placements',len(placements),'required_facts',sum(len(p['evidence']['required_facts']) for p in placements),'optional_facts',0,'misconceptions',0)
