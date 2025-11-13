# Quick Actions Reference Guide

**Set up and use the Command Center Quick Actions panel**

---

## 🎯 What's Available

Five powerful quick actions for your trading workflow:

### 1. 🔍 **Wingman Recon**
- **Trigger:** Click button or say "Wingman Recon"
- **What it does:** Runs `python scripts/automation/run_all_scrapers.py`
- **Executes:** All market scanners and data collection
- **Status:** Shows real-time notification
- **Use when:** Want fresh market data from all sources

### 2. 🗺️ **Wingman Prep**
- **Trigger:** Say "wingman prep"
- **What it does:** Manual AI research workflow (Steps 0-4)
- **Executes:** Claude reads raw data, creates 16+ provider summaries + market sentiment overview
- **Outputs:** Creates 16+ markdown files + calculates composite signal score
- **Status:** Real-time updates through conversation (not automated)
- **Time:** ~30-45 minutes
- **Prerequisites:** Must run "wingman recon" first
- **Use when:** Daily research analysis after fresh data collection

### 3. 📊 **Wingman Dash**
- **Trigger:** Say "wingman dash"
- **What it does:** Update dashboard with research data (Steps 6-9)
- **Executes:** Python automated scripts + AI narrative updates for stale sections
- **Outputs:** Updates master-plan.md, refreshes dashboard visualization
- **Status:** Real-time updates through conversation
- **Time:** ~20-60 minutes (depending on stale sections)
- **Prerequisites:** Must have completed "wingman prep" workflow first
- **Use when:** After research workflow completes, before daily trading
- **Details:** Runs automated phase checks, identifies stale sections, updates with fresh AI narratives

### 4. 📊 **Daily Plans**
- **Trigger:** Click button or say "Create daily trade plans"
- **What it does:** Generates bullish/bearish trade plans
- **Executes:** Daily trade plan workflow
- **Status:** Shows real-time notification
- **Use when:** 9:30 AM to get ready-to-trade plans for the day

### 5. 🎲 **Signals**
- **Trigger:** Click button or say "Generate signals"
- **What it does:** Creates quality-scored trading signals
- **Executes:** Signals quality scoring workflow
- **Status:** Shows real-time notification
- **Use when:** Want scored signals from research dashboard

---

## 📍 Where to Find Quick Actions

Location: **Command Center (Journal/command-center.html)**

Visual placement:
```
┌─ Wingman Command Center ──────────────────────┐
│                                               │
│ [Analyzer Input Section]                      │
│ 🎯 Analyze Ticker: [INPUT] [ANALYZE] [CLEAR]│
│                                               │
│ ⚡ QUICK ACTIONS SECTION (NEW!)               │
│ ⚡ Quick Actions:                             │
│ [🔍 Wingman Recon] [📊 Daily Plans] [🎲 Signals]
│ ⏱️ Descriptions of each action...             │
│                                               │
│ [Live Analysis Results]                       │
│ ...                                           │
└───────────────────────────────────────────────┘
```

---

## 🚀 How to Use Each Button

### Wingman Recon Button

**Click the button:**
```
🔍 Wingman Recon
```

**What happens:**
1. Orange status notification appears (top right)
2. Text: "🔍 WINGMAN RECON: Market scanners running..."
3. Backend executes: `python scripts/automation/run_all_scrapers.py`
4. All market scrapers run simultaneously:
   - Stock data collection
   - Options data collection
   - Sentiment data collection
   - Economic calendar updates
   - Any other configured scrapers
5. Status updates: "✅ WINGMAN RECON: Complete!"
6. Notification disappears after 5 seconds

**Use cases:**
- Morning (9:30 AM): Get fresh data before trading
- Mid-day: Refresh all market data
- Before signal generation: Ensure latest data
- Before daily plans: Use most recent research

---

### Daily Plans Button

**Click the button:**
```
📊 Daily Plans
```

