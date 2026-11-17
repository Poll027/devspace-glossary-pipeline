import json,re,hashlib,datetime
from pathlib import Path
ROOT=Path('00_GLOSSARY_PIPELINE_CORE')
B=Path('batches/glossary_batch_aws_devops_engineer')
def load(p): return json.loads(p.read_text())
channels={c['channel_id']:c for c in load(ROOT/'video_bank/channel_allowlist.json')['channels']}
catalog=[]
for p in sorted((ROOT/'video_bank/channel_catalogs').glob('*.json')):
 d=load(p)
 for v in d['videos']:
  catalog.append(dict(v,channel_id=d['channel_id'],channel_name=channels[d['channel_id']]['channel_name']))
if __name__=='__main__':
 for c in channels.values():
  vs=[v for v in catalog if v['channel_id']==c['channel_id'] and re.search(r'cloudformation|terraform|cloudwatch|codepipeline|guardduty|eventbridge|aws cli|disaster recovery|systems manager',v['title'],re.I)]
  if vs:
   print(c['channel_name'],len(vs))
   for v in vs[:45]: print(v['video_id'],v['duration_seconds'],v['title'])
