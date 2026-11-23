from pathlib import Path
import json,hashlib,datetime,re,collections
B=Path('batches/glossary_batch_business_analyst');C=Path('00_GLOSSARY_PIPELINE_CORE');load=lambda p:json.loads(Path(p).read_text())
g=load(B/'glossary_pass_a.json');x=load(B/'extracted_concepts.json');r=load(B/'registry_lookup.json');b=load(B/'coverage_briefs.json')
cs={c['concept_id']:c for c in x['concepts']};br={e['concept_id']:e for e in b['briefs']};rs={e['concept_id']:e for e in r['lookups']};ch={e['channel_id']:e for e in load(C/'video_bank/channel_allowlist.json')['channels']}
inputs=[B/f for f in ['glossary_pass_a.json','registry_lookup.json','extracted_concepts.json','coverage_briefs.json','approved_segments_snapshot.json']]+[C/'video_bank/channel_allowlist.json']
cat={}
for f in sorted((C/'video_bank/channel_catalogs').glob('*.json')):
 inputs.append(f);d=load(f)
 for v in d['videos']:cat[v['video_id']]={**v,'channel_id':d['channel_id'],'channel_name':ch[d['channel_id']]['channel_name']}
segs={s['segment_id']:s for s in load(B/'approved_segments_snapshot.json')['segments']}
sel=load(B/'working/catalog_selection.json');osel=load(B/'working/open_selection.json');ores=load(B/'working/open_results.json');openall={v['video_id']:v for vs in ores.values() for v in vs}
rejects={2:[('Qyu8Ihe0auo','Drug-discovery infrastructure talk, not facilitation of requirements workshops.')],10:[('2EJQU3a2Fgo','Vendor SaaS risk-assessment infrastructure talk, not an introductory requirements risk matrix.')],19:[('O85OWBJ2ayo','Matrix exponentiation is mathematics, not stakeholder influence-interest mapping.')],31:[('wpNl-JwwplA','Feature selection and missing-data treatment concern predictive decision trees, not business-rule branching.')],35:[('qb-4PdLTsJs','One-to-many VPC architecture is cloud infrastructure, not relational data cardinality.')],62:[('gDJQw84EOnM','AWS event discussion of sustainability transformation is not a bounded introductory business-case development tutorial.')]}
focus={2:'facilitating a requirements session',5:'observing work in context',7:'drawing low-fidelity screens',9:'moderating focus-group discussion',10:'plotting probability and impact',15:'constructing requirement-to-deliverable links',16:'reviewing page versions and history in Confluence',19:'plotting stakeholders on power/interest axes',20:'constructing a RACI responsibility table',22:'guiding a group workshop',23:'facilitating consensus',24:'drawing core BPMN notation',25:'building a simple process map that could support current-state modeling',26:'process-map construction that could support a proposed-state diagram',27:'identifying process capacity bottlenecks',28:'introductory process-improvement methods',30:'representing rules in a decision table',31:'drawing branching decisions rather than fitting a predictive classifier',33:'identifying primary keys',34:'foreign-key constraints',35:'one-to-many relational cardinality',36:'resolving many-to-many relationships with junction tables',37:'representing relationship cardinality',38:'drawing an entity-relationship diagram',43:'SQL inner-join results',44:'grouped SQL aggregation',45:'row filtering versus group filtering',46:'SQL NULL handling',47:'left-preserving SQL joins',48:'right-preserving SQL joins',49:'full outer SQL joins',50:'ordering SQL results',51:'grouped SQL queries used for reporting',52:'Power BI import and Power Query preparation',53:'Tableau source connection and union preparation',59:'Kano requirements prioritization',60:'weighted scoring of options',61:'comparing solution options with decision criteria',62:'structuring a business case',63:'multi-criteria option comparison',64:'interpreting measures of center',65:'variance and standard deviation',68:'sequencing releases with story maps',72:'structuring a stakeholder presentation',73:'conducting a requirements review',74:'drawing system boundaries and external interactions',75:'decomposing business functions',76:'copying relative, absolute and mixed cell references',77:'building a PivotTable summary',78:'exact-match spreadsheet lookups',79:'conditional IF/IFS alternatives',80:'creating spreadsheet charts',81:'using pivots for question-specific business reports',85:'reviewing demonstrated work in a Sprint Review',87:'following a chain of why questions',88:'organizing causes on fishbone branches',90:'arranging fact and dimension tables',91:'configuring BI model relationships',92:'constructing a Power BI report canvas',93:'constructing a Tableau dashboard',95:'publishing and sharing Power BI reports',96:'distinguishing DAX measures and calculated columns',97:'creating Tableau calculated fields',98:'reusing a semantic model and understanding Build permission'}
rows=[]
for e in g['entries']:
 if e['video_need']['level'] not in ('HIGH','MEDIUM'):continue
 cid=e['concept_id'];c=cs[cid];i=c['toc_sequence_position'];candidates=[];seen=set()
 def add(v,via,verdict='kept',reason=None):
  if v['video_id'] in seen:return
  seen.add(v['video_id']);candidates.append({k:v[k] for k in ['video_id','title','channel_id','channel_name','duration_seconds']} | {'youtube_url':'https://www.youtube.com/watch?v='+v['video_id'],'found_via':via,'filter_verdict':verdict,'reason':reason or f'Title and instructional channel suggest a candidate for {focus[i]}. Scope is suitable for introductory BA segment discovery, not whole-video assignment; exact fact coverage and prerequisite leakage remain for transcript judging.'})
 for sid in rs[cid]['reusable_segment_ids']:
  s=segs[sid];f=C/'video_bank/catalogue'/f"{s['video_id']}.json";inputs.append(f);v=load(f);v['channel_name']=ch[v['channel_id']]['channel_name'];add(v,'reused_segment',reason='Approved segment reused by exact concept_id; original source metadata resolves the video. Recheck the cut against this junior BA path\'s facts and prerequisites.')
 for vid in sel.get(str(i),[]):add(cat[vid],'allowlist_catalogue')
 for vid in osel.get(str(i),[]):add(openall[vid],'open_search')
 for vid,reason in rejects.get(i,[]):add(cat[vid],'allowlist_catalogue','rejected',reason)
 if i==75:
  add(openall['eVu2oxqbids'],'open_search','rejected','Masterclass targets design engineers rather than introductory BA functional decomposition.')
 if i==73:
  add(openall['OPP5Elhot0E'],'open_search','rejected','Title concerns gathering requirements, not reviewing already documented requirements in a walkthrough.')
 # Select likely topical drift, never arbitrary ids outside the actual blocked set.
 blocked=[cs[z] for z in c['blocked_knowledge_ids'] if z in cs]
 family=[z for z in blocked if z['concept_family_id']==c['concept_family_id']]
 family.sort(key=lambda z:(z['toc_location']['tile_id']!=c['toc_location']['tile_id'],abs(z['toc_sequence_position']-i)))
 avoid=[z['concept_id'] for z in family[:3]]
 rows.append({'concept_id':cid,'path_id':e['path_id'],'search_brief':{'concept_name':c['concept_name'],'learner_level':next(p['learner_scope'] for p in x['paths'] if p['path_id']==e['path_id']),'required_fact_ids':[f['id'] for f in br[cid]['evidence']['required_facts']],'preferred_visual_modes':e['video_need']['preferred_visual_modes'],'blocked_concepts_to_avoid':avoid},'search_route':'allowlist_then_open_search' if str(i) in ores else 'allowlist_only','candidates':candidates})
