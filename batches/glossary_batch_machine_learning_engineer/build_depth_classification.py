import json
import math
import hashlib
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

batch = Path('batches/glossary_batch_machine_learning_engineer')
inputs = ['extracted_concepts.json', 'coverage_briefs.json']
raw = {name: (batch / name).read_bytes() for name in inputs}
extracted = json.loads(raw[inputs[0]])
coverage = json.loads(raw[inputs[1]])
concepts = extracted['concepts']
briefs = {(b['concept_id'], b['path_id']): b for b in coverage['briefs']}
assert len(briefs) == len(coverage['briefs'])
assert {(c['concept_id'], c['path_id']) for c in concepts} == set(briefs)

# Explicitly reviewed assessment interpretations, in the extracted TOC order.
# These distinguish contextual diagnosis/implementation from mere recognition.
applications = '''constructing a task record with prediction-time constraints
validating inputs against a batch/feature contract
choosing numeric representation under precision and memory constraints
implementing vectorized operations while preventing unintended broadcasting
matching ingestion to a concrete format and access pattern
choosing a feasible chunk size under a memory budget
diagnosing constraints from a dataset inspection summary
testing observations against a dataset schema
applying cleaning decisions consistently to observations
comparing sample evidence against a deployment population
checking labels against a prediction task's timing and alignment
selecting a split under time, grouping or sampling constraints
applying training-learned imputation to other data
applying training-fitted scaling to unseen features
handling known and unseen categories consistently
preserving fitted transformations across evaluation and inference
auditing a workflow for concrete leakage defects
deriving prediction-time-safe features
applying a handling policy to sensitive datasets and logs
choosing a metric for stated task consequences
setting measurable acceptance criteria before comparison
constructing and measuring a task-compatible baseline
justifying an approach under quality, latency, cost and operational constraints
fitting an estimator and generating aligned validation predictions
choosing a threshold from validation evidence and task costs
selecting a candidate using fixed criteria and expected-cost calculations
diagnosing recurring failures from residuals or misclassified examples
interpreting subgroup metrics with counts and limitations
choosing a mitigation for a documented subgroup risk
resolving parameters, metrics and artifacts for a specific run
controlling seeds and interpreting remaining reproducibility limits
choosing regularization from observed overfitting evidence
selecting a configuration using budgeted validation-only search
writing limitations and misuse risks grounded in task evidence
judging supplied foundation-model outputs against a matched baseline and fixed criteria
constructing tensors for a supplied model's shape and dtype contract
implementing aligned minibatches with correct boundaries
checking layer and activation outputs against task requirements
verifying loss gradients with respect to trainable parameters
choosing a loss for the actual target and output representation
configuring an optimizer for a supplied objective
executing a correctly ordered parameter update
applying training/evaluation modes to dropout, normalization and inference
reloading compatible weights and reproducing predictions
choosing and preserving a checkpoint using a validation stopping rule
localizing a failing run from loss, gradient and update evidence
repairing device mismatches while avoiding unnecessary transfers
choosing batch size from measured memory limits
diagnosing the source of memory exhaustion from allocation evidence
localizing a bottleneck from profiling evidence
choosing hardware under memory, time and cost constraints
evaluating fine-tuning against a pretrained supervised-task baseline
running a training entry point independently of notebook state
creating an exact training-snapshot reference
producing an environment manifest that round-trips and matches the real environment
reproducing a recorded outcome under stochastic tolerances
resolving and verifying an immutable registry artifact despite mutable-key overwrites
reloading a versioned fitted package and reproducing outputs
reporting a frozen model's protected-test comparison without retuning
executing a managed job with bounded resources and correct artifact references
validating request and response schemas
serving predictions from a frozen fitted package
producing row-aligned batch predictions without refitting
blocking traffic until the fitted package is usable
recreating a deployment while preserving its immutable artifact reference
verifying a release's serving version, predictions and runtime
applying identity-based prediction access controls
computing external availability and reconciling it with handler telemetry
measuring successful throughput under fixed latency and error limits
choosing a batching limit from tail-latency evidence
choosing concurrency that avoids unsafe execution and oversubscription
selecting scaling settings from capacity evidence and service objectives
restoring an approved artifact and verifying the active serving version
proving that a dataset-contract failure blocks downstream training
writing assertions to detect preprocessing or inference regressions
blocking promotion when candidate evidence fails acceptance criteria
specifying correct immutable artifact dependencies between stages
promoting only an approved version through accountable environment gates
recovering a failed pipeline without duplicate side effects or bypassed checks
validating a deployed model's lineage rather than repeating recorded links
producing production-window input and prediction distribution summaries
classifying distribution and quality scenarios from evidence without unsupported conclusions
applying a reference-based input drift detection rule
calculating quality for a correctly joined and mature prediction cohort
choosing an owned actionable alert while avoiding routine-noise paging
choosing repair, rollback or gated retraining from regression evidence
defining a fail-closed authorized retraining policy and pipeline handoff
verifying authorized-trigger execution with the required immutable input
verifying launch idempotency under concurrency and worker restarts
permitting or blocking a retrained candidate against incumbent-relative criteria
executing an authorized recovery action from a runbook
interpreting workload compute/memory telemetry for underuse or saturation
allocating workload spend to the correct reporting window
exercising a cost limit with an authorized response
removing only authorized retired resources while preserving the active release and secrets'''.splitlines()
assert len(applications) == len(concepts) == 95

