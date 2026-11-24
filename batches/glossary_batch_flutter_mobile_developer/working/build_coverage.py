import json, hashlib, re, copy
from datetime import datetime,timezone
from pathlib import Path
P=Path('batches/glossary_batch_flutter_mobile_developer')
cs=json.loads((P/'extracted_concepts.json').read_text())
look=json.loads((P/'registry_lookup.json').read_text())
pack_path=Path(json.loads((P/'source_pack_manifest.json').read_text())['packs'][0]['file'])
source_ids={s['source_id'] for s in json.loads(pack_path.read_text())['sources']}
bank={}; n=None
for line in (P/'working/coverage_bank.txt').read_text().splitlines():
 if not line:continue
 if line.startswith('@'):
  number,ref=line[1:].split(' ',1);n=int(number);bank[n]=[]
 else:
  text,reference=line.rsplit(' || ',1) if ' || ' in line else (line,ref)
  bank[n].append({'statement':text,'source_refs':[reference]})
def replace(i,j,text,refs=None):
 bank[i][j-1]['statement']=text
 if refs:bank[i][j-1]['source_refs']=refs
# Self-check fixes: remove unnecessary or forward-reaching material; make forms and locators precise.
bank[3].pop(4) # Short-circuit detail is not stated on the operator page and is unnecessary for this objective.
replace(2,1,'Analyzer diagnostics identify source problems with a diagnostic name, message, and source location.',['dart_language#tools/diagnostics'])
replace(2,2,"Use the diagnostic's description and documented correction to edit the indicated source, then run `flutter analyze` again to check the correction.",['dart_language#tools/diagnostics','flutter_docs#reference/flutter-cli:flutter-analyze'])
replace(27,3,"Compare `constraints.maxWidth` with the required breakpoint and return the appropriate widget layout from an if/else branch.")
replace(28,2,"Provide layout space for enlarged text; use `Flexible(child: Text(...))` in a bounded Row when text must fit the available width rather than overflow it.",['flutter_docs#ui/accessibility/ui-design-and-styling:Large-fonts','flutter_api#widgets/Row-class.html:Troubleshooting'])
replace(30,3,"Give the interactive control a sufficiently large layout area, for example with `ConstrainedBox(constraints: BoxConstraints(minWidth: requiredWidth, minHeight: requiredHeight), child: control)`.",['flutter_docs#ui/accessibility/ui-design-and-styling:Tap-target-size','flutter_api#widgets/ConstrainedBox-class.html'])
replace(31,2,"Set an item's `key: ValueKey(itemIdentity)` from a stable identity, not its current list position, so reordered stateful children can remain matched to the same items.",['flutter_docs#ui:Keys','flutter_api#foundation/ValueKey-class.html'])
replace(43,2,'Read the reported exception and framework context, then inspect the call stack to locate the application call that caused the failure.',['flutter_devtools#debugger:The-call-stack-and-variable-areas'])
replace(43,3,"Select the first relevant application frame and inspect that frame's source and variables rather than treat a framework reporting frame as the faulty application statement.",['flutter_devtools#debugger:The-call-stack-and-variable-areas'])
for f in bank[52]:f['source_refs']=['flutter_api#implementation:packages/flutter/lib/src/widgets/async.dart:_FutureBuilderState._subscribe']
replace(60,3,"Check that a nullable route parameter is present before converting it; for an integer contract use `int.tryParse(rawValue)` and reject a null parse result before constructing the destination.",['go_router_docs#Configuration:Parameters','dart_language#api.dart.dev/dart-core/int/tryParse.html'])
replace(63,3,'When unsaved changes block dismissal, handle `onPopInvokedWithResult: (didPop, result) async { ... }`, return if didPop is true, and otherwise obtain confirmation before performing an allowed pop.')
replace(65,2,"Evaluate the package's completeness, documentation and API usability, publisher, license, and quality score; a Flutter Favorite designation is not a guarantee of suitability.",['flutter_docs#packages-and-plugins/favorites:Metrics'])
# Variant platforms/setup compatibility is verified through the plugin's own requirements.
bank[65][2]['source_refs']=['permission_handler_docs#Setup']
bank[74].pop(2)
replace(75,3,'SQLite is a local database suitable for large amounts of structured local data, rather than a few simple settings or a file of application-managed contents.',['flutter_persistence#sqlite:Introduction'])
replace(79,2,"Create a table in an openDatabase onCreate callback with `await db.execute('CREATE TABLE tableName (id INTEGER PRIMARY KEY, fieldName TEXT)')`, substituting the schema's names and column types.")
replace(82,1,"Update matching rows with `await db.update(tableName, valuesMap, where: 'id = ?', whereArgs: [id])`; include the fields to change in valuesMap.")
bank[85].append({'statement':'Catch expected SQL failures with `on DatabaseException catch (e)` at the persistence boundary and return or propagate the application-facing failure rather than report success.','source_refs':['sqflite_docs#doc/handling_errors.md:Handling-SQL-error']})
replace(95,1,'Emit a custom analytics event with `await FirebaseAnalytics.instance.logEvent(name: eventName, parameters: parameterMap)`.',['firebase_flutter_analytics#docs/analytics/flutter/events:Log-events'])
replace(95,2,'Event names are case-sensitive; use the same name and prescribed parameter names for repeated occurrences of an interaction.',['firebase_flutter_analytics#docs/analytics/flutter/events:Log-events'])
bank[95].append({'statement':'Custom parameter names must start with a letter, contain only alphanumeric characters and underscores, and be at most 40 characters; supported parameter values include String and num.','source_refs':['firebase_flutter_analytics#docs/analytics/flutter/events:Log-events']})
replace(96,3,'When consent is required, keep analytics collection disabled until it is granted and use `setAnalyticsCollectionEnabled(false)` or `setAnalyticsCollectionEnabled(true)` to control collection as that state changes.',['apple_review_guidelines#5.1.1-Data-Collection-and-Storage','firebase_flutter_analytics#docs/analytics/configure-data-collection:Disable-Analytics-data-collection'])
replace(100,3,"When list rows have a known equal extent, set ListView's `itemExtent` to that extent so the scroll machinery can avoid computing varying child extents.",['flutter_api#widgets/ListView-class.html:Item-extents'])
replace(106,4,"Verify the installed build's core journey on the target device before promoting it to production.")
# Align by the actual extraction order, not an assumed topic list.
old=copy.deepcopy(bank)
def facts(*items):
 return [{'statement':text,'source_refs':refs if isinstance(refs,list) else [refs]} for text,refs in items]
