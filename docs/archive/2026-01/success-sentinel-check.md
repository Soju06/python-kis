# Success Payload Sentinel Check

- Criteria: fields with all values in {"", 0, 0.0, 00000000, None, null, nan, 888888} counted as sentinel

## 77de2a74-b26c-40ca-a5b7-f87e2ef64f9f
- rt_cd: 0 msg1: 정상처리 되었습니다.
- output1: sentinel_fields=3/30 ratio=0.10
- output2: sentinel_fields=0/8 ratio=0.00

## 86194480-c8f0-4b0b-9d3d-001c2fc33422
- rt_cd: 0 msg1: 정상처리 되었습니다.
- output1: sentinel_fields=3/31 ratio=0.10
- output2: sentinel_fields=0/8 ratio=0.00

## ca2e71e1-5ef4-4489-b4c4-118e10588690
- rt_cd: 0 msg1: 정상처리 되었습니다.
- output: sentinel_fields=0/2 ratio=0.00

## e5f413ec-3e68-47d7-931f-d7eb263990d9
- rt_cd: 0 msg1: 정상처리 되었습니다.
- output1: sentinel_fields=11/16 ratio=0.69
  - sentinel_fields: elw_prpr, prdy_vrss_sign, prdy_vrss, prdy_ctrt, acml_vol, prdy_vol, prit, invl_val, tmvl_val, acpr, elw_ko_barrier
- output2: sentinel_fields=1/13 ratio=0.08

## 147e81db-e0d2-40cd-95f5-d8da90c2d998
- success.json: missing

## 4769336b-3280-419e-b69d-7531195b2221
- success.json: missing

## 6bd62480-d165-415e-9d82-bffe2f43aa7e
- success.json: missing

## a08c3421-e50f-4f24-b1fe-64c12f723c77
- rt_cd: 0 msg1: 정상처리 되었습니다.
- output1: sentinel_fields=1/30 ratio=0.03
- output2: sentinel_fields=2/13 ratio=0.15

## cf3b44a4-1864-4cc3-8650-ba4e2dbcbf06
- rt_cd: 0 msg1: 정상처리 되었습니다.
- output: sentinel_fields=0/67 ratio=0.00

## 6b0b388e-f815-4009-b46d-e08e47575ca7
- rt_cd: 0 msg1: 정상처리 되었습니다.
- output: sentinel_fields=70/74 ratio=0.95
  - sentinel_fields: ovtm_untp_askp1, ovtm_untp_askp2, ovtm_untp_askp3, ovtm_untp_askp4, ovtm_untp_askp5, ovtm_untp_askp6, ovtm_untp_askp7, ovtm_untp_askp8, ovtm_untp_askp9, ovtm_untp_askp10, ovtm_untp_bidp1, ovtm_untp_bidp2, ovtm_untp_bidp3, ovtm_untp_bidp4, ovtm_untp_bidp5, ovtm_untp_bidp6, ovtm_untp_bidp7, ovtm_untp_bidp8, ovtm_untp_bidp9, ovtm_untp_bidp10, ovtm_untp_askp_icdc1, ovtm_untp_askp_icdc2, ovtm_untp_askp_icdc3, ovtm_untp_askp_icdc4, ovtm_untp_askp_icdc5, ovtm_untp_askp_icdc6, ovtm_untp_askp_icdc7, ovtm_untp_askp_icdc8, ovtm_untp_askp_icdc9, ovtm_untp_askp_icdc10, ovtm_untp_bidp_icdc1, ovtm_untp_bidp_icdc2, ovtm_untp_bidp_icdc3, ovtm_untp_bidp_icdc4, ovtm_untp_bidp_icdc5, ovtm_untp_bidp_icdc6, ovtm_untp_bidp_icdc7, ovtm_untp_bidp_icdc8, ovtm_untp_bidp_icdc9, ovtm_untp_bidp_icdc10

## 1e375270-7d8d-4e4b-bcac-d11cb41542cb
- rt_cd: 0 msg1: 정상처리 되었습니다.
- output: sentinel_fields=16/35 ratio=0.46

## e53eb2e6-b292-4e2b-b150-22d92b401453
- rt_cd: 0 msg1: 정상처리 되었습니다.
- output: sentinel_fields=20/59 ratio=0.34

## 636e216a-f3bb-4dc6-8bc3-e6d9babca5f1
- rt_cd: 0 msg1: 정상처리 되었습니다.
- output1: sentinel_fields=0/2 ratio=0.00

