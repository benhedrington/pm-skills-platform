# /skill-validate

Validate skill files in a specific environment.

## Description

Runs enterprise-quality lint checks on skills in dev, stage, or live. Reports pass/fail with specific fixes. Use this before promotion and before build.

## Usage

```
/skill-validate [path-to-skill.md] --env <dev|stage|live>
/skill-validate --all --env <dev|stage|live>
/skill-validate --category <category> --env <dev|stage|live>
```

## Validation Rules

1. **Frontmatter**: Must include `name`, `category`, `version`, `author`, `description`, `classification`
2. **Required Sections**: Context, Role, Principles, Frameworks, Anti-Patterns, Examples
3. **Anti-Patterns**: At least 3 specific, concrete anti-patterns
4. **Examples**: At least 2 concrete input/output pairs or scenarios
5. **Knowledge References**: If `requires_knowledge` specified, files must exist in the *same environment's* `knowledge/` folder
6. **Classification**: Must be `internal` or `confidential`
7. **Body Length**: > 500 words
8. **No Generic AI Voice**: Flag phrases like "it's important to note", "in today's fast-paced world"

## Output Format

```
Environment: stage

✓ opportunity-assessment.md (discovery)
  - frontmatter: pass
  - sections: pass
  - anti-patterns: pass (4 found)
  - examples: pass (3 found)
  - knowledge refs: pass
  - classification: pass
  - word count: 1,247

✗ exec-comms.md (stakeholders)
  - anti-patterns: FAIL (only 1 found, need 3+)
  - classification: FAIL (missing)

Summary: 1 pass, 1 fail
```

## Notes

- Always validate before promoting to the next environment.
- `live` environment should have zero failures before build.
- Knowledge file references are resolved against the environment being validated, not globally.
