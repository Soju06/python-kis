# HTTP 500 원인 구분 결과

기준: 요청 파라미터가 문서 예시 텍스트를 그대로 포함(괄호/"최대"/불필요 공백/접두 00 등)하면 **요청 파라미터 문제**로 분류. 동일 요청을 정상화 후 재시도 필요.

- b290d16e-aa18-4e41-9c08-f4d941efe9a1 | 국내주식 체결금액별 매매비중 [국내주식-192] | /uapi/domestic-stock/v1/quotations/tradprt-byamt
  - spec: `tmp/docs/normalized/국내주식/시세분석/tradprt_byamt__b290d16e-aa18-4e41-9c08-f4d941efe9a1.json`
  - classification: request_param_error
  - query.FID_INPUT_ISCD: (005930 (삼성전자 -> paren,space

- 9de56f62-938c-40df-970e-8fd13a59b445 | 국내주식 종목투자의견 [국내주식-188] | /uapi/domestic-stock/v1/quotations/invest-opinion
  - spec: `tmp/docs/normalized/국내주식/종목정보/invest_opinion__9de56f62-938c-40df-970e-8fd13a59b445.json`
  - classification: request_param_error
  - query.FID_INPUT_ISCD: 005930(삼성전자 -> paren
  - query.FID_INPUT_DATE_1: 0020231113 -> leading_00_date
  - query.FID_INPUT_DATE_2: 0020240513 -> leading_00_date

- 9fa44d82-f5f3-4edc-adec-8bad25800bd3 | 해외옵션 분봉조회 [해외선물-040] | /uapi/overseas-futureoption/v1/quotations/inquire-time-optchartprice
  - spec: `tmp/docs/normalized/해외선물옵션/기본시세/inquire_time_optchartprice__9fa44d82-f5f3-4edc-adec-8bad25800bd3.json`
  - classification: request_param_error
  - query.SRS_CD: OESU24 C5500 -> space
  - query.START_DATE_TIME:  -> blank
  - query.CLOSE_DATE_TIME:  -> blank
  - query.QRY_CNT: 120 (최대 120 -> paren,max_text,space
  - query.INDEX_KEY:  -> blank

- 1ecba681-1f73-4fb7-98b0-b7feef13b354 | 해외옵션 체결추이(일간) [해외선물-037] | /uapi/overseas-futureoption/v1/quotations/opt-daily-ccnl
  - spec: `tmp/docs/normalized/해외선물옵션/기본시세/opt_daily_ccnl__1ecba681-1f73-4fb7-98b0-b7feef13b354.json`
  - classification: request_param_error
  - query.SRS_CD: OESU24 C5500 -> space
  - query.START_DATE_TIME:  -> blank
  - query.CLOSE_DATE_TIME:  -> blank
  - query.QRY_CNT: 100 (최대 119 -> paren,max_text,space
  - query.QRY_GAP:  -> blank
  - query.INDEX_KEY:  -> blank

- 94959cbc-bbb7-4776-8cd0-7058138a08aa | 해외옵션 체결추이(월간) [해외선물-039] | /uapi/overseas-futureoption/v1/quotations/opt-monthly-ccnl
  - spec: `tmp/docs/normalized/해외선물옵션/기본시세/opt_monthly_ccnl__94959cbc-bbb7-4776-8cd0-7058138a08aa.json`
  - classification: request_param_error
  - query.SRS_CD: OESU24 C5500 -> space
  - query.START_DATE_TIME:  -> blank
  - query.CLOSE_DATE_TIME:  -> blank
  - query.QRY_CNT: 20 (최대 120 -> paren,max_text,space
  - query.QRY_GAP:  -> blank
  - query.INDEX_KEY:  -> blank

- 41290e2a-6e25-49c0-91a1-99b96ce53efe | 해외옵션 체결추이(틱) [해외선물-038] | /uapi/overseas-futureoption/v1/quotations/opt-tick-ccnl
  - spec: `tmp/docs/normalized/해외선물옵션/기본시세/opt_tick_ccnl__41290e2a-6e25-49c0-91a1-99b96ce53efe.json`
  - classification: request_param_error
  - query.SRS_CD: OESU24 C5500 -> space
  - query.START_DATE_TIME:  -> blank
  - query.CLOSE_DATE_TIME:  -> blank
  - query.QRY_CNT: 30 (최대 40 -> paren,max_text,space
  - query.QRY_GAP:  -> blank
  - query.INDEX_KEY:  -> blank

- 14431ddf-c0d5-4c33-a945-86e77bcf6486 | 해외옵션 체결추이(주간) [해외선물-036] | /uapi/overseas-futureoption/v1/quotations/opt-weekly-ccnl
  - spec: `tmp/docs/normalized/해외선물옵션/기본시세/opt_weekly_ccnl__14431ddf-c0d5-4c33-a945-86e77bcf6486.json`
  - classification: request_param_error
  - query.SRS_CD: OESU24 C5500 -> space
  - query.START_DATE_TIME:  -> blank
  - query.CLOSE_DATE_TIME:  -> blank
  - query.QRY_CNT: 20 (최대 120 -> paren,max_text,space
  - query.QRY_GAP:  -> blank
  - query.INDEX_KEY:  -> blank

- 7f77a12b-b23c-4605-93ea-4e1b3c0356fb | 해외주식 상품기본정보[v1_해외주식-034] | /uapi/overseas-price/v1/quotations/search-info
  - spec: `tmp/docs/normalized/해외주식/기본시세/search_info__7f77a12b-b23c-4605-93ea-4e1b3c0356fb.json`
  - classification: request_param_error
  - query.PDNO: AAPL (애플 -> paren,space
