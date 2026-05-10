# Consumer Guide — PM Skills Platform

## Who This Is For

You are a product manager who wants better AI assistance. Your org has a skill admin who maintains a certified library of AI context.

## What You Get

A **skill package** is a folder of markdown files. When you paste them into Claude or ChatGPT, your AI stops giving generic advice and starts giving advice shaped by your org's frameworks, terminology, and constraints.

## Finding Packages

1. Open your org's shared folder (OneDrive, SharePoint, network drive, etc.)
2. Look for `PM-Skills-Platform/` or whatever your admin named it
3. Browse `packages/` for versioned bundles
4. Open `index.md` for a catalog of what's available

Each package contains:
- Skill `.md` files (the AI instructions)
- Knowledge `.md` files (org context)
- `README-INSTALL.md` (step-by-step install guide)
- `manifest.json` (what's included)

## Installing

### Claude Projects (Best for recurring work)

1. Go to [Claude.ai](https://claude.ai) → **Projects** → **Create Project**
2. Name it: "PM Discovery Skills" or whatever fits
3. **Project Settings** → **Custom Instructions**
4. Copy the full text of a skill `.md` file into the **Instructions** box
5. Copy knowledge files into **Knowledge** (or upload as documents)
6. Save

**To use it:** Start a chat in that project. Say:
- "Using the opportunity-assessment skill, evaluate whether we should build..."

### ChatGPT Custom Instructions (Best for quick use)

1. Settings → **Custom Instructions**
2. "What would you like ChatGPT to know?" → Paste **Context** and **Role**
3. "How would you like ChatGPT to respond?" → Paste **Principles** and **Frameworks**

**Limit:** ~1500 words. For longer skills, use Claude Projects.

### Claude Code (Terminal)

1. `cd` your work project
2. `mkdir -p .claude/skills`
3. Copy skill files: `cp ~/Downloads/opportunity-assessment.md .claude/skills/`
4. In Claude Code: "Using the opportunity-assessment skill, help me..."

## Tips

- **Start with one skill.** Pick what you're working on right now. Add more later.
- **Combine skills.** Load multiple into one Claude Project. "Roadmap Prioritization" + "Exec Comms" = prioritized roadmap with exec-ready rationale.
- **Reference explicitly.** The more you name the skill, the better it performs:
  - ❌ "Help me write this email"
  - ✅ "Using the exec-comms skill, draft a quarterly review email"
- **Give feedback.** If a skill feels wrong, tell your skill admin. Skills are living documents.

## Contributing Back

Your org's skill library gets better when you share what you learn. If you:
- Found an anti-pattern the skill missed
- Have a real example that would make a skill better
- Built a framework your team uses that others should know about
- Noticed the skill gives advice that doesn't work at your company

**Submit it!**

1. Open your org's shared output folder (where you get packages from)
2. Find the `incoming/` folder
3. Read `CONTRIBUTION-TEMPLATE.md` for the format
4. Drop your markdown file in `incoming/`
5. The skill admin reviews it and may include it in the next release

No git, no PRs, no approval process — just write it and drop it.

## Updating

When your admin announces a new version:
1. Download the new package from the shared folder
2. In your AI tool, replace the old skill text with the new version
3. Update knowledge files if they changed

Keep a personal list:
```
Claude Project "PM Discovery":
  - opportunity-assessment v1.2.0
  - exec-comms v1.1.0
```

## FAQ

**Q: Do I need to understand prompt engineering?**
A: No. The admin did that work. You copy and paste.

**Q: Can I edit the skill myself?**
A: You can, but your edits won't be shared. Better to suggest changes to the admin.

**Q: What if my company doesn't use Claude?**
A: Skills are just markdown. Paste them into any AI tool that accepts text instructions.

**Q: Are skills confidential?**
A: Check the `classification` field. `internal` = share within company. `confidential` = be more careful. Don't post on public forums.

## Need Help?

Contact your skill admin (the person who posted the package announcement).
