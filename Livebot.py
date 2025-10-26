import datetime
import time
import threading
import requests
import os
from dotenv import load_dotenv
import schedule
from Tweeter import tweet, mdprinter

#https://www.openligadb.de/

current_matches_url = "https://api.openligadb.de/getmatchdata/bl1"
matchday_url = "https://api.openligadb.de/getcurrentgroup/bl1"

print(datetime.datetime.now())


def api(url):
    response = requests.get(url)
    data = response.json()
    return data


def get_matchday():
    matchday = api(matchday_url)
    matchday = matchday["groupName"]
    with open("Spieltag.txt", "r") as f:
        current_content = f.read().strip()
    if current_content != matchday:
        with open("Spieltag.txt", "w") as f:
            f.write(matchday)
            post = mdprinter(matchday)
            tweet(post)
    return matchday
              

    


def main():
    matchday = get_matchday()


   


schedule.every().day.at("12:23:00").do(main)
while True:
    schedule.run_pending()
    time.sleep(1)


#todo -- kürzere Teamnames, dass alles passt
