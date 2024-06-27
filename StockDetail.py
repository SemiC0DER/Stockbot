'''
StockDetail은 investing.com에서 주식을 검색하여 상세한 데이터를 반환해주는 모듈입니다.
반환값은 [제목, 정보, 가격, 변화, 변화%, 시장상태, url]입니다.
'''
import requests
from bs4 import BeautifulSoup

class Stock(): #생성자 -> searchStock -> getStock 순으로 주식을 검색하는 클래스입니다.
    def __init__(self, message, type): #investing.com의 검색결과를 보여주는 링크를 초기화합니다.
        message.replace(' ', '%20')
        self.url = f'https://kr.investing.com/search?q={message}'
        self.type = type

    def __searchStock(self): #검색결과 중 연관성이 높은 것을 나열하여 속성이 type인 것을 돌려줍니다.
        url = self.url
        res = requests.get(url).text
        soup = BeautifulSoup(res , 'lxml')

        searched = soup.find('div', attrs={'class':'js-inner-all-results-quotes-wrapper newResultsContainer quatesTable'})

        if searched is None:
            return None
        
        searched = searched.select('a')

        for stock in searched:
            if stock.find('span', attrs={'class':'fourth'}).text[:2] == self.type:
                found = stock['href']
                return f'https://kr.investing.com{found}'

        return None
    
    def getStock(self): #검색한 주식의 상세한 정보를 돌려줍니다.
        url = self.__searchStock()
        if url is None:
            return None
        
        res = requests.get(url).text
        soup = BeautifulSoup(res , 'lxml')

        detail = soup.find('div', attrs={'class':'flex flex-col gap-6 md:gap-0'})
        if detail is None:
            print('웹사이트에서 정보를 가져오는데 실패했습니다.')
            return None
        temp = detail.find('div', attrs={'class':'relative mb-3.5 md:flex-1'})
        title = temp.find('h1').text #주식 이름
        market = temp.find('span', attrs={'class':'flex-shrink overflow-hidden text-ellipsis text-xs/5 font-normal'}).text
        currency = temp.find('div', attrs={'data-test':'currency-in-label'}).text if self.type == '주식' else title.split()[0].split('/')[-1]
        description = market + currency #주식 정보 (상장 시장, 사용 통화)
        temp = detail.find('div', attrs={'class':'flex-1'})
        last_price = temp.find('div', attrs={'data-test':'instrument-price-last'}).text + ' ' + currency.split()[-1] #현재 주식 가격
        price_change = temp.find('span', attrs={'data-test':'instrument-price-change'}).text #주식 변화
        change_percent = temp.find('span', attrs={'data-test':'instrument-price-change-percent'}).text #주식 변화 %
        current_state = temp.find('span', attrs={'data-test':'trading-state-label'}).text #시장 상태

        return [title, description, last_price, price_change, change_percent, current_state, url]
    
stock = Stock('달러','외환')
print(stock.getStock())
