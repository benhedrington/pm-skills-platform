# Contributing to PM Skills Platform

## Skill Contributions

### Proposing a New Skill

1. Open an issue with:
   - Name and category
   - Problem it solves
   - Target user (IC PM, senior PM, leader?)
   - Draft of 2-3 principles

2. After discussion, the skill admin will create a draft in `dev/`.

3. Author the skill. Focus on:
   - Real frameworks your org uses
   - Anti-patterns you've witnessed
   - Examples with messy, realistic details

4. Submit for review. Include:
   - The skill file
   - Evidence that `/skill-validate --env dev` passes
   - Notes on what changed and why

### Editing Skills

When editing an existing skill:
- Bump `version` in frontmatter (semver)
- Start in `dev/`, promote through stage to live
- Re-run validation and review for substantial changes

### Knowledge File Updates

Knowledge files change as the org evolves. Propose updates for:
- New terminology after reorgs
- Updated tech stack
- Changed ceremonies

Keep knowledge factual and neutral. Opinions belong in skills.

## Style Guide

- **Markdown:** `##` for sections, `###` for subsections, `-` for bullets
- **Voice:** Write like a senior PM talking to a peer. Use "you" (addressing the AI).
- **Anti-patterns:** War stories, not warnings. Include why it happens and how to catch it.
- **Examples:** Realistic messiness — vague inputs, political constraints, incomplete data.
- **Naming:** `kebab-case.md` for files, `kebab-case` for skill names.

## Governance

- **Skill Admin:** Maintains repo, approves certifications, publishes
- **Peer Reviewers:** Senior PMs who run `/skill-review`
- **Contributors:** Any PM who proposes skills or knowledge updates

No skill ships without validation + review.
