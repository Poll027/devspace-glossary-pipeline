import json
from pathlib import Path
p=Path('batches/glossary_batch_machine_learning_engineer/glossary_pass_a.part.all.json')
d=json.loads(p.read_text())
e=next(e for e in d['entries'] if e['concept_id']=='mle.serving_resource_cleanup')
b={b['id']:b for b in e['teaching_blocks']}
old='Check captured commands and logs for secret values or sensitive data, with runtime-injected credentials kept out of cleanup code and printed output.'
new='Keep runtime-injected credentials in the authorized runtime secret mechanism, not in cleanup code or printed output. Check captured commands and logs for secret values or sensitive data. This non-disclosure check is supported by Docker’s [Manage secrets securely in Docker Compose](https://docs.docker.com/compose/how-tos/use-secrets/) (introductory guidance on exposure in debug logs; Use secrets), [SecretsUsedInArgOrEnv](https://docs.docker.com/reference/build-checks/secrets-used-in-arg-or-env/) (Description), and [Swarm secrets](https://docs.docker.com/engine/swarm/secrets/) (Example: Rotate a secret, which keeps passwords off the command line and out of shell history). Container-log retrieval alone does not establish the credential-handling rule.'
assert old in b['tb3']['content']
b['tb3']['content']=b['tb3']['content'].replace(old,new,1)
# The audit-record instruction depends on the corrected non-disclosure fact.
assert b['tb4']['fact_ids']==['f7','f8','f9']
b['tb4']['fact_ids']=['f4','f7','f8','f9']
old='Keep runtime credentials out of cleanup code and captured logs.'
new='Keep runtime-injected credentials in the authorized runtime secret mechanism and out of cleanup code and printed output; check captured commands and logs for secret values or sensitive data before including cleanup evidence in the audit record.'
assert old in b['tb6']['content']
b['tb6']['content']=b['tb6']['content'].replace(old,new,1)
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
print('entries:',len(d['entries']),'teaching blocks:',sum(len(e['teaching_blocks']) for e in d['entries']))
print('Changed only mle.serving_resource_cleanup: tb3 content, tb4 fact_ids, tb6 content.')
