import requests
from bs4 import BeautifulSoup

def getLink():
    url = "https://www.bloomberg.co.kr/blog/category/news/"
    res = requests.get(url).text
    soup = BeautifulSoup(res, "lxml")
    link = soup.find('h3').find('a')['href']
    return link


def getArticle():
    url = getLink()
    res = requests.get(url).text

    soup = BeautifulSoup(res, "lxml")
    title = soup.find('h1')
    subtitles = soup.select("strong")

    result = [f"{title.text}\n"]
    result.append('\n'.join(list(map(lambda num: f"{num}. {subtitles[num-1].text.strip()}", range(1, len(subtitles) + 1)))))
    img = soup.find('img')['src']
    result.append(img)
    result.append(url)

    return result