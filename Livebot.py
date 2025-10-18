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
uhrzeit = "11:46"

print(datetime.datetime.now())


def api(url):
    response = requests.get(url)
    data = response.json()
    return data


def get_matchday():
    global matchday
    matchday = api(matchday_url)
    matchday = matchday["groupName"]
    print(matchday)
    return matchday
    

def get_matches():
    global this_week
    this_week = api(current_matches_url)
    print(this_week)
    return this_week

def main():
    schedule.every().saturday.at(uhrzeit).do(get_matchday)
    schedule.every().saturday.at(uhrzeit).do(get_matches)
    while True:
        schedule.run_pending()
        time.sleep(1)


main()

