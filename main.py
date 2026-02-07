
import time
from config import INTERVAL, CANDLE_LIMIT, SCAN_EVERY_SECONDS, TOP_VOLUME_COINS, STATE_FILE, REQUEST_DELAY_SECONDS
from modules.logger import setup_logger
from modules.binance_client import get_futures_client
from modules.volume_filter import get_top_volume_symbols
from modules.market_data import fetch_klines
from modules.indicators import add_ema
from modules.signals import detect_ema_cross
from modules.notifier_telegram import send_telegram
from modules.state_store import load_state, save_state, already_alerted, mark_alerted

def format_message(symbol, signal, candle_time, price, interval):
    emoji = "🟢" if signal == "BULLISH" else "🔴"
    direction = "Bullish EMA Cross" if signal == "BULLISH" else "Bearish EMA Cross"
    return (
        f"{emoji} <b>{direction}</b>\n"
        f"<b>Symbol:</b> {symbol}\n"
        f"<b>Timeframe:</b> {interval}\n"
        f"<b>Close Price:</b> {price}\n"
        f"<b>Candle Close:</b> {candle_time}"
    )

def run():
    logger = setup_logger()
    client = get_futures_client()
    state = load_state(STATE_FILE)
    logger.info("EMA bot started ✅")

    while True:
        try:
            symbols = get_top_volume_symbols(client, top_n=TOP_VOLUME_COINS)
            logger.info(f"Scanning {len(symbols)} top volume symbols...")

            for symbol in symbols:
                logger.info("Scanning: " + symbol)
                df = fetch_klines(client, symbol, interval=INTERVAL, limit=CANDLE_LIMIT)
                if df.empty:
                    continue
                df = add_ema(df)
                signal = detect_ema_cross(df)

                if signal:
                    candle_time = str(df.iloc[-2]["close_time"])
                    price = df.iloc[-2]["close"]

                    if not already_alerted(state, symbol, signal, candle_time):
                        msg = format_message(symbol, signal, candle_time, price, INTERVAL)
                        send_telegram(msg)
                        mark_alerted(state, symbol, signal, candle_time)
                        save_state(STATE_FILE, state)
                        logger.info(f"ALERT: {signal} on {symbol}")

        except Exception as e:
            logger.error(f"Loop error: {e}")

        logger.info(f"Sleeping {SCAN_EVERY_SECONDS}s...")
        time.sleep(SCAN_EVERY_SECONDS)

if __name__ == "__main__":
    run()

