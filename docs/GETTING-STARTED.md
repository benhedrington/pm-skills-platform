# Getting Started

This guide walks you through your first day with the PM Skills Platform — from installation to your first published skill.

## What you need

- [Claude Code](https://claude.ai/code) installed
- Git (to clone the repo)
- Python 3 (for the helper scripts)
- A folder you can share with your team (OneDrive, Dropbox, network drive, or a local shared folder)

## Installation

### 1. Clone the repo

```bash
git clone https://github.com/benhedrington/pm-skills-platform.git
cd pm-skills-platform
```

### 2. Open in Claude Code

```bash
claude
```

Claude Code automatically discovers `.claude/commands/*.md`. All slash commands are ready immediately.

### 3. Initialize

```
/pm-skills-init
```

This runs `scripts/init.py` and asks you three questions:

- **Gold repository path**: Where `skills/{dev,stage,live}/` live. Usually the current directory.
- **Output path**: Where built packages go. Often a shared folder like `~/OneDrive/PM-Skills/`.
- **Organization name**: For the config file.

It scaffolds directories and writes `config.yaml` with absolute paths.

That is the entire installation. You are now the curator.

---

## Your first skill

### Create a draft

```
/pm-skills-new stakeholder-communication
```

This creates `skills/dev/stakeholder-communication.md` from the template. Fill in the YAML frontmatter and write the body.

### Validate before promoting

```
/pm-skills-validate --env dev --skill stakeholder-communication
```

Fix any errors. The validator checks:
- All required frontmatter fields present
- `id` matches filename
- Markdown body is not empty

### Move to review

```
/pm-skills-promote stakeholder-communication dev stage
```

The skill is now in `skills/stage/`. This is where peer review happens. Read it yourself or ask a colleague to review.

### Publish

```
/pm-skills-promote stakeholder-communication stage live
```

The skill is now in `skills/live/`. It is available to packs and shareable with teams.

---

## Your first pack

Packs are curated manifests of skills for a specific audience. They live in `packs/`.

Create `packs/new-pm-starter.md`:

```yaml
---
id: new-pm-starter
name: New PM Starter Pack
audience: New PMs, 0–2 years experience
estimated_onboarding: 4 weeks
prerequisite_packs: []
curator: "@you"
last_updated: 2026-05-10
---

- backlog-prioritization
- user-story-writing
- stakeholder-communication
```

Validate it:

```
/pm-skills-validate
```

This checks that every skill listed exists in `skills/live/`. If a skill is missing or deprecated, validation warns you.

---

## Share with your team

The folder to share is `skills/live/` inside your gold repository path. Configure your sync tool (OneDrive, Dropbox, rsync, or a shared network drive) to make this folder readable by your team.

Your team does not install anything. They read the markdown files directly or copy them into their own Claude projects.

### What teams see

When a team member opens `skills/live/`, they see:
- Versioned, reviewed skills with clear structure
- A `packs/` folder they can browse by persona
- No broken references (validation guarantees coexistence)

---

## The day-to-day workflow

### Adding a new skill

1. `/pm-skills-new <skill-id>` — draft in `dev/`
2. Edit the file directly or with Claude
3. `/pm-skills-validate --env dev`
4. `/pm-skills-promote <skill-id> dev stage`
5. Review
6. `/pm-skills-promote <skill-id> stage live`

### Updating an existing skill

You do not edit a live skill directly. Instead:

1. Copy the live skill back to `dev/`:
   ```bash
   cp skills/live/backlog-prioritization.md skills/dev/backlog-prioritization.md
   ```
2. Edit in `dev/`, bump the version in frontmatter
3. Validate and promote through stage → live
4. The old live version is marked `deprecated: true` (not deleted)
5. Packs automatically see the latest version

### Processing contributions from your team

Your team drops files in `incoming/`.

1. `/pm-skills-inbox --list` — see what's waiting
2. `/pm-skills-inbox --process idea.md` — classify and route
3. Choose A (new skill), B (improvement), or C (fragment)
4. Claude handles the mechanical work

### Curating fragments

Raw material accumulates in `incoming/fragments/`.

1. `/pm-skills-curate --list-fragments` — see the backlog
2. `/pm-skills-curate --fragment war-story.md --to-skill user-story-writing` — fold it into an existing skill
3. `/pm-skills-curate --fragment war-story.md --new-skill escalation-handling` — turn it into a new skill

---

## Key concepts to remember

- **Skills are atomic and versioned.** They live in `dev/`, `stage/`, or `live/`.
- **Packs are curated playlists.** They reference skill names only, never versions. A pack always floats to latest `live/`.
- **Deprecated skills stay in `live/`.** Packs do not break when a skill is retired — they see the deprecation flag.
- **You are the curator.** The platform enforces structure and validity, but you decide what belongs in which pack and when it is ready for teams.

---

## Next steps

- Read `ARCHITECTURE.md` for the full specification
- Read `docs/IMPORTING-EXTERNAL-SKILLS.md` if you want to bring in skills from other authors
- Run `/pm-skills-list` to see everything in your platform
- Run `/pm-skills-diff --from dev --to live` to see what is pending publication
