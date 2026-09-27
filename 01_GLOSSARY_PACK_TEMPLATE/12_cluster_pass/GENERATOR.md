# 12_cluster_pass — GENERATOR

Produce `clusters.json` (playbook §24): groups of adjacent concepts that may appear together as clickable sub-concepts in one explanation area. The curriculum is never merged — every concept keeps its own bundle and TOC position.

TOC tiles already group 2–3 related concepts, so each tile is the natural candidate. Within a tile, cluster concepts only when:
- they're adjacent in TOC order, and the learner has every prerequisite for all of them at the tile's start;
- showing them side by side doesn't hide an important boundary (e.g. two join types that learners must learn to tell apart may be better as separate steps);
- they read as parts of one idea — steps of a workflow, variants of one operation.

Clusters never cross tiles and need at least two concepts, listed in TOC order. Not every tile needs a cluster. `reasoning` says why these belong together, or skip the tile.
