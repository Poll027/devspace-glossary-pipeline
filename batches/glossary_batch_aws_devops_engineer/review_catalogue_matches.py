from discover_video_candidates import *
g=load(B/'glossary_pass_a.json')['entries']
patterns=load(B/'video_topic_patterns.json')
def reject(v):
 t=v['title'].lower()
 if re.search(r'\[(spanish|japanese|french|german|korean|portuguese)\]|\b(hindi|telugu|tamil)\b',t) or re.search(r'[\u3040-\u30ff\u4e00-\u9fff\u0900-\u097f]',t): return 'Title signals non-English instruction.'
 if re.search(r'\b(new launch|what.s new|newly announced|news|fire destroys|compromising|hacked|keynote|founder|roundtable|future of)\b|aws on.?air',t): return 'News, launch discussion or commentary rather than bounded instruction.'
 if re.search(r'\b(advanced|deep dive|at scale|multi.stage|sophisticated|enterprise|global infrastructure|cop4\d\d|sec4\d\d|dop4\d\d|api4\d\d)\b',t): return 'Title signals advanced material beyond routine entry/junior operations.'
 if re.search(r'\b(azure|google cloud|gcp|mongodb|openai|gemini|bedrock|kiro|mcp|cloudability|terramate|sentinel|opa|atlantis)\b',t): return 'Wrong cloud/tool or specialist scope for this bounded AWS target.'
 return None
def score(v,pattern):
 t=v['title'].lower(); s=0
 m=re.search(pattern,t,re.I)
 # Earlier alternatives are more topic-specific than broad fallback matches.
 for i,p in enumerate(re.split(r'\|(?![^()]*\))',pattern)):
  if re.search(p,t,re.I):s=max(s,35-3*i)
 if re.search(r'beginner|introduction|intro\b|basics|step by step|tutorial|core concepts|overview',t):s+=15
 if re.search(r'learncantrill|be a better dev|devops directive',v['channel_name'],re.I):s+=6
 if 'aws' in t or 'amazon' in t:s+=3
 duration=v.get('duration_seconds') or 0
 if duration>18000:s-=12
 if duration<180:s-=8
 if 'aws events'==v['channel_name'].lower():s-=8
 return s
if __name__=='__main__':
 for ix,e in enumerate(g):
  if e['video_need']['level'] not in ['HIGH','MEDIUM']:continue
  p=patterns[str(ix)]; matches=sorted([v for v in catalog if re.search(p,v['title'],re.I) and not reject(v)],key=lambda v:-score(v,p))
  print('\n',ix,e['concept_id'],'usable',len(matches))
  for v in matches[:4]:print(v['video_id'],v['channel_name'],v['duration_seconds'],v['title'])
