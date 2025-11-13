/**
 * Sorters Module
 * Placeholder for advanced sorting logic
 * Core sorting is handled in app.js
 */

const Sorters = {
    /**
     * Sort by score (high to low)
     */
    byScoreDesc(tickers) {
        return [...tickers].sort((a, b) => (b.scores?.total || 0) - (a.scores?.total || 0));
    },

    /**
     * Sort by score (low to high)
     */
    byScoreAsc(tickers) {
        return [...tickers].sort((a, b) => (a.scores?.total || 0) - (b.scores?.total || 0));
    },

    /**
     * Sort by date (newest first)
     */
    byDateDesc(tickers) {
        return [...tickers].sort((a, b) => new Date(b.last_updated) - new Date(a.last_updated));
    },

    /**
     * Sort by date (oldest first)
     */
    byDateAsc(tickers) {
        return [...tickers].sort((a, b) => new Date(a.last_updated) - new Date(b.last_updated));
    },

    /**
     * Sort by ticker (alphabetical)
     */
    byTickerAsc(tickers) {
        return [...tickers].sort((a, b) => a.ticker.localeCompare(b.ticker));
    }
};
