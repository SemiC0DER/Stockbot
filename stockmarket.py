import requests
from bs4 import BeautifulSoup

def getDomesticMarket(n):
    url = "https://finance.naver.com/sise/"
    res = requests.get(url).text
    soup = BeautifulSoup(res , 'lxml')
    market = soup.find('li', attrs={"onmouseover":f'moveIndex(\'tab_sel{n}\')'})
    market = market.text.split()
    market[2] += '상승' if market[3][0] == '+' else '하락'
    market[3] = market[3][:-2]
    
    if n == 1:
        market.append("https://ssl.pstatic.net/imgfinance/chart/sise/siseMainKOSPI.png?sid=1718722491864")
    elif n == 2:
        market.append("https://ssl.pstatic.net/imgfinance/chart/sise/siseMainKOSDAQ.png?sid=1718722491864")
    elif n == 3:
        market.append("https://ssl.pstatic.net/imgfinance/chart/sise/siseMainKPI200.png?sid=1718722491864")

    return market