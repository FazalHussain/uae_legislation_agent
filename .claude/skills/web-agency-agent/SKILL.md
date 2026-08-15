---
name: web-agency-agent
description: >
  Full-cycle web agency lead generation and outreach agent. Use this skill whenever
  a user wants to find local businesses that need a website, audit businesses for
  digital problems, score or rank leads by conversion potential or revenue loss,
  generate a website design brief or demo link for a prospect, or write outreach
  messages (Instagram DM, WhatsApp, email) to pitch web services. Trigger even
  when the user phrases it casually — "find me businesses without a website near
  Dubai", "who should I pitch next?", "write me a cold email for this salon", or
  "run the full lead-gen flow for [city]". This skill covers the entire pipeline:
  scrape → audit → rank → brief → outreach.
---

# Web Agency Agent

A five-phase pipeline that turns a location and a niche into a ranked, ready-to-pitch prospect list — complete with estimated revenue-loss figures, a website design brief, a demo link, and personalised outreach copy for Instagram, WhatsApp, and email.

## How to use this skill

Read the phase the user needs and execute it. Each phase can run independently OR you can run all five in sequence by asking for a target **location** and **niche** (business category).

If the user says "run the full flow" — work through Phases 1 → 5 in order, presenting a summary after each phase before moving to the next.

Reference files (read them when you reach the relevant phase):
- `references/scraping-guide.md` — Phase 1: how to pull business data from maps
- `references/audit-criteria.md` — Phase 2: how to score individual businesses
- `references/lead-scoring.md` — Phase 3: ranking formula and revenue-loss model
- `references/website-brief-templates.md` — Phase 4: how to build the design brief and demo link
- `references/outreach-templates.md` — Phase 5: outreach message structures

---

## Phase 1 — Scrape: Find Businesses by Location

**Goal:** Produce a raw list of businesses in the target niche and location.

Read `references/scraping-guide.md` before writing any code.

### Inputs to collect from the user
- **Location** — city, neighbourhood, or lat/lng (e.g. "Dubai Marina", "Bur Dubai")
- **Niche** — business category (e.g. "restaurants", "salons", "gyms", "plumbers")
- **Radius** — default 3 km if not specified
- **Target count** — default 30 leads

### What to extract per business
At minimum collect:
- Business name
- Address / area
- Phone number (if visible)
- Category / type
- Google rating + review count
- Website URL (or flag as MISSING)
- Google Maps URL
- Instagram handle (search if not on Maps)
- Brief description (from Maps listing or website)

### Output format — Raw Lead Table
Present a markdown table:

| # | Name | Area | Category | Rating | Reviews | Website | Phone |
|---|------|------|----------|--------|---------|---------|-------|
| 1 | … | … | … | ⭐ 4.2 | 138 | ❌ None | … |

Flag businesses with `❌ None` for website — these are your hottest leads.

---

## Phase 2 — Audit: Identify Digital Problems

**Goal:** For each business, diagnose what's costing them customers online.

Read `references/audit-criteria.md` before auditing.

Run audits against the ~10 best-looking candidates from Phase 1 (or all if the list is short). For businesses WITH a website, fetch it and check real issues. For businesses WITHOUT, flag all website-absence penalties.

### Audit dimensions (score each 0–10, 10 = no problems)

| Dimension | What to check |
|-----------|--------------|
| **Web Presence** | Has website? Is it indexed on Google? |
| **Mobile UX** | Renders on mobile? No horizontal scroll? Fast load? |
| **SEO Basics** | Title tag, meta description, H1, Google Business claim |
| **Trust Signals** | SSL, phone/address visible, social proof, hours |
| **Conversion** | CTA button, WhatsApp link, booking link, menu/price list |
| **Social Presence** | Active Instagram/Facebook? Link in bio? |
| **Reputation** | Rating ≥ 4.0? Responded to reviews? |

### Audit output per business

```
🏪 [Business Name]
📍 [Area] | 📞 [Phone] | ⭐ [Rating] ([N] reviews)
🌐 Website: ❌ None / ⚠️ Outdated / ✅ Present

PROBLEMS FOUND:
• No website — invisible to anyone searching online
• Not claimed on Google Business Profile
• No WhatsApp click-to-chat link
• Instagram inactive (last post: 8 months ago)
• No SSL certificate on existing site

AUDIT SCORE: 3/10 — High opportunity
```

---

## Phase 3 — Rank: Score Leads by Conversion Potential

**Goal:** Rank the audited businesses by (a) likelihood to buy and (b) revenue loss they're suffering.

Read `references/lead-scoring.md` for the full formula and industry multipliers.

### Lead Score formula

```
Lead Score = (Problem Severity × 0.4)
           + (Revenue Loss Potential × 0.3)
           + (Buying Signal Strength × 0.2)
           + (Competition Gap × 0.1)
```

Score each component 1–10. Multiply. Present a ranked table:

