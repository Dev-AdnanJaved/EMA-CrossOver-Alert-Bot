from binance.client import Client

API_KEY = "YOUR_TESTNET_KEY"
API_SECRET = "YOUR_TESTNET_SECRET"

client = Client(API_KEY, API_SECRET, testnet=True)
client.FUTURES_URL = "https://testnet.binancefuture.com"

tickers = client.futures_ticker(symbol=None)
print(tickers[:5])