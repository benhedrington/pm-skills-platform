# /pm-skills-validate

Validate skills and packs against quality rules.

## Usage
```
/pm-skills-validate [--env dev|stage|live] [--skill <skill-id>] [--pack <pack-id>]
```

## Steps
1. Run `python scripts/validate.py`.
2. If `--env` is passed, only validate skills in that environment.
3. If `--skill` is passed, only validate that specific skill.
4. If `--pack` is passed, validate that pack's references against `skills/live/`.
5. Report pass/fail with specific, actionable errors.
