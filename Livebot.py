import datetime
import time
import threading
import requests
import os
from dotenv import load_dotenv

def api():
    load_dotenv()
    api_key = os.getenv("API2_KEY")
    url = "https://v3.football.api-sports.io/leagues?id=78"
    headers = {
        "x-apisports-key": api_key
    }

    print(api_key)

    response = requests.get(url, headers=headers)
    data = response.json()
    print(data)

api()