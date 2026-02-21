# ST_FO_STK_CODE

- 헤더: [https://raw.githubusercontent.com/koreainvestment/open-trading-api/main/stocks_info/%EC%A2%85%EB%AA%A9%EB%A7%88%EC%8A%A4%ED%84%B0%EC%A0%95%EB%B3%B4%28%EC%A3%BC%EC%8B%9D%EC%84%A0%EB%AC%BC%EC%98%B5%EC%85%98%29.h](https://raw.githubusercontent.com/koreainvestment/open-trading-api/main/stocks_info/%EC%A2%85%EB%AA%A9%EB%A7%88%EC%8A%A4%ED%84%B0%EC%A0%95%EB%B3%B4%28%EC%A3%BC%EC%8B%9D%EC%84%A0%EB%AC%BC%EC%98%B5%EC%85%98%29.h)
- 레코드 길이: `121`

| 필드명 | 타입 | 길이 | 설명 |
|---|---|---|---|
| `info_type` | `char` | 1 | 1:코스피 주식선물 2:코스피 주식선물 SP<br>3:코스닥 주식선물 4:코스닥 주식선물 SP<br>5:주식 콜옵션 6:주식 풋옵션 |
| `shrn_iscd` | `char` | 9 | 단축코드 |
| `stnd_iscd` | `char` | 12 | 표준코드 |
| `kor_name` | `char` | 40 | 한글종목명 |
| `atm_cls_code` | `char` | 1 | ATM구분(1:ATM,2:ITM,3:OTM) |
| `acpr` | `char` | 8 | 행사가 |
| `mmsc_cls_code` | `char` | 1 | 월물구분코드 (0:연결선물, 1:최근월물<br>2:차근월물 3:차차근월물 4:차차차근월물 |
| `unas_shrn_iscd` | `char` | 9 | 기초자산 단축코드 |
| `unas_kor_name` | `char` | 40 | 기초자산 명 |
