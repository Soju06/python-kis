# SRS_CD Master Probe Report

## f9f83090-60d0-4dcf-99c9-a4b36852848e
- name: 해외선물종목상세 [v1_해외선물-008]
- path: /uapi/overseas-futureoption/v1/quotations/stock-detail
- probe 1: SRS_CD=SPIG26 EXCH_CD=ASX -> ok output1:0.09(2/23)

## 621bdd34-a902-4117-98b8-57733197742a
- name: 해외옵션종목현재가 [해외선물-035]
- path: /uapi/overseas-futureoption/v1/quotations/opt-price
- probe 1: SRS_CD=1EAG26 C100 EXCH_CD=CME -> ok output1:0.00(0/32)

## 3d3ad086-7c1b-41cb-9b76-ba05ccf6ba95
- name: 해외선물종목현재가 [v1_해외선물-009]
- path: /uapi/overseas-futureoption/v1/quotations/inquire-price
- probe 1: SRS_CD=SPIG26 EXCH_CD=ASX -> ok output1:0.00(0/32)

## 14431ddf-c0d5-4c33-a945-86e77bcf6486
- name: 해외옵션 체결추이(주간) [해외선물-036]
- path: /uapi/overseas-futureoption/v1/quotations/opt-weekly-ccnl
- probe 1: SRS_CD=1EAG26 C100 EXCH_CD=CME -> error [augment] HTTP 500 for 14431ddf-c0d5-4c33-a945-86e77bcf6486
- probe 2: SRS_CD=1EAG26 C10100 EXCH_CD=CME -> error [augment] HTTP 500 for 14431ddf-c0d5-4c33-a945-86e77bcf6486
- probe 3: SRS_CD=1
1EAG26 C2100 EXCH_CD=CME -> error [augment] HTTP 500 for 14431ddf-c0d5-4c33-a945-86e77bcf6486
- probe 4: SRS_CD=I1
1EAG26 C4100 EXCH_CD=CME -> error [augment] HTTP 500 for 14431ddf-c0d5-4c33-a945-86e77bcf6486
- probe 5: SRS_CD=2I1
1EAG26 C4200 EXCH_CD=CME -> error [augment] HTTP 500 for 14431ddf-c0d5-4c33-a945-86e77bcf6486
- no low-sentinel response found in first 5 codes
