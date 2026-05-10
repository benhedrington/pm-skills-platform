# /pm-skills-curate

Turn raw fragments into structured skills or enrich existing skills.

## Usage
```
/pm-skills-curate --list-fragments
/pm-skills-curate --fragment <filename> --to-skill <skill-id>
/pm-skills-curate --fragment <filename> --new-skill <skill-id>
```

## Steps

### `--list-fragments`
1. List all `.md` files in `incoming/fragments/` (not in `incoming/archive/`).
2. Show title/topic, date, and a one-line summary.

### `--fragment <file> --to-skill <skill-id>`
1. Read the fragment from `incoming/fragments/<file>`.
2. Read the target skill from `skills/dev/<skill-id>.md` (or `stage/` or `live/` if not in dev).
3. Ask the user which sections to enrich:
   - Examples
   - Anti-patterns
   - Exit criteria
   - Playbook steps
4. Apply the enrichment with a clear edit summary.
5. Write a curation note: `incoming/fragments/<file>.curated.md` documenting what was absorbed.
6. Move the original fragment to `incoming/archive/<file>`.

### `--fragment <file> --new-skill <skill-id>`
1. Read the fragment from `incoming/fragments/<file>`.
2. Create a new skill draft at `skills/dev/<skill-id>.md` using the standard template.
3. Structure the fragment content into Summary, Playbook, Examples, Anti-patterns, Exit criteria.
4. Set `version: 0.0.0-curated`, `source: incoming/fragments/<file>`.
5. Move the original fragment to `incoming/archive/<file>`.

## Notes
- This is a human-in-the-loop workflow. The slash command guides the curator; Claude does the mechanical rewrite.
- Always archive the original fragment after curation. Do not delete.
