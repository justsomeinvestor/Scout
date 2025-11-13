# Signal Card HTML Template for Command Center

This template shows how to add trading signal cards to your Command Center. Copy and modify as needed.

---

## Quick Single Signal Card (Minimal)

```html
<div class="signal-score-card">
  <div class="signal-header">
    <div class="signal-composite-score">78</div>
    <div class="signal-tier tier-strong-buy">STRONG BUY</div>
  </div>

  <div class="signal-setup">📈 ES Long at Support 5650-5655</div>

  <div class="signal-breakdown">
    <div class="breakdown-title">QUALITY BREAKDOWN</div>
    <div class="breakdown-grid">
      <div class="breakdown-item">
        <div class="breakdown-label">Technical</div>
        <div class="breakdown-bar-container">
          <div class="breakdown-bar" style="width: 85%"></div>
        </div>
        <div class="breakdown-value">85</div>
      </div>

      <div class="breakdown-item">
        <div class="breakdown-label">Consensus</div>
        <div class="breakdown-bar-container">
          <div class="breakdown-bar" style="width: 73%"></div>
        </div>
        <div class="breakdown-value">73</div>
      </div>

      <div class="breakdown-item">
        <div class="breakdown-label">Sentiment</div>
        <div class="breakdown-bar-container">
          <div class="breakdown-bar" style="width: 75%"></div>
        </div>
        <div class="breakdown-value">75</div>
      </div>

      <div class="breakdown-item">
        <div class="breakdown-label">Catalyst</div>
        <div class="breakdown-bar-container">
          <div class="breakdown-bar" style="width: 70%"></div>
        </div>
        <div class="breakdown-value">70</div>
      </div>

      <div class="breakdown-item">
        <div class="breakdown-label">Volume</div>
        <div class="breakdown-bar-container">
          <div class="breakdown-bar" style="width: 80%"></div>
        </div>
        <div class="breakdown-value">80</div>
      </div>
    </div>
  </div>

  <div class="signal-recommendation">
    ✅ <strong>STRONG SIGNAL</strong><br>
    Double bottom at 5650 support with 73% provider consensus bullish.
    Breadth improving, AI shows modest upside bias. <br><br>
    <strong>Entry:</strong> 5650-5655<br>
    <strong>Stop:</strong> 5640 (-10 points)<br>
    <strong>Target 1:</strong> 5680 (+25 points) - Resistance<br>
    <strong>Target 2:</strong> 5700 (+45 points) - Higher Resistance<br>
    <strong>Risk/Reward:</strong> 1:3.5<br>
    <strong>Confidence:</strong> 78/100
  </div>
</div>
```

---

## Full Trading Signals Panel (3 Signals)

