import concurrent.futures
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess

root = Path.cwd()
batch = root / 'batches/glossary_batch_flutter_mobile_developer'
context_file = batch / 'batch_run_context.json'
context = json.loads(context_file.read_text())
workspace = Path(context['paths'][0]['toc_workspace'])
seed = json.loads((workspace / 'source_registry_snapshot.json').read_text())
exclude = {'onet_software_developers', 'flutter_junior_postings'}
sources = [dict(source_id=s['source_id'], title=s['name'], source_type='official_docs', url_or_citation=s['url_or_citation'], trust_tier='technical_truth') for s in seed['sources'] if s['source_id'] not in exclude]
extra = [
 ('dart_async', 'Asynchronous programming: futures, async, await', 'https://dart.dev/libraries/async/async-await'),
 ('dart_io', 'dart:io library', 'https://api.dart.dev/dart-io/'),
 ('flutter_api', 'Flutter API documentation', 'https://api.flutter.dev/'),
 ('flutter_networking', 'Networking recipes', 'https://docs.flutter.dev/cookbook/networking'),
 ('flutter_persistence', 'Persistence recipes', 'https://docs.flutter.dev/cookbook/persistence'),
 ('flutter_navigation', 'Navigation and routing', 'https://docs.flutter.dev/ui/navigation'),
 ('flutter_accessibility', 'Accessibility', 'https://docs.flutter.dev/ui/accessibility-and-internationalization/accessibility'),
 ('flutter_performance', 'Performance', 'https://docs.flutter.dev/perf'),
 ('flutter_devtools', 'Flutter DevTools', 'https://docs.flutter.dev/tools/devtools'),
 ('provider_docs', 'provider package documentation', 'https://pub.dev/packages/provider'),
 ('go_router_docs', 'go_router package documentation', 'https://pub.dev/packages/go_router'),
 ('shared_preferences_docs', 'shared_preferences package documentation', 'https://pub.dev/packages/shared_preferences'),
 ('sqflite_docs', 'sqflite package documentation', 'https://pub.dev/packages/sqflite'),
 ('permission_handler_docs', 'permission_handler package documentation', 'https://pub.dev/packages/permission_handler'),
 ('flutter_secure_storage_docs', 'flutter_secure_storage package documentation', 'https://pub.dev/packages/flutter_secure_storage'),
 ('firebase_flutter_auth', 'Firebase Authentication for Flutter', 'https://firebase.google.com/docs/auth/flutter/start'),
 ('firebase_flutter_firestore', 'Get started with Cloud Firestore', 'https://firebase.google.com/docs/firestore/quickstart'),
 ('firebase_flutter_messaging', 'Receive messages in a Flutter app', 'https://firebase.google.com/docs/cloud-messaging/flutter/receive'),
 ('firebase_flutter_analytics', 'Get started with Google Analytics', 'https://firebase.google.com/docs/analytics/get-started?platform=flutter'),
]
sources.extend(dict(source_id=i, title=t, source_type='official_docs', url_or_citation=u, trust_tier='technical_truth') for i,t,u in extra)

def verify(s):
    result = subprocess.run(['curl', '-sS', '-L', '--max-time', '60', '--retry', '1', '-w', '\n%{http_code}\n%{url_effective}', s['url_or_citation']], capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(f"{s['source_id']}: {result.stderr}")
    body, code, final = result.stdout.rsplit('\n', 2)
    if code != '200' or len(body) < 100:
        raise RuntimeError(f"{s['source_id']}: HTTP {code}, body length {len(body)}")
    title = re.search(r'<title[^>]*>(.*?)</title>', body, re.I | re.S)
    report = {'source_id': s['source_id'], 'url': s['url_or_citation'], 'http_status': int(code), 'final_url': final, 'page_title': re.sub(r'\s+', ' ', title.group(1)).strip() if title else None, 'response_bytes': len(body.encode())}
    print(json.dumps(report), flush=True)
    return report

with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
    checks = list(pool.map(verify, sources))
(batch / 'working/source_url_verification.json').write_text(json.dumps(checks, indent=2) + '\n')
pack_file = root / '00_GLOSSARY_PIPELINE_CORE/source_packs/flutter_mobile_developer.source_pack.json'
if pack_file.exists():
    raise RuntimeError('Refusing to overwrite existing pack')
pack_file.parent.mkdir(parents=True, exist_ok=True)
pack_file.write_text(json.dumps({'career_family_id': context['career_family_id'], 'sources': sources}, indent=2) + '\n')
subprocess.run(['python3', '00_GLOSSARY_PIPELINE_CORE/scripts/schema_check.py', 'source_pack.schema.json', str(pack_file)], check=True)
manifest = {'batch_id': context['batch_id'], 'packs': [{'career_family_id': context['career_family_id'], 'file': str(pack_file.relative_to(root)), 'source_count': len(sources)}]}
(batch / 'source_pack_manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
for live, snapshot in [('00_GLOSSARY_PIPELINE_CORE/registry/concept_evidence_registry.json', 'concept_evidence_registry_snapshot.json'), ('00_GLOSSARY_PIPELINE_CORE/video_bank/approved_segments.json', 'approved_segments_snapshot.json')]:
    shutil.copyfile(root / live, batch / snapshot)
    a = hashlib.sha256((root / live).read_bytes()).hexdigest()
    b = hashlib.sha256((batch / snapshot).read_bytes()).hexdigest()
    assert a == b
    print(f'{snapshot}: live SHA-256={a}; snapshot SHA-256={b}; MATCH')
# Findings concern missing referenced files, not the context's contents. Patch only
# the named snapshot reference if necessary, preserving all other text and fields.
expected = 'concept_evidence_registry_snapshot.json'
if context['registry_snapshot_ref'] != expected:
    original = context_file.read_text()
    patched = re.sub(r'("registry_snapshot_ref"\s*:\s*)"[^"]*"', lambda m: m.group(1) + json.dumps(expected), original, count=1)
    context_file.write_text(patched)
print('Source count:', len(sources))
