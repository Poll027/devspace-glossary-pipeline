# Devspace Glossary + YouTube Segment AI Pipeline Playbook — v3

**Status:** Production-ready planning draft — updated with resolved YouTube links, worked teaching-quality benchmark, and explicit IFrame rendering contract  
**Primary goal:** Turn a frozen Devspace TOC into a source-backed teaching knowledge bundle that can later be broken into short, clear, interactive learning screens by the Final Schema.

> **Pack copy note:** this is the pipeline's working copy of the playbook. Two fixes to the §4 example versus the original: the "Share the result" segment no longer overlaps "Analyze" (now 523–612s), and "Analyze" is tagged with a new fact `f4` instead of the cleaning fact `f2`. Four implementation decisions made on top of this playbook are listed in `README.md` → *Decisions on top of the playbook*; where they differ from a section here, the README wins.

This version incorporates the **optimal tile demo** as the learner-experience reference. The demo is not copied literally; it is used to define what information the glossary must prepare in advance so the Final Schema can reproduce the same energy: short explanations, tightly matched video segments, clickable sub-concepts, visible clip lengths, read/transcript alternatives, diagrams/data examples, immediate checks, and hands-on application.

---

# 1. The locked system

The production flow should be:

```text
Frozen TOC
→ Concept Coverage Brief
→ Source Evidence
→ Glossary Pass A
→ YouTube Discovery
→ Segment Selection
→ Glossary + Video Reconciliation
→ Final Glossary Learning Bundle
→ Final Schema
→ Learner Screens
```

The responsibilities are:

```text
TOC
= what must be learned and in what order

Sources
= what is technically trustworthy

Glossary
= what Devspace actually needs to teach

YouTube segments
= selected external explanations/demonstrations that strengthen the teaching

Final Schema
= how the approved information is divided into screens, video states,
  checks, visuals, and practice
```

A weak pipeline would be:

```text
Find a YouTube video
→ pull transcript
→ rewrite transcript into lesson
```

That would make Devspace inherit the creator's:

- omissions;
- terminology;
- pacing;
- teaching order;
- examples;
- prerequisite assumptions;
- and possible mistakes.

The correct rule is:

> **The TOC controls order. Sources control truth. The glossary controls teaching. Video supports the explanation. The Final Schema controls presentation.**

---

# 2. What the optimal tile demo changes

The demo confirms several things that should now be treated as design requirements.

## 2.1 Explanations should be short and layered

The learner should not receive a long article on one screen.

A concept is introduced with:

- a short heading;
- one clear explanation;
- one useful example/visual;
- optional supporting video;
- then a check or application.

The richer glossary can remain detailed internally, but it must be structured into blocks that can be shortened or distributed later.

---

## 2.2 One screen may teach a cluster of closely related ideas

The demo shows an overall concept such as an **analysis workflow**, while related ideas such as:

- start with the question;
- analyze;
- share the result;

can exist as clickable options inside the same learner-facing explanation area.

This means the glossary must support:

```text
Teaching Cluster
├── Sub-concept / idea A
├── Sub-concept / idea B
└── Sub-concept / idea C
```

Each sub-concept may have:

- its own short explanation;
- its own video segment;
- its own timestamp/duration;
- its own read alternative.

The Final Schema still decides whether these are shown together on one screen. The glossary simply needs enough structure to make that possible.

### Important distinction

The curriculum is **not being merged**.

Every Atomic Concept Unit keeps its TOC identity and prerequisite position.

The pipeline may only mark adjacent concepts/sub-concepts as **presentation-compatible** when:

- their TOC order permits it;
- the learner already has the needed prerequisites;
- showing them together does not hide an important conceptual boundary.

---

## 2.3 Video segments should look intentional before play

Before pressing play, the learner should already understand:

- what idea they are about to watch;
- which segment is selected;
- how long the clip is;
- optionally where it occurs inside the full video.

The glossary/video bundle must therefore provide enough data for the Final Schema to show something like:

```text
Watch: Analyze
2m 05s clip

[Video]
```

or:

```text
Analyze
06:12–08:17 · 2m 05s
```

The exact UI is a Final Schema/UI decision.

---

## 2.4 Several segments can be clickable inside one explanation cluster

A learner can switch between related segments without leaving the lesson.

This may be:

- several chapters from the same strong video;
- segments from different strong videos;
- or a mixture of video and Devspace visual explanations.

The production system should therefore support a **media group**.

Example:

```text
Analysis workflow

[Start with the question] [Analyze] [Share the result]

selected segment:
Analyze
05:22–06:54
```

### Updated video rule

The previous rule:

```text
one concept → zero or one primary video
```

is still useful at the **Atomic Concept** level.

But at the **teaching-cluster** level, several atomic concepts/subtopics may each contribute one selected segment and appear as clickable options.

Also, if one excellent long video contains multiple clean chapter boundaries, Devspace should reuse those chapters rather than searching for a different creator unnecessarily.

Do not force one long video across an entire tile, but do not reject continuity when the same creator genuinely has the best segment for several adjacent concepts.

---

## 2.5 Video and Devspace text should be concurrent, not repetitive

The demo works because the written explanation and video feel like parts of one lesson.

The text may:

- introduce the idea;
- establish the exact Devspace terminology;
- explain why it matters;
- tell the learner what to watch for.

The video may then:

- demonstrate it;
- draw it;
- animate it;
- show it in code;
- show it in a tool;
- walk through a real example.

Afterward, Devspace may:

- state the takeaway;
- connect it back to the project;
- fill a gap the video did not cover;
- move directly into a check.

The text should not simply repeat the transcript.

---

## 2.6 A read alternative is necessary

The demo includes a "prefer to read" style alternative. Devspace also wants transcript access.

Every approved video segment should therefore support:

