import json, copy

path = "batches/glossary_batch_001_data_analyst_pilot/glossary_bundles_draft.part.c1.json"

with open(path) as f:
    d = json.load(f)

def get_bundle(concept_id):
    for b in d['bundles']:
        if b['context']['concept_id'] == concept_id:
            return b
    raise KeyError(concept_id)

# ── 1. python.variables_assignment ──────────────────────────────────────────
# ADVISORY: Remove the first blocked_syntax entry
# 'division and other operators beyond the single multiplication shown in the width * height example'
# since the explicit operator list already covers it.
b = get_bundle('python.variables_assignment')
bs = b['practice_anchor']['live_code']['blocked_syntax']
target = 'division and other operators beyond the single multiplication shown in the width * height example'
if target in bs:
    bs.remove(target)
    print(f"[1] Removed '{target}' from python.variables_assignment blocked_syntax")
else:
    print(f"[1] WARNING: entry not found: {target!r}")

# ── 2. python.logical_operators ──────────────────────────────────────────────
# ADVISORY: Change starter_state_intent to remove the first-week flag.
# Two findings both point to the same field; apply the more specific wording
# from the second finding (which is also consistent with the first):
#   "A few variables holding delivery minutes and distance, used to derive is_late and is_far boolean values."
# Also adjust objective and success to use only is_late and is_far.
b = get_bundle('python.logical_operators')
lc = b['practice_anchor']['live_code']
old_ssi = lc['starter_state_intent']
new_ssi = "A few variables holding delivery minutes and distance, used to derive is_late and is_far boolean values."
lc['starter_state_intent'] = new_ssi
print(f"[2] starter_state_intent changed from: {old_ssi!r}")
print(f"    to: {new_ssi!r}")

# Adjust objective: remove 'two or three comparisons' / first-week flag reference,
# keep is_late and is_far only.
old_obj = b['practice_anchor']['objective']
new_obj = "Write a rule that combines comparisons with and, or and not and print whether a sample delivery meets it, using is_late and is_far as the condition variables."
b['practice_anchor']['objective'] = new_obj
print(f"[2] objective changed from: {old_obj!r}")
print(f"    to: {new_obj!r}")

# Adjust success: ensure it references is_late/is_far, not a third variable.
old_suc = b['practice_anchor']['success']
new_suc = "The compound expression prints the expected True or False for sample values of is_late and is_far, including a case where the priority of and over or matters."
b['practice_anchor']['success'] = new_suc
print(f"[2] success changed from: {old_suc!r}")
print(f"    to: {new_suc!r}")

# ── 3. python.sets ───────────────────────────────────────────────────────────
# ADVISORY: Update bridge_note.before to note the if-statement is a blocked concept.
b = get_bundle('python.sets')
old_bn = b['media']['bridge_note']['before']
new_bn = ("Watch the duplicates disappear in both clips, then the | and & results on two small sets. "
          "The membership check near the end uses an if-statement the course hasn't covered yet — "
          "focus on the expression 1 in first, which is the membership test.")
b['media']['bridge_note']['before'] = new_bn
print(f"[3] bridge_note.before changed from: {old_bn!r}")
print(f"    to: {new_bn!r}")

# ── 4. python.for_loops ──────────────────────────────────────────────────────
# ADVISORY: Remove the standalone '+=' entry from blocked_syntax,
# keeping only '+= and other augmented assignment'.
b = get_bundle('python.for_loops')
bs = b['practice_anchor']['live_code']['blocked_syntax']
standalone = '+='
if standalone in bs:
    bs.remove(standalone)
    print(f"[4] Removed standalone '{standalone}' from python.for_loops blocked_syntax")
else:
    print(f"[4] WARNING: standalone '+=' not found in blocked_syntax")

# ── Write back ───────────────────────────────────────────────────────────────
with open(path, 'w') as f:
    json.dump(d, f, indent=2, ensure_ascii=False)
    f.write('\n')

print("\nDone. File written.")
