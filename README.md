# Magic Price Finder

Search for any magic trick and get prices from across the web.

## Your files
```
magic_finder/
  app.py            ← Flask web server
  scraper.py        ← Google scraping logic (edit this)
  requirements.txt  ← Python packages needed
  Procfile          ← Tells Render how to start the app
  templates/
    index.html      ← The search page
```

---

## Step 1 — Deploy on Render

1. Go to **render.com** and create a free account
2. Click **New** → **Web Service**
3. Connect your GitHub account
4. Select your `magic-finder` repository
5. Fill in:
   - **Name**: magic-finder
   - **Runtime**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
6. Click **Create Web Service**
7. Wait 2-3 minutes — Render builds and deploys it
8. You get a URL like `magic-finder.onrender.com` — that's your live app!

---

## Step 2 — Stop it sleeping (free fix)

1. Go to **cron-job.org** and create a free account
2. Create a new cronjob
3. Set the URL to your Render URL e.g. `https://magic-finder.onrender.com`
4. Set it to run every **10 minutes**
5. Save — your app will never sleep again

---

## Updating your scraper later

Just edit `scraper.py`, re-upload to GitHub, Render updates automatically.