1. **Short segment summary**  
   A concise Devspace-written explanation of the selected segment.

2. **Transcript reference**  
   Time-aligned transcript/caption text where legally/permissibly available.

The Final Schema can decide whether to expose:

```text
Show summary
Show transcript
```

or another interaction.

The transcript should not be required to understand the lesson. It is an alternative/supporting representation.

---

## 2.7 Visuals are broader than illustrations

The demo uses real instructional artifacts:

- dataset/table previews;
- spreadsheet-like data;
- workflow lists;
- reorder interactions;
- field-selection cards;
- realistic examples.

The glossary should therefore identify **what information should be visualized**, not just whether an illustration exists.

Possible visual needs include:

```text
diagram
data_table
spreadsheet
code
UI_state
process_flow
before_after
comparison
formula
chart
annotated_screenshot
```

The Final Schema chooses the actual visual template.

---

## 2.8 Practice should change with the concept

The demo does not rely only on multiple choice.

It includes:

- normal questions;
- ordering a workflow;
- selecting relevant dataset fields;
- working with realistic data.

Devspace will also use:

- live coding;
- spreadsheet editing;
- tool simulations;
- other path-specific interactions.

So the glossary should prepare a **practice anchor**, not generate one universal exercise format.

---

## 2.9 Progress/reward UI is not a glossary responsibility

The demo also contains:

- progress bars;
- coins;
- concept-complete states;
- tile completion;
- next mission;
- reward transitions.

These belong to the Final Schema/runtime experience.

Do **not** pollute the glossary format with those attributes.

---

# 3. What the glossary should actually store

The glossary should be rich enough to drive the Final Schema but not overloaded with UI/runtime information.

The cleanest structure is:

```text
Glossary Learning Bundle
├── Context
├── Coverage
├── Teaching Blocks
├── Media
├── Assessment Anchors
├── Practice Anchor
├── Visual Anchor
├── Teaching Notes
└── Validation
```

That is enough.

---

# 4. Minimal production format

Below is the recommended handoff format.

It deliberately avoids storing dozens of attributes the Final Schema does not need.

```json
{
  "context": {
    "concept_id": "analysis_workflow",
    "concept_name": "The Analysis Workflow",
    "path_id": "data_analyst",
    "level": "beginner",
    "toc_location": {
      "region": "quality_and_analysis",
      "terrain": "analysis_workflow",
      "tile": "quality_and_analysis_workflow"
    },
    "prerequisites": ["data_quality"],
    "blocked_future_concepts": ["advanced_statistics"]
  },

  "coverage": {
    "learning_objective": "Understand that analysis follows a repeatable workflow rather than starting immediately with calculations.",
    "required_facts": [
      {
        "id": "f1",
        "statement": "Analysis begins by defining the question or problem."
      },
      {
        "id": "f2",
        "statement": "Data should be inspected and cleaned before relying on the analysis."
      },
      {
        "id": "f3",
        "statement": "Results must be communicated clearly after analysis."
      },
      {
        "id": "f4",
        "statement": "The analysis step answers the original question using the prepared data."
      }
    ],
    "source_refs": ["source_01", "source_02"]
  },

  "teaching_blocks": [
    {
      "id": "tb1",
      "purpose": "intro",
      "title": "Analysis is a process, not a button",
      "content": "Analysts do not begin by throwing data into a chart. They start with a question and move through a repeatable workflow.",
      "fact_ids": ["f1", "f2", "f3", "f4"]
    },
    {
      "id": "tb2",
      "purpose": "workflow",
      "content": "Ask → Inspect → Clean → Analyze → Visualize → Communicate",
      "fact_ids": ["f1", "f2", "f3", "f4"]
    }
  ],

  "media": {
    "group_title": "See the workflow explained",
    "segments": [
      {
        "label": "Start with the question",
        "video_ref": "vid_analysis_process",
        "video_id": "AbCdEf12345",
        "youtube_url": "https://www.youtube.com/watch?v=AbCdEf12345",
        "review_url": "https://www.youtube.com/watch?v=AbCdEf12345&t=22s",
        "start_seconds": 22,
        "end_seconds": 146,
        "summary": "Shows why an analyst should first define the question being answered.",
        "fact_ids": ["f1"],
        "transcript_ref": "tr_analysis_process_22_146"
      },
      {
        "label": "Analyze",
        "video_ref": "vid_analysis_process",
        "video_id": "AbCdEf12345",
        "youtube_url": "https://www.youtube.com/watch?v=AbCdEf12345",
        "review_url": "https://www.youtube.com/watch?v=AbCdEf12345&t=442s",
        "start_seconds": 442,
        "end_seconds": 523,
        "summary": "Shows the analysis stage after the data has been prepared.",
        "fact_ids": ["f4"],
        "transcript_ref": "tr_analysis_process_442_523"
      },
      {
        "label": "Share the result",
        "video_ref": "vid_analysis_process",
        "video_id": "AbCdEf12345",
        "youtube_url": "https://www.youtube.com/watch?v=AbCdEf12345",
        "review_url": "https://www.youtube.com/watch?v=AbCdEf12345&t=523s",
        "start_seconds": 523,
        "end_seconds": 612,
        "summary": "Shows why findings must be communicated rather than left as calculations.",
        "fact_ids": ["f3"],
        "transcript_ref": "tr_analysis_process_523_612"
      }
    ],
    "bridge_note": "Use Devspace terminology before and after each segment. Do not repeat the creator's explanation word for word."
  },

  "assessment_anchors": [
    {
      "fact_ids": ["f1"],
      "capability": "choose_first_action"
    },
    {
      "fact_ids": ["f2", "f3", "f4"],
      "capability": "order_workflow"
    }
  ],

  "practice_anchor": {
    "type": "ordering",
    "objective": "Put the analysis workflow stages in the correct order.",
    "success": "Learner orders Ask → Inspect → Clean → Analyze → Visualize → Communicate."
  },

  "visual_anchor": {
    "type": "data_table",
    "purpose": "Show a realistic messy dataset that makes inspection and cleaning concrete."
  },

  "teaching_notes": [
    "Keep the explanation short because the video demonstrates the workflow visually.",
    "Do not introduce advanced statistical methods here.",
    "The learner should understand process before tools."
  ],

  "validation": {
    "source_supported": true,
    "prerequisite_safe": true,
    "media_aligned": true,
    "ready_for_final_schema": true
  }
}
```

