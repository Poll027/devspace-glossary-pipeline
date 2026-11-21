import json,re,pathlib,subprocess,concurrent.futures,urllib.parse
B=pathlib.Path('batches/glossary_batch_learn_python');S=json.load(open(B/'working/curated_selection.json'));G=json.load(open(B/'glossary_pass_a.json'))['entries']
custom={
'variables_assignment':'Python variables assignment beginner tutorial', 'type_conversion':'Python type conversion int float str beginner tutorial',
'floating_point_limits':'Python floating point precision math isclose tutorial','indentation_and_blocks':'Python indentation code blocks beginner tutorial',
'range_iteration':'Python range start stop step tutorial', 'statements_and_expressions':'Python statements expressions assignment tutorial',
'interactive_execution':'Python interactive interpreter REPL beginner tutorial', 'unicode_and_bytes':'Python Unicode str bytes encode decode utf8 tutorial',
'diagnostic_printing':'Python debugging print repr tutorial', 'closures_and_enclosing_scope':'Python closures nonlocal tutorial', 'reading_tracebacks':'Python reading tracebacks beginner tutorial', 'debugger_usage':'Python pdb debugger breakpoint tutorial',
'safe_mutable_defaults':'Python mutable default arguments None tutorial', 'composition':'Python object composition delegation tutorial',
'custom_exceptions':'Python custom exceptions tutorial','object_introspection':'Python type isinstance dir getattr tutorial',
'text_file_encodings':'Python open file encoding utf8 UnicodeDecodeError tutorial', 'binary_files':'Python read write binary files rb wb tutorial',
'datetime_operations':'Python datetime strptime date timedelta tutorial','importable_packages':'Python create package __init__ modules tutorial',
'argparse_command_line':'Python argparse tutorial positional arguments store_true', 'random_vs_secrets':'Python random vs secrets token_hex tutorial',
'unittest_test_cases':'Python unittest TestCase assertRaises tutorial', 'unittest_execution_and_results':'Python unittest discover failures errors tutorial', 'unittest_setup_and_teardown':'Python unittest setUp tearDown addCleanup tutorial',
'read_generated_code':'review understand AI generated Python code tutorial', 'review_generated_file_operations':'review Python file operations overwrite unlink rename safety tutorial',
'verify_generated_api_claims':'verify ChatGPT Python API hallucinations documentation tutorial', 'review_generated_dependencies':'AI generated Python package hallucinations dependency security tutorial', 'accept_repair_or_reject_generated_code':'testing reviewing AI generated Python code safety tutorial'}
needed=[x['concept_id'].split('.')[1] for x in G if x['video_need']['level'] in ('HIGH','MEDIUM') and len(S.get(x['concept_id'].split('.')[1],[]))<2]
def walk(x):
 if isinstance(x,dict):
  if 'videoRenderer' in x:yield x['videoRenderer']
  else:
   for v in x.values():yield from walk(v)
 elif isinstance(x,list):
  for v in x:yield from walk(v)
def txt(x):return x.get('simpleText') or ''.join(t['text'] for t in x.get('runs',[]))
def search(short):
 q=custom[short];url='https://www.youtube.com/results?search_query='+urllib.parse.quote_plus(q)
 dest=B/'working'/('search_'+short+'.html')
 subprocess.run(['curl','-sL','--max-time','35',url,'-o',str(dest)],check=True)
 html=dest.read_text();m=re.search(r'(?:var ytInitialData\s*=|window\["ytInitialData"\]\s*=)\s*',html)
 if not m:return short,{'query':q,'search_url':url,'error':'No parsable search results','results':[]}
 data=json.JSONDecoder().raw_decode(html[m.end():])[0];results=[]
 for v in walk(data):
  try:
   watch=v['navigationEndpoint']['commandMetadata']['webCommandMetadata']['url']
   vid=re.search(r'[?&]v=([\w-]{11})',watch).group(1)
   owner=(v.get('ownerText') or v['longBylineText'])['runs'][0]
   channel_id=owner['navigationEndpoint']['browseEndpoint']['browseId']
   duration=txt(v.get('lengthText',{}));parts=[int(x) for x in duration.split(':')];secs=0
   for x in parts:secs=secs*60+x
   if not duration:continue
   results.append({'video_id':vid,'result_url':'https://www.youtube.com'+watch if watch.startswith('/') else watch,'title':txt(v['title']),'channel_id':channel_id,'channel_name':owner['text'],'duration_seconds':secs})
  except (KeyError,AttributeError,ValueError):continue
  if len(results)>=12:break
 return short,{'query':q,'search_url':url,'results':results}
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:out=dict(ex.map(search,needed))
json.dump(out,open(B/'working/open_search_results.json','w'),indent=2)
for short,d in out.items():
 print('\n'+short)
 for i,v in enumerate(d['results']):print(i,v['video_id'],v['channel_name'],v['duration_seconds'],v['title'])
