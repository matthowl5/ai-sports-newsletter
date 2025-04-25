import os

from dotenv import load_dotenv

import time
from openai import OpenAI


# Load .env variables
load_dotenv()

# You don't need to pass api_key if it's in the environment
client = OpenAI()

SUMMARY_PROMPT_TEMPLATE = (
    "Summarize the following sports news article in 2–3 clear, objective, and professional-sounding sentences, "
    "suitable for inclusion in an email newsletter.\n\nArticle:\n{article_text}"
)

def summarize_article_text(article_text):
    try:
        prompt = SUMMARY_PROMPT_TEMPLATE.format(article_text=article_text[:3000])
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes sports articles."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=200
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"Error during summarization: {e}")
        return "Summary unavailable due to an API error."

def summarize_articles(articles):
    summarized = []
    for i, article in enumerate(articles, start=1):
        print(f"Summarizing article {i}: {article['title']}")
        summary = summarize_article_text(article["text"])
        summarized.append({
            "title": article["title"],
            "url": article["url"],
            "summary": summary
        })
        time.sleep(1)
    return summarized

if __name__ == "__main__":
    sample_articles = [
        {
            "title": "Sample Title",
            "url": "https://example.com/article",
            "text": "This is a long article about an exciting sports event that needs to be summarized concisely."
        }
    ]
    summaries = summarize_articles(sample_articles)
    for summary in summaries:
        print("\n--- Summary ---")
        print(f"Title: {summary['title']}")
        print(f"URL: {summary['url']}")
        print(f"Summary: {summary['summary']}")