### YouTube identity and review links are mandatory

Every selected YouTube segment must be **human-reviewable without looking up another database by hand**.

For that reason, the production/review representation of every selected segment must expose:

```text
video_ref
video_id
youtube_url
review_url
start_seconds
end_seconds
```

Where:

- `video_id` is the resolvable YouTube video ID used by the player;
- `youtube_url` opens the original video;
- `review_url` opens the original video at or near the proposed segment start;
- `start_seconds` and `end_seconds` define the approved learner-facing range.

The central Video Catalogue can remain the canonical home for full metadata, but **human QA exports, transcript-generation jobs, and Final Schema handoff data must never contain only an opaque `video_ref`**. A reviewer should be able to click the link immediately and validate the source and proposed cut.

Example:

```json
{
  "video_ref": "vid_python_variables_01",
  "video_id": "AbCdEf12345",
  "youtube_url": "https://www.youtube.com/watch?v=AbCdEf12345",
  "review_url": "https://www.youtube.com/watch?v=AbCdEf12345&t=112s",
  "start_seconds": 112,
  "end_seconds": 248
}
```

The pipeline should derive the URLs deterministically from the returned `video_id`; they should not be manually typed.

### What is intentionally not here

Do not store in the glossary:

- progress bar positions;
- coin rewards;
- button styles;
- screen IDs;
- exact frontend component;
- card radius;
- video-player theme;
- question option text;
- live-editor filenames unless technically required by a practice asset;
- reward animation;
- next-tile UI;
- exact screen count.

Those belong later.

---

# 5. Stage 1 — Take the frozen TOC as law

The glossary pipeline receives the frozen concept and its curriculum boundary.

For each concept, compute:

```text
available_knowledge
=
all completed previous concepts
+
approved inline vocabulary
```

The pipeline must check:

- explanation;
- examples;
- video segments;
- transcript content;
- diagrams;
- assessment anchors;
- practice anchors;

against this boundary.

A future term may be mentioned only as a preview if understanding it is not required.

---

# 6. Stage 2 — Build the Concept Coverage Brief

Before writing the glossary, establish exactly what must be learned.

Example:

```json
{
  "learning_objective": "Learner understands variables as reusable names for values.",
  "required_facts": [
    "A variable associates a name with a value.",
    "A value can be assigned to a variable.",
    "The value can be reused through the variable name.",
    "The variable can later receive another value."
  ],
  "misconceptions": [
    "The variable name and the current value are not the same thing."
  ]
}
```

The Coverage Brief becomes the standard against which:

- sources;
- glossary;
- videos;
- questions;
- practice;

are checked.

---

# 7. Stage 3 — Gather source evidence

Do not perform a completely new research project for every concept.

Use curated source packs for each career family.

Preferred hierarchy:

1. official documentation/specification;
2. trusted educational/reference source;
3. respected practitioner material;
4. educational research where teaching methodology matters.

The pipeline should know which source supports which fact.

At minimum:

```json
{
  "fact_id": "f1",
  "source_refs": ["python_docs_01"]
}
```

Do not merely append a random bibliography to the end.

---

# 8. Stage 4 — Generate Glossary Pass A

Generate structured teaching blocks from:

- TOC context;
- Concept Coverage Brief;
- source evidence;
- path context;
- learner level.

Possible blocks:

```text
intro
definition
mental_model
mechanism
syntax
example
walkthrough
misconception
practical_context
takeaway
```

Not every concept needs every block.

### Depth

Reuse importance/depth information already available from the TOC where possible.

The practical treatment is still:

```text
Core
Standard
Reference
```

but this should not create a second curriculum ranking system.

A Core concept may need:

- deeper explanation;
- worked example;
- video;
- misconception;
- practice.

A Reference concept may only need:

- definition;
- one contextual example.

The goal is **textbook-quality understanding without textbook-length prose everywhere**.

## Worked quality benchmark — what a good explanation should actually read like

The schema above is not enough by itself. The generation agent also needs a concrete reference for the **quality of the actual sentences** it is expected to produce.

Below is an illustrative beginner Data Analyst glossary example for **Data cleaning**.

### Example: Devspace explanation block

> **Data cleaning**
>
> Imagine you have a spreadsheet containing 500 delivery orders. One order appears twice, some rows have no delivery time, and the city column contains `Lagos`, `lagos`, and `LAGOS`.
>
> If you calculate the average delivery time immediately, the result may be misleading. The duplicated order could be counted twice, missing values could remove useful records from the calculation, and the three versions of Lagos could be treated as different locations.
>
> **Data cleaning is the process of finding and fixing problems like these before you rely on the data for analysis.**
>
> Cleaning does not mean making a spreadsheet look neat. It means making the information consistent and trustworthy enough for the question you are trying to answer.
>
> In this dataset, you might remove the duplicated order, investigate the missing delivery time, and standardize `Lagos`, `lagos`, and `LAGOS` into one value. Once those problems are handled, the calculations and charts built from the dataset are much more likely to describe what actually happened.
>
> **Why this matters:** a calculation can be mathematically correct and still lead to the wrong conclusion when the data going into it is unreliable.

### Why this is a good Devspace explanation

It:

