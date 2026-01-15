# (야간)선물옵션 잔고현황 [국내선물-010]

> [국내선물옵션] 주문/계좌

(야간)선물옵션 잔고현황 API입니다.

(야간)선물옵션 잔고현황 [국내선물-010]

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `3af368ec-3627-4fdc-9bb9-4e4ff1a1968f` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-futureoption/v1/trading/inquire-ngt-balance` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `(구) JTCE6001R (신) CTFN6118R` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2022-09-23
- **최종 수정일**: 2025-06-06

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials G... |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | (구) JTCE6001R (신) CTFN6118R |
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
| `ACNT_PWD` | 계좌비밀번호 | String | 84 | Y | 공란("")으로 조회 |
| `MGNA_DVSN` | 증거금구분 | String | 2 | Y | 01 : 개시,  02 : 유지 |
| `EXCC_STAT_CD` | 정산상태코드 | String | 1 | Y | 1 : 정산 (정산가격으로 잔고 조회) 2 : 본정산 (매입가격으로 잔고 조회) |
| `CTX_AREA_FK200` | 연속조회검색조건200 | String | 200 | Y | 공란 : 최초 조회시 이전 조회 Output CTX_AREA_FK200값 : 다음페이지 조회시(2번째부터) |
| `CTX_AREA_NK200` | 연속조회키200 | String | 200 | Y | 공란 : 최초 조회시 이전 조회 Output CTX_AREA_NK200값 : 다음페이지 조회시(2번째부터) |

### 요청 예시

```json
{
  "CANO": "80012345",
  "ACNT_PRDT_CD": "03",
  "ACNT_PWD": "",
  "MGNA_DVSN": "01",
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
| `output2` | 응답상세2 | String |   | Y |  |
| `dnca_cash` | 예수금현금 | String | 19 | Y | 총주문수량 |
| `frcr_dncl_amt` | 외화예수금액 | String | 19 | Y | 주문채번지점번호 |
| `dnca_sbst` | 예수금대용 | String | 19 | Y |  |
| `tot_dncl_amt` | 총예수금액 | String | 19 | Y |  |
| `cash_mgna` | 현금증거금 | String | 19 | Y |  |
| `sbst_mgna` | 대용증거금 | String | 19 | Y |  |
| `mgna_tota` | 증거금총액 | String | 19 | Y |  |
| `opt_dfpa` | 옵션차금 | String | 19 | Y |  |
| `thdt_dfpa` | 당일차금 | String | 19 | Y |  |
| `rnwl_dfpa` | 갱신차금 | String | 19 | Y |  |
| `fee` | 수수료 | String | 19 | Y |  |
| `nxdy_dnca` | 익일예수금 | String | 19 | Y |  |
| `nxdy_dncl_amt` | 익일예수금액 | String | 19 | Y |  |
| `prsm_dpast` | 추정예탁자산 | String | 19 | Y | 종합계좌번호 |
| `pprt_ord_psbl_cash` | 적정주문가능현금 | String | 19 | Y | 총체결수량 |
| `add_mgna_cash` | 추가증거금현금 | String | 19 | Y | 총체결금액 |
| `add_mgna_tota` | 추가증거금총액 | String | 19 | Y | 종합계좌명 |
| `futr_trad_pfls_amt` | 선물매매손익금액 | String | 19 | Y | 수수료 |
| `opt_trad_pfls_amt` | 옵션매매손익금액 | String | 19 | Y | 계좌상품코드 |
| `futr_evlu_pfls_amt` | 선물평가손익금액 | String | 19 | Y | 주문일자 |
| `opt_evlu_pfls_amt` | 옵션평가손익금액 | String | 19 | Y | 주문번호 |
| `trad_pfls_amt_smtl` | 매매손익금액합계 | String | 19 | Y |  |
| `evlu_pfls_amt_smtl` | 평가손익금액합계 | String | 19 | Y |  |
| `wdrw_psbl_tot_amt` | 인출가능총금액 | String | 19 | Y |  |
| `ord_psbl_cash` | 주문가능현금 | String | 19 | Y |  |
| `ord_psbl_sbst` | 주문가능대용 | String | 19 | Y |  |
| `ord_psbl_tota` | 주문가능총액 | String | 19 | Y |  |
| `mmga_tot_amt` | 유지증거금총금액 | String | 19 | Y | 신규 TR 미사용 필드 |
| `mmga_cash_amt` | 유지증거금현금금액 | String | 19 | Y | 신규 TR 미사용 필드 |
| `mtnc_rt` | 유지비율 | String | 32238 | Y | 신규 TR 미사용 필드 |
| `isfc_amt` | 부족금액 | String | 19 | Y | 신규 TR 미사용 필드 |
| `pchs_amt_smtl` | 매입금액합계 | String | 19 | Y |  |
| `evlu_amt_smtl` | 평가금액합계 | String | 19 | Y |  |
| `output1` | 응답상세2 | Object |   | Y | 시간별체결 정보 |
| `cano` | 종합계좌번호 | String | 8 | Y |  |
| `acnt_prdt_cd` | 계좌상품코드 | String | 2 | Y |  |
| `pdno` | 상품번호 | String | 12 | Y |  |
| `prdt_type_cd` | 상품유형코드 | String | 3 | Y |  |
| `shtn_pdno` | 단축상품번호 | String | 12 | Y |  |
| `prdt_name` | 상품명 | String | 60 | Y |  |
| `sll_buy_dvsn_name` | 매도매수구분명 | String | 4 | Y | 신규 TR 사용 필드 |
| `sll_buy_dvsn_cd` | 매도매수구분코드 | String | 2 | Y |  |
| `trad_dvsn_name` | 매매구분명 | String | 60 | Y |  |
| `cblc_qty` | 잔고수량 | String | 19 | Y |  |
| `excc_unpr` | 정산단가 | String | 32238 | Y |  |
| `ccld_avg_unpr1` | 체결평균단가1 | String | 32238 | Y |  |
| `idx_clpr` | 지수종가 | String | 32238 | Y |  |
| `pchs_amt` | 매입금액 | String | 19 | Y |  |
| `evlu_amt` | 평가금액 | String | 19 | Y |  |
| `evlu_pfls_amt` | 평가손익금액 | String | 19 | Y |  |
| `trad_pfls_amt` | 매매손익금액 | String | 19 | Y |  |
| `lqd_psbl_qty` | 청산가능수량 | String | 19 | Y |  |

### 응답 예시

```json
{
  "ctx_area_fk200": "80012345^03^01^1^                                                                                                                                                                                       ",
  "ctx_area_nk200": "                                                                                                                                                                                                        ",
  "output1": [
    {
      "cano": "80012345",
      "acnt_prdt_cd": "03",
      "pdno": "KR4101SC0009",
      "prdt_type_cd": "301",
      "shtn_pdno": "101S12",
      "prdt_name": "F 202212",
      "sll_buy_dvsn_cd": "02",
      "trad_dvsn_name": "매수",
      "cblc_qty": "3",
      "excc_unpr": "309.10000000",
      "ccld_avg_unpr1": "320.50000000",
      "idx_clpr": "307.45000000",
      "pchs_amt": "231825000",
      "evlu_amt": "230587500",
      "evlu_pfls_amt": "-1237500",
      "trad_pfls_amt": "0",
      "lqd_psbl_qty": "3"
    }
  ],
  "output2": {
    "dnca_cash": "10101527360",
    "frcr_dncl_amt": "0",
    "dnca_sbst": "0",
    "tot_dncl_amt": "10101527360",
    "cash_mgna": "108922232",
    "sbst_mgna": "133854708",
    "mgna_tota": "242776940",
    "opt_dfpa": "0",
    "thdt_dfpa": "0",
    "rnwl_dfpa": "-16200000",
    "fee": "0",
    "nxdy_dnca": "10085327360",
    "prsm_dpast": "10085327360",
    "pprt_ord_psbl_cash": "9858750420",
    "add_mgna_cash": "0",
    "add_mgna_tota": "0",
    "futr_trad_pfls_amt": "0",
    "opt_trad_pfls_amt": "0",
    "futr_evlu_pfls_amt": "-1237500",
    "opt_evlu_pfls_amt": "0",
    "trad_pfls_amt_smtl": "0",
    "evlu_pfls_amt_smtl": "-1237500",
    "wdrw_psbl_tot_amt": "9858750420",
    "ord_psbl_cash": "9858750420",
    "ord_psbl_sbst": "0",
    "ord_psbl_tota": "9858750420",
    "mmga_tot_amt": "0",
    "mmga_cash_amt": "0",
    "mtnc_rt": "0.00000000",
    "isfc_amt": "0",
    "pchs_amt_smtl": "231825000",
    "evlu_amt_smtl": "230587500"
  },
  "rt_cd": "0",
  "msg_cd": "KIOK0510",
  "msg1": "조회가 완료되었습니다                                                           "
}
```

