# Friday Options Playbook (US Markets)

A focused, rules-based plan for trading **Friday options/0DTE**. Copy/paste into your workflow and customize risk numbers to fit your account.

---

## The Friday Edge (facts to anchor the plan)

- Many underlyings have **Friday-expiring weeklies/0DTE**, so liquidity and gamma are concentrated into the session’s final hours.
- **SPX/SPXW** options are **European-style, cash-settled** (no early assignment); **SPY/QQQ/TSLA** are **American-style, physically settled** (assignment possible).
- **Theta decay** accelerates into expiration—buying late premium needs strong momentum or IV expansion; otherwise prefer **defined-risk spreads** or **premium selling**.
- **Exercise/assignment timing**: Last trading is 4:00 pm ET; holders typically have until **~5:30 pm ET** to submit exercise instructions (**broker cutoffs vary—confirm yours**).
- **Pin risk**: Price often “sticks” near large strikes into the close on expirations; manage short strikes carefully.

---

## Risk Guardrails (non‑negotiable)

- **Max daily loss**: −2R (or −1% of account). Stop trading for the day if hit.
- **Per-trade risk** (0DTE): ≤0.25R on naked debits; ≤0.5R on defined‑risk spreads.
- **Position limits**: Max **2** concurrent open risk positions before noon ET; max **3** after.
- **No naked short options** into the weekend: keep short premium **defined‑risk** (iron fly/condor/BWB).
- **Assignment control**: Prefer **SPX/SPXW** if you want to avoid early assignment; if using SPY/QQQ single‑leg shorts near the bell, flatten or convert to spreads before **3:50 pm ET**.

---

## Friday Schedule (PT / ET)

**06:10–06:25 PT (09:10–09:25 ET) — Prep**  
- Note macro/events, premarket leaders/laggards, and **largest SPY/QQQ/SPX strike open interest** (potential pins).  
- Mark premarket HOD/LOD; load **VWAP** and prior day H/L.  
- Decide your **primary product** (SPXW vs SPY/QQQ) and **strategy mode** (trend vs range).

**06:35–07:15 PT (09:35–10:15 ET) — Opening impulse**  
- Trade **directional only** (debit spreads) once the first pullback/flag forms relative to VWAP.  
- Avoid pure naked calls/puts unless RVOL & tape are exceptional.

**07:15–10:00 PT (10:15–13:00 ET) — Midday**  
- If range-bound around VWAP, **sell premium with defined risk** (iron fly/condor or broken‑wing butterfly) centered on the developing range.  
- If a clean trend persists, keep using **debit spreads** and trail with structure (5‑min swing lows/highs).

**12:00–13:00 PT (15:00–16:00 ET) — Power hour & pin**  
- Expect **pin behavior** toward large strikes; IV usually compresses into the close.  
- Manage short strikes proactively (tighten, roll inside the structure, or close).  
- Be done by **12:50 PT / 3:50 ET**, unless you explicitly plan for exercise/assignment windows.

---

## Core Friday Setups (pick 1–2 per day)

### 1) AM Momentum Debit‑Spread (trend day starter)
**When**: Strong gap with **RVOL > 1.2**, first pullback above/below VWAP.  
**Structure**: Buy **0DTE vertical** near **30–40Δ** (e.g., buy 40Δ call, sell 25–30Δ call; width $1–$5 depending on product).  
**Entry**: Break of pullback high/low with tape confirmation.  
**Risk**: 0.25R per spread; stop = close back through VWAP or loss of structure.  
**Exit**: Scale 50% at ~1.0× debit; trail remainder on 5‑min swing/20‑EMA.

**Why spreads?** They blunt theta/vega drag if momentum stalls vs. naked long options.

---

