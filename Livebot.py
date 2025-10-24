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
    with open("Spielbeginn.txt", "r") as f:
        current_content = f.read().strip()
    if current_content != matchday:
        with open("Spielbeginn.txt", "w") as f:
            f.write(matchday)
    return matchday
            
       
    

def get_matches():
    return 0
    


def main():
    matchday = get_matchday()
    week_data = get_matches()

   
    

    


schedule.every().day.at("22:11:50").do(main)
while True:
    schedule.run_pending()
    time.sleep(1)


