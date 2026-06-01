import os
import smtplib
import urllib.request
import urllib.parse
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

# ─────────────────────────────────────────────
#  CONFIGURATION — edit these to your liking
# ─────────────────────────────────────────────

NEWS_TOPICS = [
    "Chicago Bears",
    "NFL",
    "artificial intelligence",
    "technology",
    # Add or remove topics freely
]

NEWS_ARTICLES_PER_TOPIC = 3  # top N articles per topic

# ─────────────────────────────────────────────
#  SECRETS (set as GitHub Actions secrets)
# ─────────────────────────────────────────────

NEWSAPI_KEY = os.environ["NEWSAPI_KEY"]
GMAIL_USER  = os.environ["GMAIL_USER"]
GMAIL_PASS  = os.environ["GMAIL_APP_PASSWORD"]
RECIPIENT   = os.environ.get("RECIPIENT_EMAIL", GMAIL_USER)


# ─────────────────────────────────────────────
#  FETCHER
# ─────────────────────────────────────────────

def fetch_news(topic: str) -> list[dict]:
    """Fetch top articles for a topic from NewsAPI."""
    params = urllib.parse.urlencode({
        "q": topic,
        "sortBy": "publishedAt",
        "pageSize": NEWS_ARTICLES_PER_TOPIC,
        "language": "en",
        "apiKey": NEWSAPI_KEY,
    })
    url = f"https://newsapi.org/v2/everything?{params}"
    req = urllib.request.Request(url, headers={"User-Agent": "DailyDigest/1.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read())
    articles = []
    for a in data.get("articles", []):
        if a.get("title") and a.get("url") and "[Removed]" not in a.get("title", ""):
            articles.append({
                "title": a["title"],
                "url": a["url"],
                "source": a.get("source", {}).get("name", "Unknown"),
                "published": a.get("publishedAt", "")[:10],
            })
    return articles


# ─────────────────────────────────────────────
#  EMAIL BUILDER
# ─────────────────────────────────────────────

def build_html(news_data: dict) -> str:
    today = datetime.now().strftime("%A, %B %d, %Y")

    news_html = ""
    for topic, articles in news_data.items():
        if not articles:
            continue
        rows = ""
        for a in articles:
            rows += f"""
            <tr>
              <td style="padding:10px 0; border-bottom:1px solid #f0f0f0;">
                <a href="{a['url']}" style="color:#1a1a2e;font-weight:600;text-decoration:none;font-size:14px;line-height:1.4;">{a['title']}</a>
                <div style="margin-top:4px;font-size:12px;color:#888;">
                  {a['source']} &nbsp;·&nbsp; {a['published']}
                </div>
              </td>
            </tr>"""
        news_html += f"""
        <div style="margin-bottom:28px;">
          <h3 style="margin:0 0 12px;font-size:13px;font-weight:700;text-transform:uppercase;
                     letter-spacing:1.5px;color:#e63946;border-bottom:2px solid #e63946;
                     padding-bottom:6px;">{topic}</h3>
          <table width="100%" cellpadding="0" cellspacing="0">{rows}</table>
        </div>"""

    return f"""<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
<body style="margin:0;padding:0;background:#f4f4f8;font-family:'Georgia',serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#f4f4f8;padding:32px 0;">
    <tr><td align="center">
      <table width="600" cellpadding="0" cellspacing="0" style="max-width:600px;width:100%;">

        <!-- Header -->
        <tr>
          <td style="background:#1a1a2e;padding:32px 36px;border-radius:8px 8px 0 0;">
            <div style="font-size:22px;font-weight:700;color:#ffffff;letter-spacing:-0.5px;">
              ☕ Your Daily Digest
            </div>
            <div style="font-size:13px;color:#a0a0c0;margin-top:4px;">{today}</div>
          </td>
        </tr>

        <!-- News -->
        <tr>
          <td style="background:#ffffff;padding:32px 36px;border-radius:0 0 8px 8px;">
            <h2 style="margin:0 0 24px;font-size:18px;color:#1a1a2e;font-weight:700;">📰 News</h2>
            {news_html}
          </td>
        </tr>

        <!-- Footer -->
        <tr>
          <td style="padding:20px 0;text-align:center;font-size:12px;color:#aaa;">
            Delivered by your Daily Digest bot · Edit topics in digest.py
          </td>
        </tr>

      </table>
    </td></tr>
  </table>
</body>
</html>"""


# ─────────────────────────────────────────────
#  SEND EMAIL
# ─────────────────────────────────────────────

def send_email(subject: str, html_body: str):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = GMAIL_USER
    msg["To"] = RECIPIENT
    msg.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(GMAIL_USER, GMAIL_PASS)
        server.sendmail(GMAIL_USER, RECIPIENT, msg.as_string())
    print(f"✅ Email sent to {RECIPIENT}")


# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────

def main():
    print("Fetching news...")
    news_data = {}
    for topic in NEWS_TOPICS:
        try:
            news_data[topic] = fetch_news(topic)
            print(f"  ✓ {topic}: {len(news_data[topic])} articles")
        except Exception as e:
            print(f"  ✗ {topic}: {e}")
            news_data[topic] = []

    html = build_html(news_data)
    today_str = datetime.now().strftime("%b %d")
    send_email(f"☕ Daily Digest — {today_str}", html)


if __name__ == "__main__":
    main()