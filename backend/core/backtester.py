# backend/core/backtester.py
import pandas as pd
import numpy as np

class Backtester:
    def __init__(self, initial_capital=10000):
        self.capital = initial_capital

    def run_simulation(self, df, sentiment_scores):
        """
        df: DataFrame from DataIngestor with 'SMA_50' and 'RSI'
        sentiment_scores: A list of fake/historic scores for testing logic
        """
        df = df.copy()
        df['sentiment'] = sentiment_scores

        # Define the Signal: 1 is BUY, 0 is WAIT
        df['signal'] = np.where(
            (df['close'] > df['SMA_50']) &
            (df['RSI'] < 70) &
            (df['sentiment'] > 0.5),
            1, 0
        )

        # Calculate Returns
        df['market_returns'] = df['close'].pct_change()
        df['strategy_returns'] = df['signal'].shift(1) * df['market_returns']

        # Calculate Performance Metrics
        total_return = (1 + df['strategy_returns'].fillna(0)).prod() - 1
        win_rate = len(df[df['strategy_returns'] > 0]) / len(df[df['signal'] == 1])

        return {
            "Total Return": f"{total_return:.2%}",
            "Win Rate": f"{win_rate:.2%}",
            "Max Drawdown": f"{self.calculate_drawdown(df):.2%}"
        }

    def calculate_drawdown(self, df):
        cumulative = (1 + df['strategy_returns'].fillna(0)).cumprod()
        peak = cumulative.cummax()
        drawdown = (cumulative - peak) / peak
        return drawdown.min()
