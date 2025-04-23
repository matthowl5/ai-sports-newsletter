import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GUARDIAN_API_KEY")

def get_recent_guardian_sports_news():
    now = datetime.utcnow()
    yesterday = now - timedelta(days=1)

    url = (
        "https://content.guardianapis.com/search?"
        f"section=sport&"
        f"from-date={yesterday.date()}&"
        f"to-date={now.date()}&"
        f"order-by=newest&"
        f"api-key={API_KEY}&"
        f"show-fields=trailText,body,short-url"
    )

    response = requests.get(url)
    data = response.json()

    if response.status_code != 200 or "response" not in data:
        print("Failed to fetch news:", data.get("message", "Unknown error"))
        return []

    articles = data["response"]["results"]
    if not articles:
        print("No recent sports articles found.")
        return []

    cleaned_articles = []
    for i, article in enumerate(articles[:5], start=1):
        title = article["webTitle"]
        url = article["webUrl"]
        body_html = article.get("fields", {}).get("body", "")

        # Clean the HTML body into plain text
        soup = BeautifulSoup(body_html, "html.parser")
        full_text = soup.get_text()

        cleaned_articles.append({
            "title": title,
            "url": url,
            "text": full_text
        })

    return cleaned_articles

if __name__ == "__main__":
    articles = get_recent_guardian_sports_news()
    for i, article in enumerate(articles, start=1):
        print(f"{i}. {article['title']}")
        print(f"URL: {article['url']}")
        print(f"Text preview: {article['text'][:300]}...\n")
