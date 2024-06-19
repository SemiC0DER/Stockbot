library = {
    '주식': '주주의 소유권 및 재산권을 나타내는 증서.',
    '채권': '자금을 빌려주고 받는 증서.',
    '펀드': '개인이 직접투자를 하는 주식과 다르게 자산운용사의 펀드매니저가 대신 투자를 하는 간접투자 방식이다.',
    '코스피': '코스피(KOSPI), 국내 상장사 중 규모가 크고 안정적인 종목들이 모여 있는 시장.',
    '코스닥': '코스닥((KOSDAQ), 자금조달이 어려운 중소기업과 벤처기업을 대상으로 하는 시장.',
    '보통주': '일반적으로 우리가 얘기하는 주식을 보통주, 의결권을 포기하는 대신 더 많은 배당을 받을 수 있는 주식은 우선주.',
    '우선주': '일반적으로 우리가 얘기하는 주식을 보통주, 의결권을 포기하는 대신 더 많은 배당을 받을 수 있는 주식은 우선주.',
    '시가총액': '개별 종목들의 경우에는 ‘발행주식총수 x 주가’가 시가총액이 되고 코스피와 같이 시장의 시가총액을 말할 때는 ‘해당 시장 내 상장사들의 시가총액의 합’을 의미한다.',
    '1월 효과': '매년 1월마다 주가가 상승한다는 효과. 중소형주가 대형주에 비해 수익률이 높아지는 것.',
    '코스피200': '한국의 대표지수이며 외국인 및 기관투자자들이 중심적으로 거래하는 지수이기도 하다.',
    '코스닥150': '시가총액, 유동성, 업종분포 등을 고려해 150개 종목을 뽑아 만든 지수.',
    '가치주': '벌어들이는 돈이나 향후 비전에 비해 현재 주가가 싸다고 판단되는 주식. = 저평가 우량주',
    '성장주': '지금 성장률이 높고 앞으로도 성장가능성이 높은 기업 or 지금은 성장률이 미미하지만 앞으로 큰 성장과 수익이 기대되는 기업',
    '매매수수료': '주식 거래 시 증권사에 내는 수수료.',
    '유관기관 수수료': '주식 거래 시 거치는 기관에 내는 수수료.',
    '증권거래세': '주식 매도 시 발생하는 세금이다.',
    '배당소득세': '배당주를 통해 받는 배당금에 대해 떼는 세금.',
    '양도소득세': '주식을 팔 때 그동안 주가가 상승한 차익에 대해 떼는 세금.',
    'T+2 시스템': '주식 매수 및 매도 시 2거래일 뒤에 입출금되는 시스템.',
    '미수거래': '일정한 증거금으로 주식을 매수한 후 이틀 뒤 갚는 거래.',
}

def stockWord(word):
    if word in library:
        return library[word]
    else:
        return '그런 단어는 없습니다. 개발자에게 추가를 요청해주세요.'
    
def wordList():
    result =[f'총 {len(library)}개의 단어가 등재되어 있습니다.\n']
    for word in sorted(library):
        result.append(word)

    return '\n'.join(result)