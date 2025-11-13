/**
 * Main Application Logic
 */

class ThesisTrackerApp {
    constructor() {
        this.allTickers = [];
        this.filteredTickers = [];
        this.currentView = 'grid';
        this.currentModalIndex = -1;
        this.selectedForComparison = new Set();

        this.initElements();
        this.attachEventListeners();
        this.loadData();
    }

    /**
     * Initialize DOM elements
     */
    initElements() {
        // Filters
        this.searchInput = document.getElementById('searchInput');
        this.assetClassFilter = document.getElementById('assetClassFilter');
        this.scoreRange = document.getElementById('scoreRange');
        this.scoreRangeDisplay = document.getElementById('scoreRangeDisplay');
        this.sortBy = document.getElementById('sortBy');

        // View controls
        this.viewBtns = document.querySelectorAll('.view-btn');
        this.views = document.querySelectorAll('.view');

        // Content areas
        this.thesisGrid = document.getElementById('thesisGrid');
        this.tableBody = document.getElementById('tableBody');
        this.comparisonCheckboxes = document.getElementById('comparisonCheckboxes');
        this.comparisonResults = document.getElementById('comparisonResults');

        // Stats
        this.totalCount = document.getElementById('totalCount');
        this.stockCount = document.getElementById('stockCount');
        this.cryptoCount = document.getElementById('cryptoCount');
        this.avgScore = document.getElementById('avgScore');
        this.lastUpdated = document.getElementById('lastUpdated');

        // Modal
        this.modal = document.getElementById('thesisModal');
        this.modalOverlay = document.getElementById('modalOverlay');
        this.modalClose = document.getElementById('modalClose');
        this.modalPrev = document.getElementById('modalPrev');
        this.modalNext = document.getElementById('modalNext');
        this.modalTicker = document.getElementById('modalTicker');
        this.modalClass = document.getElementById('modalClass');
        this.quickStats = document.getElementById('quickStats');
        this.markdownContent = document.getElementById('markdownContent');
        this.openFileBtn = document.getElementById('openFileBtn');

        // Actions
        this.refreshBtn = document.getElementById('refreshBtn');
        this.compareBtn = document.getElementById('compareBtn');
    }

