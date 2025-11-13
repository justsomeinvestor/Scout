/**
 * Visualization Component
 * Handles all Chart.js rendering for dashboard widgets and comparisons
 */

class Visualizations {
    constructor() {
        this.charts = {};
        this.chartConfigs = {
            topPerformers: null,
            scoreDist: null,
            assetAlloc: null,
            comparisonRadar: null
        };
    }

    /**
     * Initialize dashboard widgets
     */
    initDashboardWidgets(tickers) {
        const stocks = tickers.filter(t => t.asset_class === 'stock');

        this.renderTopPerformers(stocks);
        this.renderScoreDistribution(stocks);
        this.renderAssetAllocation(tickers);
    }

    /**
     * Render top performers bar chart
     */
    renderTopPerformers(stocks) {
        const canvas = document.getElementById('topPerformersChart');
        if (!canvas) return;

        // Get top 5 by score
        const top5 = stocks
            .filter(s => s.scores?.total > 0)
            .sort((a, b) => (b.scores?.total || 0) - (a.scores?.total || 0))
            .slice(0, 5);

        if (top5.length === 0) {
            canvas.style.display = 'none';
            return;
        }

        // Destroy existing chart
        if (this.charts.topPerformers) {
            this.charts.topPerformers.destroy();
        }

        const ctx = canvas.getContext('2d');
        this.charts.topPerformers = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: top5.map(t => t.ticker),
                datasets: [{
                    label: 'Score',
                    data: top5.map(t => t.scores?.total || 0),
                    backgroundColor: [
                        'rgba(99, 102, 241, 0.8)',
                        'rgba(139, 92, 246, 0.8)',
                        'rgba(16, 185, 129, 0.8)',
                        'rgba(245, 158, 11, 0.8)',
                        'rgba(59, 130, 246, 0.8)'
                    ],
                    borderColor: [
                        'rgba(99, 102, 241, 1)',
                        'rgba(139, 92, 246, 1)',
                        'rgba(16, 185, 129, 1)',
                        'rgba(245, 158, 11, 1)',
                        'rgba(59, 130, 246, 1)'
                    ],
                    borderWidth: 2,
                    borderRadius: 6,
                    hoverBackgroundColor: 'rgba(99, 102, 241, 0.95)',
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        backgroundColor: 'rgba(10, 14, 39, 0.9)',
                        borderColor: 'rgba(99, 102, 241, 0.5)',
                        borderWidth: 1,
                        titleColor: 'rgba(224, 231, 255, 1)',
                        bodyColor: 'rgba(224, 231, 255, 1)',
                        padding: 12,
                        displayColors: false,
                        callbacks: {
                            label: (context) => `Score: ${context.parsed.x}/100`
                        }
                    }
                },
                scales: {
                    x: {
                        beginAtZero: true,
                        max: 100,
                        grid: {
                            color: 'rgba(99, 102, 241, 0.1)',
                            drawBorder: false
                        },
                        ticks: {
                            color: 'rgba(160, 174, 192, 0.7)',
                            font: {
                                size: 11
                            }
                        }
                    },
                    y: {
                        grid: {
                            display: false
                        },
                        ticks: {
                            color: 'rgba(224, 231, 255, 0.9)',
                            font: {
                                weight: 600,
                                size: 12
                            }
                        }
                    }
                }
            }
        });
    }

    /**
     * Render score distribution histogram
     */
    renderScoreDistribution(stocks) {
        const canvas = document.getElementById('scoreDistChart');
        if (!canvas) return;

        // Create score buckets
        const buckets = {
            '0-20': 0,
            '20-40': 0,
            '40-60': 0,
            '60-80': 0,
            '80-100': 0
        };

        stocks.forEach(stock => {
            const score = stock.scores?.total || 0;
            if (score < 20) buckets['0-20']++;
            else if (score < 40) buckets['20-40']++;
            else if (score < 60) buckets['40-60']++;
            else if (score < 80) buckets['60-80']++;
            else buckets['80-100']++;
        });

        // Destroy existing chart
        if (this.charts.scoreDist) {
            this.charts.scoreDist.destroy();
        }

        const ctx = canvas.getContext('2d');
        this.charts.scoreDist = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: Object.keys(buckets),
                datasets: [{
                    data: Object.values(buckets),
                    backgroundColor: [
                        'rgba(239, 68, 68, 0.8)',      // red < 20
                        'rgba(245, 158, 11, 0.8)',     // yellow 20-40
                        'rgba(59, 130, 246, 0.8)',     // blue 40-60
                        'rgba(34, 197, 94, 0.8)',      // green 60-80
                        'rgba(16, 185, 129, 0.8)'      // emerald 80-100
                    ],
                    borderColor: 'rgba(10, 14, 39, 0.9)',
                    borderWidth: 3,
                    hoverOffset: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            color: 'rgba(224, 231, 255, 0.9)',
                            font: {
                                size: 11
                            },
                            padding: 12,
                            generateLabels: (chart) => {
                                const labels = chart.data.labels;
                                const data = chart.data.datasets[0].data;
                                return labels.map((label, i) => ({
                                    text: `${label} (${data[i]})`,
                                    fillStyle: chart.data.datasets[0].backgroundColor[i],
                                    hidden: false,
                                    index: i
                                }));
                            }
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(10, 14, 39, 0.9)',
                        borderColor: 'rgba(99, 102, 241, 0.5)',
                        borderWidth: 1,
                        titleColor: 'rgba(224, 231, 255, 1)',
                        bodyColor: 'rgba(224, 231, 255, 1)',
                        callbacks: {
                            label: (context) => `Count: ${context.parsed}`
                        }
                    }
                }
            }
        });
    }

    /**
     * Render asset allocation pie chart
     */
    renderAssetAllocation(tickers) {
        const canvas = document.getElementById('assetAllocChart');
        if (!canvas) return;

        const stocks = tickers.filter(t => t.asset_class === 'stock').length;
        const crypto = tickers.filter(t => t.asset_class === 'crypto').length;

        // Destroy existing chart
        if (this.charts.assetAlloc) {
            this.charts.assetAlloc.destroy();
        }

        const ctx = canvas.getContext('2d');
        this.charts.assetAlloc = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Stocks', 'Crypto'],
                datasets: [{
                    data: [stocks, crypto],
                    backgroundColor: [
                        'rgba(99, 102, 241, 0.8)',
                        'rgba(139, 92, 246, 0.8)'
                    ],
                    borderColor: 'rgba(10, 14, 39, 0.9)',
                    borderWidth: 3,
                    hoverOffset: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            color: 'rgba(224, 231, 255, 0.9)',
                            font: {
                                size: 12,
                                weight: 600
                            },
                            padding: 15,
                            generateLabels: (chart) => {
                                const labels = chart.data.labels;
                                const data = chart.data.datasets[0].data;
                                return labels.map((label, i) => ({
                                    text: `${label} (${data[i]})`,
                                    fillStyle: chart.data.datasets[0].backgroundColor[i],
                                    hidden: false,
                                    index: i
                                }));
                            }
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(10, 14, 39, 0.9)',
                        borderColor: 'rgba(99, 102, 241, 0.5)',
                        borderWidth: 1,
                        titleColor: 'rgba(224, 231, 255, 1)',
                        bodyColor: 'rgba(224, 231, 255, 1)',
                        callbacks: {
                            label: (context) => `Count: ${context.parsed}`
                        }
                    }
                }
            }
        });
    }

    /**
     * Render comparison radar chart for stocks
     */
    renderComparisonRadar(selectedTickers) {
        const canvas = document.getElementById('comparisonRadarChart');
        const chartsContainer = document.getElementById('comparisonCharts');

        if (!canvas || !chartsContainer) return;

        // Filter only stocks
        const stocks = selectedTickers.filter(t => t.asset_class === 'stock');

        if (stocks.length === 0) {
            chartsContainer.style.display = 'none';
            return;
        }

        chartsContainer.style.display = 'block';

        // Destroy existing chart
        if (this.charts.comparisonRadar) {
            this.charts.comparisonRadar.destroy();
        }

        const dimensions = ['Fundamentals', 'Technicals', 'Management', 'Risk', 'Sentiment'];
        const colors = [
            'rgba(99, 102, 241, 0.2)',
            'rgba(139, 92, 246, 0.2)',
            'rgba(16, 185, 129, 0.2)',
            'rgba(245, 158, 11, 0.2)',
            'rgba(59, 130, 246, 0.2)'
        ];
        const borderColors = [
            'rgba(99, 102, 241, 1)',
            'rgba(139, 92, 246, 1)',
            'rgba(16, 185, 129, 1)',
            'rgba(245, 158, 11, 1)',
            'rgba(59, 130, 246, 1)'
        ];

        const datasets = stocks.map((ticker, idx) => ({
            label: ticker.ticker,
            data: [
                (ticker.scores?.fundamentals || 0) / (ticker.scores?.fundamentals_max || 40) * 100,
                (ticker.scores?.technicals || 0) / (ticker.scores?.technicals_max || 25) * 100,
                (ticker.scores?.management || 0) / (ticker.scores?.management_max || 15) * 100,
                (ticker.scores?.risk || 0) / (ticker.scores?.risk_max || 10) * 100,
                (ticker.scores?.sentiment || 0) / (ticker.scores?.sentiment_max || 10) * 100
            ],
            borderColor: borderColors[idx % borderColors.length],
            backgroundColor: colors[idx % colors.length],
            borderWidth: 2,
            pointRadius: 4,
            pointBackgroundColor: borderColors[idx % borderColors.length],
            pointBorderColor: 'rgba(10, 14, 39, 1)',
            pointBorderWidth: 2,
            pointHoverRadius: 6,
            fill: true,
            tension: 0.3
        }));

        const ctx = canvas.getContext('2d');
        this.charts.comparisonRadar = new Chart(ctx, {
            type: 'radar',
            data: {
                labels: dimensions,
                datasets: datasets
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                indexAxis: 'r',
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            color: 'rgba(224, 231, 255, 0.9)',
                            font: {
                                size: 12,
                                weight: 600
                            },
                            padding: 15,
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
                            label: (context) => `${context.label}: ${context.parsed.r.toFixed(1)}%`
                        }
                    }
                },
                scales: {
                    r: {
                        beginAtZero: true,
                        max: 100,
                        grid: {
                            color: 'rgba(99, 102, 241, 0.1)',
                            drawBorder: false
                        },
                        ticks: {
                            color: 'rgba(160, 174, 192, 0.7)',
                            font: {
                                size: 10
                            },
                            backdropColor: 'transparent',
                            showLabelBackdrop: false
                        },
                        pointLabels: {
                            color: 'rgba(224, 231, 255, 0.9)',
                            font: {
                                size: 12,
                                weight: 600
                            }
                        }
                    }
                }
            }
        });
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
const visualizations = new Visualizations();