- begins with a situation the learner can picture;
- introduces the problem before giving the formal definition;
- defines the concept in plain language;
- uses one continuous example instead of unrelated mini-examples;
- explains the consequence of getting the concept wrong;
- avoids advanced statistics that have not been taught yet;
- gives the Final Schema several natural break points without writing like a slide deck.

The glossary should **not** intentionally write every sentence as a tiny screen fragment. It should produce one coherent teaching chunk of this quality. The Final Schema may later split it.

### How the explanation should match a video segment

Assume the video-discovery pipeline finds this illustrative candidate:

```json
{
  "label": "Spot the problems before analyzing",
  "video_id": "AbCdEf12345",
  "youtube_url": "https://www.youtube.com/watch?v=AbCdEf12345",
  "review_url": "https://www.youtube.com/watch?v=AbCdEf12345&t=134s",
  "start_seconds": 134,
  "end_seconds": 241,
  "fact_ids": ["f_data_clean_1", "f_data_clean_2"],
  "transcript_ref": "tr_AbCdEf12345_134_241"
}
```

The selected segment should **not merely say the exact paragraph above in another voice**.

A good match would be:

```text
Devspace text establishes:
- dirty data can distort an otherwise correct analysis;
- what "data cleaning" means;
- the delivery-order example.

Video demonstrates:
- the creator opening a messy table;
- identifying a duplicate row;
- noticing a blank delivery-time cell;
- normalizing inconsistent city labels;
- showing the cleaned version.

Devspace after-video takeaway:
- cleaning is not cosmetic;
- the goal is trustworthy input for the analysis question.
```

### Example of transcript-to-glossary alignment

The following is an **illustrative transcript note**, not a quotation from a real creator:

```text
02:14–02:37
Creator introduces a delivery-order table and says there are several data-quality problems.

02:38–03:05
Creator identifies a duplicated order and explains that keeping it would count the same event twice.

03:06–03:31
Creator points to blank delivery-time values and inconsistent city labels.

03:32–04:01
Creator fixes the values and compares the cleaned table with the original.
```

The reconciliation agent should map that to the glossary like this:

| Teaching need | Devspace text | Video/transcript | Final action |
|---|---|---|---|
| Define data cleaning | Strong | Partial | Keep Devspace definition |
| Show what dirty data looks like | Some | Strong | Let video demonstrate |
| Duplicate-row consequence | Strong | Strong | Avoid repeating at length after video |
| Missing/inconsistent values | Strong | Strong | Reinforce only as needed |
| Why cleaning matters | Strong | Partial | Keep Devspace takeaway |
| Advanced cleaning methods | Not required | If present later | Stop segment before them |

### Example of the learner-facing synergy the Final Schema could later create

```text
SCREEN / STATE 1
Data cleaning

Imagine your delivery spreadsheet counts one order twice...

[short Devspace explanation]

WATCH
Spot the problems before analyzing
02:14–04:01 · 1m 47s

Prefer to read?
[Show summary] [View transcript]

AFTER VIDEO
The key idea: cleaning is not about making a sheet look tidy.
It is about making the data reliable enough to answer your question.

CHECK
Which problem could cause the same delivery to be counted twice?
```

The glossary does **not** generate that final screen layout. This example exists to prove what the glossary must make possible.

### Writing rule for the generation agent

A strong explanation should usually move through this logic:

```text
concrete situation
→ problem/tension
→ clear definition
→ explanation of what changes or how it works
→ practical example
→ why it matters
→ optional misconception/contrast
```

Do not force this exact order when another structure is clearer, but preserve the underlying qualities:

- understandable;
- concrete;
- accurate;
- prerequisite-safe;
- example-led where useful;
- concise enough to remain focused;
- rich enough that the Final Schema does not need to invent missing teaching.

---

# 9. Stage 5 — Decide whether video helps

Do not search YouTube for every concept.

Classify:

```text
HIGH
MEDIUM
LOW
NONE
```

## HIGH video value

Use video aggressively when understanding benefits from:

- diagrams;
- animation;
- drawing;
- code running;
- changing state;
- workflow demonstrations;
- UI/tool usage;
- before/after;
- spatial/process relationships.

## LOW/NONE

Skip video when:

- a one-paragraph explanation is clearer;
- the concept is minor syntax;
- a simple visual block is enough;
- video would only repeat the text.

The optimal tile demo supports this principle: video is powerful because it is embedded where it adds explanation, not because every screen must contain one.

---

# 10. Stage 6 — Create the YouTube Search Brief

The search agent should receive the exact learning target.

Example:

```json
{
  "concept": "Data cleaning",
  "path": "Data Analyst",
  "level": "beginner",
  "required_facts": ["f1", "f2", "f3"],
  "allowed_knowledge": ["dataset", "rows", "columns"],
  "blocked_knowledge": ["advanced_statistics"],
  "preferred_visual_modes": [
    "spreadsheet_demo",
    "annotated_data_table",
    "diagram"
  ]
}
```

Search for the concept at the correct level and in the correct professional context.

Do not optimize for views/popularity alone.

The discovery stage must return a **resolvable candidate**, not only a title or semantic description.

Every candidate passed to the next stage should include:

```text
video_id
youtube_url
review_url
title
channel
publish_date
duration
reason_for_candidate
```

`youtube_url` should be the normal source URL.

`review_url` should be generated once a candidate start time exists, so manual reviewers can jump directly to the proposed section.

---

# 11. YouTube search prompt

