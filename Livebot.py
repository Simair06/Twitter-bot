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
    week_data = api(current_matches_url)
    return week_data

def matchdata(week_data):
    games_this_week = []
    for i in week_data:
        match_date = i ["matchDateTime"]
        match_ID = i ["matchID"]
        team_1 = i ["team1"]["teamName"]
        team_2 = i ["team2"]["teamName"]
        
        matchlist = [match_date, match_ID, team_1, team_2]
        print(matchlist)
    return matchlist





def main():
    matchday = get_matchday()
    week_data = get_matches()
    match_data = matchdata(week_data)
    print(matchday)
    print(f"{week_data}\n\n\n\n")
    print(match_data)

    


schedule.every().thursday.at("18:22:00").do(main)
while True:
    schedule.run_pending()
    time.sleep(1)