**What happens:**
1. Blue status notification appears (top right)
2. Text: "📊 DAILY PLANS: Generating trade plans..."
3. Backend executes daily trade plan workflow:
   - Loads research dashboard data
   - Identifies key levels for your watchlist
   - Creates bullish scenarios with targets/stops
   - Creates bearish scenarios with targets/stops
   - Pulls context about recent price action
   - Formats all plans for display
4. Status updates: "✅ DAILY PLANS: Generated!"
5. Plans populate in Command Center
6. Notification disappears after 5 seconds

**Use cases:**
- Every morning (9:30 AM ET): Get fresh daily plans
- Mid-day: Regenerate with updated prices
- Before trading: Review available plans
- When market opens: Decide which to trade

**What you see after:**
```
$SPX TRADE PLAN 📈 📉
BULLISH: SPX above 6640 | SPX Oct 22 6700C
T: 6700, 6762  SL: 6600

BEARISH: SPX under 6600 | SPX Oct 22 6550P
T: 6550, 6500  SL: 6640

[Context + Today's Bias]
```

---

### Signals Button

**Click the button:**
```
🎲 Signals
```

**What happens:**
1. Yellow status notification appears (top right)
2. Text: "🎲 SIGNALS: Generating quality-scored signals..."
3. Backend executes signals workflow:
   - Loads research dashboard
   - Extracts sentiment, consensus, levels, catalysts
   - Identifies top setups
   - Scores each on 5 dimensions (0-100)
   - Assigns quality tier (EXTREME/STRONG/MODERATE/WEAK/AVOID)
   - Calculates entry/stop/targets
4. Status updates: "✅ SIGNALS: Generated!"
5. Signal cards populate in Command Center
6. Notification disappears after 5 seconds

**Use cases:**
- Morning: Get quality-scored trading signals
- Mid-day: Update if market changed
- Before execution: Review quality scores
- End-of-day: Track which signals worked

**What you see after:**
```
SIGNAL #1: ES Long at 5650-5655
Quality Score: 78/100 → STRONG BUY

Technical   ██████████  85/100
Consensus   ████████░   73/100
Sentiment   ████████░   75/100
Catalyst    ███████░    70/100
Volume      ██████████  80/100

Entry: 5650-5655 | Stop: 5600 | Target: 5700
```

---

## 🔊 Voice Commands

You can trigger these via voice commands to Claude:

### Wingman Recon
```
"Wingman Recon"
or
"Run market scanners"
or
"Get fresh market data"
```

### Wingman Prep (Research Workflow)
```
"Wingman prep"
or
"Run research workflow"
or
"Create research summaries"
```

### Wingman Dash (Dashboard Update)
```
"Wingman dash"
or
"Update dashboard"
or
"Sync research to dashboard"
```

### Daily Plans
```
"Create daily trade plans"
or
"Generate daily plans for SPX, ES, QQQ"
or
"Build my morning trade plans"
```

### Signals
```
"Generate trading signals"
or
"Create quality-scored signals"
or
"Build signals from research"
```

---

## 📊 Daily Workflow Using Quick Actions

### Morning (9:30 AM)
```
1. Click/Say: 🔍 Wingman Recon
   └─ Wait for completion (1-2 minutes)
   └─ Fresh market data ready

2. Say: 🗺️ Wingman Prep
   └─ Wait for completion (30-45 minutes)
   └─ 16+ research summaries + signal score calculated

3. Say: 📊 Wingman Dash
   └─ Wait for completion (20-60 minutes)
   └─ Dashboard updated with fresh research

4. Click: 📊 Daily Plans
   └─ Wait for completion (30 seconds)
   └─ See bullish/bearish plans for each ticker

5. Click: 🎲 Signals
   └─ Wait for completion (30 seconds)
   └─ Quality-scored trading opportunities

6. Review plans & signals
   └─ Pick 1-2 best setups
   └─ Set entry alerts
```

### During Trading (10:00 AM - 3:30 PM)
```
1. Monitor prices against your plans
2. Execute when entry levels hit
3. Log entry to journal
4. Exit at target or stop
```

### Before Close (3:30 PM)
```
1. Close all positions
2. Log trades to journal
```

