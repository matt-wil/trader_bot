# backend/run_full_backtest.py
import os
from core.data_ingestor import DataIngestor
from core.backtester import Backtester
import numpy as np

def run_full_report():
    ingestor = DataIngestor(os.getenv("ALPACA_API_KEY"), os.getenv("ALPACA_API_SECRET"))
    tester = Backtester(initial_capital=10000)

    assets = [
        ("GLD", "stock"), ("NVDA", "stock"),
        ("BTC/USD", "crypto"), ("ETH/USD", "crypto")
    ]

    print(f"{'ASSET':<10} | {'RETURN':<10} | {'WIN RATE':<10} | {'DRAWDOWN':<10}")
    print("-" * 50)

    for symbol, atype in assets:
        df = ingestor.get_180d_history(symbol, atype)
        df = ingestor.get_signals(df) # SMA/RSI logic from Phase 4

        # Simulate sentiment (In real life, you'd use historic news data)
        # We generate random 'Bullish' signals to test the math logic
        simulated_sentiment = np.random.uniform(0, 1, len(df))

        results = tester.run_simulation(df, simulated_sentiment)

        print(f"{symbol:<10} | {results['Total Return']:<10} | "
              f"{results['Win Rate']:<10} | {results['Max Drawdown']:<10}")

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    run_full_report()
