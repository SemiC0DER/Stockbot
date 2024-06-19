def stockWord(word):
    library = {
        '주식': '주주의 소유권 및 재산권을 나타내는 증서.',
        '채권': '자금을 빌려주고 받는 증서.',
        '펀드': '개인이 직접투자를 하는 주식과 다르게 자산운용사의 펀드매니저가 대신 투자를 하는 간접투자 방식이다.'
    }

    if word in library:
        return library[word]
    else:
        return '그런 단어는 없습니다. 개발자에게 추가를 요청해주세요.'