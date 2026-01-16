from alpaca.data.historical import StockHistoricalDataClient, CryptoHistoricalDataClient
from alpaca.data.requests import StockBarsRequest, CryptoBarsRequest
from alpaca.data.timeframe import TimeFrame
from datetime import datetime, timedelta

class DataIngestor:
    def __init__(self, api_key: str, api_secret: str):
        self.stock_client = StockHistoricalDataClient(api_key, api_secret)
        self.crypto_client = CryptoHistoricalDataClient(api_key, api_secret)

    def get_latest_price(self, symbol, asset_type='stock'):
        end_time = datetime.now()
        start_time = end_time - timedelta(days=1)

        try:
            if asset_type == 'stock':
                request_params = StockBarsRequest(
                    symbol_or_symbols=[symbol],
                    timeframe=TimeFrame.Minute,
                    start=start_time
                )
                bars = self.stock_client.get_stock_bars(request_params)
            elif asset_type == 'crypto':
                request_params = CryptoBarsRequest(
                    symbol_or_symbols=[symbol],
                    timeframe=TimeFrame.Minute,
                    start=start_time
                )
                bars = self.crypto_client.get_crypto_bars(request_params)
            else:
                print(f"Unsupported asset type: {asset_type}")
                return None

            data = bars.data
            if symbol in data and len(data[symbol]) > 0:
                return data[symbol][-1].close
            return None

        except Exception as e:
            print(f"Error fetching {symbol}: {e}")
            return None
