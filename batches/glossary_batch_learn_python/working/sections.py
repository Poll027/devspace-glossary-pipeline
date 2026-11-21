from pathlib import Path
import sys,re
from html import unescape
p=Path('batches/glossary_batch_learn_python/working/sources')
for query in sys.argv[1:]:
 name,anchor=query.split(':',1);text=(p/(name+'.html')).read_text();m=re.search(r'<[^>]+id="'+re.escape(anchor)+r'"[^>]*>',text)
 if not m:print('MISSING',query);continue
 start=m.start();end=text.find('<section ',m.end());end=min(end if end!=-1 else len(text),start+16000)
 t=text[start:end];t=re.sub('<[^>]+>',' ',t);t=unescape(t);t=re.sub(r'\s+',' ',t)
 print('\n===',query,'===\n',t[:int(__import__('os').environ.get('CAP','2600'))])
