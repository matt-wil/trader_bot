import pandas as pd
import pandas_ta as ta
from alpaca.data.historical import StockHistoricalDataClient, CryptoHistoricalDataClient
from alpaca.data.requests import StockBarsRequest, CryptoBarsRequest
from alpaca.data.timeframe import TimeFrame
from datetime import datetime, timedelta

class DataIngestor:
    def __init__(self, api_key, api_secret):
        self.stock_client = StockHistoricalDataClient(api_key, api_secret)
        self.crypto_client = CryptoHistoricalDataClient(api_key, api_secret)

    def get_bars(self, symbol, asset_type, days=180):
        """Fetch historical data for backtesting or live monitoring."""
        start_time = datetime.now() - timedelta(days=days)

        if asset_type == 'stock':
            request = StockBarsRequest(symbol_or_symbols=[symbol], timeframe=TimeFrame.Day, start=start_time)
            bars = self.stock_client.get_stock_bars(request).df
        else:
            # Note: Crypto symbols like BTC/USD or ETH/USD
            request = CryptoBarsRequest(symbol_or_symbols=[symbol], timeframe=TimeFrame.Day, start=start_time)
            bars = self.crypto_client.get_crypto_bars(request).df

        # Alpaca returns a MultiIndex; we must isolate the symbol
        if isinstance(bars.index, pd.MultiIndex):
            bars = bars.xs(symbol)

        return bars
