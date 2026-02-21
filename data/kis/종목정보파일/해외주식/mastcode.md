# mastcode

- 헤더: [https://raw.githubusercontent.com/koreainvestment/open-trading-api/main/stocks_info/%ED%95%B4%EC%99%B8%EC%A2%85%EB%AA%A9%EC%BD%94%EB%93%9C%EC%A0%95%EB%B3%B4%28%EB%AF%B8%EA%B5%AD%2C%EC%A4%91%EA%B5%AD%2C%EC%9D%BC%EB%B3%B8%2C%ED%99%8D%EC%BD%A9%2C%EB%B2%A0%ED%8A%B8%EB%82%A8%29.h](https://raw.githubusercontent.com/koreainvestment/open-trading-api/main/stocks_info/%ED%95%B4%EC%99%B8%EC%A2%85%EB%AA%A9%EC%BD%94%EB%93%9C%EC%A0%95%EB%B3%B4%28%EB%AF%B8%EA%B5%AD%2C%EC%A4%91%EA%B5%AD%2C%EC%9D%BC%EB%B3%B8%2C%ED%99%8D%EC%BD%A9%2C%EB%B2%A0%ED%8A%B8%EB%82%A8%29.h)
- 레코드 길이: `266`

| 필드명 | 타입 | 길이 | 설명 |
|---|---|---|---|
| `ncod` | `char` | 3 | National code |
| `exid` | `char` | 4 | Exchange id |
| `excd` | `char` | 4 | Exchange code |
| `exnm` | `char` | 17 | Exchange name |
| `symb` | `char` | 17 | Symbol |
| `rsym` | `char` | 17 | realtime symbol |
| `knam` | `char` | 65 | Korea name |
| `enam` | `char` | 65 | English name |
| `stis` | `char` | 2 | Security type<br>1:Index<br>2:Stock<br>3:ETP(ETF)<br>4:Warrant |
| `curr` | `char` | 5 | currency |
| `zdiv` | `char` | 2 | float position |
| `ztyp` | `char` | 2 | data type |
| `base` | `char` | 13 | base price |
| `bnit` | `char` | 9 | Bid order size |
| `anit` | `char` | 9 | Ask order size |
| `mstm` | `char` | 5 | market start time(HHMM) |
| `metm` | `char` | 5 | market end time(HHMM) |
| `isdr` | `char` | 2 | DR 여부 :Y, N |
| `drcd` | `char` | 3 | DR 국가코드 |
| `icod` | `char` | 5 | 업종분류코드 |
| `sjong` | `char` | 2 | 지수구성종목 존재 여부<br>0:구성종목없음<br>1:구성종목있음 |
| `ttyp` | `char` | 2 | Tick size Type |
| `etyp` | `char` | 4 | 001: ETF 002: ETN 003: ETC 004: Others 005: VIX Underlying ETF 006: VIX Underlying ETN |
| `ttyp_sb` | `char` | 4 | Tick size type 상세 (ttyp 9일 경우 사용) : 런던 제트라 유로넥스트 |
