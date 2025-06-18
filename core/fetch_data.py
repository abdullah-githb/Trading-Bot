import yfinance as yf
import os
import pandas as pd

DATA_DIR = "data/raw_data"

def fetch_stock_data(symbol, period="6mo", interval="1d"):
    """
    Fetch historical stock data from Yahoo Finance and save it to CSV.
    """
    try:
        df = yf.download(symbol, period=period, interval=interval)
        if df.empty:
            print(f"[SKIP] No data for {symbol}")
            return None

        # Ensure data directory exists
        os.makedirs(DATA_DIR, exist_ok=True)

        # Save data
        df.to_csv(f"{DATA_DIR}/{symbol}.csv")
        print(f"[DONE] Saved data for {symbol}")
        return df

    except Exception as e:
        print(f"[ERROR] Could not fetch {symbol}: {e}")
        return None

