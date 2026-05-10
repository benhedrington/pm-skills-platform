# /pm-skills-inbox

Process incoming skill contributions from internal teams.

## Usage
```
/pm-skills-inbox --list
/pm-skills-inbox --sweep
/pm-skills-inbox --process <filename.md>
/pm-skills-inbox --reject <filename.md> --reason "..."
```

## Steps

### `--list`
1. List all `.md` files in `incoming/` (not in `archive/` or `rejected/`).
2. Show filenames and a 2-line preview of each.

### `--process <file>`
1. Read `incoming/<file>`.
2. Classify the contribution by asking the user:
   - **A. New skill** — structured enough to become a skill draft
   - **B. Improvement to existing skill** — enriches a current skill with examples, anti-patterns, or nuance
   - **C. Raw fragment / knowledge** — war story, template, half-formed idea for later curation
3. Execute based on classification:
   - **A (New skill)**: Write to `skills/dev/` with clean frontmatter (`version: 0.0.0-contributed`, `source: incoming/<file>`). Fill standard sections from the raw content.
   - **B (Improvement)**: Ask which existing skill it enriches. Create a review note at `skills/dev/<skill-id>/reviews/<timestamp>-<file>` or directly patch the skill in `dev/` with a clear edit summary. Prefer the review note if the change is large.
   - **C (Fragment)**: Move to `incoming/fragments/` with a dated filename (`YYYY-MM-DD--topic--source.md`). Add a `source:` note in the frontmatter.
4. Move the original to `incoming/archive/YYYY-MM-DD--<file>`.
5. Report what was created and where.

### `--reject <file>`
1. Move `incoming/<file>` to `incoming/rejected/<file>`.
2. Write `incoming/rejected/<file>.reason.md` with the rejection reason.
3. Report the action.

### `--sweep`
1. List all unprocessed files in `incoming/`.
2. For each file, show the first 20 lines and ask: import (then classify A/B/C), reject, or skip?
3. Execute the chosen action for each.
4. Summarize: imported (how many as skill vs improvement vs fragment), rejected, skipped.

## Notes
- This command uses Claude Code's built-in file tools. No external script needed.
- Always preserve the original in `archive/` or `rejected/`.
- Fragments in `fragments/` are reviewed periodically by the curator and turned into skills or folded into existing ones.
