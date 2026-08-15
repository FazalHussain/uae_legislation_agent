# Phase 2 — Audit Criteria

## Audit scoring system

Each dimension scores 0–10 (10 = perfect, no problem). Lower scores = bigger opportunity.

---

## Dimension 1 — Web Presence (weight: 30%)

| Score | Condition |
|-------|-----------|
| 0 | No website whatsoever |
| 2 | Domain exists but returns 404/500 |
| 4 | Website exists but not indexed on Google (`site:domain.com` returns nothing) |
| 6 | Website exists, indexed, but barely (< 5 pages indexed) |
| 8 | Website exists, well indexed, but not ranking for brand name |
| 10 | Website ranks #1 for brand name, appears in Knowledge Panel |

**Check:** Google `site:[domain]` and `"[Business Name]" [City]`

---

## Dimension 2 — Mobile UX (weight: 20%)

| Score | Condition |
|-------|-----------|
| 0 | Site not usable on mobile (broken layout, tiny text) |
| 3 | Renders but requires horizontal scrolling |
| 5 | Usable but slow (> 5s load time on mobile) |
| 7 | Decent mobile layout but no tap-to-call, no WhatsApp |
| 9 | Mobile-friendly, fast, tap-to-call works |
| 10 | Mobile-first design, < 2s load, all CTAs thumb-accessible |

**Check:** Google PageSpeed Insights mobile score, manual test on Chrome DevTools mobile view

```python
def check_mobile_speed(url: str) -> dict:
    # Use Google PageSpeed Insights API (free, no key needed for basic)
    api = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&strategy=mobile"
    r = requests.get(api, timeout=15)
    data = r.json()
    score = data.get("lighthouseResult", {}).get("categories", {}).get("performance", {}).get("score", 0)
    return {"mobile_score": int(score * 100)}
```

---

## Dimension 3 — SEO Basics (weight: 15%)

Check these elements by fetching the page HTML:

```python
from bs4 import BeautifulSoup
import requests

def audit_seo(url: str) -> dict:
    r = requests.get(url, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(r.text, "html.parser")
    
    return {
        "has_title": bool(soup.find("title") and soup.find("title").text.strip()),
        "title_text": soup.find("title").text.strip() if soup.find("title") else None,
        "has_meta_desc": bool(soup.find("meta", {"name": "description"})),
        "has_h1": bool(soup.find("h1")),
        "has_og_tags": bool(soup.find("meta", {"property": "og:title"})),
        "has_schema": '"@context"' in r.text or 'application/ld+json' in r.text,
    }
```

| Score | Condition |
|-------|-----------|
| 0 | No title tag, no H1, no meta description |
| 4 | Has title but it's generic ("Home" or business name only) |
| 6 | Has title + meta desc but no local keywords |
| 8 | Good title, meta, H1 with city/niche keywords |
| 10 | Full SEO: schema markup, OG tags, sitemap, fast TTFB |

---

## Dimension 4 — Trust Signals (weight: 15%)

Check for presence of:
- SSL (HTTPS) — if missing: -3 points
- Phone number visible above fold — if missing: -2 points
- Address visible on page — if missing: -1 point
- Business hours listed — if missing: -1 point
- Customer reviews/testimonials on site — if missing: -1 point
- Team/About page — if missing: -1 point

Start from 10, subtract per missing element.

---

## Dimension 5 — Conversion Features (weight: 10%)

Score by counting present conversion elements:

| Element | Points |
|---------|--------|
| Click-to-call button | +2 |
| WhatsApp click-to-chat link | +2 |
| Online booking / reservation link | +2 |
| Menu / services with prices | +1 |
| Contact form | +1 |
| Google Maps embed | +1 |
| Clear primary CTA ("Book Now", "Order") | +1 |

Score = min(sum, 10)

---

## Dimension 6 — Social Presence (weight: 5%)

| Score | Condition |
|-------|-----------|
| 0 | No Instagram, no Facebook |
| 2 | Exists but last post > 6 months ago |
| 4 | Posts monthly, < 500 followers |
| 6 | Posts weekly, link in bio, active Stories |
| 8 | Posts daily, 1k+ followers, running ads |
| 10 | Strong presence, UGC, reels, 5k+ followers |

---

## Dimension 7 — Reputation (weight: 5%)

| Score | Condition |
|-------|-----------|
| 0 | < 3.0 stars or < 5 reviews |
| 3 | 3.0–3.5 stars, unanswered negative reviews |
| 5 | 3.5–4.0 stars |
| 7 | 4.0–4.5 stars, responds to some reviews |
| 9 | 4.5–5.0 stars, active responder |
| 10 | 4.8+ stars, 100+ reviews, perfect responses |

---

## Composite audit score

```python
def composite_score(dimensions: dict) -> float:
    weights = {
        "web_presence": 0.30,
        "mobile_ux": 0.20,
        "seo_basics": 0.15,
        "trust_signals": 0.15,
        "conversion": 0.10,
        "social_presence": 0.05,
        "reputation": 0.05,
    }
    return sum(dimensions[k] * w for k, w in weights.items())
```

**Score interpretation:**
- 0–3: 🔥 Critical — massive opportunity, easy sell
- 3–5: ⚠️ Serious — good lead
- 5–7: 🟡 Moderate — worth pitching with strong angle
- 7–9: 🟢 Minor — harder to sell, lower priority
- 9–10: ✅ Strong — skip unless they're looking to upgrade

---

## No-website fast track

If a business has NO website at all, auto-score it as follows (do not spend time auditing a non-existent site):

- Web Presence: 0
- Mobile UX: 0
- SEO Basics: 0
- Trust Signals: 2 (assume Google Business only)
- Conversion: 0
- Social Presence: depends on Instagram check
- Reputation: check Google rating

**Composite will almost always land in 0–2 range — treat as maximum-opportunity lead.**