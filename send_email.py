import os
import smtplib
import datetime # Import datetime to get the current year for the footer
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart # Use MIMEMultipart for HTML emails
from dotenv import load_dotenv

# Import the functions from your other scripts
# Ensure these files (fetch_news.py and summarizer.py) exist and
# the functions do what's expected.
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
# Using the more engaging subject line
EMAIL_SUBJECT = "🌸 Your Daily Dose of Sports Sunshine ☀️"

# --- Main Execution ---

def send_newsletter():
    """Fetches REAL news, summarizes it, and sends the stylish email newsletter."""
    print("--- Starting AI-Powered Newsletter Generation ---")

    # 1. Fetch Articles (Using your actual function)
    print("Fetching recent sports news...")
    try:
        # Assuming get_recent_guardian_sports_news returns a list of dicts
        # where each dict has at least 'webTitle' and 'webUrl' keys.
        fetched_articles = get_recent_guardian_sports_news()
        if not fetched_articles:
            print("No new articles fetched. Exiting.")
            return
        print(f"Successfully fetched {len(fetched_articles)} articles.")
    except Exception as e:
        print(f"Error fetching articles: {e}")
        # Optionally send an error email or log the error
        return

    # 2. Summarize Articles (Using your actual function)
    print("Summarizing articles...")
    try:
        # Pass the fetched articles to the summarizer.
        # Assuming summarize_articles returns a list of dicts,
        # where each dict has 'title', 'url', and 'summary' keys.
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

        # --- Create the Beautiful HTML Version (Copied from previous refinement) ---
        # Get the current year dynamically
        current_year = datetime.date.today().year

        html_body = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="preconnect" href="https://fonts.googleapis.com">
            <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
            <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
            <style>
                /* Reset basic styles */
                body, h1, h2, h3, p, a {{ margin: 0; padding: 0; font-family: 'Poppins', sans-serif, Helvetica, Arial; box-sizing: border-box; }}

                body {{
                    width: 100% !important;
                    height: 100%;
                    -webkit-text-size-adjust: 100%;
                    -ms-text-size-adjust: 100%;
                    background-color: #fdf6f9; /* Very light pastel pink background */
                    line-height: 1.6;
                    color: #555; /* Soft dark grey for text */
                }}

                .email-container {{
                    max-width: 600px;
                    margin: 20px auto;
                    padding: 30px;
                    background-color: #ffffff; /* White container */
                    border-radius: 15px; /* Rounded corners */
                    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05); /* Subtle shadow */
                    border: 1px solid #f0e4e8; /* Soft border */
                }}

                .header {{
                    text-align: center;
                    margin-bottom: 30px;
                    padding-bottom: 20px;
                    border-bottom: 1px dashed #e8d8de; /* Dashed pastel separator */
                }}

                .header h1 {{
                    font-size: 28px;
                    font-weight: 600;
                    color: #e58cba; /* Muted rose pink */
                    margin-bottom: 5px;
                }}

                 .header .subtitle {{
                    font-size: 14px;
                    color: #aaa;
                    font-weight: 300;
                 }}

                .article {{
                    margin-bottom: 30px;
                    padding-bottom: 30px;
                    border-bottom: 1px dashed #e8d8de; /* Dashed pastel separator */
                }}

                .article:last-child {{
                    margin-bottom: 0;
                    padding-bottom: 0;
                    border-bottom: none; /* No border for the last article */
                }}

                .article h2 {{
                    font-size: 20px; /* Slightly smaller than main header */
                    font-weight: 600;
                    color: #6a8dcf; /* Soft blue/lavender */
                    margin-bottom: 10px;
                    line-height: 1.3;
                    /* Title is NOT a link */
                }}

                .summary {{
                    font-size: 15px;
                    color: #666; /* Slightly darker grey for summary */
                    margin-bottom: 20px;
                    font-weight: 300; /* Lighter weight for summary */
                }}

                .button {{
                    display: inline-block; /* Button behavior */
                    background-color: #87ceeb; /* Pastel sky blue */
                    color: #ffffff !important; /* White text - important to override default link color */
                    padding: 10px 20px;
                    text-decoration: none; /* No underline */
                    border-radius: 25px; /* Pill shape */
                    font-weight: 400;
                    font-size: 14px;
                    text-align: center;
                    transition: background-color 0.3s ease;
                }}

                .button:hover {{
                    background-color: #76b8d8; /* Slightly darker blue on hover */
                    color: #ffffff !important; /* Ensure text remains white on hover */
                    text-decoration: none; /* Ensure no underline on hover */
                }}

                .footer {{
                    text-align: center;
                    margin-top: 30px;
                    font-size: 12px;
                    color: #aaa;
                }}

                /* Responsive styles (basic) */
                @media only screen and (max-width: 640px) {{
                    .email-container {{
                        padding: 20px;
                        margin: 10px;
                        border-radius: 10px;
                    }}
                     .header h1 {{
                        font-size: 24px;
                     }}
                     .article h2 {{
                        font-size: 18px;
                     }}
                     .summary {{
                        font-size: 14px;
                     }}
                     .button {{
                        padding: 12px 25px; /* Slightly larger tap target */
                     }}
                }}

            </style>
        </head>
        <body>
            <div class="email-container">
                <div class="header">
                    <h1>Your Sports Update</h1>
                    <p class="subtitle">Freshly Curated Just For You</p>
                </div>

        """

        # Add content if summaries exist
        if not summarized_data:
            html_body += "<p style='text-align: center; color: #888;'>No fresh news to share right now, check back later! ✨</p>"
        else:
            # Loop through the data returned by YOUR summarizer function
            for article in summarized_data:
                # Ensure these .get() calls match the keys in the dicts
                # returned by your 'summarize_articles' function.
                # Basic HTML escaping for safety
                title = article.get('title', 'No Title Available').replace('<', '&lt;').replace('>', '&gt;')
                summary = article.get('summary', 'Summary unavailable.').replace('<', '&lt;').replace('>', '&gt;')
                url = article.get('url', '#') # Use '#' as a fallback if URL is missing

                html_body += f"""
                <div class="article">
                    <h2>{title}</h2>
                    <p class="summary">{summary}</p>
                    <a href="{url}" target="_blank" class="button">View Full Article</a>
                </div>
                """

        # Close the container and add a footer
        html_body += f"""
                <div class="footer">
                    <p>Happy reading!</p>
                    <p>&copy; {current_year} Your AI News Bot</p>
                </div>
            </div> </body>
        </html>
        """

        # Attach the HTML part to the message
        part2 = MIMEText(html_body, "html", "utf-8") # Specify UTF-8 encoding
        msg.attach(part2)

        # Send the email using improved error handling
        print("Attempting to connect to SMTP server...")
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            print("Logging in...")
            server.login(SENDER_EMAIL, APP_PASSWORD)
            print(f"Sending email to: {RECIPIENT_EMAIL}")
            # Handles multiple recipients if comma-separated in .env
            server.send_message(msg, from_addr=SENDER_EMAIL, to_addrs=RECIPIENT_EMAIL.split(','))

        print("✅ Stylish newsletter with REAL articles sent successfully!")

    except smtplib.SMTPAuthenticationError:
        print("❌ Failed to send email: Authentication failed. Check SENDER_EMAIL and APP_PASSWORD.")
    except smtplib.SMTPConnectError:
         print(f"❌ Failed to send email: Could not connect to SMTP server {SMTP_SERVER}:{SMTP_PORT}.")
    except Exception as e:
        print(f"❌ Failed to send email: An unexpected error occurred: {e}")
        # Optionally send an error email or log the error

    print("--- Newsletter Generation Complete ---")

# Run the newsletter generation process
if __name__ == "__main__":
    # Add checks for required environment variables before proceeding
    if not SENDER_EMAIL or not APP_PASSWORD or not RECIPIENT_EMAIL:
        print("Error: Please ensure SENDER_EMAIL, APP_PASSWORD, and RECIPIENT_EMAIL are set in your .env file.")
    else:
        send_newsletter()