from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import datetime
import os



def ask_gemini(prompt: str):
    load_dotenv()
    API_KEY = os.getenv("GEM_API")
    MODEL = "gemini-2.5-flash"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"
    data = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ]
    }

    response = requests.post(url, json=data)  # ← requests macht das JSON selbst
    response.raise_for_status()
    result = response.json()

    try:
        return result["candidates"][0]["content"]["parts"][0]["text"]
    except KeyError:
        return result



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
        prompt = f"Please write {tweets} tweet(s) with Hashtag and everything to gain reach about the following articles. Try to define the most important news and write about them the most. Write it in english and if you put different infos in a tweet (example form different articels in 1 tweet), please add a space for example 1 line between. do only include news from 1. Bundesliga. Please only return a string with the two tweets seperated by a |, if theres only 1 tweet do tweet | . it's very important to not write more than 265 signs per tweet!: {text}"

        tweets = ask_gemini(prompt)
    else:
        tweets = ""

    
    try:
        t1,t2 = tweets.split("|")
        tweetlist = [t1,t2]
    except:
        tweetlist = []



    datenow = datetime.datetime.now(datetime.timezone.utc)
    print(datenow)
    datestr = datenow.strftime("%Y-%m-%d %H:%MZ")
    with open("last_exe.txt", "w") as f:
        f.write(datestr)

    return tweetlist