replace(6,4,'Initialize final instance fields at declaration, with initializing formal parameters, or in an initializer list before the constructor body runs.',['dart_language#constructors:Initializer-list'])
# Nullable assertions need no forward instruction in exception handling.
replace(15,5,'The postfix `!` asserts that a value is not null; if it is null the assertion fails at runtime, so handle an uncertain nullable value with a check instead.')
bank[92]=facts(
 ('Address the intended document with `db.collection(collectionPath).doc(documentId)`; keep that reference for both the read and the write.','firebase_flutter_firestore#docs/firestore/query-data/get-data:Get-a-document'),
 ('Await `reference.get()` to obtain a DocumentSnapshot and check for an absent document or absent data before mapping its fields into the edit model.','firebase_flutter_firestore#docs/firestore/query-data/get-data:Get-a-document'),
 ('Write the contract\'s field mapping with `await reference.set(payloadMap)`; an ordinary set creates or overwrites the addressed document.','firebase_flutter_firestore#docs/firestore/manage-data/add-data:Set-a-document'),
 ('For a partial edit that must preserve unspecified fields, use `reference.set(payloadMap, SetOptions(merge: true))` rather than overwrite the whole document.','firebase_flutter_firestore#docs/firestore/manage-data/add-data:Set-a-document'),
 ('Await write completion before report success and keep the selected path and encoded field names consistent between the read and edited payload.','firebase_flutter_firestore#docs/firestore/manage-data/add-data:Set-a-document'))
bank[93]=facts(
 ('Cloud Firestore Security Rules evaluate mobile and web client requests and deny an operation when its access conditions are not satisfied.','firebase_flutter_firestore#docs/rules/basics'),
 ('Catch an expected Firebase failure around the awaited operation with `on FirebaseException catch (e)` and inspect its code to distinguish the documented denied-access outcome.','firebase_flutter_firestore#Flutter-SDK:cloud_firestore/FirebaseException-class.html'),
 ('Translate a denied operation into an application-facing access failure rather than treat it as successful data retrieval or mutation.',['firebase_flutter_firestore#docs/firestore/query-data/get-data:Get-a-document','firebase_flutter_firestore#docs/rules/basics']),
 ('Do not recover by making the rules allow all access: handle the denied operation under the existing policy and obtain authorized access only through the policy\'s permitted conditions.','firebase_flutter_firestore#docs/rules/basics'))
