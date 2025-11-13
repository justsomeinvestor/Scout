# Workflow Metadata Guide

**Purpose:** Centralized reference for workflow tracking metadata system.

**Location:** `Journal/account_state.json` (single source of truth)

---

## Metadata Fields

All workflow metadata stored in `account_state.json`:

| Field | Type | Example | Purpose |
|-------|------|---------|---------|
| `last_workflow_run` | Date (YYYY-MM-DD) | `2025-10-31` | Date of last workflow completion |
| `last_workflow_type` | String | `recon` | Type of workflow that ran |
| `last_workflow_status` | String | `success` | Completion status |
| `last_workflow_timestamp` | ISO 8601 | `2025-10-31T06:05:23Z` | Exact completion time |
| `data_freshness` | String | `FRESH` | Freshness indicator |

---

## Workflow Types

```
"recon"        - Data collection (run_all_scrapers.py)
"prep"         - AI research analysis (WINGMAN PREP)
"dash"         - Dashboard updates (WINGMAN DASH)
"cleanup"      - Data cleanup (wingman_cleanup.py)
```

---

## Status Values

```
"success"           - All sub-tasks completed successfully
"partial_success"   - Some tasks failed, but overall completed
"failed"            - Workflow failed or was interrupted
```

---

## Freshness Levels

```
"FRESH"   - Completed today (same day as now)
"PARTIAL" - Completed but with partial failures
"STALE"   - 2+ days old, needs rerun
```

---

## Updating Metadata

### Automatic (Recommended)

When a workflow completes successfully, call:

```python
from scripts.utilities.update_workflow_metadata import update_workflow_run

update_workflow_run("recon", "success")
```

This will:
1. Set `last_workflow_run` to today's date
2. Set `last_workflow_type` to the workflow type
3. Set `last_workflow_status` to the status
4. Set `last_workflow_timestamp` to ISO timestamp
5. Set `data_freshness` based on status

### Manual (CLI)

```bash
python scripts/utilities/update_workflow_metadata.py recon success
```

---

## Checking Metadata

### In Code

```python
from scripts.utilities.update_workflow_metadata import get_workflow_freshness

info = get_workflow_freshness()
print(info['last_run_date'])      # "2025-10-31"
print(info['last_run_type'])      # "recon"
print(info['freshness_level'])    # "FRESH (<24hrs)"
```

### In Wingman

When Wingman loads, it checks:
1. `account_state.json` for metadata
2. If missing, falls back to `Research/YYYY-MM-DD_*_Category_Overview.md` file timestamps
3. Reports freshness in instrument check

Example output:
```
🔍 Last RECON: 2025-10-31 (FRESH - <24hrs)
🗺️ Workflow: recon (success)
📊 Data: FRESH - All systems current
```

---

## Freshness Determination

Wingman applies this logic:

```
if last_workflow_run == today:
    freshness = "FRESH (<24hrs)"
elif last_workflow_run == yesterday:
    freshness = "RECENT (acceptable)"
elif last_workflow_run is 2+ days ago:
    freshness = "STALE (recommend rerun)"
else:
    freshness = "UNKNOWN"
```

---

## Integration Points

**run_all_scrapers.py (RECON)**
- Calls `update_workflow_run("recon", status)` after completion
- Updates metadata at end of main loop

**WINGMAN PREP** (When implemented)
- Should call `update_workflow_run("prep", "success")` after analysis
- Timestamp workflow completion for auditing

**WINGMAN DASH** (When implemented)
- Should call `update_workflow_run("dash", "success")` after dashboard sync
- Track dashboard update history

**wingman_cleanup.py** (When called)
- Could call `update_workflow_run("cleanup", "success")` after cleanup
- Track data maintenance activities

---

## Troubleshooting

### Metadata Missing

**Problem:** `account_state.json` has no workflow metadata

**Solution:**
1. Manually run: `python scripts/utilities/update_workflow_metadata.py recon success`
2. Or run a RECON (which now auto-updates)
3. Or check file timestamps in `Research/` directory

### Metadata Stale

**Problem:** `last_workflow_run` shows old date

**Solution:**
1. Run RECON: `python scripts/automation/run_all_scrapers.py`
2. RECON will auto-update metadata
3. Verify: `python scripts/utilities/update_workflow_metadata.py` and check account_state.json

### Data Freshness Flag Wrong

**Problem:** `data_freshness` says "STALE" but data is fresh

**Causes:**
- Metadata wasn't updated (run RECON)
- File timestamps in Research/ directory
- System clock issue

**Solution:**
1. Check `last_workflow_timestamp` - is it recent?
2. Check Research/ files - do they exist?
3. Run RECON to force metadata update

---

## Best Practices

1. **Always update metadata after workflows**
   - Prevents data freshness confusion
   - Enables Wingman to make informed decisions

2. **Use the helper function (not manual JSON edits)**
   - Ensures consistent formatting
   - Prevents typos in field names
   - Atomic updates (all fields updated together)

3. **Check metadata regularly**
   - Before starting trading session: "Check data freshness"
   - Monitor `data_freshness` field in instrument check
   - Alert if STALE

4. **Document workflow completion**
   - Every successful workflow should update metadata
   - Provides audit trail of system activity
   - Helps debug if data seems wrong

---

## Examples

### Example 1: After RECON Completes

```json
{
  "last_workflow_run": "2025-10-31",
  "last_workflow_type": "recon",
  "last_workflow_status": "success",
  "last_workflow_timestamp": "2025-10-31T06:05:23Z",
  "data_freshness": "FRESH"
}
```

Wingman will report: ✅ FRESH (<24hrs) - All data current

---

### Example 2: After RECON Fails Partially

```json
{
  "last_workflow_run": "2025-10-31",
  "last_workflow_type": "recon",
  "last_workflow_status": "partial_success",
  "last_workflow_timestamp": "2025-10-31T08:15:47Z",
  "data_freshness": "PARTIAL"
}
```

Wingman will report: ⚠️ PARTIAL - Some data updated, some failed

---

### Example 3: Metadata 3 Days Old

```json
{
  "last_workflow_run": "2025-10-28",
  "last_workflow_type": "recon",
  "last_workflow_status": "success",
  "last_workflow_timestamp": "2025-10-28T05:30:12Z",
  "data_freshness": "STALE"
}
```

Wingman will report: ⚠️ STALE (3 days) - Recommend running RECON

---

## Future Enhancements

1. **Per-workflow freshness**
   - Track RECON, PREP, DASH separately
   - Show which data source is stale

2. **Automation**
   - Auto-run RECON if data >24hrs old
   - Auto-generate alerts if stale

3. **Metrics**
   - Track workflow success rate
   - Monitor execution times
   - Alert on failures

4. **Integration**
   - Connect to Slack/email alerts
   - Dashboard widget showing freshness
   - Trading session pre-checks

---

**Last Updated:** 2025-10-31
**Author:** Wingman System
**Status:** ACTIVE
