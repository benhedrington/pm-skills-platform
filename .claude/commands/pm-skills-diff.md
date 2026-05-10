# /pm-skills-diff

Compare two environments to see what has changed before promoting.

## Usage
```
/pm-skills-diff --from <dev|stage|live> --to <dev|stage|live>
```

## Steps
1. Scan both environments for skill files.
2. Show skills that exist in `--from` but not in `--to` (new/pending).
3. Show skills that exist in both but differ in version (drift).
4. Show deprecated skills in `--to` that have replacements in `--from`.
