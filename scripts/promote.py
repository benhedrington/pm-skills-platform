#!/usr/bin/env python3
"""Promote a skill through the dev/stage/live pipeline."""

import sys
import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_STAGES = ["dev", "stage", "live"]
VALID_TRANSITIONS = {("dev", "stage"), ("stage", "live")}

def promote(skill_id: str, from_stage: str, to_stage: str):
    if from_stage not in SKILL_STAGES or to_stage not in SKILL_STAGES:
        print(f"Invalid stage. Use: {', '.join(SKILL_STAGES)}")
        sys.exit(1)
    if (from_stage, to_stage) not in VALID_TRANSITIONS:
        print(f"Invalid transition: {from_stage} -> {to_stage}. Valid: dev->stage, stage->live")
        sys.exit(1)

    src = REPO_ROOT / "skills" / from_stage / f"{skill_id}.md"
    dst_dir = REPO_ROOT / "skills" / to_stage
    dst = dst_dir / f"{skill_id}.md"

    if not src.exists():
        print(f"Skill not found: {src.relative_to(REPO_ROOT)}")
        sys.exit(1)

    # If promoting to live, ensure we are not overwriting a non-deprecated skill without warning
    if to_stage == "live" and dst.exists():
        import yaml
        text = dst.read_text()
        _, rest = text.split("---", 1)
        parts = rest.split("---", 1)
        try:
            fm = yaml.safe_load(parts[0])
        except Exception:
            fm = {}
        if not fm.get("deprecated", False):
            print(f"ERROR: live skill '{skill_id}' exists and is not deprecated.")
            print("To replace it, mark the live version as deprecated first, or use a new skill id.")
            sys.exit(1)

    dst_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    print(f"Promoted: skills/{from_stage}/{skill_id}.md -> skills/{to_stage}/{skill_id}.md")

    # Optionally remove from source stage (keep it for traceability; uncomment to move instead of copy)
    # src.unlink()
    # print(f"Removed source: skills/{from_stage}/{skill_id}.md")

def main():
    if len(sys.argv) != 4:
        print("Usage: promote.py <skill-id> <from-stage> <to-stage>")
        print("Example: promote.py roadmap-basics stage live")
        sys.exit(1)
    skill_id, from_stage, to_stage = sys.argv[1], sys.argv[2], sys.argv[3]
    promote(skill_id, from_stage, to_stage)

if __name__ == "__main__":
    main()
