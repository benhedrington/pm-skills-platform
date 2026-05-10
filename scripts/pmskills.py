#!/usr/bin/env python3
"""
PM Skills Platform — Mechanical Helper
Manages dev/stage/live environments, validation, build, and publish.
Called by Claude Code slash commands or run directly.
"""

import argparse
import filecmp
import json
import os
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

import yaml

REQUIRED_SECTIONS = [
    "Context",
    "Role",
    "Principles",
    "Frameworks",
    "Anti-Patterns",
    "Examples",
]

GENERIC_VOICE_PHRASES = [
    "it's important to note",
    "in today's fast-paced world",
    "it's crucial to",
    "it's essential to",
    "remember that",
    "always remember",
    "don't forget to",
]

CATEGORIES = ["discovery", "delivery", "strategy", "stakeholders", "metrics"]


def load_config(root: Path) -> dict:
    path = root / "pmskills.config.yaml"
    if not path.exists():
        print(f"ERROR: No config found at {path}")
        print("Run /skill-init or 'python scripts/pmskills.py init' first.")
        sys.exit(1)
    with open(path) as f:
        return yaml.safe_load(f)


def resolve_path(base: Path, p: str) -> Path:
    """Resolve a path string relative to base or absolute."""
    q = Path(p)
    if q.is_absolute():
        return q
    return (base / q).resolve()


def get_env_path(config: dict, env: str) -> Path:
    """Get absolute path to an environment directory."""
    gold = Path(config["goldPath"])
    return gold / env


def detect_onedrive_candidates() -> list:
    home = Path.home()
    candidates = [
        home / "OneDrive",
        home / "OneDrive - Shared",
    ]
    # Also check for "OneDrive - <CompanyName>" patterns
    if home.exists():
        for d in home.iterdir():
            if d.is_dir() and d.name.startswith("OneDrive"):
                candidates.append(d)
    return [c for c in candidates if c.exists()]


def parse_frontmatter(file_path: Path) -> tuple:
    content = file_path.read_text()
    match = re.match(r"^---\n(.*?)\n---\n(.*)$", content, re.DOTALL)
    if not match:
        raise ValueError(f"Missing frontmatter in {file_path}")
    return yaml.safe_load(match.group(1)), match.group(2)


def parse_skill(file_path: Path) -> dict:
    front, body = parse_frontmatter(file_path)
    headers = re.findall(r"^##\s+(.+)$", body, re.MULTILINE)
    return {
        "frontmatter": front,
        "body": body,
        "headers": [h.strip() for h in headers],
        "word_count": len(body.split()),
    }


def validate_skill(file_path: Path, env_knowledge_dir: Path) -> list:
    errors = []
    try:
        skill = parse_skill(file_path)
    except Exception as e:
        return [str(e)]

    fm = skill["frontmatter"]
    for key in ["name", "category", "version", "author", "description"]:
        if key not in fm:
            errors.append(f"Missing frontmatter key: {key}")

    if "classification" not in fm:
        errors.append("Missing classification (internal/confidential)")

    headers = skill["headers"]
    for sec in REQUIRED_SECTIONS:
        if sec not in headers:
            errors.append(f"Missing required section: {sec}")

    # Anti-patterns
    ap_match = re.search(
        r"##\s*Anti[- ]?Patterns\s*\n(.*?)(?=\n##\s|\Z)",
        skill["body"],
        re.DOTALL | re.IGNORECASE,
    )
    if ap_match:
        ap_text = ap_match.group(1)
        bullets = re.findall(r"^[\s]*[-*\d]\.?\s+.*", ap_text, re.MULTILINE)
        subheaders = re.findall(r"^###\s+.*", ap_text, re.MULTILINE)
        total = len(bullets) + len(subheaders)
        if total < 3:
            errors.append(f"Only {total} anti-patterns (need 3+)")
    else:
        errors.append("Anti-Patterns section not found")

    # Examples
    ex_match = re.search(
        r"##\s*Examples\s*\n(.*?)(?=\n##\s|\Z)",
        skill["body"],
        re.DOTALL | re.IGNORECASE,
    )
    if ex_match:
        ex_text = ex_match.group(1)
        bullets = re.findall(r"^[\s]*[-*\d]\.?\s+.*", ex_text, re.MULTILINE)
        subheaders = re.findall(r"^###\s+.*", ex_text, re.MULTILINE)
        total = len(bullets) + len(subheaders)
        if total < 2:
            errors.append(f"Only {total} examples (need 2+)")
    else:
        errors.append("Examples section not found")

    # Knowledge refs
    requires = fm.get("requires_knowledge", [])
    for k in requires:
        k_path = env_knowledge_dir / f"{k}.md"
        if not k_path.exists():
            errors.append(f"Missing knowledge file: knowledge/{k}.md")

    # Word count
    if skill["word_count"] < 500:
        errors.append(f"Too short: {skill['word_count']} words (min 500)")

    # Generic voice
    body_lower = skill["body"].lower()
    for phrase in GENERIC_VOICE_PHRASES:
        if phrase in body_lower:
            errors.append(f"Generic voice phrase: '{phrase}'")

    return errors


