# SYSTEM OUTPUTS - What We're Building Toward

**Date:** 2025-11-01
**Purpose:** Document the target outputs for the research workflow

---

## OUTPUT FILES

### 1. scout/dash.md
**Location:** `master-plan/scout/dash.md`

**Purpose:** Narrative analysis document with market intelligence

**Key Sections:**
- **Eagle Eye Macro Overview** - Current market state, immediate implications, key risks
- **Market Sentiment Alignment** - Convictions, opportunities, risks
- **Signal Score** - Overall market assessment (e.g., "70/100 BULLISH")
- **Last Updated Timestamp** - When analysis was last refreshed

**Format:** Markdown (human-readable narrative)

---

### 2. dashboard.json
**Location:** `master-plan/dashboard.json`

**Purpose:** Structured data that feeds the visual dashboard

**Key Sections (from inspection):**
- **Sentiment Cards** (4 cards):
  - Equities
  - Crypto
  - Liquidity Cycle
  - Macro
- **Sentiment History** - Historical signal scores by date
- **Last Updated Timestamps** - Per-section timestamps
- *(Many more sections - needs further exploration)*

**Format:** JSON (machine-readable data)

---

### 3. research-dashboard.html
**Location:** `c:\Users\Iccanui\Desktop\Investing\master-plan\research-dashboard.html`

**Purpose:** Visual display in browser

**How It Works:**
- Reads `dashboard.json` from same directory
- Renders it with CSS/JS
- Static HTML file (no server needed)

**User Interaction:** Double-click to open in browser and view research findings

---

## WORKFLOW HIGH-LEVEL

```
Step 1: Clean old data
         ↓
Step 2: Run scraper (RSS, YouTube, X/Twitter, Technical)
         ↓
Step 3: Process data → Update scout/dash.md (+ dashboard.json?)
         ↓
      DONE - Dashboard ready
```

---

## OPEN QUESTIONS FOR STEP 3 DESIGN

### Q1: Which sections of scout/dash.md do we update?
- [ ] Eagle Eye Macro Overview?
- [ ] Market Sentiment Alignment?
- [ ] Signal score at bottom?
- [ ] All of the above?

### Q2: Do we create intermediate category overview files?
- [ ] Create them (X, YouTube, RSS, Technical overviews) as analysis artifacts?
- [ ] Skip them (go directly from scraped data → master-plan)?

### Q3: Do we update dashboard.json in Step 3?
- [ ] Yes - update it in the same step as scout/dash.md
- [ ] No - separate step for dashboard.json

### Q4: How is the signal score calculated?
- [ ] Python script (automated calculation)
- [ ] Claude assessment (manual analysis)
- [ ] Hybrid (script provides data, Claude interprets)

---

## NEXT STEPS

1. Answer Q1-Q4 above
2. Design Step 3 detailed process
3. Document it in next file: `02_STEP_3_DESIGN.md`
4. Build and test

---

**Status:** In Progress - Gathering requirements
**Last Updated:** 2025-11-01
