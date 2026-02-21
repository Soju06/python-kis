# ST_FRGN_CODE

- 헤더: [https://raw.githubusercontent.com/koreainvestment/open-trading-api/main/stocks_info/%ED%95%B4%EC%99%B8%EC%A3%BC%EC%8B%9D%EC%A7%80%EC%88%98%EC%A0%95%EB%B3%B4.h](https://raw.githubusercontent.com/koreainvestment/open-trading-api/main/stocks_info/%ED%95%B4%EC%99%B8%EC%A3%BC%EC%8B%9D%EC%A7%80%EC%88%98%EC%A0%95%EB%B3%B4.h)
- 레코드 길이: `104`

| 필드명 | 타입 | 길이 | 설명 |
|---|---|---|---|
| `cls_code` | `char` | 1 | 구분코드<br>W : 세계주요지수<br>P : 미국지수<br>Q : 미국종목<br>H : 세계주요종목<br>D : 미국상장국내기업<br>G : 유럽상장국내기업<br>F : CME선물<br>M : 반도체<br>X : 환율<br>C : 상품선물<br>R : 국내금리<br>L : 리보금리<br>B : 주요국정부채 |
| `symb` | `char` | 10 | 심볼 |
| `hts_eng_isnm` | `char` | 39 | 영문명 |
| `hts_kor_isnm` | `char` | 40 | 한글명 |
| `bstp_cls_code` | `char` | 4 | 종목업종코드 |
| `dow_30_yn` | `char` | 1 | 다우30 편입종목여부 0:미편입 1:편입 |
| `nasdaq_100_yn` | `char` | 1 | 나스닥100 편입종목여부 0:미편입 1:편입 |
| `snp_500_yn` | `char` | 1 | S&P 500 편입종목여부 0:미편입 1:편입 |
| `exch_cls_code` | `char` | 4 | 거래소코드 |
| `ntnl_cls_code` | `char` | 3 | 국가구분코드 |