def find_skill(env_dir: Path, skill_name: str) -> Path | None:
    skills_dir = env_dir / "skills"
    if not skills_dir.exists():
        return None
    for cat_dir in skills_dir.iterdir():
        if cat_dir.is_dir():
            candidate = cat_dir / f"{skill_name}.md"
            if candidate.exists():
                return candidate
    return None


def find_skill_envs(config: dict, skill_name: str) -> dict:
    """Find which environments contain a skill."""
    result = {}
    for env in ["dev", "stage", "live"]:
        p = find_skill(get_env_path(config, env), skill_name)
        if p:
            result[env] = p
    return result


def cmd_init(cwd: Path):
    print("Initializing PM Skills Gold Repository\n")

    # Ask for gold path
    default_gold = cwd / "pm-skills-gold"
    gold_input = input(f"Gold repository path [{default_gold}]: ").strip()
    gold_path = Path(gold_input) if gold_input else default_gold
    if not gold_path.is_absolute():
        gold_path = (cwd / gold_path).resolve()

    # Ask for output path
    onedrive_candidates = detect_onedrive_candidates()
    if onedrive_candidates:
        default_output = onedrive_candidates[0] / "PM-Skills-Platform"
        print(f"\nDetected OneDrive folders: {[str(c) for c in onedrive_candidates]}")
    else:
        default_output = gold_path / "output"
        print("\nNo OneDrive folder detected.")

    out_input = input(f"Output path (where PMs grab packages) [{default_output}]: ").strip()
    output_path = Path(out_input) if out_input else default_output
    if not output_path.is_absolute():
        output_path = (cwd / output_path).resolve()

    # Ask for org name
    org = input("Org name [my-org]: ").strip() or "my-org"

    # Create directories
    for env in ["dev", "stage", "live"]:
        for sub in ["skills", "knowledge", "reviews"]:
            p = gold_path / env / sub
            p.mkdir(parents=True, exist_ok=True)
        for cat in CATEGORIES:
            (gold_path / env / "skills" / cat).mkdir(parents=True, exist_ok=True)

    (gold_path / "packages").mkdir(parents=True, exist_ok=True)
    (gold_path / "templates").mkdir(parents=True, exist_ok=True)

    # Create incoming folder in output
    incoming_dir = output_path / "incoming"
    incoming_dir.mkdir(parents=True, exist_ok=True)
    (incoming_dir / "archive").mkdir(exist_ok=True)
    (incoming_dir / "rejected").mkdir(exist_ok=True)

    # Write config
    config = {
        "org": org,
        "goldPath": str(gold_path),
        "outputPath": str(output_path),
        "categories": CATEGORIES,
        "version": "1.0.0",
    }
    with open(gold_path / "pmskills.config.yaml", "w") as f:
        yaml.dump(config, f, sort_keys=False)

    # Write starter knowledge templates to dev/
    for env in ["dev", "stage", "live"]:
        write_knowledge_templates(gold_path / env / "knowledge")

    # Write skill template
    write_skill_template(gold_path / "templates")

    # Write contribution template to output
    write_contribution_template(output_path)

    print(f"\nCreated gold repository at: {gold_path}")
    print(f"  dev/    → Draft skills")
    print(f"  stage/  → Under review")
    print(f"  live/   → Certified")
    print(f"\nOutput path: {output_path}")
    print(f"  incoming/  → PM contributions (shared)")
    print(f"\nConfig written to: {gold_path / 'pmskills.config.yaml'}")
    print("\nNext steps:")
    print("  1. cd into your gold repository")
    print("  2. Run 'python scripts/pmskills.py validate --env dev' after adding skills")
    print("  3. Run 'python scripts/pmskills.py build --version 1.0.0' from live/")
    print("  4. Tell PMs to drop contributions in: <outputPath>/incoming/")
    print("     (There's a CONTRIBUTION-TEMPLATE.md there to help them)")


