# PM Skills Platform

Enterprise AI skill distribution toolkit for product management teams.

## What this is

A Claude Code-native workflow for curating, versioning, and distributing PM skills. No CLI package to install. The interface is slash commands inside Claude Code.

## Architecture

- **Skills** are versioned markdown files with YAML frontmatter, promoted through `dev/stage/live`.
- **Packs** are unversioned manifests that list skill names and always float to latest `live/`.
- **Gold repo** is the upstream source of truth. Share `skills/live/` with internal teams.
- **Deprecated skills** stay in `live/` with a `deprecated: true` flag — packs never break from missing files.

## Slash Commands

| Command | Purpose |
|---------|---------|
| `/pm-skills-init` | Scaffold the directory structure |
| `/pm-skills-new <skill-id>` | Create a new skill draft in `dev/` |
| `/pm-skills-validate` | Validate skills and packs |
| `/pm-skills-promote <id> --from <env> --to <env>` | Promote through the pipeline |
| `/pm-skills-list [--env]` | List skills |
| `/pm-skills-diff --from <env> --to <env>` | Compare environments |
| `/pm-skills-pack-info <pack-id>` | Show pack contents and status |
| `/pm-skills-inbox` | Process incoming contributions |
| `/pm-skills-curate` | Turn fragments into structured skills |

## Directory Structure

```
├── .claude/commands/          ← Slash command definitions
├── skills/
│   ├── dev/                   ← Drafts
│   ├── stage/                 ← Reviewed
│   └── live/                  ← Published (share this folder)
├── packs/                     ← Curated manifests
├── incoming/                  ← Contribution drop zone
│   ├── fragments/             ← Classified raw material
│   ├── archive/               ← Processed originals
│   └── rejected/              ← Declined with reasons
├── scripts/                   ← Mechanical helpers
│   ├── init.py
│   ├── validate.py
│   ├── promote.py
│   ├── list.py
│   ├── diff.py
│   └── pack-info.py
├── templates/
│   └── skill-template.md
├── ARCHITECTURE.md            ← Full spec
├── docs/
│   ├── GETTING-STARTED.md       ← First-day guide
│   └── IMPORTING-EXTERNAL-SKILLS.md
└── README.md                  ← This file
```

## Installation

This is a Claude Code-native workflow. There is no package to install.

```bash
# 1. Clone or copy the repo
git clone <repo-url> pm-skills-platform
cd pm-skills-platform

# 2. Open in Claude Code
claude
```

Claude Code automatically discovers `.claude/commands/*.md`. The slash commands are available immediately.

```
# 3. Initialize
/pm-skills-init
```

This interactively asks for:
- **Gold repository path**: Where your `skills/{dev,stage,live}/` and `packs/` live.
- **Output path**: The shared folder your internal teams will read from.
- **Organization name**: For the config file.

Done. That is the entire installation.

## Quick Start

For a full walkthrough, read `docs/GETTING-STARTED.md`. The tl;dr:

1. `/pm-skills-init` — scaffold and configure
2. `/pm-skills-new my-skill` — create a draft in `dev/`
3. `/pm-skills-validate` — check quality
4. `/pm-skills-promote my-skill dev stage` — move to review
5. `/pm-skills-promote my-skill stage live` — publish
6. Share `skills/live/` with your teams
