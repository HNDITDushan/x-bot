import tweepy
import os
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

# Authenticate
client = tweepy.Client(
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)

def post_tweet():
    message = f"Good morning! ☀️ It's {datetime.now().strftime('%Y-%m-%d')} — have a great day!"
    client.create_tweet(text=message)
    print("✅ Tweet posted:", message)

post_tweet()

# Schedule daily at 10:00 AM
# schedule.every().day.at("15:27").do(post_tweet)

# print("Bot is running…")
# while True:
#     print("Running while loop…")
#     schedule.run_pending()
#     time.sleep(60)
