import tweepy
import os
import random
from dotenv import load_dotenv
from datetime import datetime
import schedule
import time
import feedparser
import requests
from bs4 import BeautifulSoup
import requests
import json

# Load credentials
load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
BEARER_TOKEN = os.getenv("BEARER_TOKEN")

# --- Authenticate for API v1.1 (for media upload + retweet) ---
auth = tweepy.OAuth1UserHandler(
    API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET,BEARER_TOKEN
)
api = tweepy.API(auth)

# --- Authenticate for API v2 (for tweeting) ---
client = tweepy.Client(
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)

read_client = tweepy.Client(bearer_token=BEARER_TOKEN)


# 🖼️ Folder containing images
IMAGE_FOLDER = "/Volumes/PortableSSD/Projects/x-bot/images"


# ---------------------------------------------------------
# 1️⃣ YOUR DAILY TWEET FUNCTION (KEEPING ORIGINAL)
# ---------------------------------------------------------
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
        client.create_tweet(text=message)
        print("✅ Tweet (text only) posted:", message)


# ---------------------------------------------------------
# 2️⃣ RETWEET FUNCTION EVERY 20 MINUTES
# ---------------------------------------------------------

from twikit import Client as TwiClient

twi = TwiClient()

# Login cookies folder
COOKIE_FILE = "/Volumes/PortableSSD/Projects/x-bot/cookies.json"

def twikit_login():
    if os.path.exists(COOKIE_FILE):
        twi.load_cookies(COOKIE_FILE)
        print("🍪 Cookies loaded (no login required)")
    else:
        # FIRST TIME ONLY → manual login once
        twi.login(
            auth_info_1=os.getenv("X_USERNAME"),
            auth_info_2=os.getenv("X_EMAIL"),
            password=os.getenv("X_PASSWORD")
        )
        twi.save_cookies(COOKIE_FILE)
        print("🔐 Login saved to cookies.json")

twikit_login()


TARGET_ACCOUNTS = ["SriLankaTweet", "SriLanka", "vidusaraonline", "ManojNa85998637"]

def retweet_random():
    try:
        selected = random.choice(TARGET_ACCOUNTS)
        print(f"🔎 Checking tweets from @{selected}")

        # Get latest tweets (twikit v1.2 method)
        tweets = twi.get_user_tweets(screen_name=selected, count=10)

        if not tweets:
            print("⚠ No tweets found")
            return

        tweet = random.choice(tweets)

        twi.retweet(tweet.id)
        print(f"🔁 Retweeted: https://twitter.com/{selected}/status/{tweet.id}")

    except Exception as e:
        if "You have already Retweeted this Tweet" in str(e):
            print("⚠ Already retweeted — skipping")
        else:
            print("❌ Error:", e)

# ---------------------------------------------------------
# 3️⃣ SCHEDULER
# ---------------------------------------------------------

# Daily tweet at 09:30 AM
schedule.every().day.at("09:30").do(post_tweet)

# Retweet every 20 minutes
schedule.every(5).minutes.do(retweet_random)

print("🤖 Bot is running…")
while True:
    schedule.run_pending()
    time.sleep(30)
