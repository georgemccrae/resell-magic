import requests
from bs4 import BeautifulSoup
import re

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

MOCK_DATA = {
    "default": [
        {"name": "Result 1", "price": "£9.99", "shop": "Magic Shop UK", "url": "#"},
        {"name": "Result 2", "price": "£14.99", "shop": "Vanishing Inc", "url": "#"},
        {"name": "Result 3", "price": "£24.99", "shop": "Alakazam Magic", "url": "#"},
    ]
}

def search_magic_trick(query):
    try:
        results = scrape_google_shopping(query)
        if results:
            return results
        # If scraping returns nothing, fall back to mock
        return get_mock_data(query)
    except Exception as e:
        print(f"Scraping failed: {e}")
        return get_mock_data(query)

def scrape_google_shopping(query):
    search_query = f"{query} magic trick price buy"
    url = f"https://www.google.com/search?q={requests.utils.quote(search_query)}&tbm=shop"

    response = requests.get(url, headers=HEADERS, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")

    results = []

    # Try to find shopping results
    for item in soup.select(".sh-dgr__grid-result")[:6]:
        try:
            name = item.select_one(".Xjkr3b, .tAxDx")
            price = item.select_one(".a8Pemb, .kHxwFf")
            shop = item.select_one(".aULzUe, .E5ocAb")
            link = item.select_one("a")

            if name and price:
                results.append({
                    "name": name.get_text(strip=True),
                    "price": price.get_text(strip=True),
                    "shop": shop.get_text(strip=True) if shop else "Google Shopping",
                    "url": "https://www.google.com" + link["href"] if link else "#"
                })
        except Exception:
            continue

    # If shopping selectors didn't work, try regular search results
    if not results:
        for item in soup.select(".tF2Cxc")[:6]:
            try:
                name = item.select_one("h3")
                snippet = item.select_one(".VwiC3b")
                link = item.select_one("a")

                # Look for a price in the snippet
                price_match = re.search(r"£[\d,.]+", snippet.get_text() if snippet else "")
                price = price_match.group(0) if price_match else "See site"

                if name:
                    results.append({
                        "name": name.get_text(strip=True),
                        "price": price,
                        "shop": link["href"].split("/")[2] if link else "Google",
                        "url": link["href"] if link else "#"
                    })
            except Exception:
                continue

    return results

def get_mock_data(query):
    # Return mock results labelled clearly as demo data
    return [
        {"name": f"{query} - Standard Edition", "price": "£9.99", "shop": "⚠️ Demo Data - Magic Shop UK", "url": "#"},
        {"name": f"{query} - Pro Version", "price": "£19.99", "shop": "⚠️ Demo Data - Vanishing Inc", "url": "#"},
        {"name": f"{query} - Deluxe Set", "price": "£34.99", "shop": "⚠️ Demo Data - Alakazam Magic", "url": "#"},
    ]
