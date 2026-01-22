import csv
import os
from datetime import datetime

class TradingLogger:
    def __init__(self, filename="trade_logs.csv"):
        self.filepath = filename
        self.headers = [
            "timestamp", "symbol", "price", "sentiment_score",
            "rsi", "sma_50", "action", "reasoning"
        ]
        # Create file with headers if it doesn't exist
        if not os.path.exists(self.filepath):
            with open(self.filepath, mode='w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=self.headers)
                writer.writeheader()

    def log_decision(self, symbol, price, score, rsi, sma, action, reasoning):
        """Append a new decision row to the CSV."""
        with open(self.filepath, mode='a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.headers)
            writer.writerow({
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "symbol": symbol,
                "price": round(float(price), 2),
                "sentiment_score": score,
                "rsi": round(float(rsi), 2),
                "sma_50": round(float(sma), 2),
                "action": action,
                "reasoning": reasoning.replace("\n", " ") # Keep CSV clean
            })
