# What Is PM Skills Platform?

## The Problem

Most enterprise PMs have access to Claude or ChatGPT through their company. But they're not getting much out of it.

Every conversation starts from zero. The AI doesn't know how their org works. It doesn't know their tech stack, their decision-making norms, or their terminology. It gives generic advice that sounds reasonable but doesn't actually fit their constraints.

The result: PMs use a Ferrari to check email. They ask the AI to rewrite a sentence or summarize a doc, but they never unlock the real leverage — structured thinking, framework application, institutional knowledge — because nobody packaged that context.

Meanwhile, there's always *that one PM* in every org who figured it out. They spent hours crafting custom instructions. They built a personal library of prompts. They're 10x more effective than everyone else. But that knowledge is trapped in their head and their private Claude Projects.

## The Insight

The gap isn't AI capability. The gap is **distribution**.

One person — a skill admin — can curate, package, and distribute AI context to an entire PM org. The admin does the hard work of structuring institutional knowledge into reusable skill files. Everyone else benefits without needing to understand prompt engineering.

This is analogous to how design systems work. One designer maintains the component library. Every product team uses it without needing to be an expert in accessibility, spacing, or brand guidelines. The leverage is in the packaging.

## What a Skill Actually Is

A skill is a structured markdown file with three parts:

**1. Frontmatter (metadata)**
```yaml
name: opportunity-assessment
category: discovery
version: 1.0.0
author: skill-admin
requires_knowledge: [company-context]
classification: internal
```

**2. Sections that shape AI behavior**
- **Context** — when to use this skill, what situation the PM is in
- **Role** — the perspective the AI should adopt (senior PM, skeptical by default)
- **Principles** — 3-5 opinionated guidelines that shape responses
- **Frameworks** — named mental models with steps and key questions
- **Anti-Patterns** — concrete mistakes with "why it happens" and "how to catch it"
- **Examples** — realistic input/output pairs showing the skill in action

**3. Optional knowledge references**
Skills can reference org-specific knowledge files (company context, tech landscape, ways of working). When a skill is loaded, the AI's advice is grounded in how your actual company operates.

A skill is not a prompt template. A prompt template is something you paste once. A skill is persistent context that shapes every conversation in a Claude Project or ChatGPT Custom Instructions session.

## The Three-Environment Pipeline

Skills don't go straight from idea to production. They move through three environments:

### dev — "The Workshop"
Drafts, experiments, imported external skills. Things can be rough here. The admin validates them with `/skill-validate` but the quality bar is "good enough to review."

### stage — "The Review Queue"
Validated skills await peer review. A senior PM or the skill admin runs `/skill-review`, checking for accuracy, org fit, tone, and practical utility. Review notes are stored in `stage/reviews/`.

Nothing leaves stage without a review document.

### live — "The Certified Library"
Only reviewed, approved skills reach live. This is the source of truth. From here, the admin runs `/skill-build` to create versioned packages and `/skill-publish` to copy them to the shared output folder.

PMs should never see skills that haven't passed through this pipeline.

## The Feedback Loop: incoming/

Here's where it gets interesting. The shared output folder isn't just for distribution — it's also for intake.

Every package release includes:
- `packages/` — the skill bundles
- `index.md` — a catalog
- `incoming/` — a folder where PMs drop contributions
- `CONTRIBUTION-TEMPLATE.md` — a guide for what to write

A PM uses a skill, notices a gap, writes a quick markdown note with their idea or a real example from their team, and drops it in `incoming/`. No git. No PR. No approval process.

The skill admin runs `/skill-inbox` weekly. They review contributions, import good ones into `dev/`, reject ones that don't fit (with a reason), and batch-process the rest.

The result: skills improve continuously based on real usage, not just the admin's intuition.

## Why This Beats "Just Share a Google Doc"

| Approach | Problem |
|---|---|
| Shared Google Doc of prompts | Not persistent. PMs paste it once, it gets stale, nobody updates it. |
| Notion page of "AI tips" | Not structured. Tips without context don't shape AI behavior. |
| Slack channel of "good prompts" | Ephemeral. Search is terrible. No versioning. |
| Everyone writes their own | Knowledge trapped in individual Claude Projects. No sharing, no improvement. |
| Buy an AI training course | Generic. Doesn't include your org's terminology, constraints, or frameworks. |

PM Skills Platform is versioned, reviewable, distributable, and improvable. Skills get better with every release because there's a feedback mechanism built in.

## Who Should Be the Skill Admin?

The ideal skill admin is someone who:
- Is deep in PM practice (staff PM, product leader, PM coach)
- Is comfortable with Claude Code or at least willing to learn
- Has credibility across the PM org (their judgment is trusted)
- Can spend ~2-4 hours per week on curation

This doesn't have to be a dedicated role. It's usually a senior PM who cares about team leverage and sees AI as a multiplier, not a novelty.

## Org Fit

This works best in orgs where:
- PMs already have access to Claude Pro / ChatGPT Plus / Claude for Work
- There's a shared drive culture (OneDrive, SharePoint, Google Drive)
- The PM org is >10 people (below that, ad-hoc sharing is probably fine)
- There's at least one PM who cares enough to be the skill admin

It works less well if:
- PMs don't have access to AI tools (obviously)
- The org is extremely siloed and PMs don't share practices
- There's no one willing to maintain the library

## The Long-Term Vision

Over time, this becomes your org's institutional memory for how to do product work. New PMs onboard faster because the skills capture decades of accumulated wisdom. Experienced PMs stay sharp because the skills are continuously updated with new anti-patterns and frameworks. The AI doesn't replace PM judgment — it amplifies it by starting every conversation with the right context.

And because it's all just markdown, you're never locked into a platform. If Claude disappears tomorrow, you paste the skills into Gemini, Copilot, or whatever comes next.

## Want to Try It?

See [README.md](../README.md) for installation and [docs/ADMIN-GUIDE.md](ADMIN-GUIDE.md) for the full workflow.
