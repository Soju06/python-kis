# Type/Request Override Candidates

- Source: latest augment run (timeout)

## 77de2a74-b26c-40ca-a5b7-f87e2ef64f9f
- name: 선물옵션기간별시세(일/주/월/년)[v1_국내선물-008]
- path: /uapi/domestic-futureoption/v1/quotations/inquire-daily-fuopchartprice
- success rt_cd: 0 msg1: 정상처리 되었습니다.
- error rt_cd: 2 msg1: ERROR INVALID FID_COND_MRKT_DIV_CODE
- candidate: outputs.output1 required:false for null fields: kospi200_prdy_vrss, kospi200_prdy_ctrt, kospi200_prdy_vrss_sign
- request query keys: ['FID_COND_MRKT_DIV_CODE', 'FID_INPUT_DATE_1', 'FID_INPUT_DATE_2', 'FID_INPUT_ISCD', 'FID_PERIOD_DIV_CODE']

## 86194480-c8f0-4b0b-9d3d-001c2fc33422
- name: 선물옵션 분봉조회[v1_국내선물-012]
- path: /uapi/domestic-futureoption/v1/quotations/inquire-time-fuopchartprice
- success rt_cd: 0 msg1: 정상처리 되었습니다.
- error rt_cd: 2 msg1: ERROR INVALID FID_COND_MRKT_DIV_CODE
- candidate: outputs.output1 required:false for null fields: kospi200_prdy_vrss, kospi200_prdy_ctrt, kospi200_prdy_vrss_sign
- request query keys: ['FID_COND_MRKT_DIV_CODE', 'FID_FAKE_TICK_INCU_YN', 'FID_HOUR_CLS_CODE', 'FID_INPUT_DATE_1', 'FID_INPUT_HOUR_1', 'FID_INPUT_ISCD', 'FID_PW_DATA_INCU_YN']

## ca2e71e1-5ef4-4489-b4c4-118e10588690
- name: ELW 비교대상종목조회 [국내주식-183]
- path: /uapi/elw/v1/quotations/compare-stocks
- success rt_cd: 0 msg1: 정상처리 되었습니다.
- error rt_cd: 0 msg1: 정상처리 되었습니다.
- candidate: output_kinds.output -> array (spec=single)
- request query keys: ['FID_COND_SCR_DIV_CODE', 'FID_INPUT_ISCD']

## e5f413ec-3e68-47d7-931f-d7eb263990d9
- name: ELW LP매매추이 [국내주식-182]
- path: /uapi/elw/v1/quotations/lp-trade-trend
- success rt_cd: 0 msg1: 정상처리 되었습니다.
- error rt_cd: 2 msg1: ERROR INVALID FID_COND_MRKT_DIV_CODE
- candidate: outputs.output1 required:false for null fields: prdy_vrss_sign
- request query keys: ['FID_COND_MRKT_DIV_CODE', 'FID_INPUT_ISCD']

## 147e81db-e0d2-40cd-95f5-d8da90c2d998
- name: ELW 신규상장종목 [국내주식-181]
- path: /uapi/elw/v1/quotations/newly-listed
- error rt_cd: 2 msg1: ERROR INVALID FID_UNAS_INPUT_ISCD
- candidate: output output missing in success payload
- request query keys: ['FID_BLNC_CLS_CODE', 'FID_COND_MRKT_DIV_CODE', 'FID_COND_SCR_DIV_CODE', 'FID_DIV_CLS_CODE', 'FID_INPUT_DATE_1', 'FID_INPUT_ISCD_2', 'FID_UNAS_INPUT_ISCD']

## 4769336b-3280-419e-b69d-7531195b2221
- name: ELW 당일급변종목[국내주식-171]
- path: /uapi/elw/v1/ranking/quick-change
- error rt_cd: 2 msg1: ERROR INVALID FID_UNAS_INPUT_ISCD
- candidate: output output missing in success payload
- request query keys: ['FID_BLNG_CLS_CODE', 'FID_COND_MRKT_DIV_CODE', 'FID_COND_SCR_DIV_CODE', 'FID_HOUR_CLS_CODE', 'FID_INPUT_HOUR_1', 'FID_INPUT_HOUR_2', 'FID_INPUT_ISCD', 'FID_INPUT_PRICE_1', 'FID_INPUT_PRICE_2', 'FID_INPUT_VOL_1', 'FID_INPUT_VOL_2', 'FID_MRKT_CLS_CODE', 'FID_RANK_SORT_CLS_CODE', 'FID_UNAS_INPUT_ISCD']

