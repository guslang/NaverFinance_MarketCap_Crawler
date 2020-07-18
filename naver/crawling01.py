import operator
import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import os
import ast

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
    #return (rank + "," + name + "," +  href + "," +  href[20:] + "," + nowPrice + "," +  totalPrice + "," +  volume + "," + per + "," + roe +"\n")


def parse(pageString):
    bsObj = BeautifulSoup(pageString, "html.parser")
    box_type_l = bsObj.find("div", {"class":"box_type_l"})
    type_2 = box_type_l.find("table",{"class":"type_2"})
    tbody = type_2.find("tbody")
    trs = tbody.findAll("tr")
    stockInfos = []
    for tr in trs:
        try:
            stockInfo = getStockInfo(tr)
            stockInfos.append(stockInfo)
        except Exception as e:
            # print("error")
            pass
    return stockInfos


def getSiseMarketSum(sosok, page):
    url = "https://finance.naver.com/sise/sise_market_sum.nhn?sosok={}&page={}".format(sosok, page)
    pageString = crawl(url)
    list = parse(pageString)
    return list

def savedata():
    for page in range(1, 2 + 1): # 100 = 50 * 2
        lists = getSiseMarketSum(0, page) #0 코스피 1코스닥
        df=pd.DataFrame(lists)
        if not os.path.exists('./top100.csv'):
            df.to_csv('./top100.csv', index=False, mode='w', encoding='cp949')
        else:
            df.to_csv('./top100.csv', index=False, mode='a', encoding='cp949', header=False)

    # with open('kospi.csv', 'w', newline='') as csvfile:
    #     fieldnames = ['rank', 'name', 'href', 'href[20:]' , 'code','nowPrice','totalPrice', 'volume','per','roe']
    #     wr = csv.DictWriter(csvfile, fieldnames=fieldnames)
    #     wr.writeheader()
    #     result = []
    #     for page in range(1, 10 + 1): # 500 = 50 * 10
    #         lists = getSiseMarketSum(0, page) #0 코스피 1코스닥
    #         for list in lists:
    #             # print(list)
    #             wr.writerow(list)
    #         # result += list

def readdata(per):
    data = pd.read_csv("./top100.csv",encoding="cp949")
    # print(data)
    # print(type(data))
    #
    # print(data.index)
    # print(data.columns)
    # print(data.values[1])
    # print(data.index[1])
    for r in data.values:
        try:
            if eval(r[7]) > float(per):
                print(r)
        except(ValueError,TypeError) as e:
            break

    # for item in data.items():
    #     print(item.index())
    #     break


    # with open('./top100.csv', 'r', newline='') as kfile:
    #     # freader = csv.reader(kfile)
    #     freader = csv.DictReader(kfile)
    #     # for item in freader:
    #
    #     for c in freader:
    #         prtYN = 'Y'
    #         for k, v in c.items():
    #             # print (k,v)
    #             if k == 'per':
    #                 if v == 'N/A' :
    #                     prtYN = 'N'
    #                     break
    #                 elif float(v) < per:  # per 기준 추출
    #                     prtYN = 'N'
    #                     break
    #
    #         if (prtYN == 'Y'):
    #             print(c)
    #             print('-------------')

#readdata(50)

# data = pd.read_csv("./top100.csv",encoding="cp949")
# print(data)
# print(type(data))

# savedata()
# print("파일저장 완료")
# readdata(100)
# print("파일읽기 완료")

import datetime
print( datetime.datetime.today().date() )
