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
        ("ETH/USD", "crypto"), # Ethereum
        ("NVDA", "stock")      # High-volatility Stock
    ]


    while True:
        for symbol, asset_type in watch_list:
            try:
                # 1. Fetch historical data & Technical Signals
                # Use the new get_history method we added to DataIngestor
                history_df = ingestor.get_history(symbol, asset_type, days=100)
                latest_metrics = ingestor.get_signals(history_df)

                current_price = latest_metrics['close']
                sma_50 = latest_metrics['SMA_50']
                rsi = latest_metrics['RSI']

                # 2. Get AI News Sentiment
                headlines = engine.get_headlines(symbol)
                sentiment_score = engine.analyze_sentiment(headlines, symbol)

                # 3. CONVICTION LOGIC (The Money Maker)
                # We only notify if News AND Math agree
                is_bullish_math = current_price > sma_50 and rsi < 70
                is_bullish_news = sentiment_score is not None and sentiment_score > 0.4

                if is_bullish_math and is_bullish_news:
                    # High conviction tip!
                    notifier.send_alert(
                        symbol,
                        current_price,
                        sentiment_score,
                        f"🔥 STRONG BUY: Trend is UP and News is BULLISH.\n(RSI: {rsi:.2f})"
                    )

                # (Optional) Add Bearish logic here as well
                elif current_price < sma_50 and sentiment_score is not None and sentiment_score < -0.4:
                    notifier.send_alert(
                        symbol,
                        current_price,
                        sentiment_score,
                        "⚠️ STRONG SELL: Trend is DOWN and News is BEARISH."
                    )

            except Exception as e:
                print(f"Error analyzing {symbol}: {e}")

        time.sleep(900) # Sleep for 15 mins to stay in free tier

if __name__ == "__main__":
    run_assistant()
