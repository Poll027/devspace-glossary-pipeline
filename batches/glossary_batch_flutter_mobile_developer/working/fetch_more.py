exec(open('batches/glossary_batch_flutter_mobile_developer/working/fetch_sources.py').read().split('with concurrent')[0])
from urllib.parse import urljoin
D='variables operators built-in-types collections loops branches error-handling functions libraries classes constructors'.split()
F='tools/hot-reload tools/diagnostics ui ui/layout/constraints ui/layout cookbook/design/themes ui/assets/assets-and-images tools/devtools/inspector ui/interactivity cookbook/forms/validation ui/adaptive-responsive/general ui/accessibility/ui-design-and-styling ui/accessibility/assistive-technologies ui/accessibility/accessibility-testing data-and-backend/state-mgmt/simple app-architecture/guide cookbook/testing/widget/introduction cookbook/testing/widget/finders cookbook/testing/widget/tap-drag testing/errors cookbook/networking/fetch-data cookbook/networking/send-data cookbook/navigation/navigation-basics cookbook/navigation/passing-data cookbook/navigation/returning-data ui/navigation/deep-linking cookbook/testing/integration/introduction ui/adaptive-responsive/capabilities cookbook/persistence/reading-writing-files cookbook/persistence/sqlite perf/best-practices tools/devtools/performance tools/devtools/memory deployment/flavors'.split()
items=[('dart_'+d,'https://dart.dev/language/'+d) for d in D]+[('fd_'+f.replace('/','_'),'https://docs.flutter.dev/'+f) for f in F]
items += [('dart_null','https://dart.dev/null-safety/understanding-null-safety'),('dart_dependencies','https://dart.dev/tools/pub/dependencies')]
# These page requests are verified on retrieval; unsuccessful pages will not be cited.
with concurrent.futures.ThreadPoolExecutor(max_workers=14) as ex:
 for a in ex.map(fetch,items):print(*a)
# Keep just main content when a main element is available, avoiding navigation.
for f in root.glob('*.html'):
 r=f.read_text(); m=re.search(r'<main\b[^>]*>(.*?)</main>',r,re.S)
 if m:r=m.group(1)
 r=re.sub(r'<(script|style).*?</\1>','',r,flags=re.S);r=re.sub(r'</(?:p|div|li|pre|h[1-6]|section|tr)>','\n',r)
 r=html.unescape(re.sub('<[^>]+>','',r));r=re.sub(r'[ \t]+',' ',r);r=re.sub(r'\n\s*\n','\n',r)
 f.with_suffix('.txt').write_text(r)