def write_knowledge_templates(knowledge_dir: Path):
    company = """---
name: company-context
type: knowledge
version: 1.0.0
classification: internal
---

# Company Context

## Who We Are
[Your company description, mission, strategic priorities]

## How We Work
[Operating model, team structure, decision-making norms]

## Terminology
[Org-specific terms, acronyms, product names]
"""
    tech = """---
name: tech-landscape
type: knowledge
version: 1.0.0
classification: internal
---

# Tech Landscape

## Architecture Overview
[High-level system architecture, major platforms]

## Constraints & Non-Negotiables
[Compliance, security, legacy systems, budget limits]

## Key Vendors & Platforms
[Critical SaaS, cloud providers, internal tools]
"""
    wow = """---
name: ways-of-working
type: knowledge
version: 1.0.0
classification: internal
---

# Ways of Working

## Team Norms
[Working hours, async vs sync, communication channels]

## Ceremonies
[Sprint planning, retros, stakeholder reviews]

## Planning Cadence
[Quarterly OKRs, annual roadmap, release cycles]

## Decision Making
[RACI, escalation paths, approval gates]
"""
    (knowledge_dir / "company-context.md").write_text(company)
    (knowledge_dir / "tech-landscape.md").write_text(tech)
    (knowledge_dir / "ways-of-working.md").write_text(wow)


def write_skill_template(templates_dir: Path):
    template = """---
name: {{NAME}}
category: {{CATEGORY}}
version: 0.1.0
author: skill-admin
requires_knowledge: [company-context]
description: {{DESCRIPTION}}
classification: internal
---

# {{NAME}}

## Context
What this skill covers and when to use it.

## Role
The perspective the AI should adopt.

## Principles
Opinionated guidelines. 3-5 max.

## Frameworks
Mental models and approaches.

## Anti-Patterns
What bad looks like. At least 3 specific, concrete items.

## Examples
Concrete input/output pairs. At least 2.
"""
    (templates_dir / "skill-template.md").write_text(template)


def write_contribution_template(output_dir: Path):
    template = """# Contributing Skills & Feedback

Have an idea for a new skill? Found an issue with an existing one? Want to share a framework your team uses?

Drop a file in this `incoming/` folder. The skill admin reviews it weekly.

## How to Submit

Create a new markdown file named something like:
- `exec-comms-feedback.md`
- `new-retro-skill.md`
- `discovery-fix-june.md`

Use this format:

```markdown
---
contribution_type: [new-skill | skill-fix | idea | feedback]
skill_name: [if applicable]
category: [discovery | delivery | strategy | stakeholders | metrics]
author: [your name or team]
date: [YYYY-MM-DD]
---

# [Title of your contribution]

## Context
What prompted this? What problem are you solving?

## Content
The actual suggestion, fix, or draft skill text.

## Why This Matters
How would this help PMs in our org?
```

## What Happens Next

1. The skill admin reviews your submission.
2. If it's a good fit, it gets imported into the dev pipeline, edited, and eventually certified.
3. You may get pinged for clarification.
4. Check the release announcements to see when your contribution ships.

## Tips

- **Be specific.** "Add more examples" is less helpful than "Here's a real scenario we faced last quarter..."
- **Share war stories.** Anti-patterns and examples grounded in real experience are gold.
- **Don't worry about format.** The admin will rewrite it into proper skill structure. Focus on the substance.
- **Anonymous is fine.** If you don't want to put your name, use "Anonymous PM" or "Platform Team".

## Questions?

Contact your skill admin or post in the PM guild channel.
"""
    (output_dir / "CONTRIBUTION-TEMPLATE.md").write_text(template)


