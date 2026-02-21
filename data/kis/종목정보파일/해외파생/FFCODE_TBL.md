# FFCODE_TBL

- 헤더: [https://raw.githubusercontent.com/koreainvestment/open-trading-api/main/stocks_info/%ED%95%B4%EC%99%B8%EC%84%A0%EB%AC%BC%EC%A0%95%EB%B3%B4.h](https://raw.githubusercontent.com/koreainvestment/open-trading-api/main/stocks_info/%ED%95%B4%EC%99%B8%EC%84%A0%EB%AC%BC%EC%A0%95%EB%B3%B4.h)
- 레코드 길이: `223`

| 필드명 | 타입 | 길이 | 설명 |
|---|---|---|---|
| `sSrsCd` | `char` | 32 | 종목코드 |
| `sAutoOrdGnrlYN` | `char` | 1 | 서버자동주문 가능 종목 여부 |
| `sAutoOrdTwapYN` | `char` | 1 | 서버자동주문 TWAP 가능 종목 여부 |
| `sAutoOrdEcnmYN` | `char` | 1 | 서버자동 경제지표 주문 가능 종목 여부 |
| `sFiller` | `char` | 47 | 필러 |
| `sSeriesKrNm` | `char` | 50 | 종목한글명 |
| `sExchCd` | `char` | 10 | 거래소코드 (ISAM KEY 1) |
| `sMrktCd` | `char` | 10 | 품목코드 (ISAM KEY 2) |
| `sClasCd` | `char` | 3 | 품목종류 |
| `sDispDesz` | `char` | 5 | 출력 소수점 |
| `sCalcDesz` | `char` | 5 | 계산 소수점 |
| `sTickSz` | `char` | 14 | 틱사이즈 |
| `sTickVal` | `char` | 14 | 틱가치 |
| `sCtrtSz` | `char` | 10 | 계약크기 |
| `sDispDigit` | `char` | 4 | 가격표시진법 |
| `sMultiplier` | `char` | 10 | 환산승수 |
| `sNearFlg` | `char` | 1 | 최다월물여부 0:원월물 1:최다월물 |
| `sNearFlgDt` | `char` | 1 | 최근월물여부 0:원월물 1:최근월물 |
| `sSprdYN` | `char` | 1 | 스프레드여부 |
| `sSprdLeg1YN` | `char` | 1 | 스프레드기준종목 LEG1 여부 Y/N |
| `sExchSubCd` | `char` | 2 | 서브 거래소 코드 |
