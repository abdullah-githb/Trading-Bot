import pandas as pd
import ta  # technical analysis library

def add_indicators(df):
    """
    Adds RSI, MACD, Bollinger Bands, and ATR to the DataFrame.
    """
    df = df.copy()

    # === Price Series ===
    close = df['Close'].squeeze().astype(float)
    high = df['High'].squeeze().astype(float)
    low = df['Low'].squeeze().astype(float)

    # === RSI ===
    rsi = ta.momentum.RSIIndicator(close=close, window=14)
    df['rsi'] = rsi.rsi()

    # === MACD ===
    macd = ta.trend.MACD(close=close)
    df['macd'] = macd.macd()
    df['macd_signal'] = macd.macd_signal()

    # === Bollinger Bands ===
    bb = ta.volatility.BollingerBands(close=close, window=20, window_dev=2)
    df['bb_upper'] = bb.bollinger_hband()
    df['bb_lower'] = bb.bollinger_lband()

    # === ATR (Average True Range) ===
    atr = ta.volatility.AverageTrueRange(high=high, low=low, close=close, window=14)
    df['atr'] = atr.average_true_range()

    return df

