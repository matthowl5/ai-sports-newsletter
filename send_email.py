import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Load email credentials and recipient from .env
load_dotenv()

print(os.getenv("SENDER_EMAIL"))  # should show your Gmail
print(os.getenv("APP_PASSWORD"))  # should show the app password

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")  # Gmail app password, not your main password
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")  # Or use a list if sending to multiple people

# Example summarized articles (you'll replace this with real summaries)
summarized_articles = [
    {
        "title": "Lakers Dominate Playoffs Opener",
        "source": "ESPN",
        "summary": "The Lakers opened the playoffs with a decisive win, with LeBron leading the charge.",
        "url": "https://www.espn.com/nba/story/lakers-win"
    },
    {
        "title": "Chelsea Signs New Midfielder",
        "source": "BBC Sport",
        "summary": "Chelsea has finalized the transfer of a promising young midfielder in a £45m deal.",
        "url": "https://www.bbc.com/sport/football/chelsea-signing"
    }
]

# Format the newsletter content
newsletter_body = "🏟️ **Your AI-Powered Sports News Roundup**\n\n"
for article in summarized_articles:
    newsletter_body += f"""\
🏈 **Title**: {article["title"]}
🗞️ **Source**: {article["source"]}
📝 **Summary**: {article["summary"]}
🔗 **Read more**: {article["url"]}\n\n"""

# Convert to MIMEText email (plain text or html)
msg = MIMEText(newsletter_body, "plain")
msg["Subject"] = "Your AI Sports News Roundup"
msg["From"] = SENDER_EMAIL
msg["To"] = RECIPIENT_EMAIL

# Send the email
try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(msg)
    print("✅ Newsletter sent successfully!")
except Exception as e:
    print("❌ Failed to send email:", e)
