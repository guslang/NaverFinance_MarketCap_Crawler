import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import os
import ast
import datetime
import math

# 사이트 정보 받아오기
def crawl(url):
    data = requests.get(url)
    print("#데이터 수신 중")
    return data.content

# 크롤링 데이터에서 주요 데이터 추출
def getStockInfo(tr):    
    tds = tr.findAll("td")
    rank = tds[0].text
    aTag = tds[1].find("a")
    name = aTag.text
    nowPrice = tds[2].text
    totalPrice = tds[6].text
    volume = tds[9].text
    per = tds[10].text
    roe = tds[11].text
    return {"rank":rank, "name":name, 
             "nowPrice":nowPrice, "volume":volume, "totalPrice":totalPrice, 
             "per":per, "roe":roe
             }

# 크롤링 데이터 파싱
def parse(conditions,pageString):
    bsObj = BeautifulSoup(pageString, "html.parser")
    box_type_l = bsObj.find("div", {"class":"box_type_l"})
    type_2 = box_type_l.find("table",{"class":"type_2"})
    tbody = type_2.find("tbody")
    trs = tbody.findAll("tr")
    stockInfos = []
    for tr in trs:
        try:
            stockInfo = getStockInfo(tr)            
            if int(stockInfo.get('rank')) > conditions.get('rank'):  #해당 순위의 기업까지 데이터 수집함
                break
            if CmpCondition(conditions,stockInfo): # 필터 조건 비교
                stockInfos.append(stockInfo)            
        except Exception as e:
            # print(e)
            pass
    return stockInfos

# 주식 필터링 조건 비교하여 유효한 데이터만 리턴
def CmpCondition(conditions,stockInfo):
    cdt_start_PER = conditions['per'][0]
    cdt_end_PER = conditions['per'][1]
    stk_PER = float(stockInfo.get('per').replace('N/A','0'))
    stk_ROE = float(stockInfo.get('roe').replace('N/A','0'))    
    cdt_ROE = float(conditions.get('roe'))
    rtn = False
    if stk_PER >= cdt_start_PER and  stk_PER <= cdt_end_PER:  # PER 비교 (start <= PER <= end )
        if stk_ROE >= cdt_ROE:                                # ROE 비교 (~이상)
            rtn = True    
    return rtn

# 주식 시가총액정보 가져오기
def getSiseMarket(conditions, page):
    url = "https://finance.naver.com/sise/sise_market_sum.nhn?sosok={}&page={}".format(conditions['stockgb'], page)
    pageString = crawl(url)
    siselist = parse(conditions,pageString)
    return siselist

# Naver 주식정보 크롤링 Main Process
def crawlNaver(conditions):        
    cdt_rank = conditions.get('rank')  # rank 입력값
    if cdt_rank > 500:
        print('시가총액 500위까지만 조회됩니다. rank 입력('+cdt_rank+')')
        return
    pages = math.ceil(cdt_rank / 50) + 1  # 페이지당 50개, 소수점은 반올림
    today = datetime.datetime.today().date()
    kospi_kosdoc = ['Kospi','Kosdoc']    
    fileName = './' + str(today) + '_' + kospi_kosdoc[conditions['stockgb']]  + '.csv'    
    
    i = 0   # 첫 행 체크
    for page in range(1, pages): # 100 = 50 * 2        
        result = getSiseMarket(conditions, page) #0 코스피 1코스닥        
        df=pd.DataFrame(result)
        
        if i == 0:            
            df.columns = ['순위','종목명','현재가', '거래량','시가총액','PER','ROE']
            df.to_csv(fileName, index=False, mode='w', encoding='cp949')
        else:
            df.to_csv(fileName, index=False, mode='a', encoding='cp949', header=False)
        i +=1

if __name__ == "__main__":    
    # 필터링 조건 : 우량주
    GoodStock_conditions = {                
                    "stockgb": 0,       #0:Kospi/1:Kosdoc
                    "rank":100,         #시총 순위
                    "per":[10,20],      #PER 최소~최대
                    "roe":10            #ROE 기준값 ( 예:ROE가 10이상인 주식)
                }
    # 필터링 조건 : 성장주 
    GrowthStock_conditions = {
                    "stockgb": 1,       #0:Kospi/1:Kosdoc
                    "rank":500,         #시총 순위
                    "per":[20,200],     #PER 최소~최대
                    "roe":20            #ROE 기준값 ( 예:ROE가 20이상인 주식)
                }
    print('### Naver 증권 - 시가총액 기준 Crawling ###')
   
    crawlNaver(GoodStock_conditions)
    # crawlNaver(GrowthStock_conditions)
    # crawlNaver(100, 1, '')
    print('### Naver 증권 - 시가총액 기준 Crawling 완료 ###')