<h1>NaverFinance_MarketCap_Crawler</h1>

<br>
Python으로 구현한 주식 종목 추천 프로그램입니다. 
네이버 금융에서 시가총액 데이터를 크롤링하고 주식 주요지표인 PER/ROE를 이용하여 필터링합니다. 

<br><br>
크롤링은 BeautifulSoup4, 파일 출력은 pandas csv를 이용했습니다. 로직은 package화 했으며,
main.py에서 추천 조건을 입력할 수 있어서 simple하고 dynamic한 주식을 추천 받을 수 있습니다. 


<h2> 필터링 조건 </h2>

<pre>
 GoodStock_conditions = {                
                "stockgb": 0,       #0:Kospi/1:Kosdoc
                "rank":100,         #시총 순위 (최대 500위)
                "per":[10,30],      #PER 최소~최대
                "roe":10            #ROE (기준 이상)
            }

 print('### Naver 증권 - 시가총액 기준 Crawling ###')
 crawler.crawlNaver(GoodStock_conditions)
 print('### Naver 증권 - 시가총액 기준 Crawling 완료 ###')
 </pre>


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
