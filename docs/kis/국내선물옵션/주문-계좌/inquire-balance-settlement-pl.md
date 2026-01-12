# 선물옵션 잔고정산손익내역[v1_국내선물-013]

> [국내선물옵션] 주문/계좌

선물옵션 잔고정산손익내역 API입니다.

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `d352ed8c-30eb-4de2-83b4-62f6830b6208` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-futureoption/v1/trading/inquire-balance-settlement-pl` |
| **Content-Type** | `` |
| **요청 포맷** | `` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID** | `모의투자 미지원`, `CTFO6117R` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2023-09-08
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
| `tr_id` | 거래ID | String | 13 | Y | CTFO6117R |
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
| `INQR_DT` | 조회일자 | String | 8 | Y | 조회일자(YYYYMMDD) |
| `CTX_AREA_FK200` | 연속조회검색조건200 | String | 200 | Y | 연속조회검색조건200 |
| `CTX_AREA_NK200` | 연속조회키200 | String | 200 | Y | 연속조회키200 |

### 요청 예시

```json
{
  "CANO": "12345678",
  "ACNT_PRDT_CD": "03",
  "INQR_DT": "20230906",
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
| `tr_cont` | 연속 거래 여부 | String | 1 | N | F or M : 다음 데이터 있음 D or E : 마지막 데이터 |
| `gt_uid` | Global UID | String | 32 | N | [법인 전용] 거래고유번호로 사용하므로 거래별로 UNIQUE해야 함 |

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `rt_cd` | 성공 실패 여부 | String | 1 | Y |  |
| `msg_cd` | 응답코드 | String | 8 | Y |  |
| `msg1` | 응답메세지 | String | 80 | Y |  |
| `output2` | 응답상세 | String |   | Y |  |
| `nxdy_dnca` | 익일예수금 | String | 19 | Y |  |
| `mmga_cash` | 유지증거금현금 | String | 19 | Y |  |
| `brkg_mgna_cash` | 위탁증거금현금 | String | 19 | Y |  |
| `opt_buy_chgs` | 옵션매수대금 | String | 19 | Y |  |
| `opt_lqd_evlu_amt` | 옵션청산평가금액 | String | 19 | Y |  |
| `dnca_sbst` | 예수금대용 | String | 19 | Y |  |
| `mmga_tota` | 유지증거금총액 | String | 19 | Y |  |
| `brkg_mgna_tota` | 위탁증거금총액 | String | 19 | Y |  |
| `opt_sll_chgs` | 옵션매도대금 | String | 19 | Y |  |
| `fee` | 수수료 | String | 19 | Y |  |
| `thdt_dfpa` | 당일차금 | String | 19 | Y |  |
| `rnwl_dfpa` | 갱신차금 | String | 19 | Y |  |
| `dnca_cash` | 예수금현금 | String | 19 | Y |  |
| `output1` | 응답상세2 | String |   | Y | array |
| `pdno` | 상품번호 | String | 12 | Y |  |
| `prdt_name` | 상품명 | String | 60 | Y |  |
| `trad_dvsn_name` | 매매구분명 | String | 60 | Y |  |
| `bfdy_cblc_qty` | 전일잔고수량 | String | 19 | Y |  |
| `new_qty` | 신규수량 | String | 10 | Y |  |
| `mnpl_rpch_qty` | 전매환매수량 | String | 10 | Y |  |
| `cblc_qty` | 잔고수량 | String | 19 | Y |  |
| `cblc_amt` | 잔고금액 | String | 19 | Y |  |
| `trad_pfls_amt` | 매매손익금액 | String | 19 | Y |  |
| `evlu_amt` | 평가금액 | String | 19 | Y |  |
| `evlu_pfls_amt` | 평가손익금액 | String | 19 | Y |  |

### 응답 예시

```json
{
  "ctx_area_fk200": "12345678!^03!^20230906                                                                                                                                                                                  ",
  "ctx_area_nk200": " !^                                                                                                                                                                                                     ",
  "output1": [
    {
      "pdno": "101T09",
      "prdt_name": "F 202309",
      "trad_dvsn_name": "매수",
      "bfdy_cblc_qty": "2",
      "new_qty": "0",
      "mnpl_rpch_qty": "0",
      "cblc_qty": "2",
      "cblc_amt": "-425000",
      "trad_pfls_amt": "0",
      "evlu_amt": "149350000",
      "evlu_pfls_amt": "-1675000"
    }
  ],
  "output2": {
    "nxdy_dnca": "0",
    "mmga_cash": "0",
    "brkg_mgna_cash": "0",
    "opt_buy_chgs": "0",
    "opt_lqd_evlu_amt": "0",
    "dnca_sbst": "0",
    "mmga_tota": "0",
    "brkg_mgna_tota": "0",
    "opt_sll_chgs": "0",
    "fee": "0",
    "thdt_dfpa": "0",
    "rnwl_dfpa": "0",
    "dnca_cash": "0"
  },
  "rt_cd": "0",
  "msg_cd": "KIOK0460",
  "msg1": "조회 되었습니다. (마지막 자료)                                                  "
}
```