bank[94]=facts(
 ('Observe account transitions from the session stream and apply the retention policy to the previous owner\'s local data rather than assume a new account owns it.',['firebase_flutter_auth#Authentication-state','apple_review_guidelines#5.1.1-Data-Collection-and-Storage']),
 ('Identify the local keys or records assigned to the departing account and separately identify device-wide or other-owner data that the retention policy preserves.',['shared_preferences_docs#Remove-an-entry','sqflite_docs#SQL-helpers:deleteTodo']),
 ('Remove selected preference or secure-storage keys with `remove(key)` or `delete(key: key)`, rather than clear an entire store containing data that must be retained.',['shared_preferences_docs#Remove-an-entry','flutter_secure_storage_docs#Usage']),
 ('For database-backed account data, pass the ownership predicate and bound arguments to `db.delete(tableName, where: ownershipPredicate, whereArgs: ownerValues)` so unrelated records remain.','sqflite_docs#SQL-helpers:deleteTodo'),
 ('Await the policy-directed deletions and verify that the departing account\'s selected data is absent while retained data remains.',['sqflite_docs#SQL-helpers:deleteTodo','shared_preferences_docs#Readme']))
bank[95]=facts(
 ('Subscribe to `FirebaseMessaging.onMessage.listen((RemoteMessage message) { ... })` for messages received while the app is in the foreground.','firebase_flutter_messaging#Foreground-messages'),
 ('Read RemoteMessage.data for the application payload and RemoteMessage.notification for any notification metadata, according to the message contract.','firebase_flutter_messaging#Message-handling'),
 ('Foreground notification messages do not display a visible notification by default on Android or iOS; handle receipt with the specified in-app response instead of assume the system displayed it.','firebase_flutter_messaging#Foreground-and-notification-messages'),
 ('Cancel the owned onMessage subscription when the response owner is disposed.',['firebase_flutter_messaging#Foreground-messages','dart_language#api.dart.dev/dart-async/Stream-class.html']))
bank[96]=old[94]
bank[97]=[old[95][0],old[95][1],old[95][4],old[96][2],old[95][3]]
# Event eligibility itself must be checked, not merely the SDK-wide collection flag.
bank[97].append({'statement':'Check the consent control before invoking logEvent and pass only the consent-approved non-sensitive fields; disabling collection is not a reason to construct an unnecessary personal-data payload.','source_refs':['apple_review_guidelines#5.1.1-Data-Collection-and-Storage','firebase_flutter_analytics#docs/analytics/configure-data-collection']})
bank[98]=[old[97][0],old[97][1],old[98][0],old[98][1],old[98][2],old[98][3]]
bank[99]=facts(
 ('Enable Track Widget Builds in DevTools Performance tracing to show named widget build events in the timeline.','flutter_devtools#performance:Track-widget-builds'),
 ('Trigger the state change once and correlate the resulting subtree build events with the instrumented model notifications or setState call.',['flutter_devtools#performance:Track-widget-builds','flutter_api#widgets/State/setState.html']),
 ('A setState call invalidates its State\'s subtree, while a provider watch subscribes its calling widget to model changes; trace which dependency or ancestor invalidation reaches the unrelated subtree.',['flutter_api#widgets/State/setState.html','provider_docs#Reading-a-value']),
 ('Compare the values actually rendered by the rebuilt subtree with the changed state to identify a rebuild caused by an overly broad dependency rather than a relevant visible-data change.','provider_docs#My-widget-rebuilds-too-often'))
bank[100]=old[99]
# Tie lifetime correction to repeated route-visit/count evidence.
bank[101][1]['statement']='Record the baseline retained-instance or active-subscription count, repeat route entry and exit, and compare snapshots or counts for persistent accumulation after the owner exits.'
bank[101][3]['statement']='Dispose owned disposable resources and cancel owned subscriptions when their lifetime ends, then repeat the same route visits to verify the retained resource count returns to baseline.'
bank[102]=facts(
 ('Set Android defaultConfig.applicationId to the registered application identity; after the app is uploaded to Play Store its applicationId cannot change.','flutter_release_android#Application-ID'),
 ('When changing Android applicationId and namespace, update the MainActivity package declaration and its directory placement to match.','flutter_release_android#Application-ID'),
 ('In Xcode, open the Runner target\'s General settings and set Bundle Identifier to the registered iOS App ID.','flutter_release_ios#Review-Xcode-project-settings'),
 ('Check those identifiers against the intended service and store registrations; a user-facing display name is not the platform application identity.',['flutter_release_android#Application-ID','flutter_release_ios#Review-Xcode-project-settings']))
