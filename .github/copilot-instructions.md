# AI Agent Instructions for Investing Research Dashboard

This guide helps AI agents understand key patterns and workflows in this investment research automation codebase.

## Project Architecture

### Core Components
- **Source of Truth:** `master-plan/master-plan.md` (YAML + Markdown)
  - Drives all dashboard panels and research views
  - Front matter contains critical metadata and settings
- **Dashboard:** `master-plan/research-dashboard.html`
  - Self-contained HTML/JS bundle
  - Updates by refreshing after `master-plan.md` changes
- **Automation:** `scripts/`, `Scraper/`
  - Python scripts for data ingestion and updates
  - Selenium-based scrapers with optimization patterns

### Key Data Flows
1. Scrapers collect data → JSON files
2. Automation scripts transform → YAML frontmatter
3. Dashboard reads YAML → Renders HTML/JS visualization

## Critical Workflows

### Daily Research Cycle
1. Morning (30-45min):
   ```bash
   python scripts/automation/run_workflow.py YYYY-MM-DD
   # Updates master-plan.md with fresh research
   ```
2. Intraday (2-3min):
   ```bash
   python scripts/automation/run_intraday_update.py YYYY-MM-DD
   # Quick sentiment refresh
   ```
3. EOD (10min):
   - Log trades in `Journal/`
   - Archive day's plan to `master-plan/archive/YYYY-MM/`
   - Document lessons in `Toolbox/`

### Safety & Backup Patterns
- ALWAYS create `.backup` files before modifying critical docs
- Historical snapshots go in date-based archive folders
- Verify matching dates in `.md` and `.html` files before commits

## Project-Specific Conventions

### Scraper Optimizations
Refer to `Scraper/OPTIMIZATION_NOTES.md` for full details:
- Smart data loading with archived JSON files
- Intelligent timestamp-based cutoffs
- Early exit on duplicate detection
- Time-based safety exits

### Documentation Standards
- All AI-generated docs go in `/Toolbox/` (Markdown preferred)
- Keep live files light, archive historical data
- Reference parent docs when creating new guides

## Integration Points
- Local preview: `python -m http.server 9000`
- Dashboard URL: `http://localhost:9000/master-plan/research-dashboard.html`
- Chrome/Selenium for scraping Twitter, RSS, YouTube
- JSON/YAML for data exchange between components

When making changes:
1. Read existing patterns in similar files
2. Create backups of critical files
3. Test dashboard renders after updates
4. Archive old versions appropriately