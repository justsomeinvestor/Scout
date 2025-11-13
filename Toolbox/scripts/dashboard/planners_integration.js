/**
 * PLANNERS TAB INTEGRATION SCRIPT
 *
 * This script integrates the weekly and daily planner system into the research-dashboard
 * Reads from Research/AI/ folder and displays plans in dashboard
 */

class PlannerIntegration {
    constructor() {
        this.basePath = '/Research/AI';
        this.weeklyMetricsFile = this.getCurrentWeekMetricsFile();
        this.dailyMetricsFile = this.getTodayMetricsFile();
    }

    /**
     * Get current week's metrics file path
     * Format: YYYY-WXX_WEEKLY_METRICS.md
     */
    getCurrentWeekMetricsFile() {
        const now = new Date();
        const weekNum = this.getWeekNumber(now);
        const year = now.getFullYear();

        return `${year}-W${String(weekNum).padStart(2, '0')}_WEEKLY_METRICS.md`;
    }

    /**
     * Get today's metrics file path
     * Format: YYYY-MM-DD_DAILY_METRICS.md
     */
    getTodayMetricsFile() {
        const now = new Date();
        const year = now.getFullYear();
        const month = String(now.getMonth() + 1).padStart(2, '0');
        const day = String(now.getDate()).padStart(2, '0');

        return `${year}-${month}-${day}_DAILY_METRICS.md`;
    }

    /**
     * ISO 8601 week number
     */
    getWeekNumber(date) {
        const d = new Date(Date.UTC(date.getFullYear(), date.getMonth(), date.getDate()));
        const dayNum = d.getUTCDay() || 7;
        d.setUTCDate(d.getUTCDate() + 4 - dayNum);
        const yearStart = new Date(Date.UTC(d.getUTCFullYear(), 0, 1));
        return Math.ceil((((d - yearStart) / 86400000) + 1) / 7);
    }

