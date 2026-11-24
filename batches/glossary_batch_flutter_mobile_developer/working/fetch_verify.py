exec(open('batches/glossary_batch_flutter_mobile_developer/working/fetch_sources.py').read().split('with concurrent')[0])
items=[('fd_flavors_ios','https://docs.flutter.dev/deployment/flavors-ios'),('firebase_analytics_flutter','https://firebase.google.com/docs/analytics/flutter/get-started'),('firebase_analytics_events','https://firebase.google.com/docs/analytics/events?platform=flutter'),('firebase_auth_users','https://firebase.google.com/docs/auth/flutter/manage-users'),('firebase_write','https://firebase.google.com/docs/firestore/manage-data/add-data'),('firebase_read','https://firebase.google.com/docs/firestore/query-data/get-data'),('play_setup','https://support.google.com/googleplay/android-developer/answer/9859152'),('play_release','https://support.google.com/googleplay/android-developer/answer/9859348'),('play_review','https://support.google.com/googleplay/android-developer/answer/9859455'),('play_safety','https://support.google.com/googleplay/android-developer/answer/10787469')]
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:
 for a in ex.map(fetch,items):print(*a)
for f in root.glob('*.html'):
 r=f.read_text();m=re.search(r'<main\b[^>]*>(.*?)</main>',r,re.S)
 if m:r=m.group(1)
 r=re.sub(r'<(script|style).*?</\1>','',r,flags=re.S);r=re.sub(r'</(?:p|div|li|pre|h[1-6]|section|tr)>','\n',r)
 r=html.unescape(re.sub('<[^>]+>','',r));r=re.sub(r'[ \t]+',' ',r);r=re.sub(r'\n\s*\n','\n',r);f.with_suffix('.txt').write_text(r)
