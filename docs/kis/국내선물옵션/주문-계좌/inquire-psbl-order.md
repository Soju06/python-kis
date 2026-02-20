# 선물옵션 주문가능[v1_국내선물-005]

> [국내선물옵션] 주문/계좌

선물옵션 주문가능 API입니다. 주문가능 내역과 수량을 확인하실 수 있습니다.

[국내선물-005 v1] 선물옵션 주문가능

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `d66ffd69-8d60-4490-99d0-becf63aabf41` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-futureoption/v1/trading/inquire-psbl-order` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `https://openapivts.koreainvestment.com:29443` |
| **TR ID (실전)** | `TTTO5105R` |
| **TR ID (모의)** | `VTTO5105R` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2021-12-15T13:06:32+09:00
- **최종 수정일**: 2025-04-30T12:22:02+09:00

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | N | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access Token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Credentials Grant 절차를 준용)  제휴사(Access token 유효기간 3개월, Refresh token 유효기간 1년, OAuth2.0의 Authorization Code Grant 절차를 준용) |
| `appkey` | 앱키  | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appsecret (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | [실전투자]  TTTO5105R : 선물 옵션 주문 가능  [모의투자]  VTTO5105R : 선물 옵션 주문 가능 |
| `tr_cont` | 연속 거래 여부 | String | 1 | N | tr_cont를 이용한 다음조회 불가 API |
| `custtype` | 고객타입 | String | 1 | N | B : 법인  P : 개인 |
| `seq_no` | 일련번호 | String | 2 | N | [법인 필수] 001 |
| `mac_address` | 맥주소 | String | 12 | N | 법인고객 혹은 개인고객의 Mac address 값 |
| `phone_number` | 핸드폰번호 | String | 12 | N | [법인 필수] 제휴사 APP을 사용하는 경우 사용자(회원) 핸드폰번호 ex) 01011112222 (하이픈 등 구분값 제거) |
| `ip_addr` | 접속 단말 공인 IP | String | 12 | N | 제휴사는 사용자(회원)의 IP Address 필수이며 일반고객은 제외 |
| `gt_uid` | Global UID | String | 32 | N | [법인 전용] 거래고유번호로 사용하므로 거래별로 UNIQUE해야 함 |

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `CANO` | 종합계좌번호 | String | 8 | N | 계좌번호 체계(8-2)의 앞 8자리 |
| `ACNT_PRDT_CD` | 계좌상품코드 | String | 2 | N | 계좌번호 체계(8-2)의 뒤 2자리 |
| `PDNO` | 상품번호 | String | 12 | N | 선물옵션종목코드 선물 6자리 (예: 101S03) 옵션 9자리 (예: 201S03370) |
| `SLL_BUY_DVSN_CD` | 매도매수구분코드 | String | 2 | N | 01 : 매도 02 : 매수 |
| `UNIT_PRICE` | 주문가격1 | String | 23 | N | 주문가격 ※ 주문가격 '0'일 경우  - 옵션매수 : 현재가  - 그 이외   : 기준가 |
| `ORD_DVSN_CD` | 주문구분코드 | String | 2 | N | 01 : 지정가 02 : 시장가 03 : 조건부 04 : 최유리, 10 : 지정가(IOC) 11 : 지정가(FOK) 12 : 시장가(IOC) 13 : 시장가(FOK) 14 : 최유리(IOC) 15 : 최유리(FOK) |

### 요청 예시

```json
{
  "CANO": "810XXXXX",
  "ACNT_PRDT_CD": "03",
  "PDNO": "101R12",
  "SLL_BUY_DVSN_CD": "02",
  "UNIT_PRICE": "397.95",
  "ORD_DVSN_CD": "01"
}
```

## 응답

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
| `output` | 응답상세 | String |  | Y |  |
| `tot_psbl_qty` | 총가능수량 | String | 10 | Y | 총가능수량 |
| `lqd_psbl_qty1` | 청산가능수량1 | String | 10 | Y | 청산가능수량 |
| `ord_psbl_qty` | 주문가능수량 | String | 10 | Y | 주문가능수량 |
| `bass_idx` | 기준지수 | String | 32 | Y | 기준지수 |

### 응답 예시

```json
{
  "output": {
    "tot_psbl_qty": "11679",
    "lqd_psbl_qty1": "0",
    "ord_psbl_qty": "11665",
    "bass_idx": "379.67000000"
  },
  "rt_cd": "0",
  "msg_cd": "KIOK0510",
  "msg1": "조회가 완료되었습니다                                                           "
}
```

