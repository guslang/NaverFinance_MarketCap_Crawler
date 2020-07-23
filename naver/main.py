import Naver_finance_market_cap_crawler as crawler

# 필터링 조건 : 우량주
GoodStock_conditions = {                
                "stockgb": 0,       #0:Kospi/1:Kosdoc
                "rank":100,         #시총 순위 (최대 500위)
                "per":[10,30],      #PER 최소~최대
                "roe":10            #ROE (기준 이상)
            }

print('### Naver 증권 - 시가총액 기준 Crawling ###')
crawler.crawlNaver(GoodStock_conditions)
print('### Naver 증권 - 시가총액 기준 Crawling 완료 ###')
