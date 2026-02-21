# ST_FO_COM_CODE

- 헤더: [https://raw.githubusercontent.com/koreainvestment/open-trading-api/main/stocks_info/%EC%A2%85%EB%AA%A9%EB%A7%88%EC%8A%A4%ED%84%B0%EC%A0%95%EB%B3%B4%28%EC%83%81%ED%92%88%EC%84%A0%EB%AC%BC%EC%98%B5%EC%85%98%29.h](https://raw.githubusercontent.com/koreainvestment/open-trading-api/main/stocks_info/%EC%A2%85%EB%AA%A9%EB%A7%88%EC%8A%A4%ED%84%B0%EC%A0%95%EB%B3%B4%28%EC%83%81%ED%92%88%EC%84%A0%EB%AC%BC%EC%98%B5%EC%85%98%29.h)
- 레코드 길이: `116`

| 필드명 | 타입 | 길이 | 설명 |
|---|---|---|---|
| `com_type` | `char` | 1 | 상품구분<br>1:금리 2:통화 3:상품 |
| `info_type` | `char` | 1 | 1:선물 2:SP선물<br>5:콜옵션 6:풋옵션 |
| `shrn_iscd` | `char` | 9 | 단축코드 (SZ_SHRNCODE=9) |
| `stnd_iscd` | `char` | 12 | 표준코드 (SZ_STNDCODE=12) |
| `kor_name` | `char` | 40 | 한글종목명 (SZ_KORNAME=40) |
| `atm_cls_code` | `char` | 1 | ATM구분(1:ATM,2:ITM,3:OTM) |
| `acpr` | `char` | 8 | 행사가 |
| `mmsc_cls_code` | `char` | 1 | 월물구분코드 (0:연결선물, 1:최근월물<br>2:차근월물 3:차차근월물 4:차차차근월물<br>SP 는 무조건 1 |
| `prod_no` | `char` | 3 | 기초자산 단축코드<br>B03 : 3년국채 B05 : 5년국채<br>B10 : 10년국채 MSB : 통안증권<br>USD : 미국달러 JPY : 엔<br>EUR : 유로 GLD : 금<br>LHG : 돈육 CMU : CME미국달러<br>RFR : 3개월무위험금리 |
| `prod_name` | `char` | 40 | 기초자산 명 (SZ_KORNAME=40) |
