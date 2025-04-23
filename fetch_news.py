import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GUARDIAN_API_KEY")

def get_recent_guardian_sports_news():
    # Set time range for the last 24 hours
    now = datetime.utcnow()
    yesterday = now - timedelta(days=1)
    from_date = yesterday.strftime("%Y-%m-%dT%H:%M:%SZ")
    to_date = now.strftime("%Y-%m-%dT%H:%M:%SZ")

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
        return

    articles = data["response"]["results"]
    if not articles:
        print("No recent sports articles found.")
        return

    print(f"⚽ Sports News from The Guardian (last 24 hours):\n")
    for i, article in enumerate(articles[:5], start=1):
        print(f"{i}. {article['webTitle']}")
        print(f"   {article['webUrl']}\n")

if __name__ == "__main__":
    get_recent_guardian_sports_news()
