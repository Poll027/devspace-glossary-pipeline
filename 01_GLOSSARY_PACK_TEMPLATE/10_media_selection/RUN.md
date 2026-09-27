# 10_media_selection — script, no model

```bash
python3 00_GLOSSARY_PIPELINE_CORE/scripts/select_media.py batches/<batch_id> 00_GLOSSARY_PIPELINE_CORE/video_bank
```

Per concept: LOW/NONE video need → `no_video_needed`. Otherwise, approved segments are ranked by mean judge score, then channel trust tier, then shorter clip, and picked greedily while each adds a required fact not yet covered and doesn't overlap an already-picked cut (max 3). No approved segment → `no_segment_found`, and the concept ships text-only (playbook §30).

The script — never a model — sets `segment_id` (`seg_<concept>_<video>_<start>_<end>`), `youtube_url` and `review_url` from the approved cut.

Gate: `update_ledger.py batches/<batch_id> record 10_media_selection selected_media.json PASS`
