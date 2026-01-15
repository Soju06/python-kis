# ST_FO_IDX_CODE

- 헤더: [https://raw.githubusercontent.com/koreainvestment/open-trading-api/main/stocks_info/%EC%A2%85%EB%AA%A9%EB%A7%88%EC%8A%A4%ED%84%B0%EC%A0%95%EB%B3%B4%28%EC%A7%80%EC%88%98%EC%84%A0%EB%AC%BC%EC%98%B5%EC%85%98%29.h](https://raw.githubusercontent.com/koreainvestment/open-trading-api/main/stocks_info/%EC%A2%85%EB%AA%A9%EB%A7%88%EC%8A%A4%ED%84%B0%EC%A0%95%EB%B3%B4%28%EC%A7%80%EC%88%98%EC%84%A0%EB%AC%BC%EC%98%B5%EC%85%98%29.h)
- 레코드 길이: `121`

| 필드명 | 타입 | 길이 | 설명 |
|---|---|---|---|
| `info_type` | `char` | 1 | 1:지수선물 2:지수SP 3:스타선물 4:스타SP<br>5:지수콜옵션 6:지수풋옵션<br>7:변동성선물 8:변동성SP<br>9:섹터선물 A:섹터SP<br>B:미니선물 C:미니SP<br>D:미니콜옵션 E:미니풋옵션<br>J:코스닥150콜옵션 K:코스닥150풋옵션<br>L:위클리콜옵션 M:위클리풋옵션 |
| `shrn_iscd` | `char` | 9 | 단축코드 |
| `stnd_iscd` | `char` | 12 | 표준코드 |
| `kor_name` | `char` | 40 | 한글종목명 |
| `atm_cls_code` | `char` | 1 | ATM구분(1:ATM,2:ITM,3:OTM) |
| `acpr` | `char` | 8 | 행사가 |
| `mmsc_cls_code` | `char` | 1 | 월물구분코드 (0:연결선물, 1:최근월물<br>2:차근월물 3:차차근월물 4:차차차근월물 |
| `unas_shrn_iscd` | `char` | 9 | 기초자산 단축코드 |
| `unas_kor_name` | `char` | 40 | 기초자산 명 |
