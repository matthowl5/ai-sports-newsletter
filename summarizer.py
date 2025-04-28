import os
import time
from dotenv import load_dotenv
from openai import OpenAI

# Import the function from your fetch_news script
from fetch_news import get_recent_guardian_sports_news

# Load .env variables
load_dotenv()

# Initialize OpenAI Client (assumes OPENAI_API_KEY is in the environment)
client = OpenAI()

SUMMARY_PROMPT_TEMPLATE = (
    "Summarize the following sports news article in 2–3 clear, objective, and professional-sounding sentences, "
    "suitable for inclusion in an email newsletter.\n\nArticle:\n{article_text}"
)

def summarize_article_text(article_text):
    """Summarizes a single piece of text using the OpenAI API."""
    # Limit text length to avoid excessive token usage/cost
    # Adjust the limit (e.g., 4000 chars ~ 1000 tokens) based on model and needs
    max_chars = 4000
    truncated_text = article_text[:max_chars]

    try:
        prompt = SUMMARY_PROMPT_TEMPLATE.format(article_text=truncated_text)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", # Or consider newer/cheaper models if appropriate
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes sports articles concisely and professionally for a newsletter."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5, # Lower temperature for more factual summaries
            max_tokens=150  # Adjust based on desired summary length (2-3 sentences ~ 60-100 tokens usually)
        )
        summary = response.choices[0].message.content.strip()
        # Basic check for empty or placeholder summaries
        if not summary or "summary is unavailable" in summary.lower():
             return "Could not generate a meaningful summary for this article."
        return summary

    except Exception as e:
        print(f"Error during OpenAI API call: {e}")
        return "Summary unavailable due to an API error."

def summarize_articles(articles):
    """Takes a list of article dictionaries (with 'text') and adds a 'summary' field."""
    summarized = []
    # Ensure 'articles' is a list before iterating
    if not isinstance(articles, list):
        print("Error: Input 'articles' is not a list.")
        return []

    for i, article in enumerate(articles, start=1):
        # Defensive check for necessary keys
        if not all(k in article for k in ['title', 'url', 'text']):
            print(f"Skipping article {i}: missing 'title', 'url', or 'text'. Article data: {article}")
            continue

        print(f"Summarizing article {i}/{len(articles)}: {article.get('title', 'No Title Provided')}")
        summary = summarize_article_text(article.get("text", "")) # Pass empty string if 'text' is missing
        summarized.append({
            "title": article.get("title", "No Title"),
            "url": article.get("url", "#"), # Use '#' as fallback URL
            "summary": summary
        })
        # Consider adjusting sleep time based on API rate limits and number of articles
        time.sleep(1) # Pause between API calls
    return summarized

if __name__ == "__main__":
    print("Fetching recent sports news...")
    # Fetch real articles using the function from fetch_news.py
    fetched_articles = get_recent_guardian_sports_news()

    if not fetched_articles:
        print("No articles were fetched. Exiting.")
    else:
        print(f"Fetched {len(fetched_articles)} articles. Starting summarization...")
        # Summarize the fetched articles
        summaries = summarize_articles(fetched_articles)

        print("\n--- Generated Summaries ---")
        if not summaries:
            print("No summaries were generated.")
        else:
            for summary_data in summaries:
                print(f"\nTitle: {summary_data['title']}")
                print(f"URL: {summary_data['url']}")
                print(f"Summary: {summary_data['summary']}")
        print("\n--------------------------")
        print("Summarization process complete.")
