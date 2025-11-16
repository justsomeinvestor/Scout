# System Context - Scout Market Intelligence

**Status:** ✅ Production | Data collection automated | AI processing manual
**Last Updated:** 2025-11-14 (workflow docs reorganized)

## Quick Grounding

Scout = Market intelligence system collecting from 4 sources (X/Twitter, YouTube, RSS, Market data)

**Standard workflow:**
1. User runs `python scout/scout.py` (~13 min) → data collected & sent to API server
2. **YOU START HERE** → Process with AI (~40-55 min)
3. Output: Updated `scout/dash.md` with market signal score

**When user says ANY of these phrases:**
- "run prep"
- "run the workflow"
- "let's run the workflow"
- "start the workflow"
- "I just ran the scraper"
- "scraper is done"
- "let's work through Scout workflow"

**Your immediate action (NO QUESTIONS):**
1. ✅ Fetch data from API server (192.168.10.56:3000)
2. ✅ Start Phase 1 immediately (create prep file, run Steps 3A-3F)
3. ✅ Complete Phase 2 (update dashboard)
4. ❌ Do NOT ask "did you run the scraper?"
5. ❌ Do NOT check for local files
6. ❌ Do NOT run `python scout/scout.py` yourself

**If user says "create a changelog":**
→ `Toolbox/CHANGELOGS/SESSION_X_YYYY-MM-DD.md`
→ Include: what changed, why, files touched, next steps

## Multi-Claude Coordination (CRITICAL)

**Architecture:** Windows Claude (frontend) ↔️ Server Claude (backend) via REST API

**Coordination API:** http://192.168.10.56:3000/api/coord
**Documentation:** `Toolbox/Claude-Colab.md`

**Quick Commands:**
```bash
# Check pending tasks
npx tsx src/coordinationDemo.ts pending

# See all messages
npx tsx src/coordinationDemo.ts all

# Send task to other Claude
npx tsx src/coordinationDemo.ts send "task description" "context" <to_claude> <from_claude>

# Get stats
npx tsx src/coordinationDemo.ts stats
```

**Message Types:**
- 💬 **chat** - Direct communication between Claude instances (read & acknowledge)
- 📋 **task** - Work requests requiring execution (claim → execute → complete)

**From TypeScript/Node:**
```typescript
import { sendTask, getPendingTasks, completeTask, claimTask } from './coordinationClient';

// Send task (Windows Claude)
await sendTask('Run scraper for SPY', 'Need latest data', 'server_backend', 'windows_frontend', 'task');

// Send chat message
await sendTask('Status update: workflow complete', 'Dashboard updated', 'server_backend', 'windows_frontend', 'chat');

// Process tasks (Server Claude)
const tasks = await getPendingTasks('server_backend');
await claimTask(task.id);
// ... do work ...
await completeTask(task.id, 'Result here');
```

**Environment Setup:**
- Windows Claude: `CLAUDE_ID=windows_frontend`
- Server Claude: `CLAUDE_ID=server_backend`, `COORDINATION_API_URL=http://192.168.10.56:3000/api/coord`

## Key Files

**Workflows:**
- `Toolbox/MasterFlow/SCOUT_AI_WORKFLOW.md` - AI processing (main workflow)
- `Toolbox/MasterFlow/COMMAND_REFERENCE.md` - Quick commands

**Data locations:**
- Output: `scout/dash.md`, `scout/dash.html`
- Checkpoints: `Research/.cache/YYYY-MM-DD_dash-prep.md`
- **Data sources:** See `Toolbox/MasterFlow/SCOUT_AI_WORKFLOW.md` for where to fetch each data type

**Session history:** `Toolbox/CHANGELOGS/`

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
1. **Plan**: Outline steps, files to touch, and tests you'll add/adjust.
2. **Implement**: Make small, reviewable changes. Explain each change briefly.
3. **Verify**: Run or simulate tests and lint; report results concisely.
4. **Review**: Summarize risks, trade-offs, and follow-ups as TODOs.

## Autonomous Operation

**Task Tracking:**
- Use TodoWrite for multi-step tasks (create at start, update in real-time)
- Document work in `Toolbox/CHANGELOGS/SESSION_X_YYYY-MM-DD.md` for:
  - New features, architectural changes, bug fixes
  - Multi-session work (so other Claude instances can continue)

**Decision Making:**
- Be decisive: If user says "build X", start building with todos
- Document assumptions in todos/changelogs instead of asking
- Only ask when genuinely unclear or risky

**Progress Communication:**
- Keep todos current
- Proactively report: "✅ Done: X, Y, Z. Next: A"

**Multi-Claude Handoffs:**
- Update changelog with: status, next steps, blockers, files modified
- Commit when logical stopping point reached

## Guardrails
- Never fabricate test results or execution logs.
- Never use mock or fake data unless explicitly approved. Ask first.
- If a requirement conflicts with repository rules, call it out and propose a safer path.


