# backend/main.py
import os
import time
from pathlib import Path
from dotenv import load_dotenv

# Import your core modules
from core.data_ingestor import DataIngestor
from core.news_engine import NewsEngine
from core.notifier import Notifier

# 1. Setup Environment
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

def run_assistant():
    print("🤖 AI Trading Assistant Starting...")

    # 2. Initialize Core Services
    ingestor = DataIngestor(
        os.getenv("ALPACA_API_KEY"),
        os.getenv("ALPACA_API_SECRET")
    )
    engine = NewsEngine()
    notifier = Notifier()

    # Define your watch list: (Symbol, Type for Alpaca)
    watch_list = [
        ("GLD", "stock"),      # Gold ETF
        ("BTC/USD", "crypto"), # Bitcoin
        ("NVDA", "stock")      # High-volatility Stock
    ]

    while True:
        print(f"\n--- Starting Analysis Cycle: {time.strftime('%H:%M:%S')} ---")

        for symbol, asset_type in watch_list:
            try:
                # STEP A: Get Current Market Price
                price = ingestor.get_latest_price(symbol, asset_type)
                if not price:
                    print(f"⚠️ Skipping {symbol}: No price data available.")
                    continue

                # STEP B: Get Filtered News & AI Sentiment
                # The 'engine' now handles Boolean filtering and AI Pruning
                print(f"🔍 Analyzing {symbol}...")
                headlines = engine.get_headlines(symbol)
                sentiment_score = engine.analyze_sentiment(headlines, symbol)

                # STEP C: Signal Logic & Notification
                # If sentiment_score is None, it means the news was filtered as IRRELEVANT
                if sentiment_score is not None:
                    print(f"✅ {symbol} Score: {sentiment_score}")

                    # Only notify if the signal is strong enough to warrant a 'Tip'
                    if abs(sentiment_score) >= 0.4:
                        notifier.send_alert(symbol, price, sentiment_score)
                        print(f"📱 Notification sent for {symbol}!")
                    else:
                        print(f"⚖️ Signal for {symbol} ({sentiment_score}) is too weak for alert.")
                else:
                    print(f"🔇 No relevant news found for {symbol}.")

            except Exception as e:
                print(f"❌ Error processing {symbol}: {e}")

        # 3. Frequency Management
        # 15-minute wait ensures you stay within free-tier API limits
        print("\nCycle complete. Sleeping for 15 minutes...")
        time.sleep(900)

if __name__ == "__main__":
    run_assistant()
