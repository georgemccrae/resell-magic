# Magic Search FastAPI Starter

A tiny FastAPI app that searches a JSON file of magic trick prices.

## Run locally

```bash
cd magic-search
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload
```

Then open:

```text
http://127.0.0.1:8000
```

Search example:

```text
http://127.0.0.1:8000/search?q=deck
```

## Files

- `app.py` — the FastAPI app
- `magic_prices.json` — sample magic trick data
- `requirements.txt` — Python packages needed
