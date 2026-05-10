# /skill-init

Initialize a PM Skills Gold repository with dev/stage/live environments.

## Description

Scaffolds the folder structure for managing skills through three environments: dev (drafts), stage (under review), and live (certified). Asks the user to configure paths.

## Usage

```
/skill-init
```

## Steps

1. Check if `pmskills.config.yaml` already exists. If yes, load and display current config, ask if user wants to reinitialize.
2. Ask user for the **gold repository path** (where dev/stage/live live):
   - "Where should your gold repository live?"
   - Suggest current working directory or `~/pm-skills-gold`
   - Accept absolute or relative path
3. Ask user for the **output path** (where published packages go):
   - "Where should published packages go? (e.g., your OneDrive shared folder, a network drive, or a local shared folder)"
   - Suggest: `<goldPath>/output` or detect common OneDrive paths
   - Make clear this is where PMs will grab packages from
4. Ask for org name.
5. Create directory structure: `dev/`, `stage/`, `live/`, each with `skills/` (subcategories), `knowledge/`, and `reviews/`.
6. Create `output/incoming/` folder (if outputPath is set) for PM contributions.
7. Write `pmskills.config.yaml` with all paths resolved to absolute paths.
8. Copy starter knowledge templates into `dev/knowledge/`.
9. Copy skill template into `templates/`.
10. Copy contribution template into `output/` (so PMs know how to submit).
11. Report what was created with absolute paths for verification.

## Example

```
/skill-init
> Where should your gold repository live? /home/alice/pm-skills-gold
> Where should published packages go? /home/alice/OneDrive/PM-Skills-Platform
> Org name? acme-corp

Created:
  /home/alice/pm-skills-gold/dev/skills/discovery/
  /home/alice/pm-skills-gold/dev/skills/delivery/
  ...
  /home/alice/pm-skills-gold/pmskills.config.yaml
```

## Notes

- `outputPath` can be inside the gold repo (e.g. `<goldPath>/output`) or completely separate (e.g. a OneDrive folder).
- If the user says their gold repo IS their OneDrive folder, that's fine — set `goldPath` to the OneDrive location and `outputPath` to `<goldPath>/output`.
- Record absolute paths in config to avoid confusion.
