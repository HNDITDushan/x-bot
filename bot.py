import tweepy
import os
import random
from dotenv import load_dotenv
from datetime import datetime, date
import schedule
import time
import requests

# ------------------------------------------------
# Load credentials
# ------------------------------------------------
load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

IMAGE_FOLDER = "/Volumes/PortableSSD/Projects/x-bot/images"
QUOTE_API_KEY = "4v1qDs7dntxBJRt3HhQtYg==r9UAOHXWYL484RVc"
QUOTE_API_URL = "https://api.api-ninjas.com/v2/randomquotes?categories=success,wisdom"

# ------------------------------------------------
# Twitter Auth
# ------------------------------------------------
auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

client = tweepy.Client(
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)

# ------------------------------------------------
# Helper Functions
# ------------------------------------------------

def get_random_image():
    """Return a random image path or None."""
    try:
        files = [f for f in os.listdir(IMAGE_FOLDER)
                 if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]

        return os.path.join(IMAGE_FOLDER, random.choice(files)) if files else None
    except Exception:
        return None


def tweet(text, image_path=None):
    """Post a tweet with optional image."""
    try:
        if image_path:
            media = api.media_upload(image_path)
            media_id = getattr(media, "media_id", None)
            client.create_tweet(text=text, media_ids=[media_id])
        else:
            client.create_tweet(text=text)

        print("✅ Tweet posted:", text)
    except Exception as e:
        print("❌ Tweet error:", e)


# ------------------------------------------------
# 11:11 TWEETS
# ------------------------------------------------

def build_message(when):
    date_str = datetime.now().strftime('%Y-%m-%d')

    messages = {
        "morning": f"Good morning! ☀ It's {date_str}. 11:11 — Have a bright day!",
        "night":   f"Good Night! 🌙 It's {date_str}. 11:11 — Wishing you a peaceful night!"
    }

    return messages.get(when, f"It's {date_str} — Hello!")


def post_tweet(when):
    message = build_message(when)
    img = get_random_image()
    tweet(message, img)


# ------------------------------------------------
# 🎄 Christmas Countdown
# ------------------------------------------------

def days_until_christmas():
    today = date.today()
    xmas = date(today.year, 12, 25)
    if today > xmas:
        xmas = date(today.year + 1, 12, 25)
    return (xmas - today).days


def christmas_message():
    days = days_until_christmas()

    if days == 0:
        return "🎄 Merry Christmas! 🎅✨ Wishing everyone joy and blessings!"
    elif days == 1:
        return "🎄 Only 1 day left until Christmas! 🎁✨"
    else:
        return f"🎄 {days} days until Christmas! 🎅🎁 #ChristmasCountdown"


def post_christmas_countdown():
    tweet(christmas_message())


# ------------------------------------------------
# Quote Tweet
# ------------------------------------------------

def get_quote():
    try:
        response = requests.get(QUOTE_API_URL, headers={"X-Api-Key": QUOTE_API_KEY})
        data = response.json()

        if isinstance(data, list) and data:
            q = data[0].get("quote", "")
            a = data[0].get("author", "")
            return f'"{q}"\n\n— {a}'
    except:
        pass

    # Default fallback
    return "Success is not final, failure is not fatal."


def send_tweet():
    tweet(get_quote())

# ------------------------------------------------
# Day in History
# ------------------------------------------------

def get_day_in_history():
    url = "https://api.api-ninjas.com/v1/dayinhistory"
    headers = {"X-Api-Key": "4v1qDs7dntxBJRt3HhQtYg==r9UAOHXWYL484RVc"}

    try:
        response = requests.get(url, headers=headers)
        data = response.json()

        if isinstance(data, list) and len(data) > 0:
            event = data[0].get("event", "")
            year  = data[0].get("year", "")

            return f"📜 Today in History ({year})\n\n{event}\n\n#History #TodayInHistory"

        else:
            return "📜 Today in history — No historical data available."

    except Exception as e:
        return f"Error fetching history: {e}"

def send_day_in_history():
    message = get_day_in_history()
    tweet(message)  # uses your existing tweet() function



# ------------------------------------------------
# Scheduling
# ------------------------------------------------

# 11:11 tweets
schedule.every().day.at("11:11").do(post_tweet, when="morning")
schedule.every().day.at("23:11").do(post_tweet, when="night")

# Christmas countdown
schedule.every().day.at("10:30").do(post_christmas_countdown)

# Day in History
schedule.every().day.at("07:30").do(send_day_in_history)

# Hourly Quotes: 06:00 → 22:00
for hour in range(6, 23):
    schedule.every().day.at(f"{hour:02d}:00").do(send_tweet)

print("\n🤖 Bot Running…")
print("⏰ 11:11 AM — Morning Tweet")
print("⏰ 11:11 PM — Night Tweet")
print("🎄 10:30 AM — Christmas Countdown")
print("⏰ 06:00 AM → 10:00 PM — Hourly Quotes\n")

while True:
    try:
        schedule.run_pending()
    except Exception as e:
        print("❌ Scheduler error:", e)

    time.sleep(30)