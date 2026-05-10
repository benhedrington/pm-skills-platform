# PM Skills Platform

**A toolkit for managing a certified AI skills library across enterprise product management teams.**

Enterprise PMs have access to Claude and ChatGPT through their company. But they're starting from scratch every conversation — no shared context, no institutional knowledge, no reusable capabilities. Meanwhile, the PM who set up their AI well is 10x more effective than the one who didn't.

PM Skills Platform fixes the distribution problem. One skill admin maintains a "gold" repository — the source of truth for your org's AI context. Skills live in `dev`, get reviewed in `stage`, and ship from `live`. PMs install certified packages into their own Claude Projects or ChatGPT Custom Instructions in minutes.

## How It Works

```
Skill Admin (Claude Code)
    │
    ├─ drafts in dev/
    ├─ reviews in stage/
    └─ certifies in live/
         │
         ▼
    /skill-build → packages/
         │
         ▼
    /skill-publish → output/ (OneDrive, SharePoint, shared folder)
         │
         ▼
Enterprise PMs grab package → paste into Claude/ChatGPT
         │
         ▼
PMs drop feedback in output/incoming/ → admin intakes into dev/
```

## What Problem This Solves

| Without PM Skills Platform | With PM Skills Platform |
|---|---|
| Every PM writes their own prompts from scratch | One admin curates, everyone benefits |
| AI advice is generic and ignores your org | Skills reference real terminology, real constraints, real teams |
| Best practices live in senior PMs' heads | Codified in versioned, reviewable skill files |
| No feedback loop | PMs contribute via `incoming/`, admin intakes into next release |
| Prompts get copy-pasted into Slack and lost | Centralized, versioned, auditable |

A **skill** is not a prompt template. It's persistent context: here's how to think about opportunity assessment, here's what good executive communication looks like at our company, here are the anti-patterns to flag. When a PM loads a skill into Claude Projects, every conversation in that project starts with that context baked in.

## Getting Started (Skill Admin)

### Prerequisites