    /**
     * Create Planners tab HTML structure
     */
    createPlannersTab() {
        const plannersHTML = `
            <div class="planners-container">
                <div class="planners-header">
                    <h2>📊 Planners - Weekly Strategy & Daily Execution</h2>
                </div>

                <div class="planners-content">
                    <!-- WEEKLY PLANNER SECTION -->
                    <div class="planner-section weekly-section">
                        <div class="section-header">
                            <h3>📅 Weekly Planner</h3>
                            <span class="section-meta">Updated: Sunday morning</span>
                        </div>

                        <div class="weekly-planner-content">
                            <div class="weekly-card">
                                <h4>📈 Signal Forecast</h4>
                                <div id="weekly-signal" class="metric-display">
                                    Loading weekly signal...
                                </div>
                            </div>

                            <div class="weekly-card">
                                <h4>🎯 Weekly Trigger Stack (Top 3 Ideas)</h4>
                                <div id="weekly-triggers" class="trigger-stack">
                                    Loading trigger stack...
                                </div>
                            </div>

                            <div class="weekly-card">
                                <h4>📋 Economic Calendar</h4>
                                <div id="weekly-calendar" class="economic-calendar">
                                    Loading calendar...
                                </div>
                            </div>

                            <div class="weekly-card">
                                <h4>🗓️ Daily Positioning Guide</h4>
                                <div id="weekly-positioning" class="positioning-guide">
                                    Loading positioning...
                                </div>
                            </div>

                            <div class="weekly-card">
                                <h4>⚠️ Risk Controls</h4>
                                <div id="weekly-risk" class="risk-controls">
                                    Loading risk controls...
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="divider"></div>

                    <!-- DAILY PLANNER SECTION -->
                    <div class="planner-section daily-section">
                        <div class="section-header">
                            <h3>🚀 Daily Planner</h3>
                            <span class="section-meta">Today's Execution Plan</span>
                        </div>

                        <div class="daily-planner-content">
                            <div class="daily-card">
                                <h4>🎯 Today's 3 Priorities</h4>
                                <div id="daily-priorities" class="priorities-list">
                                    Loading priorities...
                                </div>
                            </div>

                            <div class="daily-card">
                                <h4>📍 Key Levels</h4>
                                <div id="daily-levels" class="key-levels-display">
                                    Loading key levels...
                                </div>
                            </div>

                            <div class="daily-card">
                                <h4>💰 Risk Management</h4>
                                <div id="daily-risk" class="daily-risk-display">
                                    Loading risk limits...
                                </div>
                            </div>

                            <div class="daily-card">
                                <h4>✅ Pre-Market Checklist</h4>
                                <div id="daily-checklist" class="checklist-display">
                                    Loading checklist...
                                </div>
                            </div>

                            <div class="daily-card">
                                <h4>📊 Trade Execution Log</h4>
                                <div id="daily-trades" class="trades-log">
                                    <p>No trades yet today</p>
                                </div>
                            </div>

                            <div class="daily-card">
                                <h4>🌙 EOD Summary & Next Day Prep</h4>
                                <div id="daily-eod" class="eod-summary">
                                    Loading EOD template...
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;

        return plannersHTML;
    }

    /**
     * Load and parse weekly metrics file
     */
    async loadWeeklyMetrics() {
        try {
            // Construct file path
            const filePath = `/Research/AI/${this.weeklyMetricsFile}`;

            // Fetch file content
            const response = await fetch(filePath);
            if (!response.ok) {
                throw new Error('Weekly metrics file not found');
            }

            const content = await response.text();
            return this.parseMetricsMarkdown(content);
        } catch (error) {
            console.warn('Could not load weekly metrics:', error);
            return this.getDefaultWeeklyMetrics();
        }
    }

    /**
     * Load and parse daily metrics file
     */
    async loadDailyMetrics() {
        try {
            const filePath = `/Research/AI/${this.dailyMetricsFile}`;

            const response = await fetch(filePath);
            if (!response.ok) {
                throw new Error('Daily metrics file not found');
            }

            const content = await response.text();
            return this.parseMetricsMarkdown(content);
        } catch (error) {
            console.warn('Could not load daily metrics:', error);
            return this.getDefaultDailyMetrics();
        }
    }

    /**
     * Parse markdown metrics file into structured data
     */
    parseMetricsMarkdown(content) {
        const sections = {};
        const lines = content.split('\n');
        let currentSection = null;
        let currentContent = [];

        for (const line of lines) {
            if (line.startsWith('##')) {
                if (currentSection) {
                    sections[currentSection] = currentContent.join('\n');
                }
                currentSection = line.replace(/^#+\s+/, '').trim();
                currentContent = [];
            } else if (currentSection) {
                currentContent.push(line);
            }
        }

        if (currentSection) {
            sections[currentSection] = currentContent.join('\n');
        }

        return sections;
    }

    /**
     * Get default weekly metrics if file not found
     */
    getDefaultWeeklyMetrics() {
        return {
            'Signal Forecast': 'No weekly metrics loaded. Run Sunday weekly planner.',
            'Trigger Stack': '1. Awaiting setup identification\n2. Awaiting setup identification\n3. Awaiting setup identification',
            'Economic Calendar': 'Check master-plan.md for this week\'s events',
            'Daily Positioning': 'Monday-Friday positioning guide not yet created',
            'Risk Controls': 'Daily loss limit: 2%\nWeekly loss limit: 3%\nMax portfolio heat: [See risk rules]',
        };
    }

    /**
     * Get default daily metrics if file not found
     */
    getDefaultDailyMetrics() {
        return {
            'Priorities': 'Today\'s daily planner not yet created. Create from weekly template.',
            'Levels': 'Key support/resistance levels not loaded',
            'Risk': 'Daily loss limit: 2%\nDaily heat limit: 4 concurrent trades',
            'Checklist': '☐ Review weekly plan\n☐ Check economic calendar\n☐ Set alerts at key levels\n☐ Pre-market bias confirmation',
            'Trades': 'No trades executed yet today',
            'EOD': 'Ready for EOD wrap at market close',
        };
    }

    /**
     * Render weekly planner data to HTML
     */
    async renderWeeklyPlanner() {
        const metrics = await this.loadWeeklyMetrics();

        // Update weekly signal
        const signalEl = document.getElementById('weekly-signal');
        if (signalEl) {
            signalEl.innerHTML = this.formatContent(metrics['Signal Forecast'] || 'Loading...');
        }

        // Update trigger stack
        const triggersEl = document.getElementById('weekly-triggers');
        if (triggersEl) {
            const triggers = (metrics['Trigger Stack'] || 'No triggers').split('\n');
            let html = '<ol class="trigger-list">';
            triggers.forEach((trigger, idx) => {
                if (trigger.trim()) {
                    html += `<li>${trigger.trim()}</li>`;
                }
            });
            html += '</ol>';
            triggersEl.innerHTML = html;
        }

        // Update economic calendar
        const calendarEl = document.getElementById('weekly-calendar');
        if (calendarEl) {
            calendarEl.innerHTML = this.formatContent(metrics['Economic Calendar'] || 'Check master plan');
        }

        // Update positioning guide
        const positioningEl = document.getElementById('weekly-positioning');
        if (positioningEl) {
            positioningEl.innerHTML = this.formatContent(metrics['Daily Positioning'] || 'Loading...');
        }

        // Update risk controls
        const riskEl = document.getElementById('weekly-risk');
        if (riskEl) {
            riskEl.innerHTML = this.formatContent(metrics['Risk Controls'] || 'See risk rules');
        }
    }

    /**
     * Render daily planner data to HTML
     */
    async renderDailyPlanner() {
        const metrics = await this.loadDailyMetrics();

        // Update daily priorities
        const prioritiesEl = document.getElementById('daily-priorities');
        if (prioritiesEl) {
            const priorities = (metrics['Priorities'] || 'Loading...').split('\n');
            let html = '<ol class="priorities-list">';
            priorities.forEach((priority, idx) => {
                if (priority.trim()) {
                    html += `<li>${priority.trim()}</li>`;
                }
            });
            html += '</ol>';
            prioritiesEl.innerHTML = html;
        }

        // Update key levels
        const levelsEl = document.getElementById('daily-levels');
        if (levelsEl) {
            levelsEl.innerHTML = this.formatContent(metrics['Levels'] || 'No levels set');
        }

        // Update risk management
        const riskEl = document.getElementById('daily-risk');
        if (riskEl) {
            riskEl.innerHTML = this.formatContent(metrics['Risk'] || 'See account limits');
        }

        // Update checklist
        const checklistEl = document.getElementById('daily-checklist');
        if (checklistEl) {
            const items = (metrics['Checklist'] || 'No checklist').split('\n');
            let html = '<ul class="checklist-items">';
            items.forEach((item) => {
                if (item.trim()) {
                    const checked = item.includes('☑') ? 'checked' : '';
                    html += `<li class="${checked}">${item.trim()}</li>`;
                }
            });
            html += '</ul>';
            checklistEl.innerHTML = html;
        }

        // Update trades log
        const tradesEl = document.getElementById('daily-trades');
        if (tradesEl) {
            tradesEl.innerHTML = `<p>${metrics['Trades'] || 'No trades yet'}</p>`;
        }

        // Update EOD section
        const eodEl = document.getElementById('daily-eod');
        if (eodEl) {
            eodEl.innerHTML = this.formatContent(metrics['EOD'] || 'EOD wrap ready');
        }
    }

    /**
     * Format markdown content to HTML
     */
    formatContent(content) {
        if (!content) return 'Loading...';

        return content
            .split('\n')
            .map(line => {
                if (line.match(/^\*\*/)) {
                    return `<strong>${line.replace(/\*\*/g, '')}</strong>`;
                }
                if (line.match(/^-/)) {
                    return `<li>${line.replace(/^-\s*/, '')}</li>`;
                }
                return `<p>${line}</p>`;
            })
            .join('');
    }

    /**
     * Initialize the Planners tab
     */
    async initialize() {
        // Create tab HTML
        const plannersHTML = this.createPlannersTab();

        // Add to dashboard
        const container = document.getElementById('planners-container');
        if (container) {
            container.innerHTML = plannersHTML;
        }

        // Render data
        await this.renderWeeklyPlanner();
        await this.renderDailyPlanner();

        // Set up auto-refresh (every 5 minutes)
        setInterval(() => {
            this.renderWeeklyPlanner();
            this.renderDailyPlanner();
        }, 5 * 60 * 1000);

        console.log('✓ Planners tab initialized and rendering');
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    const plannerIntegration = new PlannerIntegration();
    plannerIntegration.initialize();
});
