# Dashboard Update System - Quick Reference

**Status:** ✅ Phase 1 Production Ready
**Phase:** Phase 1 (3 critical user-facing sections)
**Phases 2-4:** Documented, ready for implementation when needed

**TL;DR:** Use this when you need to update dashboard.json quickly.

---

## Daily Update (Phase 1 - 5 minutes)

```bash
# 1. Scan for stale sections
python scripts/utilities/scan_dashboard_timestamps.py --target-date 2025-11-01

# 2. Update critical sections (quickActions, riskItems, providerConsensus)
python scripts/utilities/update_dashboard_phase1.py --target-date 2025-11-01

# 3. Verify updates worked
python scripts/utilities/scan_dashboard_timestamps.py --target-date 2025-11-01

# 4. Open in browser to see changes
# scout/dash.html
```

**Expected Output:**
```
[OK] Updated quickActions (4 cards)
[OK] Updated riskItems (5 items)
[OK] Updated providerConsensus (5 themes)

[OK] PHASE 1 UPDATE COMPLETE!
```

---

## File Locations

| File | Purpose |
|---|---|
| `Toolbox/MasterFlow/Docs/DASHBOARD_SYSTEM_COMPLETE.md` | Full system overview |
| `Toolbox/MasterFlow/Docs/DASHBOARD_STALE_SECTIONS_MAPPING.md` | All 18 stale sections |
| `Toolbox/MasterFlow/Docs/DASHBOARD_UPDATE_GUIDE.md` | Manual update steps (6-8) |
| `Toolbox/MasterFlow/Docs/DASHBOARD_SECTION_MAPPING.md` | Data source mapping |
| `scripts/utilities/scan_dashboard_timestamps.py` | Scanner tool |
| `scripts/utilities/update_dashboard_phase1.py` | Updater tool |

---

## What Gets Updated

### Phase 1 (✅ Complete)

**3 Critical User-Facing Sections:**

1. **quickActions** - 4 cards (RISK, HEDGE, ENTRY, CATALYST)
   - Data from: scout/dash.md IMMEDIATE IMPLICATIONS
   - Visible: Top of dashboard

2. **riskItems** - 5 risk items
   - Data from: scout/dash.md KEY RISKS
   - Visible: Risk monitoring list

3. **providerConsensus** - 5 themes
   - Data from: prep file Step 3E (Cross-Source)
   - Visible: Dashboard themes section

### Phase 2-4 (Documented for Future)

14 additional sections in tabs (not yet automated)

---

## When to Run

| Time | Action |
|---|---|
| After Step 3G (Update master-plan.md) | Run scanner + Phase 1 updater |
| Daily | As part of Step 3H workflow |
| Before reviewing dashboard | Verify with scanner |
| If dashboard looks stale | Run Phase 1 updater |

---

## Troubleshooting

| Problem | Solution |
|---|---|
| Script not found | Verify path: `scripts/utilities/scan_*.py` |
| Prep file missing | Ensure `Research/.cache/2025-11-01_dash-prep.md` exists |
| JSON errors | Run `python -m json.tool master-plan/dashboard.json` |
| Dashboard not updating | Hard refresh browser (Ctrl+Shift+R) |

---

## Manual Update (If Scripts Fail)

See: `Toolbox/MasterFlow/Docs/DASHBOARD_UPDATE_GUIDE.md`

Steps to do manually:
- Step 6: Update quickActions (10 min)
- Step 7: Update riskItems (5 min)
- Step 8: Update providerConsensus (5 min)

---

## Integration with Workflow

```
Step 3G: Update master-plan.md
  ↓
Step 3H: Update dashboard.json
  ├─ python scan_dashboard_timestamps.py
  ├─ python update_dashboard_phase1.py
  └─ Verify in browser
  ↓
Done! Dashboard is current
```

---

## Status

| Component | Status |
|---|---|
| Phase 1 Automation | ✅ Ready |
| Phase 1 Updates | ✅ Applied (Nov 1) |
| Documentation | ✅ Complete |
| Scanner | ✅ Working |
| Phases 2-4 | 📋 Documented |

---

## For More Information

- Full system details → DASHBOARD_SYSTEM_COMPLETE.md
- All 18 stale sections → DASHBOARD_STALE_SECTIONS_MAPPING.md
- Manual steps → DASHBOARD_UPDATE_GUIDE.md
- Field mapping → DASHBOARD_SECTION_MAPPING.md

---

**Status:** Production Ready
**Last Updated:** 2025-11-01
