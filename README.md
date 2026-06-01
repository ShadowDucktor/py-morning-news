# ☕ Daily Digest

Emails you a clean daily briefing at 7 AM with:
- Top news articles for topics you choose
- Top Reddit posts from subreddits you follow

Runs free in the cloud via GitHub Actions — no server needed.

---

## Setup (one-time, ~10 minutes)

### Step 1 — Get a free NewsAPI key
1. Go to [newsapi.org](https://newsapi.org) and click **Get API Key**
2. Sign up for a free account (100 requests/day, plenty for this)
3. Copy your API key — you'll need it in Step 4

---

### Step 2 — Create a Gmail App Password
> Regular Gmail passwords won't work. You need an App Password.

1. Go to your Google Account → **Security**
2. Make sure **2-Step Verification** is ON
3. Search for **App passwords** (or go to myaccount.google.com/apppasswords)
4. Create a new app password — name it "Daily Digest"
5. Copy the 16-character password shown (no spaces)

---

### Step 3 — Put this project on GitHub
1. Create a new **private** GitHub repository (private keeps your workflow file hidden)
2. Upload both files:
   - `digest.py`
   - `.github/workflows/daily-digest.yml`

   Easiest way if you're not a git user:
   - Click **Add file → Upload files** on your new repo page
   - For the workflow file, you'll need to create the folder structure:
     click **Add file → Create new file**, type `.github/workflows/daily-digest.yml`
     and paste the contents

---

### Step 4 — Add your secrets
In your GitHub repo, go to **Settings → Secrets and variables → Actions → New repository secret**

Add these four secrets:

| Secret name | Value |
|---|---|
| `NEWSAPI_KEY` | Your NewsAPI key from Step 1 |
| `GMAIL_USER` | Your Gmail address (e.g. you@gmail.com) |
| `GMAIL_APP_PASSWORD` | The 16-char app password from Step 2 |
| `RECIPIENT_EMAIL` | Where to send the digest (can be same as GMAIL_USER) |

---

### Step 5 — Test it
1. In your repo, go to **Actions → Daily Digest → Run workflow**
2. Click **Run workflow** (green button)
3. Check your inbox in ~30 seconds!

---

## Customizing topics & subreddits

Edit the top of `digest.py`:

```python
NEWS_TOPICS = [
    "Chicago Bears",
    "NFL",
    "esports",
    "artificial intelligence",
    "technology",
    # Add anything here — be specific for better results
    # e.g. "Formula 1", "Python programming", "Chicago local news"
]

SUBREDDITS = [
    "nfl",
    "chibears",
    "esports",
    # Add any subreddit name here
]
```

Commit the change and it takes effect the next morning.

---

## Adjusting the send time

Edit the cron line in `.github/workflows/daily-digest.yml`.
GitHub Actions runs on UTC, so adjust for your timezone:

| Your timezone | Cron for 7 AM |
|---|---|
| Central (CT, UTC-6) | `0 13 * * *` |
| Eastern (ET, UTC-5) | `0 12 * * *` |
| Mountain (MT, UTC-7) | `0 14 * * *` |
| Pacific (PT, UTC-8) | `0 15 * * *` |

> Note: GitHub Actions cron can be delayed by a few minutes during busy periods.

---

## Troubleshooting

- **No email received**: Check the Actions tab in GitHub for error logs
- **"Invalid credentials"**: Re-generate your Gmail App Password — they expire if 2FA changes
- **News results look stale**: NewsAPI free tier searches the last 30 days; try more specific topic names
- **Reddit fetch fails**: Reddit occasionally rate-limits; the script will just skip that subreddit