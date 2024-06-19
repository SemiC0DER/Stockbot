import requests
from bs4 import BeautifulSoup

def getDomesticMarket(n):
    url = "https://finance.naver.com/sise/"
    res = requests.get(url).text
    soup = BeautifulSoup(res , 'lxml')

    
    if n == 1:
        market = ['코스피']
        now = soup.find('span', attrs={'id': 'KOSPI_now'}).text
        change = soup.find('span', attrs={'id': 'KOSPI_change'}).text.split()
        change[0] += '상승' if change[1][0] == '+' else '하락'
        change[1] = change[1][:-2]
        link = soup.select('img', attrs={'width' : '559'})[0]['src']
        market.append(now)
        market.extend(change)
        market.append(link)
    elif n == 2:
        market = ['코스닥']
        now = soup.find('span', attrs={'id': 'KOSDAQ_now'}).text
        change = soup.find('span', attrs={'id': 'KOSDAQ_change'}).text.split()
        change[0] += '상승' if change[1][0] == '+' else '하락'
        change[1] = change[1][:-2]
        link = soup.select('img', attrs={'width' : '559'})[1]['src']
        market.append(now)
        market.extend(change)
        market.append(link)
    elif n == 3:
        market = ['코스피200']
        now = soup.find('span', attrs={'id': 'KPI200_now'}).text
        change = soup.find('span', attrs={'id': 'KPI200_change'}).text.split()
        change[0] += '상승' if change[1][0] == '+' else '하락'
        change[1] = change[1][:-2]
        link = soup.select('img', attrs={'width' : '559'})[2]['src']
        market.append(now)
        market.extend(change)
        market.append(link)
    else:
        market = None

    return market