### 2) Midday Iron Fly (range capture)
**When**: Price compresses around VWAP; realized range < implied move; no fresh catalyst.  
**Structure**: **0DTE iron butterfly** centered near VWAP or the nearest large strike; wings ~0.20–0.25Δ.  
**Risk**: 0.5R; defined.  
**Management**:  
- If price breaks from range with volume, **close** or **roll the tested side** inward to keep a credit.  
- 45–30 min before close, either **take profits** if IV has crushed toward 0.10–0.15Δ wings or convert to an **iron condor** if the range widens slightly.

**Why defined‑risk?** Friday pins can snap; defined wings cap tail risk while harvesting accelerated time decay.

---

### 3) Late‑Day Broken‑Wing Butterfly (“pin hitch”)
**When**: Clear magnet at a high‑OI strike; price repeatedly reverts to that level.  
**Structure**: **0DTE BWB** aligned so max profit sits 0–0.3% from the “pin” strike; target cheap or zero‑debit if possible.  
**Risk**: Typically small (use 0.25R).  
**Exit**: If price leaves the magnet zone, scratch quickly; otherwise manage into the close. Flatten by **3:50 ET** unless fully defined and you’re comfortable with exercise risk.

---

## Instrument Selection (quick guide)

- **SPX/SPXW**: Cash‑settled, European‑style; larger notional; avoids early assignment—excellent for defined‑risk structures and late‑day management.  
- **SPY/QQQ**: Tighter ticks/contract size; American‑style physical settlement—great for scalps but manage assignment risk near the bell.  
- **Single names (TSLA/NVDA/MSFT)**: Only if liquid 0DTE chains with tight spreads and clear catalysts/levels.

---

## Entries & Management — Hard Rules

- **Wait 5–10 minutes after the open**; let spreads tighten.  
- **Only buy premium** when momentum + RVOL are strong **and** you expect **IV expansion**. Otherwise use **spreads**.  
- **Stops**: structure‑based (VWAP loss or prior swing) **or** 50% of debit—whichever comes first.  
- **Scaling**: take partials at 1R; trail to MFE‑50% (half of max favorable excursion).  
- **No averaging down** on 0DTE singles.  
- **Flatten** any American‑style short strikes you don’t want exercised **before 3:50 ET**.

---

## Friday Checklist (print this)

**Pre‑open**
- [ ] Top strikes/open interest for SPY/QQQ/SPX; mark likely **pin levels**.  
- [ ] Econ/news & single‑stock catalysts (earnings, FDA, upgrades).  
- [ ] Choose product + setup (Trend: debit spread; Range: iron fly/condor).  
- [ ] Define **R** and max daily loss.

**During session**
- [ ] Trade only A‑setups that align with VWAP/structure.  
- [ ] Use **limit** orders; work mid‑price; avoid chasing wide spreads.  
- [ ] Monitor realized range vs. IV; shift to premium‑selling if range compresses.

**Power hour**
- [ ] If short premium in SPY/QQQ, decide: close, tighten, or convert to farther‑OTM defined‑risk.  
- [ ] If playing a pin, keep it **defined‑risk** and small.  
- [ ] Flatten discretionary risk by **3:50 ET**.

---

## Compliance & Ops Notes

- **PDT**: If flagged as a Pattern Day Trader in a margin account, you must keep **$25k** equity minimum; day‑trading options counts toward PDT.  
- **Broker mechanics** (exercise/assignment windows, special handling): **confirm with your broker**; internal cutoffs can be earlier than OCC deadlines.

---

## Regime Variants

- **Trend day** (breadth > 70%, strong linear move) → **Debit verticals**; roll winners; avoid selling premium.  
- **Chop day** (VWAP magnet, overlapping 5‑min bars) → **Iron fly/condor** centered on VWAP or largest strike; harvest decay; keep wings tight.  
- **News‑whipsaw** (Fed/CPI on Friday) → Trade **smaller, later**; wait for post‑news structure; avoid naked long premium into IV crush.

---

*This is educational, not financial advice. Backtest and right‑size to your risk.*
