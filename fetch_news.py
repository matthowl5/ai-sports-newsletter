import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
# All this is imported libraries that help with the script.
# Load environment variables
load_dotenv()
API_KEY = os.getenv("GUARDIAN_API_KEY")
# Define function to get recent news articles
def get_recent_guardian_sports_news():
    now = datetime.utcnow()
    yesterday = now - timedelta(days=1) 
# Ensured news comes from last day
# Next: building url for the API request from Guardian
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
# Sending request and checking for errors
    if response.status_code != 200 or "response" not in data:
        print("Failed to fetch news:", data.get("message", "Unknown error"))
# Extracting articles from API response
    articles = data["response"]["results"]
    if not articles:
        print("No recent sports articles found.")
        return []
# Extracting specific details from articles
    cleaned_articles = []
    for i, article in enumerate(articles[:5], start=1):
        title = article["webTitle"]
        url = article["webUrl"]
        body_html = article.get("fields", {}).get("body", "")

        # Cleaning the HTML body into plain text with BeautifulSoup
        soup = BeautifulSoup(body_html, "html.parser")
        full_text = soup.get_text()
# Creating dictionary with cleaned articles
        cleaned_articles.append({
            "title": title,
            "url": url,
            "text": full_text
        })

    return cleaned_articles
# Basic script to show fetched articles
if __name__ == "__main__":
    articles = get_recent_guardian_sports_news()
    for i, article in enumerate(articles, start=1):
        print(f"{i}. {article['title']}")
        print(f"URL: {article['url']}")
        print(f"Text preview: {article['text'][:300]}...\n")
