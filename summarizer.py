import os
import openai
from dotenv import load_dotenv
import time

# Load OpenAI API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# GPT model to use
MODEL = "gpt-3.5-turbo"

# Prompt template
SUMMARY_PROMPT_TEMPLATE = (
    "Summarize the following sports news article in 2–3 clear, objective, and professional-sounding sentences, "
    "suitable for inclusion in an email newsletter.\n\nArticle:\n{article_text}"
)

def summarize_article_text(article_text):
    try:
        prompt = SUMMARY_PROMPT_TEMPLATE.format(article_text=article_text[:3000])  # Truncate if needed
        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes sports articles."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=200
        )
        summary = response['choices'][0]['message']['content'].strip()
        return summary

    except openai.error.OpenAIError as e:
        print(f"Error summarizing article: {e}")
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
        time.sleep(1)  # Be kind to the API
    return summarized

if __name__ == "__main__":
    # Example usage (replace with actual article list from fetch_news.py)
    sample_articles = [
        {
            "title": "Sample Title",
            "url": "https://example.com/article",
            "text": "This is the full article text. It can be quite long and needs to be summarized into a few concise sentences."
        }
    ]

    summaries = summarize_articles(sample_articles)
    for item in summaries:
        print("\n--- Summary ---")
        print(f"Title: {item['title']}")
        print(f"URL: {item['url']}")
        print(f"Summary: {item['summary']}")
