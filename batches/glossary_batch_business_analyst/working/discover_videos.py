import json,glob,re,pathlib,hashlib,datetime,subprocess,concurrent.futures
B=pathlib.Path('batches/glossary_batch_business_analyst'); CORE=pathlib.Path('00_GLOSSARY_PIPELINE_CORE')
load=lambda p:json.loads(pathlib.Path(p).read_text())
g=load(B/'glossary_pass_a.json');x=load(B/'extracted_concepts.json');r=load(B/'registry_lookup.json');briefs=load(B/'coverage_briefs.json')
channels={c['channel_id']:c for c in load(CORE/'video_bank/channel_allowlist.json')['channels']}
cat={}
for f in sorted((CORE/'video_bank/channel_catalogs').glob('*.json')):
 d=load(f)
 for v in d['videos']:
  cat[v['video_id']]={**v,'channel_id':d['channel_id'],'channel_name':channels.get(d['channel_id'],{}).get('channel_name',d.get('channel_name',''))}
# Topic-specific title queries, in TOC order. All catalogues searched for every topic.
patterns={
2:r'facilitat|requirements workshop',5:r'contextual inquiry|job shadow|observation.*(technique|requirement|research)|user research.*observ',7:r'wirefram|low.fidelity prototyp',9:r'focus group',10:r'risk (matrix|identification|assessment)|probability.*impact',15:r'traceability|traceability matrix',16:r'requirements life.?cycle|confluence.*(history|version|requirement)',19:r'(stakeholder|power|influence).*(interest|matrix)|interest.*matrix',20:r'\braci\b',22:r'facilitat|meeting.*(effective|workshop)',23:r'conflict resolution|consensus building',24:r'\bbpmn\b',25:r'as.is.*process|current.state.*process|\bbpmn\b',26:r'to.be.*process|future.state.*process|\bbpmn\b',27:r'bottleneck|process.*gap',28:r'process improvement|lean.*(process|six sigma)|value stream',30:r'decision table',31:r'decision tree',33:r'primary key',34:r'foreign key|referential integrity',35:r'one.to.many|database.*relationship',36:r'many.to.many|junction table',37:r'cardinality|database.*relationship|entity.relationship',38:r'entity.relationship|\berd\b',43:r'inner join|sql.*joins',44:r'group by|sql.*aggregation',45:r'\bhaving\b|sql.*where',46:r'sql.*(null|data type)|null.*sql',47:r'left.*join|sql.*joins',48:r'right.*join|sql.*joins',49:r'full.*join|sql.*joins',50:r'order by|sql.*sorting',51:r'sql.*(report|business|group by|aggregation)',52:r'power (bi|query).*(import|transform|clean|beginner)|power query.*(tutorial|excel)',53:r'tableau.*(connect|data source|join|union|beginner)',59:r'\bkano\b',60:r'weighted.*(scor|decision)|decision matrix',61:r'decision matrix|solution.*evaluat|option.*evaluat',62:r'business case',63:r'multi.criteria|decision matrix|weighted.*decision',64:r'mean.*median|measures of cent|mean median mode',65:r'standard deviation|variance|interquartile|measures of (spread|dispersion)',68:r'phased.*(delivery|release)|release planning|story mapping',72:r'stakeholder.*present|presentation.*(business|effective)|powerpoint.*(present|story)',73:r'requirements walkthrough|requirements.*demo',74:r'context diagram|scope model',75:r'functional decomposition',76:r'excel.*(reference|basic formula)|relative.*absolute|mixed reference',77:r'pivot.?table',78:r'vlookup|xlookup|index.*match',79:r'excel.*(\bif\b|\bifs\b|conditional)|nested if',80:r'excel.*(chart|graph)|chart.*excel',81:r'pivot.?table|excel.*report',85:r'sprint review',87:r'five why|5 why|5.whys',88:r'fishbone|ishikawa',90:r'star schema|dimensional model',91:r'power bi.*relationship|relationship.*power bi',92:r'power bi.*(dashboard|report|visual)',93:r'tableau.*dashboard',95:r'power bi.*(publish|shar|permission)',96:r'\bdax\b|power bi.*(measure|calculated column)',97:r'tableau.*calculat',98:r'semantic (layer|model)|power bi.*dataset|power bi.*build permission'}
concepts={c['concept_id']:c for c in x['concepts']}; needs=[e for e in g['entries'] if e['video_need']['level'] in ['HIGH','MEDIUM']]
# Rejection is based solely on obvious title/channel mismatch, never transcript assumptions.
def reject(v,c):
 t=v['title'].lower();idx=c['toc_sequence_position']
 if re.search(r'\b(news|reaction|roast|rant)\b|changed everything|is dead|shocking|i quit|millionaire|founder|startup advice',t):return 'Title signals news, opinion, entertainment, or founder advice rather than instruction.'
 if re.search(r'advanced|masterclass|\blstm\b|\brandom forest\b|\bxgboost\b|\bcart\b|machine learning|classification|\bpython\b|scikit|\bspark\b',t) and idx not in [96]:return 'Title signals advanced programming/statistical material outside this junior BA learning target.'
 if idx==31 and re.search(r'regression|classifier|entropy|information gain|gini|\bid3\b',t):return 'Predictive-model decision trees are outside the business-rule decision-tree target.'
 if idx in [52,53,91,92,93,95,96,97,98] and re.search(r'\b201[0-8]\b',t):return 'Title explicitly identifies an obsolete version for this version-sensitive BI workflow.'
 return None
short={}
for e in needs:
 c=concepts[e['concept_id']];idx=c['toc_sequence_position'];vs=[v for v in cat.values() if re.search(patterns[idx],v['title'],re.I)]
 def rank(v):
  t=v['title'].lower();return (reject(v,c) is not None, not bool(re.search(r'beginner|basic|introduction|explained|tutorial',t)),v['duration_seconds'] is None, v['duration_seconds'] or 99999)
 vs.sort(key=rank);short[str(idx)]=vs[:12]
(B/'working/catalog_shortlists.json').write_text(json.dumps(short,indent=2))
for e in needs:
 c=concepts[e['concept_id']];idx=c['toc_sequence_position'];print('\n',idx,c['concept_name'])
 for v in short[str(idx)][:6]:print(v['video_id'],v['channel_name'],v['duration_seconds'],v['title'], 'REJECT:'+str(reject(v,c)) if reject(v,c) else '')
