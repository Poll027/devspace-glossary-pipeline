exec(open('batches/glossary_batch_flutter_mobile_developer/working/fetch_sources.py').read().split('with concurrent')[0])
items=[('dart_diagnostics','https://dart.dev/tools/diagnostics'),('fd_cli','https://docs.flutter.dev/reference/flutter-cli'),('fd_serialization','https://docs.flutter.dev/data-and-backend/serialization/json'),('async_source','https://raw.githubusercontent.com/flutter/flutter/main/packages/flutter/lib/src/widgets/async.dart'),('api_Future_then','https://api.dart.dev/dart-async/Future/then.html'),('api_List_isEmpty','https://api.dart.dev/dart-core/List/isEmpty.html'),('api_ConstrainedBox','https://api.flutter.dev/flutter/widgets/ConstrainedBox-class.html')]
items += [('router_'+x.lower().replace(' ','_'),'https://pub.dev/documentation/go_router/latest/topics/'+x.replace(' ','%20')+'-topic.html') for x in ['Configuration','Navigation','Redirection','Deep linking','Error handling']]
items += [('firebase_rules','https://firebase.google.com/docs/rules/basics'),('firebase_remove','https://firebase.google.com/docs/firestore/manage-data/delete-data'),('firebase_auth_password','https://firebase.google.com/docs/auth/flutter/password-auth'),('firebase_analytics_collection','https://firebase.google.com/docs/analytics/configure-data-collection?platform=flutter')]
with concurrent.futures.ThreadPoolExecutor(max_workers=12) as ex:
 for a in ex.map(fetch,items):print(*a)
for f in root.glob('*.html'):
 r=f.read_text();m=re.search(r'<main\b[^>]*>(.*?)</main>',r,re.S)
 if m:r=m.group(1)
 r=re.sub(r'<(script|style).*?</\1>','',r,flags=re.S);r=re.sub(r'</(?:p|div|li|pre|h[1-6]|section|tr)>','\n',r)
 r=html.unescape(re.sub('<[^>]+>','',r));r=re.sub(r'[ \t]+',' ',r);r=re.sub(r'\n\s*\n','\n',r);f.with_suffix('.txt').write_text(r)