inputs=list(dict.fromkeys(inputs));hashes={str(f.relative_to(B)) if f.is_relative_to(B) else str(f):hashlib.sha256(f.read_bytes()).hexdigest() for f in inputs}
meta={'artifact_type':'video_candidates','artifact_version':'1.0.0','schema_version':'1.0.0','batch_id':B.name,'run_id':B.name,'prompt_version':'06_video_candidates@v1','model':'none','generated_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_snapshot_id':B.name,'parent_artifact_hashes':hashes}
out={'metadata':meta,'batch_id':B.name,'searches':rows};dest=B/'video_candidates.part.all.json';dest.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
# Mistakes/self-check: exact batch coverage, no duplicate rows/videos, exact required facts/blocked ids,
# URL derived only from observed id, byte-matched catalogue titles, route honesty, <=5 kept.
expected={(e['concept_id'],e['path_id']) for e in g['entries'] if e['video_need']['level'] in ('HIGH','MEDIUM')}
assert {(e['concept_id'],e['path_id']) for e in rows}==expected and len(rows)==len(expected)
for row in rows:
 cid=row['concept_id'];assert set(row['search_brief']['blocked_concepts_to_avoid'])<=set(cs[cid]['blocked_knowledge_ids'])
 assert row['search_brief']['required_fact_ids']==[f['id'] for f in br[cid]['evidence']['required_facts']]
 assert sum(v['filter_verdict']=='kept' for v in row['candidates'])<=5
 for v in row['candidates']:
  assert re.fullmatch('[A-Za-z0-9_-]{11}',v['video_id']) and v['youtube_url']=='https://www.youtube.com/watch?v='+v['video_id']
  if v['found_via']=='allowlist_catalogue':assert v['title']==cat[v['video_id']]['title']
  if v['found_via']=='open_search':assert v['video_id'] in openall and v['title']==openall[v['video_id']]['title']
print('rows',len(rows),'candidates',sum(len(r['candidates']) for r in rows),'verdicts',collections.Counter(v['filter_verdict'] for r in rows for v in r['candidates']),'routes',collections.Counter(r['search_route'] for r in rows))
print('fewer than 2 kept',[(r['concept_id'],sum(v['filter_verdict']=='kept' for v in r['candidates'])) for r in rows if sum(v['filter_verdict']=='kept' for v in r['candidates'])<2])
