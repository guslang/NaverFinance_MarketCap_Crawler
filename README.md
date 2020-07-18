<h1>NaverFinance_MarketCap_Crawler</h1>

<br>
네이버 금융 시가총액 정보를 가져와서 우량 주식을 찾아주는 크롤링 프로그램입니다. 
주요 추출 조건을 리스트로 등록하고 실행 시 조건에 맞는 데이터를 추출하여 파일로 저장합니다. 


<h2> 필터링 조건 : 우량주 </h2>
# '
GoodStock_conditions = {                
                "stockgb": 0,       #0:Kospi/1:Kosdoc
                "rank":100,         #시총 순위 (최대 500위)
                "per":[10,30],      #PER 최소~최대
                "roe":10            #ROE (기준 이상)
            }
<p>
 print('### Naver 증권 - 시가총액 기준 Crawling ###')
 crawler.crawlNaver(GoodStock_conditions)
 print('### Naver 증권 - 시가총액 기준 Crawling 완료 ###')
 </p>



BeautifulSoup4로 크롤링한 결과를 pandas로 csv 파일로 출력합니다. 
Simple하고 강력한 기능으로 투자 주식을 찾아줍니다. 

<h2>네이버 시가총액</h2>
<a target="_blank" rel="noopener noreferrer" href="https://github.com/guslang/NaverFinance_MarketCap_Crawler/blob/master/image/naver_finance_market_cap.png">
<img src="https://github.com/guslang/NaverFinance_MarketCap_Crawler/blob/master/image/naver_finance_market_cap.png" alt="Naver Finanace" style="max-width:100%;"></a>
<br>

<h2>크롤링 실행 화면</h2>
<a target="_blank" rel="noopener noreferrer" href="https://github.com/guslang/NaverFinance_MarketCap_Crawler/blob/master/image/run_processing.png">
<img src="https://github.com/guslang/NaverFinance_MarketCap_Crawler/blob/master/image/run_processing.png" alt="Naver Finanace" style="max-width:100%;"></a>

<br>
<h2>주식 추출 결과</h2>
<a target="_blank" rel="noopener noreferrer" href="https://github.com/guslang/NaverFinance_MarketCap_Crawler/blob/master/image/sample_result.png">
<img src="https://github.com/guslang/NaverFinance_MarketCap_Crawler/blob/master/image/sample_result.png" alt="Naver Finanace" style="max-width:100%;"></a>
