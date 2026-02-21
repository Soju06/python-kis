# Validator Candidate Param Patterns

- Source specs: tmp/docs/normalized/**/<endpoint>.json
- Candidate source: tmp/docs/reports/validation_hints_candidates.json

## 01fd59f1-e7f6-4192-8b02-d52e5dd7c8f3

- section: [국내주식] 종목정보 / 국내주식 / 종목정보
- name: 예탁원정보(상장정보일정)[국내주식-150]
- path: /uapi/domestic-stock/v1/ksdinfo/list-info

### required query
- SHT_CD | 종목코드 | 공백: 전체,  특정종목 조회시 : 종목코드
  - suggested_value:  (blank)
- T_DT | 조회일자To | ~ 일자
  - suggested_value: (needs manual)
- F_DT | 조회일자From | 일자 ~
  - suggested_value: (needs manual)
- CTS | CTS | 공백
  - suggested_value:  (blank)

## 05980ed5-8ab1-471a-975c-3e129841cbb8

- section: [해외주식] 시세분석 / 해외주식 / 시세분석
- name: 해외주식 거래증가율순위[해외주식-045]
- path: /uapi/overseas-stock/v1/ranking/trade-growth

### required query
- KEYB | NEXT KEY BUFF | 공백
  - suggested_value:  (blank)
- AUTH | 사용자권한정보 | 공백
  - suggested_value:  (blank)
- EXCD | 거래소코드 | 'NYS : 뉴욕, NAS : 나스닥,  AMS : 아멕스  HKS : 홍콩, SHS : 상해 , SZS : 심천 HSX : 호치민, HNX : 하노이 TSE : 도쿄 '
  - suggested_value: NYS (exchange_default)
- NDAY | N일자값 | N일전 : 0(당일), 1(2일), 2(3일), 3(5일), 4(10일), 5(20일전), 6(30일), 7(60일), 8(120일), 9(1년)
  - suggested_value: 0 (nday_default)
- VOL_RANG | 거래량조건 | 0(전체), 1(1백주이상), 2(1천주이상), 3(1만주이상), 4(10만주이상), 5(100만주이상), 6(1000만주이상)
  - suggested_value: 0 (all_value)

## 05a719af-aa3c-46c7-a670-55f2f11654c2

- section: [국내주식] 순위분석 / 국내주식 / 순위분석
- name: 국내주식 예상체결 상승/하락상위[v1_국내주식-103]
- path: /uapi/domestic-stock/v1/ranking/exp-trans-updown

### required query
- fid_rank_sort_cls_code | 순위 정렬 구분 코드 | 0:상승률1:상승폭2:보합3:하락율4:하락폭5:체결량6:거래대금
  - suggested_value: 0 (rank_default)
- fid_cond_mrkt_div_code | 조건 시장 분류 코드 | 시장구분코드 (주식 J)
  - suggested_value: J (market_default)
- fid_cond_scr_div_code | 조건 화면 분류 코드 | Unique key(20182)
  - suggested_value: 20182 (unique_key)
- fid_input_iscd | 입력 종목코드 | 0000:전체, 0001:거래소, 1001:코스닥, 2001:코스피200, 4001: KRX100
  - suggested_value: 0000 (all_value)
- fid_div_cls_code | 분류 구분 코드 | 0:전체 1:보통주 2:우선주
  - suggested_value: 0 (all_value)
- fid_aply_rang_prc_1 | 적용 범위 가격1 | 입력값 없을때 전체 (가격 ~)
  - suggested_value: (needs manual)
- fid_vol_cnt | 거래량 수 | 입력값 없을때 전체 (거래량 ~)
  - suggested_value: (needs manual)
- fid_pbmn | 거래대금 | 입력값 없을때 전체 (거래대금 ~) 천원단위
  - suggested_value: (needs manual)
- fid_blng_cls_code | 소속 구분 코드 | 0: 전체
  - suggested_value: 0 (all_value)
- fid_mkop_cls_code | 장운영 구분 코드 | 0:장전예상1:장마감예상
  - suggested_value: (needs manual)

## 0c2760ca-7fc9-4f41-9abd-33b2f5ff3b3b

- section: [국내주식] 순위분석 / 국내주식 / 순위분석
- name: 국내주식 신용잔고 상위[국내주식-109]
- path: /uapi/domestic-stock/v1/ranking/credit-balance

### required query
- FID_COND_SCR_DIV_CODE | 조건 화면 분류 코드 | Unique key(11701)
  - suggested_value: 11701 (unique_key)
- FID_INPUT_ISCD | 입력 종목코드 | 0000:전체, 0001:거래소, 1001:코스닥, 2001:코스피200,
  - suggested_value: 0000 (all_value)
- FID_OPTION | 증가율기간 | 2~999
  - suggested_value: (needs manual)
- FID_COND_MRKT_DIV_CODE | 조건 시장 분류 코드 | 시장구분코드 (주식 J)
  - suggested_value: J (market_default)
- FID_RANK_SORT_CLS_CODE | 순위 정렬 구분 코드 | '(융자)0:잔고비율 상위, 1: 잔고수량 상위, 2: 잔고금액 상위, 3: 잔고비율 증가상위, 4: 잔고비율 감소상위  (대주)5:잔고비율 상위, 6: 잔고수량 상위, 7: 잔고금액 상위, 8: 잔고비율 증가상위, 9: 잔고비율 감소상위 '
  - suggested_value: 0 (rank_default)

## 1394ba1d-e17d-42c8-8e53-6bed5dce7588

- section: [해외주식] 기본시세 / 해외주식 / 기본시세
- name: 해외결제일자조회[해외주식-017]
- path: /uapi/overseas-stock/v1/quotations/countries-holiday

### required query
- TRAD_DT | 기준일자 | 기준일자(YYYYMMDD)
  - suggested_value: (needs manual)
- CTX_AREA_NK | 연속조회키 | 공백으로 입력
  - suggested_value:  (blank)
- CTX_AREA_FK | 연속조회검색조건 | 공백으로 입력
  - suggested_value:  (blank)

## 2549b1c6-2c8c-4826-b632-74c0b68c24e9

- section: [해외주식] 시세분석 / 해외주식 / 시세분석
- name: 해외주식 가격급등락[해외주식-038]
- path: /uapi/overseas-stock/v1/ranking/price-fluct

### required query
- KEYB | NEXT KEY BUFF | 공백
  - suggested_value:  (blank)
- AUTH | 사용자권한정보 | 공백
  - suggested_value:  (blank)
- EXCD | 거래소코드 | 'NYS : 뉴욕, NAS : 나스닥,  AMS : 아멕스  HKS : 홍콩, SHS : 상해 , SZS : 심천 HSX : 호치민, HNX : 하노이 TSE : 도쿄 '
  - suggested_value: NYS (exchange_default)
- GUBN | 급등/급락구분 | 0(급락), 1(급등)
  - suggested_value: (needs manual)
- MIXN | N분전콤보값 | N분전 : 0(1분전), 1(2분전), 2(3분전), 3(5분전), 4(10분전), 5(15분전), 6(20분전), 7(30분전), 8(60분전), 9(120분전)
  - suggested_value: (needs manual)
- VOL_RANG | 거래량조건 | 0(전체), 1(1백주이상), 2(1천주이상), 3(1만주이상), 4(10만주이상), 5(100만주이상), 6(1000만주이상)
  - suggested_value: 0 (all_value)

## 264533d3-00eb-4794-984a-fecb84350f39

- section: [국내주식] ELW 시세 / 국내주식 / ELW 시세
- name: ELW 종목검색 [국내주식-166]
- path: /uapi/elw/v1/quotations/cond-search

### required query
- FID_COND_MRKT_DIV_CODE | 조건시장분류코드 | ELW(W)
  - suggested_value: E (market_default)
- FID_COND_SCR_DIV_CODE | 조건화면분류코드 | 화면번호(11510)
  - suggested_value: 11510 (screen_default)
