#!/usr/bin/env python3
"""
Patch script for glossary_bundles_draft.part.c2.json repair round.

Changes:
1. BLOCKING: In pandas.melt_reshaping practice_anchor.live_code.blocked_syntax,
   remove "df.groupby" (groupby is in allowed_prior_concepts, so it must not be blocked).
2. ADVISORY: In stats.outlier_reasoning assessment_anchors,
   rename capability "decide_keep_investigate_or_exclude"
   to "decide_and_explain_outlier_handling" to match the assessment_target's
   'propose a plausible explanation' requirement.
"""

import json, sys

path = "batches/glossary_batch_001_data_analyst_pilot/glossary_bundles_draft.part.c2.json"

with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

changes = 0

for bundle in data["bundles"]:
    concept_id = bundle.get("context", {}).get("concept_id", "")

    # --- FIX 1 (BLOCKING): pandas.melt_reshaping blocked_syntax ---
    if concept_id == "pandas.melt_reshaping":
        pa = bundle.get("practice_anchor", {})
        lc = pa.get("live_code", {})
        blocked = lc.get("blocked_syntax", [])
        if "df.groupby" in blocked:
            blocked.remove("df.groupby")
            lc["blocked_syntax"] = blocked
            pa["live_code"] = lc
            bundle["practice_anchor"] = pa
            print("FIX 1 applied: removed 'df.groupby' from pandas.melt_reshaping blocked_syntax")
            changes += 1

    # --- FIX 2 (ADVISORY): stats.outlier_reasoning assessment_anchors ---
    if concept_id == "stats.outlier_reasoning":
        anchors = bundle.get("assessment_anchors", [])
        for anchor in anchors:
            if anchor.get("capability") == "decide_keep_investigate_or_exclude":
                anchor["capability"] = "decide_and_explain_outlier_handling"
                print("FIX 2 applied: renamed capability to 'decide_and_explain_outlier_handling' in stats.outlier_reasoning")
                changes += 1

print(f"\nTotal changes applied: {changes}")

with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("File written successfully.")