## 6bd62480-d165-415e-9d82-bffe2f43aa7e
- name: ELW 거래량순위[국내주식-168]
- path: /uapi/elw/v1/ranking/volume-rank
- error rt_cd: 2 msg1: ERROR INVALID FID_UNAS_INPUT_ISCD
- candidate: output output missing in success payload
- request query keys: ['FID_BLNG_CLS_CODE', 'FID_COND_MRKT_DIV_CODE', 'FID_COND_SCR_DIV_CODE', 'FID_DIV_CLS_CODE', 'FID_INPUT_DATE_1', 'FID_INPUT_DATE_2', 'FID_INPUT_ISCD', 'FID_INPUT_ISCD_2', 'FID_INPUT_PRICE_1', 'FID_INPUT_PRICE_2', 'FID_INPUT_RMNN_DYNU_1', 'FID_INPUT_VOL_1', 'FID_INPUT_VOL_2', 'FID_RANK_SORT_CLS_CODE', 'FID_UNAS_INPUT_ISCD']

## a08c3421-e50f-4f24-b1fe-64c12f723c77
- name: 국내주식기간별시세(일/주/월/년)[v1_국내주식-016]
- path: /uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice
- success rt_cd: 0 msg1: 정상처리 되었습니다.
- error rt_cd: 2 msg1: ERROR INVALID FID_COND_MRKT_DIV_CODE
- candidate: outputs.output1 required:false for null fields: itewhol_loan_rmnd_ratem
- request query keys: ['FID_COND_MRKT_DIV_CODE', 'FID_INPUT_DATE_1', 'FID_INPUT_DATE_2', 'FID_INPUT_ISCD', 'FID_ORG_ADJ_PRC', 'FID_PERIOD_DIV_CODE']

## cf3b44a4-1864-4cc3-8650-ba4e2dbcbf06
- name: 주식현재가 회원사[v1_국내주식-013]
- path: /uapi/domestic-stock/v1/quotations/inquire-member
- success rt_cd: 0 msg1: 정상처리 되었습니다.
- error rt_cd: 2 msg1: ERROR INVALID FID_COND_MRKT_DIV_CODE
- request query keys: ['FID_COND_MRKT_DIV_CODE', 'FID_INPUT_ISCD']

## 6b0b388e-f815-4009-b46d-e08e47575ca7
- name: 국내주식 시간외호가[국내주식-077]
- path: /uapi/domestic-stock/v1/quotations/inquire-overtime-asking-price
- success rt_cd: 0 msg1: 정상처리 되었습니다.
- error rt_cd: 2 msg1: ERROR INVALID FID_COND_MRKT_DIV_CODE
- candidate: outputs.output1 required:false for null fields: ovtm_untp_askp_icdc4, ovtm_untp_askp_icdc5, ovtm_untp_askp_icdc6, ovtm_untp_askp_icdc7, ovtm_untp_askp_icdc8, ovtm_untp_askp_icdc9, ovtm_untp_askp_icdc10, ovtm_untp_bidp_icdc4, ovtm_untp_bidp_icdc5, ovtm_untp_bidp_icdc6, ovtm_untp_bidp_icdc7, ovtm_untp_bidp_icdc8, ovtm_untp_bidp_icdc9, ovtm_untp_bidp_icdc10
- request query keys: ['FID_COND_MRKT_DIV_CODE', 'FID_INPUT_ISCD']

## 1e375270-7d8d-4e4b-bcac-d11cb41542cb
- name: 국내주식 시간외현재가[국내주식-076]
- path: /uapi/domestic-stock/v1/quotations/inquire-overtime-price
- success rt_cd: 0 msg1: 정상처리 되었습니다.
- error rt_cd: 2 msg1: ERROR INVALID FID_COND_MRKT_DIV_CODE
- candidate: outputs.output required:false for null fields: mang_issu_cls_name, mrkt_warn_cls_name, revl_issu_reas_name, flng_cls_name
- request query keys: ['FID_COND_MRKT_DIV_CODE', 'FID_INPUT_ISCD']

## e53eb2e6-b292-4e2b-b150-22d92b401453
- name: ETF/ETN 현재가[v1_국내주식-068]
- path: /uapi/etfetn/v1/quotations/inquire-price
- success rt_cd: 0 msg1: 정상처리 되었습니다.
- error rt_cd: 0 msg1: 정상처리 되었습니다.
- candidate: outputs.output required:false for null fields: nmix_ctrt, mbcr_name
- request query keys: ['fid_cond_mrkt_div_code', 'fid_input_iscd']

