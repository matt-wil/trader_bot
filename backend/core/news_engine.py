import os
import requests
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser # NEW IMPORT

class NewsEngine:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        self.news_api_key = os.getenv("NEWS_API_KEY")

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=self.api_key,
            temperature=0.1
        )

    def get_headlines(self, query):
        exclude_terms = "NOT (election OR sports OR entertainment OR lifestyle)"

            # Force keywords that imply market movement
            refined_query = f"({query} AND (market OR price OR inflation OR Fed OR 'interest rates')) {exclude_terms}"

            url = (
                f"https://newsapi.org/v2/everything?q={refined_query}"
                f"&language=en"
                f"&category=business" # Strictly filter for business sources
                f"&sortBy=relevance"
                f"&pageSize=10&apiKey={self.news_api_key}"
            )
        response = requests.get(url).json()
        return [a['title'] for a in response.get('articles', [])]

    def analyze_sentiment(self, headlines, asset):
        if not headlines:
            return None # No news, no tip

        # This prompt forces the AI to act as a gatekeeper
        prompt = ChatPromptTemplate.from_template("""
            Role: Senior Financial Intelligence Officer.
            Asset: {asset}
            Data: {headlines}

            Task:
            1. Filter: If a headline is NOT directly related to the price or market status of {asset}, discard it.
            2. Analyze: For the remaining relevant headlines, provide a collective sentiment score.

            Output format:
            - If NO headlines are relevant: Output 'IRRELEVANT'.
            - If headlines ARE relevant: Output ONLY the float number between -1.0 and 1.0.
        """)

        chain = prompt | self.llm | StrOutputParser()
        result = chain.invoke({"asset": asset, "headlines": headlines})

        # LOGIC: If the AI says IRRELEVANT, we stop immediately
        if "IRRELEVANT" in result.upper():
            return None

        try:
            return float(result.strip())
        except ValueError:
            return None
