/**
 * Enhanced Visualization Component
 * Handles all Chart.js rendering and custom visualizations
 */

class VisualizationsEnhanced {
    constructor() {
        this.charts = {};
    }

    /**
     * Initialize all dashboard widgets
     */
    initDashboardWidgets(tickers) {
        const stocks = tickers.filter(t => t.asset_class === 'stock');

        this.renderFundamentalsQuality(stocks);
        this.renderRiskRewardScatter(stocks);
        this.renderConvictionGauges(tickers);
        this.renderPortfolioGaps(tickers);
        this.renderActionItems(tickers);
        this.renderPortfolioStats(tickers);
    }

    /**
     * Render Fundamentals Quality - Stacked Horizontal Bar Chart
     */
    renderFundamentalsQuality(stocks) {
        const canvas = document.getElementById('fundamentalsChart');
        if (!canvas) return;

        const topTickers = Analytics.getTopTickers(stocks, 8);

        if (topTickers.length === 0) {
            canvas.style.display = 'none';
            return;
        }

        // Destroy existing chart
        if (this.charts.fundamentals) {
            this.charts.fundamentals.destroy();
        }

        const ctx = canvas.getContext('2d');
        this.charts.fundamentals = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: topTickers.map(t => t.ticker),
                datasets: [
                    {
                        label: 'Fundamentals',
                        data: topTickers.map(t => t.fundamentals.percent),
                        backgroundColor: 'rgba(99, 102, 241, 0.8)',
                        borderColor: 'rgba(99, 102, 241, 1)',
                        borderWidth: 0
                    },
                    {
                        label: 'Technicals',
                        data: topTickers.map(t => t.technicals.percent),
                        backgroundColor: 'rgba(139, 92, 246, 0.8)',
                        borderColor: 'rgba(139, 92, 246, 1)',
                        borderWidth: 0
                    },
                    {
                        label: 'Management',
                        data: topTickers.map(t => t.management.percent),
                        backgroundColor: 'rgba(16, 185, 129, 0.8)',
                        borderColor: 'rgba(16, 185, 129, 1)',
                        borderWidth: 0
                    },
                    {
                        label: 'Risk',
                        data: topTickers.map(t => t.risk.percent),
                        backgroundColor: 'rgba(245, 158, 11, 0.8)',
                        borderColor: 'rgba(245, 158, 11, 1)',
                        borderWidth: 0
                    },
                    {
                        label: 'Sentiment',
                        data: topTickers.map(t => t.sentiment.percent),
                        backgroundColor: 'rgba(59, 130, 246, 0.8)',
                        borderColor: 'rgba(59, 130, 246, 1)',
                        borderWidth: 0
                    }
                ]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: true,
                scales: {
                    x: {
                        stacked: true,
                        min: 0,
                        max: 100,
                        grid: {
                            color: 'rgba(99, 102, 241, 0.1)',
                            drawBorder: false
                        },
                        ticks: {
                            color: 'rgba(160, 174, 192, 0.7)',
                            font: { size: 10 },
                            callback: (value) => value + '%'
                        }
                    },
                    y: {
                        stacked: true,
                        grid: { display: false },
                        ticks: {
                            color: 'rgba(224, 231, 255, 0.9)',
                            font: { weight: 600, size: 12 }
                        }
                    }
                },
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            color: 'rgba(224, 231, 255, 0.9)',
                            font: { size: 11, weight: 500 },
                            padding: 12,
                            usePointStyle: true
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(10, 14, 39, 0.9)',
                        borderColor: 'rgba(99, 102, 241, 0.5)',
                        borderWidth: 1,
                        titleColor: 'rgba(224, 231, 255, 1)',
                        bodyColor: 'rgba(224, 231, 255, 1)',
                        padding: 10,
                        callbacks: {
                            label: (context) => `${context.dataset.label}: ${context.parsed.x}%`
                        }
                    }
                }
            }
        });
    }

    /**
     * Render Risk-Reward Scatter Plot
     */
    renderRiskRewardScatter(stocks) {
        const canvas = document.getElementById('riskRewardChart');
        if (!canvas) return;

        const data = Analytics.getRiskRewardData(stocks);

        if (data.length === 0) {
            canvas.style.display = 'none';
            return;
        }

        // Destroy existing chart
        if (this.charts.riskReward) {
            this.charts.riskReward.destroy();
        }

        const ctx = canvas.getContext('2d');
        this.charts.riskReward = new Chart(ctx, {
            type: 'scatter',
            data: {
                datasets: [
                    {
                        label: 'High Conviction',
                        data: data.filter(d => d.conviction === 'high').map(d => ({
                            x: d.score,
                            y: (d.risk / d.riskMax) * 10,
                            ticker: d.ticker
                        })),
                        backgroundColor: 'rgba(16, 185, 129, 0.7)',
                        borderColor: 'rgba(16, 185, 129, 1)',
                        borderWidth: 2,
                        pointRadius: 6,
                        pointHoverRadius: 8
                    },
                    {
                        label: 'Medium Conviction',
                        data: data.filter(d => d.conviction === 'medium').map(d => ({
                            x: d.score,
                            y: (d.risk / d.riskMax) * 10,
                            ticker: d.ticker
                        })),
                        backgroundColor: 'rgba(245, 158, 11, 0.7)',
                        borderColor: 'rgba(245, 158, 11, 1)',
                        borderWidth: 2,
                        pointRadius: 6,
                        pointHoverRadius: 8
                    },
                    {
                        label: 'Speculative',
                        data: data.filter(d => d.conviction === 'speculative').map(d => ({
                            x: d.score,
                            y: (d.risk / d.riskMax) * 10,
                            ticker: d.ticker
                        })),
                        backgroundColor: 'rgba(239, 68, 68, 0.7)',
                        borderColor: 'rgba(239, 68, 68, 1)',
                        borderWidth: 2,
                        pointRadius: 6,
                        pointHoverRadius: 8
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'Conviction Score',
                            color: 'rgba(224, 231, 255, 0.9)',
                            font: { weight: 600 }
                        },
                        min: 0,
                        max: 100,
                        grid: {
                            color: 'rgba(99, 102, 241, 0.1)',
                            drawBorder: false
                        },
                        ticks: {
                            color: 'rgba(160, 174, 192, 0.7)',
                            font: { size: 10 }
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Risk Level',
                            color: 'rgba(224, 231, 255, 0.9)',
                            font: { weight: 600 }
                        },
                        min: 0,
                        max: 10,
                        grid: {
                            color: 'rgba(99, 102, 241, 0.1)',
                            drawBorder: false
                        },
                        ticks: {
                            color: 'rgba(160, 174, 192, 0.7)',
                            font: { size: 10 }
                        }
                    }
                },
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            color: 'rgba(224, 231, 255, 0.9)',
                            font: { size: 11, weight: 500 },
                            padding: 12,
                            usePointStyle: true,
                            pointStyle: 'circle'
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(10, 14, 39, 0.95)',
                        borderColor: 'rgba(99, 102, 241, 0.5)',
                        borderWidth: 1,
                        titleColor: 'rgba(224, 231, 255, 1)',
                        bodyColor: 'rgba(224, 231, 255, 1)',
                        padding: 12,
                        callbacks: {
                            title: (context) => context[0].raw.ticker,
                            label: (context) => [
                                `Conviction: ${context.raw.x.toFixed(0)}/100`,
                                `Risk: ${context.raw.y.toFixed(1)}/10`
                            ]
                        }
                    }
                }
            }
        });
    }

    /**
     * Render Conviction Strength Gauges (SVG-based)
     */
    renderConvictionGauges(tickers) {
        const container = document.getElementById('convictionContent');
        if (!container) return;

        const dist = Analytics.calculateConvictionDistribution(tickers);

        const html = `
            <div class="gauge-container">
                <div class="gauge">
                    <div class="gauge-ring">
                        ${this.createGaugeSVG(dist.high.percent, '#10b981')}
                    </div>
                    <div class="gauge-label">High Conviction</div>
                    <div class="gauge-value">${dist.high.count}</div>
                    <div class="gauge-percent">${dist.high.percent}%</div>
                </div>
                <div class="gauge">
                    <div class="gauge-ring">
                        ${this.createGaugeSVG(dist.medium.percent, '#f59e0b')}
                    </div>
                    <div class="gauge-label">Medium Conviction</div>
                    <div class="gauge-value">${dist.medium.count}</div>
                    <div class="gauge-percent">${dist.medium.percent}%</div>
                </div>
                <div class="gauge">
                    <div class="gauge-ring">
                        ${this.createGaugeSVG(dist.speculative.percent, '#ef4444')}
                    </div>
                    <div class="gauge-label">Speculative</div>
                    <div class="gauge-value">${dist.speculative.count}</div>
                    <div class="gauge-percent">${dist.speculative.percent}%</div>
                </div>
            </div>
            <div style="text-align: center; margin-top: var(--spacing-lg); padding-top: var(--spacing-lg); border-top: 1px solid var(--color-border);">
                <div style="font-size: 0.75rem; color: var(--color-text-secondary); margin-bottom: var(--spacing-sm);">Portfolio Strength</div>
                <div style="font-size: 2rem; font-weight: 700; color: var(--color-accent-primary);">${dist.strengthScore}%</div>
            </div>
        `;

        container.innerHTML = html;
    }

    /**
     * Create SVG gauge circle
     */
    createGaugeSVG(percent, color) {
        const circumference = 2 * Math.PI * 45; // radius = 45
        const offset = circumference - (percent / 100) * circumference;

        return `
            <svg viewBox="0 0 100 100">
                <circle cx="50" cy="50" r="45" fill="none" stroke="rgba(99, 102, 241, 0.1)" stroke-width="8"/>
                <circle
                    cx="50" cy="50" r="45"
                    fill="none"
                    stroke="${color}"
                    stroke-width="8"
                    stroke-dasharray="${circumference}"
                    stroke-dashoffset="${offset}"
                    stroke-linecap="round"
                    style="transition: stroke-dashoffset 0.5s ease;"
                />
            </svg>
        `;
    }

    /**
     * Render Portfolio Gaps - Theme Distribution
     */
    renderPortfolioGaps(tickers) {
        const canvas = document.getElementById('gapsChart');
        if (!canvas) return;

        const themes = Analytics.getThemeDistribution(tickers);

        if (themes.length === 0) {
            canvas.style.display = 'none';
            return;
        }

        // Destroy existing chart
        if (this.charts.gaps) {
            this.charts.gaps.destroy();
        }

        const ctx = canvas.getContext('2d');
        this.charts.gaps = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: themes.map(t => t.name),
                datasets: [
                    {
                        label: 'Count',
                        data: themes.map(t => t.count),
                        backgroundColor: themes.map(t => t.conviction),
                        borderColor: themes.map(t => t.conviction),
                        borderWidth: 2,
                        borderRadius: 6
                    }
                ]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: true,
                scales: {
                    x: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(99, 102, 241, 0.1)',
                            drawBorder: false
                        },
                        ticks: {
                            color: 'rgba(160, 174, 192, 0.7)',
                            font: { size: 10 }
                        }
                    },
                    y: {
                        grid: { display: false },
                        ticks: {
                            color: 'rgba(224, 231, 255, 0.9)',
                            font: { weight: 600, size: 11 }
                        }
                    }
                },
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        backgroundColor: 'rgba(10, 14, 39, 0.9)',
                        borderColor: 'rgba(99, 102, 241, 0.5)',
                        borderWidth: 1,
                        titleColor: 'rgba(224, 231, 255, 1)',
                        bodyColor: 'rgba(224, 231, 255, 1)',
                        padding: 10,
                        callbacks: {
                            afterLabel: (context) => {
                                const theme = themes[context.dataIndex];
                                return `Avg Score: ${theme.avgScore}/100`;
                            }
                        }
                    }
                }
            }
        });
    }

    /**
     * Render Action Items - Freshness & Completeness
     */
    renderActionItems(tickers) {
        const container = document.getElementById('actionItemsContent');
        if (!container) return;

        const health = Analytics.getThesisHealth(tickers);

        let html = '<div class="action-items-list">';

        // Outdated items (most urgent)
        health.outdated.forEach(item => {
            html += `
                <div class="action-item outdated">
                    <div class="action-item-icon">🔴</div>
                    <div class="action-item-content">
                        <div class="action-item-title">${item.ticker}</div>
                        <div class="action-item-detail">Thesis outdated (${item.daysOld} days)</div>
                    </div>
                </div>
            `;
        });

        // Stale items
        health.stale.forEach(item => {
            html += `
                <div class="action-item stale">
                    <div class="action-item-icon">⚠️</div>
                    <div class="action-item-content">
                        <div class="action-item-title">${item.ticker}</div>
                        <div class="action-item-detail">Thesis aging (${item.daysOld} days)</div>
                    </div>
                </div>
            `;
        });

        // Upcoming catalysts
        if (health.upcoming.length > 0) {
            health.upcoming.slice(0, 3).forEach(item => {
                html += `
                    <div class="action-item upcoming">
                        <div class="action-item-icon">✅</div>
                        <div class="action-item-content">
                            <div class="action-item-title">${item.ticker}</div>
                            <div class="action-item-detail">${item.event} (${item.date})</div>
                        </div>
                    </div>
                `;
            });
        }

        if (html === '<div class="action-items-list">') {
            html += '<div style="text-align: center; color: var(--color-text-secondary); padding: var(--spacing-lg);">All theses current & complete ✓</div>';
        }

        html += '</div>';
        container.innerHTML = html;
    }

    /**
     * Render Portfolio Statistics
     */
    renderPortfolioStats(tickers) {
        const container = document.getElementById('statsContent');
        if (!container) return;

        const stocks = tickers.filter(t => t.asset_class === 'stock');
        const stats = Analytics.getPortfolioStats(tickers);

        const html = `
            <div class="stats-grid">
                <div class="stat-box">
                    <div class="stat-box-value">${stats.avgScore}</div>
                    <div class="stat-box-label">Avg Score</div>
                </div>
                <div class="stat-box">
                    <div class="stat-box-value">${stats.avgFundamentals}</div>
                    <div class="stat-box-label">Avg Fundamentals</div>
                </div>
                <div class="stat-box">
                    <div class="stat-box-value">${stats.avgTechnicals}</div>
                    <div class="stat-box-label">Avg Technicals</div>
                </div>
                <div class="stat-box">
                    <div class="stat-box-value">${stats.avgRisk.toFixed(1)}</div>
                    <div class="stat-box-label">Avg Risk</div>
                </div>
                <div class="stat-box">
                    <div class="stat-box-value">${stats.highestScore}</div>
                    <div class="stat-box-label">Highest (${stats.highestTicker})</div>
                </div>
                <div class="stat-box">
                    <div class="stat-box-value">${stats.lowestScore}</div>
                    <div class="stat-box-label">Lowest (${stats.lowestTicker})</div>
                </div>
            </div>
        `;

        container.innerHTML = html;
    }

    /**
     * Clean up all charts
     */
    destroyAll() {
        Object.values(this.charts).forEach(chart => {
            if (chart) chart.destroy();
        });
        this.charts = {};
    }
}

// Create singleton instance
const visualizations = new VisualizationsEnhanced();
