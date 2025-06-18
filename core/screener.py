from core.logger import log_to_existing_journal
import pandas as pd
from core.fetch_data import fetch_stock_data
from core.indicators import add_indicators
from core.filters import filter_stock

def run_screener():
    # Load your Shariah-compliant stock list
    symbols = pd.read_csv("config/shariah_stocks.csv")["Symbol"].tolist()

    results = []

    for symbol in symbols:
        print(f"[INFO] Checking {symbol}...")
        df = fetch_stock_data(symbol, period="1y", interval="1d")
        if df is None or df.empty:
            continue

        df = add_indicators(df)
        signal = filter_stock(df, symbol)

        if signal:
            results.append(signal)

    # Save results to output CSV
    if results:
        df_results = pd.DataFrame(results)
        df_results.to_csv("output/screened_stocks.csv", index=False)
        print(f"\n✅ Saved {len(results)} signals to output/screened_stocks.csv")
        log_to_existing_journal(results)
        print("📒 Signals logged to your journal sheet.")
    else:
        print("\n⚠️ No trade signals found today.")

if __name__ == "__main__":
    run_screener()

