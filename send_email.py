import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart # Use MIMEMultipart for HTML emails
from dotenv import load_dotenv

# Import the functions from your other scripts
from fetch_news import get_recent_guardian_sports_news
from summarizer import summarize_articles

# Load email credentials and recipient from .env
load_dotenv()

# --- Configuration ---
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")  # Gmail app password or service-specific password
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL") # Or a comma-separated string "email1@example.com,email2@example.com"
SMTP_SERVER = "smtp.gmail.com" # Example for Gmail
SMTP_PORT = 465 # Example port for SSL (Gmail)
EMAIL_SUBJECT = "Your Daily AI Sports News Roundup"

# --- Main Execution ---

def send_newsletter():
    """Fetches news, summarizes, and sends the email newsletter."""
    print("--- Starting AI-Powered Newsletter Generation ---")

    # 1. Fetch Articles
    print("Fetching recent sports news...")
    try:
        fetched_articles = get_recent_guardian_sports_news()
        if not fetched_articles:
            print("No new articles fetched. Exiting.")
            return
        print(f"Successfully fetched {len(fetched_articles)} articles.")
    except Exception as e:
        print(f"Error fetching articles: {e}")
        # Optionally send an error email or log the error
        return

    # 2. Summarize Articles
    print("Summarizing articles...")
    try:
        # Pass the fetched articles to the summarizer
        summarized_data = summarize_articles(fetched_articles)
        if not summarized_data:
            print("No summaries generated. Exiting.")
            return
        print(f"Successfully generated {len(summarized_data)} summaries.")
    except Exception as e:
        print(f"Error summarizing articles: {e}")
        # Optionally send an error email or log the error
        return

    # 3. Format and Send Email
    print("Formatting and sending email...")
    try:
        # Create the email message container
        msg = MIMEMultipart("alternative")
        msg["Subject"] = EMAIL_SUBJECT
        msg["From"] = SENDER_EMAIL
        msg["To"] = RECIPIENT_EMAIL

        # Create the HTML version of the email
        html_body = """
        <html>
        <head>
            <style>
                body {{ font-family: sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 20px auto; padding: 20px; border: 1px solid #ddd; border-radius: 8px; }}
                h1 {{ color: #0056b3; text-align: center; margin-bottom: 20px; }}
                h2 {{ color: #007bff; margin-top: 20px; margin-bottom: 5px; font-size: 1.2em; }}
                .article {{ margin-bottom: 20px; padding-bottom: 15px; border-bottom: 1px solid #eee; }}
                .article:last-child {{ border-bottom: none; }}
                a {{ color: #007bff; text-decoration: none; }}
                a:hover {{ text-decoration: underline; }}
                .summary {{ font-style: italic; color: #555; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Your Daily AI Sports News Roundup</h1>
        """

        if not summarized_data:
            html_body += "<p>No news found to summarize today.</p>"
        else:
            for article in summarized_data:
                html_body += f"""
                <div class="article">
                    <h2><a href="{article.get('url', '#')}" target="_blank">{article.get('title', 'No Title Available')}</a></h2>
                    <p class="summary">{article.get('summary', 'Summary unavailable.')}</p>
                    <p><a href="{article.get('url', '#')}" target="_blank">Read the full article</a></p>
                </div>
                """

        html_body += """
            </div>
        </body>
        </html>
        """

        # Attach the HTML part to the message
        part2 = MIMEText(html_body, "html")
        msg.attach(part2)

        # Send the email
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SENDER_EMAIL, APP_PASSWORD)
            server.send_message(msg, from_addr=SENDER_EMAIL, to_addrs=RECIPIENT_EMAIL.split(',')) # Handles multiple recipients if comma-separated

        print("✅ Newsletter sent successfully!")

    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        # Optionally send an error email or log the error

    print("--- Newsletter Generation Complete ---")

# Run the newsletter generation process
if __name__ == "__main__":
    # Add checks for required environment variables before proceeding
    if not SENDER_EMAIL or not APP_PASSWORD or not RECIPIENT_EMAIL:
        print("Error: Please ensure SENDER_EMAIL, APP_PASSWORD, and RECIPIENT_EMAIL are set in your .env file.")
    else:
        send_newsletter()