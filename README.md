# Scout - Market Intelligence System

**One Command. One Workflow. One Dashboard.**

Automated market research platform that collects multi-source intelligence and generates an interactive dashboard for daily trading decisions.

## Quick Start

```bash
python scout/scout.py
```

**Data collection workflow (~5-10 minutes):**
- Cleanup stale cache (30 sec)
- Collect X/Twitter data (3-5 min)
- Collect API data (instant) - YouTube, RSS, Market
- Manual AI processing step (documented separately)

**System recently rebuilt (2025-11-11):** 95% code reduction, single entry point, all data sources verified working.

## What Scout Does

**Scout runs RECON** (reconnaissance) to gather market intelligence from:
- ✅ X/Twitter - Social sentiment from curated lists
- ✅ YouTube - Investment channel analysis (via API server)
- ✅ RSS - News feeds from MarketWatch, CNBC, Federal Reserve (via API server)
- ✅ Market Data - Real-time market data from API server (192.168.10.56:3000)

**Output:**
- `scout/dash.md` - Structured market intelligence
- `scout/dash.html` - Interactive web dashboard

## For AI Assistants (Claude Code)

**System Overview:**
- Start here: **[CLAUDE.md](./CLAUDE.md)** — Project rules and protocols
- Scout system: **[scout/README.md](./scout/README.md)** — Quick start guide
- Complete workflow: **[Toolbox/MasterFlow/00_SCOUT_WORKFLOW.md](./Toolbox/MasterFlow/00_SCOUT_WORKFLOW.md)** — Full documentation
- Session history: **[Toolbox/CHANGELOGS/](./Toolbox/CHANGELOGS/)** — Rebuild documentation

## Project Structure

| Path | Purpose |
|------|---------|
| **`scout/`** | **Core system - single entry point** |
| `scout/scout.py` | Master orchestrator - runs complete workflow |
| `scout/dash.md` | Generated market intelligence (markdown) |
| `scout/dash.html` | Interactive web dashboard |
| **`Scraper/`** | Original data collectors |
| `Scraper/x_scraper.py` | X/Twitter scraper (local) |
| `Scraper/youtube_scraper.py` | YouTube API integration |
| `Scraper/rss_scraper.py` | RSS feed collector |
| **`Research/`** | Collected data storage |
| `Research/X/` | X/Twitter posts by list |
| `Research/.cache/` | Temporary processing files |
| **`Toolbox/`** | Documentation and utilities |
| `Toolbox/MasterFlow/` | Complete workflow documentation |
| `Toolbox/BACKUPS/` | Safety backups |
| `Toolbox/ARCHIVES/` | Historical archives |

**Recent changes (2025-11-11):**
- System rebuilt: "Wingman" → "Scout" with 95% code reduction
- Single entry point: `python scout/scout.py`
- Legacy code archived: `Toolbox/ARCHIVES/legacy_2025-11-11/`
- Complete rollback capability maintained
- See: [SESSION_5_COMPLETE_2025-11-11.md](./Toolbox/CHANGELOGS/SESSION_5_COMPLETE_2025-11-11.md)

## Usage

### Run Data Collection

```bash
python scout/scout.py
```

This executes:
1. **Cleanup** - Remove stale cache files (~30 sec)
2. **Collection** - Gather data from all sources (~5-10 min)
   - X/Twitter via local scraper (3-5 min)
   - YouTube/RSS/Market via API server (instant)
3. **Verification** - Check collected data
4. **Pause for AI Processing** - Manual step (see workflow docs)

**Note:** AI processing (Step 3) is currently a manual step. See [00_SCOUT_WORKFLOW.md](./Toolbox/MasterFlow/00_SCOUT_WORKFLOW.md) for details.

### View Dashboard

```bash
# Open dash.html directly in browser
open scout/dash.html  # macOS
start scout/dash.html  # Windows
```

Or serve locally:
```bash
cd scout/
python -m http.server 9000
# Open http://localhost:9000/dash.html
```

### Manual Steps (If Needed)

**X Scraper Only:**
```bash
python Scraper/x_scraper.py
```

**Check API Server:**
```bash
curl http://192.168.10.56:3000/api/summary
```

**Cleanup Only:**
```bash
python Toolbox/scripts/cleanup/wingman_cleanup.py
```

## Daily Use Workflow

**Morning Data Collection (~10 min):**
```bash
python scout/scout.py
# Collects: X/Twitter, YouTube, RSS, Market data
# Output: Research/X/ and API data
# Next: Manual AI processing to generate dash.md
```

**AI Processing (Manual Step):**
- Analyze collected data from Research/X/
- Review API data (YouTube/RSS/Market)
- Generate insights and signal calculations
- Update scout/dash.md with analysis
- See: [05_STEP_3_PROCESS_DATA.md](./Toolbox/MasterFlow/05_STEP_3_PROCESS_DATA.md)

**View Dashboard:**
```bash
start scout/dash.html  # Windows
open scout/dash.html   # macOS
```

## Backups & Archives

**System backups:**
- Config backups: `Toolbox/BACKUPS/` (config files with timestamps)
- Legacy system: `Toolbox/ARCHIVES/legacy_2025-11-11/` (complete old system preserved)
- Complete rollback capability maintained

**Scout outputs:**
- Live files: `scout/dash.md` and `scout/dash.html`
- No automatic backups (generate fresh daily)

## Publishing Checklist

1. Run `python scout/scout.py` to collect fresh data
2. Complete AI processing (Step 3) to generate `scout/dash.md`
3. Verify `scout/dash.html` renders correctly in browser
4. Review `git status` to see what changed
5. Stage modified files: `git add scout/dash.md scout/dash.html`
6. Commit with message like `docs: update Scout dashboard YYYY-MM-DD`
7. Push to GitHub

**Note:** Scout system is documented in `Toolbox/MasterFlow/00_SCOUT_WORKFLOW.md`
