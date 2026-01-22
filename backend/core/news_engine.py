import os
import requests
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

class NewsEngine:
    def __init__(self):
        """Initialize with Gemini 2.5 Flash for optimal free-tier performance."""
        self.api_key = os.getenv("GOOGLE_API_KEY")
        self.news_api_key = os.getenv("NEWS_API_KEY")

        # Using gemini-2.5-flash: stable, high rate limits, and zero cost.
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=self.api_key,
            temperature=0.1,  # Low temperature ensures more consistent numerical scoring.
            max_retries=2
        )

    def get_headlines(self, asset_symbol):
        """
        Fetch asset-specific news using advanced Boolean operators to filter noise.
        """
        # Asset-specific search tuning to ignore general political/sports noise.
        queries = {
            "NVDA": "(NVIDIA OR 'NVDA') AND (AI OR GPU OR Blackwell OR Earnings OR 'Jensen Huang')",
            "BTC/USD": "('Bitcoin' OR 'BTC') AND (Halving OR ETF OR 'Spot Price' OR Adoption)",
            "ETH/USD": "('Ethereum' OR 'ETH') AND (Staking OR 'Gas Fees' OR 'Layer 2' OR Vitalik)",
            "GLD": "('Gold' OR 'GLD') AND (Inflation OR 'Federal Reserve' OR 'Central Bank' OR 'Interest Rates')"
        }

        # Fallback query if the symbol isn't in our specialized list.
        base_query = queries.get(asset_symbol, f"{asset_symbol} AND (Market OR Price OR Finance)")

        # NewsAPI Everything endpoint: English only, sorted by relevance.
        url = (
            f"https://newsapi.org/v2/everything?q={base_query}"
            f"&language=en"
            f"&sortBy=relevancy"
            f"&pageSize=10"
            f"&apiKey={self.news_api_key}"
        )

        try:
            response = requests.get(url).json()
            articles = response.get('articles', [])
            # Return a list of titles; if no news found, return an empty list.
            return [a['title'] for a in articles] if articles else []
        except Exception as e:
            print(f"❌ NewsAPI Error: {e}")
            return []

    def analyze_sentiment(self, headlines, asset):
        if not headlines:
            return None

        # REFINED PROMPT: Focus on reasoning to avoid false negatives
        prompt = ChatPromptTemplate.from_template("""
            Role: Senior Equity Analyst at a Global Hedge Fund.
            Task: Evaluate how these headlines for {asset} will impact investor behavior and price action.

            Headlines: {headlines}

            Logic Steps:
            1. Identify catalysts (Product launches, earnings, macro shifts, AI demand).
            2. Evaluate impact (Bullish, Bearish, or Neutral).
            3. If headlines are purely noise (politics, sports, general fluff), score 0.0.

            Output ONLY a JSON-style response with these keys:
            - "reasoning": (1 sentence explanation)
            - "score": (float between -1.0 and 1.0)
        """)

        # We remove StrOutputParser here to handle the potential JSON
        chain = prompt | self.llm
        response = chain.invoke({"asset": asset, "headlines": headlines})

        # Extract the score using a simpler method to handle Gemini's raw text
        content = response.content
        print(f"DEBUG - AI Reasoning: {content}") # See why it's scoring what it's scoring

        # Basic extraction for safety
        import re
        scores = re.findall(r"[-+]?\d*\.\d+|\d+", content)
        if scores:
            val = float(scores[-1]) # Usually the last number is the score
            return val if val != 0.0 else None # Return None if truly irrelevant (0.0)
        return None
