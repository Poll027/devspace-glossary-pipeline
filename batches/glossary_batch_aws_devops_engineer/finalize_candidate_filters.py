from discover_video_candidates import *
from fetch_open_video_searches import fetch
cc=load(B/'catalogue_choices.json');oc=load(B/'open_search_choices.json');qs=load(B/'open_search_queries.json');op=load(B/'open_search_results.json')
cc['28']=['Pa-YrTEzxZA'];cc['58']=[]
cc['47']=[];oc['47']=['aUjJSorBE70','fSOwXvZOzRI']
oc['92']=['xThOQuhJ2Pw']
cc['111']=['7xngnjfIlK4']
for k,q in {'28':'AWS security groups inbound outbound rules tutorial beginner','58':'AWS application load balancer listener target group health check tutorial'}.items():
 qs[k]=q;_,op[k]=fetch((k,q))
 print('\n',k)
 for v in op[k][:12]:print(v['video_id'],v['channel_name'],v['duration_seconds'],v['title'])
for name,d in [('catalogue_choices.json',cc),('open_search_choices.json',oc),('open_search_queries.json',qs),('open_search_results.json',op)]:
 (B/name).write_text(json.dumps(d,indent=2))
