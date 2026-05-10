#!/usr/bin/env python3
"""Scaffold the PM Skills Platform directory structure."""

import os
import sys
from pathlib import Path
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent

def ask_path(prompt, default):
    display = str(default)
    user_input = input(f"{prompt} [{display}]: ").strip()
    return Path(user_input).resolve() if user_input else default

def init():
    print("=== PM Skills Platform Initialization ===\n")

    gold = ask_path("Gold repository path (dev/stage/live location)", REPO_ROOT)
    output = ask_path("Output path (shared folder for teams)", REPO_ROOT / "output")

    dirs = [
        gold / "skills" / "dev",
        gold / "skills" / "stage",
        gold / "skills" / "live",
        gold / "packs",
        gold / "scripts",
        gold / "templates",
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)
        print(f"Ensured: {d}")

    config_path = gold / "config.yaml"
    config = {
        "org": input("Organization name [my-org]: ").strip() or "my-org",
        "goldPath": str(gold),
        "outputPath": str(output),
        "version": "1.0.0",
    }
    config_path.write_text(yaml.dump(config, default_flow_style=False, sort_keys=False))
    print(f"\nWritten: {config_path}")
    print(f"\nNext steps:")
    print(f"  1. Create skills: /pm-skills-new <skill-id>")
    print(f"  2. Share this folder with teams: {gold / 'skills' / 'live'}")
    print(f"  3. Built packages go to: {output}")

if __name__ == "__main__":
    init()
