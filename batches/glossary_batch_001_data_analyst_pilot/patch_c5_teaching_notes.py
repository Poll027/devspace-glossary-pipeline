#!/usr/bin/env python3
"""Patch: merge duplicate teaching_notes for viz.seaborn_themes_palettes."""
import json, pathlib

artifact = pathlib.Path(
    "batches/glossary_batch_001_data_analyst_pilot/glossary_bundles_draft.part.c5.json"
)

with artifact.open() as f:
    data = json.load(f)

merged_note = (
    "TOC conflict: the practice_objective says 'apply a seaborn theme to an existing plot', "
    "but set_theme() only changes defaults for plots drawn after the call, not a plot already drawn. "
    "The practice_anchor was adapted so the learner calls set_theme() before the plot function, "
    "matching the taught mechanism; retroactive restyling is not required or implied."
)

patched = 0
for bundle in data["bundles"]:
    if bundle.get("context", {}).get("concept_id") == "viz.seaborn_themes_palettes":
        notes = bundle.get("teaching_notes", [])
        if len(notes) == 2:
            bundle["teaching_notes"] = [merged_note]
            patched += 1
            print(f"Patched bundle: viz.seaborn_themes_palettes — merged {len(notes)} notes into 1")
        else:
            print(f"WARNING: expected 2 teaching_notes, found {len(notes)} — skipping")

if patched == 0:
    raise RuntimeError("No bundle patched — check concept_id lookup")

with artifact.open("w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Done.")
