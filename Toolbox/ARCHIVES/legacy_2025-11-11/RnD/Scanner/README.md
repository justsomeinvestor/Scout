# AI-Powered Real-Time Trading Scanner

**Status:** 🔬 Research & Development (RnD)
**Location:** `RnD/Scanner/`
**Started:** 2025-10-29
**Target:** Production-ready MVP in 4-5 weeks

---

## 🎯 Project Overview

Real-time intraday trading scanner for stocks, options, and crypto using:
- **FREE data sources** (APIs + web scraping, NO yfinance)
- **Local AI/ML** (Ollama at 192.168.10.52:11434 + scikit-learn)
- **Web scraping** (Barchart, Finviz, Yahoo, MarketWatch)
- **Cost:** $0/month

### Key Features
- Real-time RVOL alerts (Alpaca WebSocket)
- Pattern detection (ORB, VWAP, bull flags)
- AI-powered alert scoring (Ollama + RandomForest)
- Options unusual activity detection
- Crypto scanning (Binance WebSocket)
- Nightly ML retraining pipeline
- Wingman trading partner integration

---

## 📁 RnD Workflow Guidance

### **IMPORTANT: RnD-to-Production Process**

This project follows a **prototype-first, promote-later** workflow:

1. **RnD Phase (Current):**
   - All code stays in `RnD/Scanner/`
   - Rapid iteration and experimentation
   - Break things, test ideas, fail fast
   - Documentation co-located with code

2. **Validation Phase:**
   - Run live for 2-4 weeks
   - Collect performance data
   - Validate data quality and reliability
   - Measure alert quality and ML accuracy

3. **Production Promotion (Once Proven):**
   - Move stable modules to production locations:
     - Scrapers → `Scraper/` (with existing scrapers)
     - Scanner core → `Scanner/` (new top-level directory)
     - Wingman integration → `Toolbox/INTEGRATIONS/Scanner/`
   - Update `CLAUDE.md` with new workflows
   - Archive RnD code (keep for reference)

### **Why This Approach?**

- ✅ **Safe:** Won't break existing systems (Wingman, Journal, scrapers)
- ✅ **Clean:** RnD code isolated from production
- ✅ **Fast:** No need to be perfect initially
- ✅ **Reversible:** Easy to abandon if approach doesn't work

### **When to Promote to Production**

Only move to production when:
- [ ] Scanner runs reliably for 2+ weeks
- [ ] No rate limit issues from scrapers
- [ ] ML models showing positive edge (>55% win rate on backtests)
- [ ] Alert quality acceptable (<20% false positive rate)
- [ ] Wingman integration tested and working
- [ ] Documentation complete

---

## 🚀 Quick Start

### Prerequisites
```bash
# Python 3.12+ required
python --version

# Install dependencies
pip install -r requirements.txt

# Verify Ollama access
curl http://192.168.10.52:11434/api/tags
```

### Run Scanner (Development)
```bash
cd RnD/Scanner
python scanner/main.py
```

### Run Nightly ML Pipeline
```bash
cd RnD/Scanner
python scanner/train.py
```

### Launch Dashboard
```bash
cd RnD/Scanner
streamlit run scanner/ui/streamlit_app.py
```

---

## 📊 Project Structure

```
RnD/Scanner/
├── scanner/                      # Main scanner package
│   ├── config/                   # Configuration files
│   ├── scrapers/                 # Web scrapers (Barchart, Finviz, etc.)
│   ├── ingestion/                # Real-time data (Alpaca, Binance)
│   ├── signals/                  # RVOL, patterns, VWAP
│   ├── rules/                    # Rule engine (YAML-driven)
│   ├── ai/                       # Ollama integration
│   ├── ml/                       # scikit-learn models
│   ├── alerts/                   # Priority routing, notifications
│   ├── storage/                  # SQLite, JSONL logging
│   ├── backtest/                 # Performance analysis
│   ├── training/                 # Nightly ML pipeline
│   ├── ui/                       # Streamlit dashboard
│   ├── integrations/wingman/     # Wingman system integration
│   └── tests/                    # Unit tests
│
├── data/                         # Data storage (gitignored)
│   ├── alerts/                   # JSONL alert logs
│   ├── bars/                     # OHLCV data
│   ├── cache/                    # Scraped data cache
│   ├── models/                   # ML models (versioned)
│   └── reports/                  # Daily reports
│
├── docs/                         # Documentation
│   ├── data_sources.md          # API/scraping details
│   ├── alert_system.md          # Alert routing specs
│   ├── ml_models.md             # ML architecture
│   └── wingman_integration.md   # Integration guide
│
├── README.md                     # This file
├── requirements.txt              # Python dependencies
├── scanner_research_plan_*.md   # Original research plan
└── .gitignore                    # Ignore data/, models/, cache/
```

---

## 🔧 Configuration

### Main Config: `scanner/config/scanner_config.yaml`
- Thresholds (RVOL, % change)
- Filter settings (price, volume, float)
- Alert priorities and channels
- Scoring weights

### Data Sources: `scanner/config/data_sources.yaml`
- API keys (Finnhub)
- Scraper rate limits
- Ollama endpoint configuration

### Models: `scanner/config/models_config.yaml`
- ML hyperparameters
- Model paths (versioned)
- Training schedules

---

## 📈 Development Phases