## 4a077f43-7053-47be-b811-8e35be4ea745
- rt_cd: 0 msg1: 정상처리 되었습니다.
- output: sentinel_fields=4/26 ratio=0.15

## e5c6c050-e63f-4ab7-b339-d1a645d3239b
- rt_cd: 0 msg1: 정상처리 되었습니다.
- output: sentinel_fields=72/72 ratio=1.00
  - sentinel_fields: frgn_seln_vol, frgn_shnu_vol, frgn_ntby_qty, frgn_seln_tr_pbmn, frgn_shnu_tr_pbmn, frgn_ntby_tr_pbmn, prsn_seln_vol, prsn_shnu_vol, prsn_ntby_qty, prsn_seln_tr_pbmn, prsn_shnu_tr_pbmn, prsn_ntby_tr_pbmn, orgn_seln_vol, orgn_shnu_vol, orgn_ntby_qty, orgn_seln_tr_pbmn, orgn_shnu_tr_pbmn, orgn_ntby_tr_pbmn, scrt_seln_vol, scrt_shnu_vol, scrt_ntby_qty, scrt_seln_tr_pbmn, scrt_shnu_tr_pbmn, scrt_ntby_tr_pbmn, ivtr_seln_vol, ivtr_shnu_vol, ivtr_ntby_qty, ivtr_seln_tr_pbmn, ivtr_shnu_tr_pbmn, ivtr_ntby_tr_pbmn, pe_fund_seln_tr_pbmn, pe_fund_seln_vol, pe_fund_ntby_vol, pe_fund_shnu_tr_pbmn, pe_fund_shnu_vol, pe_fund_ntby_tr_pbmn, bank_seln_vol, bank_shnu_vol, bank_ntby_qty, bank_seln_tr_pbmn

## fee465d1-7fd5-4c66-b4a4-731b813d569d
- rt_cd: 0 msg1: 정상처리 되었습니다.
- output: sentinel_fields=6/29 ratio=0.21

## b290d16e-aa18-4e41-9c08-f4d941efe9a1
- success.json: missing

## 5c488ab2-59fd-486e-bf74-b68e813e35c0
- rt_cd: 0 msg1: 조회가 계속됩니다..다음버튼을 Click 하십시오.                                   
- output: sentinel_fields=0/6 ratio=0.00

## fbfe7300-7096-4938-840b-9f7c328cc5fd
- success.json: missing

## 9de56f62-938c-40df-970e-8fd13a59b445
- success.json: missing

## 7d6d8ba7-bcae-4d7c-8d5b-4b51cd42a94a
- rt_cd: 0 msg1: 정상처리 되었습니다.
- output: sentinel_fields=0/9 ratio=0.00

## a274b685-7ea8-441d-a2fe-3087becb6bf2
- rt_cd: 0 msg1: 정상처리 되었습니다.
- output: sentinel_fields=13/17 ratio=0.76
  - sentinel_fields: stnd_iscd, hts_kor_isnm, bond_prpr, prdy_vrss_sign, bond_prdy_vrss, prdy_ctrt, acml_vol, bond_prdy_clpr, bond_oprc, bond_hgpr, bond_lwpr, bond_mxpr, bond_llam

## 3d3ad086-7c1b-41cb-9b76-ba05ccf6ba95
- rt_cd: 0 msg1: 정상처리 되었습니다.
- output1: sentinel_fields=32/32 ratio=1.00
  - sentinel_fields: proc_date, high_price, proc_time, open_price, trst_mgn, low_price, last_price, vol, prev_diff_flag, prev_diff_price, prev_diff_rate, bid_qntt, bid_price, ask_qntt, ask_price, prev_price, exch_cd, crc_cd, trd_fr_date, expr_date, trd_to_date, remn_cnt, last_qntt, tot_ask_qntt, tot_bid_qntt, tick_size, open_date, open_time, close_date, close_time, sbsnsdate, sttl_price

## 9fa44d82-f5f3-4edc-adec-8bad25800bd3
- rt_cd: 0 msg1: 정상처리 되었습니다.
- output1: sentinel_fields=0/0 ratio=0.00
- output2: sentinel_fields=3/3 ratio=1.00
  - sentinel_fields: ret_cnt, last_n_cnt, index_key

## 3acd4025-6e95-46dc-a90d-b38215912d11
- rt_cd: 0 msg1: 조회가 계속됩니다..다음버튼을 Click 하십시오.                                   
- output: sentinel_fields=4/15 ratio=0.27

## 1ecba681-1f73-4fb7-98b0-b7feef13b354
- rt_cd: 0 msg1: 정상처리 되었습니다.
- output1: sentinel_fields=2/3 ratio=0.67
  - sentinel_fields: last_n_cnt, index_key
