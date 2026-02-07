import time
from config import REQUEST_DELAY_SECONDS, MAX_RETRIES, RETRY_DELAY, TOP_VOLUME_COINS
def get_top_volume_symbols(client, top_n=TOP_VOLUME_COINS):
    """
    Fetch top-volume USDT-M futures symbols with retries if 403 happens.
    """
    for attempt in range(MAX_RETRIES):
        try:
            tickers = client.futures_ticker(symbol=None)
            usdt_perps = [
                {"symbol": t["symbol"], "quoteVolume": float(t.get("quoteVolume", 0))}
                for t in tickers if t["symbol"].endswith("USDT")
            ]
            usdt_perps.sort(key=lambda x: x["quoteVolume"], reverse=True)
            return [x["symbol"] for x in usdt_perps[:top_n]]
        except Exception as e:
            print(f"Volume fetch error ({attempt+1}/{MAX_RETRIES}): {e}")
            time.sleep(RETRY_DELAY)
    return []
