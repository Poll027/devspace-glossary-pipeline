from pathlib import Path
import sys
p=Path('batches/glossary_batch_product_manager/working/coverage_sources')
for n in sys.argv[1:]:
 t=(p/(n+'.txt')).read_text()
 if n.startswith('pp_'): t=t.split('\nGlossary\n',1)[-1].split('Your next roadmap starts here.')[0]
 elif n.startswith('atl_'):
  t=t.split('Browse topics',1)[-1];i=t.find('By Atlassian');
  if i>=0:t=t[i+len('By Atlassian'):]
 elif n.startswith('nngroup_'):
  t=t.split('Summary:',1)[-1].split('Related Courses')[0]
 elif n.startswith('pichler_'):
  t=t.split('Roman Pichler',2)[-1]
 print('\n###',n,'\n',t[:7000])
