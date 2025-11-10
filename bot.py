import tweepy
import os
import random
from dotenv import load_dotenv
from datetime import datetime
import schedule
import time

# Load credentials
load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

# --- Authenticate for API v1.1 (for media upload) ---
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

def post_tweet():
    message = f"Good morning! ☀️ It's {datetime.now().strftime('%Y-%m-%d')} — have a great day!"

    # Pick a random image
    image_files = [f for f in os.listdir(IMAGE_FOLDER) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]

    if image_files:
        random_image = random.choice(image_files)
        image_path = os.path.join(IMAGE_FOLDER, random_image)

        # Upload image using API v1.1
        media = api.media_upload(image_path)

        # Post tweet with image using Client (v2)
        client.create_tweet(text=message, media_ids=[media.media_id])
        print(f"✅ Tweet with image posted: {message} ({random_image})")
    else:
        # No image found
        client.create_tweet(text=message)
        print("✅ Tweet (text only) posted:", message)

# post_tweet()

# Schedule daily at 10:00
schedule.every().day.at("09:30").do(post_tweet)

print("🤖 Bot is running…")
while True:
    schedule.run_pending()
    time.sleep(60)