```html
<section class="trading-signals-panel" style="background: rgba(26, 31, 58, 0.6); border: 1px solid rgba(99, 102, 241, 0.1); border-radius: 20px; padding: 30px; margin-bottom: 40px;">

  <h2 style="font-size: 1.5em; margin-bottom: 20px; display: flex; align-items: center; gap: 10px;">
    <span>🎲</span>
    <span>Today's Trading Signals</span>
  </h2>

  <!-- THESIS SUMMARY -->
  <div style="background: rgba(99, 102, 241, 0.1); border-left: 4px solid #6366f1; padding: 15px; margin-bottom: 25px; border-radius: 8px;">
    <div style="font-weight: 600; color: #e0e6f0; margin-bottom: 8px;">📌 TODAY'S THESIS</div>
    <div style="color: #d1d5db; line-height: 1.6;">
      Tech stocks rebounding after oversold conditions and improving breadth.
      Bias: Cautiously Bullish (60% conviction). Playbook: Long ES at support,
      scale at resistance. Risk: If CPI prints hot, thesis breaks (watch for gap down).
    </div>
  </div>

  <!-- SIGNALS GRID -->
  <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 20px;">

    <!-- SIGNAL #1 -->
    <div class="signal-score-card">
      <div class="signal-header">
        <div class="signal-composite-score">78</div>
        <div class="signal-tier tier-strong-buy">STRONG BUY</div>
      </div>

      <div class="signal-setup">📈 ES Long at Support 5650-5655</div>

      <div class="signal-breakdown">
        <div class="breakdown-title">COMPONENTS</div>
        <div class="breakdown-grid">
          <div class="breakdown-item">
            <div class="breakdown-label">Technical</div>
            <div class="breakdown-bar-container">
              <div class="breakdown-bar" style="width: 85%"></div>
            </div>
            <div class="breakdown-value">85</div>
          </div>
          <div class="breakdown-item">
            <div class="breakdown-label">Consensus</div>
            <div class="breakdown-bar-container">
              <div class="breakdown-bar" style="width: 73%"></div>
            </div>
            <div class="breakdown-value">73</div>
          </div>
          <div class="breakdown-item">
            <div class="breakdown-label">Sentiment</div>
            <div class="breakdown-bar-container">
              <div class="breakdown-bar" style="width: 75%"></div>
            </div>
            <div class="breakdown-value">75</div>
          </div>
          <div class="breakdown-item">
            <div class="breakdown-label">Catalyst</div>
            <div class="breakdown-bar-container">
              <div class="breakdown-bar" style="width: 70%"></div>
            </div>
            <div class="breakdown-value">70</div>
          </div>
          <div class="breakdown-item">
            <div class="breakdown-label">Volume</div>
            <div class="breakdown-bar-container">
              <div class="breakdown-bar" style="width: 80%"></div>
            </div>
            <div class="breakdown-value">80</div>
          </div>
        </div>
      </div>

      <div class="signal-recommendation">
        ✅ <strong>STRONG - Trade this</strong><br><br>
        Double bottom at 5650 with 73% bullish consensus. Entry: 5650 | Stop: 5640 | PT1: 5680 | R/R: 1:3.5
      </div>
    </div>

    <!-- SIGNAL #2 -->
    <div class="signal-score-card">
      <div class="signal-header">
        <div class="signal-composite-score">72</div>
        <div class="signal-tier tier-moderate-buy">MODERATE BUY</div>
      </div>

      <div class="signal-setup">📈 QQQ Long at 365-367</div>

      <div class="signal-breakdown">
        <div class="breakdown-title">COMPONENTS</div>
        <div class="breakdown-grid">
          <div class="breakdown-item">
            <div class="breakdown-label">Technical</div>
            <div class="breakdown-bar-container">
              <div class="breakdown-bar" style="width: 80%"></div>
            </div>
            <div class="breakdown-value">80</div>
          </div>
          <div class="breakdown-item">
            <div class="breakdown-label">Consensus</div>
            <div class="breakdown-bar-container">
              <div class="breakdown-bar" style="width: 68%"></div>
            </div>
            <div class="breakdown-value">68</div>
          </div>
          <div class="breakdown-item">
            <div class="breakdown-label">Sentiment</div>
            <div class="breakdown-bar-container">
              <div class="breakdown-bar" style="width: 70%"></div>
            </div>
            <div class="breakdown-value">70</div>
          </div>
          <div class="breakdown-item">
            <div class="breakdown-label">Catalyst</div>
            <div class="breakdown-bar-container">
              <div class="breakdown-bar" style="width: 68%"></div>
            </div>
            <div class="breakdown-value">68</div>
          </div>
          <div class="breakdown-item">
            <div class="breakdown-label">Volume</div>
            <div class="breakdown-bar-container">
              <div class="breakdown-bar" style="width: 72%"></div>
            </div>
            <div class="breakdown-value">72</div>
          </div>
        </div>
      </div>

      <div class="signal-recommendation">
        ⚠️ <strong>MODERATE - Standard sizing</strong><br><br>
        Tech strength signal, good setup but weaker consensus. Entry: 365-367 | Stop: 360 | PT1: 375 | R/R: 1:2.5
      </div>
    </div>

    <!-- SIGNAL #3 -->
    <div class="signal-score-card">
      <div class="signal-header">
        <div class="signal-composite-score">65</div>
        <div class="signal-tier tier-weak">WEAK SELL</div>
      </div>

      <div class="signal-setup">📉 NVDA Short at 130-132</div>

      <div class="signal-breakdown">
        <div class="breakdown-title">COMPONENTS</div>
        <div class="breakdown-grid">
          <div class="breakdown-item">
            <div class="breakdown-label">Technical</div>
            <div class="breakdown-bar-container">
              <div class="breakdown-bar" style="width: 72%"></div>
            </div>
            <div class="breakdown-value">72</div>
          </div>
          <div class="breakdown-item">
            <div class="breakdown-label">Consensus</div>
            <div class="breakdown-bar-container">
              <div class="breakdown-bar" style="width: 55%"></div>
            </div>
            <div class="breakdown-value">55</div>
          </div>
          <div class="breakdown-item">
            <div class="breakdown-label">Sentiment</div>
            <div class="breakdown-bar-container">
              <div class="breakdown-bar" style="width: 65%"></div>
            </div>
            <div class="breakdown-value">65</div>
          </div>
          <div class="breakdown-item">
            <div class="breakdown-label">Catalyst</div>
            <div class="breakdown-bar-container">
              <div class="breakdown-bar" style="width: 60%"></div>
            </div>
            <div class="breakdown-value">60</div>
          </div>
          <div class="breakdown-item">
            <div class="breakdown-label">Volume</div>
            <div class="breakdown-bar-container">
              <div class="breakdown-bar" style="width: 68%"></div>
            </div>
            <div class="breakdown-value">68</div>
          </div>
        </div>
      </div>

      <div class="signal-recommendation">
        ❌ <strong>WEAK - Avoid or use tight stops</strong><br><br>
        Sellers present but weak consensus (55%). Only trade if other conditions align. Entry: 130-132 | Stop: 135 | R/R: 1:2
      </div>
    </div>

  </div>

  <!-- QUICK REFERENCE -->
  <div style="margin-top: 25px; padding: 15px; background: rgba(139, 92, 246, 0.05); border-radius: 8px;">
    <div style="font-size: 0.9em; color: #9ca3af; margin-bottom: 10px;"><strong>QUALITY TIER GUIDE:</strong></div>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px; font-size: 0.85em;">
      <div>🟢 <strong>90-100 EXTREME:</strong> Full conviction</div>
      <div>🟢 <strong>75-89 STRONG:</strong> Standard sizing</div>
      <div>🟡 <strong>60-74 MODERATE:</strong> Reduced size</div>
      <div>🔴 <strong>45-59 WEAK:</strong> Avoid if possible</div>
    </div>
  </div>

</section>
```

