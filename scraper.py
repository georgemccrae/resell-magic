import requests
import re

GOOGLE_API_KEY = "AIzaSyBQQczR_jrLgPzGXCo-v1cNXcBZgYklXZw"
SEARCH_ENGINE_ID = "f334d833f50904dfd"

MAGIC_SITES = [
    "ebay.co.uk", "ebay.com", "amazon.co.uk", "amazon.com",
    "vanishingincmagic.com", "alakazam.co.uk", "penguinmagic.com",
    "murphysmagic.com", "themagicshop.co.uk", "internationalmagiclondon.com",
    "magicshop.co.uk", "ellusionist.com", "theory11.com", "misdirection.co.uk",
    "lybrary.com", "hocus-pocus.com", "propdog.co.uk", "magicmakers.com",
    "trickshop.com", "magicstreet.co.uk",
]

SITE_FILTER = " OR ".join([f"site:{s}" for s in MAGIC_SITES])

def search_magic_trick(query):
    try:
        return google_search(query)
    except Exception as e:
        print(f"[ERROR] search_magic_trick failed: {e}")
        return {"error": str(e)}

def extract_prices(text):
    """Extract all prices found in text."""
    return re.findall(r"[\$£€]\s?[\d,]+\.?\d*", text)

def google_search(query):
    search_query = f"{query} magician price second hand ({SITE_FILTER})"
    url = "https://www.googleapis.com/customsearch/v1"

    params = {
        "key": GOOGLE_API_KEY,
        "cx": SEARCH_ENGINE_ID,
        "q": search_query,
        "num": 10,
    }

    print(f"[INFO] Searching: {search_query}")
    response = requests.get(url, params=params, timeout=10)
    print(f"[INFO] Status code: {response.status_code}")

    data = response.json()

    if "items" not in data:
        print(f"[ERROR] Full Google response: {data}")
        error_msg = data.get("error", {}).get("message", "Unknown error")
        return {"error": f"Google API error: {error_msg}"}

    print(f"[INFO] Got {len(data['items'])} items from Google")

    results = []
    seen_urls = set()

    for item in data["items"]:
        title = item.get("title", "")
        link = item.get("link", "#")
        snippet = item.get("snippet", "")
        shop = item.get("displayLink", "")

        print(f"[DEBUG] {title} | {snippet[:80]}")

        # Skip duplicates
        if link in seen_urls:
            print(f"[DEBUG] Duplicate, skipping")
            continue
        seen_urls.add(link)

        # Extract all prices, pick the lowest
        prices = extract_prices(snippet + " " + title)
        if not prices:
            print(f"[DEBUG] No price found, skipping")
            continue

        # Clean and convert prices for sorting
        def price_to_float(p):
            return float(re.sub(r"[^\d.]", "", p).replace(",", "") or 0)

        prices_sorted = sorted(prices, key=price_to_float)
        best_price = prices_sorted[0].replace(" ", "")

        # Clean up snippet for description
        description = snippet.replace("\n", " ").strip()
        if len(description) > 120:
            description = description[:120] + "…"

        results.append({
            "name": title,
            "price": best_price,
            "price_float": price_to_float(best_price),
            "shop": shop,
            "description": description,
            "url": link
        })

    # Sort all results by price low to high
    results.sort(key=lambda x: x["price_float"])

    # Remove internal float field before returning
    for r in results:
        del r["price_float"]

    print(f"[INFO] Returning {len(results)} priced results")
    return results
