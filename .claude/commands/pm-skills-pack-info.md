# /pm-skills-pack-info

Show the contents and validation status of a pack.

## Usage
```
/pm-skills-pack-info <pack-id>
```

## Steps
1. Read `packs/<pack-id>.md`.
2. Show metadata (audience, curator, last_updated).
3. List all referenced skills with their current live status (active/deprecated/missing).
4. Warn if any skill is missing from `skills/live/` or is deprecated.
