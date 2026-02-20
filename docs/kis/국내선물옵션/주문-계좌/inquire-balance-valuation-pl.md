# 선물옵션 잔고평가손익내역[v1_국내선물-015]

> [국내선물옵션] 주문/계좌

선물옵션 잔고평가손익내역 API입니다.


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `7e749979-58f8-4b71-980d-2d91ba1266e8` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-futureoption/v1/trading/inquire-balance-valuation-pl` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `CTFO6159R` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2023-09-08T07:20:13+09:00
- **최종 수정일**: 2025-04-30T12:23:02+09:00

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials Grant 절차를 준용)  법인(Access token 유효기간 3개월, Refresh token 유효기간 1년, OAuth 2.0의 Authorization Code Grant 절차를 준용) |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | CTFO6159R |
| `tr_cont` | 연속 거래 여부 | String | 1 | N | 공백 : 초기 조회 N : 다음 데이터 조회 (output header의 tr_cont가 M일 경우) |
| `custtype` | 고객 타입 | String | 1 | Y | B : 법인  P : 개인 |
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
| `MGNA_DVSN` | 증거금구분 | String | 2 | Y | 01 : 개시, 02 : 유지 |
| `EXCC_STAT_CD` | 정산상태코드 | String | 1 | Y | 1 : 정산 (정산가격으로 잔고 조회) 2 : 본정산 (매입가격으로 잔고 조회) |
| `CTX_AREA_FK200` | 연속조회검색조건200 | String | 200 | Y | 연속조회검색조건200 |
| `CTX_AREA_NK200` | 연속조회키200 | String | 200 | Y | 연속조회키200 |

### 요청 예시

```json
{
  "CANO": "12345678",
  "ACNT_PRDT_CD": "03",
  "MGNA_DVSN": "02",
  "EXCC_STAT_CD": "1",
  "CTX_AREA_FK200": "",
  "CTX_AREA_NK200": ""
}
```

## 응답

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `tr_id` | 거래ID | String | 13 | Y | 요청한 tr_id |
| `tr_cont` | 연속 거래 여부 | String | 1 | N | F or M : 다음 데이터 있음 D or E : 마지막 데이터 |
| `gt_uid` | Global UID | String | 32 | N | [법인 전용] 거래고유번호로 사용하므로 거래별로 UNIQUE해야 함 |

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `rt_cd` | 성공 실패 여부 | String | 1 | Y |  |
| `msg_cd` | 응답코드 | String | 8 | Y |  |
| `msg1` | 응답메세지 | String | 80 | Y |  |
| `output2` | 응답상세 | String |   | Y |  |
| `dnca_cash` | 예수금현금 | String | 19 | Y |  |
| `frcr_dncl_amt` | 외화예수금액 | String | 19 | Y |  |
| `dnca_sbst` | 예수금대용 | String | 19 | Y |  |
| `tot_dncl_amt` | 총예수금액 | String | 19 | Y |  |
| `tot_ccld_amt` | 총체결금액 | String | 19 | Y |  |
| `cash_mgna` | 현금증거금 | String | 19 | Y |  |
| `sbst_mgna` | 대용증거금 | String | 19 | Y |  |
| `mgna_tota` | 증거금총액 | String | 19 | Y |  |
| `opt_dfpa` | 옵션차금 | String | 19 | Y |  |
| `thdt_dfpa` | 당일차금 | String | 19 | Y |  |
| `rnwl_dfpa` | 갱신차금 | String | 19 | Y |  |
| `fee` | 수수료 | String | 19 | Y |  |
| `nxdy_dnca` | 익일예수금 | String | 19 | Y |  |
| `nxdy_dncl_amt` | 익일예수금액 | String | 19 | Y |  |
| `prsm_dpast` | 추정예탁자산 | String | 19 | Y |  |
| `prsm_dpast_amt` | 추정예탁자산금액 | String | 19 | Y |  |
| `pprt_ord_psbl_cash` | 적정주문가능현금 | String | 19 | Y |  |
| `add_mgna_cash` | 추가증거금현금 | String | 19 | Y |  |
| `add_mgna_tota` | 추가증거금총액 | String | 19 | Y |  |
| `futr_trad_pfls_amt` | 선물매매손익금액 | String | 19 | Y |  |
| `opt_trad_pfls_amt` | 옵션매매손익금액 | String | 19 | Y |  |
| `futr_evlu_pfls_amt` | 선물평가손익금액 | String | 19 | Y |  |
| `opt_evlu_pfls_amt` | 옵션평가손익금액 | String | 19 | Y |  |
| `trad_pfls_amt_smtl` | 매매손익금액합계 | String | 19 | Y |  |
| `evlu_pfls_amt_smtl` | 평가손익금액합계 | String | 19 | Y |  |
| `wdrw_psbl_tot_amt` | 인출가능총금액 | String | 19 | Y |  |
| `ord_psbl_cash` | 주문가능현금 | String | 19 | Y |  |
| `ord_psbl_sbst` | 주문가능대용 | String | 19 | Y |  |
| `ord_psbl_tota` | 주문가능총액 | String | 19 | Y |  |
| `output1` | 응답상세2 | String |   | Y | array |
| `cano` | 종합계좌번호 | String | 8 | Y |  |
| `acnt_prdt_cd` | 계좌상품코드 | String | 2 | Y |  |
| `pdno` | 상품번호 | String | 12 | Y |  |
| `prdt_type_cd` | 상품유형코드 | String | 3 | Y |  |
| `shtn_pdno` | 단축상품번호 | String | 12 | Y |  |
| `prdt_name` | 상품명 | String | 60 | Y |  |
| `sll_buy_dvsn_name` | 매도매수구분명 | String | 4 | Y |  |
| `cblc_qty1` | 잔고수량1 | String | 10 | Y |  |
| `excc_unpr` | 정산단가 | String | 24 | Y |  |
| `ccld_avg_unpr1` | 체결평균단가1 | String | 24 | Y |  |
| `idx_clpr` | 지수종가 | String | 24 | Y |  |
| `pchs_amt` | 매입금액 | String | 19 | Y |  |
| `evlu_amt` | 평가금액 | String | 19 | Y |  |
| `evlu_pfls_amt` | 평가손익금액 | String | 19 | Y |  |
| `trad_pfls_amt` | 매매손익금액 | String | 19 | Y |  |
| `lqd_psbl_qty` | 청산가능수량 | String | 19 | Y |  |

### 응답 예시

```json
{
  "ctx_area_fk200": "12345678!^03!^02!^1                                                                                                                                                                                     ",
  "ctx_area_nk200": " !^ !^ !^                                                                                                                                                                                               ",
  "output1": [
    {
      "cano": "12345678",
      "acnt_prdt_cd": "03",
      "pdno": "KR4101T90003",
      "prdt_type_cd": "301",
      "shtn_pdno": "101T09",
      "prdt_name": "F 202309",
      "sll_buy_dvsn_name": "매수",
      "cblc_qty1": "2",
      "excc_unpr": "340.30000000",
      "ccld_avg_unpr1": "345.50000000",
      "idx_clpr": "0.00000000",
      "pchs_amt": "170150000",
      "evlu_amt": "0",
      "evlu_pfls_amt": "0",
      "trad_pfls_amt": "0",
      "lqd_psbl_qty": "2"
    },
    {
      "cano": "12345678",
      "acnt_prdt_cd": "03",
      "pdno": "KR4101TC0008",
      "prdt_type_cd": "301",
      "shtn_pdno": "101T12",
      "prdt_name": "F 202312",
      "sll_buy_dvsn_name": "매수",
      "cblc_qty1": "5",
      "excc_unpr": "350.00000000",
      "ccld_avg_unpr1": "335.50000000",
      "idx_clpr": "353.35000000",
      "pchs_amt": "437500000",
      "evlu_amt": "441687500",
      "evlu_pfls_amt": "4187500",
      "trad_pfls_amt": "0",
      "lqd_psbl_qty": "5"
    },
    {
      "cano": "12345678",
      "acnt_prdt_cd": "03",
      "pdno": "KR4175TA0001",
      "prdt_type_cd": "301",
      "shtn_pdno": "175T10",
      "prdt_name": "미국달러 F 202310",
      "sll_buy_dvsn_name": "매수",
      "cblc_qty1": "1",
      "excc_unpr": "1349.20000000",
      "ccld_avg_unpr1": "1338.60000000",
      "idx_clpr": "0.00000000",
      "pchs_amt": "13492000",
      "evlu_amt": "0",
      "evlu_pfls_amt": "0",
      "trad_pfls_amt": "0",
      "lqd_psbl_qty": "1"
    },
    {
      "cano": "12345678",
      "acnt_prdt_cd": "03",
      "pdno": "KR4201TA3409",
      "prdt_type_cd": "301",
      "shtn_pdno": "201T10340",
      "prdt_name": "C 202310 340.0",
      "sll_buy_dvsn_name": "매수",
      "cblc_qty1": "1",
      "excc_unpr": "2.80000000",
      "ccld_avg_unpr1": "2.80000000",
      "idx_clpr": "0.01000000",
      "pchs_amt": "700000",
      "evlu_amt": "2500",
      "evlu_pfls_amt": "-697500",
      "trad_pfls_amt": "0",
      "lqd_psbl_qty": "1"
    }
  ],
  "output2": {
    "dnca_cash": "100000000",
    "frcr_dncl_amt": "0",
    "dnca_sbst": "0",
    "tot_dncl_amt": "100000000",
    "tot_ccld_amt": "0",
    "cash_mgna": "0",
    "sbst_mgna": "23910150",
    "mgna_tota": "23910150",
    "opt_dfpa": "0",
    "thdt_dfpa": "0",
    "rnwl_dfpa": "-30138000",
    "fee": "0",
    "nxdy_dnca": "69862000",
    "nxdy_dncl_amt": "69862000",
    "prsm_dpast": "69864500",
    "prsm_dpast_amt": "69864500",
    "pprt_ord_psbl_cash": "64184775",
    "add_mgna_cash": "0",
    "add_mgna_tota": "0",
    "futr_trad_pfls_amt": "0",
    "opt_trad_pfls_amt": "0",
    "futr_evlu_pfls_amt": "4187500",
    "opt_evlu_pfls_amt": "-697500",
    "trad_pfls_amt_smtl": "0",
    "evlu_pfls_amt_smtl": "3490000",
    "wdrw_psbl_tot_amt": "34046775",
    "ord_psbl_cash": "64184775",
    "ord_psbl_sbst": "0",
    "ord_psbl_tota": "64184775"
  },
  "rt_cd": "0",
  "msg_cd": "KIOK0460",
  "msg1": "조회 되었습니다. (마지막 자료)                                                  "
}
```