bank[103]=facts(
 ('Declare a Flutter application version in pubspec.yaml as `version: buildName+buildNumber`; Android maps these to versionName and versionCode.','flutter_release_android#Version-code-and-name'),
 ('Android versionCode is a positive integer that must increase with successive releases, independently of the user-visible versionName; do not reuse a previous Play upload\'s versionCode.','flutter_release_android#developer.android.com/studio/publish/versioning:Version-settings'),
 ('For iOS, build-name maps to CFBundleShortVersionString and build-number to CFBundleVersion.','flutter_release_ios#Update-the-app-build-and-version-numbers'),
 ('App Store Connect associates an uploaded build with the bundle ID and version record and uses the build string to distinguish the build; validate the version-and-build combination under Apple\'s upload rules rather than impose Android\'s globally increasing versionCode rule.','flutter_release_ios#developer.apple.com/help/app-store-connect/manage-builds/upload-builds'),
 ('Apply the intended build values through pubspec.yaml or the `--build-name` and `--build-number` build options and verify the resulting platform values.','flutter_release_ios#Update-the-app-build-and-version-numbers'))
bank[104]=facts(
 ('Check the release against the authoritative policy effective on its intended submission date, including the target platform and whether it is a new app, update, or existing-app availability check.','google_play_publish#answer/11926878:Target-API-level-requirements'),
 ('Google Play target-API requirements distinguish new/update submissions from continued availability of existing apps and include platform-specific exceptions and dated deadlines; compare the candidate\'s target SDK with its applicable row.','google_play_publish#answer/11926878:Target-API-level-requirements'),
 ('Apple publishes dated SDK and toolchain submission requirements; compare the candidate\'s build SDK and Xcode version with the requirement effective for that upload.','apple_review_guidelines#developer.apple.com/news/upcoming-requirements:SDK-minimum-requirements'),
 ('A locally successful build is not evidence that store requirements are satisfied; mark each unmet candidate value against the applicable policy item rather than infer eligibility from the installed toolchain.',['google_play_publish#answer/11926878:Target-API-level-requirements','apple_review_guidelines#developer.apple.com/news/upcoming-requirements:SDK-minimum-requirements']))
bank[105]=old[102]
bank[106]=[old[104][0],old[104][1],old[104][2],old[106][0],old[106][1]]
bank[107]=[old[104][3],old[107][0],old[107][1],old[107][2]]
bank[108]=[old[109][0],old[109][2],old[109][3]]
bank[108].append({'statement':'Prepare the store\'s required listing text and graphic assets in its prescribed languages, counts, dimensions, and formats; check those properties against the current store listing specification.','source_refs':['google_play_publish#answer/9859152:Set-up-your-store-listing','apple_review_guidelines#2.3-Accurate-Metadata']})
bank[109]=old[110]
bank[110]=old[108]
bank[111]=facts(
 ('Complete the release\'s required build, listing, app-content declarations, and release notes, then resolve blocking errors in the store review summary before submitting.','google_play_publish#answer/9859348:Prepare-and-roll-out-a-release'),
 ('Google Play Changes not yet sent for review means changes exist but have not been submitted; send those changes for review through Publishing overview rather than assume upload submitted them.','google_play_publish#Publishing-status'),
 ('In review means the store is reviewing the update, not that it has already been published.','google_play_publish#Publishing-status'),
 ('For App rejected or Update rejected, read the policy issue, correct it and resubmit, or use the supported appeal process.','google_play_publish#Publishing-status'),
 ('Choose the intended testing or production audience and verify the published status and availability; publication timing can be controlled through managed publishing on Google Play.','google_play_publish#App-status-and-Publishing-status'),
 ('Uploading an iOS build to App Store Connect first starts build processing; wait for processing to finish before select the build for its version and submission workflow.','flutter_release_ios#developer.apple.com/help/app-store-connect/manage-builds/upload-builds'))
