/**
 * Data Loader - Handles fetching and caching thesis data
 */

class DataLoader {
    constructor() {
        this.data = null;
        this.lastFetch = null;
        this.cacheExpiry = 5 * 60 * 1000;  // 5 minutes
        this.listeners = [];
    }

    /**
     * Load data from thesis_data.json
     */
    async load(forceRefresh = false) {
        // Check cache
        if (!forceRefresh && this.data && this.isValid()) {
            return this.data;
        }

        try {
            // Try to fetch from API first (if server is running)
            try {
                const response = await fetch('/api/thesis');
                if (response.ok) {
                    this.data = await response.json();
                    this.lastFetch = Date.now();
                    this.notifyListeners('dataLoaded');
                    return this.data;
                }
            } catch {
                // Fall back to local JSON file
            }

            // Fetch from local file
            const response = await fetch('../../../data/thesis_data.json');
            if (!response.ok) {
                throw new Error(`Failed to fetch thesis data: ${response.statusText}`);
            }

            this.data = await response.json();
            this.lastFetch = Date.now();
            this.notifyListeners('dataLoaded');
            return this.data;
        } catch (error) {
            console.error('Error loading thesis data:', error);
            this.notifyListeners('dataError', error);
            throw error;
        }
    }

    /**
     * Check if cached data is still valid
     */
    isValid() {
        if (!this.lastFetch) return false;
        return Date.now() - this.lastFetch < this.cacheExpiry;
    }

    /**
     * Get all tickers
     */
    getTickers() {
        return this.data?.tickers || [];
    }

    /**
     * Get single ticker by symbol
     */
    getTicker(symbol) {
        return this.getTickers().find(t => t.ticker === symbol);
    }

    /**
     * Filter tickers
     */
    filter(predicate) {
        return this.getTickers().filter(predicate);
    }

    /**
     * Get stock tickers only
     */
    getStocks() {
        return this.filter(t => t.asset_class === 'stock');
    }

    /**
     * Get crypto tickers only
     */
    getCrypto() {
        return this.filter(t => t.asset_class === 'crypto');
    }

    /**
     * Get summary statistics
     */
    getStats() {
        const tickers = this.getTickers();
        const stocks = this.getStocks();

        // Calculate average score (stocks only)
        const scores = stocks
            .map(s => s.scores?.total || 0)
            .filter(s => s > 0);
        const avgScore = scores.length > 0
            ? Math.round(scores.reduce((a, b) => a + b) / scores.length)
            : null;

        return {
            totalCount: tickers.length,
            stockCount: stocks.length,
            cryptoCount: tickers.length - stocks.length,
            avgScore: avgScore,
            lastGenerated: this.data?.last_generated
        };
    }

    /**
     * Subscribe to data events
     */
    subscribe(listener) {
        this.listeners.push(listener);
        return () => {
            this.listeners = this.listeners.filter(l => l !== listener);
        };
    }

    /**
     * Notify listeners
     */
    notifyListeners(event, data) {
        this.listeners.forEach(listener => {
            try {
                listener(event, data);
            } catch (error) {
                console.error('Error in listener:', error);
            }
        });
    }
}

// Create singleton instance
const dataLoader = new DataLoader();
