import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import os
import ast
import datetime
import math


def crawl(url):
    data = requests.get(url)
    print(data)
    return data.content

def getStockInfo(tr):    
    tds = tr.findAll("td")
    rank = tds[0].text
    aTag = tds[1].find("a")
    href = aTag["href"]
    name = aTag.text
    nowPrice = tds[2].text
    totalPrice = tds[6].text
    volume = tds[9].text
    per = tds[10].text
    roe = tds[11].text
    return {"rank":rank, "name":name, "href":href, "code":href[20:],
             "nowPrice":nowPrice, "totalPrice":totalPrice, "volume":volume,
             "per":per, "roe":roe
             }

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
            # 필터 조건 : per, pbr  
            if int(stockInfo.get('rank')) > conditions.get('rank'):
                break
            if float(stockInfo.get('per').replace('N/A','0')) >= float(conditions.get('per')) \
                and float(stockInfo.get('roe').replace('N/A','0')) >= float(conditions.get('roe')):
                stockInfos.append(stockInfo)            
        except Exception as e:
            # print(e)
            pass
    return stockInfos

def getSiseMarket(conditions, page):
    url = "https://finance.naver.com/sise/sise_market_sum.nhn?sosok={}&page={}".format(conditions['stockgb'], page)
    pageString = crawl(url)
    siselist = parse(conditions,pageString)
    return siselist


def crawlNaver(conditions):    
    pages = math.ceil(conditions.get('rank') / 50) + 1  # 페이지당 50개, 소수점은 반올림
    print('pages:'+str(pages))
    today = datetime.datetime.today().date()
    kospi_kosdoc = ['Kospi','Kosdoc']    
    fileName = './' + str(today) + '_' + kospi_kosdoc[conditions['stockgb']]  + '.csv'    
    if os.path.isfile(fileName): #  파일이 있는 경우 삭제
        os.remove(fileName)           
    
    for page in range(1, pages): # 100 = 50 * 2        
        result = getSiseMarket(conditions, page) #0 코스피 1코스닥        
        # dicRnk = result[0]
        # if int(dicRnk['rank']) > int(conditions.get('rank')) :  #rank 범위만 처리
        #     print('rank over :' + str(result[0]))
        #     break
        df=pd.DataFrame(result)        
        if not os.path.exists(fileName):
            df.to_csv(fileName, index=False, mode='w', encoding='cp949')
        else:
            df.to_csv(fileName, index=False, mode='a', encoding='cp949', header=False)

# 필터링 조건 : 우량주
GoodStock_conditions = {                
                "stockgb": 0,       #0:Kospi/1:Kosdoc
                "rank":30, 
                "per":20, 
                "roe":1
             }
# 필터링 조건 : 성장주 
GrowthStock_conditions = {
                "stockgb": 1,       #0:Kospi/1:Kosdoc
                "rank":200, 
                "per":30, 
                "roe":20
             }
print('### Naver 증권 - 시가총액 기준 Crawling ###')


# print(GoodStock_conditions.get('rank'))
crawlNaver(GoodStock_conditions)
crawlNaver(GrowthStock_conditions)
# crawlNaver(100, 1, '')
print('### Naver 증권 - 시가총액 기준 Crawling 완료 ###')