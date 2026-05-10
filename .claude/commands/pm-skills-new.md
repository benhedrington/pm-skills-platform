# /pm-skills-new

Create a new skill draft in `skills/dev/`.

## Usage
```
/pm-skills-new <skill-id>
```

## Steps
1. Validate the skill-id is kebab-case.
2. Check that `skills/dev/{skill-id}.md` does not already exist.
3. Copy `templates/skill-template.md` to `skills/dev/{skill-id}.md`, replacing placeholders.
4. Open the file for the user to edit.
5. Remind them to run `/pm-skills-validate --env dev` before promoting.