### After Close (4:00 PM)
```
Tell Claude: "EOD review - which plans worked?"
```

---

## ⚙️ Status Notifications

All quick actions show status notifications (top right):

### Orange (Wingman Recon)
```
🔍 WINGMAN RECON: Market scanners running...
↓ (after completion)
✅ WINGMAN RECON: Complete! All scrapers finished.
```

### Blue (Daily Plans)
```
📊 DAILY PLANS: Generating trade plans...
↓ (after completion)
✅ DAILY PLANS: Generated! Check Command Center.
```

### Yellow (Signals)
```
🎲 SIGNALS: Generating quality-scored signals...
↓ (after completion)
✅ SIGNALS: Generated! Check Command Center.
```

### Error (Any action)
```
❌ ACTION_NAME: Error message here. Check console.
```

All notifications auto-dismiss after 5 seconds or click to close.

---

## 💡 Pro Tips

### 1. **Wingman Recon First**
- Always run Wingman Recon before Daily Plans or Signals
- Ensures all your data is fresh
- Only takes 1-2 minutes

### 2. **Daily Plans Before Trading**
- Generate fresh daily plans every morning
- Review before market opens
- Pick your best setups early

### 3. **Signals for Confirmation**
- Generate signals after daily plans
- Use signals to confirm daily plan quality
- Trade only high-quality signals (75+)

### 4. **Update Mid-Day if Needed**
- Click Wingman Recon at 12:00 PM to refresh
- Regenerate plans if price moved significantly
- Update signals if new major move happened

### 5. **Track Performance**
- Note which buttons you used each day
- Track success rate of each workflow
- Optimize over time

---

## 🔧 Integration Details

### Command Center Integration
```
Quick Actions Panel
    ↓
[Wingman Recon Button] → API Call → Python Script Execution
[Daily Plans Button]   → API Call → Daily Plans Workflow
[Signals Button]       → API Call → Signals Workflow
    ↓
Status Notifications (Real-time updates)
    ↓
Results populate in Command Center panels
```

### Backend Endpoints (for developers)
```
Wingman Recon:
  POST /api/automation/run-scrapers
  Payload: {action: "run_all_scrapers"}

Daily Plans:
  POST /api/workflows/generate-daily-plans
  Payload: {action: "generate_plans"}

Signals:
  POST /api/workflows/generate-signals
  Payload: {action: "generate_signals"}
```

---

## ❓ FAQs

**Q: Can I customize the buttons?**
A: Yes - edit the HTML in command-center.html (lines 447-460) to change colors, text, or placement.

**Q: What if a script fails?**
A: Check the console (F12 → Console tab) for error details. Review the Python script logs.

**Q: Can I add more quick actions?**
A: Yes - follow the same pattern: Add button HTML + Add JavaScript function + Add backend endpoint.

**Q: How long do scripts take?**
A: Wingman Recon: 1-2 min | Daily Plans: 30 sec | Signals: 30 sec

**Q: Can I run multiple simultaneously?**
A: Yes - click multiple buttons. They'll queue and run in order.

**Q: What if I forget the command?**
A: The button text and help text reminds you. Hover over buttons for tooltips.

---

## 🎯 Next Steps

### Today:
1. Open Command Center
2. See new Quick Actions panel below analyzer
3. Click one button to test

### Tomorrow Morning (9:30 AM):
1. Click Wingman Recon
2. Click Daily Plans
3. Click Signals
4. Execute best trades

### Going Forward:
Use these buttons as your daily trading routine:
- **9:30 AM:** Recon → Plans → Signals
- **Throughout day:** Execute trades
- **4:00 PM:** EOD review

---

## 📍 Location Summary

**File Modified:** `Journal/command-center.html`
**Section Added:** Quick Actions Panel (lines 447-460)
**Functions Added:** triggerWingmanRecon(), generateDailyPlans(), generateSignals() (lines 1166-1261)
**Visible Location:** Below analyzer, above analysis results

---

**Status:** ✅ Ready to use
**Updated:** October 20, 2025
**Maintenance:** No additional setup required

Just click the buttons and go! 🚀