- [Claude Code](https://claude.ai/code) installed
- Python 3.9+ and `pip`
- A shared folder where your team can access files (OneDrive, SharePoint, network drive, or just a local folder)

### 1. Clone this repo

```bash
git clone https://github.com/yourorg/pm-skills-platform.git
cd pm-skills-platform
```

### 2. Install the helper

```bash
pip install pyyaml
# Optional but recommended: make it available everywhere
chmod +x scripts/pmskills.py
```

### 3. Initialize your gold repository

```bash
claude
```

Inside Claude Code:

```
/skill-init
```

Claude will ask you three questions:
1. **Gold repository path** — where `dev/`, `stage/`, `live/` live on your machine. Pick something permanent, e.g. `~/pm-skills-gold` or inside your OneDrive.
2. **Output path** — where published packages go. This is what your PMs see. E.g. `~/OneDrive/PM-Skills-Platform`.
3. **Org name** — for the config file.

### 4. Fill in your org's knowledge

Edit the starter files in `dev/knowledge/`:
- `company-context.md` — org structure, strategy, terminology
- `tech-landscape.md` — architecture, platforms, constraints
- `ways-of-working.md` — team norms, ceremonies, tools

These files are what make skills *yours*. Every skill that references `company-context` will inject this into its behavior.

### 5. Create your first skill

```
/skill-new --name opportunity-assessment --category discovery
```

Claude will generate a scaffold in `dev/skills/discovery/opportunity-assessment.md`. Edit it with Claude Code.

### 6. Validate, promote, build, publish

```
/skill-validate --env dev
/skill-promote opportunity-assessment --from dev --to stage
/skill-review opportunity-assessment --env stage
/skill-promote opportunity-assessment --from stage --to live
/skill-build --version 1.0.0
/skill-publish --package live-1.0.0
```

Your PMs can now grab the package from your shared output folder.

## Project Structure

```
pm-skills-gold/            ← You choose this path during init
├── dev/
│   ├── skills/            # Draft skills (discovery/, delivery/, strategy/, stakeholders/, metrics/)
│   ├── knowledge/         # Draft knowledge files
│   └── reviews/           # Review notes
├── stage/
│   ├── skills/            # Skills under peer review
│   ├── knowledge/         # Knowledge under review
│   └── reviews/           # Structured review documents
├── live/
│   ├── skills/            # Certified, publishable skills
│   └── knowledge/         # Certified knowledge files
├── packages/              # Built packages (generated, gitignored)
├── templates/
│   └── skill-template.md
├── scripts/
│   └── pmskills.py        # Mechanical helper (validate, build, publish, inbox)
├── .claude/commands/
│   ├── skill-init.md      # Initialize gold repo
│   ├── skill-new.md       # Create a new skill draft
│   ├── skill-validate.md  # Lint skills
│   ├── skill-promote.md   # Move skills between environments
│   ├── skill-review.md    # Peer review quality gate
│   ├── skill-diff.md      # Compare environments
│   ├── skill-build.md     # Bundle live/ into distributable package
│   ├── skill-publish.md   # Copy to shared output folder
│   └── skill-inbox.md     # Intake PM contributions
├── pmskills.config.yaml   # Your paths and settings
└── README.md
```

## The Three Environments

| Environment | Purpose | Quality Gate |
|---|---|---|
| **dev** | Drafting, experimenting, importing external skills | Self-review (`/skill-validate`) |
| **stage** | Internal review, testing with real PMs | Validation + peer review (`/skill-review`) |
| **live** | Certified, versioned, publishable | Admin approval. Only build and publish from here. |

## PM Contributions (The Feedback Loop)

Your shared output folder contains:
- `packages/` — built skill bundles
- `index.md` — catalog of what's available
- `incoming/` — **PMs drop contributions here**
- `CONTRIBUTION-TEMPLATE.md` — guides PMs on format

PMs write a markdown file with their idea, fix, or war story and drop it in `incoming/`. No git, no PRs.

The admin runs `/skill-inbox` weekly to review, import to `dev/`, reject with a reason, or batch-process everything.

## For Enterprise PMs (Consumers)

See [docs/CONSUMER-GUIDE.md](docs/CONSUMER-GUIDE.md) for:
- How to install into Claude Projects
- How to install into ChatGPT Custom Instructions
- How to contribute back via the `incoming/` folder

## Documentation

- [Admin Guide](docs/ADMIN-GUIDE.md) — Full guide for skill admins
- [Consumer Guide](docs/CONSUMER-GUIDE.md) — Guide for PMs installing and using skills
- [Contributing](docs/CONTRIBUTING.md) — How to propose skills and knowledge updates

## Why This Architecture?

**Why markdown files?** Because every AI tool accepts markdown. Claude Projects, ChatGPT Custom Instructions, Claude Code, Notion AI — they all take text. We don't lock you into a platform.

**Why a gold repository on the admin's machine?** Because skills contain org-sensitive context (strategy, terminology, constraints). Keeping the source of truth on the admin's machine, published only as built packages, means accidental commits to public repos don't leak internal details.

**Why three environments?** Because "it works on my machine" isn't good enough for enterprise. Skills need validation, peer review, and version history before they reach your entire PM org.

**Why an incoming folder instead of GitHub issues?** Because most enterprise PMs don't file GitHub issues. They write notes in Slack, send DMs, or vent in retros. A shared folder with a simple template lowers the barrier to contribution to "write a note and drop it here."

## Roadmap

- [x] Project scaffold and three-environment pipeline
- [x] Skill validation (structure, quality, generic-voice detection)
- [x] Build and publish to shared folders
- [x] PM contribution inbox (`incoming/`)
- [x] Starter skill library (opportunity-assessment, exec-comms, roadmap-prioritization)
- [x] Knowledge file templates
- [ ] More starter skills (delivery, metrics categories)
- [ ] Remote skill fetching (import from public repos)
- [ ] Automated diff reports between releases
- [ ] Web catalog UI (optional, for orgs that want browsing)

## Contributing

This project is for the PM community. If you have ideas, open an issue or drop a file in `incoming/` (if your org already uses this).

See [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) for conventions.

## License

MIT — see [LICENSE](LICENSE).