```text
You are Devspace's instructional-video discovery agent.

Find videos likely to contain a clean, self-contained segment for the supplied
Concept Coverage Brief.

Prioritize:
- technical accuracy;
- correct learner level;
- path relevance;
- clear topic boundaries;
- visual explanation;
- diagrams, drawings, annotated code, spreadsheet/tool demos, or animation when useful;
- concise explanation;
- minimal dependence on blocked concepts.

Do not optimize for popularity alone.
Do not assume the whole video will be used.

Return search candidates with:
- `video_id`;
- `youtube_url`;
- title;
- channel;
- publish date;
- duration;
- intended segment purpose;
- reason the video may contain a suitable segment.

Never return a recommendation that cannot be resolved to an actual YouTube source.
```

---

# 12. Stage 7 — Cheap candidate filtering first

Do not run expensive transcript/multimodal analysis on every search result.

First gather basic metadata:

```text
video_id
youtube_url
title
channel
publish_date
duration
language
caption_availability
embed_availability
description
```

As soon as a proposed segment start is known, also derive:

```text
review_url = https://www.youtube.com/watch?v={video_id}&t={start_seconds}s
```

This link is required in every human-review queue so a reviewer can validate the actual source and proposed cut in one click.

Reject cheaply when:

- wrong topic;
- wrong language;
- wrong level;
- clearly obsolete for a version-sensitive concept;
- not embeddable;
- mostly opinion/entertainment;
- obviously assumes advanced knowledge.

---

# 13. Stage 8 — Transcript acquisition

Transcript data is useful for:

- finding topic boundaries;
- checking required-fact coverage;
- generating summaries;
- aligning assessments;
- finding prerequisite leakage.

But do not make the entire product depend on full transcript access.

Every transcript-resolution job should carry the source identity alongside it:

```text
video_id
youtube_url
review_url
proposed_start_seconds
proposed_end_seconds
```

That way, when a transcript or caption result is generated, a human can still open the exact source being transcribed and inspect the cut.

Store:

```text
transcript_ref
video_id
youtube_url
review_url
timestamps
segment summary
fact coverage
```

The transcript system should never return detached text that cannot be traced back to the exact YouTube source and time range.

Store the full transcript only where permitted and necessary.

If no transcript exists:

- the video may still be usable;
- automated confidence decreases;
- stronger visual/human review is required;
- questions should be grounded primarily in the canonical glossary facts.

---

# 14. Stage 9 — Find segment boundaries

The goal is not the best video.

The goal is the best **standalone segment**.

A good segment:

- starts at a new thought;
- preferably follows a chapter/title/transition;
- explains what it is about immediately;
- does not require unresolved earlier context;
- contains one coherent explanation;
- completes its example/thought;
- ends before the next unrelated topic.

Reject/extend a start that begins with:

- "as we said earlier";
- "this is why";
- "now that we have done that";
- unresolved pronouns;
- code whose setup is missing;
- diagrams whose labels were introduced earlier.

Reject/shorten an end that:

- stops before the result;
- cuts off an example;
- moves into another concept;
- introduces an unnecessary advanced section.

---

# 15. Segment duration

The demo reinforces that the learner should know clip length before watching.

Do not use one rigid duration cap.

Prefer the shortest segment that fully serves its role.

Practical targets:

| Role | Typical range |
|---|---:|
| Mental model | 45 sec–3 min |
| Visual mechanism | 1–4 min |
| Worked example | 1.5–5 min |
| Live-code demo | 2–6 min |
| Tool/spreadsheet workflow | 2–6 min |

A longer clip must have a reason.

---

# 16. Video-quality rules

## Hard rejection

Reject if:

- technically wrong according to approved sources;
- requires untaught knowledge;
- only makes sense after watching previous parts;
- materially off-topic;
- cannot be embedded reliably;
- irrelevant content dominates the chosen range.

## Quality dimensions

Judge:

```text
technical accuracy
fact coverage
prerequisite safety
standalone clarity
visual teaching value
clarity/pacing
topic-boundary/editing quality
accessibility/reliability
```

### Visual modes worth identifying

```text
diagram_animation
whiteboard_drawing
annotated_code
live_code
spreadsheet_demo
data_table_demo
annotated_ui
slides_with_signaling
screen_demo
talking_head_with_visual_support
talking_head_only
```

The best visual mode depends on the concept.

---

# 17. Stage 10 — Build the media group

For each concept or presentation-compatible cluster, store only what the Final Schema needs.

```json
{
  "media": {
    "group_title": "See how the workflow works",
    "segments": [
      {
        "label": "Start with the question",
        "video_ref": "video_123",
        "video_id": "AbCdEf12345",
        "youtube_url": "https://www.youtube.com/watch?v=AbCdEf12345",
        "review_url": "https://www.youtube.com/watch?v=AbCdEf12345&t=22s",
        "start_seconds": 22,
        "end_seconds": 146,
        "summary": "Explains why analysis begins with a question.",
        "fact_ids": ["f1"],
        "transcript_ref": "tr_123_22_146"
      }
    ],
    "bridge_note": "Use Devspace terminology around the selected clip."
  }
}
```

### Derivable values should remain derivable

`duration_seconds` can be calculated from:

```text
end_seconds - start_seconds
```

Do not store it redundantly unless the runtime benefits from caching it.

The full external metadata remains in a central Video Catalogue, not the glossary.

However, the Final Glossary Learning Bundle must carry enough **resolved identity** for review and rendering:

```text
video_id
youtube_url
review_url
start_seconds
end_seconds
```

`video_ref` is useful for catalogue relationships, but it must not be the only way to identify the source.

---

# 18. Stage 11 — Reconcile Glossary Pass A with the selected video

Build a simple coverage matrix.

| Fact | Devspace explanation | Video | Action |
|---|---|---|---|
| f1 | Yes | Yes | Text introduces, video demonstrates |
| f2 | Yes | No | Devspace must cover |
| f3 | Yes | Yes | Avoid repeating full explanation |
| f4 | No | No | Cannot publish if required |

Rules:

