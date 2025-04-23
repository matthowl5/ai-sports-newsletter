import requests
import os
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

API_KEY = os.getenv("NEWS_API_KEY")

def get_sports_news():
    url = (
        "https://newsapi.org/v2/top-headlines?"
        "category=sports&"
        "language=en&"
        f"apiKey={API_KEY}"
    )

    response = requests.get(url)
    data = response.json()

    articles = data.get("articles", [])
    if not articles:
        print("No sports articles found.")
        return

    for i, article in enumerate(articles[:5], start=1):  # Show top 5
        print(f"{i}. {article['title']}")
        print(f"   {article['url']}\n")

if __name__ == "__main__":
    get_sports_news()
