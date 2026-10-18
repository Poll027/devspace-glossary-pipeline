#!/usr/bin/env python3
"""Patch script for glossary_bundles_draft.part.c1.json repair round."""
import json, copy, sys

path = "batches/glossary_batch_001_data_analyst_pilot/glossary_bundles_draft.part.c1.json"

with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

bundles = data["bundles"]

# Helper: find bundle by concept_id
def find_bundle(concept_id):
    for b in bundles:
        if b["context"]["concept_id"] == concept_id:
            return b
    raise KeyError(f"Bundle not found: {concept_id}")

# -----------------------------------------------------------------------
# FIX 1 (BLOCKING): python.variables_assignment
# observable_success already says the correct text per the file read
# (line 412 already has the correct text). Let's verify and fix if needed.
# The finding says: change to 'Evaluating the reassigned name shows the new
# value; the other two names still show their original values.'
# Current text: "Printing the reassigned name shows the new value; the other
# two names still show their original values."
# -----------------------------------------------------------------------
b = find_bundle("python.variables_assignment")
pa = b["practice_anchor"]["live_code"]
old_obs = pa["observable_success"]
assert "Printing the reassigned name" in old_obs, f"Unexpected: {old_obs}"
pa["observable_success"] = (
    "Evaluating the reassigned name shows the new value; "
    "the other two names still show their original values."
)
print("FIX 1 applied: python.variables_assignment observable_success")

# -----------------------------------------------------------------------
# FIX 2 (BLOCKING): python.core_data_types
# a) Remove 'using assigned names in an expression, as in the width * height
#    example' from allowed_syntax
# b) Change blocked_syntax entry to '+ - * / // % ** (all arithmetic operators)'
#    without the exception
# -----------------------------------------------------------------------
b = find_bundle("python.core_data_types")
lc = b["practice_anchor"]["live_code"]

# Fix allowed_syntax
lc["allowed_syntax"] = [
    item for item in lc["allowed_syntax"]
    if "width * height" not in item
]
print("FIX 2a applied: python.core_data_types allowed_syntax - removed width*height entry")

# Fix blocked_syntax: replace the entry that mentions the exception
new_blocked = []
for item in lc["blocked_syntax"]:
    if "width * height" in item or (item.startswith("+ -") and "only the single" in item):
        new_blocked.append("+ - * / // % ** (all arithmetic operators)")
    else:
        new_blocked.append(item)
lc["blocked_syntax"] = new_blocked
print("FIX 2b applied: python.core_data_types blocked_syntax - updated arithmetic entry")

# -----------------------------------------------------------------------
# FIX 3 (BLOCKING): python.lists tb6 fact_ids
# Change tb6.fact_ids from ['f6'] to [] since len() is supplementary
# -----------------------------------------------------------------------
b = find_bundle("python.lists")
tb6 = next(tb for tb in b["teaching_blocks"] if tb["id"] == "tb6")
assert tb6["fact_ids"] == ["f6"], f"Unexpected fact_ids: {tb6['fact_ids']}"
tb6["fact_ids"] = []
print("FIX 3 applied: python.lists tb6 fact_ids set to []")

# -----------------------------------------------------------------------
# FIX 4 (BLOCKING): python.dictionaries
# Add f4 and f5 to required_facts
# -----------------------------------------------------------------------
b = find_bundle("python.dictionaries")
rf = b["coverage"]["required_facts"]
existing_ids = {f["id"] for f in rf}
assert "f4" not in existing_ids, "f4 already in required_facts"
assert "f5" not in existing_ids, "f5 already in required_facts"

rf.append({
    "id": "f4",
    "statement": "The get() method returns None or a specified default instead of raising an error when a key is not in the dictionary.",
    "source_refs": ["python_docs_tutorial_datastructures#dictionaries"]
})
rf.append({
    "id": "f5",
    "statement": "The in keyword checks whether a key is present in a dictionary.",
    "source_refs": ["python_docs_tutorial_datastructures#dictionaries"]
})
print("FIX 4 applied: python.dictionaries required_facts - added f4 and f5")

# -----------------------------------------------------------------------
# FIX 5 (ADVISORY): python.for_loops - remove duplicate range() from blocked_syntax
# -----------------------------------------------------------------------
b = find_bundle("python.for_loops")
lc = b["practice_anchor"]["live_code"]
blocked = lc["blocked_syntax"]
# Count occurrences of "range()"
count = blocked.count("range()")
assert count == 2, f"Expected 2 range() entries, found {count}"
# Remove the second occurrence
idx = blocked.index("range()")  # first occurrence
blocked.pop(idx)  # remove first; second becomes first — actually remove last
# Re-check: find last occurrence
blocked2 = lc["blocked_syntax"]
# After removing first, find and remove one more if still duplicate
# Actually let's just deduplicate while preserving order
seen = set()
new_blocked = []
for item in blocked2:
    if item == "range()" and item in seen:
        continue  # skip duplicate
    seen.add(item)
    new_blocked.append(item)
lc["blocked_syntax"] = new_blocked
print("FIX 5 applied: python.for_loops blocked_syntax - removed duplicate range()")

# -----------------------------------------------------------------------
# FIX 6 (ADVISORY): python.while_loops - remove duplicate input() from blocked_syntax
# -----------------------------------------------------------------------
b = find_bundle("python.while_loops")
lc = b["practice_anchor"]["live_code"]
blocked = lc["blocked_syntax"]
count = blocked.count("input()")
assert count == 2, f"Expected 2 input() entries, found {count}"
seen = set()
new_blocked = []
for item in blocked:
    if item == "input()" and item in seen:
        continue
    seen.add(item)
    new_blocked.append(item)
lc["blocked_syntax"] = new_blocked
print("FIX 6 applied: python.while_loops blocked_syntax - removed duplicate input()")

# -----------------------------------------------------------------------
# Write output
# -----------------------------------------------------------------------
with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
    f.write("\n")

print("Done. File written.")