1. Approved sources beat the video.
2. Do not rewrite correct Devspace terminology just to imitate a creator.
3. If the creator uses a valid synonym, bridge it.
4. If the video explains something visually better, reduce redundant prose.
5. Devspace must fill every required gap.
6. Never leave a required fact uncovered.

---

# 19. The bridge is important

To make several creators feel like one Devspace learning experience, the glossary should carry one small `bridge_note`.

It should tell the Final Schema:

- why the video is being shown;
- what to pay attention to;
- what Devspace should clarify after it.

Example:

```text
Before:
Watch how the creator separates "cleaning" from "analysis."

After:
The important boundary is that cleaning fixes data quality; analysis answers the question.
```

The Final Schema decides the exact wording and placement.

---

# 20. Read summary + transcript

Each media segment should have:

```text
summary
transcript_ref
```

That is enough.

The Final Schema may render:

```text
Prefer to read? Show summary
View transcript
```

The transcript should be:

- scoped to the selected segment;
- time-aligned where possible;
- hidden/collapsed by default if it would make the screen feel heavy.

The short summary should remain readable without the transcript.

For manual QA, the transcript view should always retain:

```text
Source video: youtube_url
Proposed cut: start_seconds → end_seconds
Jump to source: review_url
```

This makes it possible to compare:

```text
Devspace explanation
↔ selected transcript range
↔ actual YouTube playback
```

without guessing which source produced the transcript.

---

# 21. Assessment anchors

The glossary should not write final multiple-choice questions.

It should define what can be tested.

Example:

```json
{
  "assessment_anchors": [
    {
      "fact_ids": ["f1"],
      "capability": "choose_first_action"
    },
    {
      "fact_ids": ["f2", "f3"],
      "capability": "order_steps"
    }
  ]
}
```

The Final Schema later chooses the right template:

```text
multiple choice
multi-select
ordering
matching
prediction
short answer
debug choice
etc.
```

### Traceability rule

Every later question must map back to:

```text
question
→ fact
→ glossary/video teaching evidence
```

If the answer was never taught, reject the question.

---

# 22. Practice anchor

The optimal tile demo shows that practice can be interactive without being code.

The glossary needs only:

```json
{
  "practice_anchor": {
    "type": "field_selection",
    "objective": "Choose only the fields needed to answer the analysis question.",
    "success": "Learner selects customer_segment and delivery_minutes."
  }
}
```

Possible types:

```text
live_code
spreadsheet
field_selection
ordering
matching
tool_simulation
data_cleanup
UI_edit
formula
external_proof
```

For live coding, the glossary may additionally specify:

```text
required skill
allowed syntax
blocked syntax
starter-state intent
observable success
```

The Final Schema/Live Editor generator decides exact files and UI.

---

# 23. Visual anchor

The glossary should tell the Final Schema **what must become visible**.

Example:

```json
{
  "visual_anchor": {
    "type": "data_table",
    "purpose": "Show duplicate IDs and missing values before cleaning."
  }
}
```

This can later map into Devspace's visual-block templates.

---

# 24. Presentation-compatible concept clusters

Because the demo shows several related ideas in one compact explanation area, add a lightweight cluster pass after individual glossary entries are generated.

For adjacent TOC concepts, ask:

```text
Can these be shown inside the same learner-facing explanation cluster
without violating concept order or hiding an important boundary?
```

If yes, generate:

```json
{
  "cluster": {
    "title": "Analysis workflow",
    "concept_ids": [
      "define_question",
      "analyze",
      "communicate_results"
    ],
    "preferred_order": [
      "define_question",
      "analyze",
      "communicate_results"
    ]
  }
}
```

That is all the glossary needs to say.

The Final Schema decides whether this becomes:

- clickable tabs;
- chips;
- stacked cards;
- separate screens.

---

# 25. Source and video reuse without flattening path context

The final output should still be separate career-path glossaries.

Internally:

```text
canonical concept evidence
+
path-specific context
+
TOC position
=
path-specific glossary entry
```

The same approved video segment may be reused across paths only if:

- the concept meaning matches;
- learner level matches;
- prerequisites match;
- the segment does not rely on path-specific context that is wrong for the new path.

The surrounding Devspace text and examples may still differ by path.

---

# 26. Cost control

The expensive version is:

```text
every concept
→ fresh web research
→ huge article
→ 20 videos
→ full transcript analysis
→ full multimodal review
→ questions
→ live exercise
```

Do not do this.

Use gates.

## Gate 1 — cached source packs

Reuse high-quality source sets.

## Gate 2 — variable concept depth

Do not spend Core-level inference on Reference-level concepts.

## Gate 3 — video-need gate

Skip YouTube when video adds little.

## Gate 4 — metadata filter

Cheaply reject poor candidates first.

## Gate 5 — analyze only finalists

Example:

```text
15 metadata candidates
→ 5 transcript candidates
→ 2 strong segment candidates
→ 1 expensive final review
```

Tune numbers after real runs.

## Gate 6 — cache processed videos

Once a video has been processed, store:

- metadata;
- transcript reference;
- topic/chapter boundaries;
- candidate segments;
- previous quality results.

Do not retranscribe/reanalyse it from scratch for another concept.

## Gate 7 — exploit good long videos correctly

If one strong video contains several clean chapter segments that match adjacent TOC concepts:

- process the video once;
- store several approved segment ranges;
- allow the Final Schema to expose them as clickable sub-concepts.

This is both cheaper and more coherent.

## Gate 8 — batch by tile/terrain

Related concepts share:

- source retrieval;
- search context;
- videos;
- path context.

Batching reduces duplicate calls.

---

# 27. End-to-end AI pipeline

