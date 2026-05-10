import requests
import re

GOOGLE_API_KEY = "AIzaSyBQQczR_jrLgPzGXCo-v1cNXcBZgYklXZw"
SEARCH_ENGINE_ID = "f334d833f50904dfd"

def search_magic_trick(query):
    try:
        return google_search(query)
    except Exception as e:
        print(f"[ERROR] search_magic_trick failed: {e}")
        return {"error": str(e)}

def google_search(query):
    search_query = f"{query} magician price list second hand buy"
    url = "https://www.googleapis.com/customsearch/v1"

    params = {
        "key": GOOGLE_API_KEY,
        "cx": SEARCH_ENGINE_ID,
        "q": search_query,
        "num": 10,
    }

    print(f"[INFO] Searching Google for: {search_query}")

    response = requests.get(url, params=params, timeout=10)

    print(f"[INFO] Google API status code: {response.status_code}")

    data = response.json()

    # Log the full response if no items found
    if "items" not in data:
        print(f"[ERROR] No items in Google response. Full response: {data}")
        error_msg = data.get("error", {}).get("message", "Unknown error from Google API")
        return {"error": f"Google API returned no results: {error_msg}"}

    print(f"[INFO] Google returned {len(data['items'])} items")

    results = []
    for item in data["items"]:
        title = item.get("title", "")
        link = item.get("link", "#")
        snippet = item.get("snippet", "")
        shop = item.get("displayLink", "")

        print(f"[DEBUG] Item: {title} | Snippet: {snippet[:80]}")

        # Try to extract a price from the snippet or title
        price_match = re.search(r"[\$£€]\s?[\d,]+\.?\d*", snippet + " " + title)

        if not price_match:
            print(f"[DEBUG] No price found, skipping: {title}")
            continue

        price = price_match.group(0).replace(" ", "")
        print(f"[DEBUG] Price found: {price}")

        results.append({
            "name": title,
            "price": price,
            "shop": shop,
            "url": link
        })

    print(f"[INFO] Returning {len(results)} priced results")
    return results
