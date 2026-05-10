#!/usr/bin/env python3
"""Show pack contents and validation status."""

import sys
import re
from pathlib import Path
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
LIVE_DIR = REPO_ROOT / "skills" / "live"
PACKS_DIR = REPO_ROOT / "packs"

def parse_frontmatter(path):
    text = path.read_text()
    if not text.startswith("---"):
        return None, ""
    _, rest = text.split("---", 1)
    parts = rest.split("---", 1)
    if len(parts) != 2:
        return None, ""
    try:
        return yaml.safe_load(parts[0]), parts[1]
    except yaml.YAMLError:
        return None, ""

def pack_info(pack_id):
    pack_path = PACKS_DIR / f"{pack_id}.md"
    if not pack_path.exists():
        print(f"Pack not found: packs/{pack_id}.md")
        sys.exit(1)

    fm, body = parse_frontmatter(pack_path)
    if fm is None:
        print(f"Invalid frontmatter in packs/{pack_id}.md")
        sys.exit(1)

    print(f"\n=== Pack: {fm.get('name', pack_id)} ===")
    print(f"ID:          {fm.get('id')}")
    print(f"Audience:    {fm.get('audience')}")
    print(f"Curator:     {fm.get('curator')}")
    print(f"Onboarding:  {fm.get('estimated_onboarding')}")
    print(f"Last update: {fm.get('last_updated')}")

    refs = []
    for line in body.strip().splitlines():
        m = re.match(r"^-\s+([\w-]+)\s*$", line)
        if m:
            refs.append(m.group(1))

    print(f"\nSkills referenced ({len(refs)}):")
    for ref in refs:
        ref_path = LIVE_DIR / f"{ref}.md"
        if ref_path.exists():
            ref_fm, _ = parse_frontmatter(ref_path)
            if ref_fm and ref_fm.get("deprecated"):
                print(f"  ⚠ {ref:<30} DEPRECATED")
            else:
                ver = ref_fm.get("version", "?") if ref_fm else "?"
                print(f"  ✓ {ref:<30} v{ver}")
        else:
            print(f"  ✗ {ref:<30} MISSING from skills/live/")

def main():
    if len(sys.argv) != 2:
        print("Usage: pack-info.py <pack-id>")
        sys.exit(1)
    pack_info(sys.argv[1])

if __name__ == "__main__":
    main()
