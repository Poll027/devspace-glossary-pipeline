import json, re, sys

path = "batches/glossary_batch_001_data_analyst_pilot/glossary_bundles_draft.part.c5.json"

with open(path, "r", encoding="utf-8") as f:
    text = f.read()

# Fix 2 (ADVISORY -> stakeholder.precise_finding_statement practice_anchor.type):
# Change "type": "free_response" to "type": "external_proof" for the precise_finding_statement bundle
# (free_response is not in the schema enum; external_proof is the closest valid value for a rewriting task)
old2 = '"type": "free_response",\n        "objective": "Rewrite the vague finding'
new2 = '"type": "external_proof",\n        "objective": "Rewrite the vague finding'
assert old2 in text, f"Pattern 2 not found: {old2!r}"
text = text.replace(old2, new2, 1)

with open(path, "w", encoding="utf-8") as f:
    f.write(text)

print("Patch applied successfully.")
