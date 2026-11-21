from pathlib import Path
import sys,re
p=Path('batches/glossary_batch_learn_python/working/sources')
for query in sys.argv[1:]:
 name,term=query.split(':',1);text=(p/(name+'.txt')).read_text();m=re.search(term,text,re.I)
 print('\n===',name,term,'===\n',text[max(0,m.start()-150):m.start()+1900] if m else 'NOT FOUND')
