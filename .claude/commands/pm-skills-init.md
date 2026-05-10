# /pm-skills-init

Initialize the PM Skills Platform. Scaffolds the directory structure, asks for paths interactively, and writes a config file.

## Usage
```
/pm-skills-init
```

## Steps
1. Run `python scripts/init.py` interactively. It will prompt for:
   - **Gold repository path**: Where `skills/{dev,stage,live}/` and `packs/` will live. Defaults to the current directory.
   - **Output path**: Where built packages or shared folders go. Defaults to `<current-dir>/output/`.
   - **Organization name**: For the config file.
2. The script scaffolds all directories and writes `config.yaml` with resolved absolute paths.
3. Report the configured paths. Remind the admin that `skills/live/` is the folder to share with internal teams.

## What the user needs to know
- This is the only "installation" step. After init, the slash commands are ready to use.
- The gold repo can live anywhere: local disk, OneDrive, network share, or inside a git repository.
- The output path is often a shared folder (OneDrive, Dropbox, network drive) that internal teams read from.
