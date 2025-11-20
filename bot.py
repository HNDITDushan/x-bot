import tweepy
import os
import random
from dotenv import load_dotenv
from datetime import datetime
import schedule
import time
from keep_alive import keep_alive

keep_alive()

# Load credentials from .env
load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

# --- Authenticate for API v1.1 (for media upload + retweet if needed later) ---
auth = tweepy.OAuth1UserHandler(
    API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
)
api = tweepy.API(auth)

# --- Authenticate for API v2 (for tweeting) ---
client = tweepy.Client(
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)

# 🖼️ Folder containing images
IMAGE_FOLDER = "/Volumes/PortableSSD/Projects/x-bot/images"

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
    """Post tweet with an optional random image. 'when' is 'morning' or 'night'."""
    try:
        message = build_message(when)

        # Pick a random image if available
        image_files = []
        try:
            image_files = [f for f in os.listdir(IMAGE_FOLDER) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
        except Exception as e:
            # If folder not present or unreadable, just post text
            print("⚠️ Could not read IMAGE_FOLDER:", e)

        if image_files:
            random_image = random.choice(image_files)
            image_path = os.path.join(IMAGE_FOLDER, random_image)
            try:
                media = api.media_upload(image_path)
                # media.media_id should work; fall back to media.media_id_string if available
                media_id = getattr(media, "media_id", None) or getattr(media, "media_id_string", None)
                if media_id:
                    client.create_tweet(text=message, media_ids=[media_id])
                    print(f"✅ [{when}] Tweet with image posted: {message} ({random_image})")
                else:
                    # fallback to posting text only if upload didn't return id
                    client.create_tweet(text=message)
                    print(f"⚠️ [{when}] Media uploaded but no media_id returned — posted text only: {message}")
            except Exception as e:
                print("❌ Error uploading media or posting tweet with image:", e)
                # attempt posting text only
                try:
                    client.create_tweet(text=message)
                    print(f"✅ [{when}] Tweet (text only, after media error) posted:", message)
                except Exception as e2:
                    print("❌ Failed to post text-only tweet after media error:", e2)
        else:
            # No image found or folder inaccessible
            try:
                client.create_tweet(text=message)
                print(f"✅ [{when}] Tweet (text only) posted:", message)
            except Exception as e:
                print("❌ Error posting text-only tweet:", e)

    except Exception as e:
        print("❌ Unexpected error in post_tweet:", e)


# -------------------------
# Scheduling
# -------------------------
# Post at 11:11 AM (morning)
schedule.every().day.at("11:11").do(post_tweet, when="morning")

# Post at 11:11 PM (night)
# 23:11 is 11:11 PM in 24-hour format
schedule.every().day.at("23:11").do(post_tweet, when="night")

print("🤖 Bot is running… (scheduled for 11:11 AM and 11:11 PM daily)")
while True:
    try:
        schedule.run_pending()
    except Exception as e:
        # keep bot alive even if a scheduled job raises
        print("❌ Error while running scheduled jobs:", e)
    time.sleep(30)
