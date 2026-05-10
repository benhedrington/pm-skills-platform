# /skill-diff

Show differences between environments for a skill or the entire library.

## Description

Compares skills and knowledge files across dev, stage, and live. Helps the admin understand what's changed, what's pending promotion, and whether live is drifted from stage.

## Usage

```
/skill-diff <skill-name> [--from dev] [--to stage]
/skill-diff --all [--from dev] [--to live]
/skill-diff --knowledge [file-name]
```

## Steps

1. Load config.
2. For the specified skill, compare the file in `--from` environment vs `--to` environment.
3. If `--all`, list all skills that exist in both environments and show whether they differ.
4. Also show skills that exist in `from` but not in `to` (pending promotion).
5. For knowledge files, same logic.

## Output Format

```
Comparing dev → stage

Skills:
  ✓ opportunity-assessment.md    identical
  ✗ exec-comms.md                modified (last changed: dev 2024-06-01, stage 2024-05-15)
  → roadmap-prioritization.md     only in dev (not yet promoted)

Knowledge:
  ✓ company-context.md           identical
  ✗ ways-of-working.md           modified

Pending promotion: 1 skill, 1 knowledge file
```

## Notes

- If no `--from`/`--to` specified, default to comparing the two environments where the skill exists (or dev→stage if in multiple).
- `--all` is useful before a build to see what's new in live since last publish.
