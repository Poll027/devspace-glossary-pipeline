#!/usr/bin/env python3
"""Write batches/<batch>/human_spot_check.md deterministically (no model): the user's after-the-fact review list.

    python3 make_spot_check.py <batch_dir>

Per path (CROSS_ARTIFACT_REVIEW.md step 4): 10 concepts per depth tier (Core, Standard, Reference; all if fewer) that have video,
lowest-scoring first, with ALL their segments; plus every segment with mean_score < 3.5 in its own section. Per segment: concept, label,
clickable review_url, start-end with duration, judge score, full summary. Scores come from selected_media.json (bundles don't carry them).
"""
import json, sys
from pathlib import Path

LOW = 3.5
PER_TIER = 10


def mmss(t):
    h, rem = divmod(int(t), 3600)
    m, s = divmod(rem, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def main(batch_dir):
    d = Path(batch_dir)
    ctx = json.loads((d / "batch_run_context.json").read_text())
    sel = {s["concept_id"]: s for s in json.loads((d / "selected_media.json").read_text())["selections"]}
    out = [f"# Human spot-check list\n\nBatch `{ctx['batch_id']}`. Lowest judge score first. Scores are the segment judge's mean (1-5).\n"]
    for p in ctx["paths"]:
        bundles = json.loads((d / f"path_glossary_bundle.{p['path_id']}.json").read_text())["bundles"]
        rows = []  # (concept, tier, segment dict incl. score)
        text_only = 0
        for b in bundles:
            c = b["context"]["concept_id"]
            if not b["media"]:
                text_only += 1
                continue
            scores = {g["segment_id"]: g.get("mean_score") for g in sel.get(c, {}).get("segments", [])}
            for g in b["media"]["segments"]:
                rows.append((c, b["context"]["depth_tier"], {**g, "score": scores.get(g["segment_id"])}))
        out.append(f"## Path `{p['path_id']}`: {len(bundles)} concepts, {len({r[0] for r in rows})} with video ({len(rows)} segments), {text_only} text-only\n")

        def table(items):
            lines = ["| Score | Concept | Label | Clip (review link) | Summary |", "|---|---|---|---|---|"]
            for c, _, g in items:
                sc = "n/a" if g["score"] is None else f"{g['score']:.2f}"
                dur = g["end_seconds"] - g["start_seconds"]
                lines.append(f"| {sc} | {c} | {g['label']} | [{mmss(g['start_seconds'])}-{mmss(g['end_seconds'])}]({g['review_url']}) ({mmss(dur)}) | {g['summary']} |".replace("\n", " "))
            return "\n".join(lines) + "\n"

        low = sorted((r for r in rows if r[2]["score"] is not None and r[2]["score"] < LOW), key=lambda r: r[2]["score"])
        out.append(f"### Segments scoring below {LOW} ({len(low)})\n")
        out.append(table(low) if low else f"None: every scored segment is {LOW} or higher.\n")
        for tier in ("core", "standard", "reference"):
            by_c = {}
            for r in rows:
                if r[1] == tier:
                    by_c.setdefault(r[0], []).append(r)
            lowest = lambda c: min((x[2]["score"] if x[2]["score"] is not None else 99) for x in by_c[c])
            pick = sorted(by_c, key=lowest)[:PER_TIER]
            out.append(f"### {tier.title()} ({len(pick)} of {len(by_c)} concepts with video; lowest-scoring first)\n")
            out.append(table([r for c in pick for r in sorted(by_c[c], key=lambda x: x[2]["score"] if x[2]["score"] is not None else 99)]))
    (d / "human_spot_check.md").write_text("\n".join(out))
    print(f"wrote {d / 'human_spot_check.md'}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
