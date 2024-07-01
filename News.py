import abc
import requests
from bs4 import BeautifulSoup
from Translator import translate
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

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
    
class Reuters(News):
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True) # 브라우저 꺼짐 방지
        #chrome_options.add_argument("--headless")  # 브라우저 창을 띄우지 않음
        #chrome_options.add_argument("--disable-gpu")  # GPU 비활성화

        self.driver = webdriver.Chrome(options=chrome_options)

        # 페이지 로딩이 완료될 때까지 기다림
        self.driver.implicitly_wait(10)

        self.driver.get(url='https://www.reuters.com/markets/')

    def getArticle(self):
        try:
            title = self.driver.find_element(By.XPATH,'//*[@id="main-content"]/div[3]/div/div[1]/div/div/div[2]/div/a/span').text.strip()
            title = translate(title)
            description = self.driver.find_element(By.XPATH,'//*[@id="main-content"]/div[3]/div/div[1]/div/div/div[2]/div/p').text.strip()
            description = translate(description)
            latesturl = self.driver.find_element(By.XPATH,'//*[@id="main-content"]/div[3]/div/div[1]/div/div/div[2]/div/div[2]/a').get_attribute('href')
            img = self.driver.find_element(By.XPATH,'//*[@id="main-content"]/div[3]/div/div[1]/div/div/div[2]/div/div[2]/a/div/div/div/img').get_attribute('src')
            
            result = [title, description, img, latesturl]
            return result
        finally:
            self.driver.quit()

classmap = {
    '블룸버그': Bloomberg,
    'ap': AP,
    '로이터' : Reuters,
}