## 636e216a-f3bb-4dc6-8bc3-e6d9babca5f1
- name: HTS조회상위20종목 [국내주식-214]
- path: /uapi/domestic-stock/v1/ranking/hts-top-view
- success rt_cd: 0 msg1: 정상처리 되었습니다.
- error rt_cd: 0 msg1: 정상처리 되었습니다.
- candidate: output_kinds.output1 -> array (spec=single)
- request query keys: []

## 4a077f43-7053-47be-b811-8e35be4ea745
- name: 국내기관_외국인 매매종목가집계[국내주식-037]
- path: /uapi/domestic-stock/v1/quotations/foreign-institution-total
- success rt_cd: 0 msg1: 정상처리 되었습니다.
- error rt_cd: 0 msg1: 정상처리 되었습니다.
- candidate: output_kinds.output -> array (spec=single)
- request query keys: ['FID_COND_MRKT_DIV_CODE', 'FID_COND_SCR_DIV_CODE', 'FID_DIV_CLS_CODE', 'FID_ETC_CLS_CODE', 'FID_INPUT_ISCD', 'FID_RANK_SORT_CLS_CODE']

## e5c6c050-e63f-4ab7-b339-d1a645d3239b
- name: 시장별 투자자매매동향(시세)[v1_국내주식-074]
- path: /uapi/domestic-stock/v1/quotations/inquire-investor-time-by-market
- success rt_cd: 0 msg1: 정상처리 되었습니다.
- error rt_cd: 0 msg1: 정상처리 되었습니다.
- candidate: output_kinds.output -> array (spec=single)
- request query keys: ['fid_input_iscd', 'fid_input_iscd_2']

## fee465d1-7fd5-4c66-b4a4-731b813d569d
- name: 관심종목(멀티종목) 시세조회 [국내주식-205]
- path: /uapi/domestic-stock/v1/quotations/intstock-multprice
- success rt_cd: 0 msg1: 정상처리 되었습니다.
- error rt_cd: 2 msg1: ERROR INVALID INPUT FID_COND_MRKT_DIV_CODE_1
- candidate: output_kinds.output -> array (spec=single)
- request query keys: ['FID_COND_MRKT_DIV_CODE_1', 'FID_COND_MRKT_DIV_CODE_10', 'FID_COND_MRKT_DIV_CODE_11', 'FID_COND_MRKT_DIV_CODE_12', 'FID_COND_MRKT_DIV_CODE_13', 'FID_COND_MRKT_DIV_CODE_14', 'FID_COND_MRKT_DIV_CODE_15', 'FID_COND_MRKT_DIV_CODE_16', 'FID_COND_MRKT_DIV_CODE_17', 'FID_COND_MRKT_DIV_CODE_18', 'FID_COND_MRKT_DIV_CODE_19', 'FID_COND_MRKT_DIV_CODE_2', 'FID_COND_MRKT_DIV_CODE_20', 'FID_COND_MRKT_DIV_CODE_21', 'FID_COND_MRKT_DIV_CODE_22', 'FID_COND_MRKT_DIV_CODE_23', 'FID_COND_MRKT_DIV_CODE_24', 'FID_COND_MRKT_DIV_CODE_25', 'FID_COND_MRKT_DIV_CODE_26', 'FID_COND_MRKT_DIV_CODE_27', 'FID_COND_MRKT_DIV_CODE_28', 'FID_COND_MRKT_DIV_CODE_29', 'FID_COND_MRKT_DIV_CODE_3', 'FID_COND_MRKT_DIV_CODE_30', 'FID_COND_MRKT_DIV_CODE_4', 'FID_COND_MRKT_DIV_CODE_5', 'FID_COND_MRKT_DIV_CODE_6', 'FID_COND_MRKT_DIV_CODE_7', 'FID_COND_MRKT_DIV_CODE_8', 'FID_COND_MRKT_DIV_CODE_9', 'FID_INPUT_ISCD_1', 'FID_INPUT_ISCD_10', 'FID_INPUT_ISCD_11', 'FID_INPUT_ISCD_12', 'FID_INPUT_ISCD_13', 'FID_INPUT_ISCD_14', 'FID_INPUT_ISCD_15', 'FID_INPUT_ISCD_16', 'FID_INPUT_ISCD_17', 'FID_INPUT_ISCD_18', 'FID_INPUT_ISCD_19', 'FID_INPUT_ISCD_2', 'FID_INPUT_ISCD_20', 'FID_INPUT_ISCD_21', 'FID_INPUT_ISCD_22', 'FID_INPUT_ISCD_23', 'FID_INPUT_ISCD_24', 'FID_INPUT_ISCD_25', 'FID_INPUT_ISCD_26', 'FID_INPUT_ISCD_27', 'FID_INPUT_ISCD_28', 'FID_INPUT_ISCD_29', 'FID_INPUT_ISCD_3', 'FID_INPUT_ISCD_30', 'FID_INPUT_ISCD_4', 'FID_INPUT_ISCD_5', 'FID_INPUT_ISCD_6', 'FID_INPUT_ISCD_7', 'FID_INPUT_ISCD_8', 'FID_INPUT_ISCD_9']

