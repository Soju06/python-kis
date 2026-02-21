# Override Minimization Report

- Source: docs/overrides/augment_overrides.yaml

## 3dfc942e-0ed3-4c81-9e8d-9a96f1c5c669

- name: 주식현재가 시간외시간별체결[v1_국내주식-025]
- path: /uapi/domestic-stock/v1/quotations/inquire-time-overtimeconclusion

### query
- fid_hour_cls_code: override=1 auto=090000 (keep, source=heuristic, reason=time_default)

## dd867a76-745d-4268-8ff8-b3e7f71e6e83

- name: NAV 비교추이(분)[v1_국내주식-070]
- path: /uapi/etfetn/v1/quotations/nav-comparison-time-trend

### query
- fid_input_iscd: override=069500 auto=005930 (keep, source=default, reason=None)

## 0a5782f0-0c05-4feb-90f4-b86f09b45327

- name: 장내채권현재가(호가) [국내주식-132]
- path: /uapi/domestic-bond/v1/quotations/inquire-asking-price

### query
- FID_COND_MRKT_DIV_CODE: override=B auto=J (keep, source=default, reason=None)
- FID_INPUT_ISCD: override=KR2088012A16 auto=005930 (keep, source=default, reason=None)

## 498e6384-f887-4fb2-9055-2cbc95790087

- name: 선물옵션 일중예상체결추이[국내선물-018]
- path: /uapi/domestic-futureoption/v1/quotations/exp-price-trend

### query
- FID_INPUT_ISCD: override=A01603 auto=005930 (keep, source=default, reason=None)

## 77de2a74-b26c-40ca-a5b7-f87e2ef64f9f

- name: 선물옵션기간별시세(일/주/월/년)[v1_국내선물-008]
- path: /uapi/domestic-futureoption/v1/quotations/inquire-daily-fuopchartprice

### query
- FID_INPUT_ISCD: override=A01603 auto=005930 (keep, source=default, reason=None)
- FID_INPUT_DATE_1: override=20260120 auto=20220401 (keep, source=description, reason=date_example)
- FID_INPUT_DATE_2: override=20260120 auto=W (keep, source=enum_default, reason=date_today)

## 7d30b578-018d-4250-852a-7599211ff988

- name: 해외주식 거래회전율순위[해외주식-046]
- path: /uapi/overseas-stock/v1/ranking/trade-turnover

### query
- VOL_RANG: override=0 auto=1 (keep, source=heuristic, reason=qty_default)

## 86194480-c8f0-4b0b-9d3d-001c2fc33422

- name: 선물옵션 분봉조회[v1_국내선물-012]
- path: /uapi/domestic-futureoption/v1/quotations/inquire-time-fuopchartprice

### query
- FID_INPUT_ISCD: override=A01603 auto=005930 (keep, source=default, reason=None)
- FID_INPUT_DATE_1: override=20260120 auto=20230908 (keep, source=description, reason=date_example)
- FID_INPUT_HOUR_1: override=093000 auto=CM (keep, source=enum_default, reason=hour_1_default)

## 868b0fe2-fdb5-4a32-bdb2-00db12269230

- name: 국내업종 현재지수[v1_국내주식-063]
- path: /uapi/domestic-stock/v1/quotations/inquire-index-price

### query
- FID_COND_MRKT_DIV_CODE: override=U auto=J (keep, source=default, reason=None)
- FID_INPUT_ISCD: override=1001 auto=FAQ (keep, source=enum_default, reason=None)

## 8702dab4-008d-4849-8f24-a91b57872a80

- name: 해외선물 체결추이(월간)[해외선물-020]
- path: /uapi/overseas-futureoption/v1/quotations/monthly-ccnl

