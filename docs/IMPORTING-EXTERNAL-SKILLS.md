# Importing External Skills

The PM Skills Platform is opinionated about format and quality. External skills from other authors, repos, or formats are treated as raw material — not native content.

This document describes how to bring external skills into your platform.

## Core Principle

**External skills are incoming contributions.**

They must be reformatted, adapted, and promoted through the same `dev → stage → live` pipeline as skills written from scratch. There is no auto-import that bypasses the curator.

## The Import Flow

### 1. Obtain the skill

Clone, download, or copy the external skill files. Examples:

```bash
git clone https://github.com/some-author/skills.git /tmp/external-skills
cp /tmp/external-skills/skills/debugging/SKILL.md ./incoming/debugging-from-author.md
```

Or simply copy-paste content into a new file in `incoming/`.

### 2. Classify and route

Run the inbox workflow:

```
/pm-skills-inbox --process debugging-from-author.md
```

Classify it:
- **A. New skill** — if it maps cleanly to a PM skill area
- **B. Improvement** — if it enriches an existing skill
- **C. Fragment** — if it is domain-adjacent or needs heavy rewriting

### 3. Reformat to platform schema

Every imported skill must match the PM Skills Platform format:

```yaml
---
id: debugging-customer-complaints
name: Debugging Customer Complaints
version: 0.0.0-imported
deprecated: false
category: delivery
tags: [debugging, support, escalation]
author: "@original-author"
maintainers: ["@your-handle"]
last_reviewed: 2026-05-10
estimated_minutes: 20
prerequisites: [customer-interview-basics]
---

## Summary
...

## When to use this skill
...

## The playbook
...

## Common anti-patterns
...

## Exit criteria
...
```

**Required changes:**
- Add YAML frontmatter with all required fields
- Map the external content to the standard sections (Summary, Playbook, Anti-patterns, Exit criteria)
- Translate domain-specific language if needed (engineering concepts → PM concepts)
- Set `version: 0.0.0-imported` and `source: <original-url>`
- Assign a maintainer (you or your team)

### 4. Validate

```
/pm-skills-validate --env dev --skill debugging-customer-complaints
```

Fix any errors before promoting.

### 5. Promote

```
/pm-skills-promote debugging-customer-complaints dev stage
/pm-skills-promote debugging-customer-complaints stage live
```

Only after it passes review does it enter `live/` and become available to packs.

## What NOT to do

- Do not import skills directly into `skills/live/` — this breaks the pipeline and validation.
- Do not preserve the external format (e.g., raw SKILL.md without frontmatter) in your platform.
- Do not auto-promote imported skills because they were "already published" elsewhere.
- Do not import entire external repos as-is — cherry-pick skills that fit your platform's scope.

## Shortcut: The import slash command

For convenience, a future slash command may exist:

```
/pm-skills-import --from <url> --as <skill-id>
```

This command would:
1. Fetch the content from the URL
2. Write it to `skills/dev/<skill-id>.md` with minimal scaffolding
3. Set `version: 0.0.0-imported` and `source: <url>`
4. Prompt the curator to reformat and validate

It does NOT bypass the pipeline. It just saves typing.

## Examples

**Engineering skill → PM skill**

An external engineering skill about "debugging hard bugs" can inspire a PM skill about "debugging why a feature missed its metric target." The structural pattern (build a feedback loop, generate hypotheses) translates directly. The domain language must change.

**Productivity skill → PM skill**

An external skill about "grilling stakeholders to clarify requirements" may map almost directly to PM work with minimal rewriting.

**Partial skill → Fragment**

A blog post or conversation transcript about "how we handle escalations" is not a skill yet. Classify it as a fragment, store it in `incoming/fragments/`, and fold it into a skill later via `/pm-skills-curate`.

## Remember

The value of the PM Skills Platform is curation, not collection. Every imported skill represents a decision by the curator that this content is worth maintaining in your organization's voice and format.
