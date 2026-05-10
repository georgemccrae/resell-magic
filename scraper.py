import requests
import re

GOOGLE_API_KEY = "AIzaSyBQQczR_jrLgPzGXCo-v1cNXcBZgYklXZw"
SEARCH_ENGINE_ID = "f334d833f50904dfd"

def search_magic_trick(query):
    try:
        results = google_search(query)
        if results:
            return results
        return []
    except Exception as e:
        print(f"Search failed: {e}")
        return []

def google_search(query):
    search_query = f"{query} magician price list second hand buy"
    url = "https://www.googleapis.com/customsearch/v1"

    params = {
        "key": GOOGLE_API_KEY,
        "cx": SEARCH_ENGINE_ID,
        "q": search_query,
        "num": 10,
    }

    response = requests.get(url, params=params, timeout=10)
    data = response.json()

    if "items" not in data:
        print("No results from Google:", data)
        return []

    results = []
    for item in data["items"]:
        title = item.get("title", "")
        link = item.get("link", "#")
        snippet = item.get("snippet", "")
        shop = item.get("displayLink", "")

        # Try to extract a price from the snippet or title
        price_match = re.search(r"[\$£€][\d,]+\.?\d*", snippet + " " + title)

        # Skip results with no price found
        if not price_match:
            continue

        price = price_match.group(0)

        results.append({
            "name": title,
            "price": price,
            "shop": shop,
            "url": link
        })

    return results
