# Admin Guide — PM Skills Platform

## Who This Is For

You are the skill admin: a PM leader or staff PM who curates AI context for your org. You maintain a "gold" repository on your machine with three environments.

## Workflow Overview

- **Draft in `dev`:** You and contributors write skills, test ideas, import external content.
- **Review in `stage`:** Peer reviewers validate and give feedback before certification.
- **Certify in `live`:** Only reviewed, approved skills reach the production library.
- **Build and publish from `live`:** The admin builds packages (`/skill-build`) and publishes to the shared output folder (`/skill-publish`).
- **Consume and contribute:** PMs install packages from the shared folder and drop feedback into `incoming/`.
- **Intake and iterate:** The admin runs `/skill-inbox` to process contributions, importing them into `dev/` for the next cycle.

```
PM contributes → incoming/ → /skill-inbox → dev/ → stage → live → packages/ → output/ → PMs install
```

## Your Repository

```
pm-skills-gold/          ← You choose where this lives
├── dev/                 ← Your workspace
├── stage/               ← Peer review queue
├── live/                ← Certified, publishable
├── packages/            ← Built bundles (generated)
├── pmskills.config.yaml ← Your paths and settings
└── ...
```

You choose where `pm-skills-gold/` lives. It can be:
- A local folder: `~/work/pm-skills-gold/`
- Inside your OneDrive: `~/OneDrive/pm-skills-gold/`
- On a network drive: `/Volumes/shared/pm-skills-gold/`

The `outputPath` (where published packages go) can be the same as goldPath or completely separate.

## Workflow

### Daily
- Draft skills in `dev/`
- Run `/skill-validate --env dev` to check quality

### Weekly
- Promote validated skills to `stage/`: `/skill-promote <name> --from dev --to stage`
- Request peer review (via `/skill-review` or asking a colleague)

### Per Release
- Promote reviewed skills to `live/`: `/skill-promote <name> --from stage --to live`
- Build: `/skill-build --version 1.2.0`
- Publish: `/skill-publish --package live-1.2.0`
- Verify files appear in output folder, post announcement

## Environments Explained

### dev
- **Purpose:** Drafting, experimenting, importing external skills
- **Quality bar:** Self-review. It's okay if things are rough.
- **Who:** Skill admin, contributors
- **Rule:** Nothing leaves dev without `/skill-validate`

### stage
- **Purpose:** Internal review, testing with real PMs
- **Quality bar:** Validation passes + at least one peer review
- **Who:** Peer reviewers, senior PMs
- **Rule:** Nothing leaves stage without a review file in `stage/reviews/`

### live
- **Purpose:** Certified, versioned, publishable
- **Quality bar:** Validation passes + review passed + admin approval
- **Who:** Skill admin only
- **Rule:** Only build and publish from live

## Commands

| Command | When | What it does |
|---|---|---|
| `/skill-init` | Once | Scaffold gold repo, set paths |
| `/skill-new` | Daily | Create draft in dev |
| `/skill-validate --env dev` | Daily | Lint drafts |
| `/skill-promote <name> dev stage` | Weekly | Move to review queue |
| `/skill-review <name> --env stage` | Weekly | Quality gate |
| `/skill-promote <name> stage live` | Per release | Certify |
| `/skill-build --version X` | Per release | Bundle from live |
| `/skill-publish --package X` | Per release | Ship to shared drive |
| `/skill-diff --all` | Anytime | See what's pending |
| `/skill-inbox` | Weekly | Review PM contributions from `incoming/` |

## PM Contributions

PMs can submit feedback, fixes, and new skill ideas via the `incoming/` folder in the shared output directory.

### How PMs Submit

The shared output folder contains:
- `packages/` — built skill bundles
- `index.md` — catalog of available packages
- `incoming/` — drop contributions here
- `CONTRIBUTION-TEMPLATE.md` — guide for PMs

PMs create a markdown file in `incoming/` with their idea. No git, no PRs — just a file in a shared folder.

### Admin Intake Workflow

```bash
# See what's waiting
/skill-inbox --list

# Review and import a contribution
/skill-inbox --process "new-skill.md" --import-to-dev

# Reject with a reason
/skill-inbox --process "bad-idea.md" --reject "Too specific to one team"

# Batch process everything
/skill-inbox --sweep
```

When you import a contribution:
1. The file is copied into `dev/skills/<category>/`
2. Frontmatter is rewritten: version becomes `0.0.0-contributed`, `source` points to original
3. Original is archived in `incoming/archive/`

If a contribution is free-form (not a structured skill), it becomes a review note in `dev/reviews/`.

### Encouraging Contributions

Mention the `incoming/` folder in every release announcement. Most contributions arrive right after a release when PMs start using the new skills and notice gaps.

## OneDrive Setup

If using OneDrive for output:

1. Ensure OneDrive desktop client is installed and syncing
2. Set `outputPath` to your shared folder, e.g.:
   ```yaml
   outputPath: /Users/you/OneDrive/PM-Skills-Platform
   ```
3. After publish, wait for the sync icon to clear on the package folder
4. Verify online at onedrive.com before announcing

If your gold repo IS in OneDrive:
```yaml
goldPath: /Users/you/OneDrive/pm-skills-gold
outputPath: /Users/you/OneDrive/pm-skills-gold/output
```

## Validation Rules

- Frontmatter: name, category, version, author, description, classification
- Sections: Context, Role, Principles, Frameworks, Anti-Patterns, Examples
- Anti-patterns: ≥3 specific, concrete items
- Examples: ≥2 input/output pairs or scenarios
- Knowledge refs: Referenced files must exist in same environment
- Word count: ≥500
- No generic AI voice phrases

## Managing External Skills

If you want to import from a public repo:

1. Download the `.md` file manually into `dev/skills/<category>/`
2. Edit frontmatter: set `author` to source, version to `0.0.0-imported`, add `source_url`
3. Adapt for your org (replace generic advice with org-specific)
4. Validate, review, promote through normal flow

Never publish imported skills without review.

## Troubleshooting

| Problem | Fix |
|---|---|
| "No config found" | Run `python scripts/pmskills.py init` or `/skill-init` |
| "Output path does not exist" | Create the folder or fix `outputPath` in config |
| Validation fails on imported skill | It's in dev — expected. Edit and re-validate |
| Build blocked | Fix live/ validation errors first |
| OneDrive not syncing | Check client, ensure folder is set to "Always keep on device" |
| Skill missing after promote | Check you used the right skill name (kebab-case, no .md) |

## Advanced

### Custom validation
Edit `scripts/pmskills.py` → `validate_skill()` to add org-specific rules.

### Git integration
Your gold repo should be a git repo. Commit after each release. Tag live builds:
```bash
git tag release-1.2.0
git push --tags
```

### Multiple contributors
Contributors fork the gold repo, work in their `dev/`, open PRs. The skill admin merges and handles promotion to stage/live.
