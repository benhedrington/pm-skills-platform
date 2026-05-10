# /pm-skills-promote

Promote a skill through the dev/stage/live pipeline.

## Usage
```
/pm-skills-promote <skill-id> --from <dev|stage> --to <stage|live>
```

## Steps
1. Validate the transition is allowed (dev→stage, stage→live only).
2. If promoting to live, check that no active (non-deprecated) skill with the same id already exists in live.
3. Run `python scripts/promote.py <skill-id> <from> <to>`.
4. Report the new location and remind the user to run `/pm-skills-validate`.
5. Remind the user that packs referencing this skill will now see the latest version.
