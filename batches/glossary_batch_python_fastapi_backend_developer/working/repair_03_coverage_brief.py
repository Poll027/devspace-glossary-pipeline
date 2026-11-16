import copy
import json
import re
from pathlib import Path

path = Path('batches/glossary_batch_python_fastapi_backend_developer/coverage_briefs.part.all.json')
data = json.loads(path.read_text())
before = copy.deepcopy(data)
briefs = {b['concept_id']: b for b in data['briefs']}
def evidence(cid):
    return briefs[cid]['evidence']
def fact(cid, fid):
    return next(f for f in evidence(cid)['required_facts'] if f['id'] == fid)

cid = 'fastapi_backend.orm_entity_mapping'
fact(cid, 'f1')['statement'] = "A mapped class associates Python attributes with a database table's columns; first create the shared base with class Base(DeclarativeBase): pass, then inherit mapped entities from Base and declare attributes with Mapped[Type] and mapped_column(...)."
fact(cid, 'f1')['source_refs'] = [
    'sqlalchemy_20_tutorial#https://docs.sqlalchemy.org/en/20/tutorial/metadata.html#establishing-a-declarative-base',
    'sqlalchemy_20_tutorial#https://docs.sqlalchemy.org/en/20/tutorial/metadata.html#declaring-mapped-classes',
]

# Use the artifact's existing approved source-ID + full-URL locator convention.
fact('asgi.request_lifecycle', 'f3')['source_refs'] = [
    'fastapi_docs_advanced#https://asgi.readthedocs.io/en/latest/specs/www.html#request-receive-event',
    'fastapi_docs_advanced#https://asgi.readthedocs.io/en/latest/specs/www.html#response-start-send-event',
    'fastapi_docs_advanced#https://asgi.readthedocs.io/en/latest/specs/www.html#response-body-send-event',
]
for fid in ['f2', 'f3']:
    fact('design.backend_separation_of_concerns', fid)['source_refs'] = [
        'fastapi_docs_advanced#https://www.cosmicpython.com/book/chapter_04_service_layer.html#_a_typical_service_function',
        'fastapi_docs_advanced#https://www.cosmicpython.com/book/chapter_04_service_layer.html#_wrap_up',
    ]

cid = 'fastapi_backend.webhook_replay_freshness'
fact(cid, 'f1')['statement'] = "A replay freshness check uses a delivery timestamp authenticated by the provider's signature; providers can refresh that timestamp and signature for each retry, so it establishes delivery-timestamp freshness, not the original event's age, and an unsigned timestamp cannot establish authenticated delivery freshness."
fact(cid, 'f2')['statement'] = "After signature verification, parse the signed delivery timestamp and reject a delivery outside the configured acceptance window, including timestamps unacceptably far in the future under the provider's policy."
fact(cid, 'f4')['statement'] = "Test valid signatures for an in-window delivery timestamp, an expired delivery timestamp and an impermissibly future delivery timestamp, verifying that authenticity alone does not make every signed delivery fresh."
# The acceptance-window section backs the timestamp test cases; the testing
# section explicitly requires stale-delivery freshness checks.
fact(cid, 'f4')['source_refs'].append('owasp_api_security_top10_2023#https://cheatsheetseries.owasp.org/cheatsheets/Webhook_Security_Cheat_Sheet.html#replay-attack-protection')

cid = 'python.decorator_wrappers'
e = evidence(cid)
e['optional_enrichment'].append(fact(cid, 'f4'))
e['required_facts'] = [f for f in e['required_facts'] if f['id'] != 'f4']

cid = 'http.representation_headers'
fact(cid, 'f2')['statement'] = 'Accept communicates acceptable response media types.'
evidence(cid)['optional_enrichment'].append({
    'id': 'f4',
    'statement': 'Accept quality values express relative preference among acceptable response media types.',
    'source_refs': copy.deepcopy(fact(cid, 'f2')['source_refs']),
})

cid = 'fastapi.bounded_multipart_inputs'
fact(cid, 'f4')['statement'] = fact(cid, 'f4')['statement'].replace('part size', 'non-file field size')

rfc_facts = {
    'http.method_safety_idempotency': {'f1', 'f2', 'f3', 'f4', 'f5'},
    'http.representation_headers': {'f1', 'f2', 'f3', 'f4'},
    'http.status_selection': {'f1', 'f2', 'f3', 'f4'},
    'rest.resource_contract_design': {'f1', 'f3', 'f4'},
    'fastapi.domain_error_translation': {'f2'},
    'fastapi.safe_unexpected_errors': {'f2'},
    'integration.upstream_failure_translation': {'f4'},
    'integration.bounded_idempotent_retries': {'f1', 'f2', 'f4', 'f5'},
}
for cid, ids in rfc_facts.items():
    e = evidence(cid)
    for f in e['required_facts'] + e['optional_enrichment']:
        if f['id'] in ids:
            f['source_refs'] = [re.sub(r'https://www\.rfc-editor\.org/rfc/rfc9110#([0-9.]+)$', r'https://www.rfc-editor.org/rfc/rfc9110.html#section-\1', ref) for ref in f['source_refs']]

allowed = set(rfc_facts) | {'fastapi_backend.orm_entity_mapping', 'asgi.request_lifecycle', 'design.backend_separation_of_concerns', 'fastapi_backend.webhook_replay_freshness', 'python.decorator_wrappers', 'fastapi.bounded_multipart_inputs'}
changed = []
for old, new in zip(before['briefs'], data['briefs']):
    if old != new:
        assert new['concept_id'] in allowed
        assert {k: v for k, v in old.items() if k != 'evidence'} == {k: v for k, v in new.items() if k != 'evidence'}
        changed.append(new['concept_id'])
assert data['metadata'] == before['metadata']
assert len(data['briefs']) == len(before['briefs'])
path.write_text(json.dumps(data, indent=2) + '\n')
print('Changed briefs:', len(changed), ', '.join(changed))
print('Briefs:', len(data['briefs']))
for field in ['required_facts', 'optional_enrichment', 'misconceptions']:
    print(field, sum(len(b['evidence'][field]) for b in data['briefs']))