---

## Tier CSS Classes Available

Use these classes for different signal quality levels:

```
tier-extreme-buy    → 90-100 (green border)
tier-strong-buy     → 75-89  (green border)
tier-moderate-buy   → 60-74  (blue border)
tier-weak           → 45-59  (yellow border)
tier-avoid          → <45    (red border)
```

---

## Component Score Key

| Component | Meaning | How to Score |
|-----------|---------|--------------|
| Technical | Chart pattern quality | 0-100 based on pattern strength |
| Consensus | Provider agreement % | 0-100 (use actual % from research dashboard) |
| Sentiment | AI interpretation alignment | 0-100 based on AI tone |
| Catalyst | Event timing advantage | 0-100 based on economic calendar |
| Volume | Flow confirmation | 0-100 based on options/volume data |

---

## Integration Steps

1. **Copy the HTML above**
2. **Paste into `command-center.html` after the Analysis Panel section**
3. **Update scores when you run "Generate trading signals from research dashboard"**
4. **Keep it at top of page for easy access during trading day**

---

## Dynamic Update Instructions

When Claude runs the workflow:

1. Read current research-dashboard.html
2. Extract signal data using Python script or manual analysis
3. Calculate quality scores (see RESEARCH_DASHBOARD_TO_SIGNALS_WORKFLOW.md)
4. Update only the following fields:
   - `.signal-composite-score` (main score 0-100)
   - `.signal-tier` (tier badge class)
   - `.signal-setup` (setup description)
   - `width: XX%` in breakdown bars (each component score)
   - `.breakdown-value` (component scores)
   - `.signal-recommendation` (reasoning + entry/stop/targets)

---

**Last Updated:** 2025-10-19
