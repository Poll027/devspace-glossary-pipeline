import json,re,math
p='batches/glossary_batch_aws_devops_engineer/';b=json.load(open(p+'glossary_bundles_draft.json'))['bundles'];refs=json.load(open(p+'audit13/refurls.json'));src={u:i for u,i,_ in json.load(open(p+'audit13/fetched.json'))}
stop=set('the a an and or to in of with for is are as from on by that this it its be then supplied approved inspect use configure verify against only does not rather than'.split())
def words(s):return set(re.findall(r'[a-z0-9_:.-]+',s.lower()))-stop
for start in range(0,128,8):
 out=[]
 for i in range(start,start+8):
  x=b[i];out+=['\n### '+str(i)+' '+x['context']['concept_id']];seen=set()
  for f in x['coverage']['required_facts']:
   for r in f['source_refs']:
    r=r if isinstance(r,str) else r['source_ref'];u=refs[r];n=src[u];raw=open(p+f'audit13/source{n}.txt').read();lines=[t for line in raw.splitlines() for t in re.split(r'(?<=[.!?])\s+(?=[A-Z])',line)];w=words(f['statement']);rank=[]
    for li,line in enumerate(lines):
     if len(line)<45:continue
     score=len(w&words(line));score=score-5 if ' - ' in line and len(line)<120 else score;rank.append((score,li))
    ranked=sorted(rank,reverse=True);selected=[]
    for score,li in ranked[:1]:
     if (n,li) not in seen:selected.append((li,lines[li]));seen.add((n,li))
    out+=['SOURCE '+str(n)+' '+u+' ['+f['id']+']']
    for li,t in sorted(selected):out+=[str(li+1)+': '+t[:1500]]
 open(p+f'audit13/sources{start}.txt','w').write('\n'.join(out))
