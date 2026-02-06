# Sentinel Sample Param Check

## 6b0b388e-f815-4009-b46d-e08e47575ca7
- name: 국내주식 시간외호가[국내주식-077]
- path: /uapi/domestic-stock/v1/quotations/inquire-overtime-asking-price
- spec: tmp/docs/normalized/국내주식/기본시세/inquire_overtime_asking_price__6b0b388e-f815-4009-b46d-e08e47575ca7.json
- required query fields:
  - FID_INPUT_ISCD: 종목코드
    - used: 005930
  - FID_COND_MRKT_DIV_CODE: 시장구분코드 (주식 J)
    - used: J
- success rt_cd: 0 msg1: 정상처리 되었습니다.

## f9f83090-60d0-4dcf-99c9-a4b36852848e
- name: 해외선물종목상세 [v1_해외선물-008]
- path: /uapi/overseas-futureoption/v1/quotations/stock-detail
- spec: tmp/docs/normalized/해외선물옵션/기본시세/stock_detail__f9f83090-60d0-4dcf-99c9-a4b36852848e.json
- required query fields:
  - SRS_CD: ex) CNHU24 ※ 종목코드 "포럼 > FAQ > 종목정보 다운로드(해외) - 해외지수선물" 참고
    - used: CNHU24 ※ 종목코드 "포럼 > FAQ > 종목정보 다운로드(해외
- success rt_cd: 0 msg1: 정상처리 되었습니다.

## 621bdd34-a902-4117-98b8-57733197742a
- name: 해외옵션종목현재가 [해외선물-035]
- path: /uapi/overseas-futureoption/v1/quotations/opt-price
- spec: tmp/docs/normalized/해외선물옵션/기본시세/opt_price__621bdd34-a902-4117-98b8-57733197742a.json
- required query fields:
  - SRS_CD: ex) OESU24 C5500 ※ 종목코드 "포럼 > FAQ > 종목정보 다운로드(해외) - 해외지수옵션/해외주식옵션" 참고
    - used: OESU24 C5500 ※ 종목코드 "포럼 > FAQ > 종목정보 다운로
- success rt_cd: 0 msg1: 정상처리 되었습니다.

## 3d3ad086-7c1b-41cb-9b76-ba05ccf6ba95
- name: 해외선물종목현재가 [v1_해외선물-009]
- path: /uapi/overseas-futureoption/v1/quotations/inquire-price
- spec: tmp/docs/normalized/해외선물옵션/기본시세/inquire_price__3d3ad086-7c1b-41cb-9b76-ba05ccf6ba95.json
- required query fields:
  - SRS_CD: ex) CNHU24 ※ 종목코드 "포럼 > FAQ > 종목정보 다운로드(해외) - 해외지수선물" 참고
    - used: CNHU24 ※ 종목코드 "포럼 > FAQ > 종목정보 다운로드(해외
- success rt_cd: 0 msg1: 정상처리 되었습니다.

## e5f413ec-3e68-47d7-931f-d7eb263990d9
- name: ELW LP매매추이 [국내주식-182]
- path: /uapi/elw/v1/quotations/lp-trade-trend
- spec: tmp/docs/normalized/국내주식/ELW_시세/lp_trade_trend__e5f413ec-3e68-47d7-931f-d7eb263990d9.json
- required query fields:
  - FID_COND_MRKT_DIV_CODE: 시장구분(W)
    - used: W
  - FID_INPUT_ISCD: 입력종목코드(ex 52K577(미래 K577KOSDAQ150콜)
    - used: 57K281
- success rt_cd: 0 msg1: 정상처리 되었습니다.

## a274b685-7ea8-441d-a2fe-3087becb6bf2
- name: 장내채권현재가(시세) [국내주식-200]
- path: /uapi/domestic-bond/v1/quotations/inquire-price
- spec: tmp/docs/normalized/장내채권/기본시세/inquire_price__a274b685-7ea8-441d-a2fe-3087becb6bf2.json
- required query fields:
  - FID_COND_MRKT_DIV_CODE: B (업종코드)
    - used: B
  - FID_INPUT_ISCD: 채권종목코드(ex KR2033022D33)
    - used: KR6095572D81
- success rt_cd: 0 msg1: 정상처리 되었습니다.

## 14431ddf-c0d5-4c33-a945-86e77bcf6486
- name: 해외옵션 체결추이(주간) [해외선물-036]
- path: /uapi/overseas-futureoption/v1/quotations/opt-weekly-ccnl
- spec: tmp/docs/normalized/해외선물옵션/기본시세/opt_weekly_ccnl__14431ddf-c0d5-4c33-a945-86e77bcf6486.json
- required query fields:
  - SRS_CD: ex) OESU24 C5500 ※ 종목코드 "포럼 > FAQ > 종목정보 다운로드(해외) - 해외지수옵션/해외주식옵션" 참고
    - used: OESU24 C5500 ※ 종목코드 "포럼 > FAQ > 종목정보 다운로
  - EXCH_CD: 종목코드에 맞는 거래소 코드 ex) CME
    - used: CME
  - START_DATE_TIME: "" 공란 입력
    - used: 
  - CLOSE_DATE_TIME: "" 공란 입력
    - used: 
  - QRY_TP: Q
    - used: Q
  - QRY_CNT: 예) 20 (최대 120)
    - used: 20 (최대 120
  - QRY_GAP: "" 공란 입력
    - used: 
  - INDEX_KEY: "" 공란 입력
    - used: 
- success rt_cd: 0 msg1: 정상처리 되었습니다.
