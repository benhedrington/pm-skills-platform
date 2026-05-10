#!/usr/bin/env python3
"""List skills in one or all environments."""

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

def list_env(stage):
    stage_dir = REPO_ROOT / "skills" / stage
    if not stage_dir.exists():
        print(f"Directory not found: skills/{stage}/")
        return
    files = sorted(stage_dir.glob("*.md"))
    print(f"\n=== skills/{stage}/ ({len(files)} skills) ===")
    for fpath in files:
        fm = parse_frontmatter(fpath)
        if fm:
            status = "DEPRECATED" if fm.get("deprecated") else "active"
            print(f"  {fpath.stem:<30} v{fm.get('version', '?'):<10} {status}")
        else:
            print(f"  {fpath.stem:<30} [invalid frontmatter]")

def main():
    if len(sys.argv) > 1:
        env = sys.argv[1]
        if env not in SKILL_STAGES:
            print(f"Unknown environment: {env}. Use: dev, stage, live")
            sys.exit(1)
        list_env(env)
    else:
        for stage in SKILL_STAGES:
            list_env(stage)

if __name__ == "__main__":
    main()
