import abc
import requests
from bs4 import BeautifulSoup
from Translator import translate
'''
뉴스 클래스들의 getArticle의 return값은 [제목, 설명, 이미지, 링크]여야 합니다!
'''
class News(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __init__(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def getArticle(self):
        raise NotImplementedError()
    
class Bloomberg(News):
    def __init__(self):
        url = "https://www.bloomberg.co.kr/blog/category/news/"
        res = requests.get(url).text
        soup = BeautifulSoup(res, "lxml")
        link = soup.find('h3').find('a')['href']
        self.url = link

    def getArticle(self):
        res = requests.get(self.url).text

        soup = BeautifulSoup(res, "lxml")
        title = soup.find('h1')
        subtitles = soup.select("strong")

        result = [f"{title.text}\n"]
        result.append('\n'.join(list(map(lambda num: f"{num}. {subtitles[num-1].text.strip()}", range(1, len(subtitles) + 1)))))
        img = soup.find('img')['src']
        result.append(img)
        result.append(self.url)

        return result
    
class AP(News):
    def __init__(self):
        self.url = "https://apnews.com/hub/financial-markets"

    def getArticle(self):
        res = requests.get(self.url).text
        soup = BeautifulSoup(res, "lxml")

        latest = soup.find('div', attrs={'class':'PagePromo'})
        title = latest['data-gtm-region']
        title = translate(title)
        description = latest.find('div', attrs={'class':'PagePromo-description'}).text.strip()
        description = translate(description)
        latesturl = latest.find('a', attrs={'class':'Link'})['href']
        img = latest.find('img')['src']
        result = [title, description, img, latesturl]
        return result
    
classmap = {
    '블룸버그': Bloomberg,
    'ap': AP
}