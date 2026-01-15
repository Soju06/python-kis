# 장내채권 잔고조회  [국내주식-198]

> [장내채권] 주문/계좌

장내채권 잔고조회 API입니다. 
한국투자 HTS(eFriend Plus) > [0979] 장내채권종합주문 화면의 "왼쪽 하단 잔고" 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `13a96552-4b77-411c-9ef6-5eed7192a76a` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-bond/v1/trading/inquire-balance` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `CTSC8407R` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-04-26
- **최종 수정일**: 2025-04-30

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials G... |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | CTSC8407R |
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
| `INQR_CNDT` | 조회조건 | String | 2 | Y | 00: 전체, 01: 상품번호단위 |
| `PDNO` | 상품번호 | String | 12 | Y | 공백 |
| `BUY_DT` | 매수일자 | String | 8 | Y | 공백 |
| `CTX_AREA_FK200` | 연속조회검색조건200 | String | 200 | Y |  |
| `CTX_AREA_NK200` | 연속조회키200 | String | 200 | Y |  |

### 요청 예시

```json
CANO:12345678
ACNT_PRDT_CD:01
INQR_CNDT:00
PDNO:
BUY_DT:
CTX_AREA_FK200:
CTX_AREA_NK200:
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
| `output` | 응답상세 | Object |   | Y | array |
| `pdno` | 상품번호 | String | 12 | Y |  |
| `prdt_name` | 상품명 | String | 60 | Y |  |
| `buy_dt` | 매수일자 | String | 8 | Y |  |
| `buy_sqno` | 매수일련번호 | String | 10 | Y |  |
| `cblc_qty` | 잔고수량 | String | 19 | Y |  |
| `agrx_qty` | 종합과세수량 | String | 10 | Y |  |
| `sprx_qty` | 분리과세수량 | String | 10 | Y |  |
| `exdt` | 만기일 | String | 8 | Y |  |
| `buy_erng_rt` | 매수수익율 | String | 238 | Y |  |
| `buy_unpr` | 매수단가 | String | 19 | Y |  |
| `buy_amt` | 매수금액 | String | 19 | Y |  |
| `ord_psbl_qty` | 주문가능수량 | String | 10 | Y |  |

### 응답 예시

```json
{
  "ctx_area_fk200": "!^!^null                                                                                                                                                                                                ",
  "ctx_area_nk200": " !^ !^                                                                                                                                                                                                  ",
  "output": [
    {
      "pdno": "KR101501D942",
      "prdt_name": "국민주택1종19-04",
      "buy_dt": "20240426",
      "buy_sqno": "1",
      "cblc_qty": "4",
      "agrx_qty": "4",
      "sprx_qty": "0",
      "exdt": "20240430",
      "buy_erng_rt": "0.00000000",
      "buy_unpr": "0",
      "buy_amt": "0",
      "ord_psbl_qty": "4"
    },
    {
      "pdno": "KR2088012A16",
      "prdt_name": "경남지역개발20-01",
      "buy_dt": "20240426",
      "buy_sqno": "1",
      "cblc_qty": "6",
      "agrx_qty": "5",
      "sprx_qty": "0",
      "exdt": "20250131",
      "buy_erng_rt": "0.00000000",
      "buy_unpr": "0",
      "buy_amt": "0",
      "ord_psbl_qty": "5"
    },
    {
      "pdno": "KR6003492D41",
      "prdt_name": "대한항공102-2",
      "buy_dt": "20240426",
      "buy_sqno": "1",
      "cblc_qty": "9",
      "agrx_qty": "9",
      "sprx_qty": "0",
      "exdt": "20260424",
      "buy_erng_rt": "0.00000000",
      "buy_unpr": "0",
      "buy_amt": "0",
      "ord_psbl_qty": "9"
    },
    {
      "pdno": "KR6095572D81",
      "prdt_name": "AJ네트웍스63-2",
      "buy_dt": "20240426",
      "buy_sqno": "1",
      "cblc_qty": "23",
      "agrx_qty": "22",
      "sprx_qty": "0",
      "exdt": "20250801",
      "buy_erng_rt": "0.00000000",
      "buy_unpr": "0",
      "buy_amt": "0",
      "ord_psbl_qty": "22"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "KIOK0460",
  "msg1": "조회 되었습니다. (마지막 자료)                                                  "
}
```