- output2: sentinel_fields=0/0 ratio=0.00

## 89c2f9ea-62be-4c4a-bd07-66f3fe3234a6
- rt_cd: 0 msg1: 정상처리 되었습니다.
- output1: sentinel_fields=21/21 ratio=1.00
  - sentinel_fields: exch_cd, clas_cd, crc_cd, sttl_price, sttl_date, trst_mgn, disp_digit, tick_sz, tick_val, mrkt_open_date, mrkt_open_time, mrkt_close_date, mrkt_close_time, trd_fr_date, expr_date, trd_to_date, remn_cnt, stat_tp, ctrt_size, stl_tp, frst_noti_date

## 94959cbc-bbb7-4776-8cd0-7058138a08aa
- rt_cd: 0 msg1: 정상처리 되었습니다.
- output1: sentinel_fields=2/3 ratio=0.67
  - sentinel_fields: last_n_cnt, index_key
- output2: sentinel_fields=0/0 ratio=0.00

## 621bdd34-a902-4117-98b8-57733197742a
- rt_cd: 0 msg1: 정상처리 되었습니다.
- output1: sentinel_fields=31/31 ratio=1.00
  - sentinel_fields: proc_date, proc_time, open_price, high_price, low_price, last_price, vol, prev_diff_flag, prev_diff_price, prev_diff_rate, bid_qntt, bid_price, ask_qntt, ask_price, trst_mgn, exch_cd, crc_cd, trd_fr_date, expr_date, trd_to_date, remn_cnt, last_qntt, tot_ask_qntt, tot_bid_qntt, tick_size, open_date, open_time, close_date, close_time, sbsnsdate, sttl_price

## 41290e2a-6e25-49c0-91a1-99b96ce53efe
- rt_cd: 0 msg1: 정상처리 되었습니다.
- output1: sentinel_fields=1/3 ratio=0.33
- output2: sentinel_fields=0/0 ratio=0.00

## 14431ddf-c0d5-4c33-a945-86e77bcf6486
- rt_cd: 0 msg1: 정상처리 되었습니다.
- output1: sentinel_fields=2/3 ratio=0.67
  - sentinel_fields: last_n_cnt, index_key
- output2: sentinel_fields=0/0 ratio=0.00

## f9f83090-60d0-4dcf-99c9-a4b36852848e
- rt_cd: 0 msg1: 정상처리 되었습니다.
- output1: sentinel_fields=23/23 ratio=1.00
  - sentinel_fields: exch_cd, tick_sz, disp_digit, trst_mgn, sttl_date, prev_price, crc_cd, clas_cd, tick_val, mrkt_open_date, mrkt_open_time, mrkt_close_date, mrkt_close_time, trd_fr_date, expr_date, trd_to_date, remn_cnt, stat_tp, ctrt_size, stl_tp, frst_noti_date, sprd_srs_cd1, sprd_srs_cd2

## 81269474-9c66-404f-bdfe-4bb472975330
- rt_cd: 0 msg1: 정상처리 되었습니다.
- output1: sentinel_fields=10/11 ratio=0.91
  - sentinel_fields: ovrs_nmix_prdy_vrss, hts_kor_isnm, prdy_ctrt, ovrs_nmix_prdy_clpr, acml_vol, ovrs_nmix_prpr, stck_shrn_iscd, ovrs_prod_oprc, ovrs_prod_hgpr, ovrs_prod_lwpr
- output2: sentinel_fields=0/0 ratio=0.00

## 7f77a12b-b23c-4605-93ea-4e1b3c0356fb
- rt_cd: 0 msg1: 조회되었습니다                                                                  
- output: sentinel_fields=12/55 ratio=0.22

## ae084fcd-7a30-4a14-8483-91a7fc918d23
- rt_cd: 0 msg1: 정상처리 되었습니다.
- output1: sentinel_fields=0/5 ratio=0.00
- output2: sentinel_fields=0/15 ratio=0.00

## 2549b1c6-2c8c-4826-b632-74c0b68c24e9
- rt_cd: 0 msg1: 정상처리 되었습니다.
- output1: sentinel_fields=0/3 ratio=0.00
- output2: sentinel_fields=0/16 ratio=0.00

## 40409c43-9bc7-447a-b09a-171d14b437f9
- rt_cd: 0 msg1: 정상처리 되었습니다.
- output1: sentinel_fields=0/3 ratio=0.00
- output2: sentinel_fields=0/16 ratio=0.00
