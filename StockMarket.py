import requests
from bs4 import BeautifulSoup

marketidx = {'코스피': 1,
                '코스닥': 2,
                '코스피200': 3,
                '다우': 4,
                '나스닥': 7,
                'SP': 10,
                '니케이': 5,
                '상해': 8,
                '항셍': 11,
                '영국': 6,
                '프랑스': 9,
                '독일': 12
                }

def getMarketAll():
    return marketidx

def getDomesticMarket(n):
    url = "https://finance.naver.com/sise/"
    res = requests.get(url).text
    soup = BeautifulSoup(res , 'lxml')
    idx = n - 1
    marketsymbol = ['KOSPI', 'KOSDAQ', 'KPI200']
    marketname = ['코스피', '코스닥', '코스피200']
    
    if not (1 <= n < 4):
        return False

    market = [marketname[idx]]
    now = soup.find('span', attrs={'id': f'{marketsymbol[idx]}_now'}).text
    change = soup.find('span', attrs={'id': f'{marketsymbol[idx]}_change'}).text.split()
    change[0] += '상승' if change[1][0] == '+' else '하락'
    change[1] = change[1][:-2]
    link = soup.select('img', attrs={'width' : '559'})[idx]['src']
    market.append(now)
    market.extend(change)
    market.append(link)

    return market

def getWorldMarket(n):
    symbol = ['DJI@DJI', 'NII@NI225', 'LNS@FTSE100', 'NAS@IXIC', 'SHS@000001', 'PAS@CAC40', 'SPI@SPX', 'HSI@HSI', 'XTR@DAX30']
    worldURL = f'https://finance.naver.com/world/sise.naver?symbol={symbol[n]}'
    graphURL = f"https://ssl.pstatic.net/imgfinance/chart/world/continent/{symbol[n]}.png"

    res = requests.get(worldURL).text
    soup = BeautifulSoup(res , 'lxml')
    market = [soup.find('div', attrs={'class':'h_area'}).find('h2').text]
    today = soup.find('div', attrs={'class':'today'}).select('em')

    market.append(today[0].text.strip())
    market.append(today[1].text.strip())
    market.append(today[2].text.replace('\n', '')[1:-1])
  
    market[2] += '상승' if market[3][0] == '+' else '하락'
    market.append(graphURL)

    return market