```text
FROZEN TOC
   │
   ▼
[Concept Extractor]
   │
   ▼
[Knowledge Boundary Builder]
   │
   ▼
[Concept Coverage Brief]
   │
   ├──────────────► [Source Retriever]
   │                      │
   │                      ▼
   │               [Evidence Map]
   │                      │
   ▼                      ▼
[Glossary Pass A]
   │
   ▼
[Video Need Classifier]
   │
   ├── NONE ──────────────────────────────┐
   │                                      │
   ▼                                      │
[YouTube Search Brief]                    │
   │                                      │
   ▼                                      │
[Candidate Retrieval]                     │
   │                                      │
   ▼                                      │
[Cheap Metadata Filter]                   │
   │                                      │
   ▼                                      │
[Transcript Resolver]                     │
   │                                      │
   ▼                                      │
[Segment Boundary Detector]               │
   │                                      │
   ▼                                      │
[Quality + Prerequisite Judge]             │
   │                                      │
   ▼                                      │
[Winner / No-video Decision]               │
   │                                      │
   └────────────────┬─────────────────────┘
                    ▼
       [Glossary + Video Reconciliation]
                    │
                    ▼
       [Assessment / Practice / Visual Anchors]
                    │
                    ▼
       [Presentation-Compatible Cluster Pass]
                    │
                    ▼
             [Validation Suite]
                    │
                    ▼
        FINAL GLOSSARY LEARNING BUNDLE
                    │
                    ▼
              FINAL SCHEMA
```

---

# 28. Core prompts

## 28.1 Concept Coverage Brief

```text
You are Devspace's Concept Coverage Planner.

Given:
- frozen TOC concept;
- path context;
- learning objective;
- previous concepts;
- direct prerequisites;
- allowed vocabulary;
- blocked future concepts;
- approved evidence;

produce the minimum complete knowledge contract for this concept.

Rules:
- do not add or reorder curriculum;
- separate required facts from optional enrichment;
- stay inside the learner's knowledge boundary;
- identify misconceptions that would damage later learning;
- map factual claims to evidence.

Return:
- learning objective;
- required facts;
- misconceptions;
- source mapping.
```

---

## 28.2 Video discovery

```text
You are Devspace's instructional-video discovery agent.

Given the Concept Coverage Brief, find videos likely to contain a clean,
self-contained segment for this exact learning target.

Prefer:
- accurate explanation;
- correct learner level;
- visual teaching;
- diagrams/drawings/annotated code/spreadsheets/tool demos where relevant;
- clear topic boundaries;
- minimal dependence on blocked concepts.

Do not optimize for views alone.
Do not assume the entire video will be used.
```

---

## 28.3 Segment detector

```text
You are Devspace's Segment Detector.

Given:
- required facts;
- allowed knowledge;
- blocked concepts;
- timestamped transcript or reviewed notes;
- video metadata;

find candidate ranges that can work as standalone mini-lessons.

A valid range:
- starts at a natural thought boundary;
- explains its subject immediately;
- does not require missing earlier context;
- covers the intended fact(s);
- does not rely on blocked concepts;
- finishes the explanation/example before ending.

Return REJECT if no clean segment exists.

Return only:
- label;
- video_id;
- youtube_url;
- review_url;
- start_seconds;
- end_seconds;
- summary;
- covered fact IDs;
- transcript reference;
- issues/rejection reason.

`review_url` must open the same `video_id` at the proposed `start_seconds`.
```

---

## 28.4 Glossary/video reconciliation

```text
You are Devspace's Glossary-Video Reconciliation Agent.

Input:
- Glossary Pass A;
- required facts;
- approved evidence;
- selected video segment(s);
- transcript/segment notes;
- path context.

Produce the final glossary bundle.

Rules:
- approved evidence outranks the video;
- do not imitate the creator's wording unnecessarily;
- reduce text repetition when the video demonstrates the same idea well;
- fill every video gap;
- preserve the learner's prerequisite boundary;
- provide a short summary/transcript reference for every selected segment;
- preserve the exact `video_id`, `youtube_url`, `review_url`, `start_seconds`, and `end_seconds`;
- ensure the written teaching blocks read like coherent, user-friendly teaching prose rather than schema fragments;
- use the worked Data Cleaning benchmark in this playbook as a quality reference;
- create assessment, practice and visual anchors;
- do not generate frontend screens.

Return only the minimal production schema.
```

---

# 29. Validation suite

Before a concept becomes available to the Final Schema, validate:

## Curriculum

- concept exists in frozen TOC;
- TOC order unchanged;
- prerequisites available;
- future-concept leakage absent;
- examples stay within allowed knowledge.

## Sources

- every required fact is supported;
- version-sensitive claims use current sources;
- no unresolved source conflict.

## Teaching

- required facts are actually explained;
- blocks are concise enough to later segment;
- explanation reads as coherent teaching prose, not disconnected bullet fragments;
- a learner can understand the concept from the written explanation without needing the video;
- examples paint a concrete picture where examples are useful;
- the explanation and selected video complement rather than duplicate each other;
- example is valid;
- concept remains focused.

## Video

- `video_id` resolves to the intended YouTube video;
- `youtube_url` opens the original source;
- `review_url` opens the same source at the proposed start time;
- accurate;
- prerequisite-safe;
- segment boundary is coherent;
- timestamps match transcript/notes;
- transcript/notes can be traced to the same video and time range;
- segment is not unnecessarily long;
- transcript/summary aligns;
- embed works;
- terminology conflicts are resolved.

## Handoff

- assessment anchors exist when appropriate;
- practice anchor is achievable with taught/scaffolded knowledge;
- visual anchor exists when useful;
- all required facts are covered;
- `ready_for_final_schema = true`.

---

# 30. Runtime fallback rules

## No good video

Use:

```text
Devspace explanation
+ visual
+ example
+ practice
```

Video is optional.

## Video deleted / embed disabled

Use the written/visual fallback and queue the media for replacement.

## Transcript unavailable