def cmd_validate(config: dict, env: str, target: str):
    env_dir = get_env_path(config, env)
    if not env_dir.exists():
        print(f"ERROR: Environment '{env}' not found at {env_dir}")
        sys.exit(1)

    knowledge_dir = env_dir / "knowledge"
    skills_dir = env_dir / "skills"

    files = []
    if target == "--all":
        for cat_dir in skills_dir.iterdir():
            if cat_dir.is_dir():
                files.extend(cat_dir.glob("*.md"))
    else:
        p = Path(target)
        if not p.is_absolute():
            # Try to find by name in the environment
            found = find_skill(env_dir, target)
            if found:
                p = found
            else:
                p = env_dir / target
        files = [p] if p.exists() else []

    if not files:
        print(f"No skills found to validate in {env}")
        return True

    all_pass = True
    for f in files:
        rel = f.relative_to(env_dir)
        errors = validate_skill(f, knowledge_dir)
        if errors:
            print(f"✗ {rel}")
            for e in errors:
                print(f"    - {e}")
            all_pass = False
        else:
            print(f"✓ {rel}")
    return all_pass


def cmd_promote(config: dict, skill_name: str, from_env: str, to_env: str, with_knowledge: bool = True):
    from_dir = get_env_path(config, from_env)
    to_dir = get_env_path(config, to_env)

    src = find_skill(from_dir, skill_name)
    if not src:
        print(f"ERROR: Skill '{skill_name}' not found in {from_env}")
        # List available
        avail = []
        for cat_dir in (from_dir / "skills").iterdir():
            if cat_dir.is_dir():
                avail.extend([f.stem for f in cat_dir.glob("*.md")])
        if avail:
            print(f"Available in {from_env}: {', '.join(avail)}")
        sys.exit(1)

    # Parse to get category
    try:
        fm, _ = parse_frontmatter(src)
        category = fm.get("category", "uncategorized")
    except Exception:
        category = src.parent.name

    dest_dir = to_dir / "skills" / category
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / src.name
    shutil.copy2(src, dest)

    # Knowledge files
    if with_knowledge:
        try:
            fm, _ = parse_frontmatter(src)
            requires = fm.get("requires_knowledge", [])
        except Exception:
            requires = []

        from_know = from_dir / "knowledge"
        to_know = to_dir / "knowledge"
        to_know.mkdir(parents=True, exist_ok=True)

        for k in requires:
            k_src = from_know / f"{k}.md"
            k_dst = to_know / f"{k}.md"
            if k_src.exists():
                if k_dst.exists():
                    # Check if newer in to
                    if k_dst.stat().st_mtime > k_src.stat().st_mtime:
                        print(f"  ⚠ knowledge/{k}.md exists in {to_env} and is newer. Skipped copy.")
                        continue
                shutil.copy2(k_src, k_dst)
                print(f"  → Copied knowledge/{k}.md")

    # Create review stub for stage
    if to_env == "stage":
        reviews_dir = to_dir / "reviews"
        reviews_dir.mkdir(parents=True, exist_ok=True)
        review_file = reviews_dir / f"{skill_name}-{datetime.now().strftime('%Y%m%d')}.md"
        review_stub = f"""# Review: {skill_name}

Date: {datetime.now().strftime('%Y-%m-%d')}
Reviewer: [Name]
Environment: stage

## Verdict
[PASS / PASS WITH EDITS / FAIL]

## Strengths

## Issues

## Suggested Edits
"""
        review_file.write_text(review_stub)
        print(f"  → Created review stub: {review_file}")

    print(f"\nPromoted '{skill_name}' from {from_env} → {to_env}")
    if to_env == "stage":
        print("Next: Run /skill-review or ask a peer to review.")
    elif to_env == "live":
        print("Next: Ready to build and publish.")


