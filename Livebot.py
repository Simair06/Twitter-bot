import datetime
import time
import threading
import requests
import os
from dotenv import load_dotenv
import schedule
from Tweeter import tweet, mdprinter, mprinter
from openpyxl import load_workbook

#https://www.openligadb.de/

current_matches_url = "https://api.openligadb.de/getmatchdata/bl1"
matchday_url = "https://api.openligadb.de/getcurrentgroup/bl1"
 

print(datetime.datetime.now())


def api(url):
    response = requests.get(url)
    data = response.json()
    return data


def get_matchday():
    matchday
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
              

def live():
    with open("Spieltag.txt", "r") as f:
        matchday = f.read().strip()
    today = []
    wb = load_workbook("Spiele.xlsx")
    ws = wb[matchday]
    for i, row in enumerate(ws.iter_rows(values_only=True)):
        if i == 0:
            continue
        date, time = row[2].split("T")
        match_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        if match_date == datetime.date.today():
            today.append({"id" : row[3], "time" : time })
    #today.append({"id" : , "time" : "11:00:00" }) # Spiele die noch nicht gepostet wurden 
    print(today) 
    return today
       

def pruefe_job():
    jetzt = datetime.datetime.now()
    jetzt = jetzt
    aktuell = []
    spiele = live()
    for spiel in spiele:
        start_time = datetime.datetime.strptime(spiel["time"], "%H:%M:%S").time()
        start = datetime.datetime.combine(datetime.date.today(), start_time)
        ende = start + datetime.timedelta(hours=3)
        if start <= jetzt <= ende:
            aktuell.append(spiel)

    
    if len(aktuell) > 0:
        for spiel in spiele:
            id = spiel["id"]
            data = requests.get(f"https://api.openligadb.de/getmatchdata/{id}")
            data = data.json()
            with open("posted.txt", "r") as f:
                content = f.read()
            if (data["matchIsFinished"]) and (str(id) not in content):
                    text = mprinter(data)
                    tweet(text)
                    with open("posted.txt", "a") as f:
                        f.write(f"{str(id)}\n")


def txtdel():
    with open("posted.txt", "w") as f:
        f.write("")

def main():
    matchday = get_matchday()
    





schedule.every().day.at("01:00:00").do(txtdel)
schedule.every().day.at("12:00:00").do(main)
schedule.every(1).minutes.do(pruefe_job)

while True:
    schedule.run_pending()
    time.sleep(1)



