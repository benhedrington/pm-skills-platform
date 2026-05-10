# /skill-publish

Publish a built package from packages/ to the configured output folder.

## Description

Copies a built package from `packages/` to `outputPath` (the shared folder, OneDrive, or network drive). Generates a catalog entry and consumer announcement. The output path is where enterprise PMs grab their skill bundles.

## Usage

```
/skill-publish --package <package-name>
```

## Steps

1. Load config. Verify `outputPath` is set.
2. Verify the package exists in `packages/<package-name>/`.
3. Verify `outputPath/` exists on the filesystem. If not, error with helpful message.
4. Copy the package directory to `<outputPath>/packages/<package-name>/`.
5. Update `<outputPath>/index.md` catalog:
   - Add entry with package name, version, date, skill count, short description
6. Generate `ANNOUNCEMENT.md` in `packages/`:
   - What's new in this release
   - Which PMs should install which packages
   - Direct path to output folder
   - Step-by-step consumer instructions (or link to CONSUMER-GUIDE)
7. Report: "Published to <outputPath>/packages/<package-name>/"
8. Remind admin to verify sync if outputPath is a cloud-synced folder (OneDrive, Dropbox, etc.).

## Example

```
/skill-publish --package live-1.2.0
```

## Notes

- If outputPath is a OneDrive folder, the Microsoft sync client handles cloud upload. The admin just needs to wait for the sync icon to clear.
- If outputPath is a network drive, ensure permissions allow read access for all PMs.
- The catalog (`index.md`) is what PMs browse to find available packages.
- You can republish the same package if you fix a typo — it will overwrite in outputPath.
