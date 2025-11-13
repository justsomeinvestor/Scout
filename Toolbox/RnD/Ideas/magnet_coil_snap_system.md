# Magnet–Coil–Snap System  
### BigPic Research — Systematic Trading Framework Proposal

---

## Overview
The **Magnet–Coil–Snap (MCS)** system is a modular, rules-based trading engine designed to identify and trade volatility compressions (“coils”) around price magnets (VWAP, POC, range midpoints) that precede directional expansions (“snaps”).  

It integrates **multi-timeframe price action**, **volatility and momentum metrics**, **VWAP and moving-average context**, and **options market structure** into a unified decision matrix producing **quantified trade signals**.

---

## Core Objectives
- Detect **when and where price is coiling** before an expansion.  
- Quantify **trend strength**, **volatility regime**, and **options gamma regime**.  
- Generate a consistent **bias + confidence score** across timeframes.  
- Automate **trade sizing, stops, and targets** using volatility and range data.  
- Log all signals and outcomes to the **Journal.md** and **Master-Plan** dashboards for backtesting and AI learning.

---

## System Inputs

### Price & Volatility
- OHLCV data, **ATR**, **realized volatility**, **Bollinger bandwidth**.  
- **RSI**, **EMA5/EMA20/200SMA**, **MACD slope spread**.  
- **VWAP + σ bands**, anchored VWAPs (session, weekly, monthly).  
- Range positions (yearly, monthly, weekly, daily).

### Market Profile
- **POC**, **volume shelves**, and **range midpoints**.  
- **Deviation from VWAP** in σ-score form.

### Options Data
- **Gamma exposure (GEX)**, **zero-gamma**, **max-pain**, **OI density**, **IV rank**, and **dealer gamma regime**.  
- **VIX term structure** (for index context).

---

## Regime Detection
| Regime | Criteria | Trading Behavior |
|---------|-----------|------------------|
| **Trend** | EMA20 slope + RSI>55/RSI<45 + VWAP slope aligned | Momentum continuation |
| **Mean-reversion** | Price near VWAP ±1σ, RSI 40-60, flat VWAP | Fade magnets |
| **Coil** | BB width ≤20th %ile + ATR below 40-bar median | Prepare for breakout |
| **Expansion** | Rising ATR + widening BB width | Trend follow |
| **Gamma regimes** | Dealer short-gamma → amplified moves<br>Dealer long-gamma → pin/range | Adjust stops/targets |

---

## Signal Modules (each returns −1→+1)
1. **MCS signal (35%)** – Magnet/coil/snap detection.  
2. **Base/Distribution (20%)** – 5-min basing rules confirmation.  
3. **Trend Momentum (20%)** – EMA alignment and RSI confirmation.  
4. **Range Position (10%)** – Distance from higher-TF extremes.  
5. **VWAP Deviation (10%)** – Mean-reversion strength.  
6. **Options Pressure (5%)** – Gamma and max-pain bias.

Composite score = weighted sum per timeframe → aggregated into a **Bias** and **Confidence**.

---

## Decision Matrix

| Condition | Action |
|------------|--------|
| Trend ON or Coil→Snap triggered | Enable breakout setups |
| Long-gamma pin | Enable VWAP fade setups |
| Bias = +1 | Look long |
| Bias = −1 | Look short |
| Confidence | Scales position size (0.5–1.5× risk unit) |

**Stops/Targets**
- Stop: opposite edge of coil or VWAP ± 1.5σ.  
- T1 = 0.5 W , T2 = 1 W , T3 = 1.5 W.  
- Flatten on regime flip or two closes back inside coil.

---

## Trade Types
1. **Break–Retest (preferred)** — Snap + retest of coil edge with rejection.  
2. **Stop-Entry Breakout** — Stop just beyond coil with volume confirmation.  
3. **VWAP Fade** — Pin regime trades back to magnet; smaller size.

---

## Risk Controls
- Per-trade risk: $75–$125.  
- Max 2 attempts per setup per symbol per session.  
- Session kill after 3 × −1R losses.  
- Flatten if opposite regime confirmed.

---

## Automation & Logging
All signals and trade decisions append to **Journal.md**:
- Regime snapshot (trend/MR, coil/expansion, gamma).  
- Magnet, W, VWAP Z, RSI, gamma levels.  
- Entry/stop/targets, outcome (R).  
- Notes from market context and Andy stream.

---

## Data Schema (example)
```yaml
symbol: NVDA
session:
  magnet: 188.6
  range: {high: 190.4, low: 185.8, width: 4.6}
  vwap: {value: 187.9, z: -0.8}
  mas: {ema5: 187.6, ema20: 188.3, sma200: 189.1}
  options: {gamma_zero: 188, regime: short_gamma}
signals:
  mcs: -1
  base: -0.8
  trend: -0.7
  range_pos: -0.4
  vwap_dev: -0.2
  options_pressure: -0.1
score:
  tf_5m: -0.64
  tf_15m: -0.58
decision:
  bias: short
  confidence: 0.55
  setup: break_retest
  risk_unit: 100
  size_factor: 1.0
  targets: [0.5W, 1.0W, 1.5W]
```

---

## Implementation Roadmap
| Phase | Goal | Deliverable |
|-------|------|--------------|
| **0** | Manual signal blocks + scoring (notebook) | Journal logging |
| **1** | Add options feed (GEX, γ₀, max-pain) | Dealer-regime gating |
| **2** | Integrate into **Master-Plan** dashboard (live metrics) | Real-time signal monitor |
| **3** | Feedback loop & analytics | Performance dashboards, AI tuning |

---

**Summary:**  
This proposal formalizes your observational framework — the Magnet–Coil–Snap structure — into a data-driven, multi-input system ready for automation. It preserves your discretionary edge while allowing scalable, rule-based execution.

