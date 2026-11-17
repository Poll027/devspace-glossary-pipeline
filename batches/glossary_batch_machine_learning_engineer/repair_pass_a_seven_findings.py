import json
from pathlib import Path

path = Path('batches/glossary_batch_machine_learning_engineer/glossary_pass_a.part.all.json')
data = json.loads(path.read_text())
before = json.loads(path.read_text())
entries = {e['concept_id']: e for e in data['entries']}

def block(concept, bid):
    return next(b for b in entries['mle.' + concept]['teaching_blocks'] if b['id'] == bid)

def append(concept, bid, text, facts):
    b = block(concept, bid)
    b['content'] += '\n\n' + text
    b['fact_ids'] = list(dict.fromkeys(b['fact_ids'] + facts))

b = block('numpy_shape_dtype', 'tb3')
b['content'] = '''Define the validator with def, its name, parenthesized parameters and a colon. The indented lines form its body. Each if guard also ends with a colon; its further-indented raise ValueError(...) executes only when that guard is true, rejecting the input instead of continuing. Check rank before indexing the second axis. The return statement sends the accepted array back to the caller.

```python
import numpy as np

def validate_input(fixture, feature_count, batch_count):
    a = np.array(fixture)
    if a.ndim != 2:
        raise ValueError("expected batch and feature axes")
    if a.shape[1] != feature_count:
        raise ValueError("wrong feature count")
    if a.shape[0] != batch_count:
        raise ValueError("wrong batch count")
    return a

accepted = validate_input([[2, 10], [4, 20], [6, 30]], 2, 3)
assert accepted.shape == (3, 2)
```

Here fixture, feature_count and batch_count are parameters. The accepted call reaches return; validate_input([2, 10, 4, 20, 6, 30], 2, 3) instead enters the first guard and raises ValueError. Write assert predicate checks for declared valid, boundary and failure fixtures; a false predicate raises AssertionError during ordinary non-optimized execution.'''
b['fact_ids'] = ['f2', 'f3', 'f4', 'f5', 'f6']

append('numpy_vectorization', 'tb4', '''Construct both references rather than just naming a row-wise check. Allocate a zero-filled output with np.zeros(output_shape, dtype=declared_dtype); this example declares shape (3, 2) and dtype float64. The for header ends with a colon and its assignment is indented. range stops before the row count, so i is 0, 1, then 2. input_array[i] selects row i and reference[i] assigns its transformed row.

```python
import numpy as np

input_array = np.array([[2, 10], [4, 20], [6, 30]], dtype=np.float64)
feature_reference = np.array([1, 5], dtype=np.float64)
array_result = input_array - feature_reference
reference = np.zeros((3, 2), dtype=np.float64)
for i in range(input_array.shape[0]):
    reference[i] = input_array[i] - feature_reference
reference_list = [row - feature_reference for row in input_array]
comprehension_reference = np.array(reference_list)
assert array_result.shape == (3, 2)
np.testing.assert_allclose(array_result, reference, rtol=1e-7, atol=1e-9)
np.testing.assert_allclose(array_result, comprehension_reference, rtol=1e-7, atol=1e-9)
```

The comprehension follows [expression for item in sequence]: each row supplies the expression row - feature_reference, producing a new list, which np.array converts before comparison. The loop assigns [1, 5], [3, 15] and [5, 25] to rows 0, 1 and 2; the comprehension constructs those same rows. Both therefore agree with the vectorized result under the explicit tolerances.''', ['f5', 'f6'])

append('dataset_inspection', 'tb3', '''An optional inspection setting uses name=default_value in the function signature. Omitting it at the call site uses that default; a keyword call name=value overrides it. For this numerical-summary example, use the standard-deviation divisor as the setting:

```python
import numpy as np

def inspect_numeric(numeric_values, ddof=0):
    return {"mean": np.mean(numeric_values, axis=0),
            "std": np.std(numeric_values, axis=0, ddof=ddof)}

values = np.array([[2, 10], [4, 20], [6, 30]])
population_summary = inspect_numeric(values)
sample_summary = inspect_numeric(numeric_values=values, ddof=1)
```

The first call uses ddof=0: the first feature's standard deviation is sqrt(8/3), about 1.633. The second names both arguments and overrides ddof with 1: for a stated calculation requiring the N−1 divisor, that feature's result is sqrt(8/2)=2. The mean remains 4. Choose the override only when the stated calculation requires it.''', ['f7'])

b = block('model_risk_documentation', 'tb3')
b['content'] = 'Record any grant outside the existing policy’s permitted identity scope, and state only the limitations supported by the supplied evaluation. Do not extend permission scope or imply universal suitability.'
b['fact_ids'] = ['f1', 'f3']
b = block('model_risk_documentation', 'tb4')
b['content'] = b['content'].replace('Include the documented task limits, foreseeable misuse cases and supported segment limitations from the supplied records.', 'Include supported segment limitations from the supplied evaluation.').replace('Build one record preserving the existing policy fields, so a reader can distinguish permitted use, an observed access mismatch and a supported evaluation limitation.', 'Keep the existing permitted identity scope distinct from an observed access mismatch and a supported evaluation limitation.').replace("Preserve the task's foreseeable misuse cases and stated permitted use alongside the observed facts. ", '')
for bid in ['tb4', 'tb5']:
    b = block('model_risk_documentation', bid)
    b['fact_ids'] = [f for f in b['fact_ids'] if f != 'f4']

