import os
from dotenv import load_dotenv
from core.data_ingestor import DataIngestor

load_dotenv()

def test_ingestor():
    ingestor = DataIngestor(os.getenv("ALPACA_API_KEY"), os.getenv("ALPACA_API_SECRET"))

    gold_price = ingestor.get_latest_price("GLD", "stock")
    print(f"Gold (GLD) Price: {gold_price}")

    btc_price = ingestor.get_latest_price("BTC/USD", "crypto")
    print(f"Bitcoin Price: {btc_price}")

if __name__ == "__main__":
    test_ingestor()
