# 해외주식 결제기준잔고 [해외주식-064]

> [해외주식] 주문/계좌

해외주식 결제기준잔고 API입니다.
한국투자 HTS(eFriend Plus) > [0829] 해외 결제기준잔고 화면 의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

※ 적용환율은 당일 매매기준이며, 현재가의 경우 지연된 시세로 평가되므로 실제매도금액과 상이할 수 있습니다.
※ 주문가능수량 : 보유수량 - 미결제 매도수량
※ 매입금액 계산 시 결제일의 최초고시환율을 적용하므로, 금일 최초고시환율을 적용하는 체결기준 잔고와는 상이합니다.
※ 해외증권 투자 및 업무문의 안내: 한국투자증권 해외투자지원부 02)3276-5300

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `8e78ed2f-8c3d-424e-b400-82fc94ca4a6b` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/overseas-stock/v1/trading/inquire-paymt-stdr-balance` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID** | `모의투자 미지원`, `CTRP6010R` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-05-24
- **최종 수정일**: 2025-04-30

## 요청 (Request)

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials G... |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | CTRP6010R |
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
| `CANO` | 종합계좌번호 | String | 8 | Y |  |
| `ACNT_PRDT_CD` | 계좌상품코드 | String | 2 | Y |  |
| `BASS_DT` | 기준일자 | String | 8 | Y |  |
| `WCRC_FRCR_DVSN_CD` | 원화외화구분코드 | String | 2 | Y | 01(원화기준),02(외화기준) |
| `INQR_DVSN_CD` | 조회구분코드 | String | 2 | Y | 00(전체), 01(일반), 02(미니스탁) |

### 요청 예시

```json
CANO:12345678
ACNT_PRDT_CD:01
BASS_DT:20240524
WCRC_FRCR_DVSN_CD:01
INQR_DVSN_CD:00
```

## 응답 (Response)

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
| `output1` | 응답상세 | Object |   | Y | array |
| `pdno` | 상품번호 | String | 12 | Y |  |
| `prdt_name` | 상품명 | String | 60 | Y |  |
| `cblc_qty13` | 잔고수량13 | String | 238 | Y |  |
| `ord_psbl_qty1` | 주문가능수량1 | String | 238 | Y |  |
| `avg_unpr3` | 평균단가3 | String | 244 | Y |  |
| `ovrs_now_pric1` | 해외현재가격1 | String | 235 | Y |  |
| `frcr_pchs_amt` | 외화매입금액 | String | 235 | Y |  |
| `frcr_evlu_amt2` | 외화평가금액2 | String | 236 | Y |  |
| `evlu_pfls_amt2` | 평가손익금액2 | String | 255 | Y |  |
| `bass_exrt` | 기준환율 | String | 238 | Y |  |
| `oprt_dtl_dtime` | 조작상세일시 | String | 17 | Y |  |
| `buy_crcy_cd` | 매수통화코드 | String | 3 | Y |  |
| `thdt_sll_ccld_qty1` | 당일매도체결수량1 | String | 238 | Y |  |
| `thdt_buy_ccld_qty1` | 당일매수체결수량1 | String | 238 | Y |  |
| `evlu_pfls_rt1` | 평가손익율1 | String | 238 | Y |  |
| `tr_mket_name` | 거래시장명 | String | 60 | Y |  |
| `natn_kor_name` | 국가한글명 | String | 60 | Y |  |
| `std_pdno` | 표준상품번호 | String | 12 | Y |  |
| `mgge_qty` | 담보수량 | String | 19 | Y |  |
| `loan_rmnd` | 대출잔액 | String | 19 | Y |  |
| `prdt_type_cd` | 상품유형코드 | String | 3 | Y |  |
| `ovrs_excg_cd` | 해외거래소코드 | String | 4 | Y |  |
| `scts_dvsn_name` | 유가증권구분명 | String | 60 | Y |  |
| `ldng_cblc_qty` | 대여잔고수량 | String | 19 | Y |  |
| `output2` | 응답상세 | Object |   | Y | array |
| `crcy_cd` | 통화코드 | String | 3 | Y |  |
| `crcy_cd_name` | 통화코드명 | String | 60 | Y |  |
| `frcr_dncl_amt_2` | 외화예수금액2 | String | 236 | Y |  |
| `frst_bltn_exrt` | 최초고시환율 | String | 238 | Y |  |
| `frcr_evlu_amt2` | 외화평가금액2 | String | 236 | Y |  |
| `output3` | 응답상세 | String |   | Y |  |
| `pchs_amt_smtl_amt` | 매입금액합계금액 | String | 19 | Y |  |
| `tot_evlu_pfls_amt` | 총평가손익금액 | String | 238 | Y |  |
| `evlu_erng_rt1` | 평가수익율1 | String | 201 | Y |  |
| `tot_dncl_amt` | 총예수금액 | String | 19 | Y |  |
| `wcrc_evlu_amt_smtl` | 원화평가금액합계 | String | 236 | Y |  |
| `tot_asst_amt2` | 총자산금액2 | String | 236 | Y |  |
| `frcr_cblc_wcrc_evlu_amt_smtl` | 외화잔고원화평가금액합계 | String | 236 | Y |  |
| `tot_loan_amt` | 총대출금액 | String | 19 | Y |  |
| `tot_ldng_evlu_amt` | 총대여평가금액 | String | 9 | Y |  |

### 응답 예시

```json
{
  "output1": [
    {
      "pdno": "ACVA",
      "prdt_name": "ACV 옥션스",
      "cblc_qty13": "5.00000000",
      "ord_psbl_qty1": "5.00000000",
      "avg_unpr3": "11137.2000",
      "ovrs_now_pric1": "26065.48600",
      "frcr_pchs_amt": "55686.00000",
      "frcr_evlu_amt2": "130327.000000",
      "evlu_pfls_amt2": "74641.00000",
      "bass_exrt": "1365.40000000",
      "oprt_dtl_dtime": "20240525104030326",
      "buy_crcy_cd": "USD",
      "thdt_sll_ccld_qty1": "0.00000000",
      "thdt_buy_ccld_qty1": "0.00000000",
      "evlu_pfls_rt1": "134.03000000",
      "tr_mket_name": "나스닥",
      "natn_kor_name": "미국",
      "std_pdno": "US00091G1040",
      "mgge_qty": "0",
      "loan_rmnd": "0",
      "prdt_type_cd": "512",
      "ovrs_excg_cd": "NASD",
      "scts_dvsn_name": "현금"
    },
    {
      "pdno": "DLPN",
      "prdt_name": "돌핀 엔터테인먼트",
      "cblc_qty13": "1.00000000",
      "ord_psbl_qty1": "1.00000000",
      "avg_unpr3": "2279.0000",
      "ovrs_now_pric1": "1529.24800",
      "frcr_pchs_amt": "2279.00000",
      "frcr_evlu_amt2": "1529.000000",
      "evlu_pfls_amt2": "-750.00000",
      "bass_exrt": "1365.40000000",
      "oprt_dtl_dtime": "20240525104052328",
      "buy_crcy_cd": "USD",
      "thdt_sll_ccld_qty1": "0.00000000",
      "thdt_buy_ccld_qty1": "0.00000000",
      "evlu_pfls_rt1": "-32.90000000",
      "tr_mket_name": "나스닥",
      "natn_kor_name": "미국",
      "std_pdno": "US25686H2094",
      "mgge_qty": "0",
      "loan_rmnd": "0",
      "prdt_type_cd": "512",
      "ovrs_excg_cd": "NASD",
      "scts_dvsn_name": "현금"
    },
    {
      "pdno": "NIO",
      "prdt_name": "니오(ADR)",
      "cblc_qty13": "1.00000000",
      "ord_psbl_qty1": "1.00000000",
      "avg_unpr3": "14316.0000",
      "ovrs_now_pric1": "6854.30800",
      "frcr_pchs_amt": "14316.00000",
      "frcr_evlu_amt2": "6854.000000",
      "evlu_pfls_amt2": "-7462.00000",
      "bass_exrt": "1365.40000000",
      "oprt_dtl_dtime": "20240528185338061",
      "buy_crcy_cd": "USD",
      "thdt_sll_ccld_qty1": "0.00000000",
      "thdt_buy_ccld_qty1": "0.00000000",
      "evlu_pfls_rt1": "-52.12000000",
      "tr_mket_name": "뉴욕거래소",
      "natn_kor_name": "미국",
      "std_pdno": "US62914V1061",
      "mgge_qty": "0",
      "loan_rmnd": "0",
      "prdt_type_cd": "513",
      "ovrs_excg_cd": "NYSE",
      "scts_dvsn_name": "현금"
    },
    {
      "pdno": "6731",
      "prdt_name": "[6731]픽셀라",
      "cblc_qty13": "4.00000000",
      "ord_psbl_qty1": "4.00000000",
      "avg_unpr3": "8851.7500",
      "ovrs_now_pric1": "922.30600",
      "frcr_pchs_amt": "35407.00000",
      "frcr_evlu_amt2": "3689.000000",
      "evlu_pfls_amt2": "-31718.00000",
      "bass_exrt": "870.10000000",
      "oprt_dtl_dtime": "20240528170115625",
      "buy_crcy_cd": "JPY",
      "thdt_sll_ccld_qty1": "0.00000000",
      "thdt_buy_ccld_qty1": "0.00000000",
      "evlu_pfls_rt1": "-89.58000000",
      "tr_mket_name": "일본",
      "natn_kor_name": "일본",
      "std_pdno": "JP3801620000",
      "mgge_qty": "0",
      "loan_rmnd": "0",
      "prdt_type_cd": "515",
      "ovrs_excg_cd": "TKSE",
      "scts_dvsn_name": "현금"
    },
    {
      "pdno": "CEI",
      "prdt_name": "캠버 에너지",
      "cblc_qty13": "1.00000000",
      "ord_psbl_qty1": "1.00000000",
      "avg_unpr3": "2255.0000",
      "ovrs_now_pric1": "238.94500",
      "frcr_pchs_amt": "2255.00000",
      "frcr_evlu_amt2": "238.000000",
      "evlu_pfls_amt2": "-2017.00000",
      "bass_exrt": "1365.40000000",
      "oprt_dtl_dtime": "20240528185356653",
      "buy_crcy_cd": "USD",
      "thdt_sll_ccld_qty1": "0.00000000",
      "thdt_buy_ccld_qty1": "0.00000000",
      "evlu_pfls_rt1": "-89.44000000",
      "tr_mket_name": "아멕스",
      "natn_kor_name": "미국",
      "std_pdno": "US13200M6075",
      "mgge_qty": "0",
      "loan_rmnd": "0",
      "prdt_type_cd": "529",
      "ovrs_excg_cd": "AMEX",
      "scts_dvsn_name": "현금"
    }
  ],
  "output2": [
    {
      "crcy_cd": "CNY",
      "crcy_cd_name": "중국위안",
      "frcr_dncl_amt_2": "1459.110000",
      "frst_bltn_exrt": "188.15000000",
      "frcr_evlu_amt2": "274531.000000"
    },
    {
      "crcy_cd": "USD",
      "crcy_cd_name": "미국달러",
      "frcr_dncl_amt_2": "698.190000",
      "frst_bltn_exrt": "1365.40000000",
      "frcr_evlu_amt2": "953308.000000"
    },
    {
      "crcy_cd": "VND",
      "crcy_cd_name": "베트남 동",
      "frcr_dncl_amt_2": "377568.000000",
      "frst_bltn_exrt": "5.36000000",
      "frcr_evlu_amt2": "20237.000000"
    }
  ],
  "output3": {
    "pchs_amt_smtl_amt": "109943",
    "tot_evlu_pfls_amt": "32694.00000000",
    "evlu_erng_rt1": "29.7300000000",
    "tot_dncl_amt": "296967",
    "wcrc_evlu_amt_smtl": "142637.000000",
    "tot_asst_amt2": "1687680.000000",
    "frcr_cblc_wcrc_evlu_amt_smtl": "1248076.000000",
    "tot_loan_amt": "0"
  },
  "rt_cd": "0",
  "msg_cd": "KIOK0530",
  "msg1": "조회되었습니다                                                                  "
}
```
