# Scout - Market Intelligence System

Automated market research dashboard with single-command execution.

## Quick Start

```bash
cd scout/
python scout.py
```

**Complete workflow runs in <60 minutes:**
- Cleanup (30 sec)
- Data collection (10-15 min)
- AI analysis (40 min)
- Dashboard generation

## Data Sources

**Included (Working):**
- ✅ X/Twitter - Social sentiment from lists (Technicals, Crypto, Macro)
- ✅ YouTube - Investment channel analysis
- ✅ RSS - News feeds (MarketWatch, CNBC, Federal Reserve)
- ✅ API Server - Market data (192.168.10.56:3000)

**Optional Dependencies:**
- Ollama (for YouTube transcript summarization)
- API Server (graceful degradation if offline)
- Chrome browser with profile (for X scraper)

## Output Files

- `dash.md` - Structured market intelligence (markdown)
- `dash.html` - Interactive web dashboard
- `Research/.cache/` - Temporary processing files

## Project Structure

```
scout/
├── scout.py              # Master orchestrator
├── config.py             # System configuration
├── collectors/
│   ├── core.py           # Parallel data collection
│   └── __init__.py       #  Collector exports
├── dash.md               # Market intelligence output
├── dash.html             # Web dashboard
└── README.md             # This file
```

## Requirements

- Python 3.8+
- Dependencies: See `../requirements.txt`
- Chrome browser (for X scraper)
- Optional: Ollama (local LLM for summaries)

## Complete Documentation

See `../Toolbox/MasterFlow/` for:
- Complete workflow guide
- Step-by-step documentation
- Troubleshooting
- Crash recovery

## Philosophy

**If it doesn't work immediately → it's disabled and documented.**

Scout focuses on reliable, working data sources only. Failed collectors gracefully degrade without blocking the workflow.

## Legacy System

This is a consolidation of the previous "MasterFlow" system. All legacy code is archived in `../Toolbox/ARCHIVES/legacy_2025-11-11/`.

---

**Status:** Active
**Version:** 1.0 (Consolidated from MasterFlow)
**Last Updated:** 2025-11-11
