import requests
from bs4 import BeautifulSoup
from Translator import translate

def getArticle():
    link = "https://apnews.com/hub/financial-markets"
    res = requests.get(link).text
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