## b290d16e-aa18-4e41-9c08-f4d941efe9a1
- name: 국내주식 체결금액별 매매비중 [국내주식-192]
- path: /uapi/domestic-stock/v1/quotations/tradprt-byamt
- error rt_cd: 2 msg1: ERROR INVALID FID_COND_MRKT_DIV_CODE
- candidate: output output missing in success payload
- request query keys: ['FID_COND_MRKT_DIV_CODE', 'FID_COND_SCR_DIV_CODE', 'FID_INPUT_ISCD']

## 5c488ab2-59fd-486e-bf74-b68e813e35c0
- name: 국내휴장일조회[국내주식-040]
- path: /uapi/domestic-stock/v1/quotations/chk-holiday
- success rt_cd: 0 msg1: 조회가 계속됩니다..다음버튼을 Click 하십시오.                                   
- error rt_cd: 0 msg1: 조회가 계속됩니다..다음버튼을 Click 하십시오.                                   
- candidate: output_kinds.output -> array (spec=single)
- request query keys: ['BASS_DT', 'CTX_AREA_FK', 'CTX_AREA_NK']

## fbfe7300-7096-4938-840b-9f7c328cc5fd
- name: 종합 시황/공시(제목) [국내주식-141]
- path: /uapi/domestic-stock/v1/quotations/news-title
- error rt_cd: 0 msg1: 정상처리 되었습니다.
- candidate: output output missing in success payload
- request query keys: ['FID_COND_MRKT_CLS_CODE', 'FID_INPUT_DATE_1', 'FID_INPUT_HOUR_1', 'FID_INPUT_ISCD', 'FID_INPUT_SRNO', 'FID_NEWS_OFER_ENTP_CODE', 'FID_RANK_SORT_CLS_CODE', 'FID_TITL_CNTT']

## 9de56f62-938c-40df-970e-8fd13a59b445
- name: 국내주식 종목투자의견 [국내주식-188]
- path: /uapi/domestic-stock/v1/quotations/invest-opinion
- error rt_cd: 2 msg1: ERROR INVALID FID_COND_MRKT_DIV_CODE
- candidate: output output missing in success payload
- request query keys: ['FID_COND_MRKT_DIV_CODE', 'FID_COND_SCR_DIV_CODE', 'FID_INPUT_DATE_1', 'FID_INPUT_DATE_2', 'FID_INPUT_ISCD']

## 7d6d8ba7-bcae-4d7c-8d5b-4b51cd42a94a
- name: 장내채권현재가(일별) [국내주식-202]
- path: /uapi/domestic-bond/v1/quotations/inquire-daily-price
- success rt_cd: 0 msg1: 정상처리 되었습니다.
- error rt_cd: 2 msg1: ERROR INVALID FID_COND_MRKT_DIV_CODE
- candidate: output_kinds.output -> array (spec=single)
- request query keys: ['FID_COND_MRKT_DIV_CODE', 'FID_INPUT_ISCD']

## a274b685-7ea8-441d-a2fe-3087becb6bf2
- name: 장내채권현재가(시세) [국내주식-200]
- path: /uapi/domestic-bond/v1/quotations/inquire-price
- success rt_cd: 0 msg1: 정상처리 되었습니다.
- error rt_cd: 2 msg1: ERROR INVALID FID_COND_MRKT_DIV_CODE
- candidate: outputs.output required:false for null fields: stnd_iscd, hts_kor_isnm, prdy_vrss_sign
- request query keys: ['FID_COND_MRKT_DIV_CODE', 'FID_INPUT_ISCD']

