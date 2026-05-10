import requests
import re

SERP_API_KEY = "9166a4b08dca3e139d18b7cd237394051c0d911977012e7efe2871fe9cb1def2"

def search_magic_trick(query):
    try:
        return serp_search(query)
    except Exception as e:
        print(f"[ERROR] search_magic_trick failed: {e}")
        return {"error": str(e)}

def extract_prices(text):
    return re.findall(r"[\$£€]\s?[\d,]+\.?\d*", text)

def price_to_float(p):
    return float(re.sub(r"[^\d.]", "", p).replace(",", "") or 0)

def serp_search(query):
    search_query = f"{query} magician price second hand buy"

    params = {
        "engine": "google",
        "q": search_query,
        "api_key": SERP_API_KEY,
        "num": 10,
        "gl": "uk",
        "hl": "en",
    }

    print(f"[INFO] Searching SerpAPI for: {search_query}")

    response = requests.get("https://serpapi.com/search", params=params, timeout=15)
    print(f"[INFO] Status code: {response.status_code}")

    data = response.json()

    if "error" in data:
        print(f"[ERROR] SerpAPI error: {data['error']}")
        return {"error": f"SerpAPI error: {data['error']}"}

    # Try shopping results first
    shopping = data.get("shopping_results", [])
    if shopping:
        print(f"[INFO] Found {len(shopping)} shopping results")
        results = []
        seen = set()
        for item in shopping:
            link = item.get("link") or item.get("product_link", "#")
            if link in seen:
                continue
            seen.add(link)

            title = item.get("title", "")
            price = item.get("price", "")
            shop = item.get("source", "")
            description = item.get("snippet", "")

            if not price:
                continue

            results.append({
                "name": title,
                "price": price,
                "price_float": price_to_float(price),
                "shop": shop,
                "description": description[:120] if description else "",
                "url": link
            })

        results.sort(key=lambda x: x["price_float"])
        for r in results:
            del r["price_float"]

        if results:
            return results

    # Fall back to organic results if no shopping results
    organic = data.get("organic_results", [])
    print(f"[INFO] Falling back to {len(organic)} organic results")

    results = []
    seen = set()

    for item in organic:
        link = item.get("link", "#")
        if link in seen:
            continue
        seen.add(link)

        title = item.get("title", "")
        snippet = item.get("snippet", "")
        shop = item.get("displayed_link", "")

        prices = extract_prices(snippet + " " + title)
        if not prices:
            print(f"[DEBUG] No price found, skipping: {title}")
            continue

        prices_sorted = sorted(prices, key=price_to_float)
        best_price = prices_sorted[0].replace(" ", "")

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

    results.sort(key=lambda x: x["price_float"])
    for r in results:
        del r["price_float"]

    print(f"[INFO] Returning {len(results)} results")
    return results