by_path = defaultdict(list)
for c in concepts:
    by_path[c['path_id']].append(c['dependency_graph_centrality'])
thresholds = {}
for path, values in by_path.items():
    top_n = math.ceil(len(values) / 4)
    cutoff = sorted(values, reverse=True)[top_n - 1]
    thresholds[path] = (len(values), top_n, cutoff, sum(v >= cutoff for v in values))

rows = []
for c, application in zip(concepts, applications):
    evidence = briefs[c['concept_id'], c['path_id']]['evidence']
    centrality = c['dependency_graph_centrality']
    n, top_n, cutoff, tied_n = thresholds[c['path_id']]
    # Zero never becomes a Core signal merely because a sparse path's cutoff is zero.
    top_quarter = centrality > 0 and centrality >= cutoff
    rank = (f"top-quartile signal for {c['path_id']} (top {top_n} of {n}, "
            f"cutoff {cutoff}; boundary ties included, {tied_n} concepts qualify)"
            if top_quarter else
            f"below the top-quartile cutoff {cutoff} for {c['path_id']}")
    if centrality == 0:
        rank += '; zero centrality would favor reference only for recall/lookup'
    reasoning = (
        f"Centrality {centrality}, {rank}; TOC sequence position {c['toc_sequence_position']}. "
        f"Assessment target: \"{c['assessment_target']}\" This requires {application} "
        f"in a concrete task or case, not merely recalling a definition or looking up an option, "
        f"so the application signal independently warrants core. "
        f"Coverage brief: {len(evidence['required_facts'])} required facts and "
        f"{len(evidence['misconceptions'])} misconceptions; fact count is supporting context, "
        f"not a substitute for the assessment/centrality signals."
    )
    if c['concept_id'] == 'mle.experiment_metric_logging':
        # Retrieval alone is not application: the positive centrality signal owns this tier.
        assert top_quarter
        reasoning = (
            f"Centrality {centrality}, {rank}; TOC sequence position {c['toc_sequence_position']}. "
            f"Assessment target: \"{c['assessment_target']}\" This asks for run-scoped retrieval/lookup; "
            f"it does not independently establish application in a new situation. Core is justified "
            f"by top-quartile centrality, not by the retrieval verb. Coverage brief: "
            f"{len(evidence['required_facts'])} required facts and {len(evidence['misconceptions'])} "
            f"misconceptions; these do not override the centrality signal."
        )
    rows.append({'concept_id': c['concept_id'], 'path_id': c['path_id'],
                 'depth_tier': 'core', 'reasoning': reasoning})

metadata = extracted['metadata']
output = {
    'metadata': {
        'artifact_type': 'depth_classification',
        'artifact_version': '1.0.0',
        'schema_version': '1.0.0',
        'batch_id': 'glossary_batch_machine_learning_engineer',
        'run_id': metadata['run_id'],
        'prompt_version': '04_depth_classification@v1',
        'model': 'gpt-6.1-sol',
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'source_snapshot_id': metadata['source_snapshot_id'],
        'parent_artifact_hashes': {
            str(batch / name): hashlib.sha256(raw[name]).hexdigest() for name in inputs
        },
    },
    'batch_id': 'glossary_batch_machine_learning_engineer',
    'classifications': rows,
}
path = batch / 'depth_classification.json'
path.write_text(json.dumps(output, ensure_ascii=False, indent=2) + '\n')

# Stage-specific mistakes checklist: full unique coverage; real numeric signals;
# per-path quartiles with explicit ties; no disposition-based ranking; zero-centrality
# application not confused with recall; required-fact/misconception counts verified;
# only named input hashes; requested metadata and actual UTC clock.
assert len(rows) == len({(r['concept_id'], r['path_id']) for r in rows})
assert {(r['concept_id'], r['path_id']) for r in rows} == set(briefs)
assert all(str(batch / name) in output['metadata']['parent_artifact_hashes'] for name in inputs)
for c, r in zip(concepts, rows):
    assert f"Centrality {c['dependency_graph_centrality']}," in r['reasoning']
    assert c['assessment_target'] in r['reasoning']
    assert 'disposition' not in r['reasoning']
    ev = briefs[c['concept_id'], c['path_id']]['evidence']
    assert f"{len(ev['required_facts'])} required facts" in r['reasoning']
    assert f"{len(ev['misconceptions'])} misconceptions" in r['reasoning']
print('Self-check PASS:', len(rows), 'unique concept/path rows; tiers', dict(Counter(r['depth_tier'] for r in rows)))
print('Quartiles:', thresholds)
print('Generated at:', output['metadata']['generated_at'])
