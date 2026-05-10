# /skill-promote

Move a skill (or knowledge file) from one environment to the next.

## Description

Promotes a skill through the pipeline: dev → stage → live. Copies the file and optionally its referenced knowledge files. Promoting to live should only happen after review.

## Usage

```
/skill-promote <skill-name> --from <dev|stage> --to <stage|live> [--with-knowledge]
```

## Steps

1. Load config and resolve paths.
2. Find the skill file in the `--from` environment: `<goldPath>/<from>/skills/<category>/<skill-name>.md`
3. If not found, error and list skills in that environment.
4. Parse the skill frontmatter to determine category.
5. Copy the skill to `<goldPath>/<to>/skills/<category>/<skill-name>.md`.
6. If `--with-knowledge` (default true), also copy referenced knowledge files from `<from>/knowledge/` to `<to>/knowledge/` if they don't already exist in `<to>`.
7. If promoting to `stage`, create a stub review file: `<goldPath>/stage/reviews/<skill-name>-<date>.md` with a template.
8. Report the promotion and next steps:
   - dev→stage: "Promoted to stage. Run /skill-review to begin peer review."
   - stage→live: "Promoted to live. Ready to build and publish."

## Examples

```
/skill-promote opportunity-assessment --from dev --to stage
/skill-promote exec-comms --from stage --to live
```

## Notes

- Promoting to `live` overwrites the existing live version. The old version is not archived automatically — use git for version history.
- If a knowledge file in `to/` is newer (more recently modified) than the one in `from/`, ask the user which to keep.
- You cannot promote from `live` — live is the terminal state.
- You can skip `--from` if the skill only exists in one environment (auto-detect).
