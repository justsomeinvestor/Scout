/**
 * Analytics Module
 * Computed metrics and aggregations for thesis tracker
 */

const Analytics = {
    /**
     * Calculate conviction level categories
     */
    getConvictionCategory(score) {
        if (score >= 75) return 'high';
        if (score >= 50) return 'medium';
        return 'speculative';
    },

    /**
     * Get color for conviction level
     */
    getConvictionColor(score) {
        if (score >= 75) return '#10b981';  // green
        if (score >= 50) return '#f59e0b';  // yellow
        return '#ef4444';  // red
    },

    /**
     * Calculate conviction distribution across portfolio
     */
    calculateConvictionDistribution(tickers) {
        const stocks = tickers.filter(t => t.asset_class === 'stock' && t.scores?.total);

        const high = stocks.filter(t => t.scores.total >= 75).length;
        const medium = stocks.filter(t => t.scores.total >= 50 && t.scores.total < 75).length;
        const speculative = stocks.filter(t => t.scores.total < 50).length;

        const total = stocks.length;

        return {
            high: { count: high, percent: total > 0 ? Math.round((high / total) * 100) : 0 },
            medium: { count: medium, percent: total > 0 ? Math.round((medium / total) * 100) : 0 },
            speculative: { count: speculative, percent: total > 0 ? Math.round((speculative / total) * 100) : 0 },
            total: total,
            strengthScore: total > 0 ? Math.round(((high * 1.0 + medium * 0.5 + speculative * 0.1) / total) * 100) : 0
        };
    },

    /**
     * Normalize score to 0-100 percentage
     */
    normalizeScore(value, max) {
        if (!max || max === 0) return 0;
        return Math.round((value / max) * 100);
    },

    /**
     * Calculate score breakdown percentages for stacked bar
     */
    getScoreBreakdown(ticker) {
        const scores = ticker.scores || {};
        const total = scores.total || 0;

        if (total === 0) return null;

        return {
            ticker: ticker.ticker,
            total: total,
            fundamentals: {
                value: scores.fundamentals || 0,
                percent: Math.round(((scores.fundamentals || 0) / total) * 100)
            },
            technicals: {
                value: scores.technicals || 0,
                percent: Math.round(((scores.technicals || 0) / total) * 100)
            },
            management: {
                value: scores.management || 0,
                percent: Math.round(((scores.management || 0) / total) * 100)
            },
            risk: {
                value: scores.risk || 0,
                percent: Math.round(((scores.risk || 0) / total) * 100)
            },
            sentiment: {
                value: scores.sentiment || 0,
                percent: Math.round(((scores.sentiment || 0) / total) * 100)
            }
        };
    },

    /**
     * Get top N tickers by score
     */
    getTopTickers(tickers, count = 8) {
        return tickers
            .filter(t => t.asset_class === 'stock' && t.scores?.total > 0)
            .sort((a, b) => (b.scores?.total || 0) - (a.scores?.total || 0))
            .slice(0, count)
            .map(t => this.getScoreBreakdown(t))
            .filter(b => b !== null);
    },

    /**
     * Extract theme categories from thesis theme strings
     */
    extractTheme(themeString) {
        if (!themeString) return 'Other';

        const lower = themeString.toLowerCase();

        // Map keywords to categories
        if (lower.includes('ai') || lower.includes('artificial') || lower.includes('machine learning')) return 'AI & ML';
        if (lower.includes('healthcare') || lower.includes('pharma') || lower.includes('medical')) return 'Healthcare';
        if (lower.includes('consumer') || lower.includes('retail')) return 'Consumer';
        if (lower.includes('energy') || lower.includes('oil') || lower.includes('gas')) return 'Energy';
        if (lower.includes('financial') || lower.includes('bank')) return 'Finance';
        if (lower.includes('semiconductor') || lower.includes('chip')) return 'Semiconductors';
        if (lower.includes('cloud') || lower.includes('infrastructure') || lower.includes('computing')) return 'Cloud & Infrastructure';
        if (lower.includes('automotive') || lower.includes('ev')) return 'Automotive';

        return 'Other';
    },

    /**
     * Analyze portfolio theme distribution
     */
    getThemeDistribution(tickers) {
        const stocks = tickers.filter(t => t.asset_class === 'stock');
        const themes = {};

        stocks.forEach(ticker => {
            const theme = this.extractTheme(ticker.theme);
            if (!themes[theme]) {
                themes[theme] = { count: 0, totalScore: 0, conviction: 0, tickers: [] };
            }
            themes[theme].count++;
            themes[theme].totalScore += ticker.scores?.total || 0;
            themes[theme].avgScore = Math.round(themes[theme].totalScore / themes[theme].count);
            themes[theme].tickers.push(ticker.ticker);
            themes[theme].conviction = this.getConvictionColor(themes[theme].avgScore);
        });

        // Sort by count descending
        return Object.entries(themes)
            .map(([name, data]) => ({ name, ...data }))
            .sort((a, b) => b.count - a.count);
    },

    /**
     * Prepare risk-reward scatter plot data
     */
    getRiskRewardData(tickers) {
        return tickers
            .filter(t => t.asset_class === 'stock' && t.scores?.total > 0)
            .map(t => ({
                ticker: t.ticker,
                score: t.scores?.total || 0,
                risk: t.scores?.risk || 0,
                riskMax: t.scores?.risk_max || 10,
                riskCount: (t.risks || []).length,
                conviction: this.getConvictionCategory(t.scores?.total || 0),
                color: this.getConvictionColor(t.scores?.total || 0),
                theme: this.extractTheme(t.theme)
            }))
            .sort((a, b) => b.score - a.score);
    },

    /**
     * Analyze data freshness and completeness
     */
    getThesisHealth(tickers) {
        const now = new Date();
        const stale = [];
        const outdated = [];
        const incomplete = [];
        const upcoming = [];

        tickers.forEach(ticker => {
            const lastUpdated = new Date(ticker.last_updated);
            const daysOld = Math.floor((now - lastUpdated) / (1000 * 60 * 60 * 24));

            // Check freshness
            if (daysOld > 60) {
                outdated.push({ ticker: ticker.ticker, daysOld });
            } else if (daysOld > 30) {
                stale.push({ ticker: ticker.ticker, daysOld });
            }

            // Check completeness (stocks only)
            if (ticker.asset_class === 'stock') {
                const scores = ticker.scores || {};
                const missingFields = [];
                if (!scores.fundamentals) missingFields.push('fundamentals');
                if (!scores.technicals) missingFields.push('technicals');
                if (!ticker.pillars || ticker.pillars.length === 0) missingFields.push('pillars');
                if (!ticker.catalysts || ticker.catalysts.length === 0) missingFields.push('catalysts');

                if (missingFields.length > 0) {
                    incomplete.push({ ticker: ticker.ticker, missing: missingFields });
                }
            }

            // Check upcoming catalysts
            if (ticker.catalysts && ticker.catalysts.length > 0) {
                ticker.catalysts.forEach(catalyst => {
                    // Try to parse catalyst date (basic format)
                    if (catalyst.date && !catalyst.date.includes('TBA')) {
                        upcoming.push({
                            ticker: ticker.ticker,
                            event: catalyst.event,
                            date: catalyst.date
                        });
                    }
                });
            }
        });

        return {
            stale: stale.slice(0, 5),      // >30 days
            outdated: outdated.slice(0, 5), // >60 days
            incomplete: incomplete.slice(0, 5),
            upcoming: upcoming.slice(0, 8),
            totalIssues: stale.length + outdated.length + incomplete.length
        };
    },

    /**
     * Get portfolio-wide statistics
     */
    getPortfolioStats(tickers) {
        const stocks = tickers.filter(t => t.asset_class === 'stock' && t.scores?.total > 0);

        if (stocks.length === 0) {
            return {
                avgScore: 0,
                highestScore: 0,
                highestTicker: '—',
                lowestScore: 0,
                lowestTicker: '—',
                avgFundamentals: 0,
                avgTechnicals: 0,
                avgRisk: 0
            };
        }

        const scores = stocks.map(t => t.scores?.total || 0);
        const fundamentals = stocks.map(t => this.normalizeScore(t.scores?.fundamentals || 0, t.scores?.fundamentals_max || 40));
        const technicals = stocks.map(t => this.normalizeScore(t.scores?.technicals || 0, t.scores?.technicals_max || 25));
        const risks = stocks.map(t => t.scores?.risk || 0);

        const avgScore = Math.round(scores.reduce((a, b) => a + b) / scores.length);
        const maxScore = Math.max(...scores);
        const minScore = Math.min(...scores);
        const maxTicker = stocks.find(t => t.scores?.total === maxScore)?.ticker || '—';
        const minTicker = stocks.find(t => t.scores?.total === minScore)?.ticker || '—';

        return {
            avgScore: avgScore,
            highestScore: maxScore,
            highestTicker: maxTicker,
            lowestScore: minScore,
            lowestTicker: minTicker,
            avgFundamentals: Math.round(fundamentals.reduce((a, b) => a + b) / fundamentals.length),
            avgTechnicals: Math.round(technicals.reduce((a, b) => a + b) / technicals.length),
            avgRisk: Math.round(risks.reduce((a, b) => a + b) / risks.length * 10) / 10
        };
    }
};

// Export for use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = Analytics;
}
