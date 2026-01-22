# backend/tests/test_backtester_logic.py
import pandas as pd
import numpy as np
from core.backtester import Backtester

def test_logic():
    # Create a fake dataset where price goes up 1% every day
    data = {
        'close': [100, 101, 102, 103, 104, 105],
        'SMA_50': [90, 90, 90, 90, 90, 90],  # Always below price
        'RSI': [30, 30, 30, 30, 30, 30]      # Always oversold
    }
    df = pd.DataFrame(data)

    # Fake sentiment that turns positive on day 3
    sentiment = [0, 0, 0.8, 0.8, 0.8, 0.8]

    tester = Backtester(initial_capital=1000)
    results = tester.run_simulation(df, sentiment)

    print(f"Simulation Results: {results}")
    # If the bot is working, it should show a profit starting from day 3.

test_logic()