# Remove nonessential setup of already-supplied scaffolding.
replace(88,1,'Use the target-appropriate Firebase options supplied by the generated firebase_options.dart configuration.',['firebase_flutter#Step-3-Initialize-Firebase-in-your-app'])
bank[37].pop(3)
replace(105,2,'Use the named Android product flavor already present in the project configuration rather than substitute values from another environment.')
replace(105,5,'For iOS, select the corresponding configured Xcode scheme through the Flutter command\'s `--flavor` option.',['flutter_docs#deployment/flavors-ios'])
replace(92,5,'Await write completion before reporting success and keep the selected path and encoded field names consistent between the read and edited payload.')
replace(111,6,'Uploading an iOS build to App Store Connect first starts build processing; wait for processing to finish before selecting the build for its version and submission workflow.')
replace(38,2,'Keep application state and action orchestration in the application layer, exposing the values and callbacks that the view needs.')
replace(38,3,'Place source-specific external access in the data layer and call it through the existing layer boundary rather than put that access in the view.')
bank[54].pop(3)
# Stable objective alignment check retained alongside the generator.
assert {i:cs['concepts'][i]['concept_id'] for i in range(92,112)}=={
 92:'flutter.firestore_documents',93:'flutter.service_access_failures',94:'flutter.local_data_lifetime',95:'flutter.foreground_notifications',96:'flutter.notification_open_navigation',97:'flutter.privacy_aware_analytics',98:'flutter.profile_frame_investigation',99:'flutter.unnecessary_rebuilds',100:'flutter.bounded_rebuild_fix',101:'flutter.resource_lifetime_leaks',102:'flutter.application_identifiers',103:'flutter.release_versioning',104:'flutter.current_release_requirements',105:'flutter.build_environments',106:'flutter.android_signed_bundle',107:'flutter.ios_distribution_build',108:'flutter.store_metadata_assets',109:'flutter.store_privacy_disclosures',110:'flutter.review_readiness',111:'flutter.store_submission'}

status={(x['concept_id'],x['path_id']):x for x in look['lookups']}
briefs=[];owned={}
assert len(bank)==len(cs['concepts'])==112
for i,c in enumerate(cs['concepts']):
 s=status[c['concept_id'],c['path_id']]['canonical_status']
 if s=='new':
  evidence={'concept_id':c['concept_id'],'created_in_batch_id':cs['batch_id'],'used_by_path_ids':[c['path_id']],'required_facts':[dict(id=f'f{j+1}',**f) for j,f in enumerate(bank[i])], 'misconceptions':[], 'optional_enrichment':[]}
 elif s=='shared_in_batch':evidence=copy.deepcopy(owned[c['concept_id']])
 else:raise RuntimeError('unexpected reuse; resolve snapshot evidence')
 owned[c['concept_id']]=evidence
 briefs.append({'concept_id':c['concept_id'],'path_id':c['path_id'],'learning_objective':c['primary_objective'],'canonical_status':s,'evidence':evidence})
inputs=['extracted_concepts.json','registry_lookup.json','concept_evidence_registry_snapshot.json','source_pack_manifest.json']
hashes={n:hashlib.sha256((P/n).read_bytes()).hexdigest() for n in inputs}
# Also hash the manifest-resolved approved pack used to ground the evidence.
hashes[str(pack_path)]=hashlib.sha256(pack_path.read_bytes()).hexdigest()
out={'metadata':{'artifact_type':'coverage_briefs','artifact_version':'1.0.0','schema_version':'1.0.0','batch_id':cs['batch_id'],'run_id':cs['metadata']['run_id'],'prompt_version':'03_coverage_brief@v1','model':'none','generated_at':datetime.now(timezone.utc).isoformat().replace('+00:00','Z'),'source_snapshot_id':cs['metadata']['source_snapshot_id'],'parent_artifact_hashes':hashes},'batch_id':cs['batch_id'],'briefs':briefs}
# Deterministic self-checks.
assert len({(b['concept_id'],b['path_id']) for b in briefs})==len(briefs)
for b,c in zip(briefs,cs['concepts']):
 assert (b['concept_id'],b['path_id'])==(c['concept_id'],c['path_id'])
 fs=b['evidence']['required_facts'];assert fs
 assert [f['id'] for f in fs]==[f'f{i+1}' for i in range(len(fs))]
 assert len({f['statement'] for f in fs})==len(fs)
 for f in fs:
  for r in f['source_refs']:assert '#' in r and r.split('#')[0] in source_ids,r
placeholders=[c['concept_id'] for c in cs['concepts'] if any('small analysis task' in (c.get(k) or '') or 'Given a simple example, correctly identify or apply' in (c.get(k) or '') for k in ['primary_objective','assessment_target','practice_objective'])]
(P/'coverage_briefs.part.all.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print('briefs:',len(briefs),'facts:',sum(len(b['evidence']['required_facts']) for b in briefs),'statuses:',{s:sum(b['canonical_status']==s for b in briefs) for s in {'new','reuse_registry','shared_in_batch'}},'placeholders:',placeholders)
print('tiles:',len({c['toc_location']['tile_id'] for c in cs['concepts']}))
