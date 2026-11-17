import ast
import json
from pathlib import Path
p = Path('batches/glossary_batch_machine_learning_engineer/glossary_pass_a.part.all.json')
before = json.loads(p.read_text())
after = json.loads(p.read_text())
rows = {r['concept_id']: r for r in after['entries'] if r['path_id'] == 'machine_learning_engineer'}
def block(cid, bid):
    return next(b for b in rows[cid]['teaching_blocks'] if b['id'] == bid)
b = block('ml.task_specific_pretrained_weight_fine_tuning', 'tb2')
old = 'For the bounded ViT image-classification adaptation, import torch, nn from torch, and AutoImageProcessor, ViTForImageClassification, TrainingArguments and Trainer from transformers.'
imports = 'import torch\nfrom torch import nn\nfrom transformers import AutoImageProcessor, ViTForImageClassification, TrainingArguments, Trainer'
ast.parse(imports)
assert old in b['content']
b['content'] = b['content'].replace(old, 'For the bounded ViT image-classification adaptation, use these explicit imports:\n\n```python\n' + imports + '\n```', 1)
b = block('mle.authorized_retraining_execution', 'tb7')
b['content'] = '''Consider an illustrative invocation record with trigger authorization marked approved, the authorized build/step identity recorded, and approved input identified as object training-data, generation 17. Retrieve and verify that exact generation before invoking the supplied pipeline. The record retains the supplied pipeline name, actual snapshot parameters (object training-data, generation 17), ClientRequestToken and the returned PipelineExecutionArn; the execution identity is the returned value, not a guessed identifier.

Now compare that record with the triggered execution’s observed stage inputs. In the matching fixture, the training stage consumes object training-data, generation 17: the consumed identity matches the approved immutable input, so the input check accepts it. In the mismatching fixture, the request still names generation 17, but the observed training-stage input is generation 18: reject the input check and keep that gate failure fatal. An approved request is not proof that the approved generation was consumed.

Both fixtures use the existing event-bound build stages and required successful dependencies. Approved Secret Manager versions remain references exposed only to the needed step; neither the invocation record nor captured build output contains runtime credential values. Inspect the captured output to verify non-disclosure. Permission to execute retraining does not supply the separate authorization needed for promotion.'''
allowed = {('ml.task_specific_pretrained_weight_fine_tuning', 'tb2'), ('mle.authorized_retraining_execution', 'tb7')}
changed = []
for a, z in zip(before['entries'], after['entries']):
    if a == z:
        continue
    assert {k:v for k,v in a.items() if k != 'teaching_blocks'} == {k:v for k,v in z.items() if k != 'teaching_blocks'}
    for ab, zb in zip(a['teaching_blocks'], z['teaching_blocks']):
        if ab != zb:
            key = (a['concept_id'], ab['id'])
            assert key in allowed
            assert {k:v for k,v in ab.items() if k != 'content'} == {k:v for k,v in zb.items() if k != 'content'}
            changed.append(key)
assert set(changed) == allowed
p.write_text(json.dumps(after, ensure_ascii=False, indent=2) + '\n')
print('Changed:', changed)
print('Rows:', len(after['entries']))
print('Teaching blocks:', sum(len(r['teaching_blocks']) for r in after['entries']))
