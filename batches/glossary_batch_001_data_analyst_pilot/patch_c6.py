import json

path = "batches/glossary_batch_001_data_analyst_pilot/glossary_bundles_draft.part.c6.json"

with open(path) as f:
    data = json.load(f)

for bundle in data["bundles"]:
    cid = bundle["context"]["concept_id"]

    # BLOCKING fix: capstone.building_dashboard_or_viz
    # blocked_syntax contains concept IDs, not Python syntax — replace with []
    if cid == "capstone.building_dashboard_or_viz":
        pa = bundle.get("practice_anchor", {})
        lc = pa.get("live_code", {})
        if "blocked_syntax" in lc:
            lc["blocked_syntax"] = []
            print(f"[{cid}] Set blocked_syntax to []")

    # ADVISORY fix: capstone.independent_execution
    # Remove the second (duplicate) teaching_notes entry
    if cid == "capstone.independent_execution":
        tn = bundle.get("teaching_notes", [])
        if len(tn) >= 2:
            bundle["teaching_notes"] = [tn[0]]
            print(f"[{cid}] Removed duplicate teaching_notes[1]; kept teaching_notes[0]")

with open(path, "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
    f.write("\n")

print("Patch complete.")
