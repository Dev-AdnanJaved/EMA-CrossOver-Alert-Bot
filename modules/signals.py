def detect_ema_cross(df):
    """
    Detect EMA50/200 cross on last closed candle.
    """
    if len(df) < 210:
        return None
    prev = df.iloc[-3]
    curr = df.iloc[-2]

    if prev.ema_fast < prev.ema_slow and curr.ema_fast > curr.ema_slow:
        return "BULLISH"
    if prev.ema_fast > prev.ema_slow and curr.ema_fast < curr.ema_slow:
        return "BEARISH"
    return None
