# /skill-inbox

Review and intake skill contributions from the shared incoming folder.

## Description

Enterprise PMs drop skill suggestions, fixes, or draft skills into the shared `incoming/` folder. The skill admin uses this command to review submissions, import valid ones into `dev/`, and reject or request clarification on others.

## Usage

```
/skill-inbox [--list]
/skill-inbox --process <filename.md> [--import-to-dev | --reject "reason"]
/skill-inbox --sweep
```

## Steps

1. Load config, resolve `outputPath/incoming/`.
2. If `--list`: show all files in incoming/ with metadata (who, when, size, first-line preview).
3. If `--process`:
   - Read the file.
   - Display it to the admin with a summary.
   - Check if it's a valid skill format (frontmatter + sections) or free-form feedback.
   - If valid skill:
     - Ask admin to confirm category and name.
     - Copy to `dev/skills/<category>/<name>.md`.
     - Rewrite frontmatter: set `author` to contributor name, `version` to `0.0.0-contributed`, add `source: incoming/<filename>`.
     - Delete from incoming/ (or move to `incoming/archive/`).
   - If free-form feedback:
     - Create an issue note in `dev/reviews/incoming-feedback-<date>.md`.
     - Ask admin if they want to act on it now or backlog it.
     - Delete or archive the original.
   - If `--reject`: move file to `incoming/rejected/` with a note.
4. If `--sweep`: process all files in incoming/ sequentially, pausing for admin decision on each.

## Contribution Format (for PMs)

PMs should use the `CONTRIBUTION-TEMPLATE.md` in the shared output folder:

```markdown
---
contribution_type: [new-skill | skill-fix | idea | feedback]
skill_name: [if applicable]
category: [discovery | delivery | strategy | stakeholders | metrics]
author: [their name/team]
date: [YYYY-MM-DD]
---

# [Title]

## Context
What prompted this contribution.

## Content
The actual suggestion, fix, or draft skill content.

## Why This Matters
How it would help the team.
```

## Example

```
/skill-inbox --list
/skill-inbox --action process --file "exec-comms-v2.md" --import-to-dev
/skill-inbox --action process --file "bad-idea.md" --reject "Too narrow, only applies to one team"
/skill-inbox --sweep
```

## Notes

- The incoming folder is in `outputPath/incoming/` (the shared folder PMs see).
- Always rewrite contributed skills before certifying. PMs are experts in their work, not in skill file structure.
- Credit the contributor in the skill frontmatter or a "Contributors" section.
- Rejected items go to `incoming/rejected/` — don't delete them outright, they might be useful later.
- Run this weekly or after announcing a new release (that's when most feedback arrives).