## 3d3ad086-7c1b-41cb-9b76-ba05ccf6ba95
- name: 해외선물종목현재가 [v1_해외선물-009]
- path: /uapi/overseas-futureoption/v1/quotations/inquire-price
- success rt_cd: 0 msg1: 정상처리 되었습니다.
- error rt_cd: 0 msg1: 정상처리 되었습니다.
- request query keys: ['SRS_CD']

## 9fa44d82-f5f3-4edc-adec-8bad25800bd3
- name: 해외옵션 분봉조회 [해외선물-040]
- path: /uapi/overseas-futureoption/v1/quotations/inquire-time-optchartprice
- success rt_cd: 0 msg1: 정상처리 되었습니다.
- error rt_cd: 1 msg1: Gateway 라우팅 오류가 발생했습니다.
- candidate: outputs.output1 required:false for missing fields: data_date, data_time, open_price, high_price, low_price, last_price, last_qntt, vol, prev_diff_flag, prev_diff_price, prev_diff_rate
- request query keys: ['CLOSE_DATE_TIME', 'EXCH_CD', 'INDEX_KEY', 'QRY_CNT', 'QRY_GAP', 'QRY_TP', 'SRS_CD', 'START_DATE_TIME']

## 3acd4025-6e95-46dc-a90d-b38215912d11
- name: 해외선물옵션 장운영시간 [해외선물-030]
- path: /uapi/overseas-futureoption/v1/quotations/market-time
- success rt_cd: 0 msg1: 조회가 계속됩니다..다음버튼을 Click 하십시오.                                   
- error rt_cd: 0 msg1: 조회할 내용이 없습니다                                                          
- candidate: output_kinds.output -> array (spec=single)
- request query keys: ['CTX_AREA_FK200', 'CTX_AREA_NK200', 'FM_CLAS_CD', 'FM_EXCG_CD', 'FM_PDGR_CD', 'OPT_YN']

## 1ecba681-1f73-4fb7-98b0-b7feef13b354
- name: 해외옵션 체결추이(일간) [해외선물-037]
- path: /uapi/overseas-futureoption/v1/quotations/opt-daily-ccnl
- success rt_cd: 0 msg1: 정상처리 되었습니다.
- error rt_cd: 1 msg1: 
- candidate: outputs.output2 required:false for missing fields: data_date, data_time, open_price, high_price, low_price, last_price, last_qntt, vol, prev_diff_flag, prev_diff_price, prev_diff_rate
- request query keys: ['CLOSE_DATE_TIME', 'EXCH_CD', 'INDEX_KEY', 'QRY_CNT', 'QRY_GAP', 'QRY_TP', 'SRS_CD', 'START_DATE_TIME']

## 89c2f9ea-62be-4c4a-bd07-66f3fe3234a6
- name: 해외옵션종목상세 [해외선물-034]
- path: /uapi/overseas-futureoption/v1/quotations/opt-detail
- success rt_cd: 0 msg1: 정상처리 되었습니다.
- error rt_cd: 0 msg1: 정상처리 되었습니다.
- request query keys: ['SRS_CD']

## 94959cbc-bbb7-4776-8cd0-7058138a08aa
- name: 해외옵션 체결추이(월간) [해외선물-039]
- path: /uapi/overseas-futureoption/v1/quotations/opt-monthly-ccnl
- success rt_cd: 0 msg1: 정상처리 되었습니다.
- error rt_cd: 1 msg1: 
- candidate: outputs.output2 required:false for missing fields: data_date, data_time, open_price, high_price, low_price, last_price, last_qntt, vol, prev_diff_flag, prev_diff_price, prev_diff_rate
- request query keys: ['CLOSE_DATE_TIME', 'EXCH_CD', 'INDEX_KEY', 'QRY_CNT', 'QRY_GAP', 'QRY_TP', 'SRS_CD', 'START_DATE_TIME']

## 621bdd34-a902-4117-98b8-57733197742a
- name: 해외옵션종목현재가 [해외선물-035]
- path: /uapi/overseas-futureoption/v1/quotations/opt-price
- success rt_cd: 0 msg1: 정상처리 되었습니다.
- error rt_cd: 0 msg1: 정상처리 되었습니다.
- request query keys: ['SRS_CD']

