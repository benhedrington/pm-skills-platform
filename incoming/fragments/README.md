# Fragments

Raw knowledge, war stories, templates, and half-formed ideas that arrived through `incoming/` and were classified as fragments.

## What goes here

- Unstructured contributions that are not yet skill-ready
- War stories from retrospectives
- Templates or checklists
- One-pagers on niche topics
- Notes that might enrich an existing skill

## Lifecycle

1. **Intake**: A contribution arrives in `incoming/` (root).
2. **Classification**: The curator runs `/pm-skills-inbox --process` and classifies it as a **fragment**.
3. **Storage**: The file moves here with a dated filename.
4. **Curation**: The curator periodically runs `/pm-skills-curate` to:
   - Turn a fragment into a new skill in `skills/dev/`
   - Fold a fragment into an existing skill
5. **Archive**: Once a fragment is fully absorbed, it moves to `incoming/archive/`.

## Filename convention

`YYYY-MM-DD--topic--author-or-source.md`

Example: `2026-05-10--b2b-pricing-lessons--sarah-chen.md`