- FID_RANK_SORT_CLS_CODE | 순위정렬구분코드 | '정렬1정렬안함(0)종목코드(1)현재가(2)대비율(3)거래량(4)행사가격(5) 전환비율(6)상장일(7)만기일(8)잔존일수(9)레버리지(10)'
  - suggested_value: 0 (rank_default)
- FID_INPUT_CNT_1 | 입력수1 | 정렬1기준 - 상위(1)하위(2)
  - suggested_value: (needs manual)
- FID_RANK_SORT_CLS_CODE_2 | 순위정렬구분코드2 | 정렬2
  - suggested_value: (needs manual)
- FID_INPUT_CNT_2 | 입력수2 | 정렬2기준 - 상위(1)하위(2)
  - suggested_value: (needs manual)
- FID_RANK_SORT_CLS_CODE_3 | 순위정렬구분코드3 | 정렬3
  - suggested_value: (needs manual)
- FID_INPUT_CNT_3 | 입력수3 | 정렬3기준 - 상위(1)하위(2)
  - suggested_value: (needs manual)
- FID_TRGT_CLS_CODE | 대상구분코드 | 0:발행회사종목코드,1:기초자산종목코드,2:FID시장구분코드,3:FID입력날짜1(상장일), 4:FID입력날짜2(만기일),5:LP회원사종목코드,6:행사가기초자산비교>=(1) <=(2),  7:잔존일 이상 이하, 8:현재가, 9:전일대비율, 10:거래량, 11:최종거래일, 12:레버리지
  - suggested_value: (needs manual)
- FID_INPUT_ISCD | 입력종목코드 | 발행사종목코드전체(00000)
  - suggested_value: 0000 (all_value)
- FID_UNAS_INPUT_ISCD | 기초자산입력종목코드 | 
  - suggested_value: (needs manual)
- FID_MRKT_CLS_CODE | 시장구분코드 | 권리유형전체(A)콜(CO)풋(PO)
  - suggested_value: (needs manual)
- FID_INPUT_DATE_1 | 입력날짜1 | 상장일전체(0)금일(1)7일이하(2)8~30일(3)31~90일(4)
  - suggested_value: 0 (all_value)
- FID_INPUT_DATE_2 | 입력날짜2 | 만기일전체(0)1개월(1)1~2(2)2~3(3)3~6(4)6~9(5)9~12(6)12이상(7)
  - suggested_value: 0 (all_value)
- FID_INPUT_ISCD_2 | 입력종목코드2 | 
  - suggested_value: (needs manual)
- FID_ETC_CLS_CODE | 기타구분코드 | 행사가전체(0)>=(1)
  - suggested_value: 0 (all_value)
- FID_INPUT_RMNN_DYNU_1 | 입력잔존일수1 | 잔존일이상
  - suggested_value: (needs manual)
- FID_INPUT_RMNN_DYNU_2 | 입력잔존일수2 | 잔존일이하
  - suggested_value: (needs manual)
- FID_PRPR_CNT1 | 현재가수1 | 현재가이상
  - suggested_value: (needs manual)
- FID_PRPR_CNT2 | 현재가수2 | 현재가이하
  - suggested_value: (needs manual)
- FID_RSFL_RATE1 | 등락비율1 | 전일대비율이상
  - suggested_value: (needs manual)
- FID_RSFL_RATE2 | 등락비율2 | 전일대비율이하
  - suggested_value: (needs manual)
- FID_VOL1 | 거래량1 | 거래량이상
  - suggested_value: (needs manual)
- FID_VOL2 | 거래량2 | 거래량이하
  - suggested_value: (needs manual)
- FID_APLY_RANG_PRC_1 | 적용범위가격1 | 최종거래일from
  - suggested_value: (needs manual)
- FID_APLY_RANG_PRC_2 | 적용범위가격2 | 최종거래일to
  - suggested_value: (needs manual)
- FID_LVRG_VAL1 | 레버리지값1 | 
  - suggested_value: (needs manual)
- FID_LVRG_VAL2 | 레버리지값2 | 
  - suggested_value: (needs manual)
- FID_VOL3 | 거래량3 | LP종료일from
  - suggested_value: (needs manual)
- FID_VOL4 | 거래량4 | LP종료일to
  - suggested_value: (needs manual)
- FID_INTS_VLTL1 | 내재변동성1 | 내재변동성이상
  - suggested_value: (needs manual)
- FID_INTS_VLTL2 | 내재변동성2 | 내재변동성이하
  - suggested_value: (needs manual)
- FID_PRMM_VAL1 | 프리미엄값1 | 프리미엄이상
  - suggested_value: (needs manual)
- FID_PRMM_VAL2 | 프리미엄값2 | 프리미엄이하
  - suggested_value: (needs manual)
- FID_GEAR1 | 기어링1 | 기어링이상
  - suggested_value: (needs manual)
- FID_GEAR2 | 기어링2 | 기어링이하
  - suggested_value: (needs manual)
- FID_PRLS_QRYR_RATE1 | 손익분기비율1 | 손익분기이상
  - suggested_value: (needs manual)
- FID_PRLS_QRYR_RATE2 | 손익분기비율2 | 손익분기이하
  - suggested_value: (needs manual)
- FID_DELTA1 | 델타1 | 델타이상
  - suggested_value: (needs manual)
- FID_DELTA2 | 델타2 | 델타이하
  - suggested_value: (needs manual)
- FID_ACPR1 | 행사가1 | 
  - suggested_value: (needs manual)
- FID_ACPR2 | 행사가2 | 
  - suggested_value: (needs manual)
- FID_STCK_CNVR_RATE1 | 주식전환비율1 | 전환비율이상
  - suggested_value: (needs manual)
- FID_STCK_CNVR_RATE2 | 주식전환비율2 | 전환비율이하
  - suggested_value: (needs manual)
- FID_DIV_CLS_CODE | 분류구분코드 | 0:전체,1:일반,2:조기종료
  - suggested_value: 0 (all_value)
- FID_PRIT1 | 패리티1 | 패리티이상
  - suggested_value: (needs manual)
- FID_PRIT2 | 패리티2 | 패리티이하
  - suggested_value: (needs manual)
- FID_CFP1 | 자본지지점1 | 배리어이상
  - suggested_value: (needs manual)
- FID_CFP2 | 자본지지점2 | 배리어이하
  - suggested_value: (needs manual)
- FID_INPUT_NMIX_PRICE_1 | 지수가격1 | LP보유비율이상
  - suggested_value: (needs manual)
- FID_INPUT_NMIX_PRICE_2 | 지수가격2 | LP보유비율이하
  - suggested_value: (needs manual)
- FID_EGEA_VAL1 | E기어링값1 | 접근도이상
  - suggested_value: (needs manual)
- FID_EGEA_VAL2 | E기어링값2 | 접근도이하
  - suggested_value: (needs manual)
- FID_INPUT_DVDN_ERT | 배당수익율 | 손익분기점이상
  - suggested_value: (needs manual)
- FID_INPUT_HIST_VLTL | 역사적변동성 | 손익분기점이하
  - suggested_value: (needs manual)
- FID_THETA1 | 세타1 | MONEYNESS이상
  - suggested_value: (needs manual)
- FID_THETA2 | 세타2 | MONEYNESS이하
  - suggested_value: (needs manual)

## 26c5165d-1910-4467-aed9-7213524b7546

- section: [국내주식] 종목정보 / 국내주식 / 종목정보
- name: 국내주식 재무비율[v1_국내주식-080]
- path: /uapi/domestic-stock/v1/finance/financial-ratio

### required query
- FID_DIV_CLS_CODE | 분류 구분 코드 | 0: 년, 1: 분기
  - suggested_value: 0 (div_default)
- fid_cond_mrkt_div_code | 조건 시장 분류 코드 | J
  - suggested_value: J (market_default)
- fid_input_iscd | 입력 종목코드 | 000660 : 종목코드
  - suggested_value: 0000 (input_default)

## 31d46ebe-2a19-4467-9dfb-a2d21adb1e61

