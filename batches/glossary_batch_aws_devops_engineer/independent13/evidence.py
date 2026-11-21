exec(open('batches/glossary_batch_aws_devops_engineer/independent13/check.py').read().split('for i in range')[0])
for i in range(int(sys.argv[1]),int(sys.argv[2])):
 print('\n###',i,e[i]['concept_id'])
 for f in c[i]['evidence']['required_facts']:
  matches=[];ftok=tok(f['statement'])
  for z in f['source_refs']:
   o=si[z];t=(q/f"s{o['i']}.txt").read_text();parts=re.split(r'(?<=[.!?])\s+',t)
   for k,part in enumerate(parts):
    score=sum(1 for a in ftok if a in tok(part));matches.append((score,z,part))
  score,z,part=max(matches);print(f['id'],z,part[:1200])
