# ST_BOND_CODE

- 헤더: [https://raw.githubusercontent.com/koreainvestment/open-trading-api/main/stocks_info/%EC%A2%85%EB%AA%A9%EB%A7%88%EC%8A%A4%ED%84%B0%EC%A0%95%EB%B3%B4%28%EC%B1%84%EA%B6%8C%29.h](https://raw.githubusercontent.com/koreainvestment/open-trading-api/main/stocks_info/%EC%A2%85%EB%AA%A9%EB%A7%88%EC%8A%A4%ED%84%B0%EC%A0%95%EB%B3%B4%28%EC%B1%84%EA%B6%8C%29.h)
- 레코드 길이: `106`

| 필드명 | 타입 | 길이 | 설명 |
|---|---|---|---|
| `type` | `char` | 2 | A0:장내소매채권, F9:(주식관련사채, 소액채권), C0:국고채권 |
| `bond_cls_code` | `char` | 2 | A0: GA:국고채 MA:통안채 BA:금융채 SA:비금융특수채 CA:회사채<br>F9: 03:장내소액채권 02:기타채권 04:장내주식관련사채 MM:매매종류별<br>C0: GA:국고채 MA:통안채 BA:금융채 SA:비금융특수채 MB:지방채 99:기타 |
| `stnd_iscd` | `char` | 12 |  |
| `sname` | `char` | 40 |  |
| `bond_int_cls_code` | `char` | 2 | F9/C0 : 01:할인 02:복리 03:이표 04:금리연동 05:분할상환(거리복리)<br>06:분할(거치단리) 07:단리 08:FRN 09:복5단2<br>A0 : 고정금리형 11:할인채 12:복리채 13:이표채 14:단리채 15:복5단2 19:기타<br>A0 : 변동금리형 21:이표채 22:복리채 23:단리채 29:기타 |
| `lstn_date` | `char` | 8 | 상장일 |
| `pblc_date` | `char` | 8 | 발행 일자 |
| `rdmp_date` | `char` | 8 | 상환 일자 |
| `sale_date` | `char` | 8 | 매출 일자 |
| `srfc_intrt` | `char` | 8 | 표면 이자율(사용안함) |
| `rdmt_rate` | `char` | 8 | 만기 상환 비율(사용안함) |
