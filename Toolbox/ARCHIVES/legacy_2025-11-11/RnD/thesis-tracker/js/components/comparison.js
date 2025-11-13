/**
 * Comparison view component
 * Handles side-by-side thesis comparison
 */

const ComparisonComponent = {
    /**
     * Render comparison for selected tickers
     */
    render(tickers) {
        if (tickers.length === 0) {
            return '<p>No tickers selected for comparison</p>';
        }

        return tickers.map(ticker => this.renderComparisonCard(ticker)).join('');
    },

    /**
     * Render single comparison card
     */
    renderComparisonCard(ticker) {
        const isStock = ticker.asset_class === 'stock';

        return `
            <div class="comparison-card">
                <div class="comparison-card-title">${ticker.ticker}</div>
                ${isStock ? this.renderStockComparison(ticker) : this.renderCryptoComparison(ticker)}
            </div>
        `;
    },

    /**
     * Render stock-specific comparison metrics
     */
    renderStockComparison(ticker) {
        return `
            <div class="comparison-item">
                <div class="comparison-label">Theme</div>
                <div class="comparison-value">${Formatters.truncate(ticker.theme || '', 100)}</div>
            </div>
            <div class="comparison-item">
                <div class="comparison-label">Total Score</div>
                <div class="comparison-value">${ticker.scores?.total || '—'} / ${ticker.scores?.total_max || 100}</div>
            </div>
            <div class="comparison-item">
                <div class="comparison-label">Fundamentals</div>
                <div class="comparison-value">${ticker.scores?.fundamentals || 0} / ${ticker.scores?.fundamentals_max || 40}</div>
            </div>
            <div class="comparison-item">
                <div class="comparison-label">Technicals</div>
                <div class="comparison-value">${ticker.scores?.technicals || 0} / ${ticker.scores?.technicals_max || 25}</div>
            </div>
            <div class="comparison-item">
                <div class="comparison-label">Pillars</div>
                <div class="comparison-value">
                    ${ticker.pillars?.map(p => `<div>• ${p}</div>`).join('') || '—'}
                </div>
            </div>
        `;
    },

    /**
     * Render crypto-specific comparison metrics
     */
    renderCryptoComparison(ticker) {
        return `
            <div class="comparison-item">
                <div class="comparison-label">Core Idea</div>
                <div class="comparison-value">${Formatters.truncate(ticker.core_idea || '', 150)}</div>
            </div>
            <div class="comparison-item">
                <div class="comparison-label">Key Metrics</div>
                <div class="comparison-value">
                    ${Object.entries(ticker.metrics || {})
                        .slice(0, 5)
                        .map(([k, v]) => `<div>• ${k}: ${v}</div>`)
                        .join('') || '—'}
                </div>
            </div>
            <div class="comparison-item">
                <div class="comparison-label">Bull Triggers</div>
                <div class="comparison-value">
                    ${ticker.bull_triggers?.map(t => `<div>• ${t}</div>`).join('') || '—'}
                </div>
            </div>
            <div class="comparison-item">
                <div class="comparison-label">Bear Triggers</div>
                <div class="comparison-value">
                    ${ticker.bear_triggers?.map(t => `<div>• ${t}</div>`).join('') || '—'}
                </div>
            </div>
        `;
    }
};
