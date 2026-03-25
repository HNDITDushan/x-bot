from bot import create_twitter_client, get_btc_price, send_btc_update, tweet


# send_btc_update()

api_bot4, client_bot4 = create_twitter_client("BOT4")
message = get_btc_price()
tweet(message, client_bot4)
