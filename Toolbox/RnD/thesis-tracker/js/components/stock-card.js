/**
 * Stock-specific card component
 * Placeholder for future enhancements like radar charts
 */

const StockCard = {
    /**
     * Render a stock card
     */
    render(ticker) {
        const scoreClass = Formatters.getScoreClass(ticker.scores?.total || 0);

        return `
            <div class="thesis-card stock-card" data-ticker="${ticker.ticker}">
                <div class="card-header">
                    <span class="card-ticker">${ticker.ticker}</span>
                    <span class="card-class">Stock</span>
                </div>
                <div class="card-theme">${Formatters.truncate(ticker.theme || '', 80)}</div>
                <div class="card-score ${scoreClass}">${ticker.scores?.total || '—'}</div>
                <div style="font-size: 0.75rem; color: #a0aec0; margin-bottom: var(--spacing-md);">
                    / ${ticker.scores?.total_max || 100}
                </div>
                <div class="card-meta">
                    <span>${Formatters.formatRelativeDate(ticker.last_updated)}</span>
                </div>
            </div>
        `;
    }
};
