from alpaca.data.historical import StockHistoricalDataClient, CryptoHistoricalDataClient
from alpaca.data.requests import StockBarsRequest, CryptoBarsRequest
from alpaca.data.timeframe import TimeFrame
from datetime import datetime, timedelta
import pandas as pd

class DataIngestor:
    def __init__(self, api_key, api_secret):
        self.stock_client = StockHistoricalDataClient(api_key, api_secret)
        self.crypto_client = CryptoHistoricalDataClient(api_key, api_secret)

    def get_180d_history(self, symbol, asset_type):
        """Fetch 180 days of daily candles."""
        start_date = datetime.now() - timedelta(days=180)

        if asset_type == 'stock':
            request = StockBarsRequest(
                symbol_or_symbols=symbol,
                timeframe=TimeFrame.Day,
                start=start_date
            )
            data = self.stock_client.get_stock_bars(request)
        else:
            request = CryptoBarsRequest(
                symbol_or_symbols=symbol,
                timeframe=TimeFrame.Day,
                start=start_date
            )
            data = self.crypto_client.get_crypto_bars(request)

        # Convert to DataFrame and handle MultiIndex
        df = data.df
        if isinstance(df.index, pd.MultiIndex):
            df = df.xs(symbol)
        return df