def cmd_diff(config: dict, skill_name: str | None, from_env: str, to_env: str):
    from_dir = get_env_path(config, from_env)
    to_dir = get_env_path(config, to_env)

    print(f"Comparing {from_env} → {to_env}\n")

    # Skills
    print("Skills:")
    from_skills = {}
    for cat_dir in (from_dir / "skills").iterdir():
        if cat_dir.is_dir():
            for f in cat_dir.glob("*.md"):
                from_skills[f.stem] = f

    to_skills = {}
    for cat_dir in (to_dir / "skills").iterdir():
        if cat_dir.is_dir():
            for f in cat_dir.glob("*.md"):
                to_skills[f.stem] = f

    if skill_name:
        # Single skill diff
        if skill_name not in from_skills:
            print(f"  {skill_name}: not found in {from_env}")
        elif skill_name not in to_skills:
            print(f"  {skill_name}: only in {from_env} (not yet promoted)")
        else:
            identical = filecmp.cmp(from_skills[skill_name], to_skills[skill_name], shallow=False)
            if identical:
                print(f"  {skill_name}: identical")
            else:
                print(f"  {skill_name}: MODIFIED")
    else:
        # All skills
        all_names = sorted(set(from_skills.keys()) | set(to_skills.keys()))
        pending = 0
        for name in all_names:
            if name in from_skills and name in to_skills:
                identical = filecmp.cmp(from_skills[name], to_skills[name], shallow=False)
                if identical:
                    print(f"  ✓ {name}.md  identical")
                else:
                    print(f"  ✗ {name}.md  modified")
            elif name in from_skills:
                print(f"  → {name}.md  only in {from_env}")
                pending += 1
            else:
                print(f"  ← {name}.md  only in {to_env}")
        if pending:
            print(f"\nPending promotion: {pending} skill(s)")

    # Knowledge files
    print("\nKnowledge:")
    from_know = {f.stem: f for f in (from_dir / "knowledge").glob("*.md") if f.is_file()}
    to_know = {f.stem: f for f in (to_dir / "knowledge").glob("*.md") if f.is_file()}
    all_know = sorted(set(from_know.keys()) | set(to_know.keys()))
    for name in all_know:
        if name in from_know and name in to_know:
            identical = filecmp.cmp(from_know[name], to_know[name], shallow=False)
            print(f"  {'✓' if identical else '✗'} {name}.md  {'identical' if identical else 'modified'}")
        elif name in from_know:
            print(f"  → {name}.md  only in {from_env}")
        else:
            print(f"  ← {name}.md  only in {to_env}")


