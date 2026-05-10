# /skill-review

Run an enterprise peer review on a skill file in stage (or dev).

## Description

Quality gate. Claude acts as a senior PM leader reviewing a proposed skill for certification. Checks for accuracy, tone, org fit, and practical utility.

## Usage

```
/skill-review <skill-name> [--env stage] [--focus accuracy|tone|org-fit|examples]
```

## Steps

1. Locate the skill in the specified environment (default: stage).
2. Load any referenced knowledge files from the same environment.
3. Perform a structured review across these dimensions:
   - **Accuracy**: Frameworks named correctly? Principles actually used here? Any contradictions?
   - **Tone**: Does this sound like *our* org's voice, or generic AI sludge?
   - **Org Fit**: Does it reference real terminology, teams, constraints from knowledge files?
   - **Examples Quality**: Realistic? Show enterprise messiness (politics, scope creep, OKR misalignment)?
   - **Anti-Pattern Specificity**: Are these things we've actually seen, or generic warnings?
   - **Actionability**: Could a junior PM follow this and produce better work?
4. Output a structured review with verdict: PASS, PASS WITH EDITS, or FAIL.
5. Write the review to `<goldPath>/<env>/reviews/<skill-name>-<date>.md`.
6. Report the review summary and file path.

## Output Format

```
## Review: opportunity-assessment.md
Environment: stage
Reviewer: Senior PM Lead (simulated)
Verdict: PASS with minor edits

### Strengths
...

### Issues
- [P2] Anti-pattern "Ignoring compliance" is too vague.
- [P1] Framework references "RICE" but our org uses "ICE".

### Suggested Edits
```

## Notes

- Always load referenced knowledge files before reviewing.
- A skill needs at least one /skill-review pass (with PASS or PASS WITH EDITS) before promotion to live.
- Reviews are stored in `<env>/reviews/` for audit trail.
- If the review verdict is FAIL, the skill stays in stage (or returns to dev) until fixed.