- section: [해외선물옵션] 기본시세 / 해외선물옵션 / 기본시세
- name: 해외선물 분봉조회[해외선물-016]
- path: /uapi/overseas-futureoption/v1/quotations/inquire-time-futurechartprice

### required query
- SRS_CD | 종목코드 | ex) CNHU24 ※ 종목코드 "포럼 > FAQ > 종목정보 다운로드(해외) - 해외지수선물" 참고
  - suggested_value: CNHU24 ※ (example)
- EXCH_CD | 거래소코드 | CME
  - suggested_value: CME (exchange_default)
- START_DATE_TIME | 조회시작일시 | 공백
  - suggested_value:  (blank)
- CLOSE_DATE_TIME | 조회종료일시 | ex) 20230823
  - suggested_value: 20230823 (example)
- QRY_TP | 조회구분 | Q : 최초조회시 , P : 다음키(INDEX_KEY) 입력하여 조회시
  - suggested_value: Q (query_type_default)
- QRY_CNT | 요청개수 | 120 (조회갯수)
  - suggested_value: (needs manual)
- QRY_GAP | 묶음개수 | 5 (분간격)
  - suggested_value: (needs manual)
- INDEX_KEY | 이전조회KEY | 다음조회(QRY_TP를 P로 입력) 시, 이전 호출의 "output1 > index_key" 기입하여 조회
  - suggested_value:  (continuation_default)

## 3871dd9b-e9a5-471b-a0ce-d9ceb207ac5b

- section: [국내주식] 기본시세 / 국내주식 / 기본시세
- name: ETF 구성종목시세[국내주식-073]
- path: /uapi/etfetn/v1/quotations/inquire-component-stock-price

### required query
- FID_COND_MRKT_DIV_CODE | 조건시장분류코드 | 시장구분코드 (J)
  - suggested_value: J (market_default)
- FID_INPUT_ISCD | 입력종목코드 | 종목코드
  - suggested_value: 0000 (input_default)
- FID_COND_SCR_DIV_CODE | 조건화면분류코드 | Unique key( 11216 )
  - suggested_value: 11216 (unique_key)

## 3acd4025-6e95-46dc-a90d-b38215912d11

- section: [해외선물옵션] 기본시세 / 해외선물옵션 / 기본시세
- name: 해외선물옵션 장운영시간 [해외선물-030]
- path: /uapi/overseas-futureoption/v1/quotations/market-time

### required query
- FM_PDGR_CD | FM상품군코드 | 공백
  - suggested_value:  (blank)
- FM_CLAS_CD | FM클래스코드 | '공백(전체), 001(통화), 002(금리), 003(지수), 004(농산물),005(축산물),006(금속),007(에너지)'
  - suggested_value:  (blank)
- FM_EXCG_CD | FM거래소코드 | 'CME(CME), EUREX(EUREX), HKEx(HKEx), ICE(ICE), SGX(SGX), OSE(OSE), ASX(ASX), CBOE(CBOE), MDEX(MDEX), NYSE(NYSE), BMF(BMF),FTX(FTX), HNX(HNX), ETC(기타)'
  - suggested_value: (needs manual)
- OPT_YN | 옵션여부 | %(전체), N(선물), Y(옵션)
  - suggested_value: (needs manual)
- CTX_AREA_NK200 | 연속조회키200 | 
  - suggested_value: (needs manual)
- CTX_AREA_FK200 | 연속조회검색조건200 | 
  - suggested_value: (needs manual)

## 3cb7e131-7e44-4f34-831f-e6720b4a299a

- section: [해외주식] 시세분석 / 해외주식 / 시세분석
- name: 해외주식 거래대금순위[해외주식-044]
- path: /uapi/overseas-stock/v1/ranking/trade-pbmn

### required query
- KEYB | NEXT KEY BUFF | 공백
  - suggested_value:  (blank)
- AUTH | 사용자권한정보 | 공백
  - suggested_value:  (blank)
- EXCD | 거래소코드 | 'NYS : 뉴욕, NAS : 나스닥,  AMS : 아멕스  HKS : 홍콩, SHS : 상해 , SZS : 심천 HSX : 호치민, HNX : 하노이 TSE : 도쿄 '
  - suggested_value: NYS (exchange_default)
- NDAY | N일자값 | N일전 : 0(당일), 1(2일), 2(3일), 3(5일), 4(10일), 5(20일전), 6(30일), 7(60일), 8(120일), 9(1년)
  - suggested_value: 0 (nday_default)
- VOL_RANG | 거래량조건 | 0(전체), 1(1백주이상), 2(1천주이상), 3(1만주이상), 4(10만주이상), 5(100만주이상), 6(1000만주이상)
  - suggested_value: 0 (all_value)
- PRC1 | 현재가 필터범위 1 | 가격 ~
  - suggested_value: (needs manual)
- PRC2 | 현재가 필터범위 2 | ~ 가격
  - suggested_value: (needs manual)

## 3ed0247e-d717-43ed-85e9-51f952844687

- section: [국내주식] 시세분석 / 국내주식 / 시세분석
- name: 종목별 일별 대차거래추이 [국내주식-135]
- path: /uapi/domestic-stock/v1/quotations/daily-loan-trans

### required query
- MRKT_DIV_CLS_CODE | 조회구분 | 1(코스피), 2(코스닥), 3(종목)
  - suggested_value: (needs manual)
- MKSC_SHRN_ISCD | 종목코드 | 종목코드
  - suggested_value: (needs manual)
- START_DATE | 조회시작일시 | 조회기간 ~
  - suggested_value: (needs manual)
- END_DATE | 조회종료일시 | ~ 조회기간
  - suggested_value: (needs manual)
- CTS | 이전조회KEY | 
  - suggested_value:  (continuation_default)

## 40409c43-9bc7-447a-b09a-171d14b437f9

- section: [해외주식] 시세분석 / 해외주식 / 시세분석
- name: 해외주식 거래량급증[해외주식-039]
- path: /uapi/overseas-stock/v1/ranking/volume-surge

### required query
- KEYB | NEXT KEY BUFF | 공백
  - suggested_value:  (blank)
- AUTH | 사용자권한정보 | 공백
  - suggested_value:  (blank)
- EXCD | 거래소코드 | 'NYS : 뉴욕, NAS : 나스닥,  AMS : 아멕스  HKS : 홍콩, SHS : 상해 , SZS : 심천 HSX : 호치민, HNX : 하노이 TSE : 도쿄 '
  - suggested_value: NYS (exchange_default)
- MIXN | N분전콤보값 | N분전 : 0(1분전), 1(2분전), 2(3분전), 3(5분전), 4(10분전), 5(15분전), 6(20분전), 7(30분전), 8(60분전), 9(120분전)
  - suggested_value: (needs manual)
- VOL_RANG | 거래량조건 | 0(전체), 1(1백주이상), 2(1천주이상), 3(1만주이상), 4(10만주이상), 5(100만주이상), 6(1000만주이상)
  - suggested_value: 0 (all_value)

## 4360b745-0b9b-408e-8e0d-178138dbf864

- section: [해외주식] 시세분석 / 해외주식 / 시세분석
- name: 해외주식 신고/신저가[해외주식-042]
- path: /uapi/overseas-stock/v1/ranking/new-highlow

### required query
- KEYB | NEXT KEY BUFF | 공백
  - suggested_value:  (blank)
- AUTH | 사용자권한정보 | 공백
  - suggested_value:  (blank)
- EXCD | 거래소코드 | 'NYS : 뉴욕, NAS : 나스닥,  AMS : 아멕스  HKS : 홍콩, SHS : 상해 , SZS : 심천 HSX : 호치민, HNX : 하노이 TSE : 도쿄 '
  - suggested_value: NYS (exchange_default)
- GUBN | 신고/신저 구분 | 신고(1) 신저(0)
  - suggested_value: (needs manual)
- GUBN2 | 일시돌파/돌파 구분 | 일시돌파(0) 돌파유지(1)
  - suggested_value: (needs manual)
