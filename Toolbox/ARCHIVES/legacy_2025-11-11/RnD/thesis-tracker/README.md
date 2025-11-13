# Investment Thesis Tracker

A professional web-based dashboard for analyzing, comparing, and tracking investment theses across your portfolio.

## Overview

This tool provides a visual interface to explore investment theses stored as markdown files. It parses thesis documents (both stocks and crypto), extracts structured data, and presents comprehensive analytics through an interactive web dashboard.

## Features

### 📊 Portfolio Analytics Panel (Right Side)
Real-time visualizations showing your portfolio's health:

1. **Score Composition** - Stacked bar chart showing the breakdown of what drives conviction scores for your top 8 holdings
2. **Risk vs Conviction** - Scatter plot mapping portfolio positioning across risk/reward quadrants
3. **Conviction Distribution** - Three gauges showing portfolio strength (High/Medium/Speculative breakdown)
4. **Theme Exposure** - Horizontal bar chart analyzing diversification across investment themes
5. **Portfolio Stats** - Key aggregate metrics (avg scores, fundamentals, technicals, risk)

### 📋 Main Content Area (Left Side)
Interactive thesis browsing:

- **Search & Filters** - Find theses by ticker, name, theme, asset class, or score range
- **Multiple Views:**
  - Grid View: Visual cards with key metrics
  - Table View: Sortable columns for detailed comparison
  - Comparison View: Side-by-side analysis with radar chart (up to 4 tickers)
- **Detail Modal** - Click any thesis to view full markdown content with quick stats

## Architecture

### Data Flow

```
Markdown Files (Tickers/Stocks/Thesis/*.md)
          ↓
   Python Parser (scripts/processing/parse_thesis_files.py)
          ↓
   JSON Data (data/thesis_data.json)
          ↓
   JavaScript App (js/*.js)
          ↓
   Interactive Dashboard
```

### File Structure

```
thesis-tracker/
├── index.html                    # Main application entry point
├── css/
│   └── styles.css               # All styling (layout, widgets, components)
├── js/
│   ├── app.js                   # Main application controller
│   ├── data-loader.js           # Fetches and manages thesis data
│   ├── filters.js               # Search and filter logic
│   ├── sorters.js               # Table sorting logic
│   ├── utils/
│   │   ├── analytics.js         # Derived metrics & portfolio calculations
│   │   └── formatters.js        # Display formatting utilities
│   └── components/
│       ├── stock-card.js        # Stock thesis card renderer
│       ├── crypto-card.js       # Crypto thesis card renderer
│       ├── comparison.js        # Comparison view logic
│       └── visualizations.js    # Chart.js widget renderers
├── data/
│   └── thesis_data.json         # Generated JSON from parser
└── scripts/
    └── processing/
        └── parse_thesis_files.py  # Markdown → JSON parser
```

## How It Works

### 1. Data Extraction (Python Parser)

**Location:** `scripts/processing/parse_thesis_files.py`

The parser reads markdown thesis files and extracts:

**For Stocks:**
- Ticker symbol
- Last updated date
- Investment theme
- Scorecard (5 dimensions: Fundamentals, Technicals, Management, Risk, Sentiment)
- Investment pillars
- Catalysts
- Key metrics
- Risks

**For Crypto:**
- Ticker symbol (with name-to-symbol mapping)
- Core investment idea
- On-chain metrics
- Bull/bear triggers
- Technology assessment
- Risks

**Features:**
- Multi-encoding support (UTF-8, UTF-8-sig, Latin-1, CP1252)
- Smart ticker extraction
- Structured JSON output with metadata

**Run parser:**
```bash
python scripts/processing/parse_thesis_files.py
```

### 2. Analytics Engine (JavaScript)

**Location:** `js/utils/analytics.js`

Calculates derived metrics and portfolio-level statistics:

- **Conviction categorization** - High (75+), Medium (50-74), Speculative (<50)
- **Score normalization** - Converts raw scores to percentages
- **Theme extraction** - Keyword matching for AI, Healthcare, Semiconductors, Consumer, Energy, etc.
- **Portfolio strength** - Weighted average based on conviction distribution
- **Thesis health** - Freshness tracking (outdated >90 days, stale >60 days)
- **Risk-reward mapping** - 2D positioning analysis

### 3. Visualization Layer (Chart.js)

**Location:** `js/components/visualizations.js`

Renders 5 interactive widgets:

1. **Fundamentals Quality (Stacked Bar)** - Shows composition of top 8 stocks
2. **Risk-Reward Scatter** - Plots all stocks on conviction vs risk axes
3. **Conviction Gauges (SVG)** - Three circular progress indicators with percentages
4. **Portfolio Gaps (Horizontal Bar)** - Theme concentration analysis
5. **Portfolio Stats (Grid)** - Aggregate metrics display