### query
- SRS_CD: override=BRNQ24 auto=6AM24 (keep, source=description, reason=example_value)
- EXCH_CD: override=ICE auto=CME (keep, source=description, reason=example_value)
- START_DATE_TIME: override=20240324 auto= (keep, source=description, reason=blank_description)
- CLOSE_DATE_TIME: override=20240423 auto=20240402 (keep, source=description, reason=date_example)
- QRY_CNT: override=30 auto=30 (최대 40 (keep, source=description, reason=example_value)

## 8c473311-ecfd-428f-9ec2-0b574d8592b9

- name: 해외선물 체결추이(일간)[해외선물-018]
- path: /uapi/overseas-futureoption/v1/quotations/daily-ccnl

### query
- SRS_CD: override=BRNQ24 auto=6AM24 (keep, source=description, reason=example_value)
- EXCH_CD: override=ICE auto=CME (keep, source=description, reason=example_value)
- START_DATE_TIME: override=20240324 auto= (keep, source=description, reason=blank_description)
- CLOSE_DATE_TIME: override=20240424 auto=20240402 (keep, source=description, reason=date_example)
- QRY_CNT: override=40 auto=30 (최대 40 (keep, source=description, reason=example_value)

## 9064a50c-0545-4b6c-8eb2-034f5214974b

- name: 해외뉴스종합(제목) [해외주식-053]
- path: /uapi/overseas-price/v1/quotations/news-title

### query
- NATION_CD: override= auto=CN (keep, source=enum_default, reason=code_like_default)

## a274b685-7ea8-441d-a2fe-3087becb6bf2

- name: 장내채권현재가(시세) [국내주식-200]
- path: /uapi/domestic-bond/v1/quotations/inquire-price

### query
- FID_COND_MRKT_DIV_CODE: override=B auto=J (keep, source=default, reason=None)
- FID_INPUT_ISCD: override=KR6095572D81 auto=005930 (keep, source=default, reason=None)

## bec98736-8f5a-49a0-b325-5f6c40ff13b3

- name: 선물옵션 시세호가[v1_국내선물-007]
- path: /uapi/domestic-futureoption/v1/quotations/inquire-asking-price

### query
- FID_INPUT_ISCD: override=A01603 auto=101S03 (keep, source=description, reason=example_value)

## c7be7c01-6f43-4576-b1fd-84d0102ce4c3

- name: 해외선물 체결추이(틱)[해외선물-019]
- path: /uapi/overseas-futureoption/v1/quotations/tick-ccnl

### query
- SRS_CD: override=BRNQ24 auto=6AM24 (keep, source=description, reason=example_value)
- EXCH_CD: override=ICE auto=CME (keep, source=description, reason=example_value)
- START_DATE_TIME: override=20240324 auto= (keep, source=description, reason=blank_description)
- CLOSE_DATE_TIME: override=20240423 auto=20240402 (keep, source=description, reason=date_example)
- QRY_CNT: override=40 auto=30 (최대 40 (keep, source=description, reason=example_value)

## cd2e4d9a-7e3d-44ff-9b68-36d971655c24

- name: 해외선물 체결추이(주간)[해외선물-017]
- path: /uapi/overseas-futureoption/v1/quotations/weekly-ccnl

### query
- SRS_CD: override=BRNQ24 auto=6AM24 (keep, source=description, reason=example_value)
- EXCH_CD: override=ICE auto=CME (keep, source=description, reason=example_value)
- START_DATE_TIME: override=20240324 auto= (keep, source=description, reason=blank_description)
- CLOSE_DATE_TIME: override=20240424 auto=20240402 (keep, source=description, reason=date_example)
- QRY_CNT: override=40 auto=30 (최대 40 (keep, source=description, reason=example_value)

## d9b0e346-a67d-43c6-938a-508e2d8507c6

- name: 국내옵션전광판_콜풋[국내선물-022]
- path: /uapi/domestic-futureoption/v1/quotations/display-board-callput

### query
- FID_COND_MRKT_DIV_CODE: override=O auto=J (keep, source=default, reason=None)
- FID_MRKT_CLS_CODE: override=CO auto=0 (keep, source=heuristic, reason=code_like_default)
- FID_MTRT_CNT: override=202405 auto=CODE (keep, source=enum_default, reason=qty_default)
- FID_MRKT_CLS_CODE1: override=PO auto=0 (keep, source=heuristic, reason=fid_numeric_default)

## 4112fd5d-43b7-4dc4-bf44-33df58981847

- name: 국내선물 기초자산 시세[국내선물-021]
- path: /uapi/domestic-futureoption/v1/quotations/display-board-top

### query
- FID_COND_MRKT_DIV_CODE: override=F auto=J (keep, source=default, reason=None)
- FID_INPUT_ISCD: override=101V06 auto=(101V06 (keep, source=description, reason=example_value)

## 264533d3-00eb-4794-984a-fecb84350f39

- name: ELW 종목검색 [국내주식-166]
- path: /uapi/elw/v1/quotations/cond-search

### query
- FID_COND_SCR_DIV_CODE: override=11510 auto=0 (keep, source=heuristic, reason=code_like_default)
- FID_INPUT_ISCD: override=00000 auto=005930 (keep, source=default, reason=None)

## d99d058d-4319-41ce-bce0-53c44a894ddb

- name: ELW 만기예정/만기종목 [국내주식-184]
- path: /uapi/elw/v1/quotations/expiration-stocks

### query
- FID_COND_MRKT_DIV_CODE: override=W auto=J (keep, source=default, reason=None)
- FID_COND_SCR_DIV_CODE: override=11547 auto=0 (keep, source=heuristic, reason=code_like_default)

## 937eb413-9db9-4479-887d-4cf172dcf344

- name: ELW 투자지표추이(체결) [국내주식-172]
- path: /uapi/elw/v1/quotations/indicator-trend-ccnl

### query
- FID_COND_MRKT_DIV_CODE: override=W auto=J (keep, source=default, reason=None)
- FID_INPUT_ISCD: override=57K281 auto=58J297(KBJ297삼성전자콜 (keep, source=description, reason=example_value)

## 1e0869f4-5639-4f22-be71-a28897242457

- name: ELW 투자지표추이(일별) [국내주식-173]
- path: /uapi/elw/v1/quotations/indicator-trend-daily

### query
- FID_COND_MRKT_DIV_CODE: override=W auto=J (keep, source=default, reason=None)
- FID_INPUT_ISCD: override=57K281 auto=005930 (keep, source=default, reason=None)

## 4af6e358-255c-4e4e-b691-388610068216

- name: ELW 투자지표추이(분별) [국내주식-174]
- path: /uapi/elw/v1/quotations/indicator-trend-minute

### query
- FID_COND_MRKT_DIV_CODE: override=W auto=J (keep, source=default, reason=None)
- FID_INPUT_ISCD: override=57K281 auto=58J297(KBJ297삼성전자콜 (keep, source=description, reason=example_value)
- FID_PW_DATA_INCU_YN: override=Y auto=N (keep, source=heuristic, reason=yn_default)

## e9be5d05-448e-4222-bb05-7f0e27a91d69

- name: ELW 민감도 추이(체결) [국내주식-175]
- path: /uapi/elw/v1/quotations/sensitivity-trend-ccnl

### query
- FID_COND_MRKT_DIV_CODE: override=W auto=J (keep, source=default, reason=None)
- FID_INPUT_ISCD: override=57K281 auto=58J297(KBJ297삼성전자콜 (keep, source=description, reason=example_value)

## a64dc948-de6c-4e7a-988b-9769ac8fd5b2

- name: ELW 민감도 추이(일별) [국내주식-176]
- path: /uapi/elw/v1/quotations/sensitivity-trend-daily

### query
- FID_COND_MRKT_DIV_CODE: override=W auto=J (keep, source=default, reason=None)
- FID_INPUT_ISCD: override=57K281 auto=(58J438(KBJ438삼성전자풋 (keep, source=description, reason=example_value)

## 40403e7f-bd31-4e12-ae87-553e7be28b12

- name: ELW 변동성추이(체결) [국내주식-177]
- path: /uapi/elw/v1/quotations/volatility-trend-ccnl

### query
- FID_COND_MRKT_DIV_CODE: override=W auto=J (keep, source=default, reason=None)
- FID_INPUT_ISCD: override=57K281 auto=58J297(KBJ297삼성전자콜 (keep, source=description, reason=example_value)

## 5bd31e17-ea4d-4e76-8e03-f8dfb3be25e7

- name: ELW 변동성 추이(일별) [국내주식-178]
- path: /uapi/elw/v1/quotations/volatility-trend-daily

### query
- FID_COND_MRKT_DIV_CODE: override=W auto=J (keep, source=default, reason=None)
- FID_INPUT_ISCD: override=57K281 auto=58J297(KBJ297삼성전자콜 (keep, source=description, reason=example_value)

## 31081a30-ba59-4b42-a9f2-c1fe850fadb1

- name: ELW 변동성 추이(분별) [국내주식-179]
- path: /uapi/elw/v1/quotations/volatility-trend-minute

### query
- FID_COND_MRKT_DIV_CODE: override=W auto=J (keep, source=default, reason=None)
- FID_INPUT_ISCD: override=57JS61 auto=58J297(KBJ297삼성전자콜 (keep, source=description, reason=example_value)

## f1ce6099-5bf2-4b4e-915e-e0c7020af4bf

- name: ELW 변동성 추이(틱) [국내주식-180]
- path: /uapi/elw/v1/quotations/volatility-trend-tick

### query
- FID_COND_MRKT_DIV_CODE: override=W auto=J (keep, source=default, reason=None)
- FID_INPUT_ISCD: override=57K281 auto=58J297(KBJ297삼성전자콜 (keep, source=description, reason=example_value)

## e5f413ec-3e68-47d7-931f-d7eb263990d9

- name: ELW LP매매추이 [국내주식-182]
- path: /uapi/elw/v1/quotations/lp-trade-trend

### query
- FID_COND_MRKT_DIV_CODE: override=W auto=J (keep, source=default, reason=None)
- FID_INPUT_ISCD: override=57K281 auto=005930 (keep, source=default, reason=None)

## 8869c0c3-efd8-461b-ba87-5ab468afeea2

- name: ELW 지표순위[국내주식-169]
- path: /uapi/elw/v1/ranking/indicator

### query
- FID_COND_MRKT_DIV_CODE: override=W auto=J (keep, source=default, reason=None)

## 147e81db-e0d2-40cd-95f5-d8da90c2d998

- name: ELW 신규상장종목 [국내주식-181]
- path: /uapi/elw/v1/quotations/newly-listed

### query
- FID_COND_MRKT_DIV_CODE: override=W auto=J (keep, source=default, reason=None)
- FID_INPUT_DATE_1: override=20260122 auto=20240402 (keep, source=description, reason=date_example)
- FID_UNAS_INPUT_ISCD: override=000000 auto=2001 (keep, source=enum_default, reason=code_like_default)

## 4769336b-3280-419e-b69d-7531195b2221

- name: ELW 당일급변종목[국내주식-171]
- path: /uapi/elw/v1/ranking/quick-change

### query
- FID_COND_MRKT_DIV_CODE: override=W auto=J (keep, source=default, reason=None)
- FID_MRKT_CLS_CODE: override=A auto=0 (keep, source=heuristic, reason=code_like_default)
- FID_UNAS_INPUT_ISCD: override=00000 auto=2001 (keep, source=enum_default, reason=code_like_default)
- FID_INPUT_PRICE_1: override= auto=0 (keep, source=heuristic, reason=price_default)
- FID_INPUT_PRICE_2: override= auto=0 (keep, source=heuristic, reason=price_default)
- FID_INPUT_VOL_1: override=0 auto=1 (keep, source=heuristic, reason=qty_default)
- FID_INPUT_VOL_2: override=0 auto=1 (keep, source=heuristic, reason=qty_default)
- FID_HOUR_CLS_CODE: override=2 auto=1 (keep, source=enum_default, reason=time_default)
- FID_INPUT_HOUR_1: override=1 auto=100000 (keep, source=heuristic, reason=hour_1_default)
- FID_INPUT_HOUR_2: override= auto=090000 (keep, source=heuristic, reason=time_default)

## 246842f0-450e-464b-8dbc-356133d12b42

- name: ELW 민감도 순위[국내주식-170]
- path: /uapi/elw/v1/ranking/sensitivity

### query
- FID_COND_MRKT_DIV_CODE: override=W auto=J (keep, source=default, reason=None)

## 263ef907-db8c-4bf6-8da9-388c8fb4cf10

- name: ELW 기초자산별 종목시세 [국내주식-186]
- path: /uapi/elw/v1/quotations/udrl-asset-price

### query
- FID_COND_MRKT_DIV_CODE: override=W auto=J (keep, source=default, reason=None)

## 9f6b3c41-d44a-4ae1-8324-aa222d19c6bf

- name: ELW 상승률순위[국내주식-167]
- path: /uapi/elw/v1/ranking/updown-rate

### query
- FID_COND_MRKT_DIV_CODE: override=W auto=J (keep, source=default, reason=None)

## 6bd62480-d165-415e-9d82-bffe2f43aa7e

- name: ELW 거래량순위[국내주식-168]
- path: /uapi/elw/v1/ranking/volume-rank

### query
- FID_COND_MRKT_DIV_CODE: override=W auto=J (keep, source=default, reason=None)
- FID_COND_SCR_DIV_CODE: override=20278 auto=0 (keep, source=heuristic, reason=code_like_default)
- FID_INPUT_ISCD_2: override=0000 auto=0 (keep, source=heuristic, reason=fid_numeric_default)
- FID_INPUT_DATE_1: override=20240410 auto=20260130 (keep, source=heuristic, reason=date_today)
- FID_INPUT_DATE_2: override=20240410 auto= (keep, source=description, reason=blank_description)

## 0cc848c0-4928-4b89-bca4-62df430e4a45

- name: 시장별 투자자매매동향(일별) [국내주식-075]
- path: /uapi/domestic-stock/v1/quotations/inquire-investor-daily-by-market

### query
- FID_COND_MRKT_DIV_CODE: override=U auto=J (keep, source=default, reason=None)
- FID_INPUT_ISCD: override=0001 auto=005930 (keep, source=default, reason=None)
- FID_INPUT_ISCD_2: override=0001 auto=0 (keep, source=heuristic, reason=fid_numeric_default)
- FID_INPUT_DATE_1: override=20240401 auto=20240517 (keep, source=description, reason=date_example)
- FID_INPUT_DATE_2: override=20240401 auto=20260130 (keep, source=heuristic, reason=date_today)

## 7d1b2345-32f8-463b-9f41-8b4602387d52

- name: 국내주식 예상체결 전체지수[국내주식-122]
- path: /uapi/domestic-stock/v1/quotations/exp-total-index

### query
- fid_cond_mrkt_div_code: override=U auto=J (keep, source=default, reason=None)
- fid_input_iscd: override=0001 auto=0000 (keep, source=enum_default, reason=None)

## 184519fc-37b5-4687-bebf-d3ddf5659729

- name: 국내주식업종기간별시세(일/주/월/년)[v1_국내주식-021]
- path: /uapi/domestic-stock/v1/quotations/inquire-daily-indexchartprice

### query
- FID_COND_MRKT_DIV_CODE: override=U auto=J (keep, source=default, reason=None)
- FID_INPUT_DATE_1: override=20240401 auto=20220501 (keep, source=description, reason=date_example)
- FID_INPUT_DATE_2: override=20240430 auto=20220530 (keep, source=description, reason=date_example)

## 27bef4b4-cf83-4698-8f1e-16138cb09817

- name: 국내업종 구분별전체시세[v1_국내주식-066]
- path: /uapi/domestic-stock/v1/quotations/inquire-index-category-price

### query
- FID_COND_MRKT_DIV_CODE: override=U auto=J (keep, source=default, reason=None)
- FID_INPUT_ISCD: override=0001 auto=FAQ (keep, source=enum_default, reason=None)

## b11002e2-63c7-401b-a6fd-3136cb28040a

- name: 국내업종 일자별지수[v1_국내주식-065]
- path: /uapi/domestic-stock/v1/quotations/inquire-index-daily-price

### query
- FID_COND_MRKT_DIV_CODE: override=U auto=J (keep, source=default, reason=None)
- FID_INPUT_ISCD: override=0001 auto=FAQ (keep, source=enum_default, reason=None)
- FID_INPUT_DATE_1: override=20240401 auto=20240223 (keep, source=description, reason=date_example)

## a87c0275-f467-4199-866a-876a8fcdccb0

- name: 국내업종 시간별지수(초)[국내주식-064]
- path: /uapi/domestic-stock/v1/quotations/inquire-index-tickprice

### query
- FID_COND_MRKT_DIV_CODE: override=U auto=J (keep, source=default, reason=None)

## 1d150774-eafa-49f8-9e77-67099bc28771

- name: 국내업종 시간별지수(분)[국내주식-119]
- path: /uapi/domestic-stock/v1/quotations/inquire-index-timeprice

### query
- FID_COND_MRKT_DIV_CODE: override=U auto=J (keep, source=default, reason=None)

## 5613b629-b622-4a22-8175-31a4376c36b4

- name: 업종 분봉조회[v1_국내주식-045]
- path: /uapi/domestic-stock/v1/quotations/inquire-time-indexchartprice

### query
- FID_COND_MRKT_DIV_CODE: override=U auto=J (keep, source=default, reason=None)

## 34d1b922-ab20-4839-9f15-ab1fe242a81f

- name: 장내채권현재가(체결) [국내주식-201]
- path: /uapi/domestic-bond/v1/quotations/inquire-ccnl

### query
- FID_COND_MRKT_DIV_CODE: override=B auto=J (keep, source=default, reason=None)
- FID_INPUT_ISCD: override=KR2033022D33 auto=005930 (keep, source=default, reason=None)

## f5dcbbc3-bee6-4b83-a236-5f3a5bb59d72

- name: 장내채권 기간별시세(일) [국내주식-159]
- path: /uapi/domestic-bond/v1/quotations/inquire-daily-itemchartprice

### query
- FID_COND_MRKT_DIV_CODE: override=B auto=J (keep, source=default, reason=None)
- FID_INPUT_ISCD: override=KR2033022D33 auto=005930 (keep, source=default, reason=None)

## 7d6d8ba7-bcae-4d7c-8d5b-4b51cd42a94a

- name: 장내채권현재가(일별) [국내주식-202]
- path: /uapi/domestic-bond/v1/quotations/inquire-daily-price

### query
- FID_COND_MRKT_DIV_CODE: override=B auto=J (keep, source=default, reason=None)
- FID_INPUT_ISCD: override=KR2033022D33 auto=005930 (keep, source=default, reason=None)

## ecc36b93-6f99-4cd2-b16d-79b46734769a

- name: 금리 종합(국내채권/금리) [국내주식-155]
- path: /uapi/domestic-stock/v1/quotations/comp-interest

### query
- FID_COND_MRKT_DIV_CODE: override=I auto=J (keep, source=default, reason=None)
- FID_DIV_CLS_CODE: override=1 auto=0 (keep, source=heuristic, reason=code_like_default)

## f2921c05-8b93-4a13-a0d8-6132be010066

- name: 국내주식 관심종목등록 상위[v1_국내주식-102]
- path: /uapi/domestic-stock/v1/ranking/top-interest-stock

### query
- fid_input_price_1: override= auto=0 (keep, source=heuristic, reason=price_default)
- fid_input_price_2: override= auto=0 (keep, source=heuristic, reason=price_default)
- fid_vol_cnt: override=0 auto=1 (keep, source=heuristic, reason=qty_default)
- fid_input_iscd_2: override=000000 auto=0 (keep, source=heuristic, reason=fid_numeric_default)

## 6df56964-f22b-43d4-9457-f06264018e5b

- name: 거래량순위[v1_국내주식-047]
- path: /uapi/domestic-stock/v1/quotations/volume-rank

### query
- FID_COND_SCR_DIV_CODE: override=20171 auto=0 (keep, source=heuristic, reason=code_like_default)
- FID_INPUT_ISCD: override=0000 auto=005930 (keep, source=default, reason=None)
- FID_TRGT_CLS_CODE: override=111111111 auto="111111111" (keep, source=description, reason=example_value)
- FID_TRGT_EXLS_CLS_CODE: override=0000000000 auto="0000000000" (keep, source=description, reason=example_value)

## 6723d437-b275-4c10-b7fb-9ba788cad75e

- name: 관심종목 그룹조회 [국내주식-204]
- path: /uapi/domestic-stock/v1/quotations/intstock-grouplist

### query
- TYPE: override=1 auto=0 (keep, source=heuristic, reason=code_like_default)
- FID_ETC_CLS_CODE: override=00 auto= (keep, source=heuristic, reason=etc_cls_blank)

## 4d8c6e7a-a026-4f8d-8c64-9e7ecbc3d97e

- name: 관심종목 그룹별 종목조회 [국내주식-203]
- path: /uapi/domestic-stock/v1/quotations/intstock-stocklist-by-group

### query
- TYPE: override=1 auto=0 (keep, source=heuristic, reason=code_like_default)
- INTER_GRP_CODE: override=002 auto=0 (keep, source=heuristic, reason=code_like_default)
- FID_ETC_CLS_CODE: override=4 auto= (keep, source=heuristic, reason=etc_cls_blank)

## fee465d1-7fd5-4c66-b4a4-731b813d569d

- name: 관심종목(멀티종목) 시세조회 [국내주식-205]
- path: /uapi/domestic-stock/v1/quotations/intstock-multprice

### query
- FID_COND_MRKT_DIV_CODE_2: override=J auto=0 (keep, source=heuristic, reason=fid_numeric_default)
- FID_COND_MRKT_DIV_CODE_3: override=J auto=0 (keep, source=heuristic, reason=fid_numeric_default)
- FID_COND_MRKT_DIV_CODE_4: override=J auto=0 (keep, source=heuristic, reason=fid_numeric_default)
- FID_COND_MRKT_DIV_CODE_5: override=J auto=0 (keep, source=heuristic, reason=fid_numeric_default)
- FID_COND_MRKT_DIV_CODE_6: override=J auto=0 (keep, source=heuristic, reason=fid_numeric_default)
- FID_COND_MRKT_DIV_CODE_7: override=J auto=0 (keep, source=heuristic, reason=fid_numeric_default)
- FID_COND_MRKT_DIV_CODE_8: override=J auto=0 (keep, source=heuristic, reason=fid_numeric_default)
- FID_COND_MRKT_DIV_CODE_9: override=J auto=0 (keep, source=heuristic, reason=fid_numeric_default)
- FID_COND_MRKT_DIV_CODE_10: override=J auto=0 (keep, source=heuristic, reason=fid_numeric_default)
- FID_COND_MRKT_DIV_CODE_11: override=J auto=0 (keep, source=heuristic, reason=fid_numeric_default)
- FID_COND_MRKT_DIV_CODE_12: override=J auto=0 (keep, source=heuristic, reason=fid_numeric_default)
- FID_COND_MRKT_DIV_CODE_13: override=J auto=0 (keep, source=heuristic, reason=fid_numeric_default)
- FID_COND_MRKT_DIV_CODE_14: override=J auto=0 (keep, source=heuristic, reason=fid_numeric_default)
- FID_COND_MRKT_DIV_CODE_15: override=J auto=0 (keep, source=heuristic, reason=fid_numeric_default)
- FID_COND_MRKT_DIV_CODE_16: override=J auto=0 (keep, source=heuristic, reason=fid_numeric_default)
- FID_COND_MRKT_DIV_CODE_17: override=J auto=0 (keep, source=heuristic, reason=fid_numeric_default)
- FID_COND_MRKT_DIV_CODE_18: override=J auto=0 (keep, source=heuristic, reason=fid_numeric_default)
- FID_COND_MRKT_DIV_CODE_19: override=J auto=0 (keep, source=heuristic, reason=fid_numeric_default)
- FID_COND_MRKT_DIV_CODE_20: override=J auto=0 (keep, source=heuristic, reason=fid_numeric_default)
- FID_COND_MRKT_DIV_CODE_21: override=J auto=0 (keep, source=heuristic, reason=fid_numeric_default)
- FID_COND_MRKT_DIV_CODE_22: override=J auto=0 (keep, source=heuristic, reason=fid_numeric_default)
- FID_COND_MRKT_DIV_CODE_23: override=J auto=0 (keep, source=heuristic, reason=fid_numeric_default)
- FID_COND_MRKT_DIV_CODE_24: override=J auto=0 (keep, source=heuristic, reason=fid_numeric_default)
- FID_COND_MRKT_DIV_CODE_25: override=J auto=0 (keep, source=heuristic, reason=fid_numeric_default)
- FID_COND_MRKT_DIV_CODE_26: override=J auto=0 (keep, source=heuristic, reason=fid_numeric_default)
- FID_COND_MRKT_DIV_CODE_27: override=J auto=0 (keep, source=heuristic, reason=fid_numeric_default)
- FID_COND_MRKT_DIV_CODE_28: override=J auto=0 (keep, source=heuristic, reason=fid_numeric_default)
- FID_COND_MRKT_DIV_CODE_29: override=J auto=0 (keep, source=heuristic, reason=fid_numeric_default)
- FID_COND_MRKT_DIV_CODE_30: override=J auto=0 (keep, source=heuristic, reason=fid_numeric_default)
- FID_INPUT_ISCD_2: override=005930 auto=0 (keep, source=heuristic, reason=fid_numeric_default)
- FID_INPUT_ISCD_3: override=005930 auto=0 (keep, source=heuristic, reason=fid_numeric_default)
- FID_INPUT_ISCD_4: override=005930 auto=0 (keep, source=heuristic, reason=fid_numeric_default)
- FID_INPUT_ISCD_5: override=005930 auto=0 (keep, source=heuristic, reason=fid_numeric_default)
- FID_INPUT_ISCD_6: override=005930 auto=0 (keep, source=heuristic, reason=fid_numeric_default)
- FID_INPUT_ISCD_7: override=005930 auto=0 (keep, source=heuristic, reason=fid_numeric_default)
- FID_INPUT_ISCD_8: override=005930 auto=0 (keep, source=heuristic, reason=fid_numeric_default)
- FID_INPUT_ISCD_9: override=005930 auto=0 (keep, source=heuristic, reason=fid_numeric_default)
- FID_INPUT_ISCD_10: override=005930 auto=0 (keep, source=heuristic, reason=fid_numeric_default)
- FID_INPUT_ISCD_11: override=005930 auto=0 (keep, source=heuristic, reason=fid_numeric_default)
- FID_INPUT_ISCD_12: override=005930 auto=0 (keep, source=heuristic, reason=fid_numeric_default)
- FID_INPUT_ISCD_13: override=005930 auto=0 (keep, source=heuristic, reason=fid_numeric_default)
- FID_INPUT_ISCD_14: override=005930 auto=0 (keep, source=heuristic, reason=fid_numeric_default)
- FID_INPUT_ISCD_15: override=005930 auto=0 (keep, source=heuristic, reason=fid_numeric_default)
- FID_INPUT_ISCD_16: override=005930 auto=0 (keep, source=heuristic, reason=fid_numeric_default)
- FID_INPUT_ISCD_17: override=005930 auto=0 (keep, source=heuristic, reason=fid_numeric_default)
- FID_INPUT_ISCD_18: override=005930 auto=0 (keep, source=heuristic, reason=fid_numeric_default)
- FID_INPUT_ISCD_19: override=005930 auto=0 (keep, source=heuristic, reason=fid_numeric_default)
- FID_INPUT_ISCD_20: override=005930 auto=0 (keep, source=heuristic, reason=fid_numeric_default)
- FID_INPUT_ISCD_21: override=005930 auto=0 (keep, source=heuristic, reason=fid_numeric_default)
- FID_INPUT_ISCD_22: override=005930 auto=0 (keep, source=heuristic, reason=fid_numeric_default)
- FID_INPUT_ISCD_23: override=005930 auto=0 (keep, source=heuristic, reason=fid_numeric_default)
- FID_INPUT_ISCD_24: override=005930 auto=0 (keep, source=heuristic, reason=fid_numeric_default)
- FID_INPUT_ISCD_25: override=005930 auto=0 (keep, source=heuristic, reason=fid_numeric_default)
- FID_INPUT_ISCD_26: override=005930 auto=0 (keep, source=heuristic, reason=fid_numeric_default)
- FID_INPUT_ISCD_27: override=005930 auto=0 (keep, source=heuristic, reason=fid_numeric_default)
- FID_INPUT_ISCD_28: override=005930 auto=0 (keep, source=heuristic, reason=fid_numeric_default)
- FID_INPUT_ISCD_29: override=005930 auto=0 (keep, source=heuristic, reason=fid_numeric_default)
- FID_INPUT_ISCD_30: override=005930 auto=0 (keep, source=heuristic, reason=fid_numeric_default)

## 3ed0247e-d717-43ed-85e9-51f952844687

- name: 종목별 일별 대차거래추이 [국내주식-135]
- path: /uapi/domestic-stock/v1/quotations/daily-loan-trans

### query
- MKSC_SHRN_ISCD: override=005930 auto=0 (keep, source=heuristic, reason=code_like_default)
- START_DATE: override=20240401 auto=20260130 (keep, source=heuristic, reason=date_today)
- END_DATE: override=20240430 auto=20260130 (keep, source=heuristic, reason=date_today)

## cf45db98-43d0-476a-8774-d9690365300a

- name: 장내채권 발행정보[국내주식-156]
- path: /uapi/domestic-bond/v1/quotations/issue-info

### query
- PDNO: override=KR6449111CB8 auto=AAPL (keep, source=default, reason=None)

## 56cf546c-a74f-467c-98b1-005967535e9e

- name: 장내채권 기본조회 [국내주식-129]
- path: /uapi/domestic-bond/v1/quotations/search-bond-info

### query
- PDNO: override=KR6449111CB8 auto=AAPL (keep, source=default, reason=None)

## aacab59c-7559-414b-bf73-b0d15f3d62f1

- name: 장내채권 평균단가조회 [국내주식-158]
- path: /uapi/domestic-bond/v1/quotations/avg-unit

### query
- VRFC_KIND_CD: override=00 auto=0 (keep, source=heuristic, reason=code_like_default)

## da0485b5-31f1-4c62-a3d4-294a4311ad39

- name: 주식기본조회[v1_국내주식-067]
- path: /uapi/domestic-stock/v1/quotations/search-stock-info

### query
- PDNO: override=005930 auto=AAPL (keep, source=default, reason=None)

## 07313e08-45f2-4423-abb2-2a49752910ae

- name: ELW 현재가 시세[v1_국내주식-014]
- path: /uapi/domestic-stock/v1/quotations/inquire-elw-price

### query
- FID_COND_MRKT_DIV_CODE: override=W auto=J (keep, source=default, reason=None)
- FID_INPUT_ISCD: override=57K281 auto=005930 (keep, source=default, reason=None)

## 0c2760ca-7fc9-4f41-9abd-33b2f5ff3b3b

- name: 국내주식 신용잔고 상위[국내주식-109]
- path: /uapi/domestic-stock/v1/ranking/credit-balance

### query
- FID_OPTION: override=2 auto= (keep, source=required_blank, reason=None)

## 3871dd9b-e9a5-471b-a0ce-d9ceb207ac5b

- name: ETF 구성종목시세[국내주식-073]
- path: /uapi/etfetn/v1/quotations/inquire-component-stock-price

### query
- FID_INPUT_ISCD: override=069500 auto=005930 (keep, source=default, reason=None)

## 05a719af-aa3c-46c7-a670-55f2f11654c2

- name: 국내주식 예상체결 상승/하락상위[v1_국내주식-103]
- path: /uapi/domestic-stock/v1/ranking/exp-trans-updown

### query
- fid_aply_rang_prc_1: override= auto=0 (keep, source=heuristic, reason=price_default)
- fid_vol_cnt: override=0 auto=1 (keep, source=heuristic, reason=qty_default)

## 8362a35a-e7c2-4944-a4a2-5a716737388c

- name: 국내옵션전광판_선물[국내선물-023]
- path: /uapi/domestic-futureoption/v1/quotations/display-board-futures

### query
- FID_COND_MRKT_DIV_CODE: override=F auto=J (keep, source=default, reason=None)

## 3a588de4-df48-49ac-88ca-9765998c00e1

- name: 국내주식 증권사별 투자의견 [국내주식-189]
- path: /uapi/domestic-stock/v1/quotations/invest-opbysec

### query
- FID_COND_SCR_DIV_CODE: override=16633 auto=0 (keep, source=heuristic, reason=code_like_default)
- FID_INPUT_ISCD: override=999 auto=005930 (keep, source=default, reason=None)
- FID_INPUT_DATE_1: override=20260101 auto=20260130 (keep, source=heuristic, reason=date_today)

## 4a077f43-7053-47be-b811-8e35be4ea745

- name: 국내기관_외국인 매매종목가집계[국내주식-037]
- path: /uapi/domestic-stock/v1/quotations/foreign-institution-total

### query
- FID_COND_MRKT_DIV_CODE: override=V auto=J (keep, source=default, reason=None)
- FID_COND_SCR_DIV_CODE: override=16449 auto=0 (keep, source=heuristic, reason=code_like_default)

## ca2e71e1-5ef4-4489-b4c4-118e10588690

- name: ELW 비교대상종목조회 [국내주식-183]
- path: /uapi/elw/v1/quotations/compare-stocks

### query
- FID_COND_SCR_DIV_CODE: override=11517 auto=0 (keep, source=heuristic, reason=code_like_default)
- FID_INPUT_ISCD: override=005930 auto=005930(삼성전자 (keep, source=description, reason=example_value)

## f54caf9c-65db-42ee-aa7e-a337c5a41778

- name: 변동성완화장치(VI) 현황 [v1_국내주식-055]
- path: /uapi/domestic-stock/v1/quotations/inquire-vi-status

### query
- FID_COND_SCR_DIV_CODE: override=20139 auto=0 (keep, source=heuristic, reason=code_like_default)
- FID_INPUT_ISCD: override=0000 auto=005930 (keep, source=default, reason=None)

## 0bb05819-d759-4789-8eda-27a0b88f02aa

- name: 선물옵션 시세[v1_국내선물-006]
- path: /uapi/domestic-futureoption/v1/quotations/inquire-price

### query
- FID_INPUT_ISCD: override=A01603 auto=101S03 (keep, source=description, reason=example_value)

## 7bdbff93-1334-496f-a9b8-7da6032f7407

- name: 국내주식 대량체결건수 상위[국내주식-107]
- path: /uapi/domestic-stock/v1/ranking/bulk-trans-num

### query
- fid_input_price_1: override= auto=0 (keep, source=heuristic, reason=price_default)
- fid_aply_rang_prc_1: override= auto=0 (keep, source=heuristic, reason=price_default)
- fid_aply_rang_prc_2: override= auto=0 (keep, source=heuristic, reason=price_default)
- fid_vol_cnt: override=0 auto=1 (keep, source=heuristic, reason=qty_default)

## 72e63cb2-2ab1-41a0-8ab9-62cbeaa5eea0

- name: 국내주식 신고/신저근접종목 상위[v1_국내주식-105]
- path: /uapi/domestic-stock/v1/ranking/near-new-highlow

### query
- fid_input_cnt_1: override= auto=1 (keep, source=heuristic, reason=qty_default)
- fid_input_cnt_2: override= auto=1 (keep, source=heuristic, reason=qty_default)
- fid_aply_rang_prc_1: override= auto=0 (keep, source=heuristic, reason=price_default)
- fid_aply_rang_prc_2: override= auto=0 (keep, source=heuristic, reason=price_default)

## f5c2c9d8-8d11-4a70-8694-1b71e3fc3640

- name: 국내주식 시간외등락율순위 [국내주식-138]
- path: /uapi/domestic-stock/v1/ranking/overtime-fluctuation

### query
- FID_DIV_CLS_CODE: override=2 auto=1 (keep, source=enum_default, reason=code_like_default)
- FID_INPUT_PRICE_1: override= auto=0 (keep, source=heuristic, reason=price_default)
- FID_INPUT_PRICE_2: override= auto=0 (keep, source=heuristic, reason=price_default)
- FID_VOL_CNT: override=0 auto=1 (keep, source=heuristic, reason=qty_default)

## 16958dd0-0304-4554-b12d-ec56e7874e71

- name: 국내주식 시간외거래량순위 [국내주식-139]
- path: /uapi/domestic-stock/v1/ranking/overtime-volume

### query
- FID_INPUT_PRICE_1: override= auto=0 (keep, source=heuristic, reason=price_default)
- FID_INPUT_PRICE_2: override= auto=0 (keep, source=heuristic, reason=price_default)
- FID_VOL_CNT: override=0 auto=1 (keep, source=heuristic, reason=qty_default)

## c02e3f30-5d71-4156-a039-3976f4d485f8

- name: 국내주식 당사매매종목 상위[v1_국내주식-104]
- path: /uapi/domestic-stock/v1/ranking/traded-by-company

### query
- fid_input_date_1: override=20240314 auto=20260130 (keep, source=heuristic, reason=date_today)
- fid_input_date_2: override=20240315 auto=20260130 (keep, source=heuristic, reason=date_today)
- fid_aply_rang_prc_1: override= auto=0 (keep, source=heuristic, reason=price_default)
- fid_aply_rang_prc_2: override= auto=0 (keep, source=heuristic, reason=price_default)

## 0aad2cef-b338-4f4f-a8a0-b19c67a390b3

- name: 국내주식 신용잔고 일별추이[국내주식-110]
- path: /uapi/domestic-stock/v1/quotations/daily-credit-balance

### query
- fid_input_date_1: override=20240315 auto=20240313 (keep, source=description, reason=date_example)

## ce9f2a8f-e3cb-4bd3-83ba-7b6034eafae9

- name: 회원사 실시간 매매동향(틱) [국내주식-163]
- path: /uapi/domestic-stock/v1/quotations/frgnmem-trade-trend

### query
- FID_COND_SCR_DIV_CODE: override=20432 auto=0 (keep, source=heuristic, reason=code_like_default)
- FID_INPUT_ISCD_2: override=99999 auto=FAQ (keep, source=enum_default, reason=fid_numeric_default)
- FID_MRKT_CLS_CODE: override=A auto=ELW (keep, source=enum_default, reason=code_like_default)
- FID_VOL_CNT: override=0 auto=1 (keep, source=heuristic, reason=qty_default)

## fc52daa5-9919-4f80-b926-ee35ef298c54

- name: 국내주식 시간외예상체결등락률 [국내주식-140]
- path: /uapi/domestic-stock/v1/ranking/overtime-exp-trans-fluct

### query
- FID_INPUT_PRICE_2: override=0 auto= (keep, source=description, reason=blank_description)
- FID_INPUT_VOL_1: override=0 auto=1 (keep, source=heuristic, reason=qty_default)

## 43c17205-d112-4f9f-83f9-1704af8e4f79

- name: 국내주식 당사 신용가능종목[국내주식-111]
- path: /uapi/domestic-stock/v1/quotations/credit-by-company

### query
- fid_rank_sort_cls_code: override=1 auto=0 (keep, source=heuristic, reason=price_default)

## 1ecba681-1f73-4fb7-98b0-b7feef13b354

- name: 해외옵션 체결추이(일간) [해외선물-037]
- path: /uapi/overseas-futureoption/v1/quotations/opt-daily-ccnl

### query
- QRY_TP: override=Q auto= (keep, source=required_blank, reason=None)

## 94959cbc-bbb7-4776-8cd0-7058138a08aa

- name: 해외옵션 체결추이(월간) [해외선물-039]
- path: /uapi/overseas-futureoption/v1/quotations/opt-monthly-ccnl

### query
- QRY_TP: override=Q auto= (keep, source=required_blank, reason=None)

## 14431ddf-c0d5-4c33-a945-86e77bcf6486

- name: 해외옵션 체결추이(주간) [해외선물-036]
- path: /uapi/overseas-futureoption/v1/quotations/opt-weekly-ccnl

### query
- QRY_TP: override=Q auto= (keep, source=required_blank, reason=None)

## 31d46ebe-2a19-4467-9dfb-a2d21adb1e61

- name: 해외선물 분봉조회[해외선물-016]
- path: /uapi/overseas-futureoption/v1/quotations/inquire-time-futurechartprice

### query
- SRS_CD: override=BRNQ24 auto=CNHU24 ※ 종목코드 "포럼 > FAQ > 종목정보 다운로드(해외 (keep, source=description, reason=example_value)
- EXCH_CD: override=ICE auto=0 (keep, source=heuristic, reason=code_like_default)
- CLOSE_DATE_TIME: override=20240423 auto=20230823 (keep, source=description, reason=date_example)
- QRY_CNT: override=120 auto=1 (keep, source=heuristic, reason=qty_default)
- QRY_GAP: override=1 auto= (keep, source=required_blank, reason=None)

## 3acd4025-6e95-46dc-a90d-b38215912d11

- name: 해외선물옵션 장운영시간 [해외선물-030]
- path: /uapi/overseas-futureoption/v1/quotations/market-time

### query
- FM_CLAS_CD: override= auto=001 (keep, source=enum_default, reason=code_like_default)
- OPT_YN: override=% auto=N (keep, source=heuristic, reason=yn_default)

## ca0f8e3e-9f99-4ebd-a81c-c5f8017c4d65

- name: 당사 대주가능 종목 [국내주식-195]
- path: /uapi/domestic-stock/v1/quotations/lendable-by-company

### query
- THCO_STLN_PSBL_YN: override=Y auto=N (keep, source=heuristic, reason=yn_default)

## e0f9b38e-774a-441e-8dbd-27ab5f5ebb8b

- name: 예탁원정보(유상증자일정) [국내주식-143]
- path: /uapi/domestic-stock/v1/ksdinfo/paidin-capin

### query
- F_DT: override=20230101 auto=20260130 (keep, source=heuristic, reason=date_today)


## Summary

- redundant_fields: 0
- keep_fields: 251
- unknown_fields: 0