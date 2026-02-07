import pandas as pd
import time
from config import REQUEST_DELAY_SECONDS, MAX_RETRIES, RETRY_DELAY

def fetch_klines(client, symbol, interval="15m", limit=500):
    """
    Fetch candlestick data with retries if 403 or other errors occur.
    """
    for attempt in range(MAX_RETRIES):
        try:
            klines = client.futures_klines(symbol=symbol, interval=interval, limit=limit)
            df = pd.DataFrame(klines, columns=[
                "time","open","high","low","close","volume",
                "close_time","qav","num_trades",
                "taker_base_vol","taker_quote_vol","ignore"
            ])
            df["close"] = df["close"].astype(float)
            df["time"] = pd.to_datetime(df["time"], unit="ms")
            df["close_time"] = pd.to_datetime(df["close_time"], unit="ms")
            time.sleep(REQUEST_DELAY_SECONDS)
            return df
        except Exception as e:
            print(f"Klines fetch error for {symbol} ({attempt+1}/{MAX_RETRIES}): {e}")
            time.sleep(RETRY_DELAY)
    return pd.DataFrame()
