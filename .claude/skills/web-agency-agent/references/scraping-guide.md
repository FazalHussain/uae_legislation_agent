# Phase 1 — Scraping Guide

## Approach selection

Use the best available method in this order of preference:

### Option A — SerpAPI / Google Places API (Recommended if API key provided)
If the user has a SerpAPI or Google Places API key, use it:

```python
import requests, json

# SerpAPI — Google Maps results
params = {
    "engine": "google_maps",
    "q": f"{niche} in {location}",
    "api_key": SERPAPI_KEY,
    "type": "search",
    "ll": "@{lat},{lng},14z"  # optional coordinate zoom
}
response = requests.get("https://serpapi.com/search", params=params)
results = response.json().get("local_results", [])
```

Fields to extract: `title`, `address`, `phone`, `website`, `rating`, `reviews`, `type`, `place_id`

### Option B — Web Scraping via Playwright (no API key)
Install and run headless browser to scrape Google Maps:

```python
# Install: pip install playwright && playwright install chromium
from playwright.async_api import async_playwright
import asyncio

async def scrape_maps(query: str, location: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        url = f"https://www.google.com/maps/search/{query}+{location}"
        await page.goto(url)
        await page.wait_for_selector('[role="feed"]', timeout=10000)
        
        # Scroll to load more results
        feed = page.locator('[role="feed"]')
        for _ in range(5):
            await feed.evaluate("el => el.scrollBy(0, 1000)")
            await page.wait_for_timeout(1500)
        
        # Extract listing cards
        cards = await page.query_selector_all('[role="article"]')
        results = []
        for card in cards:
            name = await card.query_selector('span.fontHeadlineSmall')
            rating = await card.query_selector('span[aria-label*="stars"]')
            results.append({
                "name": await name.inner_text() if name else "Unknown",
                "rating": await rating.get_attribute("aria-label") if rating else "No rating",
            })
        
        await browser.close()
        return results
```

### Option C — Manual-Guided Workflow (fallback)
If scraping is blocked or unavailable, guide the user:

1. Open Google Maps → search `[niche] in [location]`
2. Open browser DevTools → Network tab → filter `maps.googleapis.com`
3. Copy the JSON response from the places API call
4. Paste it here and Claude will parse it automatically

OR use this structured copy approach:
- For each result visible on screen, press Tab to cycle through listings
- Copy: Name, address, rating, website (right-click → "Go to website")
- Paste into a table here

### Option D — Outscraper / Apify (if user has account)
```python
# Outscraper
import outscraper
client = outscraper.ApiClient(api_key=OUTSCRAPER_KEY)
results = client.google_maps_search(
    [f"{niche} in {location}"],
    limit=30,
    language="en"
)
```

---

## Extracting website presence

For each business found, determine website status:

```python
import requests
from urllib.parse import urlparse

def check_website(url: str | None) -> dict:
    if not url:
        return {"status": "MISSING", "reachable": False}
    try:
        r = requests.get(url, timeout=5, allow_redirects=True)
        return {
            "status": "PRESENT",
            "reachable": r.status_code < 400,
            "final_url": r.url,
            "has_ssl": r.url.startswith("https://"),
            "status_code": r.status_code
        }
    except Exception as e:
        return {"status": "BROKEN", "reachable": False, "error": str(e)}
```

---

## Finding Instagram handles

If Instagram handle not on Maps listing, search:
1. `site:instagram.com "[Business Name]" [City]` via Google
2. Search directly on instagram.com/explore
3. Check website footer/header for social links

```python
def find_instagram(business_name: str, city: str) -> str | None:
    query = f'site:instagram.com "{business_name}" {city}'
    # Use web_search tool with this query
    # Parse first result URL to extract handle
    pass
```

---

## Data quality checklist

Before passing data to Phase 2:
- [ ] All business names are real (not duplicates or ads)
- [ ] Phone numbers are formatted consistently
- [ ] Website URLs are actual business sites (not booking platforms as primary)
- [ ] At least 30% of listings have no website — if not, broaden search or try adjacent niche
- [ ] Flag businesses with < 10 reviews (very new or very inactive)