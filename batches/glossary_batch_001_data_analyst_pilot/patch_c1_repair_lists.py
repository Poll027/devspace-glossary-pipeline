#!/usr/bin/env python3
"""
Repair patch for glossary_bundles_draft.part.c1.json
Findings addressed:
1. python.lists tb6: remove tb6 entirely (len() is not a required fact; fact_ids [] still structural error per evaluator)
2. python.lists media.bridge_note.after: remove mention of len() and counting items
"""
import json, sys

ARTIFACT = "batches/glossary_batch_001_data_analyst_pilot/glossary_bundles_draft.part.c1.json"

with open(ARTIFACT, "r") as f:
    data = json.load(f)

patched = False
for bundle in data["bundles"]:
    if bundle["context"]["concept_id"] != "python.lists":
        continue

    # Fix 1: Remove tb6 from teaching_blocks
    before = len(bundle["teaching_blocks"])
    bundle["teaching_blocks"] = [
        tb for tb in bundle["teaching_blocks"] if tb["id"] != "tb6"
    ]
    after = len(bundle["teaching_blocks"])
    if before != after:
        print(f"Removed tb6 from python.lists teaching_blocks ({before} -> {after} blocks)")
        patched = True
    else:
        print("WARNING: tb6 not found in python.lists teaching_blocks")

    # Fix 2: Update bridge_note.after
    old_after = bundle["media"]["bridge_note"]["after"]
    new_after = (
        "Neither clip shows append(); the text covers adding to the end. "
        "The first clip stops at reading values, and the second shows replacing one."
    )
    if old_after != new_after:
        bundle["media"]["bridge_note"]["after"] = new_after
        print(f"Updated bridge_note.after:\n  OLD: {old_after}\n  NEW: {new_after}")
        patched = True
    else:
        print("bridge_note.after already matches target (no change needed)")

    break

if not patched:
    print("ERROR: No changes made — check concept_id lookup")
    sys.exit(1)

with open(ARTIFACT, "w") as f:
    json.dump(data, f, indent=2)
    f.write("\n")

print("Patch applied successfully.")
