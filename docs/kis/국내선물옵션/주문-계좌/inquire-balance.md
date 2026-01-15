# 선물옵션 잔고현황[v1_국내선물-004]

> [국내선물옵션] 주문/계좌

선물옵션 잔고현황 API입니다. 한 번의 호출에 최대 20건까지 확인 가능하며, 이후의 값은 연속조회를 통해 확인하실 수 있습니다.

[국내선물-004 v1] 선물옵션 잔고현황

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `71356fc2-c4ca-4d5f-b564-cd16b8155ecc` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-futureoption/v1/trading/inquire-balance` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `https://openapivts.koreainvestment.com:29443` |
| **TR ID** | `VTFO6118R`, `CTFO6118R` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2021-12-15
- **최종 수정일**: 2025-04-30

## 요청 (Request)

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | N | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials G... |
| `appkey` | 앱키  | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appsecret (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | [실전투자] CTFO6118R : 선물 옵션 잔고 현황  [모의투자]  VTFO6118R : 선물 옵션 잔고 현황 |
| `tr_cont` | 연속 거래 여부 | String | 1 | N | tr_cont를 이용한 다음조회 불가 API |
| `custtype` | 고객타입 | String | 1 | N | B : 법인  P : 개인 |
| `seq_no` | 일련번호 | String | 2 | N | [법인 필수] 001 |
| `mac_address` | 맥주소 | String | 12 | N | 법인고객 혹은 개인고객의 Mac address 값 |
| `phone_number` | 핸드폰번호 | String | 12 | N | [법인 필수] 제휴사APP을 사용하는 경우 사용자(회원) 핸드폰번호  ex) 01011112222 (하이픈 등 구분값 제거) |
| `ip_addr` | 접속 단말 공인 IP | String | 12 | N | [법인 필수] 사용자(회원)의 IP Address |
| `gt_uid` | Global UID | String | 32 | N | [법인 전용] 거래고유번호로 사용하므로 거래별로 UNIQUE해야 함 |

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `CANO` | 종합계좌번호 | String | 8 | Y | 계좌번호 체계(8-2)의 앞 8자리 |
| `ACNT_PRDT_CD` | 계좌상품코드 | String | 2 | Y | 계좌번호 체계(8-2)의 뒤 2자리 |
| `MGNA_DVSN` | 증거금 구분 | String | 2 | Y | 01 : 개시 02 : 유지 |
| `EXCC_STAT_CD` | 정산상태코드 | String | 1 | Y | 1 : 정산 (정산가격으로 잔고 조회) 2 : 본정산 (매입가격으로 잔고 조회) |
| `CTX_AREA_FK200` | 연속조회검색조건200 | String | 200 | Y | 공란 : 최초 조회시 이전 조회 Output CTX_AREA_FK200값 : 다음페이지 조회시(2번째부터) |
| `CTX_AREA_NK200` | 연속조회키200 | String | 200 | Y | 공란 : 최초 조회시 이전 조회 Output CTX_AREA_NK200값 : 다음페이지 조회시(2번째부터) |

### 요청 예시

```json
{
  "CANO": "810XXXXX",
  "ACNT_PRDT_CD": "3",
  "MGNA_DVSN": "01",
  "EXCC_STAT_CD": "1",
  "CTX_AREA_FK200": "",
  "CTX_AREA_NK200": ""
}
```

