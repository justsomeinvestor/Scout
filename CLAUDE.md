# System Context - Scout Market Intelligence

**Current System:** Scout (production ready as of 2025-11-11)
**Status:** ✅ Data collection working | ⏸️ AI processing (manual)
**Entry Point:** `python scout/scout.py` (single command)

## Quick Grounding

Scout is a market intelligence system that collects data from 4 sources:
- X/Twitter posts (local Selenium scraper - 12 min)
- YouTube videos (API server at 192.168.10.56:3000)
- RSS news feeds (API server)
- Market data (API server - ETFs, max pain, options)

**Workflow:**
1. Run `python scout/scout.py` → collects all data (~13 min)
2. Manual AI processing → analyze collected data
3. Generate `scout/dash.md` → market intelligence output
4. View `scout/dash.html` → interactive dashboard

**Recent Changes (Session 6 - 2025-11-11):**
- Fixed X scraper timeout with real-time output streaming
- Cleaned root directory per project rules
- All documentation in `Toolbox/CHANGELOGS/SESSION_6_*.md`

**Key Docs:**
- Complete workflow: `Toolbox/MasterFlow/00_SCOUT_WORKFLOW.md`
- Session history: `Toolbox/CHANGELOGS/`
- Quick summary: `Toolbox/SESSION_6_SUMMARY.md`

**Next Steps:**
- Option 1: Complete AI processing workflow (Step 3)
- Option 2: Build Trading Command Center (bigger project, see `Toolbox/Docs/PROJECT_PLAN.md`)

---

# Project Rules

## File Organization (CRITICAL - Keep Root Clean)

**Root directory should ONLY contain:**
- `.env`, `.gitignore` (environment/git config)
- `README.md`, `CLAUDE.md` (project entry points ONLY)
- `requirements.txt` (package manifest ONLY)
- Core directories: `scout/`, `Scraper/`, `Research/`, `scripts/`, `Toolbox/`

**❌ NO scripts in root**
**❌ NO config.py in root** → Use `scout/config.py` or `Toolbox/config.py`
**❌ NO documentation in root** → Use `Toolbox/`

**Everything else MUST go in Toolbox/:**
- Documentation → `Toolbox/` (e.g., `Toolbox/PROJECT_STRUCTURE.md`)
- Changelogs → `Toolbox/CHANGELOGS/` with date (e.g., `CHANGELOG_YYYY-MM-DD_<context>.md`)
- Tech support docs → `Toolbox/` or `Toolbox/MasterFlow/`
- Planning docs → `Toolbox/` or `Toolbox/MasterFlow/`
- Analysis docs → `Toolbox/`
- Audit files → `Toolbox/` (e.g., `Toolbox/DATA_SOURCES_AUDIT.md`)
- Session handoffs → `Toolbox/CHANGELOGS/`
- Summaries → `Toolbox/CHANGELOGS/`

**Scripts organization:**
- Core system scripts → `scout/` (e.g., `scout/scout.py`)
- Data collectors → `Scraper/` (e.g., `Scraper/x_scraper.py`)
- API clients → `scripts/trading/` (e.g., `scripts/trading/api_client.py`)
- Utility scripts → `Toolbox/scripts/` (e.g., `Toolbox/scripts/cleanup/`)

## Development Rules
- Before executing any large plans that are potentially system breaking, make a project plan and save to `Toolbox/` so if there is a crash or context window reset, we can easily pick up where we left off
- When modifying critical documents, make sure to make a backup first
- Never commit to github without passing testing phases


## Repository Rules
- Never commit secrets or tokens. If found, stop and propose a remediation plan.
- Prefer additive changes over destructive refactors unless asked.

## Planning Protocol (follow every task)
1. **Plan**: Outline steps, files to touch, and tests you’ll add/adjust.
2. **Implement**: Make small, reviewable changes. Explain each change briefly.
3. **Verify**: Run or simulate tests and lint; report results concisely.
4. **Review**: Summarize risks, trade-offs, and follow-ups as TODOs.

## Guardrails
- Never fabricate test results or execution logs.
- Never use mock or fake data unless explicitly approved. Ask first.
- If a requirement conflicts with repository rules, call it out and propose a safer path.


