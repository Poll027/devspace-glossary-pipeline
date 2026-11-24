exec(open('batches/glossary_batch_flutter_mobile_developer/working/fetch_sources.py').read().split('with concurrent')[0])
items=[('fd_debugger','https://docs.flutter.dev/tools/devtools/debugger'),('dart_types','https://dart.dev/language/type-system'),('api_pumpAndSettle','https://api.flutter.dev/flutter/flutter_test/WidgetTester/pumpAndSettle.html'),('api_Navigator_push','https://api.flutter.dev/flutter/widgets/Navigator/push.html'),('api_int_tryParse','https://api.dart.dev/dart-core/int/tryParse.html'),('router_started','https://pub.dev/documentation/go_router/latest/topics/Get%20started-topic.html'),('fd_packages','https://docs.flutter.dev/packages-and-plugins/using-packages'),('dart_pub_get','https://dart.dev/tools/pub/cmd/pub-get'),('sqflite_migration','https://raw.githubusercontent.com/tekartik/sqflite/master/sqflite/doc/migration_example.md'),('sqflite_open','https://raw.githubusercontent.com/tekartik/sqflite/master/sqflite/doc/opening_db.md')]
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:
 for a in ex.map(fetch,items):print(*a)
for f in root.glob('*.html'):
 r=f.read_text();m=re.search(r'<main\b[^>]*>(.*?)</main>',r,re.S)
 if m:r=m.group(1)
 r=re.sub(r'<(script|style).*?</\1>','',r,flags=re.S);r=re.sub(r'</(?:p|div|li|pre|h[1-6]|section|tr)>','\n',r)
 r=html.unescape(re.sub('<[^>]+>','',r));r=re.sub(r'[ \t]+',' ',r);r=re.sub(r'\n\s*\n','\n',r);f.with_suffix('.txt').write_text(r)