## 응답 (Response)

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `tr_id` | 거래ID | String | 13 | Y | 요청한 tr_id |
| `tr_cont` | 연속 거래 여부 | String | 1 | Y | tr_cont를 이용한 다음조회 불가 API |
| `gt_uid` | Global UID | String | 32 | Y | [법인 전용] 거래고유번호로 사용하므로 거래별로 UNIQUE해야 함 |

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `rt_cd` | 성공 실패 여부 | String | 1 | Y | 0 : 성공 0 이외의 값 : 실패 |
| `msg_cd` | 응답코드 | String | 8 | Y | 응답코드 |
| `msg1` | 응답메세지 | String | 80 | Y | 응답메세지 |
| `ctx_area_fk200` | 연속조회검색조건200 | String | 200 | Y |  |
| `ctx_area_nk200` | 연속조회키200 | String | 200 | Y |  |
| `output1` | 응답상세1 | String |  | Y |  |
| `cano` | 종합계좌번호 | String | 8 | Y | 계좌번호 체계(8-2)의 앞 8자리 |
| `acnt_prdt_cd` | 계좌상품코드 | String | 2 | Y | 계좌번호 체계(8-2)의 뒤 2자리 |
| `pdno` | 상품번호 | String | 12 | Y | 선물옵션종목코드 |
| `prdt_type_cd` | 상품유형코드 | String | 3 | Y |  |
| `shtn_pdno` | 단축상품번호 | String | 12 | Y | 단축상품번호 (예: 101P09) |
| `prdt_name` | 상품명 | String | 60 | Y |  |
| `sll_buy_dvsn_name` | 매도매수구분명 | String | 4 | Y | 매도/매수 구분의 명칭  - 매수잔고를 가진 경우, "매수" 혹은 "BUY"로 출력 - 매도잔고를 가진 경우, "매도" 혹은 "SLL"로 출력 - 당일 잔고를 청산하여 잔고를... |
| `cblc_qty` | 잔고수량 | String | 10 | Y | 보유한 종목의 수량 |
| `excc_unpr` | 정산단가 | String | 32 | Y | 당일 종가로 정산한 가격 |
| `ccld_avg_unpr1` | 체결평균단가1 | String | 32 | Y | 보유한 종목의 평균 체결 가격 |
| `idx_clpr` | 지수종가 | String | 32 | Y |  |
| `pchs_amt` | 매입금액 | String | 19 | Y | 보유 종목을 매수한 금액 |
| `evlu_amt` | 평가금액 | String | 19 | Y | 보유 종목을 현재가로 평가하여 산출한 금액 |
| `evlu_pfls_amt` | 평가손익금액 | String | 19 | Y | 매입금액과 평가금액을 비교한 손익 |
| `trad_pfls_amt` | 매매손익금액 | String | 19 | Y | 매수와 매도가 완료된 수량에 대한 실현 손익 |
| `lqd_psbl_qty` | 청산가능수량 | String | 19 | Y | 청산 가능한 수량 |
| `output2` | 응답상세2 | String |  | Y |  |
| `dnca_cash` | 예수금현금 | String | 19 | Y | 원화로 보유한 현금 (현금미수금액, 수수료미수금액 차감) |
| `frcr_dncl_amt` | 외화예수금액 | String | 19 | Y | 외화로 보유한 현금 |
| `dnca_sbst` | 예수금대용 | String | 19 | Y | 주식대용금액+채권대용금액+전일대용매도대용금액+당일대용매도대용금액 |
| `tot_dncl_amt` | 총예수금액 | String | 19 | Y | 상기 3개 예수금 항목의 합계 금액 |
| `tot_ccld_amt` | 총체결금액 | String | 19 | Y | 체결된 주문의 합계금액 |
| `cash_mgna` | 현금증거금 | String | 19 | Y | 원화 현금 중 주문증거금으로 사용된 금액 |
| `sbst_mgna` | 대용증거금 | String | 19 | Y | 대용 예수금 중 주문증거금으로 사용된 금액 |
| `mgna_tota` | 증거금총액 | String | 19 | Y | 증거금으로 사용된 항목의 합계 금액 |
| `opt_dfpa` | 옵션차금 | String | 19 | Y | 당일옵션매도금에서 당일옵션매수금을 차감한 금액 |
| `thdt_dfpa` | 당일차금 | String | 19 | Y | 당일의 각 매수거래에 대하여 1에 의하여 산출한 금액의 합계액과 당일의 각 매도거래에 대하여 2에 의하여 산출한 금액의 합계액을 합산한 금액 1. 매수거래수량*(당일의 정산가... |
| `rnwl_dfpa` | 갱신차금 | String | 19 | Y | 직전 거래일의 매수미결제약정에 대하여 1에 의하여 산출한 금액과 직전거래일의 매도미결제약정에 대하여 2에 의하여 산출한 금액을 합산한 금액 1. 매수미결제약정*(당일의 정산가... |
| `fee` | 수수료 | String | 19 | Y | 체결된 주문에 의한 매매수수료 |
| `nxdy_dnca` | 익일예수금 | String | 19 | Y | 당일 매매내역을 근거로 익일(결제일) 고객님 계좌에 있는 현금 |
| `nxdy_dncl_amt` | 익일예수금액 | String | 19 | Y |  |
| `prsm_dpast` | 추정예탁자산 | String | 19 | Y | 보유한 잔고를 정산 기준으로 평가한 금액과 예수금을 합한 금액 |
| `prsm_dpast_amt` | 추정예탁자산금액 | String | 19 | Y |  |
| `pprt_ord_psbl_cash` | 적정주문가능현금 | String | 19 | Y | 미수없는 주문가능금액 |
| `add_mgna_cash` | 추가증거금현금 | String | 19 | Y | 장 종료 후 예탁평가액이 유지증거금을 하회할 경우 또는 예탁현금이 결제금액 보다 적은 경우 고객이 추가적으로 납부해야 하는 증거금 |
| `add_mgna_tota` | 추가증거금총액 | String | 19 | Y |  |
| `futr_trad_pfls_amt` | 선물매매손익금액 | String | 19 | Y | 선물 매수와 매도가 완료된 수량에 대한 실현 손익 |
| `opt_trad_pfls_amt` | 옵션매매손익금액 | String | 19 | Y | 옵션 매수와 매도가 완료된 수량에 대한 실현 손익 |
| `futr_evlu_pfls_amt` | 선물평가손익금액 | String | 19 | Y | 선물 잔고의 매입가격 또는 정산가격과 평가금액을 비교한 손익 |
| `opt_evlu_pfls_amt` | 옵션평가손익금액 | String | 19 | Y | 옵션 잔고의 매입가격 또는 정산가격과 평가금액을 비교한 손익 |
| `trad_pfls_amt_smtl` | 매매손익금액합계 | String | 19 | Y | 선물매매손익금액과 옵션매매손익금액을 합한 금액 |
| `evlu_pfls_amt_smtl` | 평가손익금액합계 | String | 19 | Y | 선물평가손익금액과 옵션평가손익금액을 합한 금액 |
| `wdrw_psbl_tot_amt` | 인출가능총금액 | String | 19 | Y | 출금 가능한 현금(예탁현금+예탁대용-예탁증거금총액) |
| `ord_psbl_cash` | 주문가능현금 | String | 19 | Y | 예수금현금에서 현금증거금을 차감한 금액 |
| `ord_psbl_sbst` | 주문가능대용 | String | 19 | Y | 예수금대용에서 대용증거금을 차감한 금액 |
| `ord_psbl_tota` | 주문가능총액 | String | 19 | Y | 주문가능현금과 주문가능대용을 합한 금액 |
| `pchs_amt_smtl` | 매입금액합계 | String | 19 | Y | 종목별 매입금액의 합계 금액 |
| `evlu_amt_smtl` | 평가금액합계 | String | 19 | Y | 종목별 평가금액의 합계 금액 |

### 응답 예시

```json
{
  "ctx_area_fk200": "연속조회검색조건200을 입력하세요.",
  "output1": {
    "lqd_psbl_qty": [
      "6",
      "133",
      "110",
      "1000",
      "1000",
      "1000",
      "1000",
      "1",
      "25"
    ],
    "pdno": [
      "KR4101RC0000",
      "KR4101S30001",
      "KR4111RA0000",
      "KR41ACRC0005",
      "KR41ACS60004",
      "KR41ADRC0004",
      "KR41ADS30005",
      "KR41AES90007",
      "KR41DRRA0007"
    ],
    "prdt_type_cd": [
      "301",
      "301",
      "301",
      "301",
      "301",
      "301",
      "301",
      "301",
      "301"
    ],
    "pchs_amt": [
      "586950000",
      "12937575000",
      "78980000",
      "3003000000",
      "3012000000",
      "5686000000",
      "5672000000",
      "2610000",
      "21350000"
    ],
    "sll_buy_dvsn_name": [
      "SLL",
      "BUY",
      "BUY",
      "BUY",
      "SLL",
      "BUY",
      "SLL",
      "SLL",
      "BUY"
    ],
    "trad_pfls_amt": [
      "0",
      "0",
      "0",
      "0",
      "0",
      "0",
      "0",
      "0",
      "0"
    ],
    "shtn_pdno": [
      "101R12",
      "101S03",
      "111R10",
      "1ACR12",
      "1ACS06",
      "1ADR12",
      "1ADS03",
      "1AES09",
      "1DRR10"
    ],
    "acnt_prdt_cd": [
      "",
      "",
      "",
      "",
      "",
      "",
      "",
      "",
      ""
    ],
    "cblc_qty": [
      "6",
      "133",
      "110",
      "1000",
      "1000",
      "1000",
      "1000",
      "1",
      "25"
    ],
    "excc_unpr": [
      "391.30000000",
      "389.10000000",
      "71800.00000000",
      "3003.00000000",
      "3012.00000000",
      "5686.00000000",
      "5672.00000000",
      "2610.00000000",
      "85400.00000000"
    ],
    "cano": [
      "",
      "",
      "",
      "",
      "",
      "",
      "",
      "",
      ""
    ],
    "idx_clpr": [
      "380.55000000",
      "389.10000000",
      "71800.00000000",
      "3003.00000000",
      "3012.00000000",
      "5686.00000000",
      "5672.00000000",
      "2610.00000000",
      "85400.00000000"
    ],
    "ccld_avg_unpr1": [
      "402.28975400",
      "406.38538995",
      "71618.18181818",
      "4626.00000000",
      "4766.50000000",
      "6992.50000000",
      "5695.50000000",
      "3430.50000000",
      "87700.00000000"
    ],
    "evlu_pfls_amt": [
      "16125000",
      "0",
      "0",
      "0",
      "0",
      "0",
      "0",
      "0",
      "0"
    ],
    "evlu_amt": [
      "570825000",
      "12937575000",
      "78980000",
      "3003000000",
      "3012000000",
      "5686000000",
      "5672000000",
      "2610000",
      "21350000"
    ],
    "prdt_name": [
      "F 202112",
      "F 202203",
      "SamsungEle F 202110 (  10)",
      "BBIG K-NewDeal     F 202112",
      "BBIG K-NewDeal     F 202206",
      "Battery K-NewDeal  F 202112",
      "Battery K-NewDeal  F 202203",
      "Bio K-NewDeal      F 202209",
      "C2S        F 202110 (  10)"
    ]
  },
  "rt_cd": "0",
  "output2": {
    "nxdy_dnca": "90016125000",
    "sbst_mgna": "1391065523",
    "cash_mgna": "0",
    "ord_psbl_tota": "88608934477",
    "opt_dfpa": "0",
    "fee": "0",
    "pchs_amt_smtl": "31000465000",
    "prsm_dpast": "90016125000",
    "evlu_pfls_amt_smtl": "16125000",
    "thdt_dfpa": "0",
    "prsm_dpast_amt": "90016125000",
    "frcr_dncl_amt": "0",
    "pprt_ord_psbl_cash": "88608934477",
    "evlu_amt_smtl": "30984340000",
    "futr_trad_pfls_amt": "0",
    "rnwl_dfpa": "16125000",
    "futr_evlu_pfls_amt": "16125000",
    "wdrw_psbl_tot_amt": "88608934477",
    "dnca_sbst": "0",
    "opt_evlu_pfls_amt": "0",
    "dnca_cash": "90000000000",
    "tot_dncl_amt": "90000000000",
    "nxdy_dncl_amt": "90016125000",
    "tot_ccld_amt": "0",
    "opt_trad_pfls_amt": "0",
    "trad_pfls_amt_smtl": "0",
    "ord_psbl_cash": "88608934477",
    "mgna_tota": "1391065523",
    "ord_psbl_sbst": "0",
    "add_mgna_tota": "0",
    "add_mgna_cash": "0"
  },
  "msg1": "조회 되었습니다. (마지막 자료) ",
  "msg_cd": "KIOK0460",
  "ctx_area_nk200": ""
}
```