- NDAY | N일자값 | N일전 : 0(5일), 1(10일), 2(20일), 3(30일), 4(60일), 5(120일전), 6(52주), 7(1년)
  - suggested_value: 0 (nday_default)
- VOL_RANG | 거래량조건 | 0(전체), 1(1백주이상), 2(1천주이상), 3(1만주이상), 4(10만주이상), 5(100만주이상), 6(1000만주이상)
  - suggested_value: 0 (all_value)

## 43c17205-d112-4f9f-83f9-1704af8e4f79

- section: [국내주식] 종목정보 / 국내주식 / 종목정보
- name: 국내주식 당사 신용가능종목[국내주식-111]
- path: /uapi/domestic-stock/v1/quotations/credit-by-company

### required query
- fid_rank_sort_cls_code | 순위 정렬 구분 코드 | 0:코드순, 1:이름순
  - suggested_value: 0 (rank_default)
- fid_slct_yn | 선택 여부 | 0:신용주문가능, 1: 신용주문불가
  - suggested_value: (needs manual)
- fid_input_iscd | 입력 종목코드 | 0000:전체, 0001:거래소, 1001:코스닥, 2001:코스피200, 4001: KRX100
  - suggested_value: 0000 (all_value)
- fid_cond_scr_div_code | 조건 화면 분류 코드 | Unique key(20477)
  - suggested_value: 20477 (unique_key)
- fid_cond_mrkt_div_code | 조건 시장 분류 코드 | 시장구분코드 (주식 J)
  - suggested_value: J (market_default)

## 4a077f43-7053-47be-b811-8e35be4ea745

- section: [국내주식] 시세분석 / 국내주식 / 시세분석
- name: 국내기관_외국인 매매종목가집계[국내주식-037]
- path: /uapi/domestic-stock/v1/quotations/foreign-institution-total

### required query
- FID_COND_MRKT_DIV_CODE | 시장 분류 코드 | V(Default)
  - suggested_value: J (market_default)
- FID_COND_SCR_DIV_CODE | 조건 화면 분류 코드 | 16449(Default)
  - suggested_value: 16449 (screen_default)
- FID_INPUT_ISCD | 입력 종목코드 | 0000:전체, 0001:코스피, 1001:코스닥 ... 포탈 (FAQ : 종목정보 다운로드(국내) - 업종코드 참조)
  - suggested_value: 0000 (all_value)
- FID_DIV_CLS_CODE | 분류 구분 코드 | 0: 수량정열, 1: 금액정열
  - suggested_value: 0 (div_default)
- FID_RANK_SORT_CLS_CODE | 순위 정렬 구분 코드 | 0: 순매수상위, 1: 순매도상위
  - suggested_value: 0 (rank_default)
- FID_ETC_CLS_CODE | 기타 구분  정렬 | 0:전체 1:외국인 2:기관계 3:기타
  - suggested_value: 0 (all_value)

## 506cd6e9-97d9-4c4b-82bc-6a6c13586885

- section: [해외선물옵션] 기본시세 / 해외선물옵션 / 기본시세
- name: 해외옵션 호가 [해외선물-033]
- path: /uapi/overseas-futureoption/v1/quotations/opt-asking-price

### required query
- SRS_CD | 종목명 | 예)OESM24 C5340
  - suggested_value: OESM24 C5340 (example)

## 50775574-8832-4db8-aeb5-51a32c8250ed

- section: [국내주식] 시세분석 / 국내주식 / 시세분석
- name: 주식현재가 회원사 종목매매동향 [국내주식-197]
- path: /uapi/domestic-stock/v1/quotations/inquire-member-daily

### required query
- FID_COND_MRKT_DIV_CODE | 조건시장분류코드 | J: KRX, NX: NXT, UN: 통합
  - suggested_value: J (market_default)
- FID_INPUT_ISCD | 입력종목코드 | 주식종목코드입력
  - suggested_value: 0000 (input_default)
- FID_INPUT_ISCD_2 | 회원사코드 | 회원사코드 (kis developers 포탈 사이트 포럼-> FAQ -> 종목정보 다운로드(국내) > 회원사 참조)
  - suggested_value: (needs manual)
- FID_INPUT_DATE_1 | 입력날짜1 | 날짜 ~
  - suggested_value: (needs manual)
- FID_INPUT_DATE_2 | 입력날짜2 | ~ 날짜
  - suggested_value: (needs manual)
- FID_SCTN_CLS_CODE | 구간구분코드 | 공백
  - suggested_value:  (blank)

## 65db61e3-49a5-4a95-9cf3-61298c7b8461

- section: [해외주식] 기본시세 / 해외주식 / 기본시세
- name: 해외주식조건검색[v1_해외주식-015]
- path: /uapi/overseas-price/v1/quotations/inquire-search

### required query
- EXCD | 거래소코드 | NYS : 뉴욕, NAS : 나스닥,  AMS : 아멕스  HKS : 홍콩, SHS : 상해 , SZS : 심천 HSX : 호치민, HNX : 하노이 TSE : 도쿄
  - suggested_value: NYS (exchange_default)

## 72e63cb2-2ab1-41a0-8ab9-62cbeaa5eea0

- section: [국내주식] 순위분석 / 국내주식 / 순위분석
- name: 국내주식 신고/신저근접종목 상위[v1_국내주식-105]
- path: /uapi/domestic-stock/v1/ranking/near-new-highlow

### required query
- fid_aply_rang_vol | 적용 범위 거래량 | 0: 전체, 100: 100주 이상
  - suggested_value: 0 (all_value)
- fid_cond_mrkt_div_code | 조건 시장 분류 코드 | 시장구분코드 (주식 J)
  - suggested_value: J (market_default)
- fid_cond_scr_div_code | 조건 화면 분류 코드 | Unique key(20187)
  - suggested_value: 20187 (unique_key)
- fid_div_cls_code | 분류 구분 코드 | 0:전체, 1:관리종목, 2:투자주의, 3:투자경고
  - suggested_value: 0 (all_value)
- fid_input_cnt_1 | 입력 수1 | 괴리율 최소
  - suggested_value: (needs manual)
- fid_input_cnt_2 | 입력 수2 | 괴리율 최대
  - suggested_value: (needs manual)
- fid_prc_cls_code | 가격 구분 코드 | 0:신고근접, 1:신저근접
  - suggested_value: (needs manual)
- fid_input_iscd | 입력 종목코드 | 0000:전체, 0001:거래소, 1001:코스닥, 2001:코스피200, 4001: KRX100
  - suggested_value: 0000 (all_value)
- fid_trgt_cls_code | 대상 구분 코드 | 0: 전체
  - suggested_value: 0 (all_value)
- fid_trgt_exls_cls_code | 대상 제외 구분 코드 | 0:전체, 1:관리종목, 2:투자주의, 3:투자경고, 4:투자위험예고, 5:투자위험, 6:보통주, 7:우선주
  - suggested_value: 0 (all_value)
- fid_aply_rang_prc_1 | 적용 범위 가격1 | 가격 ~
  - suggested_value: (needs manual)
- fid_aply_rang_prc_2 | 적용 범위 가격2 | ~ 가격
  - suggested_value: (needs manual)

## 7bdbff93-1334-496f-a9b8-7da6032f7407

- section: [국내주식] 순위분석 / 국내주식 / 순위분석
- name: 국내주식 대량체결건수 상위[국내주식-107]
- path: /uapi/domestic-stock/v1/ranking/bulk-trans-num

### required query
- fid_aply_rang_prc_2 | 적용 범위 가격2 | ~ 가격
  - suggested_value: (needs manual)
- fid_cond_mrkt_div_code | 조건 시장 분류 코드 | 시장구분코드 (J:KRX, NX:NXT)
  - suggested_value: J (market_default)
- fid_cond_scr_div_code | 조건 화면 분류 코드 | Unique key(11909)
  - suggested_value: 11909 (unique_key)
