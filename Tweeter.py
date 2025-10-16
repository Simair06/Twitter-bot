import tweepy
from dotenv import load_dotenv
import os


load_dotenv()
print("Working dir:", os.getcwd())
bearer_key = os.getenv("BEARER_KEY")
api_key = os.getenv("API_KEY")
api_key_secret = os.getenv("API_KEY_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")



client = tweepy.Client(bearer_key,api_key,api_key_secret,access_token,access_token_secret)

response = client.create_tweet(text="Hallo das ist der 1. Post")
print(response)