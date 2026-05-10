#!/usr/bin/env python3
"""Compare two environments for drift and pending promotions."""

import sys
from pathlib import Path
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_STAGES = ["dev", "stage", "live"]

def parse_frontmatter(path):
    text = path.read_text()
    if not text.startswith("---"):
        return None
    _, rest = text.split("---", 1)
    parts = rest.split("---", 1)
    if len(parts) != 2:
        return None
    try:
        return yaml.safe_load(parts[0])
    except yaml.YAMLError:
        return None

def diff(from_stage, to_stage):
    if from_stage not in SKILL_STAGES or to_stage not in SKILL_STAGES:
        print(f"Invalid stage. Use: {', '.join(SKILL_STAGES)}")
        sys.exit(1)

    from_dir = REPO_ROOT / "skills" / from_stage
    to_dir = REPO_ROOT / "skills" / to_stage

    from_skills = {p.stem: p for p in from_dir.glob("*.md")} if from_dir.exists() else {}
    to_skills = {p.stem: p for p in to_dir.glob("*.md")} if to_dir.exists() else {}

    only_in_from = set(from_skills) - set(to_skills)
    only_in_to = set(to_skills) - set(from_skills)
    in_both = set(from_skills) & set(to_skills)

    print(f"\n=== Diff: {from_stage} -> {to_stage} ===\n")

    if only_in_from:
        print(f"Only in {from_stage} ({len(only_in_from)}):")
        for sid in sorted(only_in_from):
            print(f"  + {sid}")
    else:
        print(f"Only in {from_stage}: none")

    if only_in_to:
        print(f"\nOnly in {to_stage} ({len(only_in_to)}):")
        for sid in sorted(only_in_to):
            print(f"  - {sid}")
    else:
        print(f"\nOnly in {to_stage}: none")

    drift = []
    for sid in sorted(in_both):
        from_fm = parse_frontmatter(from_skills[sid])
        to_fm = parse_frontmatter(to_skills[sid])
        from_ver = from_fm.get("version", "?") if from_fm else "?"
        to_ver = to_fm.get("version", "?") if to_fm else "?"
        if from_ver != to_ver:
            drift.append((sid, from_ver, to_ver))

    if drift:
        print(f"\nVersion drift ({len(drift)}):")
        for sid, fv, tv in drift:
            print(f"  ~ {sid:<30} {from_stage}: v{fv}  ->  {to_stage}: v{tv}")
    else:
        print("\nVersion drift: none")

def main():
    if len(sys.argv) != 3:
        print("Usage: diff.py <from-stage> <to-stage>")
        print("Example: diff.py dev stage")
        sys.exit(1)
    diff(sys.argv[1], sys.argv[2])

if __name__ == "__main__":
    main()
