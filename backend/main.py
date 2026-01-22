# backend/main.py
import os
import time
from dotenv import load_dotenv
from core.data_ingestor import DataIngestor
from core.news_engine import NewsEngine
from core.notifier import Notifier
from core.logger import TradingLogger

load_dotenv()

def run_money_maker():
    print("💰 AI Trading Assistant: Money Maker Mode Active")

    # Initialize Services
    ingestor = DataIngestor(os.getenv("ALPACA_API_KEY"), os.getenv("ALPACA_API_SECRET"))
    engine = NewsEngine()
    notifier = Notifier()

    # Your Focus Assets
    watch_list = [
        ("GLD", "stock"),
        ("NVDA", "stock"),
        ("BTC/USD", "crypto"),
        ("ETH/USD", "crypto")
    ]

    while True:
        print(f"\n--- 🔎 Scanning Markets: {time.strftime('%H:%M:%S')} ---")

        for symbol, atype in watch_list:
            try:
                # 1. QUANT: Fetch Math Signals (SMA 50 and RSI)
                df = ingestor.get_bars(symbol, atype)
                latest_tech = ingestor.get_signals(df)

                price = latest_tech['close']
                sma_50 = latest_tech['SMA_50']
                rsi = latest_tech['RSI']

                # 2. QUAL: Fetch AI Sentiment
                headlines = engine.get_headlines(symbol)
                sentiment_score = engine.analyze_sentiment(headlines, symbol)

                # LOGGING: Capture all data points for review
                # Extract reasoning from the raw AI output we saw in the test
                            reasoning = "N/A"
                            if hasattr(engine, 'last_reasoning'): # Assuming you store it in the engine
                                reasoning = engine.last_reasoning

                            # Determine the status for the log
                            action_status = "HOLD"
                            if sentiment_score and sentiment_score > 0.4 and price > sma_50:
                                action_status = "BUY_ALERT"
                            elif sentiment_score and sentiment_score < -0.4 and price < sma_50:
                                action_status = "SELL_ALERT"

                            # 📝 LOG EVERYTHING
                            trade_log.log_decision(
                                symbol, price, sentiment_score,
                                rsi, sma_50, action_status, reasoning
                            )

                # 3. CONFLUENCE: The Entry Logic
                # Bullish: Trend is UP (Price > SMA), Not Overbought (RSI < 70), News is GOOD (> 0.4)
                if sentiment_score and sentiment_score > 0.4:
                    if price > sma_50 and rsi < 70:
                        print(f"✅ {symbol}: STRONG BUY SIGNAL")
                        notifier.send_alert(symbol, price, sentiment_score, "🔥 STRONG BUY (Trend + News)")
                    else:
                        print(f"⚖️ {symbol}: Bullish news, but math says WAIT (Price < SMA or RSI too high)")

                # Bearish: Trend is DOWN (Price < SMA), News is BAD (< -0.4)
                elif sentiment_score and sentiment_score < -0.4:
                    if price < sma_50:
                        print(f"⚠️ {symbol}: STRONG SELL SIGNAL")
                        notifier.send_alert(symbol, price, sentiment_score, "📉 STRONG SELL (Trend + News)")

                else:
                    print(f"😴 {symbol}: No significant action (Score: {sentiment_score})")

            except Exception as e:
                print(f"❌ Error on {symbol}: {e}")

        # Cycle frequency: Every 1 hour to capture intraday swings without hitting rate limits
        print("\nCycle complete. Next scan in 60 minutes...")
        time.sleep(3600)

if __name__ == "__main__":
    run_money_maker()