- fid_input_iscd | 입력 종목코드 | 0000:전체, 0001:거래소, 1001:코스닥, 2001:코스피200, 4001: KRX100
  - suggested_value: 0000 (all_value)
- fid_rank_sort_cls_code | 순위 정렬 구분 코드 | 0:매수상위, 1:매도상위
  - suggested_value: 0 (rank_default)
- fid_div_cls_code | 분류 구분 코드 | 0:전체
  - suggested_value: 0 (all_value)
- fid_input_price_1 | 입력 가격1 | 건별금액 ~
  - suggested_value: (needs manual)
- fid_aply_rang_prc_1 | 적용 범위 가격1 | 가격 ~
  - suggested_value: (needs manual)
- fid_input_iscd_2 | 입력 종목코드2 | 공백:전체종목, 개별종목 조회시 종목코드 (000660)
  - suggested_value:  (blank)
- fid_trgt_exls_cls_code | 대상 제외 구분 코드 | 0:전체
  - suggested_value: 0 (all_value)
- fid_trgt_cls_code | 대상 구분 코드 | 0:전체
  - suggested_value: 0 (all_value)
- fid_vol_cnt | 거래량 수 | 거래량 ~
  - suggested_value: (needs manual)

## 7d1b2345-32f8-463b-9f41-8b4602387d52

- section: [국내주식] 업종/기타 / 국내주식 / 업종/기타
- name: 국내주식 예상체결 전체지수[국내주식-122]
- path: /uapi/domestic-stock/v1/quotations/exp-total-index

### required query
- fid_mrkt_cls_code | 시장 구분 코드 | 0:전체 K:거래소 Q:코스닥
  - suggested_value: 0 (all_value)
- fid_cond_mrkt_div_code | 조건 시장 분류 코드 | 시장구분코드 (업종 U)
  - suggested_value: J (market_default)
- fid_cond_scr_div_code | 조건 화면 분류 코드 | Unique key(11175)
  - suggested_value: 11175 (unique_key)
- fid_input_iscd | 입력 종목코드 | 0000:전체, 0001:거래소, 1001:코스닥, 2001:코스피200, 4001: KRX100
  - suggested_value: 0000 (all_value)
- fid_mkop_cls_code | 장운영 구분 코드 | 1:장시작전, 2:장마감
  - suggested_value: (needs manual)

## 7d30b578-018d-4250-852a-7599211ff988

- section: [해외주식] 시세분석 / 해외주식 / 시세분석
- name: 해외주식 거래회전율순위[해외주식-046]
- path: /uapi/overseas-stock/v1/ranking/trade-turnover

### required query
- KEYB | NEXT KEY BUFF | 공백
  - suggested_value:  (blank)
- AUTH | 사용자권한정보 | 공백
  - suggested_value:  (blank)
- EXCD | 거래소코드 | 'NYS : 뉴욕, NAS : 나스닥,  AMS : 아멕스  HKS : 홍콩, SHS : 상해 , SZS : 심천 HSX : 호치민, HNX : 하노이 TSE : 도쿄 '
  - suggested_value: NYS (exchange_default)
- NDAY | N일자값 | N일전 : 0(당일), 1(2일), 2(3일), 3(5일), 4(10일), 5(20일전), 6(30일), 7(60일), 8(120일), 9(1년)
  - suggested_value: 0 (nday_default)
- VOL_RANG | 거래량조건 | 0(전체), 1(1백주이상), 2(1천주이상), 3(1만주이상), 4(10만주이상), 5(100만주이상), 6(1000만주이상)
  - suggested_value: 0 (all_value)

## 8702dab4-008d-4849-8f24-a91b57872a80

- section: [해외선물옵션] 기본시세 / 해외선물옵션 / 기본시세
- name: 해외선물 체결추이(월간)[해외선물-020]
- path: /uapi/overseas-futureoption/v1/quotations/monthly-ccnl

### required query
- SRS_CD | 종목코드 | 예) 6AM24
  - suggested_value: 6AM24 (example)
- EXCH_CD | 거래소코드 | 예) CME
  - suggested_value: CME (example)
- START_DATE_TIME | 조회시작일시 | 공백
  - suggested_value:  (blank)
- CLOSE_DATE_TIME | 조회종료일시 | 예) 20240402
  - suggested_value: 20240402 (example)
- QRY_TP | 조회구분 | Q : 최초조회시 , P : 다음키(INDEX_KEY) 입력하여 조회시
  - suggested_value: Q (query_type_default)
- QRY_CNT | 요청개수 | 예) 30 (최대 40)
  - suggested_value: 30 (최대 (example)
- QRY_GAP | 묶음개수 | 공백 (분만 사용)
  - suggested_value:  (blank)
- INDEX_KEY | 이전조회KEY | 공백
  - suggested_value:  (blank)

## 89e1ffde-0cda-4426-8277-72710c193cf2

- section: [국내선물옵션] 기본시세 / 국내선물옵션 / 기본시세
- name: 국내옵션전광판_옵션월물리스트[국내선물-020]
- path: /uapi/domestic-futureoption/v1/quotations/display-board-option-list

### required query
- FID_COND_SCR_DIV_CODE | 조건 화면 분류 코드 | Unique key(509)
  - suggested_value: 509 (unique_key)
- FID_COND_MRKT_DIV_CODE | 조건 시장 분류 코드 | 공백
  - suggested_value:  (blank)
- FID_COND_MRKT_CLS_CODE | 조건 시장 구분 코드 | 공백
  - suggested_value:  (blank)

## 8c473311-ecfd-428f-9ec2-0b574d8592b9

- section: [해외선물옵션] 기본시세 / 해외선물옵션 / 기본시세
- name: 해외선물 체결추이(일간)[해외선물-018]
- path: /uapi/overseas-futureoption/v1/quotations/daily-ccnl

### required query
- SRS_CD | 종목코드 | 예) 6AM24
  - suggested_value: 6AM24 (example)
- EXCH_CD | 거래소코드 | 예) CME
  - suggested_value: CME (example)
- START_DATE_TIME | 조회시작일시 | 공백
  - suggested_value:  (blank)
- CLOSE_DATE_TIME | 조회종료일시 | 예) 20240402
  - suggested_value: 20240402 (example)
- QRY_TP | 조회구분 | Q : 최초조회시 , P : 다음키(INDEX_KEY) 입력하여 조회시
  - suggested_value: Q (query_type_default)
- QRY_CNT | 요청개수 | 예) 30 (최대 40)
  - suggested_value: 30 (최대 (example)
- QRY_GAP | 묶음개수 | 공백 (분만 사용)
  - suggested_value:  (blank)
- INDEX_KEY | 이전조회KEY | 공백
  - suggested_value:  (blank)

## 9064a50c-0545-4b6c-8eb2-034f5214974b

- section: [해외주식] 시세분석 / 해외주식 / 시세분석
- name: 해외뉴스종합(제목) [해외주식-053]
- path: /uapi/overseas-price/v1/quotations/news-title

### required query
- INFO_GB | 뉴스구분 | 전체: 공백
  - suggested_value:  (blank)
- CLASS_CD | 중분류 | 전체: 공백
  - suggested_value:  (blank)
- NATION_CD | 국가코드 | 전체: 공백 CN(중국), HK(홍콩), US(미국)
  - suggested_value:  (blank)
- EXCHANGE_CD | 거래소코드 | 전체: 공백
  - suggested_value:  (blank)
- SYMB | 종목코드 | 전체: 공백
  - suggested_value:  (blank)
- DATA_DT | 조회일자 | 전체: 공백 특정일자(YYYYMMDD) ex. 20240502
  - suggested_value:  (blank)
- DATA_TM | 조회시간 | 전체: 공백 전체: 공백 특정시간(HHMMSS) ex. 093500
  - suggested_value:  (blank)
- CTS | 다음키 | 공백 입력
  - suggested_value:  (blank)

## 967e60c7-f1eb-4f23-b893-71747556ad49

- section: [해외주식] 시세분석 / 해외주식 / 시세분석
- name: 당사 해외주식담보대출 가능 종목 [해외주식-051]
- path: /uapi/overseas-price/v1/quotations/colable-by-company

### required query
- PDNO | 상품번호 | ex)AMD
  - suggested_value: AMD (example)
