'''
StockDetail은 investing.com에서 주식을 검색하여 상세한 데이터를 반환해주는 모듈입니다.
'''
import requests
from bs4 import BeautifulSoup

class Stock(): #생성자 -> searchStock -> getStock순으로 주식을 검색하는 클래스입니다.
    def __init__(self, message): #investing.com의 검색결과를 보여주는 링크를 초기화합니다.
        self.url = f'https://kr.investing.com/search?q={message}'

    def __searchStock(self): #검색결과 중 연관성이 높은 것을 나열하여 속성이 '주식'인 것을 돌려줍니다.
        url = self.url
        res = requests.get(url).text
        soup = BeautifulSoup(res , 'lxml')

        searched = soup.find('div', attrs={'class':'js-inner-all-results-quotes-wrapper newResultsContainer quatesTable'})

        if searched is None:
            return None
        
        searched = searched.select('a')

        for stock in searched:
            if stock.find('span', attrs={'class':'fourth'}).text[:2] == '주식':
                return f'https://kr.investing.com{stock['href']}'

        return None
    
    def getStock(self): #검색한 주식의 상세한 정보를 돌려줍니다.
        url = self.__searchStock()
        if url is None:
            return None
        
        res = requests.get(url).text
        soup = BeautifulSoup(res , 'lxml')
        detail = soup.find('div', attrs={'class':'flex flex-col gap-6 md:gap-0'})
        temp = detail.find('div', attrs={'class':'relative mb-3.5 md:flex-1'})

        title = temp.find('h1').text #주식 이름
        market = temp.find('span', attrs={'class':'flex-shrink overflow-hidden text-ellipsis text-xs/5 font-normal'}).text
        currency = temp.find('div', attrs={'data-test':'currency-in-label'}).text
        description = market + currency #주식 정보 (상장 시장, 통화)
        print(market, currency)
        temp = detail.find('div', attrs={'class':'flex-1'})
        last_price = temp.find('div', attrs={'data-test':'instrument-price-last'}).text
        price_change = temp.find('span', attrs={'data-test':'instrument-price-change'}).text
        change_percent = temp.find('span', attrs={'data-test':'instrument-price-change-percent'}).text
        current_state = temp.find('span', attrs={'data-test':'trading-state-label'}).text

        del detail
        del temp

        img = self.__getImage(f'{url}-chart')

        return [title, description, last_price, price_change, change_percent, current_state]
    
    def __getImage(self, url):
        return True


        



stock = Stock('nvda')
print(stock.getStock())