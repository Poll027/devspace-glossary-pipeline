import sys,pathlib
r=pathlib.Path('batches/glossary_batch_learn_python/working/coverage_sources')
for arg in sys.argv[1:]:
 f,s,*sz=arg.split(':');t=(r/(f+'.txt')).read_text();i=t.find('SECTION '+s+'\n');end=t.find('SECTION ',i+8); end=len(t) if end<0 else end
 print('\n=== '+f+'#'+s+' ===\n'+(t[i:min(end,i+int(sz[0] if sz else 1600))] if i>=0 else 'NOT FOUND'))
