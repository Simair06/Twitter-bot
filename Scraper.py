from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import datetime
import os
import time



def ask_gemini(prompt: str, retries: int = 5):
    load_dotenv()
    GEM_KEY = os.getenv("GEM_KEY")

    MODELS = [
        "gemini-2.5-flash",
        "gemini-1.5-pro"
    ]

    data = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ]
    }

    for model in MODELS:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={GEM_KEY}"

        for attempt in range(retries):
            try:
                response = requests.post(
                    url,
                    json=data,
                    timeout=30
                )

                if response.status_code == 200:
                    result = response.json()
                    return result["candidates"][0]["content"]["parts"][0]["text"]

                if response.status_code in (429, 500, 503):
                    wait = 2 ** attempt
                    print(f"[Gemini] {model} {response.status_code}, retry in {wait}s")
                    time.sleep(wait)
                    continue

                response.raise_for_status()

            except (requests.exceptions.RequestException, KeyError) as e:
                wait = 2 ** attempt
                print(f"[Gemini] {model} error: {e}, retry in {wait}s")
                time.sleep(wait)

        print(f"[Gemini] Model {model} failed, switching...")

    print("[Gemini] All models unavailable")
    return ""




def scraper():
    with open("last_exe.txt", "r") as f:
        datelast = f.read().strip()
        datelast = datetime.datetime.strptime(datelast, "%Y-%m-%d %H:%MZ")
        


    url = "https://bulinews.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")


    article = soup.find("div", class_="bulinews-article-flow")
    
    links = []
    # Alle <a>-Tags mit href durchsuchen
    for a_tag in article.find_all('a', href=True):
        link = a_tag['href']
        
        # Prüfen, ob ein <time>-Tag innerhalb des <a>-Tags vorhanden ist
        time_tag = a_tag.find('time', class_='zypor-timing')
        if time_tag and time_tag.has_attr('datetime'):
            datetime_value = time_tag['datetime']
        else:
            datetime_value = "Keine Zeit gefunden"
        

        datetime_value = datetime.datetime.strptime(datetime_value, "%Y-%m-%dT%H:%MZ")
        



        if datetime_value >= datelast:
            links.append(link)

        

    print(links)

    text = {}

    for link in links:
        url = link
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        article = soup.find("article", id="zypor-article")
        
        title_tag = article.find("h1")
        title = title_tag.get_text(strip=True) if title_tag else ""

        # 2. Untertitel / Artikelkopf
        head_tag = article.find("div", class_="article_head")
        intro = head_tag.get_text(strip=True) if head_tag else ""

        # 3. gesamter Artikeltext (alle <p>-Tags)
        paragraphs = [
            p.get_text(strip=True)
            for p in article.find_all("p")
        ]
        full_text = "\n\n".join(paragraphs)

        """print("=== TITEL ===")
        print(title)

        print("\n=== INTRO ===")
        print(intro)

        print("\n=== ARTIKELTEXT ===")
        print(full_text)"""

        text[title] = full_text
    return text    

def main():
    text = scraper()
        
    if len(text) > 3 :
        tweets = 2
    else:
        tweets = 1


    if len(text) >= 1:
        prompt = f"Please write {tweets} tweet(s) with Hashtag and everything to gain reach about the following articles. Try to define the most important news and write about them the most. Write it in english and if you put different infos in a tweet (example form different articels in 1 tweet), please add a space for example 1 line between. Please try to write the info very short, that you can potentially fit 2 different news in 1 tweet, if there are multiple. do only include news from 1. Bundesliga. Please only return a string with the two tweets seperated by a |, if theres only 1 tweet do tweet | . it's very important to not write more than 265 signs per tweet!: {text}"

        tweets = ask_gemini(prompt)
    else:
        tweets = ""

    
    try:
        t1,t2 = tweets.split("|")
        tweetlist = [t1,t2]
    except:
        tweetlist = []





    return tweetlist


