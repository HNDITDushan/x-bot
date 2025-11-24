import tweepy
import os
import random
from dotenv import load_dotenv
from datetime import datetime, date
import schedule
import time

# Load credentials from .env
load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

# --- Authenticate for API v1.1 (media upload) ---
auth = tweepy.OAuth1UserHandler(
    API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
)
api = tweepy.API(auth)

# --- Authenticate for API v2 (tweet posting) ---
client = tweepy.Client(
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)

# 🖼️ Folder containing images for your regular tweets
IMAGE_FOLDER = "/Volumes/PortableSSD/Projects/x-bot/images"

# ------------------------------------------------
# 11:11 Tweet Messages
# ------------------------------------------------

def build_message(when: str) -> str:
    """Return the message text based on 'morning' or 'night'."""
    date_str = datetime.now().strftime('%Y-%m-%d')
    if when == "morning":
        return f"Good morning! ☀️ It's {date_str}. 11:11 — Have a bright day!"
    elif when == "night":
        return f"Good evening! 🌙 It's {date_str}. 11:11 — Wishing you a peaceful night!"
    else:
        return f"It's {date_str} — Hello!"


def post_tweet(when="morning"):
    """Post tweet with optional random image."""
    try:
        message = build_message(when)

        # Pick a random image if available
        image_files = []
        try:
            image_files = [f for f in os.listdir(IMAGE_FOLDER)
                           if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
        except Exception as e:
            print("⚠️ Could not read IMAGE_FOLDER:", e)

        if image_files:
            random_image = random.choice(image_files)
            image_path = os.path.join(IMAGE_FOLDER, random_image)

            try:
                media = api.media_upload(image_path)
                media_id = getattr(media, "media_id", None) or getattr(media, "media_id_string", None)

                if media_id:
                    client.create_tweet(text=message, media_ids=[media_id])
                    print(f"✅ [{when}] Tweet with image posted: {message} ({random_image})")
                else:
                    client.create_tweet(text=message)
                    print(f"⚠️ [{when}] Media uploaded but no media_id — posted text only: {message}")

            except Exception as e:
                print("❌ Media upload error:", e)
                try:
                    client.create_tweet(text=message)
                    print(f"✅ [{when}] Text-only fallback posted:", message)
                except Exception as e2:
                    print("❌ Failed to post text-only fallback:", e2)

        else:
            # No images present
            try:
                client.create_tweet(text=message)
                print(f"✅ [{when}] Text-only tweet posted:", message)
            except Exception as e:
                print("❌ Error posting tweet:", e)

    except Exception as e:
        print("❌ Unexpected error in post_tweet:", e)


# ------------------------------------------------
# 🎄 CHRISTMAS COUNTDOWN
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
    try:
        message = christmas_message()
        client.create_tweet(text=message)
        print(f"🎄 Countdown Tweet Posted: {message}")
    except Exception as e:
        print("❌ Error posting Christmas Countdown tweet:", e)


# ------------------------------------------------
# Scheduling
# ------------------------------------------------

# 11:11 AM
schedule.every().day.at("11:11").do(post_tweet, when="morning")

# 11:11 PM
schedule.every().day.at("23:11").do(post_tweet, when="night")

# 🎄 Christmas Countdown (daily at 09:00)
schedule.every().day.at("09:00").do(post_christmas_countdown)

print("🤖 Bot Running…")
print("⏰ 11:11 AM — Morning Tweet")
print("⏰ 11:11 PM — Night Tweet")
print("🎄 09:00 AM — Christmas Countdown Tweet")

while True:
    try:
        schedule.run_pending()
    except Exception as e:
        print("❌ Scheduler error:", e)
    time.sleep(30)
