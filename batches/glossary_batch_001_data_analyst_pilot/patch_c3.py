import json, sys

path = "batches/glossary_batch_001_data_analyst_pilot/glossary_bundles_draft.part.c3.json"

with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

bundles = data["bundles"]

patched = {
    "sql.select_fundamentals": False,
    "sql.null_handling": False,
    "sql.order_by": False,
    "sql.group_by": False,
}

for bundle in bundles:
    cid = bundle["context"]["concept_id"]

    # --- ADVISORY 1 & 2: sql.select_fundamentals bridge_note.after ---
    if cid == "sql.select_fundamentals":
        media = bundle.get("media")
        if media and "bridge_note" in media:
            old_after = media["bridge_note"]["after"]
            # Append the advisory caveat (combining both advisories into one sentence)
            new_after = (
                old_after
                + " The step-through's FROM-first order previews execution order covered later; for now just note that the database reads the table before picking columns."
            )
            media["bridge_note"]["after"] = new_after
            patched["sql.select_fundamentals"] = True

    # --- ADVISORY 3: sql.null_handling assessment_anchors[0] fact_ids ---
    if cid == "sql.null_handling":
        anchors = bundle.get("assessment_anchors", [])
        if anchors and anchors[0].get("capability") == "explain_why_equals_null_never_matches":
            anchors[0]["fact_ids"] = ["f1", "m1"]
            patched["sql.null_handling"] = True

    # --- ADVISORY 4 & 5: sql.order_by practice_anchor.live_code.observable_success ---
    if cid == "sql.order_by":
        pa = bundle.get("practice_anchor", {})
        lc = pa.get("live_code", {})
        if "observable_success" in lc and "grouped" in lc["observable_success"]:
            lc["observable_success"] = (
                "Rows are ordered by the first sort column ascending, and within tied values the second column descends."
            )
            patched["sql.order_by"] = True

    # --- ADVISORY 6: sql.group_by practice_anchor.live_code.starter_state_intent ---
    if cid == "sql.group_by":
        pa = bundle.get("practice_anchor", {})
        lc = pa.get("live_code", {})
        if "starter_state_intent" in lc:
            lc["starter_state_intent"] = (
                "A table with a category column and a numeric column (for example orders with category and sale_amount) is loaded; the editor is empty."
            )
            patched["sql.group_by"] = True

print("Patch results:", patched)

with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=1, ensure_ascii=False)

print("Done.")