### **Phase 1: Scraper Infrastructure (Week 1)** ✅
- Build 5 web scrapers (Barchart, Finviz, Yahoo, MarketWatch)
- Test for 1 week (verify no rate limits)
- Set up SQLite database and caching

### **Phase 2: Core Scanner (Week 2)** 🔄
- Alpaca WebSocket real-time ingestion
- Signal calculations (RVOL, patterns, VWAP)
- Basic rule engine + Streamlit dashboard

### **Phase 3: AI/ML Scoring (Week 3)** ⏳
- Ollama integration (sentiment, reasoning)
- ML alert scorer (RandomForest)
- Priority routing + Telegram bot

### **Phase 4: Nightly Pipeline + Multi-Asset (Week 4)** ⏳
- Automated model retraining
- Threshold optimization
- Options overlay + crypto scanner

### **Phase 5: Wingman Integration (Week 5)** ⏳
- Journal recording integration
- Rules checking
- Production hardening

---

## 🧪 Testing

### Run Unit Tests
```bash
cd RnD/Scanner
pytest scanner/tests/
```

### Test Scrapers (48-hour burn-in)
```bash
python -m scanner.scrapers.test_all
```

### Backtest Alert Quality
```bash
python -m scanner.backtest.replay --start-date 2025-10-01 --end-date 2025-10-29
```

---

## 📊 Data Sources (All FREE)

### Real-Time APIs
- **Alpaca WebSocket:** Stock quotes/bars (unlimited)
- **Binance WebSocket:** Crypto (BTC, ETH, SOL)
- **Finnhub API:** News, fundamentals (60 calls/min)

### Web Scraping
- **Barchart:** Options chains (volume, OI, IV)
- **Finviz:** Fundamentals, screener, movers
- **Yahoo Finance:** Stats page (fallback)
- **MarketWatch:** Earnings calendar
- **SEC Edgar:** Official filings

### Local AI/ML
- **Ollama** (192.168.10.52:11434): qwen2.5:32b, deepseek-r1:8b, llama3.1:8b
- **scikit-learn:** RandomForest alert scorer
- **LightGBM:** Forward return predictor
- **Prophet:** Volume baseline forecaster

---

## 🎯 Success Criteria (Exit RnD)

Before promoting to production, must achieve:

- [ ] **Reliability:** 2+ weeks of 100% uptime
- [ ] **Data Quality:** 95%+ tickers have valid fundamentals
- [ ] **Alert Quality:** <20% false positive rate (user feedback)
- [ ] **ML Performance:** >55% win rate on backtests (30-min forward returns)
- [ ] **Scraping Stability:** Zero rate limit errors for 1 month
- [ ] **Integration:** Wingman alerts auto-populate Journal correctly
- [ ] **Performance:** Alert latency <10 seconds from setup forming
- [ ] **Documentation:** Complete user guide and troubleshooting docs

---

## 📝 Daily Logs

Keep development journal in `docs/dev_log.md`:
- What worked / what didn't
- Scraper issues (rate limits, HTML changes)
- Alert quality observations
- Model performance notes
- Ideas for improvement

---

## 🐛 Known Issues / Limitations

*(Update as we discover issues)*

- **Scrapers:** Subject to website HTML changes
- **Ollama:** 20-30 second inference for qwen2.5:32b (acceptable for batch)
- **Options Data:** 5-min cache means slight delay vs real-time
- **Finviz:** Rate limiting requires careful delays

---

## 🔮 Future Enhancements (Post-MVP)

Ideas for v2.0 (after production promotion):
- Dark pool print detection
- Sector rotation signals
- Institutional ownership tracking
- Auto-chart snapshots (save images of setups)
- Voice alerts (TTS for critical setups)
- Mobile app (React Native)
- Multi-timeframe analysis (swing + intraday)

---

## 📚 Documentation

See `docs/` folder for detailed guides:
- `data_sources.md` - Complete API/scraping documentation
- `alert_system.md` - Priority routing and deduplication logic
- `ml_models.md` - Feature engineering and model architecture
- `wingman_integration.md` - How scanner connects to Wingman

---

## 🤝 Contributing (Internal Notes)

Since this is RnD:
- **Break things:** It's okay, that's what RnD is for
- **Document learnings:** Update dev_log.md daily
- **Measure everything:** Log all alerts, track outcomes
- **Fail fast:** If approach isn't working, pivot quickly
- **No production dependencies:** Keep completely isolated

---

## 📞 Support / Questions

For Claude (AI assistant):
- Load this README when working on scanner
- Check `scanner_research_plan_*.md` for original research
- Follow RnD workflow (don't move to production prematurely)
- Update todos via TodoWrite tool

For Daryll (User):
- Review daily logs in `docs/dev_log.md`
- Check alert quality via Streamlit dashboard
- Provide feedback on false positives/negatives
- Decide when to promote to production

---

## 🎓 References

- Original Research Plan: `scanner_research_plan_2025-10-29_03-20.md`
- Wingman System: `../../Toolbox/INSTRUCTIONS/Domains/`
- Existing Scrapers: `../../Scraper/`
- Journal System: `../../Journal/`

---

**Remember:** This is RnD. Experiment boldly, document thoroughly, promote carefully.

**Project Status:** Week 1 - Scraper Infrastructure Build 🔨
