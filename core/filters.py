import pandas as pd

# Strategy toggles
USE_MEAN_REVERSION = True
USE_MOMENTUM = True
USE_VOLATILITY_BREAKOUT = True

def safe_item(x):
    try:
        return x.item() if hasattr(x, "item") else x
    except:
        return x

def filter_stock(df, symbol):
    if df is None or len(df) < 2:
        return None

    latest = df.iloc[-1]
    prev = df.iloc[-2]

    try:
        rsi = safe_item(latest['rsi'])
        macd = safe_item(latest['macd'])
        macd_signal = safe_item(latest['macd_signal'])
        close = safe_item(latest['Close'])
        prev_close = safe_item(prev['Close'])
        bb_upper = safe_item(latest['bb_upper'])
        bb_lower = safe_item(latest['bb_lower'])
        atr = safe_item(latest['atr'])

        signals = []

        # === Strategy 1: Mean Reversion ===
        if USE_MEAN_REVERSION:
            if rsi < 30 and close > prev_close:
                signals.append("Reversion (RSI < 30 and bounce)")

        # === Strategy 2: Momentum ===
        if USE_MOMENTUM:
            if rsi > 50 and macd > macd_signal:
                signals.append("Momentum (RSI > 50 & MACD crossover)")

        # === Strategy 3: Volatility Breakout ===
        if USE_VOLATILITY_BREAKOUT:
            bb_range = bb_upper - bb_lower
            price_change = close - prev_close
            strong_candle = price_change > 0.01 * prev_close
            breakout = close > bb_upper
            atr_avg = df['atr'].rolling(14).mean().iloc[-1]
            volatility_ok = atr > 1.2 * atr_avg

            if rsi > 60 and macd > macd_signal and strong_candle and breakout and volatility_ok:
                signals.append("Momentum Breakout + Volatility")


        # Optional: Comment out to disable
        # if close < bb_lower:
        #     signals.append("Below BB")
        # elif close > bb_upper:
        #     signals.append("Above BB")

        if signals:
            return {
                "Symbol": symbol,
                "Close": close,
                "RSI": rsi,
                "MACD": macd,
                "Signal": ", ".join(signals),
                "executed": True
            }
        else:
            return None

    except Exception as e:
        print(f"[SKIP] {symbol} - error: {e}")
        return None

