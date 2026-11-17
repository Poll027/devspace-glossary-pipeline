from discover_video_candidates import *
q=load(B/'open_search_queries.json')
updates={'15':'AWS STS get caller identity boto3 account region tutorial','104':'AWS Backup restore IAM role permissions tutorial','105':'AWS Backup restore testing isolated environment tutorial','106':'AWS Systems Manager automation aws approve tutorial','126':'software incident postmortem SRE tutorial blameless'}
for k,v in updates.items():
 q[k]=v;p=B/'working/video_search'/f'{k}.html';p.rename(p.with_suffix('.first.html'))
(B/'open_search_queries.json').write_text(json.dumps(q,indent=2))