- PRDT_TYPE_CD | 상품유형코드 | 공백
  - suggested_value:  (blank)
- INQR_STRT_DT | 조회시작일자 | 공백
  - suggested_value:  (blank)
- INQR_END_DT | 조회종료일자 | 공백
  - suggested_value:  (blank)
- INQR_DVSN | 조회구분 | 공백
  - suggested_value:  (blank)
- NATN_CD | 국가코드 | 840(미국), 344(홍콩), 156(중국)
  - suggested_value: (needs manual)
- INQR_SQN_DVSN | 조회순서구분 | 01(이름순), 02(코드순)
  - suggested_value: (needs manual)
- RT_DVSN_CD | 비율구분코드 | 공백
  - suggested_value:  (blank)
- RT | 비율 | 공백
  - suggested_value:  (blank)
- LOAN_PSBL_YN | 대출가능여부 | 공백
  - suggested_value:  (blank)
- CTX_AREA_FK100 | 연속조회검색조건100 | 공백
  - suggested_value:  (blank)
- CTX_AREA_NK100 | 연속조회키100 | 공백
  - suggested_value:  (blank)

## a27c026a-744f-4ddd-9d35-c35b285af74c

- section: [국내주식] 종목정보 / 국내주식 / 종목정보
- name: 국내주식 안정성비율[v1_국내주식-083]
- path: /uapi/domestic-stock/v1/finance/stability-ratio

### required query
- fid_input_iscd | 입력 종목코드 | 000660 : 종목코드
  - suggested_value: 0000 (input_default)
- fid_div_cls_code | 분류 구분 코드 | 0: 년, 1: 분기
  - suggested_value: 0 (div_default)
- fid_cond_mrkt_div_code | 조건 시장 분류 코드 | J
  - suggested_value: J (market_default)

## a4275fc3-384b-4b24-bf3a-38b72786b5ab

- section: [국내주식] 종목정보 / 국내주식 / 종목정보
- name: 국내주식 수익성비율[v1_국내주식-081]
- path: /uapi/domestic-stock/v1/finance/profit-ratio

### required query
- fid_input_iscd | 입력 종목코드 | 000660 : 종목코드
  - suggested_value: 0000 (input_default)
- FID_DIV_CLS_CODE | 분류 구분 코드 | 0: 년, 1: 분기
  - suggested_value: 0 (div_default)
- fid_cond_mrkt_div_code | 조건 시장 분류 코드 | J
  - suggested_value: J (market_default)

## ae084fcd-7a30-4a14-8483-91a7fc918d23

- section: [해외주식] 시세분석 / 해외주식 / 시세분석
- name: 해외주식 시가총액순위[해외주식-047]
- path: /uapi/overseas-stock/v1/ranking/market-cap

### required query
- KEYB | NEXT KEY BUFF | 공백
  - suggested_value:  (blank)
- AUTH | 사용자권한정보 | 공백
  - suggested_value:  (blank)
- EXCD | 거래소코드 | 'NYS : 뉴욕, NAS : 나스닥,  AMS : 아멕스  HKS : 홍콩, SHS : 상해 , SZS : 심천 HSX : 호치민, HNX : 하노이 TSE : 도쿄 '
  - suggested_value: NYS (exchange_default)
- VOL_RANG | 거래량조건 | 0(전체), 1(1백주이상), 2(1천주이상), 3(1만주이상), 4(10만주이상), 5(100만주이상), 6(1000만주이상)
  - suggested_value: 0 (all_value)

## b664e9df-7ab6-4b89-89a0-5537ae380caf

- section: [국내주식] 시세분석 / 국내주식 / 시세분석
- name: 프로그램매매 투자자매매동향(당일) [국내주식-116]
- path: /uapi/domestic-stock/v1/quotations/investor-program-trade-today

### required query
- EXCH_DIV_CLS_CODE | 거래소 구분 코드 | J : KRX, NX : NXT, UN : 통합
  - suggested_value: (needs manual)
- MRKT_DIV_CLS_CODE | 시장 구분 코드 | 1:코스피, 4:코스닥
  - suggested_value: (needs manual)

## bac2f657-36b1-4538-aabc-0bee8ba77229

- section: [해외주식] 시세분석 / 해외주식 / 시세분석
- name: 해외주식 상승율/하락율[해외주식-041]
- path: /uapi/overseas-stock/v1/ranking/updown-rate

### required query
- KEYB | NEXT KEY BUFF | 공백
  - suggested_value:  (blank)
- AUTH | 사용자권한정보 | 공백
  - suggested_value:  (blank)
- EXCD | 거래소코드 | 'NYS : 뉴욕, NAS : 나스닥,  AMS : 아멕스  HKS : 홍콩, SHS : 상해 , SZS : 심천 HSX : 호치민, HNX : 하노이 TSE : 도쿄 '
  - suggested_value: NYS (exchange_default)
- GUBN | 상승율/하락율 구분 | 0(하락율), 1(상승율)
  - suggested_value: (needs manual)
- NDAY | N일자값 | N일전 : 0(당일), 1(2일), 2(3일), 3(5일), 4(10일), 5(20일전), 6(30일), 7(60일), 8(120일), 9(1년)
  - suggested_value: 0 (nday_default)
- VOL_RANG | 거래량조건 | 0(전체), 1(1백주이상), 2(1천주이상), 3(1만주이상), 4(10만주이상), 5(100만주이상), 6(1000만주이상)
  - suggested_value: 0 (all_value)

## c5933de1-4016-485a-a9ff-729818881d28

- section: [국내주식] 종목정보 / 국내주식 / 종목정보
- name: 국내주식 손익계산서[v1_국내주식-079]
- path: /uapi/domestic-stock/v1/finance/income-statement

### required query
- FID_DIV_CLS_CODE | 분류 구분 코드 | 0: 년, 1: 분기  ※ 분기데이터는 연단위 누적합산
  - suggested_value: 0 (div_default)
- fid_cond_mrkt_div_code | 조건 시장 분류 코드 | J
  - suggested_value: J (market_default)
- fid_input_iscd | 입력 종목코드 | 000660 : 종목코드
  - suggested_value: 0000 (input_default)

## ca0f8e3e-9f99-4ebd-a81c-c5f8017c4d65

- section: [국내주식] 종목정보 / 국내주식 / 종목정보
- name: 당사 대주가능 종목 [국내주식-195]
- path: /uapi/domestic-stock/v1/quotations/lendable-by-company

### required query
- EXCG_DVSN_CD | 거래소구분코드 | 00(전체), 02(거래소), 03(코스닥)
  - suggested_value: 0 (all_value)
- PDNO | 상품번호 | 공백 : 전체조회, 종목코드 입력 시 해당종목만 조회
  - suggested_value:  (blank)
- THCO_STLN_PSBL_YN | 당사대주가능여부 | Y
  - suggested_value: (needs manual)
- INQR_DVSN_1 | 조회구분1 | 0 : 전체조회, 1: 종목코드순 정렬
  - suggested_value: 0 (all_value)
- CTX_AREA_FK200 | 연속조회검색조건200 | 미입력 (다음조회 불가)
  - suggested_value: (needs manual)
- CTX_AREA_NK100 | 연속조회키100 | 미입력 (다음조회 불가)
  - suggested_value: (needs manual)

## ca2e71e1-5ef4-4489-b4c4-118e10588690

- section: [국내주식] ELW 시세 / 국내주식 / ELW 시세
- name: ELW 비교대상종목조회 [국내주식-183]
- path: /uapi/elw/v1/quotations/compare-stocks

### required query
- FID_COND_SCR_DIV_CODE | 조건화면분류코드 | 11517(Primary key)
  - suggested_value: 11517 (screen_default)
