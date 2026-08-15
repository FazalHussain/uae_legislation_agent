# Phase 3 — Lead Scoring & Revenue Loss Model

## Lead Score Formula

```
Lead Score (0–10) =
    (Problem Severity × 0.40)
  + (Revenue Loss Potential × 0.30)
  + (Buying Signal Strength × 0.20)
  + (Competition Gap × 0.10)
```

---

## Component 1 — Problem Severity (from Phase 2 audit)

Convert audit composite score to problem severity:
```
Problem Severity = 10 - Audit Composite Score
```
A business with audit score 1.5 has problem severity 8.5 — very high opportunity.

---

## Component 2 — Revenue Loss Potential

Estimate how much business this prospect is losing monthly by NOT being online.

### Step 1: Estimate Monthly Foot Traffic

Use Google review count as a proxy:
```
Review Count → Traffic Estimate
< 20 reviews    → ~50 customers/month
20–50 reviews   → ~120 customers/month
50–150 reviews  → ~300 customers/month
150–500 reviews → ~800 customers/month
500+ reviews    → ~2,000 customers/month
```
Rationale: roughly 1–3% of customers leave reviews. Use 2% as mid-estimate.

### Step 2: Apply Industry Average Ticket (AED — UAE market)

| Category | Avg Ticket (AED) | Online Discovery % |
|----------|------------------|--------------------|
| Restaurant / Café | 80 | 35% |
| Salon / Barbershop | 120 | 40% |
| Spa / Wellness | 250 | 45% |
| Gym / Fitness Studio | 350 | 30% |
| Dental Clinic | 500 | 50% |
| Driving School | 2,000 | 60% |
| Real Estate Agency | 8,000 | 55% |
| Cleaning Service | 200 | 65% |
| Catering / Event | 3,000 | 55% |
| Retail Shop | 150 | 25% |
| Auto Repair / Car Wash | 200 | 30% |
| Photography Studio | 800 | 50% |
| Nursery / School | 1,500 | 45% |
| Legal / Accounting | 1,000 | 40% |
| General (unknown) | 200 | 35% |

### Step 3: Calculate Monthly Loss

```python
def monthly_revenue_loss(
    review_count: int,
    category: str,
    has_website: bool,
    mobile_score: int  # 0-100
) -> tuple[int, int]:
    
    # Traffic estimate
    if review_count < 20:
        traffic = 50
    elif review_count < 50:
        traffic = 120
    elif review_count < 150:
        traffic = 300
    elif review_count < 500:
        traffic = 800
    else:
        traffic = 2000
    
    # Category data
    categories = {
        "restaurant": (80, 0.35),
        "cafe": (60, 0.35),
        "salon": (120, 0.40),
        "spa": (250, 0.45),
        "gym": (350, 0.30),
        "dental": (500, 0.50),
        "default": (200, 0.35),
    }
    avg_ticket, online_pct = categories.get(category.lower(), categories["default"])
    
    # Potential online customers being missed
    online_customers_missed = traffic * online_pct
    
    # If no website: lose 100% of those who search online
    # If website but poor: lose 40% (bad UX / not ranking)
    if not has_website:
        loss_factor = 1.0
    elif mobile_score < 40:
        loss_factor = 0.60
    elif mobile_score < 70:
        loss_factor = 0.35
    else:
        loss_factor = 0.15
    
    lost_customers = online_customers_missed * loss_factor
    monthly_loss = lost_customers * avg_ticket
    
    # Return low/high range (±30%)
    return int(monthly_loss * 0.7), int(monthly_loss * 1.3)
```

### Revenue Loss Score (for the formula)

| Monthly Loss (AED) | Score |
|--------------------|-------|
| < 1,000 | 2 |
| 1,000–3,000 | 4 |
| 3,000–6,000 | 5 |
| 6,000–10,000 | 7 |
| 10,000–20,000 | 9 |
| > 20,000 | 10 |

---

## Component 3 — Buying Signal Strength

Look for indicators the business owner is ready to invest:

| Signal | Points |
|--------|--------|
| Business is < 2 years old (new, growing) | +2 |
| Recently responded to reviews | +1 |
| Active on Instagram in last 30 days | +1 |
| Posted about expansion / new services | +2 |
| Running Facebook/Google Ads (check via Facebook Ad Library) | +2 |
| High-rating business in a competitive area | +1 |
| Owner name visible on Google profile | +1 |

Max score: 10 (cap at 10 if signals add up to more)

If NO signals found: score = 3 (neutral)

---

## Component 4 — Competition Gap

Compare this business to its top 3 competitors on Google Maps:

| Condition | Score |
|-----------|-------|
| All competitors have strong websites; this one has nothing | 10 |
| 2 of 3 competitors have websites; this one doesn't | 8 |
| Mixed — some competitors have websites too | 5 |
| Competitors also have poor/no websites | 3 |
| Competitors have excellent SEO and this can't compete easily | 2 |

---

## Final Lead Score Interpretation

| Score | Label | Action |
|-------|-------|--------|
| 8.5–10 | 🔥 HOT | Reach out today, personalise deeply |
| 7–8.4 | 🌡️ WARM | High priority, strong pitch |
| 5–6.9 | 🟡 MEDIUM | Batch pitch, less personalised |
| 3–4.9 | ❄️ COLD | Add to nurture list |
| < 3 | ⏭️ SKIP | Not worth your time right now |

---

## Presenting revenue loss to prospects

Use this framing in outreach — it's research-based and non-threatening:

> "Based on businesses similar to yours in [area], with [X] reviews and no website, 
> you're likely missing around AED [low]–[high] every month from people who search 
> online and can't find you. That's AED [annual] a year — and a website pays itself 
> back in the first month."

Always say "likely" or "estimated" — never present this as a guaranteed figure.