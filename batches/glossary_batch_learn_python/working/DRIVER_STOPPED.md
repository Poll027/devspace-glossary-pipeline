# STOPPED glossary_batch_learn_python

command failed (1): /home/azureuser/env/bin/python /home/azureuser/roles/learn_python/glossary/00_GLOSSARY_PIPELINE_CORE/scripts/glm_generate.py '/home/azureuser/roles/learn_python/glossary/batches/glossary_batch_learn_python' 'c4'
: 0 proposals, 1 rejected
qhgTj7GQUiM: 1 proposals, 0 rejected
3ohzBxoFHAY: 1 proposals, 0 rejected
6v9VKY71n28: 0 proposals, 1 rejected
-aKFBoZpiqA: 1 proposals, 0 rejected
utjgdD1l7S4: 1 proposals, 0 rejected
ozxD0eiag6Y: 0 proposals, 1 rejected
eirjjyP2qcQ: 0 proposals, 1 rejected
DwBDHsdX6XQ: 0 proposals, 1 rejected
VEbuZox5qC4: 0 proposals, 1 rejected
-ARI4Cz-awo: no catalogue entry (transcript fetch failed), skipping
urrfJgHwIJA: 0 proposals, 1 rejected
sugvnHA7ElY: 1 proposals, 0 rejected
8A0E1dSyjFM: 0 proposals, 1 rejected
0twL6MXCLdQ: 0 proposals, 1 rejected
88pl8TuuKz0: 1 proposals, 0 rejected
HNChkuE6HyA: 0 proposals, 1 rejected
tJxcKyFMTGo: 0 proposals, 1 rejected
5iWhQWVXosU: 0 proposals, 1 rejected
KzqSDvzOFNA: 1 proposals, 0 rejected
Traceback (most recent call last):
  File "/home/azureuser/roles/learn_python/glossary/00_GLOSSARY_PIPELINE_CORE/scripts/schema_check.py", line 24, in <module>
    validate(json.loads(Path(sys.argv[2]).read_text()), sys.argv[1])
  File "/home/azureuser/roles/learn_python/glossary/00_GLOSSARY_PIPELINE_CORE/scripts/schema_check.py", line 18, in validate
    jsonschema.Draft202012Validator(schema, registry=reg).validate(obj)
  File "/home/azureuser/env/lib/python3.12/site-packages/jsonschema/validators.py", line 450, in validate
    raise error
jsonschema.exceptions.ValidationError: [] should be non-empty

Failed validating 'minItems' in schema['properties']['proposals']['items']['properties']['covered_fact_ids']:
    {'type': 'array', 'minItems': 1, 'items': {'type': 'string'}}

On instance['proposals'][6]['covered_fact_ids']:
    []
Traceback (most recent call last):
  File "/home/azureuser/roles/learn_python/glossary/00_GLOSSARY_PIPELINE_CORE/scripts/glm_generate.py", line 191, in <module>
    main()
  File "/home/azureuser/roles/learn_python/glossary/00_GLOSSARY_PIPELINE_CORE/scripts/glm_generate.py", line 186, in main
    subprocess.run([sys.executable, str(CORE / "scripts" / "schema_check.py"), "segment_proposals.schema.json", str(dest)], check=True)
  File "/usr/lib/python3.12/subprocess.py", line 571, in run
    raise CalledProcessError(retcode, process.args,
subprocess.CalledProcessError: Command '['/home/azureuser/env/bin/python', '/home/azureuser/roles/learn_python/glossary/00_GLOSSARY_PIPELINE_CORE/scripts/schema_check.py', 'segment_proposals.schema.json', '/home/azureuser/roles/learn_python/glossary/batches/glossary_batch_learn_python/segment_proposals.part.c4.json']' returned non-zero exit status 1.


Spend so far $6.62. Fix the cause, then rerun the same command (finished stages are skipped).
