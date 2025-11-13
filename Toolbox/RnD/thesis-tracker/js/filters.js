/**
 * Filters Module
 * Placeholder for advanced filter logic
 * Core filtering is handled in app.js
 */

const Filters = {
    /**
     * Apply text search across multiple fields
     */
    textSearch(tickers, query) {
        const q = query.toLowerCase();
        return tickers.filter(t =>
            t.ticker.toLowerCase().includes(q) ||
            t.theme?.toLowerCase().includes(q) ||
            t.core_idea?.toLowerCase().includes(q)
        );
    },

    /**
     * Filter by asset class
     */
    byAssetClass(tickers, assetClass) {
        if (!assetClass) return tickers;
        return tickers.filter(t => t.asset_class === assetClass);
    },

    /**
     * Filter by score range
     */
    byScoreRange(tickers, minScore) {
        if (minScore <= 0) return tickers;
        return tickers.filter(t => (t.scores?.total || 0) >= minScore);
    },

    /**
     * Filter by date range
     */
    byDateRange(tickers, startDate, endDate) {
        return tickers.filter(t => {
            const date = new Date(t.last_updated);
            return date >= startDate && date <= endDate;
        });
    }
};
