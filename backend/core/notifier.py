import requests
import os

class Notifier:
    def __init__(self):
        self.token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")

    def send_alert(self, asset, price, score):
        # Professional formatting for your phone
        emoji = "🚀" if score > 0.2 else "📉" if score < -0.2 else "⚖️"
        message = (
            f"{emoji} **AI MARKET ALERT** {emoji}\n\n"
            f"Asset: {asset}\n"
            f"Price: ${price}\n"
            f"AI Sentiment: {score}\n\n"
            f"Action: {'Consider BUY' if score > 0.4 else 'Consider SELL' if score < -0.4 else 'Monitor'}"
        )
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        requests.post(url, data={"chat_id": self.chat_id, "text": message, "parse_mode": "Markdown"})
