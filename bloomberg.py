import requests
from bs4 import BeautifulSoup

def getArticle():
    url = "https://www.bloomberg.co.kr/blog/five-france-stock-optimism/"
    res = requests.get(url).text

    soup = BeautifulSoup(res, "lxml")
    title = soup.find('h1')
    subtitles = soup.select("strong")

    result = [f"{title.text}\n"]
    result.extend(list(map(lambda num: f"{num}. {subtitles[num-1].text.strip('\n')}" , range(1, len(subtitles) + 1))))

    return result