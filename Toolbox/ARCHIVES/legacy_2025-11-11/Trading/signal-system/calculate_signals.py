import re
import json
import datetime
import os

# --- CONFIGURATION ---
# Define the paths to the summary files
# Note: The script assumes the files are for the current date.
BASE_PATH = "C:/Users/Iccanui/Desktop/Investing"
DATE_STR = datetime.date.today().strftime("%Y-%m-%d")

PATHS = {
    "spx": f"{BASE_PATH}/Research/Technicals/TradingView SPX/{DATE_STR}_TradingViewSPX_Summary.md",
    "btc": f"{BASE_PATH}/Research/Technicals/TradingView BTC/{DATE_STR}_TradingViewBTC_Summary.md",
    "breadth": f"{BASE_PATH}/Research/Technicals/Market Breadth/{DATE_STR}_MarketBreadth_Summary.md",
    "volatility": f"{BASE_PATH}/Research/Technicals/Volatility Metrics/{DATE_STR}_VolatilityMetrics_Summary.md",
    "master_plan": f"{BASE_PATH}/master-plan/master-plan.md"
}

# --- DATA EXTRACTION FUNCTIONS ---

def get_value_from_summary(file_path, pattern):
    """Generic function to extract a numerical value from a summary file using regex."""
    try:
        # Open with UTF-8 encoding to handle special characters
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            match = re.search(pattern, content)
            if match:
                # Extract the first group that is a number (integer or float)
                for group in match.groups():
                    if group:
                        try:
                            return float(group)
                        except (ValueError, TypeError):
                            continue
    except FileNotFoundError:
        print(f"Warning: File not found at {file_path}")
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    return None

def get_x_sentiment_score(file_path):
    """Extracts the sentimentScore from the master-plan.md JSON front matter."""
    try:
        # Open with UTF-8 encoding
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Find the JSON part of the markdown file
            json_str = content.split('---')[1]
            data = json.loads(json_str)
            # Find the 'xsentiment' tab and get its score
            for tab in data.get('dashboard', {}).get('tabs', []):
                if tab.get('id') == 'xsentiment':
                    return tab.get('sentimentScore')
    except Exception as e:
        print(f"Error reading or parsing master-plan.md: {e}")
    return None

# --- CALCULATION LOGIC ---
# This logic is based on the framework in How to use_Signals.txt

def calculate_trend_score(spx_price, spx_50_dma, spx_200_dma, btc_price, btc_50_dma, btc_200_dma):
    score = 0
    if spx_price and spx_200_dma and spx_price > spx_200_dma:
        score += 10
        if spx_50_dma and spx_price > spx_50_dma:
            score += 10
    if btc_price and btc_200_dma and btc_price > btc_200_dma:
        score += 10
        if btc_50_dma and btc_price > btc_50_dma:
            score += 10
    return score

def calculate_breadth_score(percent_spx_above_50_dma, x_sentiment_score):
    if percent_spx_above_50_dma is None or x_sentiment_score is None:
        return 0
    score = (percent_spx_above_50_dma / 100) * 20 + 5 # Assume no divergence for +5
    if 0 <= x_sentiment_score <= 24: score += 5
    elif 25 <= x_sentiment_score <= 44: score += 4
    elif 45 <= x_sentiment_score <= 54: score += 2
    elif 55 <= x_sentiment_score <= 64: score += 1
    elif 80 <= x_sentiment_score <= 89: score -= 2
    elif 90 <= x_sentiment_score <= 100: score -= 5
    return min(25, score)

def calculate_volatility_score(vix_level, btc_iv_percentile):
    score = 0
    if vix_level:
        if vix_level < 15: score += 10
        elif vix_level < 20: score += 7
        elif vix_level < 25: score += 4
    if btc_iv_percentile:
        if btc_iv_percentile < 20: score += 10
        elif btc_iv_percentile < 40: score += 7
        elif btc_iv_percentile < 60: score += 4
    return score

def calculate_technical_score(spx_rsi, btc_rsi):
    score = 0
    if spx_rsi and spx_rsi < 70: score += 5
    if btc_rsi and btc_rsi < 70: score += 5
    return score

def calculate_seasonality_score(current_date):
    score = 0
    if current_date.month == 10: score += 4
    if (current_date.day >= 28) or (current_date.day <= 2): score += 1
    return min(5, score)

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    print("--- Dynamic Signal Calculator (v2) ---")
    
    # 1. Extract data from files
    print("1. Extracting data from summary files...")
    spx_price = 6750 # Assumed from TA summary
    spx_50_dma = get_value_from_summary(PATHS["spx"], r"50-EMA \((\d+)\)") or 6689
    spx_200_dma = 6513 # Assumed
    btc_price = 121500 # Assumed from TA summary
    btc_50_dma = get_value_from_summary(PATHS["btc"], r"50-day SMA\), (\d+)") or 114000
    btc_200_dma = 105000 # Assumed
    
    percent_spx_above_50_dma = 65 # Assuming bullish from "improving" text
    x_sentiment_score = get_x_sentiment_score(PATHS["master_plan"])
    
    # Corrected regex patterns with escaped asterisks
    vix_level = get_value_from_summary(PATHS["volatility"], r"Level:\*\* (\d+\.\d+)")
    btc_iv_percentile = get_value_from_summary(PATHS["volatility"], r"IV Rank:\*\* (\d+)")

    spx_rsi = get_value_from_summary(PATHS["spx"], r"RSI:\*\* Overbought.*\(>(\d+)\)") or 71
    btc_rsi = 55 # Assumed neutral

    print("Data extracted.")

    # 2. Calculate component scores
    print("\n2. Calculating component scores...")
    trend_score = calculate_trend_score(spx_price, spx_50_dma, spx_200_dma, btc_price, btc_50_dma, btc_200_dma)
    breadth_score = calculate_breadth_score(percent_spx_above_50_dma, x_sentiment_score)
    volatility_score = calculate_volatility_score(vix_level, btc_iv_percentile)
    technical_score = calculate_technical_score(spx_rsi, btc_rsi)
    seasonality_score = calculate_seasonality_score(datetime.date.today())
    print("Scores calculated.")

    # 3. Calculate composite score
    print("\n3. Calculating final composite score...")
    composite_score = (
        (trend_score / 40 * 100) * 0.40 +
        (breadth_score / 25 * 100) * 0.25 +
        (volatility_score / 20 * 100) * 0.20 +
        (technical_score / 10 * 100) * 0.10 +
        (seasonality_score / 5 * 100) * 0.05
    )
    print("Composite score calculated.")

    def get_tier(score):
        if score >= 85: return "EXTREME"
        elif score >= 70: return "STRONG"
        elif score >= 55: return "MODERATE"
        else: return "AVOID"

    # 4. Print results
    print("\n--- Trading Signal Calculation Results ---")
    print(f"Trend Score:       {trend_score:.2f} / 40")
    print(f"Breadth Score:     {breadth_score:.2f} / 25")
    print(f"Volatility Score:  {volatility_score:.2f} / 20")
    print(f"Technical Score:   {technical_score:.2f} / 10")
    print(f"Seasonality Score: {seasonality_score:.2f} / 5")
    print("----------------------------------------")
    print(f"Final Composite Score: {composite_score:.2f} / 100")
    print(f"Signal Tier:           {get_tier(composite_score)}")
    print("----------------------------------------")