# 주식예약주문조회[v1_국내주식-020]

> [국내주식] 주문/계좌

국내예약주문 처리내역 조회 API 입니다.
실전계좌/모의계좌의 경우, 한 번의 호출에 최대 20건까지 확인 가능하며, 이후의 값은 연속조회를 통해 확인하실 수 있습니다.

[국내주식-020 v1] 주식예약주문조회

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `4da32292-291d-4b58-9ab4-f9d40ca983a6` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/trading/order-resv-ccnl` |
| **Content-Type** | `application/json; charset=utf-8` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID** | `모의투자 미지원`, `CTSC0004R` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2022-05-04
- **최종 수정일**: 2025-04-30

## 요청 (Request)

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | N | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials G... |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appsecret (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | [실전투자] CTSC0004R : 국내주식예약주문조회 * 모의투자 사용 불가 |
| `tr_cont` | 연속 거래 여부 | String | 1 | N | 공백 : 초기 조회 N : 다음 데이터 조회 (output header의 tr_cont가 M일 경우) |
| `custtype` | 고객타입 | String | 1 | N | B : 법인  P : 개인 |
| `seq_no` | 일련번호 | String | 2 | N | [법인 필수] 001 |
| `mac_address` | 맥주소 | String | 12 | N | 법인고객 혹은 개인고객의 Mac address 값 |
| `phone_number` | 핸드폰번호 | String | 12 | N | [법인 필수] 제휴사APP을 사용하는 경우 사용자(회원) 핸드폰번호  ex) 01011112222 (하이픈 등 구분값 제거) |
| `ip_addr` | 접속 단말 공인 IP | String | 12 | N | [법인 필수] 사용자(회원)의 IP Address |
| `gt_uid` | Global UID | String | 32 | N | [법인 전용] 거래고유번호로 사용하므로 거래별로 UNIQUE해야 함 |

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `RSVN_ORD_ORD_DT` | 예약주문시작일자 | String | 8 | Y |  |
| `RSVN_ORD_END_DT` | 예약주문종료일자 | String | 8 | Y |  |
| `RSVN_ORD_SEQ` | 예약주문순번 | String | 10 | Y |  |
| `TMNL_MDIA_KIND_CD` | 단말매체종류코드 | String | 2 | Y | "00" 입력 |
| `CANO` | 종합계좌번호 | String | 8 | Y | 계좌번호 체계(8-2)의 앞 8자리 |
| `ACNT_PRDT_CD` | 계좌상품코드 | String | 2 | Y | 계좌번호 체계(8-2)의 뒤 2자리 |
| `PRCS_DVSN_CD` | 처리구분코드 | String | 2 | Y | 0: 전체 1: 처리내역 2: 미처리내역 |
| `CNCL_YN` | 취소여부 | String | 1 | Y | "Y" 유효한 주문만 조회 |
| `PDNO` | 상품번호 | String | 12 | Y | 종목코드(6자리) (공백 입력 시 전체 조회) |
| `SLL_BUY_DVSN_CD` | 매도매수구분코드 | String | 2 | Y |  |
| `CTX_AREA_FK200` | 연속조회검색조건200 | String | 200 | Y | 다음 페이지 조회시 사용 |
| `CTX_AREA_NK200` | 연속조회키200 | String | 200 | Y | 다음 페이지 조회시 사용 |

### 요청 예시

```json
{
  "RSVN_ORD_ORD_DT": "20220520",
  "RSVN_ORD_END_DT": "20220523",
  "RSVN_ORD_SEQ": "",
  "TMNL_MDIA_KIND_CD": "00",
  "CANO": "81019970",
  "ACNT_PRDT_CD": "01",
  "PRCS_DVSN_CD": "0",
  "CNCL_YN": "Y",
  "PDNO": "",
  "SLL_BUY_DVSN_CD": "",
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
| `tr_cont` | 연속 거래 여부 | String | 1 | Y | F or M : 다음 데이터 있음 D or E : 마지막 데이터 |
| `gt_uid` | Global UID | String | 32 | Y | [법인 전용] 거래고유번호로 사용하므로 거래별로 UNIQUE해야 함 |

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `rt_cd` | 성공 실패 여부 | String | 1 | Y | 0 : 성공  0 이외의 값 : 실패 |
| `msg_cd` | 응답코드 | String | 8 | Y |  |
| `msg1` | 응답메세지 | String | 80 | Y |  |
| `output` | 응답상세 | String |  | Y |  |
| `rsvn_ord_seq` | 예약주문 순번 | String | 10 | N |  |
| `rsvn_ord_ord_dt` | 예약주문주문일자 | String | 8 | N |  |
| `rsvn_ord_rcit_dt` | 예약주문접수일자 | String | 8 | N |  |
| `pdno` | 상품번호 | String | 12 | N |  |
| `ord_dvsn_cd` | 주문구분코드 | String | 2 | N |  |
| `ord_rsvn_qty` | 주문예약수량 | String | 10 | N |  |
| `tot_ccld_qty` | 총체결수량 | String | 10 | N |  |
| `cncl_ord_dt` | 취소주문일자 | String | 8 | N |  |
| `ord_tmd` | 주문시각 | String | 6 | N |  |
| `ctac_tlno` | 연락전화번호 | String | 20 | N |  |
| `rjct_rson2` | 거부사유2 | String | 200 | N |  |
| `odno` | 주문번호 | String | 10 | N |  |
| `rsvn_ord_rcit_tmd` | 예약주문접수시각 | String | 6 | N |  |
| `kor_item_shtn_name` | 한글종목단축명 | String | 60 | N |  |
| `sll_buy_dvsn_cd` | 매도매수구분코드 | String | 2 | N |  |
| `ord_rsvn_unpr` | 주문예약단가 | String | 19 | N |  |
| `tot_ccld_amt` | 총체결금액 | String | 19 | N |  |
| `loan_dt` | 대출일자 | String | 8 | N |  |
| `cncl_rcit_tmd` | 취소접수시각 | String | 6 | N |  |
| `prcs_rslt` | 처리결과 | String | 60 | N |  |
| `ord_dvsn_name` | 주문구분명 | String | 60 | N |  |
| `tmnl_mdia_kind_cd` | 단말매체종류코드 | String | 2 | N |  |
| `rsvn_end_dt` | 예약종료일자 | String | 8 | N |  |

### 응답 예시

```json
{
  "ctx_area_fk200": "20220520!^null!^0!^Y!^!^                                                                                                                                                                                ",
  "ctx_area_nk200": " !^ !^                                                                                                                                                                                                  ",
  "output": [
    {
      "rsvn_ord_seq": "42401",
      "rsvn_ord_ord_dt": "20220523",
      "rsvn_ord_rcit_dt": "20220520",
      "pdno": "005940",
      "ord_dvsn_cd": "01",
      "ord_rsvn_qty": "1",
      "tot_ccld_qty": "0",
      "cncl_ord_dt": "",
      "ord_tmd": "",
      "ctac_tlno": "0",
      "rjct_rson2": "",
      "odno": "",
      "rsvn_ord_rcit_tmd": "165318",
      "kor_item_shtn_name": "NH투자증권",
      "sll_buy_dvsn_cd": "02",
      "ord_rsvn_unpr": "6000",
      "tot_ccld_amt": "0",
      "loan_dt": "",
      "cncl_rcit_tmd": "",
      "prcs_rslt": "미처리",
      "ord_dvsn_name": "현금매수",
      "tmnl_mdia_kind_cd": "31",
      "rsvn_end_dt": "20220523"
    },
    {
      "rsvn_ord_seq": "42405",
      "rsvn_ord_ord_dt": "20220523",
      "rsvn_ord_rcit_dt": "20220520",
      "pdno": "005940",
      "ord_dvsn_cd": "01",
      "ord_rsvn_qty": "1",
      "tot_ccld_qty": "0",
      "cncl_ord_dt": "",
      "ord_tmd": "",
      "ctac_tlno": "0",
      "rjct_rson2": "",
      "odno": "",
      "rsvn_ord_rcit_tmd": "170422",
      "kor_item_shtn_name": "NH투자증권",
      "sll_buy_dvsn_cd": "02",
      "ord_rsvn_unpr": "6000",
      "tot_ccld_amt": "0",
      "loan_dt": "",
      "cncl_rcit_tmd": "",
      "prcs_rslt": "미처리",
      "ord_dvsn_name": "현금매수",
      "tmnl_mdia_kind_cd": "31",
      "rsvn_end_dt": ""
    },
    {
      "rsvn_ord_seq": "42406",
      "rsvn_ord_ord_dt": "20220523",
      "rsvn_ord_rcit_dt": "20220520",
      "pdno": "005940",
      "ord_dvsn_cd": "01",
      "ord_rsvn_qty": "1",
      "tot_ccld_qty": "0",
      "cncl_ord_dt": "",
      "ord_tmd": "",
      "ctac_tlno": "0",
      "rjct_rson2": "",
      "odno": "",
      "rsvn_ord_rcit_tmd": "170453",
      "kor_item_shtn_name": "NH투자증권",
      "sll_buy_dvsn_cd": "02",
      "ord_rsvn_unpr": "6000",
      "tot_ccld_amt": "0",
      "loan_dt": "",
      "cncl_rcit_tmd": "",
      "prcs_rslt": "미처리",
      "ord_dvsn_name": "현금매수",
      "tmnl_mdia_kind_cd": "31",
      "rsvn_end_dt": "20220523"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "KIOK0460",
  "msg1": "조회 되었습니다. (마지막 자료)                                                  "
}
```
