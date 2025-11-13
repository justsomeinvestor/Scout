# Dashboard Backup & Restore Guide

**Created:** 2025-11-13 Session 8
**Purpose:** Provide restore points for Scout dashboard redesigns

---

## Quick Restore

### Restore Latest Redesign (Session 8)
```bash
cp Toolbox/BACKUPS/dash.html.session-8-redesign scout/dash.html
```

### Restore to Git Commit
```bash
git checkout <commit-hash> -- scout/dash.html
```

---

## Available Backups

### Session 8: Professional Redesign
**File:** `dash.html.session-8-redesign`
**Lines:** 1206
**Size:** 52 KB
**Date:** 2025-11-13
**Changes:**
- Color palette: Cyan → Professional blue/emerald/red
- Gradients: Removed (except intentional accent stripe)
- Glows: Removed
- Typography: Added Inter font + type scale
- Spacing: 8px grid system
- Interactions: Elevation-based hover states

---

## Git History

### View Commits
```bash
git log --oneline scout/dash.html
```

### Show Specific Commit
```bash
git show <commit-hash>:scout/dash.html
```

### View Changes Between Commits
```bash
git diff <old-commit>..<new-commit> scout/dash.html
```

---

## Manual Restore Procedures

### Option 1: From Git History
```bash
# List recent commits
git log --oneline -10 scout/dash.html

# Restore specific commit
git checkout <commit-hash> -- scout/dash.html
git add scout/dash.html
git commit -m "Restore dashboard from commit <hash>"
```

### Option 2: From File Backup
```bash
# Copy backup file
cp Toolbox/BACKUPS/dash.html.session-8-redesign scout/dash.html

# Stage and commit
git add scout/dash.html
git commit -m "Restore dashboard from backup (Session 8)"
```

### Option 3: Full Revert (Keep History)
```bash
# Find the commit you want to revert FROM
git log --oneline scout/dash.html

# Revert that commit
git revert <commit-hash>
```

---

## What Was Changed in Session 8

### CSS Variables Added (54 Total)

#### Colors: 30 variables
```css
/* Signals */
--signal-positive: #10b981;
--signal-negative: #ef4444;
--signal-neutral: #6366f1;
--signal-warning: #f59e0b;

/* Interactive */
--interactive-primary: #3b82f6;
--interactive-hover: #60a5fa;
--interactive-active: #2563eb;

/* Backgrounds */
--bg-primary: #0a0e14;
--bg-secondary: #141921;
--bg-tertiary: #1d2433;

/* Borders */
--border-subtle: #232936;
--border-default: #2d3748;
--border-emphasis: #3d4a5e;

/* Text */
--text-primary: #e8edf4;
--text-secondary: #9ba3b3;
--text-tertiary: #6b7280;

/* Charts */
--chart-bullish: #26a69a;
--chart-bearish: #ef5350;
--chart-neutral: #8b93a6;
--chart-accent: #7c3aed;

/* Shadows */
--shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
--shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
--shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
--shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
--shadow-2xl: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
```

#### Typography: 24 variables
```css
/* Fonts */
--font-primary: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
--font-mono: 'Roboto Mono', 'SF Mono', Consolas, monospace;

/* Sizes */
--text-xs: 0.75rem;
--text-sm: 0.875rem;
--text-base: 1rem;
--text-lg: 1.125rem;
--text-xl: 1.25rem;
--text-2xl: 1.563rem;
--text-3xl: 1.953rem;
--text-4xl: 2.441rem;
--text-5xl: 3.052rem;
--text-6xl: 3.815rem;

/* Weights */
--font-normal: 400;
--font-medium: 500;
--font-semibold: 600;
--font-bold: 700;
--font-extrabold: 800;

/* Heights */
--leading-tight: 1.25;
--leading-snug: 1.375;
--leading-normal: 1.5;
--leading-relaxed: 1.625;
--leading-loose: 2;
```

#### Spacing: 7 variables (8px grid)
```css
--space-1: 0.5rem;   /* 8px */
--space-2: 1rem;     /* 16px */
--space-3: 1.5rem;   /* 24px */
--space-4: 2rem;     /* 32px */
--space-5: 2.5rem;   /* 40px */
--space-6: 3rem;     /* 48px */
--space-8: 4rem;     /* 64px */
```

### Major Changes
1. **Removed:** 7 gradients
2. **Removed:** All glow effects
3. **Replaced:** All cyan references (52+ instances)
4. **Added:** Inter font from Google Fonts
5. **Implemented:** Professional type scale
6. **Implemented:** 8px grid spacing
7. **Updated:** All component styles
8. **Updated:** Chart colors (JavaScript)
9. **Added:** Professional shadow system
10. **Added:** Focus states for accessibility

---

## Verification Steps

### Confirm Backup Exists
```bash
ls -lh Toolbox/BACKUPS/dash.html.session-8-redesign
```

### Verify Backup Matches Current
```bash
diff scout/dash.html Toolbox/BACKUPS/dash.html.session-8-redesign
# Should show: Files are identical
```

### Check Line Count
```bash
wc -l scout/dash.html
# Should be: 1206 lines
```

### Verify No Cyan Colors
```bash
grep "00d9ff" scout/dash.html
# Should show: (no results)
```

### Check CSS Variables Defined
```bash
grep -c "var(--" scout/dash.html
# Should be: 140+ uses
```

---

## Troubleshooting

### If Restore Fails

#### Git Conflict
```bash
# Abort merge
git merge --abort

# Try restore again
git checkout <commit-hash> -- scout/dash.html
```

#### File Locked
```bash
# Close all editors
# Try restore again
```

#### Backup Corrupted
```bash
# Restore from git history instead
git log --oneline scout/dash.html
git checkout <old-commit> -- scout/dash.html
```

---

## File Locations

### Current Dashboard
`scout/dash.html` (1206 lines, 52 KB)

### Session 8 Backup
`Toolbox/BACKUPS/dash.html.session-8-redesign` (1206 lines, 52 KB)

### Session 8 Changelog
`Toolbox/CHANGELOGS/SESSION_8_DASHBOARD_REDESIGN.md`

### Previous Session Notes
`Toolbox/CHANGELOGS/SESSION_7_HANDOFF.md`

---

## Important Notes

1. **Always commit before major changes:** `git add . && git commit -m "message"`
2. **Backup is automated:** Git history is primary backup
3. **No data loss risk:** Only CSS/styling changed, all data preserved
4. **Backward compatible:** Design system, no breaking changes
5. **Easy to reverse:** All changes in CSS variables and classes

---

## Support

### Questions?
Refer to: `Toolbox/CHANGELOGS/SESSION_8_DASHBOARD_REDESIGN.md`

### Need to understand changes?
Read through the changelog's "Technical Details" section

### Want to make further adjustments?
Edit CSS variables in `:root` block (lines 11-89 of dash.html)

