import json
from pathlib import Path

from fastapi import FastAPI

app = FastAPI()

DATA_FILE = Path(__file__).parent / "magic_prices.json"


def load_prices():
    """Load magic trick price data from the JSON file."""
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


@app.get("/")
def home():
    return {
        "message": "Magic search API is running",
        "try_this": "/search?q=deck"
    }


@app.get("/search")
def search(q: str):
    """
    Search magic tricks by name.

    Example:
    /search?q=deck
    """
    data = load_prices()

    results = [
        item for item in data
        if q.lower() in item["name"].lower()
    ]

    return {
        "query": q,
        "count": len(results),
        "results": results
    }
