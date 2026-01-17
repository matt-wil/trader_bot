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

    def get_history(self, symbol, asset_type='stock', days=100):
        """Fetch historical OHLCV data for technical analysis."""
        start_time = datetime.now() - timedelta(days=days)

        if asset_type == 'stock':
            request = StockBarsRequest(symbol_or_symbols=[symbol], timeframe=TimeFrame.Day, start=start_time)
            bars = self.stock_client.get_stock_bars(request).df
        else:
            request = CryptoBarsRequest(symbol_or_symbols=[symbol], timeframe=TimeFrame.Day, start=start_time)
            bars = self.crypto_client.get_crypto_bars(request).df

        # Ensure the index is a flat symbol-based index for pandas-ta
        if isinstance(bars.index, pd.MultiIndex):
            bars = bars.xs(symbol)

        return bars

    def get_signals(self, df):
        """Calculate technical indicators."""
        # (1) SMA 50: Long-term trend. Price > SMA50 is Bullish
        df['SMA_50'] = ta.sma(df['close'], length=50)

        # (2) RSI: Momentum. < 30 is Oversold (Buy), > 70 is Overbought (Sell)
        df['RSI'] = ta.rsi(df['close'], length=14)

        return df.iloc[-1] # Return only the most recent data row
