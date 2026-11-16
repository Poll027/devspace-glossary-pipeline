import copy
import json
from pathlib import Path

path = Path('batches/glossary_batch_python_fastapi_backend_developer/glossary_pass_a.part.all.json')
data = json.loads(path.read_text())
before = copy.deepcopy(data)
entries = {r['concept_id']: r for r in data['entries']}

def block(concept, block_id):
    return next(b for b in entries[concept]['teaching_blocks'] if b['id'] == block_id)

def replace(concept, block_id, old, new):
    b = block(concept, block_id)
    assert old in b['content']
    b['content'] = b['content'].replace(old, new, 1)

replace('testing.database_state_isolation', 'tb4',
        'Close session and connection, roll back the outer transaction and restore overrides during teardown',
        'During teardown, close the test session, roll back the outer transaction, close the connection, and restore dependency overrides')
replace('pydantic.model_validation_conversion', 'tb6',
        'Default validation can convert compatible values.',
        'Ordinary model validation can convert compatible input values.')
replace('fastapi_backend.application_lifespan', 'tb5',
        "The reason to share here is the brief's explicit goal of avoiding repeated startup work;",
        'Sharing here avoids repeated startup work;')

block('fastapi.endpoint_integration_tests', 'tb5')['content'] = '''For a synthetic order-retrieval contract, GET /orders/42 should return status 200 and the JSON body {"id": 42, "quantity": 2}. With app configured for that contract, this test demonstrates both assertions:

```python
from fastapi.testclient import TestClient

def test_get_order():
    with TestClient(app) as client:
        response = client.get("/orders/42")
        assert response.status_code == 200
        assert response.json() == {"id": 42, "quantity": 2}
```

Run the test_ function with pytest. The request goes through route and dependency resolution, unlike a direct handler call. The TestClient context executes lifespan setup and teardown when the case requires application-lifetime resources. The status assertion checks the intended HTTP outcome; the JSON assertion checks the expected public content. Neither assertion substitutes for the other.'''

block('fastapi.openapi_generation', 'tb5')['content'] = '''Retrieve /openapi.json and locate the order operation under paths. This minimal illustrative excerpt represents a POST /orders contract with an OrderInput body and an OrderOutput response; unrelated document fields are omitted:

```json
{
  "paths": {
    "/orders": {
      "post": {
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {"$ref": "#/components/schemas/OrderInput"}
            }
          }
        },
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {"$ref": "#/components/schemas/OrderOutput"}
              }
            }
          }
        }
      }
    }
  },
  "components": {
    "schemas": {
      "OrderInput": {
        "type": "object",
        "properties": {"quantity": {"type": "integer"}},
        "required": ["quantity"]
      },
      "OrderOutput": {
        "type": "object",
        "properties": {"id": {"type": "integer"}},
        "required": ["id"]
      }
    }
  }
}
```

Follow the request body's $ref to OrderInput: its quantity field corresponds to the typed body declaration quantity: int. Follow the response's $ref to OrderOutput: its id field corresponds to the response-model declaration id: int. Here quantity belongs to input and id to output, so the operation's two references lead to different public definitions. This connects declarations to generated structure; documentation is not proof of every runtime outcome.'''

block('fastapi.contract_examples_metadata', 'tb5')['content'] = '''For a synthetic order sample, use quantity 2 with a model whose quantity must be greater than zero. This places the compatible payload in model-level schema examples and validates it before publishing the documentation:

```python
from pydantic import BaseModel, ConfigDict, Field

example = {"quantity": 2}

class OrderInput(BaseModel):
    quantity: int = Field(gt=0)
    model_config = ConfigDict(json_schema_extra={"examples": [example]})

OrderInput.model_validate(example)
```

The sample's quantity satisfies the declared bound; an incompatible sample would mislead about accepted input. For field-level schema examples, use Field(examples=[...]); for named request-body examples, use Body(openapi_examples={...}). Add tags, summary and description to group and explain the operation without assuming they change behavior. The validated synthetic sample illustrates the declared shape rather than a different contract.'''

entries['fastapi.header_cookie_binding']['video_need']['level'] = 'MEDIUM'
entries['fastapi.header_cookie_binding']['video_need']['reason'] = 'Annotated code supports the Header and Cookie declarations and underscore-to-hyphen conversion; a demonstration can help, but the text largely suffices.'

allowed = {
    ('testing.database_state_isolation', 'tb4'),
    ('pydantic.model_validation_conversion', 'tb6'),
    ('fastapi_backend.application_lifespan', 'tb5'),
    ('fastapi.endpoint_integration_tests', 'tb5'),
    ('fastapi.openapi_generation', 'tb5'),
    ('fastapi.contract_examples_metadata', 'tb5'),
}
for old, new in zip(before['entries'], data['entries']):
    cid = old['concept_id']
    for ob, nb in zip(old['teaching_blocks'], new['teaching_blocks']):
        if ob != nb:
            assert (cid, ob['id']) in allowed
            assert {k:v for k,v in ob.items() if k != 'content'} == {k:v for k,v in nb.items() if k != 'content'}
    if old['video_need'] != new['video_need']:
        assert cid == 'fastapi.header_cookie_binding'
    assert old['teaching_notes'] == new['teaching_notes']
assert before['metadata'] == data['metadata']
path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
print('Entries:', len(data['entries']))
print('Teaching blocks:', sum(len(r['teaching_blocks']) for r in data['entries']))
print('Changed entries:', sum(a != b for a,b in zip(before['entries'], data['entries'])))