- FID_INPUT_ISCD | 입력종목코드 | 종목코드(ex)005930(삼성전자))
  - suggested_value: 005930(삼성전자 (example)

## cd2e4d9a-7e3d-44ff-9b68-36d971655c24

- section: [해외선물옵션] 기본시세 / 해외선물옵션 / 기본시세
- name: 해외선물 체결추이(주간)[해외선물-017]
- path: /uapi/overseas-futureoption/v1/quotations/weekly-ccnl

### required query
- SRS_CD | 종목코드 | 예) 6AM24
  - suggested_value: 6AM24 (example)
- EXCH_CD | 거래소코드 | 예) CME
  - suggested_value: CME (example)
- START_DATE_TIME | 조회시작일시 | 공백
  - suggested_value:  (blank)
- CLOSE_DATE_TIME | 조회종료일시 | 예) 20240402
  - suggested_value: 20240402 (example)
- QRY_TP | 조회구분 | Q : 최초조회시 , P : 다음키(INDEX_KEY) 입력하여 조회시
  - suggested_value: Q (query_type_default)
- QRY_CNT | 요청개수 | 예) 30 (최대 40)
  - suggested_value: 30 (최대 (example)
- QRY_GAP | 묶음개수 | 공백 (분만 사용)
  - suggested_value:  (blank)
- INDEX_KEY | 이전조회KEY | 공백
  - suggested_value:  (blank)

## d5dc7247-6f82-4cd7-8133-afabd8f003f7

- section: [해외선물옵션] 기본시세 / 해외선물옵션 / 기본시세
- name: 해외선물 미결제추이 [해외선물-029]
- path: /uapi/overseas-futureoption/v1/quotations/investor-unpd-trend

### required query
- PROD_ISCD | 상품 | 금리 (GE, ZB, ZF,ZN,ZT), 금속(GC, PA, PL,SI, HG), 농산물(CC, CT,KC, OJ, SB, ZC,ZL, ZM, ZO, ZR, ZS, ZW), 에너지(CL, HO, NG, WBS), 지수(ES, NQ, TF, YM, VX), 축산물(GF, HE, LE), 통화(6A, 6B, 6C, 6E, 6J, 6N, 6S, DX)
  - suggested_value: (needs manual)
- BSOP_DATE | 일자 | 기준일(ex)20240513)
  - suggested_value: 20240513 (example)
- UPMU_GUBUN | 구분 | 0(수량), 1(증감)
  - suggested_value: (needs manual)
- CTS_KEY | CTS_KEY | 공백
  - suggested_value:  (blank)

## dd867a76-745d-4268-8ff8-b3e7f71e6e83

- section: [국내주식] 기본시세 / 국내주식 / 기본시세
- name: NAV 비교추이(분)[v1_국내주식-070]
- path: /uapi/etfetn/v1/quotations/nav-comparison-time-trend

### required query
- fid_hour_cls_code | FID 시간 구분 코드 | 1분 :60, 3분: 180 … 120분:7200
  - suggested_value: (needs manual)
- fid_cond_mrkt_div_code | FID 조건 시장 분류 코드 | E - 고정값
  - suggested_value: E (fixed_value)
- fid_input_iscd | FID 입력 종목코드 | 종목코드
  - suggested_value: 0000 (input_default)

## dfd2502e-0d5c-4999-8a24-84ff15a74696

- section: [국내주식] 순위분석 / 국내주식 / 순위분석
- name: 국내주식 시장가치 순위[v1_국내주식-096]
- path: /uapi/domestic-stock/v1/ranking/market-value

### required query
- fid_trgt_cls_code | 대상 구분 코드 | 0 : 전체
  - suggested_value: 0 (all_value)
- fid_cond_mrkt_div_code | 조건 시장 분류 코드 | 시장구분코드 (J:KRX, NX:NXT)
  - suggested_value: J (market_default)
- fid_cond_scr_div_code | 조건 화면 분류 코드 | Unique key( 20179 )
  - suggested_value: 20179 (unique_key)
- fid_input_iscd | 입력 종목코드 | 0000:전체, 0001:거래소, 1001:코스닥, 2001:코스피200
  - suggested_value: 0000 (all_value)
- fid_div_cls_code | 분류 구분 코드 | 0: 전체, 1:관리종목, 2:투자주의, 3:투자경고, 4:투자위험예고, 5:투자위험, 6:보톧주, 7:우선주
  - suggested_value: 0 (all_value)
- fid_input_price_1 | 입력 가격1 | 입력값 없을때 전체 (가격 ~)
  - suggested_value: (needs manual)
- fid_input_price_2 | 입력 가격2 | 입력값 없을때 전체 (~ 가격)
  - suggested_value: (needs manual)
- fid_vol_cnt | 거래량 수 | 입력값 없을때 전체 (거래량 ~)
  - suggested_value: (needs manual)
- fid_input_option_1 | 입력 옵션1 | 회계연도 입력 (ex 2023)
  - suggested_value: (needs manual)
- fid_input_option_2 | 입력 옵션2 | 0: 1/4분기 , 1: 반기, 2: 3/4분기, 3: 결산
  - suggested_value: (needs manual)
- fid_rank_sort_cls_code | 순위 정렬 구분 코드 | '가치분석(23:PER, 24:PBR, 25:PCR, 26:PSR, 27: EPS, 28:EVA, 29: EBITDA, 30: EV/EBITDA, 31:EBITDA/금융비율'
  - suggested_value: 0 (rank_default)
- fid_blng_cls_code | 소속 구분 코드 | 0 : 전체
  - suggested_value: 0 (all_value)
- fid_trgt_exls_cls_code | 대상 제외 구분 코드 | 0 : 전체
  - suggested_value: 0 (all_value)

## e0f9b38e-774a-441e-8dbd-27ab5f5ebb8b

- section: [국내주식] 종목정보 / 국내주식 / 종목정보
- name: 예탁원정보(유상증자일정) [국내주식-143]
- path: /uapi/domestic-stock/v1/ksdinfo/paidin-capin

### required query
- CTS | CTS | 공백
  - suggested_value:  (blank)
- GB1 | 조회구분 | 1(청약일별), 2(기준일별)
  - suggested_value: (needs manual)
- F_DT | 조회일자From | 일자 ~
  - suggested_value: (needs manual)
- T_DT | 조회일자To | ~ 일자
  - suggested_value: (needs manual)
- SHT_CD | 종목코드 | 공백(전체),  특정종목 조회시(종목코드)
  - suggested_value:  (blank)

## e27baf2f-6ec0-4029-b4fd-4c873f340478

- section: [국내주식] 기본시세 / 국내주식 / 기본시세
- name: 주식현재가 투자자[v1_국내주식-012]
- path: /uapi/domestic-stock/v1/quotations/inquire-investor

### required query
- FID_COND_MRKT_DIV_CODE | 조건 시장 분류 코드 | J : KRX, NX : NXT, UN : 통합
  - suggested_value: J (market_default)
- FID_INPUT_ISCD | 입력 종목코드 | 종목코드 (ex 005930 삼성전자)
  - suggested_value: 0000 (input_default)

## e7a0d02d-2aec-4358-8738-65c7c6da3b1b

- section: [국내주식] 종목정보 / 국내주식 / 종목정보
- name: 국내주식 성장성비율[v1_국내주식-085]
- path: /uapi/domestic-stock/v1/finance/growth-ratio

### required query
- fid_input_iscd | 입력 종목코드 | ex : 000660
  - suggested_value: 0000 (input_default)
- fid_div_cls_code | 분류 구분 코드 | 0: 년, 1: 분기
  - suggested_value: 0 (div_default)
- fid_cond_mrkt_div_code | 조건 시장 분류 코드 | 시장구분코드 (주식 J)
  - suggested_value: J (market_default)

## e8fcb701-6f36-4ba5-bbc7-84a577beec50

- section: [해외주식] 기본시세 / 해외주식 / 기본시세
- name: 해외주식 업종별시세[해외주식-048]
- path: /uapi/overseas-price/v1/quotations/industry-theme

