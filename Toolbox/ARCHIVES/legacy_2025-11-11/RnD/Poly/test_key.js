#!/usr/bin/env node
// Simple Polygon.io API key tester (server-side).
// Usage:
//   node test_key.js YOUR_KEY
// or
//   $env:POLYGON_API_KEY = 'YOUR_KEY'
//   node test_key.js

const key = process.argv[2] || process.env.POLYGON_API_KEY;
if (!key) {
  console.error('Usage: node test_key.js YOUR_KEY  (or set POLYGON_API_KEY env var)');
  process.exit(1);
}

(async () => {
  try {
    const ticker = 'AAPL';
    const url = `https://api.polygon.io/v3/reference/tickers/${encodeURIComponent(ticker)}?apiKey=${key}`;

    // Prefer global fetch (Node 18+). Fallback to node-fetch if not available.
    const fetchFn = (typeof fetch === 'function')
      ? fetch
      : (...args) => require('node-fetch')(...args);

    const res = await fetchFn(url);
    const text = await res.text();

    console.log('HTTP', res.status, res.statusText);
    try {
      console.log(JSON.stringify(JSON.parse(text), null, 2));
    } catch (e) {
      console.log(text);
    }
  } catch (err) {
    console.error('Error:', err && err.message ? err.message : String(err));
    process.exit(2);
  }
})();
