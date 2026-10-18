"""
Patch: merge the two assessment_anchors for stats.outlier_reasoning
  - 'decide_and_explain_outlier_handling' (f2, f3)
  - 'recognize_genuine_outlier' (m1)
into a single anchor that explicitly covers the unified capability of
proposing a plausible explanation for each outlier (matching the
assessment_target: 'identify which specific values are outliers and
propose a plausible explanation for each').

The 'identify_outlier' anchor (f1) is left unchanged.
"""

import json, sys

ARTIFACT = "batches/glossary_batch_001_data_analyst_pilot/glossary_bundles_draft.part.c2.json"

with open(ARTIFACT, encoding="utf-8") as fh:
    data = json.load(fh)

patched = False
for bundle in data["bundles"]:
    if bundle.get("context", {}).get("concept_id") != "stats.outlier_reasoning":
        continue

    old_anchors = bundle["assessment_anchors"]

    # Verify the expected structure is present before patching
    caps = {a["capability"] for a in old_anchors}
    assert "decide_and_explain_outlier_handling" in caps, "anchor not found"
    assert "recognize_genuine_outlier" in caps, "anchor not found"

    # Build the merged anchor: fact_ids = f2 + f3 + m1 (union, preserving order)
    merged_fact_ids = ["f2", "f3", "m1"]

    new_anchors = []
    for a in old_anchors:
        if a["capability"] == "decide_and_explain_outlier_handling":
            # Replace with merged anchor
            new_anchors.append({
                "fact_ids": merged_fact_ids,
                "capability": "explain_and_decide_outlier_handling"
            })
        elif a["capability"] == "recognize_genuine_outlier":
            # Drop — absorbed into the merged anchor above
            pass
        else:
            new_anchors.append(a)

    bundle["assessment_anchors"] = new_anchors
    patched = True
    print(f"Patched assessment_anchors for stats.outlier_reasoning: "
          f"{[a['capability'] for a in new_anchors]}")
    break

assert patched, "stats.outlier_reasoning bundle not found — nothing patched"

with open(ARTIFACT, "w", encoding="utf-8") as fh:
    json.dump(data, fh, indent=2, ensure_ascii=False)

print("Done.")