### required query
- KEYB | NEXT KEY BUFF | 공백
  - suggested_value:  (blank)
- AUTH | 사용자권한정보 | 공백
  - suggested_value:  (blank)
- EXCD | 거래소코드 | 'NYS : 뉴욕, NAS : 나스닥,  AMS : 아멕스  HKS : 홍콩, SHS : 상해 , SZS : 심천 HSX : 호치민, HNX : 하노이 TSE : 도쿄 '
  - suggested_value: NYS (exchange_default)
- ICOD | 업종코드 | 업종코드별조회(HHDFS76370100) 를 통해 확인
  - suggested_value: (needs manual)
- VOL_RANG | 거래량조건 | 0(전체), 1(1백주이상), 2(1천주이상), 3(1만주이상), 4(10만주이상), 5(100만주이상), 6(1000만주이상)
  - suggested_value: 0 (all_value)

## ebf1dc17-7b48-4192-841d-0ccb6ce3f016

- section: [국내주식] 기본시세 / 국내주식 / 기본시세
- name: 국내주식 장마감 예상체결가[국내주식-120]
- path: /uapi/domestic-stock/v1/quotations/exp-closing-price

### required query
- FID_RANK_SORT_CLS_CODE | 순위 정렬 구분 코드 | 0:전체, 1:상한가마감예상, 2:하한가마감예상, 3:직전대비상승률상위 ,4:직전대비하락률상위
  - suggested_value: 0 (all_value)
- FID_COND_MRKT_DIV_CODE | 조건 시장 분류 코드 | 시장구분코드 (주식 J)
  - suggested_value: J (market_default)
- FID_COND_SCR_DIV_CODE | 조건 화면 분류 코드 | Unique key(11173)
  - suggested_value: 11173 (unique_key)
- FID_INPUT_ISCD | 입력 종목코드 | 0000:전체, 0001:거래소, 1001:코스닥, 2001:코스피200, 4001: KRX100
  - suggested_value: 0000 (all_value)
- FID_BLNG_CLS_CODE | 소속 구분 코드 | 0:전체, 1:종가범위연장
  - suggested_value: 0 (all_value)

## ec944971-3694-4692-8a17-761c2b549cd9

- section: [해외주식] 시세분석 / 해외주식 / 시세분석
- name: 해외주식 거래량순위[해외주식-043]
- path: /uapi/overseas-stock/v1/ranking/trade-vol

### required query
- KEYB | NEXT KEY BUFF | 공백
  - suggested_value:  (blank)
- AUTH | 사용자권한정보 | 공백
  - suggested_value:  (blank)
- EXCD | 거래소코드 | 'NYS : 뉴욕, NAS : 나스닥,  AMS : 아멕스  HKS : 홍콩, SHS : 상해 , SZS : 심천 HSX : 호치민, HNX : 하노이 TSE : 도쿄 '
  - suggested_value: NYS (exchange_default)
- NDAY | N일자값 | N일전 : 0(당일), 1(2일), 2(3일), 3(5일), 4(10일), 5(20일전), 6(30일), 7(60일), 8(120일), 9(1년)
  - suggested_value: 0 (nday_default)
- PRC1 | 현재가 필터범위 1 | 가격 ~
  - suggested_value: (needs manual)
- PRC2 | 현재가 필터범위 2 | ~ 가격
  - suggested_value: (needs manual)
- VOL_RANG | 거래량조건 | 0(전체), 1(1백주이상), 2(1천주이상), 3(1만주이상), 4(10만주이상), 5(100만주이상), 6(1000만주이상)
  - suggested_value: 0 (all_value)

## f54caf9c-65db-42ee-aa7e-a337c5a41778

- section: [국내주식] 업종/기타 / 국내주식 / 업종/기타
- name: 변동성완화장치(VI) 현황 [v1_국내주식-055]
- path: /uapi/domestic-stock/v1/quotations/inquire-vi-status

### required query
- FID_DIV_CLS_CODE | FID 분류 구분 코드 | 0:전체 1:상승 2:하락
  - suggested_value: 0 (all_value)
- FID_COND_SCR_DIV_CODE | FID 조건 화면 분류 코드 | 20139
  - suggested_value: 20139 (screen_default)
- FID_MRKT_CLS_CODE | FID 시장 구분 코드 | 0:전체 K:거래소 Q:코스닥
  - suggested_value: 0 (all_value)
- FID_INPUT_ISCD | FID 입력 종목코드 | 
  - suggested_value: 0000 (input_default)
- FID_RANK_SORT_CLS_CODE | FID 순위 정렬 구분 코드 | 0:전체1:정적2:동적3:정적&동적
  - suggested_value: 0 (all_value)
- FID_INPUT_DATE_1 | FID 입력 날짜1 | 영업일
  - suggested_value: (needs manual)
- FID_TRGT_CLS_CODE | FID 대상 구분 코드 | 
  - suggested_value: (needs manual)
- FID_TRGT_EXLS_CLS_CODE | FID 대상 제외 구분 코드 | 
  - suggested_value: (needs manual)

## f77aedcb-b46f-4aa0-b062-f03b9a444405

- section: [국내주식] 종목정보 / 국내주식 / 종목정보
- name: 국내주식 대차대조표[v1_국내주식-078]
- path: /uapi/domestic-stock/v1/finance/balance-sheet

### required query
- FID_DIV_CLS_CODE | 분류 구분 코드 | 0: 년, 1: 분기
  - suggested_value: 0 (div_default)
- fid_cond_mrkt_div_code | 조건 시장 분류 코드 | J
  - suggested_value: J (market_default)
- fid_input_iscd | 입력 종목코드 | 000660 : 종목코드
  - suggested_value: 0000 (input_default)

## fc52daa5-9919-4f80-b926-ee35ef298c54

- section: [국내주식] 시세분석 / 국내주식 / 시세분석
- name: 국내주식 시간외예상체결등락률 [국내주식-140]
- path: /uapi/domestic-stock/v1/ranking/overtime-exp-trans-fluct

### required query
- FID_COND_MRKT_DIV_CODE | 조건 시장 분류 코드 | 시장구분코드 (J: 주식)
  - suggested_value: J (market_default)
- FID_COND_SCR_DIV_CODE | 조건 화면 분류 코드 | Unique key(11186)
  - suggested_value: 11186 (unique_key)
- FID_INPUT_ISCD | 입력 종목코드 | 0000(전체), 0001(코스피), 1001(코스닥)
  - suggested_value: 0000 (all_value)
- FID_RANK_SORT_CLS_CODE | 순위 정렬 구분 코드 | 0(상승률), 1(상승폭), 2(보합), 3(하락률), 4(하락폭)
  - suggested_value: 0 (rank_default)
- FID_DIV_CLS_CODE | 분류 구분 코드 | '0(전체), 1(관리종목), 2(투자주의), 3(투자경고),  4(투자위험예고), 5(투자위험), 6(보통주), 7(우선주)'
  - suggested_value: 0 (all_value)
- FID_INPUT_PRICE_1 | 입력 가격1 | 가격 ~
  - suggested_value: (needs manual)
- FID_INPUT_PRICE_2 | 입력 가격2 | 공백
  - suggested_value:  (blank)
- FID_INPUT_VOL_1 | 입력 거래량 | 거래량 ~
  - suggested_value: (needs manual)

## fdb555c9-b958-48ad-a836-fd81f18ad73e

- section: [국내주식] 종목정보 / 국내주식 / 종목정보
- name: 국내주식 기타주요비율[v1_국내주식-082]
- path: /uapi/domestic-stock/v1/finance/other-major-ratios

### required query
- fid_input_iscd | 입력 종목코드 | 000660 : 종목코드
  - suggested_value: 0000 (input_default)
- fid_div_cls_code | 분류 구분 코드 | 0: 년, 1: 분기
  - suggested_value: 0 (div_default)
- fid_cond_mrkt_div_code | 조건 시장 분류 코드 | J
  - suggested_value: J (market_default)