| Rank | Business | Score | Est. Monthly Loss | Key Problem | Priority |
|------|----------|-------|-------------------|-------------|----------|
| 1 | … | 8.7 | AED 12,000–18,000 | No website | 🔥 HOT |
| 2 | … | 7.2 | AED 6,000–9,000 | No mobile UX | 🌡️ WARM |
| 3 | … | 5.1 | AED 2,000–4,000 | Weak SEO | ❄️ COLD |

**Revenue-loss estimate approach:** Use industry benchmarks (see `references/lead-scoring.md`) — estimate monthly foot traffic from review count and category, apply average ticket, assume 20–40% of that traffic could have found them online. This gives a defensible, personalised number to use in outreach.

---

## Phase 4 — Brief: Website Design Prompt + Demo Link

**Goal:** Produce a complete, ready-to-use brief for building this business's website — plus a shareable demo link they can see immediately.

Read `references/website-brief-templates.md` for category-specific templates.

### What to produce per lead

**A. One-page Website Design Brief**

```markdown
# Website Brief — [Business Name]

## Business Overview
[Name], [Category], [Location]. [2-sentence description].

## Target Audience
[Who comes to this business and why]

## Website Goal
Primary: [Book appointment / Order online / Get directions / Call now]
Secondary: [Show menu / Build trust / Show before/afters]

## Pages Required
1. Home — hero with CTA, 3 USPs, photo gallery, WhatsApp button
2. About — story, team photo, years in business
3. Services/Menu — with prices if appropriate
4. Gallery — [# images needed]
5. Contact — map embed, phone, WhatsApp, hours

## Design Direction
Tone: [Luxury / Friendly / Professional / Vibrant]
Colours: [Primary] / [Accent] — inspired by their logo/branding
Font style: [Modern sans / Classic serif / Playful]
Reference sites: [2–3 real URLs that have a similar vibe]

## Must-Have Features
- WhatsApp click-to-chat (number: [if found])
- Google Maps embed
- Mobile-first layout
- Fast load — no heavy video backgrounds
- [Industry-specific: e.g. online booking for salon, menu PDF for restaurant]

## Content Needed from Client
- Logo file (PNG/SVG)
- 10–20 photos of premises and work
- Team bio (optional)
- Pricing list (optional)

## Suggested Tech Stack
[Webflow / Framer / WordPress + Elementor / Shopify] — choose based on complexity
Estimated build time: [X days]
Estimated one-time cost range: AED [X]–[Y]
Monthly maintenance: AED [Z] (optional)
```

**B. Demo Link**

Generate a Framer or Typedream instant-demo URL using the business name and category, or construct a v0.dev prompt the user can paste to get a live preview in 60 seconds. Present the prompt clearly formatted so the user can copy it.

```
🔗 INSTANT DEMO — Paste this into https://v0.dev:

"Create a mobile-first landing page for [Business Name], a [category] in [city].
Include: hero section with '[Primary CTA]' button, services grid (3 items),
photo gallery, WhatsApp floating button, Google Maps embed, and footer with
phone and hours. Color scheme: [Primary] and [Accent]. Clean, modern design."
```

---

## Phase 5 — Outreach: Personalised Pitch Messages

**Goal:** Write ready-to-send outreach messages for each hot lead, personalised with their name, specific problems found, and revenue-loss estimate.

Read `references/outreach-templates.md` for tone guidelines and proven structures.

Produce three message variants per lead:

### Instagram DM (≤ 300 characters — fits preview pane)
- Hook: compliment or observation about their page
- Problem: one specific pain they have (no link in bio, no website, etc.)
- Curiosity: tease a result, not a pitch
- CTA: soft — "want me to send you an example?"

### WhatsApp Message (≤ 200 words)
- Personal opener (reference their business by name)
- 2–3 specific problems + what it's costing them
- Social proof (one line)
- Demo offer: "I built a quick demo of what your site could look like"
- CTA: "Can I share it with you? Takes 30 seconds to view"

### Email (subject line + body, ≤ 300 words)
- Subject: curiosity-led, not salesy (e.g. "I made something for [Business Name]")
- Opening: personalised observation — show you've done your homework
- Body: problem → cost → solution → proof
- CTA: single, clear next step (reply, book a call, view demo)
- P.S.: re-state the demo offer

---

## Output Delivery

After running the full pipeline, deliver:

1. **Raw Leads Table** (Phase 1) — markdown table
2. **Top 5 Audit Reports** (Phase 2) — one block per business  
3. **Ranked Lead Scorecard** (Phase 3) — table with scores and loss estimates
4. **Website Briefs + Demo Prompts** (Phase 4) — one section per top 3 leads
5. **Outreach Pack** (Phase 5) — 3 messages × top 3 leads = 9 messages total

If the output is large, offer to save it as a Markdown file the user can download.

---

## Important principles

**Be specific, not generic.** Every output should mention the actual business name, real problems found, real numbers. Generic outreach gets ignored.

**Revenue-loss numbers are estimates** — frame them as "based on similar businesses in your area" and show your working. Don't invent precision you don't have.

**Respect privacy.** Only use publicly available data (Google Maps, public websites, public social profiles). Never scrape or use private data.

**When scraping fails** — if automated scraping is blocked, guide the user through a manual search workflow using Google Maps + a structured copy-paste approach.