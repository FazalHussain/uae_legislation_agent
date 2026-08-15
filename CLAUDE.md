# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**NaxoraAgents** is a skills-based project containing two specialized Claude Code skills for design and business development workflows:

1. **ui-ux-pro-max** — UI/UX design intelligence for web, mobile, and desktop
2. **web-agency-agent** — Full-cycle web agency lead generation and outreach

This is not a traditional application codebase with build/test commands. It's a collection of skills that extend Claude Code's capabilities.

## Installed Skills

### ui-ux-pro-max
**Location:** `.claude/skills/ui-ux-pro-max/`

A comprehensive UI/UX design intelligence system with searchable local data:
- 79 searchable styles (50 active)
- 192 product palettes and reasoning profiles
- 74 font pairings
- 119 UX guidelines
- 105 curated icons
- 17 GSAP presets
- 25 chart types
- 22 technology stacks

**Invocation:** `/ui-ux-pro-max` or `Skill({skill: "ui-ux-pro-max"})`

**Key workflows:**
- `--design-system` — Generate coherent product-wide visual direction for new projects/pages
- `--domain <domain>` — Targeted searches (ux, style, color, typography, icons, gsap, chart, landing, product, google-fonts, react, web, etc.)
- `--stack <stack>` — Stack-specific implementation guidance (react, nextjs, vue, svelte, flutter, swiftui, html-tailwind, shadcn, etc.)
- `--persist` + `--output-dir` — Save design system as Master + page overrides

**Search script:** `python "${CLAUDE_PLUGIN_ROOT}/.claude/skills/ui-ux-pro-max/scripts/search.py" "<query>" [options]`

### web-agency-agent
**Location:** `.claude/skills/web-agency-agent/`

A five-phase pipeline for lead generation:
1. **Scrape** — Find businesses by location/niche via Google Maps
2. **Audit** — Diagnose digital problems (web presence, mobile UX, SEO, trust, conversion, social, reputation)
3. **Rank** — Score leads by conversion potential and revenue loss
4. **Brief** — Generate website design briefs + instant demo links (v0.dev prompts)
5. **Outreach** — Write personalized Instagram DM, WhatsApp, and email messages

**Invocation:** `/web-agency-agent` or `Skill({skill: "web-agency-agent"})`

**Reference files** (read at each phase):
- `references/scraping-guide.md`
- `references/audit-criteria.md`
- `references/lead-scoring.md`
- `references/website-brief-templates.md`
- `references/outreach-templates.md`

## Project Structure

```
.claude/
├── settings.local.json          # Project-specific permissions
├── skills/
│   ├── ui-ux-pro-max/           # UI/UX design intelligence skill
│   │   ├── SKILL.md             # Skill definition & usage guide
│   │   ├── data/                # 20+ CSV catalogs (styles, colors, fonts, icons, stacks)
│   │   ├── references/          # pro-rules.md, quick-reference.md
│   │   └── scripts/             # search.py, core.py, design_system.py, etc.
│   └── web-agency-agent/        # Lead generation skill
│       ├── SKILL.md
│       └── references/          # Phase-specific reference guides
└── references/                  # Shared reference docs (e.g., audit-criteria.md)
```

## Common Commands

### UI/UX Design Workflows
```bash
# Generate design system for new project
python "${CLAUDE_PLUGIN_ROOT}/.claude/skills/ui-ux-pro-max/scripts/search.py" "beauty spa wellness" --design-system -p "Serenity Spa"

# Persist design system to project
python "${CLAUDE_PLUGIN_ROOT}/.claude/skills/ui-ux-pro-max/scripts/search.py" "ai search tool modern minimal" --design-system --persist -p "AI Search" --output-dir "/Users/fazal/Documents/projects/NaxoraAgents"

# Search specific UX concern
python "${CLAUDE_PLUGIN_ROOT}/.claude/skills/ui-ux-pro-max/scripts/search.py" "keyboard focus modal" --domain ux

# Stack-specific guidance (detect stack first from project files)
python "${CLAUDE_PLUGIN_ROOT}/.claude/skills/ui-ux-pro-max/scripts/search.py" "suspense streaming bundle" --stack nextjs

# Design dials for tuning output
python "${CLAUDE_PLUGIN_ROOT}/.claude/skills/ui-ux-pro-max/scripts/search.py" "analytics dashboard" --design-system --variance 8 --motion 7 --density 8 -p "Ops Console"
```

### Web Agency Lead Generation
```bash
# Run full pipeline (interactive - will prompt for location/niche)
# Phase 1: Scrape businesses
# Phase 2: Audit top candidates
# Phase 3: Rank by conversion potential
# Phase 4: Generate briefs + demo links
# Phase 5: Write outreach messages
```

## Skill Usage Guidelines

### When to use ui-ux-pro-max
- Designing new pages, components, or design systems
- Choosing color/typography/spacing/layout systems
- Reviewing UI for accessibility, consistency, usability
- Implementing navigation, animation, responsive behavior
- Improving perceived quality and usability

**Skip for:** pure backend logic, API/database design, non-visual performance, infrastructure/DevOps

### When to use web-agency-agent
- Finding local businesses needing websites
- Auditing businesses for digital problems
- Scoring/ranking leads by revenue loss
- Generating website design briefs or demo links
- Writing outreach messages (Instagram, WhatsApp, email)

## Key Reference Files

| File | Purpose |
|------|---------|
| `.claude/skills/ui-ux-pro-max/references/quick-reference.md` | Full 119 UX guidelines with rationale |
| `.claude/skills/ui-ux-pro-max/references/pro-rules.md` | Pre-delivery checklist for app UI |
| `.claude/skills/web-agency-agent/references/audit-criteria.md` | Phase 2 audit dimensions |
| `.claude/skills/web-agency-agent/references/lead-scoring.md` | Phase 3 ranking formula |

## Development Notes

- **No build/lint/test commands** — this is a skills repository, not an application
- **Python 3.x required** for ui-ux-pro-max search script (no external deps)
- **Design systems persist** to `design-system/<project-slug>/` with Master + page overrides
- **Stack detection** should be done from project files (package.json, pubspec.yaml, etc.) — never assume
- **Search results are recommendations** — never override user or repository rules