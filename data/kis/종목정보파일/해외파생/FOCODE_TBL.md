# FOCODE_TBL

- 헤더: [https://raw.githubusercontent.com/koreainvestment/open-trading-api/main/stocks_info/%ED%95%B4%EC%99%B8%EC%98%B5%EC%85%98%EC%A0%95%EB%B3%B4.h](https://raw.githubusercontent.com/koreainvestment/open-trading-api/main/stocks_info/%ED%95%B4%EC%99%B8%EC%98%B5%EC%85%98%EC%A0%95%EB%B3%B4.h)
- 레코드 길이: `344`

| 필드명 | 타입 | 길이 | 설명 |
|---|---|---|---|
| `sSrsCd` | `char` | 32 | 종목코드 (UNIQ-KEY) |
| `sAutoOrdGnrlYN` | `char` | 1 | 서버자동주문 가능 종목 여부 |
| `sAutoOrdTwapYN` | `char` | 1 | 서버자동주문 TWAP 가능 종목 여부 |
| `sAutoOrdEcnmYN` | `char` | 1 | 서버자동 경제지표 주문 가능 종목 여부 |
| `sExchSubCd` | `char` | 2 | 서브 거래소 코드 2019.12.27<br>10:ASX 20:BALTIC 30:BMF 40:CBOE<br>50:CME 51:CME_CBOT 52:CME_NYMEX 53:CME_COMEX<br>60:EUREX 70:FTX 80:HKEx<br>90:ICE_US 91:ICE_금융 92:ICE_상품 93:ICE_SG<br>A0:ISE B0:ITA C0:JSE D0:KCBT<br>E0:LBMA F0:LME G0:MDEX H0:MDX<br>I0:MEFF J0:NYSE K0:OSE L0:SGX<br>M0:SSE N0:TFEX O0:TMX P0:HNX |
| `sFiller` | `char` | 45 | 필러 |
| `sSeriesKrNm` | `char` | 50 | 종목한글명 |
| `sExchCd` | `char` | 10 | 거래소코드 |
| `sMrktCd` | `char` | 10 | 품목코드 |
| `sClasCd` | `char` | 3 | 품목종류<br>1: 지수옵션<br>2: 주식옵션 (M)<br>3: 현물옵션<br>4: 선물옵션<br>5: 주식옵션 (W) |
| `sDispDesz` | `char` | 5 | 출력 소수점 |
| `sCalcDesz` | `char` | 5 | 계산 소수점 |
| `sTickSz` | `char` | 14 | 틱사이즈 |
| `sTickVal` | `char` | 14 | 틱가치 |
| `sCtrtSz` | `char` | 10 | 계약크기 |
| `sDispDigit` | `char` | 4 | 가격표시진법 |
| `sMultiplier` | `char` | 10 | 환산승수 |
| `sSymbol` | `char` | 1 | 옵션 구분 C, P |
| `sStkPrc` | `char` | 20 | Strike Price |
| `sUndrInstr` | `char` | 10 | 관련선물코드<br>해외선물 품목 코드<br>주식옵션인 경우 거래소 코드<br>ex: NAS, NYS, AMS |
| `sUndrAsset` | `char` | 32 | 관련선물종목<br>해외선물 기초자산 종목코드<br>주식옵션인 경우 Ticker 코드<br>AAPL, TSLA |
| `sRefrAsset` | `char` | 32 | 참조자산 Index등<br>지수인경우 지수명<br>해외선물인경우 관련 선물 종목코드 |
| `sIncTickPrc` | `char` | 19 | 틱증가기준가 |
| `sIncTickSz` | `char` | 5 | 틱증가배수 |
| `sYearMon` | `char` | 6 | 년월 |
| `sAtmFlg` | `char` | 1 | A: ATM, I:ITM, O:OTM |
| `sNearFlg` | `char` | 1 | 근월물여부 0:원월물 1:근월물 |
