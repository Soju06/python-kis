# 퇴직연금 잔고조회[v1_국내주식-036]

> [국내주식] 주문/계좌

주식, ETF, ETN만 조회 가능하며 펀드는 조회 불가합니다.

​※ 55번 계좌(DC가입자계좌)의 경우 해당 API 이용이 불가합니다.
KIS Developers API의 경우 HTS ID에 반드시 연결되어있어야만 API 신청 및 앱정보 발급이 가능한 서비스로 개발되어서 실물계좌가 아닌 55번 계좌는 API 이용이 불가능한 점 양해 부탁드립니다.

퇴직연금 잔고조회[v1_국내주식-036]

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `fe014543-4baa-4452-a388-2d6558d1e212` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/trading/pension/inquire-balance` |
| **Content-Type** | `` |
| **요청 포맷** | `` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID** | `모의투자 미지원`, `TTTC2208R` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2022-10-28
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
| `tr_id` | 거래ID | String | 13 | Y | TTTC2208R |
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
| `ACNT_PRDT_CD` | 계좌상품코드 | String | 2 | Y | 29 |
| `ACCA_DVSN_CD` | 적립금구분코드 | String | 2 | Y | 00 |
| `INQR_DVSN` | 조회구분 | String | 2 | Y | 00 : 전체 |
| `CTX_AREA_FK100` | 연속조회검색조건100 | String | 100 | Y |  |
| `CTX_AREA_NK100` | 연속조회키100 | String | 100 | Y |  |

### 요청 예시

```json
{
  "CANO": "12345678",
  "ACNT_PRDT_CD": "29",
  "ACCA_DVSN_CD": "00",
  "INQR_DVSN": "00",
  "CTX_AREA_FK100": "",
  "CTX_AREA_NK100": ""
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
| `output1` | 응답상세 | Object |   | Y | Array |
| `cblc_dvsn_name` | 잔고구분명 | String | 60 | Y |  |
| `prdt_name` | 상품명 | String | 60 | Y |  |
| `pdno` | 상품번호 | String | 12 | Y |  |
| `item_dvsn_name` | 종목구분명 | String | 60 | Y |  |
| `thdt_buyqty` | 금일매수수량 | String | 10 | Y |  |
| `thdt_sll_qty` | 금일매도수량 | String | 10 | Y |  |
| `hldg_qty` | 보유수량 | String | 19 | Y |  |
| `ord_psbl_qty` | 주문가능수량 | String | 10 | Y |  |
| `pchs_avg_pric` | 매입평균가격 | String | 184 | Y |  |
| `pchs_amt` | 매입금액 | String | 19 | Y |  |
| `prpr` | 현재가 | String | 19 | Y |  |
| `evlu_amt` | 평가금액 | String | 19 | Y |  |
| `evlu_pfls_amt` | 평가손익금액 | String | 19 | Y |  |
| `evlu_erng_rt` | 평가수익율 | String | 238 | Y |  |
| `output2` | 응답상세2 | String |   | Y |  |
| `dnca_tot_amt` | 예수금총금액 | String | 19 | Y |  |
| `nxdy_excc_amt` | 익일정산금액 | String | 19 | Y |  |
| `prvs_rcdl_excc_amt` | 가수도정산금액 | String | 19 | Y |  |
| `thdt_buy_amt` | 금일매수금액 | String | 19 | Y |  |
| `thdt_sll_amt` | 금일매도금액 | String | 19 | Y |  |
| `thdt_tlex_amt` | 금일제비용금액 | String | 19 | Y |  |
| `scts_evlu_amt` | 유가평가금액 | String | 19 | Y |  |
| `tot_evlu_amt` | 총평가금액 | String | 19 | Y |  |

### 응답 예시

```json
{
  "ctx_area_fk100": "12345678^29^00^00^                                                                                  ",
  "ctx_area_nk100": "                                                                                                    ",
  "output1": [
    {
      "cblc_dvsn_name": "사용자",
      "prdt_name": "ACE 미국S&P500",
      "pdno": "360200",
      "item_dvsn_name": "현금",
      "thdt_buyqty": "5",
      "thdt_sll_qty": "0",
      "hldg_qty": "5",
      "ord_psbl_qty": "5",
      "pchs_avg_pric": "13235.0000",
      "pchs_amt": "66175",
      "prpr": "13235",
      "evlu_amt": "66175",
      "evlu_pfls_amt": "0",
      "evlu_erng_rt": "0.00000000"
    }
  ],
  "output2": {
    "dnca_tot_amt": "100000",
    "nxdy_excc_amt": "100000",
    "prvs_rcdl_excc_amt": "33825",
    "thdt_buy_amt": "66175",
    "thdt_sll_amt": "0",
    "thdt_tlex_amt": "0",
    "scts_evlu_amt": "66175",
    "tot_evlu_amt": "100000"
  },
  "rt_cd": "0",
  "msg_cd": "KIOK0510",
  "msg1": "조회가 완료되었습니다                                                           "
}
```
