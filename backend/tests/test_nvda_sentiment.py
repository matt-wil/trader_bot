# backend/tests/test_nvda_sentiment.py
import os
from pathlib import Path
from dotenv import load_dotenv
from core.news_engine import NewsEngine

# Load environment variables
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

def test_nvda_earnings_logic():
    print("🚀 Testing NewsEngine with NVIDIA Catalyst Check...")

    engine = NewsEngine()
    asset = "NVDA"

    # 1. Fetch live headlines specifically for NVDA
    print(f"Fetching latest headlines for {asset}...")
    headlines = engine.get_headlines(asset)

    if not headlines:
        print("⚠️ No headlines found. Ensure your NewsAPI key is active.")
        return

    print(f"✅ Found {len(headlines)} headlines.")
    for idx, h in enumerate(headlines[:3]):
        print(f"   {idx+1}. {h}")

    # 2. Run Sentiment Analysis
    print("\nAnalyzing sentiment with Gemini 2.5 Flash...")
    score = engine.analyze_sentiment(headlines, asset)

    # 3. Validation
    print("-" * 30)
    if score is None:
        print("Result: IRRELEVANT (No market-moving NVIDIA news found)")
    else:
        print(f"Asset: {asset}")
        print(f"Sentiment Score: {score}")

        # Decision logic check
        if score > 0.4:
            print("Action: Strong Bullish Signal (Potential AI/Earnings catalyst)")
        elif score < -0.4:
            print("Action: Strong Bearish Signal (Potential Overvaluation/Market risk)")
        else:
            print("Action: Neutral (Monitor for technical breakout)")

if __name__ == "__main__":
    test_nvda_earnings_logic()
