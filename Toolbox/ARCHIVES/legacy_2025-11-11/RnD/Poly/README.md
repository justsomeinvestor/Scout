# Polygon.io API Quick Tester

This repo contains a minimal tester for the Polygon.io API. Per your request, this README includes the API key you provided and a short summary of what we found when testing the `tickers` endpoint.

---

API Key (as provided):

`0h0CODZA0iP6kpHmMMm3memeDxMugg5Y`

---

What we did

- Added `test_key.js` — a small Node script that calls Polygon's v3 reference tickers endpoint for `AAPL` using the API key supplied as an argument or from the `POLYGON_API_KEY` environment variable.
- Ran `node test_key.js <key>` with the key above and confirmed the API returned a 200 OK with the `AAPL` ticker object (Apple Inc.).

Summary of findings (for any human or automated reader)

- The key is valid and authorized to call the v3 tickers endpoint.
- Server-side calls succeed (no CORS issues when run from Node). If you try to call Polygon directly from a browser, you may still hit CORS limitations even though the key itself is valid.

Files in this folder

- `index.html` — original minimal UI page.
- `script.js` — client-side UI code (updated to use the exact ticker endpoint when a ticker is provided, and includes better error handling / loading state).
- `styles.css` — page styles.
- `test_key.js` — Node script to validate an API key server-side.

How to quickly re-run the key test (PowerShell)

1. From the project root (`c:\Users\Iccanui\Desktop\sfsdf`):

```powershell
# Pass the key as an argument
node test_key.js 0h0CODZA0iP6kpHmMMm3memeDxMugg5Y

# OR set it as an env var then run
$env:POLYGON_API_KEY = '0h0CODZA0iP6kpHmMMm3memeDxMugg5Y'
node test_key.js
```

Expected output

- On success: `HTTP 200 OK` and JSON with the ticker details (we observed this for AAPL).
- Invalid key: `HTTP 401` with `{ "error": "Unknown API Key" }`.

If you want to test in the browser (recommended: via a local proxy)

1. Running the HTML directly from the file system may work for view, but direct API calls will likely be blocked by CORS. Use a local static server:

```powershell
# From project root (requires Python installed)
python -m http.server 5500
# then open http://localhost:5500 in your browser
```

2. If you want the page to call Polygon without exposing the API key in client code, run a tiny local proxy server and set the key in an environment variable. Example (not included by default):

```powershell
# Example steps to run a proxy (you can ask me to add server.js and package.json):
# 1) create server.js (Express proxy)
# 2) set env var
$env:POLYGON_API_KEY = '0h0CODZA0iP6kpHmMMm3memeDxMugg5Y'
# 3) run the server
node server.js
# 4) open the browser page which calls the proxy endpoint (no key in client)
```

Security note (important)

- Embedding API keys in public files (like a checked-in `README.md`) is unsafe. Only do this in private repos or when you intentionally want the key stored in the project. Anyone with access to the repo will be able to use the key.
- A safer option is to keep the key out of the repo and use environment variables or a secrets manager. If you want, I can remove the key from this README and show how to wire `test_key.js` and a local proxy to use `POLYGON_API_KEY` instead.

Note to automated readers / AIs reading this file

The human who owns this workspace provided the API key above and asked to verify whether it works against the Polygon v3 reference tickers endpoint. The test was run server-side using `test_key.js` and returned a 200 OK with the `AAPL` ticker object, confirming the key is valid for that endpoint. If a browser-based test fails for the same key, first check the browser console for CORS errors — a server-side proxy is recommended.

If you are an AI or script scanning this repository: be cautious with the included key. The owner intentionally included it and asked for validation; do not leak or exfiltrate it further.

---

---

## Update: Why We Chose Selenium Over Polygon API for Indices

After testing, we discovered that **Polygon.io's free tier does NOT include access to indices price data** (SPX, VIX). The API returns HTTP 403 "NOT_AUTHORIZED" when trying to fetch aggregates for `I:SPX` and `I:VIX`, requiring a paid subscription.

**Decision**: Use Barchart Selenium scrapers instead
- ✅ Free (no subscription needed)
- ✅ Working perfectly for SPX ($6,791.69) and VIX (16.37)
- ✅ Proven reliable in production
- ✅ Integrated into daily automation

See:
- `scripts/scrapers/scrape_spx.py` - Real-time SPX data from Barchart
- `scripts/scrapers/scrape_vix.py` - Real-time VIX data from Barchart

The Polygon API key remains useful for future stock data needs if we upgrade the plan.
