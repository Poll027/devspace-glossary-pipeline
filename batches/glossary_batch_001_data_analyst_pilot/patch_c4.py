import json, sys

path = "batches/glossary_batch_001_data_analyst_pilot/glossary_bundles_draft.part.c4.json"

with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

patched = {"cross_sheet": False, "cond_agg": False}

for bundle in data["bundles"]:
    cid = bundle.get("context", {}).get("concept_id", "")

    # ── PATCH 1 & 2: spreadsheet.cross_sheet_references practice_anchor ──────
    # Advisory: change type from 'matching' to a writing task type ('formula'),
    # update objective and success to match the writing task.
    # 'write' is not a valid schema enum; 'formula' is the correct schema type
    # for a task that requires writing a formula.
    if cid == "spreadsheet.cross_sheet_references":
        pa = bundle.get("practice_anchor", {})
        pa["type"] = "formula"
        pa["objective"] = (
            "Write a formula in cell B2 of a Summary sheet that pulls the value "
            "from cell B4 on a sheet named Q1 Sales."
        )
        pa["success"] = (
            "The learner writes ='Q1 Sales'!B4, correctly quoting the sheet name "
            "because it contains a space."
        )
        bundle["practice_anchor"] = pa
        patched["cross_sheet"] = True

    # ── PATCH 3: spreadsheet.conditional_aggregation bridge_note.before ──────
    # BLOCKING: swap which clip uses text-only vs text+cell-reference criteria
    if cid == "spreadsheet.conditional_aggregation":
        media = bundle.get("media")
        if media and "bridge_note" in media:
            old = media["bridge_note"]["before"]
            expected_fragment = "The first clip uses text and cell-reference criteria"
            if expected_fragment in old:
                media["bridge_note"]["before"] = (
                    "Watch how each argument slot is filled in order. "
                    "The first clip uses text criteria only; the second clip uses both "
                    "text and cell-reference criteria \u2014 no comparison operators like \">32\" appear in either."
                )
                patched["cond_agg"] = True

print("Patch results:", patched)

with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Done.")
