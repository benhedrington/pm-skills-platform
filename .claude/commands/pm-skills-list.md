# /pm-skills-list

List skills in an environment or across all environments.

## Usage
```
/pm-skills-list [--env dev|stage|live]
```

## Steps
1. Scan `skills/<env>/` for `.md` files.
2. Extract `id`, `name`, `version`, and `deprecated` from frontmatter.
3. Print a formatted table or list.
4. If no `--env` is given, show all environments with a summary count.
