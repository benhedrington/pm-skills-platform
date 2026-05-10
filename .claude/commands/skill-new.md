# /skill-new

Create a new skill draft in the dev environment.

## Description

Generates a new skill markdown file from the standard template in `dev/skills/<category>/`. The admin then edits the body with Claude Code.

## Usage

```
/skill-new --name <skill-name> --category <category> [--description "..."]
```

## Steps

1. Load `pmskills.config.yaml` to confirm gold repo path.
2. Validate the category exists (or is one of: discovery, delivery, strategy, stakeholders, metrics).
3. Check if a skill with this name already exists in dev, stage, or live. If yes, warn and ask to confirm overwrite or bump version.
4. Read `templates/skill-template.md`.
5. Replace placeholders: `{{NAME}}`, `{{CATEGORY}}`, `{{DESCRIPTION}}`, `{{DATE}}`.
6. Write to `<goldPath>/dev/skills/<category>/<skill-name>.md`.
7. Open the file for editing.
8. Report: "Created draft in dev/. Run /skill-validate --env dev when ready."

## Example

```
/skill-new --name opportunity-assessment --category discovery --description "Structured opportunity sizing for enterprise PMs"
```

## Notes

- Skill names should be kebab-case.
- Always creates in `dev/` — never in stage or live directly.
- If you want to base a new skill on an existing one, copy the existing file manually in dev/ first.
