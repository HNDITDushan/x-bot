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

def create_twitter_client(prefix):
    api_key = os.getenv(f"{prefix}_API_KEY")
    api_secret = os.getenv(f"{prefix}_API_SECRET")
    access_token = os.getenv(f"{prefix}_ACCESS_TOKEN")
    access_secret = os.getenv(f"{prefix}_ACCESS_TOKEN_SECRET")

    # v1.1 (media)
    auth = tweepy.OAuth1UserHandler(
        api_key, api_secret, access_token, access_secret
    )
    api = tweepy.API(auth)

    # v2 (tweets)
    client = tweepy.Client(
        consumer_key=api_key,
        consumer_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_secret
    )

    return api, client


# API_KEY = os.getenv("API_KEY")
# API_SECRET = os.getenv("API_SECRET")
# ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
# ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

IMAGE_FOLDER = os.getenv("IMAGE_FOLDER")

QUOTE_API_KEY_1 = os.getenv("QUOTE_API_KEY_1")
QUOTE_API_KEY_2 = os.getenv("QUOTE_API_KEY_2")
QUOTE_API_KEY_3 = os.getenv("QUOTE_API_KEY_3")

QUOTE_API_URL = "https://api.api-ninjas.com/v2/randomquotes?categories=success,wisdom"
DAY_OF_HISTORY_API_URL = "https://api.api-ninjas.com/v1/dayinhistory"
BTC_API_URL = "https://api.api-ninjas.com/v1/bitcoin"

def get_btc_price():
   
    try:
        response = requests.get(BTC_API_URL, headers={"X-Api-Key": QUOTE_API_KEY_3}, timeout=10)
        data = response.json()

        if not isinstance(data, dict):
            return "BTC price data unavailable."

        # Convert safely
        price = float(data.get("price", 0))
        change_24h = float(data.get("24h_price_change", 0))
        change_pct = float(data.get("24h_price_change_percent", 0))
        high_24h = float(data.get("24h_high", 0))
        low_24h = float(data.get("24h_low", 0))
        volume_24h = float(data.get("24h_volume", 0))

        trend_emoji = "📈" if change_24h >= 0 else "📉"
        sign = "+" if change_24h >= 0 else ""

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

        return (
            f"₿ Bitcoin (BTC) Update {trend_emoji}\n\n"
            f"💰 Price: ${price:,.2f}\n"
            f"{trend_emoji} 24h Change: {sign}${change_24h:,.2f} ({sign}{change_pct:.2f}%)\n"
            f"🔼 24h High: ${high_24h:,.2f}\n"
            f"🔽 24h Low: ${low_24h:,.2f}\n"
            f"📊 Volume (24h): {volume_24h:,.4f} BTC\n"
            f"⏰ {timestamp}\n\n"
            f"#Bitcoin #BTC #Crypto"
        )

    except Exception as e:
        return f"BTC update unavailable ❌\nError: {e}"



message = get_btc_price()
print(message)