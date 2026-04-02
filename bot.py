import tweepy
import os
import random
from dotenv import load_dotenv
from datetime import datetime, date
import schedule
import time
import requests

from image_with_quote import generate_image_with_quote

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
IMAGE_FOLDER_QUOTES = os.getenv("IMAGE_FOLDER_QUOTES")

QUOTE_API_KEY_1 = os.getenv("QUOTE_API_KEY_1")
QUOTE_API_KEY_2 = os.getenv("QUOTE_API_KEY_2")
QUOTE_API_KEY_3 = os.getenv("QUOTE_API_KEY_3")

QUOTE_API_URL = "https://api.api-ninjas.com/v2/randomquotes?categories=success,wisdom"
DAY_OF_HISTORY_API_URL = "https://api.api-ninjas.com/v1/dayinhistory"
BTC_API_URL = "https://api.api-ninjas.com/v1/bitcoin"

# ------------------------------------------------
# Twitter Auth
# ------------------------------------------------
# auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
# api = tweepy.API(auth)

# client = tweepy.Client(
#     consumer_key=API_KEY,
#     consumer_secret=API_SECRET,
#     access_token=ACCESS_TOKEN,
#     access_token_secret=ACCESS_TOKEN_SECRET
# )

api_bot1, client_bot1 = create_twitter_client("BOT1")
api_bot2, client_bot2 = create_twitter_client("BOT2")
api_bot3, client_bot3 = create_twitter_client("BOT3")
api_bot4, client_bot4 = create_twitter_client("BOT4")

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
    
def get_random_image_Quote():
    """Return a random image path or None."""
    try:
        files = [f for f in os.listdir(IMAGE_FOLDER_QUOTES)
                 if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]

        return os.path.join(IMAGE_FOLDER_QUOTES, random.choice(files)) if files else None
    except Exception:
        return None


def tweet(text, client, api=None, image_path=None):
    try:
        if image_path and api:
            media = api.media_upload(image_path)
            client.create_tweet(text=text, media_ids=[media.media_id])
        else:
            client.create_tweet(text=text)

        print("✅ Tweet sent:", text)
    except Exception as e:
        print("❌ Tweet failed:", e)


# ------------------------------------------------
# 11:11 TWEETS
# ------------------------------------------------

def build_message(when):
    date_str = datetime.now().strftime('%Y-%m-%d')

    messages = {
        "morning": f"Good Morning! ☀ It's {date_str}. 11:11 — Have a bright day!",
        "night":   f"Good Night! 🌙 It's {date_str}. 11:11 — Wishing you a peaceful night!"
    }

    return messages.get(when, f"It's {date_str} — Hello!")


def post_tweet(when):
    message = build_message(when)
    img = get_random_image()
    tweet(message, client_bot1, api_bot1, img)



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
    tweet(christmas_message(), client_bot1)


# ------------------------------------------------
# Quote Tweet
# ------------------------------------------------

def get_quote(QUOTE_API_KEY):
    try:
        response = requests.get(QUOTE_API_URL, headers={"X-Api-Key": QUOTE_API_KEY})
        data = response.json()

        if isinstance(data, list) and data:
            q = data[0].get("quote", "")
            a = data[0].get("author", "")
            generate_image_with_quote(q, a)
            return f'"{q}"\n\n— {a}'
    except:
        get_quote(QUOTE_API_KEY_2)
        pass

    # Default fallback
    return "Success is not final, failure is not fatal."


def send_tweet():
    # img = get_random_image_Quote()
    # print("Selected quote image:", img)
    tweet(get_quote(QUOTE_API_KEY_1), client_bot2)

# ------------------------------------------------
# Day in History
# ------------------------------------------------

def get_day_in_history():
    
    try:
        response = requests.get(DAY_OF_HISTORY_API_URL, headers={"X-Api-Key": QUOTE_API_KEY_1})
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
    tweet(message, client_bot1)

# ------------------------------------------------
# Hourly BTC Update
# ------------------------------------------------

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


def send_btc_update():
    message = get_btc_price()
    # print(message)
    tweet(message, client_bot1)
    # tweet(message, client_bot3)
    # tweet(message, client_bot4)

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

# Hourly Quotes: 06:00 AM → 10:00 PM
for hour in range(5, 23):
    schedule.every().day.at(f"{hour:02d}:00").do(send_tweet)
    
# Hourly BTC Update
schedule.every().hour.at(":45").do(send_btc_update)

print("\n🤖 Bot Running…")
print("⏰ 11:11 AM — Morning Tweet")
print("⏰ 11:11 PM — Night Tweet")
print("🎄 10:30 AM — Christmas Countdown")
print("⏰ 06:00 AM → 10:00 PM — Hourly Quotes")
print("⏰ Hourly BTC Update\n")

# send_btc_update()  # Initial BTC update on startup

while True:
    try:
        schedule.run_pending()
    except Exception as e:
        print("❌ Scheduler error:", e)

    time.sleep(30)