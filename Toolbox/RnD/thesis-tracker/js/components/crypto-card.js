/**
 * Crypto-specific card component
 */

const CryptoCard = {
    /**
     * Render a crypto card
     */
    render(ticker) {
        const metricsCount = Object.keys(ticker.metrics || {}).length;

        return `
            <div class="thesis-card crypto-card" data-ticker="${ticker.ticker}">
                <div class="card-header">
                    <span class="card-ticker">${ticker.ticker}</span>
                    <span class="card-class">Crypto</span>
                </div>
                <div class="card-theme">${Formatters.truncate(ticker.core_idea || '', 80)}</div>
                <div style="color: #a0aec0; margin-bottom: var(--spacing-md); font-size: 0.85rem;">
                    ${metricsCount} Key Metrics
                </div>
                <div class="card-meta">
                    <span>${Formatters.formatRelativeDate(ticker.last_updated)}</span>
                </div>
            </div>
        `;
    }
};