def cmd_build(config: dict, version: str):
    live_dir = get_env_path(config, "live")
    if not live_dir.exists():
        print("ERROR: live/ environment not found")
        sys.exit(1)

    # Validate all in live first
    ok = cmd_validate(config, "live", "--all")
    if not ok:
        print("\nBuild blocked: fix validation errors in live/ first.")
        sys.exit(1)

    pkg_name = f"live-{version}"
    gold_path = Path(config["goldPath"])
    pkg_dir = gold_path / "packages" / pkg_name
    if pkg_dir.exists():
        shutil.rmtree(pkg_dir)
    pkg_dir.mkdir(parents=True)

    manifest = {
        "name": pkg_name,
        "version": version,
        "built_at": datetime.now().isoformat(),
        "skills": [],
        "knowledge": [],
    }

    skills_dir = live_dir / "skills"
    for cat_dir in skills_dir.iterdir():
        if cat_dir.is_dir():
            for f in cat_dir.glob("*.md"):
                fm, _ = parse_frontmatter(f)
                manifest["skills"].append({
                    "name": fm.get("name", f.stem),
                    "category": fm.get("category", cat_dir.name),
                    "file": f.name,
                })
                shutil.copy(f, pkg_dir / f"{fm.get('name', f.stem)}.md")

    # Copy all knowledge files from live/
    know_dir = live_dir / "knowledge"
    if know_dir.exists():
        for f in know_dir.glob("*.md"):
            manifest["knowledge"].append(f.stem)
            shutil.copy(f, pkg_dir / f.name)

    with open(pkg_dir / "manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)

    readme = generate_install_readme(pkg_name, version, manifest)
    with open(pkg_dir / "README-INSTALL.md", "w") as f:
        f.write(readme)

    print(f"Built package: {pkg_dir}")
    print(f"  Skills: {len(manifest['skills'])}")
    print(f"  Knowledge: {len(manifest['knowledge'])}")
    return pkg_dir


def generate_install_readme(pkg_name: str, version: str, manifest: dict) -> str:
    skills_list = "\n".join(f"- `{s['name']}` ({s['category']})" for s in manifest["skills"])
    know_list = "\n".join(f"- `{k}`" for k in manifest["knowledge"])

    return f"""# {pkg_name} — Install Guide

**Version:** {version}  
**Built:** {manifest["built_at"]}

## What's Included

### Skills
{skills_list}

### Knowledge Files
{know_list}

## Install into Claude Projects

1. Open [Claude.ai](https://claude.ai) → Projects → Create Project
2. Go to **Project Settings** → **Custom Instructions**
3. Copy the full text of each skill `.md` file into the **Instructions** box
4. For knowledge files, paste into **Knowledge** or upload as documents
5. Name the project descriptively (e.g., "PM Discovery Skills")

## Install into ChatGPT Custom Instructions

1. Settings → Custom Instructions
2. Paste **Context** and **Role** into "What would you like ChatGPT to know?"
3. Paste **Principles** and **Frameworks** into "How would you like ChatGPT to respond?"

## Install into Claude Code (Terminal)

1. `cd` into your project
2. Copy skills to `.claude/skills/`
3. Reference in prompts: "Using the opportunity-assessment skill, evaluate..."

## Updating

When a new version is published:
1. Download the new package from your org's shared folder
2. Replace the old skill text in your AI tool
3. Check release notes in the manifest

---
*Built with PM Skills Platform*
"""


def cmd_publish(config: dict, package_name: str):
    output = Path(config["outputPath"])
    if not output.exists():
        print(f"Output path does not exist: {output}")
        create = input("Create it? [Y/n]: ").strip().lower()
        if create in ("", "y", "yes"):
            output.mkdir(parents=True, exist_ok=True)
            print(f"Created: {output}")
        else:
            print("Aborting publish.")
            sys.exit(1)

    gold_path = Path(config["goldPath"])
    pkg_dir = gold_path / "packages" / package_name
    if not pkg_dir.exists():
        print(f"ERROR: Package not found: {pkg_dir}")
        print("Run build first.")
        sys.exit(1)

    dest = output / "packages" / package_name
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(pkg_dir, dest)

    # Update catalog
    catalog = output / "index.md"
    entry = f"- **{package_name}** — {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
    if catalog.exists():
        with open(catalog, "a") as f:
            f.write(entry)
    else:
        catalog.write_text(f"# PM Skills Catalog\n\n{entry}")

    # Ensure incoming folder exists in output
    (output / "incoming").mkdir(exist_ok=True)
    (output / "incoming" / "archive").mkdir(exist_ok=True)
    (output / "incoming" / "rejected").mkdir(exist_ok=True)

    # Generate announcement
    manifest_path = pkg_dir / "manifest.json"
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    skills = ", ".join(s["name"] for s in manifest.get("skills", []))
    announce = f"""# New Skill Release: {package_name}

**Published:** {datetime.now().strftime('%Y-%m-%d')}
**Skills included:** {skills}

## What's New
[Describe changes since last release]

## How to Install
1. Open the shared folder: {output}
2. Find the package: `{package_name}/`
3. Open `README-INSTALL.md` for copy-paste instructions
4. Paste skills into Claude Projects or ChatGPT Custom Instructions

## Who Should Install This
- [ ] PMs working on [area]
- [ ] Team leads preparing for [event]

---
*Questions? Contact your skill admin.*

## Have Feedback or Ideas?
Drop a file in the `incoming/` folder! See `CONTRIBUTION-TEMPLATE.md` for how.
"""
    announce_path = gold_path / "packages" / f"ANNOUNCEMENT-{package_name}.md"
    announce_path.write_text(announce)

    print(f"Published to: {dest}")
    print(f"Catalog: {catalog}")
    print(f"Announcement: {announce_path}")
    print(f"Incoming folder: {output / 'incoming'}")
    print("\nNext: Verify files appear in your shared drive, then post the announcement.")
    print("Remind PMs they can submit feedback via the incoming/ folder.")


def cmd_inbox(config: dict, action: str | None, filename: str | None, import_to_dev: bool, reject_reason: str | None, sweep: bool):
    output = Path(config["outputPath"])
    incoming = output / "incoming"
    if not incoming.exists():
        print(f"ERROR: Incoming folder does not exist: {incoming}")
        sys.exit(1)

    gold_path = Path(config["goldPath"])
    dev_dir = gold_path / "dev"

    if sweep:
        files = [f for f in incoming.iterdir() if f.is_file() and f.suffix == ".md"]
        for f in files:
            print(f"\n{'='*60}")
            print(f"Processing: {f.name}")
            print(f"{'='*60}")
            try:
                content = f.read_text()
                print(content[:500])
                if len(content) > 500:
                    print("... [truncated]")
            except Exception as e:
                print(f"Error reading file: {e}")
                continue
            choice = input("\nAction? [i]mport to dev / [r]eject / [s]kip / [q]uit: ").strip().lower()
            if choice == "i":
                _import_incoming(gold_path, dev_dir, f)
            elif choice == "r":
                reason = input("Rejection reason (optional): ").strip()
                _reject_incoming(incoming, f, reason)
            elif choice == "q":
                print("Stopping sweep.")
                break
            else:
                print("Skipped.")
        return

    if action == "list" or not filename:
        files = [f for f in incoming.iterdir() if f.is_file() and f.suffix == ".md"]
        if not files:
            print("No submissions in inbox.")
            return
        print(f"\nIncoming submissions ({len(files)}):")
        for f in files:
            stat = f.stat()
            size = stat.st_size
            modified = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M")
            preview = ""
            try:
                lines = f.read_text().splitlines()[:3]
                preview = " | ".join(lines[:2])
            except Exception:
                pass
            print(f"  - {f.name} ({size} bytes, {modified})")
            if preview:
                print(f"    {preview[:80]}...")
        print(f"\nPath: {incoming}")
        return

    if filename:
        f = incoming / filename
        if not f.exists():
            print(f"ERROR: File not found in inbox: {f}")
            # List available
            avail = [x.name for x in incoming.iterdir() if x.is_file() and x.suffix == ".md"]
            if avail:
                print(f"Available: {', '.join(avail)}")
            sys.exit(1)

        if reject_reason:
            _reject_incoming(incoming, f, reject_reason)
            print(f"Rejected: {f.name}")
            print(f"  Reason: {reject_reason}")
            print(f"  Moved to: {incoming / 'rejected' / f.name}")
            return

        if import_to_dev:
            _import_incoming(gold_path, dev_dir, f)
            print(f"Imported: {f.name}")
            print(f"  To dev environment")
            print("Next: Run /skill-validate --env dev and /skill-review")
            return

        # Default: just show the file
        print(f.read_text())
        print(f"\nFile: {f}")
        print("Use --import-to-dev or --reject to act on it.")


def _import_incoming(gold_path: Path, dev_dir: Path, file: Path):
    """Import an incoming file into dev environment."""
    content = file.read_text()

    # Try to parse as skill
    try:
        fm, body = parse_frontmatter(file)
        is_skill = True
    except Exception:
        fm = {}
        body = content
        is_skill = False

    # Determine category
    category = fm.get("category", "uncategorized")
    if category not in CATEGORIES:
        category = "uncategorized"

    name = fm.get("name", file.stem)
    if not name:
        name = file.stem

    target_dir = dev_dir / "skills" / category
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / f"{name}.md"

    # Rewrite frontmatter if it's a contribution format
    if is_skill:
        # Check if it has contribution_type marker
        contrib_type = fm.get("contribution_type", "")
        if contrib_type:
            # Rewrite as a proper draft skill
            new_fm = {
                "name": name,
                "category": category,
                "version": "0.0.0-contributed",
                "author": fm.get("author", "contributor"),
                "requires_knowledge": fm.get("requires_knowledge", ["company-context"]),
                "description": fm.get("description", f"Contributed skill: {name}"),
                "classification": fm.get("classification", "internal"),
                "source": f"incoming/{file.name}",
            }
            new_content = f"---\n{yaml.dump(new_fm, sort_keys=False)}---\n\n{body}"
            target.write_text(new_content)
        else:
            # Already a proper skill, just copy with source annotation
            fm["source"] = f"incoming/{file.name}"
            if "version" not in fm or not fm.get("version"):
                fm["version"] = "0.0.0-contributed"
            new_content = f"---\n{yaml.dump(fm, sort_keys=False)}---\n\n{body}"
            target.write_text(new_content)
    else:
        # Free-form feedback — create a review note instead
        reviews_dir = dev_dir / "reviews"
        reviews_dir.mkdir(parents=True, exist_ok=True)
        note = f"""# Incoming Feedback: {file.name}

Date: {datetime.now().strftime('%Y-%m-%d')}
Source: incoming/{file.name}

## Content

{content}

## Action Needed
- [ ] Review and decide if this should become a skill or knowledge update
"""
        note_file = reviews_dir / f"incoming-{file.stem}-{datetime.now().strftime('%Y%m%d')}.md"
        note_file.write_text(note)
        print(f"  Created feedback note: {note_file}")
        # Don't delete free-form files automatically
        return

    # Move original to archive
    archive_dir = (file.parent / "archive")
    archive_dir.mkdir(exist_ok=True)
    shutil.move(str(file), str(archive_dir / f"{file.stem}-{datetime.now().strftime('%Y%m%d')}{file.suffix}"))
    print(f"  Archived original to: {archive_dir}")
    print(f"  Imported as: {target}")


def _reject_incoming(incoming_dir: Path, file: Path, reason: str = ""):
    rejected = incoming_dir / "rejected"
    rejected.mkdir(exist_ok=True)
    dest = rejected / f"{file.stem}-{datetime.now().strftime('%Y%m%d')}{file.suffix}"
    shutil.move(str(file), str(dest))
    if reason:
        note = rejected / f"{dest.stem}-reason.txt"
        note.write_text(f"Rejected: {datetime.now().isoformat()}\nReason: {reason}\n")
    print(f"  Rejected and moved to: {dest}")


def main():
    parser = argparse.ArgumentParser(description="PM Skills Platform")
    sub = parser.add_subparsers(dest="command")

    init = sub.add_parser("init", help="Initialize gold repository")

    val = sub.add_parser("validate", help="Validate skills")
    val.add_argument("target", nargs="?", default="--all")
    val.add_argument("--env", default="dev", choices=["dev", "stage", "live"])

    promote = sub.add_parser("promote", help="Promote skill between environments")
    promote.add_argument("skill_name")
    promote.add_argument("--from", dest="from_env", required=True, choices=["dev", "stage"])
    promote.add_argument("--to", dest="to_env", required=True, choices=["stage", "live"])
    promote.add_argument("--with-knowledge", action="store_true", default=True)

    diff = sub.add_parser("diff", help="Compare environments")
    diff.add_argument("skill_name", nargs="?")
    diff.add_argument("--from", dest="from_env", default="dev")
    diff.add_argument("--to", dest="to_env", default="stage")

    build = sub.add_parser("build", help="Build package from live")
    build.add_argument("--version", default=datetime.now().strftime("%Y.%m.%d"))

    pub = sub.add_parser("publish", help="Publish to output")
    pub.add_argument("--package", required=True)

    inbox = sub.add_parser("inbox", help="Process incoming contributions")
    inbox.add_argument("--action", choices=["list", "process"], default="list")
    inbox.add_argument("--file", help="Specific file to process")
    inbox.add_argument("--import-to-dev", action="store_true", help="Import to dev environment")
    inbox.add_argument("--reject", help="Reject with reason")
    inbox.add_argument("--sweep", action="store_true", help="Process all files interactively")

    args = parser.parse_args()
    cwd = Path.cwd()

    if args.command == "init":
        cmd_init(cwd)
    elif args.command == "validate":
        config = load_config(cwd)
        ok = cmd_validate(config, args.env, args.target)
        sys.exit(0 if ok else 1)
    elif args.command == "promote":
        config = load_config(cwd)
        cmd_promote(config, args.skill_name, args.from_env, args.to_env, args.with_knowledge)
    elif args.command == "diff":
        config = load_config(cwd)
        cmd_diff(config, args.skill_name, args.from_env, args.to_env)
    elif args.command == "build":
        config = load_config(cwd)
        cmd_build(config, args.version)
    elif args.command == "publish":
        config = load_config(cwd)
        cmd_publish(config, args.package)
    elif args.command == "inbox":
        config = load_config(cwd)
        cmd_inbox(config, args.action, args.file, args.import_to_dev, args.reject, args.sweep)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
