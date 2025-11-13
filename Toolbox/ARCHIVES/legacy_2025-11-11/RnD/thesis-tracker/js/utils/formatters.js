/**
 * Utility functions for formatting data
 */

const Formatters = {
    /**
     * Format a date string (YYYY-MM-DD) to a readable format
     */
    formatDate(dateString) {
        if (!dateString) return '—';
        try {
            const date = new Date(dateString + 'T00:00:00');
            return date.toLocaleDateString('en-US', {
                year: 'numeric',
                month: 'short',
                day: 'numeric'
            });
        } catch {
            return dateString;
        }
    },

    /**
     * Format a date as relative time (e.g., "2 days ago")
     */
    formatRelativeDate(dateString) {
        if (!dateString) return '—';
        try {
            const date = new Date(dateString + 'T00:00:00');
            const now = new Date();
            const daysAgo = Math.floor((now - date) / (1000 * 60 * 60 * 24));

            if (daysAgo === 0) return 'Today';
            if (daysAgo === 1) return 'Yesterday';
            if (daysAgo < 7) return `${daysAgo} days ago`;
            if (daysAgo < 30) return `${Math.floor(daysAgo / 7)} weeks ago`;
            if (daysAgo < 365) return `${Math.floor(daysAgo / 30)} months ago`;
            return `${Math.floor(daysAgo / 365)} years ago`;
        } catch {
            return dateString;
        }
    },

    /**
     * Format a number with currency
     */
    formatCurrency(value) {
        if (typeof value !== 'number') return value;
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD',
            minimumFractionDigits: 0,
            maximumFractionDigits: 0
        }).format(value);
    },

    /**
     * Format a large number with K/M/B suffix
     */
    formatNumber(value) {
        if (typeof value !== 'number') return value;
        if (value >= 1000000000) return (value / 1000000000).toFixed(1) + 'B';
        if (value >= 1000000) return (value / 1000000).toFixed(1) + 'M';
        if (value >= 1000) return (value / 1000).toFixed(1) + 'K';
        return Math.round(value).toString();
    },

    /**
     * Format a percentage
     */
    formatPercent(value, decimals = 1) {
        if (typeof value !== 'number') return value;
        return (value * 100).toFixed(decimals) + '%';
    },

    /**
     * Get score color class
     */
    getScoreClass(score) {
        if (score >= 80) return 'high';
        if (score >= 60) return 'medium';
        return 'low';
    },

    /**
     * Get score color
     */
    getScoreColor(score) {
        if (score >= 80) return '#10b981';  // green
        if (score >= 60) return '#f59e0b';  // yellow
        return '#ef4444';  // red
    },

    /**
     * Clean HTML/markdown characters from text
     */
    sanitize(text) {
        if (!text) return '';
        return text
            .replace(/\*\*/g, '')  // Remove bold markers
            .replace(/\*/g, '')    // Remove emphasis
            .replace(/`/g, '')     // Remove code markers
            .replace(/\n+/g, ' ')  // Replace newlines with spaces
            .trim();
    },

    /**
     * Truncate text to specified length
     */
    truncate(text, length = 100) {
        if (!text) return '';
        if (text.length <= length) return text;
        return text.substring(0, length) + '...';
    },

    /**
     * Get readable asset class name
     */
    assetClassName(assetClass) {
        const names = {
            'stock': 'Stock',
            'crypto': 'Crypto',
            'etf': 'ETF',
            'bond': 'Bond',
            'commodity': 'Commodity'
        };
        return names[assetClass] || assetClass;
    },

    /**
     * Format timestamp for last updated display
     */
    formatLastUpdated(isoString) {
        if (!isoString) return 'Unknown';
        try {
            const date = new Date(isoString);
            return date.toLocaleDateString('en-US', {
                year: 'numeric',
                month: 'short',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            });
        } catch {
            return 'Unknown';
        }
    }
};

// Export for use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = Formatters;
}
