#!/usr/bin/env python3
"""Validate the PM Skills Platform repository."""

import sys
import os
import re
import yaml
from pathlib import Path
from collections import defaultdict

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_STAGES = ["dev", "stage", "live"]
REQUIRED_SKILL_FIELDS = {
    "id", "name", "version", "deprecated", "category", "tags",
    "author", "maintainers", "last_reviewed", "estimated_minutes", "prerequisites",
}
REQUIRED_PACK_FIELDS = {"id", "name", "audience", "estimated_onboarding", "curator", "last_updated"}

errors = []
warnings = []

def error(msg):
    errors.append(msg)

def warn(msg):
    warnings.append(msg)

def parse_frontmatter(path):
    text = path.read_text()
    if not text.startswith("---"):
        return None, text
    _, rest = text.split("---", 1)
    parts = rest.split("---", 1)
    if len(parts) != 2:
        return None, text
    try:
        return yaml.safe_load(parts[0]), parts[1]
    except yaml.YAMLError as e:
        return None, text

def validate_skills():
    for stage in SKILL_STAGES:
        stage_dir = REPO_ROOT / "skills" / stage
        if not stage_dir.exists():
            continue
        seen_ids = set()
        for fpath in sorted(stage_dir.glob("*.md")):
            fm, body = parse_frontmatter(fpath)
            rel = fpath.relative_to(REPO_ROOT)
            if fm is None:
                error(f"{rel}: invalid YAML frontmatter")
                continue
            sid = fm.get("id")
            if sid is None:
                error(f"{rel}: missing 'id' in frontmatter")
                continue
            if sid != fpath.stem:
                error(f"{rel}: id '{sid}' does not match filename '{fpath.stem}'")
            if sid in seen_ids:
                error(f"{rel}: duplicate id '{sid}' in {stage}/")
            seen_ids.add(sid)

            if stage == "dev":
                # dev can be sparse; just check id + name
                if "name" not in fm:
                    warn(f"{rel}: dev skill missing 'name'")
                continue

            # stage and live must have all required fields
            missing = REQUIRED_SKILL_FIELDS - set(fm.keys())
            if missing:
                error(f"{rel}: missing required fields: {', '.join(sorted(missing))}")

            if not isinstance(fm.get("deprecated"), bool):
                error(f"{rel}: 'deprecated' must be a boolean")

            if not body.strip():
                error(f"{rel}: empty markdown body")

def validate_packs():
    live_skills_dir = REPO_ROOT / "skills" / "live"
    live_skills = {p.stem for p in live_skills_dir.glob("*.md")} if live_skills_dir.exists() else set()

    packs_dir = REPO_ROOT / "packs"
    if not packs_dir.exists():
        return

    for fpath in sorted(packs_dir.glob("*.md")):
        fm, body = parse_frontmatter(fpath)
        rel = fpath.relative_to(REPO_ROOT)
        if fm is None:
            error(f"{rel}: invalid YAML frontmatter")
            continue

        missing = REQUIRED_PACK_FIELDS - set(fm.keys())
        if missing:
            error(f"{rel}: missing required fields: {', '.join(sorted(missing))}")

        # Extract skill references from body: lines starting with "- "
        refs = []
        for line in body.strip().splitlines():
            m = re.match(r"^-\s+([\w-]+)\s*$", line)
            if m:
                refs.append(m.group(1))

        for ref in refs:
            ref_path = live_skills_dir / f"{ref}.md"
            if ref not in live_skills:
                error(f"{rel}: references skill '{ref}' which does not exist in skills/live/")
            else:
                # Check deprecation
                ref_fm, _ = parse_frontmatter(ref_path)
                if ref_fm and ref_fm.get("deprecated"):
                    warn(f"{rel}: references deprecated skill '{ref}'")

def main():
    validate_skills()
    validate_packs()

    for w in warnings:
        print(f"WARN: {w}")
    for e in errors:
        print(f"ERROR: {e}")

    if warnings:
        print(f"\n{len(warnings)} warning(s)")
    if errors:
        print(f"{len(errors)} error(s)")
        sys.exit(1)
    print("Validation passed.")
    sys.exit(0)

if __name__ == "__main__":
    main()