    /**
     * Attach event listeners
     */
    attachEventListeners() {
        // Filter events
        this.searchInput.addEventListener('input', () => this.applyFilters());
        this.assetClassFilter.addEventListener('change', () => {
            this.updateScoreFilterVisibility();
            this.applyFilters();
        });
        this.scoreRange.addEventListener('input', () => {
            this.scoreRangeDisplay.textContent = `${this.scoreRange.value}+`;
            this.applyFilters();
        });
        this.sortBy.addEventListener('change', () => this.applyFilters());

        // View switching
        this.viewBtns.forEach(btn => {
            btn.addEventListener('click', () => this.switchView(btn.dataset.view));
        });

        // Modal controls
        this.modalClose.addEventListener('click', () => this.closeModal());
        this.modalOverlay.addEventListener('click', () => this.closeModal());
        this.modalPrev.addEventListener('click', () => this.previousModal());
        this.modalNext.addEventListener('click', () => this.nextModal());

        // Other
        this.refreshBtn.addEventListener('click', () => this.loadData(true));
        this.compareBtn.addEventListener('click', () => this.performComparison());

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (!this.modal.classList.contains('active')) return;
            if (e.key === 'Escape') this.closeModal();
            if (e.key === 'ArrowLeft') this.previousModal();
            if (e.key === 'ArrowRight') this.nextModal();
        });
    }

    /**
     * Load data from data loader
     */
    async loadData(forceRefresh = false) {
        try {
            const data = await dataLoader.load(forceRefresh);
            this.allTickers = data.tickers || [];
            this.updateStats();
            // Initialize dashboard widgets
            visualizations.initDashboardWidgets(this.allTickers);
            this.applyFilters();
        } catch (error) {
            console.error('Failed to load data:', error);
            this.thesisGrid.innerHTML = '<div class="error">Failed to load thesis data. Please try again.</div>';
        }
    }

    /**
     * Update statistics display
     */
    updateStats() {
        const stats = dataLoader.getStats();

        this.totalCount.textContent = stats.totalCount;
        this.stockCount.textContent = stats.stockCount;
        this.cryptoCount.textContent = stats.cryptoCount;
        this.avgScore.textContent = stats.avgScore !== null ? stats.avgScore : '—';

        if (stats.lastGenerated) {
            this.lastUpdated.textContent = Formatters.formatLastUpdated(stats.lastGenerated);
        }
    }

    /**
     * Show/hide score filter based on asset class
     */
    updateScoreFilterVisibility() {
        const assetClass = this.assetClassFilter.value;
        const scoreFilterGroup = document.getElementById('scoreFilterGroup');
        scoreFilterGroup.style.display = assetClass === 'stock' ? 'block' : 'none';
    }

    /**
     * Apply all active filters
     */
    applyFilters() {
        let filtered = [...this.allTickers];

        // Search
        const search = this.searchInput.value.toLowerCase();
        if (search) {
            filtered = filtered.filter(t =>
                t.ticker.toLowerCase().includes(search) ||
                t.theme?.toLowerCase().includes(search) ||
                t.core_idea?.toLowerCase().includes(search)
            );
        }

        // Asset class
        const assetClass = this.assetClassFilter.value;
        if (assetClass) {
            filtered = filtered.filter(t => t.asset_class === assetClass);
        }

        // Score range (stocks only)
        const minScore = parseInt(this.scoreRange.value);
        if (minScore > 0) {
            filtered = filtered.filter(t => (t.scores?.total || 0) >= minScore);
        }

        // Apply sorting
        const sortBy = this.sortBy.value;
        filtered = this.sortTickers(filtered, sortBy);

        this.filteredTickers = filtered;
        this.render();
    }

    /**
     * Sort tickers
     */
    sortTickers(tickers, sortBy) {
        const sorted = [...tickers];

        switch (sortBy) {
            case 'score-desc':
                return sorted.sort((a, b) => (b.scores?.total || 0) - (a.scores?.total || 0));
            case 'score-asc':
                return sorted.sort((a, b) => (a.scores?.total || 0) - (b.scores?.total || 0));
            case 'date-desc':
                return sorted.sort((a, b) => new Date(b.last_updated) - new Date(a.last_updated));
            case 'date-asc':
                return sorted.sort((a, b) => new Date(a.last_updated) - new Date(b.last_updated));
            case 'ticker-asc':
                return sorted.sort((a, b) => a.ticker.localeCompare(b.ticker));
            default:
                return sorted;
        }
    }

    /**
     * Render current view
     */
    render() {
        switch (this.currentView) {
            case 'grid':
                this.renderGrid();
                break;
            case 'table':
                this.renderTable();
                break;
            case 'comparison':
                this.renderComparisonSelector();
                break;
        }
    }

    /**
     * Render grid view
     */
    renderGrid() {
        if (this.filteredTickers.length === 0) {
            this.thesisGrid.innerHTML = '<div class="loading">No results found</div>';
            return;
        }

        this.thesisGrid.innerHTML = this.filteredTickers.map((ticker, index) => {
            const scoreClass = Formatters.getScoreClass(ticker.scores?.total || 0);
            const isStock = ticker.asset_class === 'stock';

            return `
                <div class="thesis-card" data-ticker="${ticker.ticker}" data-index="${index}">
                    <div class="card-header">
                        <span class="card-ticker">${ticker.ticker}</span>
                        <span class="card-class">${Formatters.assetClassName(ticker.asset_class)}</span>
                    </div>
                    <div class="card-theme">${Formatters.truncate(ticker.theme || ticker.core_idea || 'No description', 80)}</div>
                    ${isStock ? `
                        <div class="card-score ${scoreClass}">${ticker.scores?.total || '—'}</div>
                        <div style="font-size: 0.75rem; color: #a0aec0; margin-bottom: var(--spacing-md);">
                            / ${ticker.scores?.total_max || 100}
                        </div>
                    ` : `
                        <div style="color: #a0aec0; margin-bottom: var(--spacing-md); font-size: 0.85rem;">
                            Metrics: ${Object.keys(ticker.metrics || {}).length}
                        </div>
                    `}
                    <div class="card-meta">
                        <span>${Formatters.formatRelativeDate(ticker.last_updated)}</span>
                        <span>Updated ${Formatters.formatDate(ticker.last_updated)}</span>
                    </div>
                </div>
            `;
        }).join('');

        // Attach card click handlers
        document.querySelectorAll('.thesis-card').forEach((card, idx) => {
            card.addEventListener('click', () => this.openModal(idx));
        });
    }

    /**
     * Render table view
     */
    renderTable() {
        if (this.filteredTickers.length === 0) {
            this.tableBody.innerHTML = '<tr><td colspan="5" style="text-align: center; padding: 2rem;">No results found</td></tr>';
            return;
        }

        this.tableBody.innerHTML = this.filteredTickers.map((ticker, index) => {
            const isStock = ticker.asset_class === 'stock';
            const scoreClass = Formatters.getScoreClass(ticker.scores?.total || 0);

            return `
                <tr data-ticker="${ticker.ticker}" data-index="${index}" style="cursor: pointer;">
                    <td class="table-ticker">${ticker.ticker}</td>
                    <td>${Formatters.assetClassName(ticker.asset_class)}</td>
                    <td>${Formatters.truncate(ticker.theme || ticker.core_idea || '—', 50)}</td>
                    <td class="table-score ${scoreClass}">
                        ${isStock ? ticker.scores?.total || '—' : 'N/A'}
                    </td>
                    <td>${Formatters.formatDate(ticker.last_updated)}</td>
                </tr>
            `;
        }).join('');

        // Attach row click handlers
        document.querySelectorAll('tbody tr').forEach((row, idx) => {
            row.addEventListener('click', () => this.openModal(idx));
        });
    }

    /**
     * Render comparison selector
     */
    renderComparisonSelector() {
        this.comparisonCheckboxes.innerHTML = this.filteredTickers.map((ticker, index) => `
            <div class="comparison-checkbox">
                <input
                    type="checkbox"
                    id="comp-${ticker.ticker}"
                    value="${ticker.ticker}"
                    data-index="${index}"
                >
                <label for="comp-${ticker.ticker}">${ticker.ticker}</label>
            </div>
        `).join('');

        document.querySelectorAll('#comparisonCheckboxes input').forEach(checkbox => {
            checkbox.addEventListener('change', (e) => {
                if (e.target.checked) {
                    if (this.selectedForComparison.size < 4) {
                        this.selectedForComparison.add(parseInt(e.target.dataset.index));
                    } else {
                        e.target.checked = false;
                        alert('Maximum 4 tickers can be compared');
                    }
                } else {
                    this.selectedForComparison.delete(parseInt(e.target.dataset.index));
                }
            });
        });
    }

    /**
     * Perform comparison
     */
    performComparison() {
        if (this.selectedForComparison.size === 0) {
            alert('Please select at least one ticker to compare');
            return;
        }

        const selected = Array.from(this.selectedForComparison)
            .map(idx => this.filteredTickers[idx])
            .filter(t => t);

        // Render radar chart for stocks
        visualizations.renderComparisonRadar(selected);

        this.comparisonResults.innerHTML = selected.map(ticker => {
            const isStock = ticker.asset_class === 'stock';

            return `
                <div class="comparison-card">
                    <div class="comparison-card-title">${ticker.ticker}</div>
                    <div class="comparison-item">
                        <div class="comparison-label">Asset Class</div>
                        <div class="comparison-value">${Formatters.assetClassName(ticker.asset_class)}</div>
                    </div>
                    <div class="comparison-item">
                        <div class="comparison-label">Theme</div>
                        <div class="comparison-value">${Formatters.truncate(ticker.theme || ticker.core_idea || '—', 100)}</div>
                    </div>
                    ${isStock ? `
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
                    ` : `
                        <div class="comparison-item">
                            <div class="comparison-label">Key Metrics</div>
                            <div class="comparison-value">
                                ${Object.entries(ticker.metrics || {})
                                    .slice(0, 3)
                                    .map(([k, v]) => `<div>${k}: ${v}</div>`)
                                    .join('')}
                            </div>
                        </div>
                    `}
                    <div class="comparison-item">
                        <div class="comparison-label">Last Updated</div>
                        <div class="comparison-value">${Formatters.formatDate(ticker.last_updated)}</div>
                    </div>
                </div>
            `;
        }).join('');

        this.comparisonResults.style.display = 'grid';
    }

    /**
     * Switch view mode
     */
    switchView(view) {
        this.currentView = view;

        // Update buttons
        this.viewBtns.forEach(btn => {
            btn.classList.toggle('active', btn.dataset.view === view);
        });

        // Update views
        this.views.forEach(v => {
            v.style.display = v.id === `${view}View` ? 'block' : 'none';
        });

        this.render();
    }

    /**
     * Open modal with thesis details
     */
    openModal(index) {
        this.currentModalIndex = index;
        const ticker = this.filteredTickers[index];

        if (!ticker) return;

        const isStock = ticker.asset_class === 'stock';

        // Update header
        this.modalTicker.textContent = ticker.ticker;
        this.modalClass.textContent = Formatters.assetClassName(ticker.asset_class);

        // Update quick stats
        this.quickStats.innerHTML = isStock ? `
            <div class="quick-stat">
                <div class="quick-stat-label">Total Score</div>
                <div class="quick-stat-value">${ticker.scores?.total || '—'} / ${ticker.scores?.total_max || 100}</div>
            </div>
            <div class="quick-stat">
                <div class="quick-stat-label">Fundamentals</div>
                <div class="quick-stat-value">${ticker.scores?.fundamentals || 0} / ${ticker.scores?.fundamentals_max || 40}</div>
            </div>
            <div class="quick-stat">
                <div class="quick-stat-label">Technicals</div>
                <div class="quick-stat-value">${ticker.scores?.technicals || 0} / ${ticker.scores?.technicals_max || 25}</div>
            </div>
            <div class="quick-stat">
                <div class="quick-stat-label">Last Updated</div>
                <div class="quick-stat-value">${Formatters.formatDate(ticker.last_updated)}</div>
            </div>
        ` : `
            <div class="quick-stat">
                <div class="quick-stat-label">Asset Class</div>
                <div class="quick-stat-value">${Formatters.assetClassName(ticker.asset_class)}</div>
            </div>
            <div class="quick-stat">
                <div class="quick-stat-label">Metrics</div>
                <div class="quick-stat-value">${Object.keys(ticker.metrics || {}).length}</div>
            </div>
            <div class="quick-stat">
                <div class="quick-stat-label">Last Updated</div>
                <div class="quick-stat-value">${Formatters.formatDate(ticker.last_updated)}</div>
            </div>
        `;

        // Render markdown content
        let content = `# ${ticker.ticker}\n\n`;

        if (ticker.theme) {
            content += `**Theme:** ${ticker.theme}\n\n`;
        }
        if (ticker.core_idea) {
            content += `## Core Idea\n${ticker.core_idea}\n\n`;
        }
        if (ticker.pillars && ticker.pillars.length) {
            content += `## Thesis Pillars\n`;
            ticker.pillars.forEach((p, i) => {
                content += `${i + 1}. ${p}\n`;
            });
            content += '\n';
        }
        if (ticker.metrics && Object.keys(ticker.metrics).length) {
            content += `## Key Metrics\n`;
            Object.entries(ticker.metrics).forEach(([k, v]) => {
                content += `- **${k}:** ${v}\n`;
            });
            content += '\n';
        }
        if (ticker.catalysts && ticker.catalysts.length) {
            content += `## Catalysts\n`;
            ticker.catalysts.forEach(c => {
                content += `- **${c.event}** (${c.date})\n`;
            });
            content += '\n';
        }
        if (ticker.risks && ticker.risks.length) {
            content += `## Risk Factors\n`;
            ticker.risks.forEach(r => {
                content += `- ${r}\n`;
            });
        }

        this.markdownContent.innerHTML = marked.parse(content);

        // Update navigation buttons
        this.modalPrev.disabled = index === 0;
        this.modalNext.disabled = index === this.filteredTickers.length - 1;

        // Open modal
        this.modal.classList.add('active');
    }

    /**
     * Close modal
     */
    closeModal() {
        this.modal.classList.remove('active');
        this.currentModalIndex = -1;
    }

    /**
     * Navigate to previous modal
     */
    previousModal() {
        if (this.currentModalIndex > 0) {
            this.openModal(this.currentModalIndex - 1);
        }
    }

    /**
     * Navigate to next modal
     */
    nextModal() {
        if (this.currentModalIndex < this.filteredTickers.length - 1) {
            this.openModal(this.currentModalIndex + 1);
        }
    }
}

/**
 * Initialize app when DOM is ready
 */
document.addEventListener('DOMContentLoaded', () => {
    const app = new ThesisTrackerApp();
});
