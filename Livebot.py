import datetime
import time
import threading
import requests
import os
from dotenv import load_dotenv
import schedule
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
    return matchday
    

def get_matches():
    this_week = api(current_matches_url)
    return this_week

def main():
    matchday = get_matchday()
    this_week = get_matches()
    print(matchday)
    print(this_week)

    


schedule.every().saturday.at("12:11:50").do(main)
while True:
    schedule.run_pending()
    time.sleep(1)


