import runpy,re
from pathlib import Path
B=Path('batches/glossary_batch_laravel_vue_full_stack_developer');ns=runpy.run_path(str(B/'working/build_coverage.py'));D=B/'working/coverage_sources'
seen=set()
for i,fs in ns['data'].items():
 for ref,text in fs:
  ref=ns['normalize'](ref)
  if ref in seen:continue
  seen.add(ref);root,loc=ref.split('#',1)
  if 'linked' in loc or ' -> ' in loc or root=='php_manual':continue
  if root=='laravel_docs':page,sec=loc.split('/',1);file='laravel_'+page
  elif root=='laravel_eloquent':file='laravel_eloquent';sec=loc
  elif root=='laravel_sanctum':file='laravel_sanctum';sec=loc
  elif root=='laravel_testing':file='laravel_testing';sec=loc
  elif root=='vue_docs':page,sec=loc.rsplit('/',1);file='vue_'+page.replace('/','_')
  elif root=='composer_docs':page,sec=loc.split('/',1);file='composer_'+page
  elif root=='vite_docs':
   page,_,sec=loc.partition('/');file='vite_'+({'getting-started':'guide'}.get(page,page))
   if page=='config':file='vite_server';sec=loc.rsplit('/',1)[-1]
  elif root=='vitest_docs':
   if loc.startswith('api/mock/'):file='vitest_mockapi';sec=loc.split('/')[-1]
   elif loc.startswith('api/vi/'):file='vitest_vi';sec=loc.split('/')[-1]
   else:
    bits=loc.split('/');sec=bits[-1];file='vitest_'+('_'.join(bits[1:-1]) or 'guide')
    if bits[-1]=='functions':file='vitest_functions';sec='mocking-functions'
  elif root=='unused':
   bits=loc.split('/');sec=bits[-1];file='vitest_'+('_'.join(bits[1:-1]) or 'guide')
   if bits[-1]=='functions':file='vitest_functions';sec='mocking-functions'
  elif root=='pinia_docs':
   bits=loc.split('/');sec=bits[-1];file={'introduction':'pinia_introduction.html','getting-started':'pinia_start','core-concepts':'pinia_define'}.get('/'.join(bits[:-1]),'pinia_'+'_'.join(bits[:-1])+'.html')
  elif root=='vue_router_docs':
   bits=loc.split('/');sec=bits[-1];file='router_'+('_'.join(bits[1:-1]) or 'start');file=file.replace('essentials_history-mode','history')
  else:continue
  p=D/(file+'.txt')
  if not p.exists(): print(i,'FILE MISSING',ref,file);continue
  t=p.read_text();ids=re.findall(r'^SECTION ([^ ]*)',t,re.M)
  if sec not in ids:print(i,'LOCATOR MISSING',ref,'; headings',','.join(ids[-30:]))
