# /skill-build

Build a distributable package from the live environment.

## Description

Bundles skills and knowledge files from `live/` into a versioned package in `packages/`. Only builds from `live` — dev and stage are not buildable. The output package includes install instructions for consumers.

## Usage

```
/skill-build --version <semver>
```

## Steps

1. Load config.
2. Validate all skills in `live/`. Fail fast on any error.
3. Validate all knowledge files in `live/` (must parse with frontmatter).
4. Generate `manifest.json`:
   - package name, version, timestamp
   - list of skills with metadata
   - list of included knowledge files
   - required knowledge (referenced but not bundled — consumer must provide, or marked as template)
5. Generate `README-INSTALL.md`:
   - What's in the package
   - How to install into Claude Projects
   - How to install into ChatGPT Custom Instructions
   - How to install into Claude Code
   - Version and update notes
6. Copy everything to `packages/live-<version>/`.
7. Report the package path, skill count, knowledge count.

## Example

```
/skill-build --version 1.2.0
```

## Notes

- If `--version` omitted, use `pmskills.config.yaml` version + build date (e.g., `1.0.0-20240615`).
- The build is deterministic: same live/ content always produces the same package structure.
- Only `live/` is buildable. If you try to build from dev or stage, refuse and tell the admin to promote first.