**Chart Configuration:**
- Dark theme colors
- Responsive sizing
- Interactive tooltips
- Legend customization

## Development Session Summary

### Phase 1: Initial Setup (Messages 1-3)
- Created markdown parser for stock and crypto theses
- Fixed Unicode encoding issues (Windows CP1252 vs UTF-8)
- Implemented crypto ticker mapping (Solana → SOL)
- Generated initial JSON data (17 theses: 16 stocks + 1 crypto)
- Built basic web app with grid/table/comparison views

### Phase 2: Widget Enhancement (Messages 4-7)
- User feedback: "widgets aren't telling us much"
- Designed 6 new analytics widgets with derived metrics
- Created `analytics.js` helper module (350+ lines)
- Built `visualizations.js` with Chart.js integrations (550+ lines)
- Replaced basic widgets with data-rich visualizations

### Phase 3: Layout Iteration (Messages 8-11)
- Removed Action Items widget per user request
- Attempted 2x2 grid layout (didn't work well)
- Multiple sizing iterations (too big → way too small → just right)
- Canvas heights: 250px → 180px → 120px → 90px → final: 140px/120px

### Phase 4: Final Polish (Messages 12-13)
- Fixed broken HTML structure (widgets outside main-layout)
- Redesigned to side-by-side layout:
  - Left 60%: Thesis list, filters, comparison
  - Right 420px fixed: Analytics panel
- Added "Portfolio Analytics" header
- Enhanced visual styling:
  - Glassmorphism with backdrop blur
  - Purple accent borders with hover states
  - Custom scrollbar styling
  - Professional shadows and transitions
  - Improved typography and spacing

## Usage

1. **Update Data:**
   ```bash
   python scripts/processing/parse_thesis_files.py
   ```

2. **Open Dashboard:**
   - Open `index.html` in a web browser
   - Or use a local server:
     ```bash
     python -m http.server 8000
     ```
     Then visit: `http://localhost:8000`

3. **Interact:**
   - Browse theses in grid/table view
   - Use filters to narrow results
   - Click cards to view full thesis details
   - Select up to 4 tickers for side-by-side comparison
   - Monitor portfolio analytics in real-time

## Technical Details

### Dependencies
- **Chart.js 4.4.0** - Data visualization library
- **Marked 11.0.0** - Markdown rendering in modal
- **Vanilla JavaScript** - No framework dependencies
- **Python 3.x** - For data parsing

### Browser Compatibility
- Modern browsers with ES6+ support
- CSS Grid and Flexbox
- CSS Custom Properties (variables)
- Backdrop filter support recommended

### Data Format

The parser generates JSON with this structure:

```json
{
  "last_generated": "2025-10-28T15:44:19.039596Z",
  "tickers": [
    {
      "ticker": "AAPL",
      "asset_class": "stock",
      "last_updated": "2025-10-01",
      "file_path": "Tickers\\Stocks\\Thesis\\2025-10-01_AAPL.md",
      "theme": "Consumer AI + Services flywheel, Vision Pro ecosystem",
      "scores": {
        "fundamentals": 32,
        "fundamentals_max": 40,
        "technicals": 18,
        "technicals_max": 25,
        "management": 14,
        "management_max": 15,
        "risk": 7,
        "risk_max": 10,
        "sentiment": 7,
        "sentiment_max": 10,
        "total": 78,
        "total_max": 100
      },
      "pillars": [...],
      "catalysts": [...],
      "metrics": [...],
      "risks": [...]
    }
  ]
}
```

## Current Limitations

- No persistence (changes to filters/views not saved)
- No export functionality (CSV, PDF)
- Single portfolio view (no multi-portfolio support)
- Static data (requires manual parser re-run)
- No historical tracking (snapshot only)

## Future Enhancements

- Real-time data refresh
- Portfolio performance tracking
- Advanced filters (custom score ranges, multi-theme selection)
- Export capabilities
- Historical thesis comparison
- Alert system for outdated theses
- Mobile responsive design
- Dark/light theme toggle

## Styling Philosophy

The design uses a **dark glassmorphism** aesthetic with:
- Deep navy background gradients
- Semi-transparent panels with backdrop blur
- Purple accent colors (#6366f1)
- Subtle shadows and borders
- Smooth transitions and hover effects
- Professional typography with letter-spacing

## Performance

- Lightweight (no heavy frameworks)
- Fast load times (<1s for 17 theses)
- Efficient rendering (virtual DOM not needed for dataset size)
- Optimized chart configurations
- Minimal external dependencies

---

**Created:** October 2025
**Version:** 1.0
**Parser Success Rate:** 100% (17/17 theses)
**Total Widgets:** 5 analytics + 3 view modes
**Lines of Code:** ~2,000+ (JS + CSS + HTML)
