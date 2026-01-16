import os
from pathlib import Path
from dotenv import load_dotenv
from core.news_engine import NewsEngine

env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

def test_news_sentiment():
    print("🚀 Initializing Gemini News Engine...")

    google_key = os.getenv("GOOGLE_API_KEY")
    news_key = os.getenv("NEWS_API_KEY")

    if not google_key or not news_key:
        print(f"❌ ERROR: Missing API Keys in .env")
        print(f"Checking path: {env_path.absolute()}")
        return

    engine = NewsEngine()

    asset = "Gold"
    print(f"Fetching latest headlines for: {asset}...")
    headlines = engine.get_headlines(asset)

    if not headlines:
        print("⚠️ No headlines found. Check your NewsAPI key or query.")
        return

    print(f"✅ Found {len(headlines)} headlines.")
    print(f"Top Headline: {headlines[0]}")

    print("Analyzing sentiment with Gemini...")
    score = engine.analyze_sentiment(headlines, asset)

    print(f"--- Final Report ---")
    print(f"Asset: {asset}")
    print(f"AI Sentiment Score: {score}")

    if isinstance(score, float):
        print("✅ SUCCESS: Gemini returned a valid numerical score.")
    else:
        print("❌ FAILED: Gemini did not return a float.")

if __name__ == "__main__":
    test_news_sentiment()
