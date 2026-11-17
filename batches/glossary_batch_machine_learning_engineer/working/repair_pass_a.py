import json
from pathlib import Path

path = Path('batches/glossary_batch_machine_learning_engineer/glossary_pass_a.part.all.json')
data = json.loads(path.read_text())
entries = {r['concept_id']: r for r in data['entries'] if r['path_id'] == 'machine_learning_engineer'}
def block(concept, block_id):
    return next(b for b in entries[concept]['teaching_blocks'] if b['id'] == block_id)

b = block('mle.training_fitted_imputation', 'tb3')
b['content'] = 'Calculate each feature’s training mean and spread using only its observed, nonmissing training values. For arrays without missing values, np.mean(observed_training_values, axis=0) summarizes each column over rows, and np.std(observed_training_values, axis=0, ddof=0) divides squared deviations by N before taking the square root; use ddof=1 only when the stated calculation requires the N−1 divisor. When missing entries are NaN, use np.nanmean(X_train, axis=0) and np.nanstd(X_train, axis=0, ddof=0): these ignore NaNs within each feature. Ordinary np.mean/np.std on NaN-containing columns do not provide those observed-only summaries. With strategy="mean", compare the feature means against the fitted imputer statistics_. Write assert predicate checks for the declared valid, boundary and failure cases; a false predicate raises AssertionError during ordinary non-optimized execution.'
b['fact_ids'] = ['f3', 'f4', 'f5', 'f6', 'f7']
b = block('mle.training_fitted_imputation', 'tb4')
b['content'] = '''Use an illustrative training fixture with two numerical features, distance and duration:

```python
import numpy as np
from sklearn.impute import SimpleImputer

X_train = np.array([[2, 10], [6, np.nan], [np.nan, 14]])
X_validation = np.array([[100, 20], [np.nan, np.nan]])
means = np.nanmean(X_train, axis=0)
spread = np.nanstd(X_train, axis=0, ddof=0)
imputer = SimpleImputer(strategy="mean").fit(X_train)
before = imputer.statistics_.copy()
transformed = imputer.transform(X_validation)
assert np.allclose(means, imputer.statistics_)
assert np.allclose(spread, [2, 2])
assert np.allclose(imputer.statistics_, before)
assert np.allclose(transformed, [[100, 20], [4, 12]])
```

Distance is summarized from 2 and 6; duration from 10 and 14. The observed-only means are [4, 12] and the ddof=0 spreads are [2, 2]. Both columns contain a NaN, so ordinary np.mean(X_train, axis=0) and np.std(X_train, axis=0, ddof=0) instead return [nan, nan]. The NaN-aware means agree with statistics_, demonstrating that mean imputation learned the replacements from the same observed training values.

Validation retains its complete row [100, 20] and replaces its missing row with [4, 12]. Neither 100 nor 20 contributes to the training summaries. Checking both transformed output and unchanged statistics_ verifies replacement and reuse of fitted state. Keep the declared boundary and failure checks alongside this complete-row and missing-row fixture. Spread summarizes the training observations; it does not select the imputer strategy. Median, most_frequent or constant can specify different replacements, so agreement with training means is specifically a check for strategy="mean".'''
b['fact_ids'] = ['f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7']

b = block('mle.dataset_quality_gate', 'tb6')
old = 'Set step IDs and waitFor dependencies; textual order alone does not establish the required dependency.'
new = "With omitted waitFor or an empty waitFor list, a Cloud Build step waits for all preceding steps to succeed; under that default, placing training after the fatal quality gate establishes the dependency. Explicit waitFor entries instead name the preceding step IDs that must succeed, such as waitFor: ['quality_gate'] on training. A step with waitFor: ['-'] depends only on the build starting and launches independently of preceding steps; do not give training that setting when it must wait for the gate. Inspect the configured dependencies rather than assuming every step uses the default."
assert old in b['content']
b['content'] = b['content'].replace(old, new)

b = block('mle.sklearn_baseline_workflow', 'tb4')
b['content'] = '''For an illustrative six-order fixture with two numerical features, use these aligned training and validation arrays:

```python
import numpy as np
from sklearn.linear_model import LogisticRegression

X_train = np.array([[0, 0], [1, 0], [0, 1], [3, 3], [4, 3], [3, 4]])
y_train = np.array([0, 0, 0, 1, 1, 1])
X_validation = np.array([[0, 0], [4, 4], [1, 0], [3, 3]])
y_validation = np.array([0, 1, 1, 0])
estimator = LogisticRegression(random_state=0)
estimator.fit(X_train, y_train)
predictions = estimator.predict(X_validation)
```

X_train has shape (6, 2), and y_train has shape (6,). Predictions are [0, 1, 0, 1], aligned with validation labels [0, 1, 1, 0]. In row order these give a true negative, true positive, false negative and false positive: TN=TP=FN=FP=1. Thus FPR=1/(1+1)=0.5 and FNR=1/(1+1)=0.5.

For this fixture, fix the reference predictions at [0, 0, 0, 0] before comparison. They give TN=2, FN=2, FP=TP=0, hence FPR=0 and FNR=1. Declare deployment probabilities P(Y=0)=P(Y=1)=0.5, cost_FP=2, cost_FN=8 and zero cost for correct predictions. The fitted estimator’s expected error cost is 0.5×0.5×2 + 0.5×0.5×8 = 2.5; the fixed reference’s is 0.5×0×2 + 0.5×1×8 = 4. Under this fixture’s fixed cost rule, the fitted estimator has lower expected error cost. That comparison does not establish satisfaction of other required constraints.

This fixture uses the supplied numerical representation directly. If training instead includes fitted preprocessing, obtain validation predictions through that fitted pipeline, not a freshly constructed validation representation. Fit establishes training state; predict applies it; evaluation compares corresponding held-out outputs with labels under the fixed rule.'''

path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')
print('entries:', len(data['entries']))
print('teaching blocks:', sum(len(r['teaching_blocks']) for r in data['entries']))
print('changed blocks: training_fitted_imputation tb3/tb4; dataset_quality_gate tb6; sklearn_baseline_workflow tb4')
print('skipped advisory: validation_early_stopping has no tb6; existing block IDs:', [b['id'] for b in entries['mle.validation_early_stopping']['teaching_blocks']])
