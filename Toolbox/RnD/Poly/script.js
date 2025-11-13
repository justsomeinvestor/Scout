const fetchButton = document.getElementById('fetchButton');
const apiKeyInput = document.getElementById('apiKey');
const tickerInput = document.getElementById('ticker');
const resultsDiv = document.getElementById('results');

async function fetchTickers() {
    const apiKey = apiKeyInput.value.trim();
    const tickerRaw = tickerInput.value.trim();

    if (!apiKey) {
        resultsDiv.textContent = 'Please enter an API key.';
        return;
    }

    // UI: loading state
    resultsDiv.textContent = 'Fetching data...';
    fetchButton.disabled = true;

    try {
        let url;

        if (tickerRaw) {
            // For exact ticker lookup use the {ticker} endpoint (uppercase is typical)
            const ticker = encodeURIComponent(tickerRaw.toUpperCase());
            url = `https://api.polygon.io/v3/reference/tickers/${ticker}?apiKey=${apiKey}`;
        } else {
            // No ticker provided: fetch a small list as a quick smoke test
            // Limit to 10 to keep response small
            url = `https://api.polygon.io/v3/reference/tickers?apiKey=${apiKey}&limit=10`;
        }

        const response = await fetch(url);

        // Read response text first so we can show raw body on parse errors
        const text = await response.text();
        let data;
        try {
            data = JSON.parse(text);
        } catch (err) {
            data = { _raw: text };
        }

        if (!response.ok) {
            // Show status and body for troubleshooting (CORS issues show up differently — see catch)
            resultsDiv.textContent = `HTTP ${response.status} ${response.statusText}\n` + JSON.stringify(data, null, 2);
        } else {
            resultsDiv.textContent = JSON.stringify(data, null, 2);
        }
    } catch (err) {
        // Fetch will throw on network/CORS errors; give a helpful hint
        const msg = (err && err.message) ? err.message : String(err);
        resultsDiv.textContent = `Fetch error: ${msg}\n\nIf you see a CORS-related error in the browser console, the Polygon API may not allow direct browser requests for your key — try running a local proxy or server-side relay. See README for guidance.`;
    } finally {
        fetchButton.disabled = false;
    }
}

fetchButton.addEventListener('click', fetchTickers);