Keep the segment only if manually/multimodally verified.

Do not generate transcript-specific questions.

## Creator uses another valid term

Keep Devspace terminology canonical and bridge the synonym.

## Creator contradicts approved evidence

Reject the segment.

## Segment depends on earlier context

Extend to a clean boundary or choose another segment.

---

# 31. YouTube playback requirement

The selected range should be played inside the lesson using approved start/end timestamps.

The segment record is intentionally compatible with the YouTube IFrame Player API.

The minimum runtime contract is:

```json
{
  "video_id": "AbCdEf12345",
  "start_seconds": 134,
  "end_seconds": 241
}
```

The Final Schema does **not** need to store a finished iframe URL.

The frontend can derive the player request from those fields.

Using the JavaScript IFrame API, the equivalent runtime action is conceptually:

```javascript
player.loadVideoById({
  videoId: segment.video_id,
  startSeconds: segment.start_seconds,
  endSeconds: segment.end_seconds
});
```

A normal embed URL can also be derived when needed:

```text
https://www.youtube.com/embed/{video_id}
  ?start={start_seconds}
  &end={end_seconds}
  &enablejsapi=1
```

The production schema should therefore preserve the **data**, not hard-code one frontend implementation.

### Why the fields are sufficient

From:

```text
video_id
start_seconds
end_seconds
```

the application can render:

- the correct YouTube video;
- the approved starting point;
- the approved ending point;
- the clip duration;
- the clickable chapter/segment state;
- replay of the same segment;
- switching between several segments in one media group.

From:

```text
youtube_url
review_url
```

the team can manually validate the source.

From:

```text
summary
transcript_ref
```

the Final Schema can expose the read/transcript alternative.

That separation is correct:

```text
Glossary
→ stores the approved media facts and relationships

Final Schema
→ decides which media segment appears in which learner state

Frontend player
→ translates video_id + timestamps into YouTube IFrame behavior
```

### Frontend safeguards

The frontend should:

- load at the approved start;
- stop/pause at the approved end;
- monitor current playback time because a learner may manually seek;
- tolerate the start landing near a YouTube keyframe rather than at an exact millisecond;
- optionally expose the full YouTube video separately;
- keep the primary learner flow scoped to the approved segment.

Do not download/rehost the creator's video.

---

# 32. What the Final Schema receives

The Final Schema should not have to research or infer teaching truth.

It receives only:

```text
context
coverage
teaching blocks
media group
  └── video_id + youtube_url + review_url + start/end + summary + transcript_ref
assessment anchors
practice anchor
visual anchor
teaching notes
presentation-compatible cluster refs
validation status
```

From that, it can generate the demo-like experience:

```text
short explanation
→ optional visual/data example
→ clickable video segment(s)
→ summary/transcript alternative
→ concise takeaway
→ check
→ application/live editor
→ progress
```

A media item is **not Final-Schema-ready** unless the Final Schema can receive it and answer all of these without another research call:

```text
Which YouTube video is it?
Can I open the original source?
Can a reviewer jump to the proposed start?
Where does learner playback begin?
Where should learner playback stop?
What is this segment supposed to teach?
Which required facts does it support?
What can the learner read instead?
Which transcript record belongs to this exact cut?
```

---

# 33. What the demo specifically tells us to preserve

The reference flow works because it has the following energy:

- **one clear idea at a time;**
- **very little dead text;**
- **video is inside the explanation rather than a detached resource;**
- **related video chapters are clickable before watching;**
- **the learner can see clip scope/length before committing;**
- **the written explanation and video cover the same learning target;**
- **a read alternative exists;**
- **realistic artifacts such as datasets/tables sit beside abstract explanation;**
- **checks appear immediately after enough teaching has happened;**
- **wrong answers lead to remediation rather than unexplained failure;**
- **practice becomes progressively more realistic;**
- **the flow moves from explain → check → apply instead of dumping theory first.**

The glossary must prepare the **knowledge and media relationships** that make this possible.

The Final Schema remains responsible for turning those relationships into the actual UI.

---

# 34. Rollout plan

## Phase 1 — one frozen path

Run the full pipeline on one completed TOC.

Manually review:

- 10 Core concepts;
- 10 Standard concepts;
- 10 Reference concepts.

Specifically inspect:

- whether the glossary is too long;
- whether video actually adds value;
- whether segment boundaries feel standalone;
- whether summaries and transcripts are useful;
- whether cluster grouping feels natural;
- whether Final Schema can generate the reference flow without inventing information.

## Phase 2 — five paths

Measure:

```text
cost per concept
video-needed rate
no-video rate
accepted-segment rate
average candidates searched
video reuse rate
source reuse rate
transcript availability
human-review rate
prerequisite leakage rate
```

## Phase 3 — scale

Only after thresholds and failure modes are stable should the pipeline continuously process the remaining frozen TOCs.

---

# 35. Final locked rule

```text
TOC
= the learning order

Evidence
= the truth

Glossary
= the teaching bank

Video segment
= the best supporting explanation/demonstration

Transcript/summary
= alternate and grounding representation of that selected segment

Final Schema
= the arrangement engine

Learner experience
= short explanation + strong visual/video + check + application
```

The target is not to produce "articles with YouTube links."

The target is to produce **structured teaching bundles** where:

- the written explanation is good enough to teach the idea clearly on its own;
- every recommended YouTube segment has a resolvable `video_id`, clickable source/review link, and approved timestamps;
- the transcript/summary can be traced back to that exact video cut;
- the written explanation and video complement each other rather than repeat each other;
- every visual, question anchor, and practice anchor teaches or checks the same approved facts at the correct point in the learner's journey.

That is the complete contract the Final Schema needs.

That is what gives the Final Schema enough information to build the compact, fluid experience shown in the reference demo without making the glossary itself bloated or expensive.
