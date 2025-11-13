# STEP 1: CLEANUP - Remove Old Data

**Date:** 2025-11-01
**Purpose:** Clean old research data before running new scrapers

---

## WHAT IT DOES

Removes stale data files to:
- Prevent analyzing old data
- Reduce disk space usage
- Keep only current/recent data
- Clear legacy backup files

---

## HOW TO RUN

**Command:**
```bash
python c:\Users\Iccanui\Desktop\Investing\Toolbox\scripts\cleanup\scout_cleanup.py
```

**Expected Duration:** ~5-10 seconds

**Output:** Log showing what was removed and how much space was freed

---

## WHAT GETS CLEANED

### Ultra-Aggressive (Keeps ONLY Today's Data)

**Category Overview Files:**
- Research/RSS/*_Category_Overview.md (retention: 1 day)
- Research/YouTube/*_Category_Overview.md (retention: 1 day)
- Research/Technicals/*_Category_Overview.md (retention: 1 day)
- Research/X/*_Category_Overview.md (retention: 1 day)

**Cached Analysis Files:**
- Research/.cache/*_Market_Sentiment_Overview.md (retention: 1 day)
- Research/.cache/*_key_themes.md (retention: 1 day)

**Signal History (KEPT FOR TREND TRACKING):**
- Research/.cache/signals_*.json - **NOT cleaned** (kept indefinitely for trend analysis)

**Why Ultra-Aggressive on Intermediate Files?**
- Prevents token inflation from reading old files
- Forces fresh analysis each day
- Signal history preserved separately for trend tracking

---

### Moderate Retention (Keeps Recent History)

**Provider Archives:**
- Research/RSS/_archives/* (retention: 30 days)
- Research/YouTube/_archives/* (retention: 30 days)
- Research/.archive/* (retention: 60 days)

**Legacy Scraper Output:**
- Scraper/output/RSS/* (retention: 7 days)
- Scraper/output/X/* (retention: 7 days)
- Scraper/output/YouTube/* (retention: 7 days)

**Archived Twitter Data:**
- Toolbox/archived_data/X_twitter_archive/*.json (retention: 14 days)

---

### Immediate Removal (retention: 0 days)

**Legacy Folders:**
- Toolbox/archived_data/* (deprecated workflow artifacts)
- Toolbox/archived_scrapers/* (old scraper code)
- Toolbox/Backups/* (manual backup folders)

**Backup Files:**
- master-plan/master-plan.backup*
- master-plan/research-dashboard-backup*.html
- master-plan/archive/backups/*

**Bytecode Caches:**
- Scraper/__pycache__/*.pyc
- scripts/__pycache__/*.pyc

**Legacy Technical Data:**
- Research/Technicals/RealTime/**
- Research/Technicals/2025-10/**

---

## CLEANUP RULES SUMMARY

**Total Rules:** 30+ cleanup rules defined

**Categories:**
1. Category overviews (1 day retention)
2. Cached analysis files (1 day retention)
3. Provider archives (7-60 day retention)
4. Legacy folders (0 day retention - immediate removal)
5. Backup files (0 day retention)
6. Bytecode caches (0 day retention)

---

## VERIFICATION

**After cleanup completes, verify:**
- [ ] Log shows "Wingman cleanup complete"
- [ ] Number of files removed reported
- [ ] Disk space reclaimed reported
- [ ] No errors in log

**Expected Log Output:**
```
Wingman cleanup starting (dry_run=False)
Applying rule: Research category overviews | removed=4 | reclaimed=125.3KB
...
Wingman cleanup complete | paths_removed=47 | total_reclaimed=2.8MB
```

---

## DRY RUN MODE

**To see what WOULD be deleted without actually deleting:**
```bash
python scout_cleanup.py --dry-run
```

**Use this to:**
- Preview what will be removed
- Verify cleanup behavior
- Test before running for real

---

## ADVANCED OPTIONS

**Keep data from specific date:**
```bash
python scout_cleanup.py --keep-from 2025-11-01
```

**Override retention for all rules:**
```bash
python scout_cleanup.py --retention-override 7
```

**Run specific rules only:**
```bash
python scout_cleanup.py --rules "category overviews" "cached"
```

---

## TROUBLESHOOTING

**Problem:** Cleanup fails with permission error
**Solution:** Check file isn't open in another program, close Excel/text editors

**Problem:** Cleanup removes too much
**Solution:** Use `--dry-run` first to preview, adjust retention with `--keep-from`

**Problem:** Cleanup removes too little
**Solution:** Check retention days are correct, verify file modification dates

---

## NEXT STEP

After cleanup completes successfully:
→ Proceed to **STEP 2: Run Scrapers**

---

**Status:** Documented
**Script Location:** `Toolbox/scripts/cleanup/scout_cleanup.py`
**Log Location:** `logs/wingman_cleanup.log`
**Last Updated:** 2025-11-01
