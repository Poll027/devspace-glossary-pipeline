exec(open('batches/glossary_batch_flutter_mobile_developer/working/fetch_sources.py').read().split('with concurrent')[0])
items=[('api_'+x,'https://api.flutter.dev/flutter/widgets/'+x+'-class.html') for x in ['State','Widget','StatelessWidget','Row','Column','Expanded','Flexible','Stack','Positioned','ListView','LayoutBuilder','Semantics','PopScope','FutureBuilder']]
items += [('api_canUpdate','https://api.flutter.dev/flutter/widgets/Widget/canUpdate.html'),('api_setState','https://api.flutter.dev/flutter/widgets/State/setState.html'),('api_builder','https://api.flutter.dev/flutter/widgets/ListView/ListView.builder.html'),('api_mounted','https://api.flutter.dev/flutter/widgets/State/mounted.html'),('api_MethodChannel','https://api.flutter.dev/flutter/services/MethodChannel/invokeMethod.html'),('api_Future_timeout','https://api.dart.dev/dart-async/Future/timeout.html'),('api_Stream','https://api.dart.dev/dart-async/Stream-class.html')]
with concurrent.futures.ThreadPoolExecutor(max_workers=14) as ex:
 for a in ex.map(fetch,items):print(*a)
for f in root.glob('api*.html'):
 r=f.read_text();m=re.search(r'<main\b[^>]*>(.*?)</main>',r,re.S)
 if m:r=m.group(1)
 r=re.sub(r'<(script|style).*?</\1>','',r,flags=re.S);r=re.sub(r'</(?:p|div|li|pre|h[1-6]|section|tr)>','\n',r)
 r=html.unescape(re.sub('<[^>]+>','',r));r=re.sub(r'[ \t]+',' ',r);r=re.sub(r'\n\s*\n','\n',r);f.with_suffix('.txt').write_text(r)
