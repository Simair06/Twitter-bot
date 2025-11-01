import tweepy
from dotenv import load_dotenv
import os
import datetime
from openpyxl import load_workbook

def tweet(post):
    load_dotenv()
    print("Working dir:", os.getcwd())
    bearer_key = os.getenv("BEARER_KEY")
    api_key = os.getenv("API_KEY")
    api_key_secret = os.getenv("API_KEY_SECRET")
    access_token = os.getenv("ACCESS_TOKEN")
    access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")
    client = tweepy.Client(bearer_key,api_key,api_key_secret,access_token,access_token_secret)
    response = client.create_tweet(text=post)
    print("POst")
    print(response)


def mdprinter(matchday):
    md,irr = matchday.split(".")
    wb = load_workbook("Spiele.xlsx")
    ws = wb[matchday]
    

    text = f"⚽Bundesliga MD{md}\n"
    current_day = None
    
    for i, row in enumerate(ws.iter_rows(values_only=True)):
        if i == 0:
            continue
        home = row[0]
        away = row[1]
        date = row[2]

        date_obj = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
        weekday = date_obj.strftime("%a")  # Kürzer: Mon, Tue, ...
        time_str = date_obj.strftime("%H:%M")
        
        if weekday != current_day:
            text += f"\n{weekday}\n"
            current_day = weekday

        text += f"{time_str} {home} 🆚 {away}\n"
        
        # Check if we are over 280 characters
        if len(text) > 280:
            text = text[:277] + "..."
            break

    return text


def mprinter(data):
    text = "⚽ FT\n\n"

    result = data["matchResults"][1]

    home = data["team1"] ["teamName"]
    away = data["team2"] ["teamName"]
    home_goals = result["pointsTeam1"]
    away_goals = result["pointsTeam2"]
    number_goals = int(home_goals) + int(away_goals)

    text += f"{home} {home_goals} - {away_goals} {away}\n\n"

    for e in data["goals"]:
        min = e ["matchMinute"]
        scorer = e ["goalGetterName"]
        text += f"⚽ {min}' {scorer}\n"

    return text
    


    