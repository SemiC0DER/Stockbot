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

def getWorldMarket(n):
    symbol = ['DJI@DJI', 'NII@NI225', 'LNS@FTSE100', 'NAS@IXIC', 'SHS@000001', 'PAS@CAC40', 'SPI@SPX', 'HSI@HSI', 'XTR@DAX30']
    worldURL = f'https://finance.naver.com/world/sise.naver?symbol={symbol[n]}'
    graphURL = 'https://finance.naver.com/world/'

    res = requests.get(worldURL).text
    soup = BeautifulSoup(res , 'lxml')
    market = [soup.find('div', attrs={'class':'h_area'}).find('h2').text]
    today = soup.find('div', attrs={'class':'today'}).select('em')

    market.append(today[0].text.strip())
    market.append(today[1].text.strip())
    market.append(today[2].text.replace('\n', '')[1:-1])
  
    market[2] += '상승' if market[3][0] == '+' else '하락'
    
    res = requests.get(graphURL).text
    soup = BeautifulSoup(res , 'lxml')
    graph = soup.find('div', attrs={'class':'market_data'}).select('li')[n].find('img')['src']
    print(graph)
    market.append(graph)

    return market

print(getWorldMarket(2))