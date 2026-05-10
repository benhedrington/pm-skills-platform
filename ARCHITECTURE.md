# PM Skills Platform — Architecture

## Core Concepts

### Skill
An atomic, versioned unit of knowledge. Always a markdown file with YAML frontmatter.

**Filesystem path:** `skills/{dev,stage,live}/{skill-name}.md`

- `dev/`: Work in progress. Anyone can write here.
- `stage/`: Reviewed and tested. Ready for curation.
- `live/`: Published and available to packs. The only directory packs reference.
- Deprecated skills stay in `live/` with `deprecated: true` in frontmatter.

### Pack
An unversioned manifest that lists skill names. Always floats to latest `live/`.

**Filesystem path:** `packs/{pack-name}.md`

Curated centrally by the packager. Packs are segmented by constituency (e.g., `junior-pm-core`, `b2b-saas-growth`).

### Fragment
Raw knowledge, war stories, templates, or half-formed ideas that are not yet structured skills.

**Filesystem path:** `incoming/fragments/YYYY-MM-DD--topic--source.md`

Fragments arrive through `incoming/` and are classified by the curator. They are reviewed periodically and either:
- Turned into new skills in `skills/dev/`
- Folded into existing skills as enriched examples or anti-patterns

### Gold Repo
The upstream source of truth. Enterprises sync from it. Local team contributions flow back to it.

---

## Directory Structure

```
pm-skills-platform/
├── .claude/commands/          ← Claude Code slash commands
├── skills/
│   ├── dev/                   ← Drafts and contributed work
│   ├── stage/                 ← Reviewed
│   └── live/                  ← Published (share this folder)
├── packs/                     ← Curated manifests
├── incoming/                  ← Contribution drop zone
│   ├── fragments/             ← Classified raw material
│   ├── archive/               ← Processed originals
│   └── rejected/              ← Declined with reasons
├── scripts/                   ← Mechanical helpers
├── templates/                   ← Starters
├── ARCHITECTURE.md
└── README.md
```

## Skill Schema

```yaml
---
id: user-story-writing              # unique kebab-case identifier
name: User Story Writing             # human-readable title
version: 2.3.1                       # semver
deprecated: false                    # optional; true keeps file in live but flags it
category: foundational               # broad bucket
tags: [agile, requirements, pm-101]  # searchable tags
author: "@benhedrington"               # original author
maintainers: ["@benhedrington"]        # current owners
last_reviewed: 2026-05-10            # ISO date
estimated_minutes: 15                # time to consume
prerequisites: [backlog-basics]      # skill ids that should precede this
---

# Markdown body

## Summary
...

## When to use this skill
...

## The playbook
...

## Common anti-patterns
...

## Exit criteria (how you know you have it)
...
```

**Rules:**
- `id` must match the filename (without `.md`).
- `version` follows semver.
- A skill in `live/` must have all fields present.
- A skill in `dev/` may omit optional fields.
- A skill in `stage/` must have all fields present (pre-flight check).

---

## Pack Schema

```yaml
---
id: junior-pm-core
name: Junior PM Core Pack
audience: New PMs, 0–2 years experience
estimated_onboarding: 4 weeks
prerequisite_packs: []              # optional ordered list of pack ids
curator: "@benhedrington"             # person/org responsible
last_updated: 2026-05-10
---

# Skills in recommended order

- user-story-writing
- backlog-prioritization
- stakeholder-communication
- roadmap-basics
- metric-definition
```

**Rules:**
- A pack is valid only if every skill listed exists in `skills/live/` (active or deprecated).
- Packs do not version pin. They reference skill names only.
- Order in the list is the recommended consumption order.
- Packs may reference deprecated skills, but validation warns.

---

## Promotion Pipeline

```
dev/  →  stage/  →  live/
  ↑                      ↓ (retirement)
  └──────────────────────┘ (deprecated skills remain in live/)
```

**dev → stage:**
- Skill is complete (all required fields, markdown body present).
- Self-review or peer review passed.
- Run: `scripts/promote.py {skill-id} dev stage`

**stage → live:**
- Curator review passed.
- No naming conflicts in `live/`.
- If replacing an older version, old skill is marked `deprecated: true` (not deleted).
- Run: `scripts/promote.py {skill-id} stage live`

**Retirement (from live):**
- Set `deprecated: true` in frontmatter.
- Skill file remains in `live/`.
- Curator updates packs to remove or swap at their own pace.

---

## Contribution & Curation Workflow

Internal teams drop files into `incoming/`. The curator processes them via `/pm-skills-inbox`.

### Classification
Every contribution is classified as one of:

- **A. New skill draft** — structured enough to become a skill in `skills/dev/`
- **B. Improvement to existing skill** — enriches a live skill with examples, anti-patterns, or nuance
- **C. Raw fragment / knowledge** — war story, template, or half-formed idea for `incoming/fragments/`

### Inbox (`/pm-skills-inbox`)
- `--list`: see unprocessed files in `incoming/`
- `--process <file>`: classify and route to `skills/dev/`, an existing skill, or `incoming/fragments/`
- `--reject <file>`: move to `incoming/rejected/` with reason note
- `--sweep`: batch-process all unprocessed files interactively

### Curation (`/pm-skills-curate`)
Periodically, the curator turns fragments in `incoming/fragments/` into skills:
- `--list-fragments`: see raw material waiting
- `--fragment <file> --to-skill <id>`: fold a fragment into an existing skill
- `--fragment <file> --new-skill <id>`: turn a fragment into a new skill draft

Absorbed fragments are moved to `incoming/archive/`. Original contributions are always preserved in `incoming/archive/`.

---

## Validation Rules

Run: `scripts/validate.py`

Checks:
1. Every skill file has valid YAML frontmatter with required fields.
2. Every skill `id` matches its filename.
3. Every pack skill reference resolves to a file in `skills/live/`.
4. No duplicate `id`s within a stage directory.
5. Deprecated skills are flagged but not treated as errors.

