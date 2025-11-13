# Trading Signals Quick Reference

**One-page guide to get AI-powered trading signals into your Command Center**

---

## 🎯 What This Does

Takes all the data from `master-plan/research-dashboard.html` and distills it into:
- **1 Market Thesis** (your bias for the day)
- **3-5 Trade Setups** (ready to execute)
- **Quality Scores** (0-100 confidence for each)
- **Entry/Stop/Target** levels (clearly defined)

Result: Signal cards displayed in Command Center, ready to trade.

---

## 🚀 How to Trigger It

### Voice Command to Claude:
```
"Generate trading signals from research dashboard"
or
"Build my trading thesis and top setups"
or
"Create signal cards from current research"
```

---

## 📋 What Claude Does

### Step 1: Load Research Dashboard
- Opens `master-plan/research-dashboard.html`
- Extracts sentiment, consensus, trading levels, economic calendar

### Step 2: Identify Top Setups
- Finds 3-5 highest quality trades based on research
- Each has: asset, direction, entry zone, stop, targets

### Step 3: Score Each Setup
Using 5-component system (all from research dashboard):

```
Technical Confirmation    (40%)  → Chart pattern quality
Provider Consensus        (20%)  → % of signals bullish/bearish
Sentiment Alignment       (15%)  → AI interpretation match
Catalyst Timing          (15%)  → Economic event window
Volume/Flow Quality      (10%)  → Options/volume confirmation

COMPOSITE = (TA×0.4) + (Consensus×0.2) + (Sentiment×0.15) +
            (Catalyst×0.15) + (Volume×0.1)
```

### Step 4: Create Thesis
2-3 sentence summary of market bias and playbook

### Step 5: Display in Command Center
Populates signal cards with all data

---

## 💾 Output Files Created

When Claude runs this workflow:

| File | Purpose |
|------|---------|
| `scripts/research/signals_extracted.json` | Raw data extracted from research dashboard |
| `scripts/research/signals_preview.html` | HTML preview of signal cards |
| Command Center Signal Panel | Live display in browser |

---

## 🎲 Signal Quality Tiers

| Score | Tier | Action |
|-------|------|--------|
| 90-100 | EXTREME | Trade full conviction |
| 75-89 | STRONG | Trade standard sizing |
| 60-74 | MODERATE | Trade reduced size, tight stops |
| 45-59 | WEAK | Avoid or skip |
| <45 | AVOID | Don't trade |

---

## 📊 Each Signal Card Shows

```
┌─────────────────────────────────────┐
│ Composite Score: 78/100             │
│ Tier: STRONG BUY                    │
├─────────────────────────────────────┤
│ Setup: ES Long at 5650-5655         │
├─────────────────────────────────────┤
│ Technical:      85/100 ████████░   │
│ Consensus:      73/100 ███████░    │
│ Sentiment:      75/100 ███████░    │
│ Catalyst:       70/100 ███████░    │
│ Volume:         80/100 ████████░   │
├─────────────────────────────────────┤
│ Entry: 5650-5655                    │
│ Stop: 5640 (-10 points)             │
│ Target 1: 5680 (+25 points)         │
│ Target 2: 5700 (+45 points)         │
│ Risk/Reward: 1:3.5                  │
├─────────────────────────────────────┤
│ Reasoning: Double bottom support    │
│ with 73% bullish consensus.         │
│ Breadth improving, AI bullish.      │
└─────────────────────────────────────┘
```

---

## 🔄 When to Run This

| Time | Action |
|------|--------|
| **9:30 AM** | "Generate trading signals" → Get day's thesis and top setups |
| **12:00 PM** | "Check research, any new signals?" → Update if thesis broken |
| **3:30 PM** | "EOD signal review" → What worked, what didn't |
| **After News** | Anytime major event breaks → Rebuild signals |

---

## 📚 Related Workflows

- **JOURNAL_ANALYSIS_WORKFLOW.md** - End-of-day analysis (uses these signals)
- **QUICK_COMMANDS_USER_GUIDE.md** - All available commands
- **RESEARCH_DASHBOARD_TO_SIGNALS_WORKFLOW.md** - Full detailed guide

---

## 💡 Pro Tips

1. **Don't force weak signals**
   - Only trade signals with 60+ quality score
   - Better to miss a trade than lose on a weak one

2. **Update aggressively when thesis breaks**
   - If research dashboard changes significantly, rebuild
   - Don't try to force old setups to work

3. **Track what works**
   - Note which signal scores correlate with your wins
   - Adjust component weightings over time

4. **Use the thesis as your daily guide**
   - If thesis is bullish, avoid shorting weak signals
   - If thesis breaks, stop trading and reassess

---

## ✅ Checklist Before Trading

Before entering any signal trade:

- [ ] Signal quality score ≥ 60
- [ ] Stop loss defined (not vague)
- [ ] Risk/Reward ≥ 1:1.5
- [ ] Research dashboard still supports bias
- [ ] No black swan catalysts in next 2 hours
- [ ] You're not already in a winning trade on that setup

---

## 🆘 Troubleshooting

**Q: "Signals aren't showing in Command Center"**
A: Make sure Claude pasted HTML into correct panel. Check console for errors.

**Q: "Scores seem too high/low"**
A: Adjust component weightings in workflow. Technical might be 50% vs 40%, etc.

**Q: "Old signals still showing"**
A: Command Center needs refresh (Ctrl+R). Make sure Claude cleared old cards.

**Q: "Research dashboard doesn't have signal data"**
A: Run extraction Python script: `python scripts/research/extract_signals.py`

---

## 📞 Commands to Use

### Daily Workflow:
```
Morning (9:30 AM):
"Generate trading signals from research dashboard"

Mid-day (12:00 PM):
"Check research, any new signals?"

End-of-day (4:00 PM):
"EOD signal review - what worked"
```

### Anytime:
```
"Rebuild thesis for [TICKER]"
"Check quality of [SETUP NAME]"
"Why is this signal weak?"
"Show me only strong signals (75+)"
"What changed since 9:30?"
```

---

**Last Updated:** 2025-10-19
**Status:** Ready to use immediately
