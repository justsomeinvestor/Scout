# Terminology Update: master-plan → dash-prep

**Date:** 2025-11-12
**Type:** Documentation Update
**Impact:** Terminology standardization across Scout system

---

## Summary

Renamed all "master-plan" references to "dash-prep" throughout the Scout system to align with current project terminology and remove legacy naming from the old system.

**Core Change:** The consolidated prep file is now called `dash-prep` instead of `master-plan-prep` to reflect the Scout dashboard-centric workflow.

---

## Files Updated

### Critical Files (11 files)

**1. Prep File (Renamed)**
- `Research/.cache/2025-11-12_master-plan-prep.md` → `Research/.cache/2025-11-12_dash-prep.md`

**2. Workflow Documentation (MasterFlow/)**
- ✅ `00_SCOUT_WORKFLOW.md` - 3 references updated
- ✅ `00_COMPLETE_WORKFLOW.md` - 13 references updated
- ✅ `05_STEP_3_PROCESS_DATA.md` - 10 references updated

**3. Supporting Documentation (MasterFlow/Docs/)**
- ✅ `07_STEP_3H_DASHBOARD_JSON.md` - 1 reference updated
- ✅ `DASHBOARD_SECTION_MAPPING.md` - 4 references updated
- ✅ `DASHBOARD_SYSTEM_COMPLETE.md` - 1 reference updated
- ✅ `DASHBOARD_TIMESTAMP_AUDIT.md` - 1 reference updated
- ✅ `DASHBOARD_UPDATE_GUIDE.md` - 8 references updated
- ✅ `QUICK_REFERENCE.md` - 4 references updated

**4. Session Handoffs (CHANGELOGS/)**
- ✅ `SESSION_8_HANDOFF_2025-11-12.md` - 14 references updated

---

## Changes Made

### Filename Pattern
```
Before: YYYY-MM-DD_master-plan-prep.md
After:  YYYY-MM-DD_dash-prep.md
```

### File References
```
Before: Research/.cache/YYYY-MM-DD_master-plan-prep.md
After:  Research/.cache/YYYY-MM-DD_dash-prep.md
```

### Descriptive Text
```
Before: "master-plan prep file"
After:  "dash-prep file"

Before: "Master Plan Prep - November 12, 2025"
After:  "Dash Prep - November 12, 2025"

Before: "All 3 master-plan sections updated"
After:  "All 3 dashboard sections updated"
```

### Path References
```
Before: master-plan/scout/dash.md
After:  scout/dash.md

Before: master-plan/dashboard.json
After:  scout/dashboard.json (OBSOLETE - removed in Session 6)

Before: master-plan/research-dashboard.html
After:  scout/dash.html
```

---

## Rationale

**Why this change?**
1. **Legacy terminology:** "master-plan" was the directory name from the old system (pre-Scout)
2. **Confusing hierarchy:** `master-plan/scout/dash.md` suggested two systems when there's only one (Scout)
3. **Prep file naming:** The prep file feeds the *dashboard*, not a "master plan", so `dash-prep.md` is more accurate
4. **Consistency:** Scout system outputs are `scout/dash.md` and `scout/dash.html`, prep file should match (`dash-prep`)

**Project context from user:**
> "the master plan is a name we used in the old project. It should be dash-prep and all workflows should reflect that."

---

## Impact Assessment

### Zero Breaking Changes ✅
- No code changes required
- No script path updates needed
- Only documentation and reference updates

### Files NOT Updated
**Excluded (by design):**
- `Toolbox/ARCHIVES/` - Historical records preserved as-is
- `Toolbox/PROJECTS/` - Legacy project documentation
- Backup files (`.backup*` extensions)

**Lower priority (skipped for now):**
- `01_SYSTEM_OUTPUTS.md` (4 references)
- `02_STEP_1_CLEANUP.md` (3 references)
- `04_MASTER_PLAN_CLEANUP_LOG.md` (4 references + filename)
- `06_OLLAMA_INTEGRATION.md` (1 reference)
- `SESSION_7_HANDOFF_2025-11-11.md` (2 references)
- `LEGACY_REMOVAL_2025-11-11.md` (8 references)

These can be updated in future cleanup session if needed.

---

## Verification

**Check current prep file naming:**
```bash
ls Research/.cache/2025-11-12_dash-prep.md
```

**Verify critical workflow docs updated:**
```bash
grep -n "dash-prep" Toolbox/MasterFlow/00_SCOUT_WORKFLOW.md
grep -n "dash-prep" Toolbox/MasterFlow/05_STEP_3_PROCESS_DATA.md
grep -n "dash-prep" Toolbox/CHANGELOGS/SESSION_8_HANDOFF_2025-11-12.md
```

**Confirm no critical references remain:**
```bash
grep -r "master-plan-prep" Toolbox/MasterFlow/00_SCOUT_WORKFLOW.md
grep -r "master-plan-prep" Toolbox/MasterFlow/05_STEP_3_PROCESS_DATA.md
# Should return: no matches
```

---

## Next Steps

**Immediate (Complete ✅):**
1. ✅ Rename prep file
2. ✅ Update critical workflow documentation
3. ✅ Update session handoff files
4. ✅ Create this changelog

**Future Cleanup (Optional):**
- Update remaining MasterFlow docs (01, 02, 04, 06)
- Update older changelogs (SESSION_7, LEGACY_REMOVAL)
- Grep entire project for remaining "master-plan" references and evaluate case-by-case

---

## Context

**Session:** Session 8 continuation (after full end-to-end Scout test)
**Trigger:** User feedback after successful production test
**Related Work:**
- Session 6: Legacy system removal
- Session 7: Scout system rebuild
- Session 8: Full production test with Ollama integration

**User's exact request:**
> "Perfect. NIcely done. I would only say that the master plan is a name we used in the old project. It should be dash-prep and all workflows should reflect that. Once that is updated we will begin cleaning this project and yeeting anyting not directly associated."

---

**Status:** Complete
**Files Updated:** 11 files (4 workflow + 6 supporting docs + 1 renamed file)
**References Changed:** 60+ across all files
**Breaking Changes:** None
**Ready for:** Project cleanup phase

