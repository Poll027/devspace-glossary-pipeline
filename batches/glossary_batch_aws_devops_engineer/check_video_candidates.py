from discover_video_candidates import *
from review_catalogue_matches import reject
D=load(B/'video_candidates.part.all.json'); G=load(B/'glossary_pass_a.json'); EX=load(B/'extracted_concepts.json'); CB=load(B/'coverage_briefs.json')
expected={(e['concept_id'],e['path_id']):e for e in G['entries'] if e['video_need']['level'] in {'HIGH','MEDIUM'}}
ex={(c['concept_id'],c['path_id']):c for c in EX['concepts']};cb={(c['concept_id'],c['path_id']):c for c in CB['briefs']}
rows={(s['concept_id'],s['path_id']):s for s in D['searches']}
assert len(rows)==len(D['searches']) and set(rows)==set(expected)
cat={v['video_id']:v for v in catalog}; op=load(B/'open_search_results.json');search={v['video_id']:v for vs in op.values() for v in vs}
choices=load(B/'catalogue_choices.json'); queries=load(B/'open_search_queries.json');lookup=load(B/'registry_lookup.json')
assert not any(x['reusable_segment_ids'] for x in lookup['lookups'])
idx={(e['concept_id'],e['path_id']):str(i) for i,e in enumerate(G['entries'])}
under=[]
for key,s in rows.items():
 e=expected[key];c=ex[key];brief=cb[key];b=s['search_brief'];ix=idx[key]
 assert b['concept_name']==c['concept_name']
 assert b['preferred_visual_modes']==e['video_need']['preferred_visual_modes']
 assert b['required_fact_ids']==[f['id'] for f in brief['evidence']['required_facts']]
 assert len(b['blocked_concepts_to_avoid'])<=3 and set(b['blocked_concepts_to_avoid'])<=set(c['blocked_knowledge_ids'])
 vs=s['candidates'];assert len(vs)<=5 and len({v['video_id'] for v in vs})==len(vs)
 kept=[v for v in vs if v['filter_verdict']=='kept'];assert len(kept)<=5
 if len(kept)<2:under.append((c['concept_id'],len(kept)))
 if s['search_route']=='allowlist_then_open_search':
  assert ix in queries and len(choices[ix])<2,(ix,'premature open search')
 else:assert len(choices[ix])>=2,(ix,'needs fallback search')
 for v in vs:
  assert re.fullmatch(r'[A-Za-z0-9_-]{11}',v['video_id'])
  assert v['youtube_url']=='https://www.youtube.com/watch?v='+v['video_id']
  source=cat[v['video_id']] if v['found_via']=='allowlist_catalogue' else search[v['video_id']]
  for k in ['video_id','title','channel_id','channel_name','duration_seconds']:assert v[k]==source[k],(ix,k)
  assert v['reason'].strip()
  if v['filter_verdict']=='kept':
   assert not reject(source),(ix,v['title'],reject(source))
   assert v['duration_seconds']>=90
for p,h in D['metadata']['parent_artifact_hashes'].items():assert hashlib.sha256(Path(p).read_bytes()).hexdigest()==h
assert D['batch_id']==D['metadata']['batch_id']=='glossary_batch_aws_devops_engineer'
assert D['metadata']['prompt_version']=='06_video_candidates@v1' and D['metadata']['model']=='none'
now=datetime.datetime.now(datetime.timezone.utc);stamp=datetime.datetime.fromisoformat(D['metadata']['generated_at']);assert stamp.utcoffset()==datetime.timedelta(0) and datetime.timedelta(0)<now-stamp<datetime.timedelta(hours=1)
report={'checklist':'PASS','batch_entries':len(G['entries']),'required_search_rows':len(expected),'actual_search_rows':len(rows),'low_video_need_skipped':len(G['entries'])-len(rows),'candidate_rows':sum(len(s['candidates']) for s in rows.values()),'kept':sum(v['filter_verdict']=='kept' for s in rows.values() for v in s['candidates']),'rejected':sum(v['filter_verdict']=='rejected' for s in rows.values() for v in s['candidates']),'under_two_kept':under,'uncertainty':'Titles and metadata only: English instruction, required-fact coverage and usable visual segment remain to be checked in transcript/segment stages. Dry-run and EC2 blue/green each have one plausible kept candidate after fallback search; no padding with unsuitable results.'}
(B/'video_candidates.mistakes_checklist.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
