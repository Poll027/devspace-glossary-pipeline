import json
from pathlib import Path
p = Path('batches/glossary_batch_python_fastapi_backend_developer/glossary_pass_a.part.all.json')
d = json.loads(p.read_text())
before = json.loads(p.read_text())
rows = {r['concept_id']: r for r in d['entries']}
b = next(b for b in rows['pydantic.model_validation_conversion']['teaching_blocks'] if b['id'] == 'tb2')
b['content'] += " In default non-strict validation, bool accepts the case-insensitive strings '0', 'off', 'f', 'false', 'n', 'no', '1', 'on', 't', 'true', 'y', and 'yes'. Integer validation rejects non-finite floats, including nan and inf."
b['fact_ids'].append('f2')
b = next(b for b in rows['fastapi.validated_environment_configuration']['teaching_blocks'] if b['id'] == 'tb5')
old = 'Construct Settings() to read environment variables and validate them. Try one missing required setting and one value that cannot satisfy its declared type; both should fail validation rather than becoming unchecked application inputs.'
new = 'In the application lifespan function, construct settings = Settings() before the yield, so environment variables are read and validated before requests are served. Retain that validated settings instance for the application to use while serving requests, rather than constructing it for the first time inside an endpoint. Only proceed to the yield after construction succeeds. Try one missing required setting and one value that cannot satisfy its declared type; let either validation failure propagate and abort startup instead of waiting for the first request to fail.'
assert old in b['content']
b['content'] = b['content'].replace(old, new)
changed = [(old['concept_id'], ob['id']) for old, new in zip(before['entries'], d['entries']) for ob, nb in zip(old['teaching_blocks'], new['teaching_blocks']) if ob != nb]
assert changed == [('pydantic.model_validation_conversion', 'tb2'), ('fastapi.validated_environment_configuration', 'tb5')], changed
p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n')
print('Changed:', changed)
print('Entries:', len(d['entries']), 'teaching blocks:', sum(len(r['teaching_blocks']) for r in d['entries']))