## 41290e2a-6e25-49c0-91a1-99b96ce53efe
- name: 해외옵션 체결추이(틱) [해외선물-038]
- path: /uapi/overseas-futureoption/v1/quotations/opt-tick-ccnl
- success rt_cd: 0 msg1: 정상처리 되었습니다.
- error rt_cd: 1 msg1: 
- candidate: outputs.output2 required:false for missing fields: data_date, data_time, open_price, high_price, low_price, last_price, last_qntt, vol, prev_diff_flag, prev_diff_price, prev_diff_rate
- request query keys: ['CLOSE_DATE_TIME', 'EXCH_CD', 'INDEX_KEY', 'QRY_CNT', 'QRY_GAP', 'QRY_TP', 'SRS_CD', 'START_DATE_TIME']

## 14431ddf-c0d5-4c33-a945-86e77bcf6486
- name: 해외옵션 체결추이(주간) [해외선물-036]
- path: /uapi/overseas-futureoption/v1/quotations/opt-weekly-ccnl
- success rt_cd: 0 msg1: 정상처리 되었습니다.
- error rt_cd: 1 msg1: 
- candidate: outputs.output2 required:false for missing fields: data_date, data_time, open_price, high_price, low_price, last_price, last_qntt, vol, prev_diff_flag, prev_diff_price, prev_diff_rate
- request query keys: ['CLOSE_DATE_TIME', 'EXCH_CD', 'INDEX_KEY', 'QRY_CNT', 'QRY_GAP', 'QRY_TP', 'SRS_CD', 'START_DATE_TIME']

## f9f83090-60d0-4dcf-99c9-a4b36852848e
- name: 해외선물종목상세 [v1_해외선물-008]
- path: /uapi/overseas-futureoption/v1/quotations/stock-detail
- success rt_cd: 0 msg1: 정상처리 되었습니다.
- error rt_cd: 0 msg1: 정상처리 되었습니다.
- request query keys: ['SRS_CD']

## 81269474-9c66-404f-bdfe-4bb472975330
- name: 해외지수분봉조회[v1_해외주식-031]
- path: /uapi/overseas-price/v1/quotations/inquire-time-indexchartprice
- success rt_cd: 0 msg1: 정상처리 되었습니다.
- error rt_cd: 2 msg1: ERROR INVALID FID_COND_MRKT_DIV_CODE
- candidate: outputs.output1 required:false for null fields: hts_kor_isnm, stck_shrn_iscd
- candidate: outputs.output2 required:false for missing fields: stck_bsop_date, stck_cntg_hour, optn_prpr, optn_oprc, optn_hgpr, optn_lwpr, cntg_vol
- request query keys: ['FID_COND_MRKT_DIV_CODE', 'FID_HOUR_CLS_CODE', 'FID_INPUT_ISCD', 'FID_PW_DATA_INCU_YN']

## 7f77a12b-b23c-4605-93ea-4e1b3c0356fb
- name: 해외주식 상품기본정보[v1_해외주식-034]
- path: /uapi/overseas-price/v1/quotations/search-info
- success rt_cd: 0 msg1: 조회되었습니다                                                                  
- error rt_cd: 7 msg1: 조회된 데이터가 없습니다.(해외주식기본)                                         
- request query keys: ['PDNO', 'PRDT_TYPE_CD']

## ae084fcd-7a30-4a14-8483-91a7fc918d23
- name: 해외주식 시가총액순위[해외주식-047]
- path: /uapi/overseas-stock/v1/ranking/market-cap
- success rt_cd: 0 msg1: 정상처리 되었습니다.
- error rt_cd: 2 msg1: ERROR INVALID [EXCD]=[9999]
- request query keys: ['AUTH', 'EXCD', 'KEYB', 'VOL_RANG']

## 2549b1c6-2c8c-4826-b632-74c0b68c24e9
- name: 해외주식 가격급등락[해외주식-038]
- path: /uapi/overseas-stock/v1/ranking/price-fluct
- success rt_cd: 0 msg1: 정상처리 되었습니다.
- error rt_cd: 2 msg1: ERROR INPUT FIELD NOT FOUND [MINX]
- request query keys: ['AUTH', 'EXCD', 'GUBN', 'KEYB', 'MIXN', 'VOL_RANG']

## 40409c43-9bc7-447a-b09a-171d14b437f9
- name: 해외주식 거래량급증[해외주식-039]
- path: /uapi/overseas-stock/v1/ranking/volume-surge
- success rt_cd: 0 msg1: 정상처리 되었습니다.
- error rt_cd: 2 msg1: ERROR INPUT FIELD NOT FOUND [MINX]
- request query keys: ['AUTH', 'EXCD', 'KEYB', 'MIXN', 'VOL_RANG']
