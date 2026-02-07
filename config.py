import os
from dotenv import load_dotenv

load_dotenv()

BINANCE_API_KEY = os.getenv("BINANCE_API_KEY", "")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET", "")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# Bot settings
INTERVAL = "15m"
CANDLE_LIMIT = 500

SCAN_EVERY_SECONDS = 900  # 15 min safe scan
TOP_VOLUME_COINS = 100     # top 100 coins by volume

STATE_FILE = "data/state.json"

# Rate limit safety
REQUEST_DELAY_SECONDS = 0.5  # ~2 req/sec
MAX_RETRIES = 5              # retry API calls if 403 / timeout
RETRY_DELAY = 5               # seconds between retries
