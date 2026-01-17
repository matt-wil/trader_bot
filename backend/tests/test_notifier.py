# backend/tests/test_notifier.py
import os
from pathlib import Path
from dotenv import load_dotenv
from core.notifier import Notifier

# Load environment
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

def test_telegram():
    print("🚀 Sending test notification...")
    bot = Notifier()

    # Simulate a fake trading tip
    bot.send_alert(
        asset="GOLD (TEST)",
        price="2650.45",
        score=0.85
    )
    print("✅ Check your phone!")

if __name__ == "__main__":
    test_telegram()