append('pytorch_input_tensors', 'tb3', '''Matrix multiplication is a different operation from elementwise multiplication. Use A @ B or torch.matmul(A, B). For two-dimensional inputs, (m, n) @ (n, p) produces (m, p): first check the matching inner dimensions A.shape[1] == B.shape[0], then check the output axes.

```python
import torch

A = torch.tensor([[2., 10.], [4., 20.], [6., 30.]])
B = torch.tensor([[1.], [0.5]])
assert A.shape[1] == B.shape[0]
result = A @ B
assert result.shape == (3, 1)
assert torch.matmul(A, B).shape == (3, 1)
```

Here (3, 2) @ (2, 1) gives (3, 1), with values [[7], [14], [21]]: the first output is 2×1 + 10×0.5. A weight fixture shaped (3, 1) would fail the inner-dimension check. A * B instead multiplies elements under elementwise broadcasting rules, not by summing these products; it is not a substitute for @.''', ['f3'])

b = block('task_loss_selection', 'tb4')
b['content'] = '''For the class-index cross-entropy fixture, assume unweighted mean reduction, no ignored examples and no label smoothing. N is the number of examples (rows) in logits of shape (N, C); C is the number of classes. Sum the per-example losses and divide by N. Each logit derivative is (softmax probability−one-hot target)/N.

Compute sigmoid(z) = 1 / (1 + exp(−z)), where exp is the exponential function, for each binary logit's probability. For each row of C class logits, softmax gives p[c] = exp(z[c]) / sum_j exp(z[j]); the denominator sums over classes in that row, not over examples. torch.nn.Softmax(dim=1)(logits) performs this class-axis normalization for (N, C) logits. A one-hot target row places 1 at the target class index and 0 elsewhere. torch.nn.functional.one_hot(targets, num_classes=C) converts long indices of shape (N,) to rows of shape (N, C) for the manual gradient reference.'''
b['fact_ids'] = ['f7', 'f8', 'f9', 'f10']
append('task_loss_selection', 'tb5', '''Trace the probability constructions before subtracting targets. In the binary fixture, M=1 loss element, so sigmoid(0)=1/(1+exp(0))=1/2, and (0.5−1)/1=−0.5. For an unweighted, unsmoothed class-index fixture with no ignored examples, take two rows of three zero logits and target indices [1, 2]. N=2 examples and C=3 classes. Each row's exponential values are [1, 1, 1], with denominator 3, so both probability rows are [1/3, 1/3, 1/3]. The one-hot rows are [0, 1, 0] and [0, 0, 1]. Subtract and divide by N=2 to obtain gradients [1/6, −1/3, 1/6] and [1/6, 1/6, −1/3].

```python
import torch

logits = torch.tensor([[0., 0., 0.], [0., 0., 0.]])
targets = torch.tensor([1, 2], dtype=torch.long)
probabilities = torch.nn.Softmax(dim=1)(logits)
one_hot = torch.nn.functional.one_hot(targets, num_classes=3)
manual_gradient = (probabilities - one_hot) / logits.shape[0]
```

This code constructs the same rows used in the manual trace. The MSE reference instead divides by M, the number of output elements across all axes; here M=2 and 2×([2, 4]−[1, 2])/2=[1, 2]. The unweighted mean binary reference also divides by M, not by an assumed batch count. Keep these fixture conditions explicit rather than applying the class-index formula to weighted or smoothed losses.''', ['f8', 'f9', 'f10'])

b = block('prediction_authentication', 'tb3')
b['content'] = b['content'].split(' A Compose YAML document')[0]
b['fact_ids'] = ['f4', 'f5']
b = block('prediction_authentication', 'tb4')
b['content'] = 'Keep the declared nonsecret authentication settings separate from the credential secret. Write the mapping/list configuration with yaml.safe_dump, reload it with yaml.safe_load, and inspect the required resolved fields before submitting it to the existing runtime.'
b['fact_ids'] = ['f3', 'f12']
b = block('prediction_authentication', 'tb7')
b['content'] = b['content'].replace('Configure the immutable image, ports and nonsecret authentication fields in parsed Compose YAML, with secrets supplied only through runtime references.', 'Keep the nonsecret authentication fields separate from secrets supplied through runtime references, and inspect the required configuration fields after safe loading.')
b['fact_ids'] = [f for f in b['fact_ids'] if f not in ['f6', 'f7', 'f8', 'f9']]

changed = [a['concept_id'] for a, b in zip(data['entries'], before['entries']) if a != b]
assert len(changed) == 7
assert data['metadata'] == before['metadata'] and data['batch_id'] == before['batch_id']
briefs = json.loads(Path('batches/glossary_batch_machine_learning_engineer/coverage_briefs.json').read_text())['briefs']
for cid in changed:
    required = {f['id'] for r in briefs if r['concept_id'] == cid for f in r['evidence']['required_facts']}
    tagged = {f for b in entries[cid]['teaching_blocks'] for f in b['fact_ids']}
    assert tagged == required, (cid, tagged, required)
path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
print('Changed:', ', '.join(changed))
print('Entries:', len(data['entries']))
print('Teaching blocks:', sum(len(e['teaching_blocks']) for e in data['entries']))
