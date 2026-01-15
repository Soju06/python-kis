# (야간)선물옵션 주문가능 조회 [국내선물-011]

> [국내선물옵션] 주문/계좌

(야간)선물옵션 주문가능 조회 API입니다.

(야간)선물옵션 주문가능 조회 [국내선물-011]

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `bca48008-6f73-4753-ab4b-aa8506145340` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-futureoption/v1/trading/inquire-psbl-ngt-order` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `(구) JTCE1004R (신) STTN5105R` |
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
| `tr_id` | 거래ID | String | 13 | Y | (구) JTCE1004R (신) STTN5105R |
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
| `PDNO` | 상품번호 | String | 12 | Y |  |
| `PRDT_TYPE_CD` | 상품유형코드 | String | 3 | Y | 301 : 선물옵션 |
| `SLL_BUY_DVSN_CD` | 매도매수구분코드 | String | 2 | Y | 01 : 매도 , 02 : 매수 |
| `UNIT_PRICE` | 주문가격1 | String | 23 | Y |  |
| `ORD_DVSN_CD` | 주문구분코드 | String | 2 | Y | '01 : 지정가        02 : 시장가  03 : 조건부        04 : 최유리,  10 : 지정가(IOC) 11 : 지정가(FOK)  12 : 시장가(IOC) ... |

### 요청 예시

```json
{
  "CANO": "80012345",
  "ACNT_PRDT_CD": "03",
  "PDNO": "101T03",
  "PRDT_TYPE_CD": "301",
  "SLL_BUY_DVSN_CD": "02",
  "UNIT_PRICE": "",
  "ORD_DVSN_CD": "01"
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
| `output` | 응답상세1 | String |   | Y |  |
| `max_ord_psbl_qty` | 최대주문가능수량 | String | 19 | Y | 최대주문가능수량 (신규 TR 미사용 필드) |
| `tot_psbl_qty` | 최대주문가능수량 | String | 19 | Y |  |
| `lqd_psbl_qty` | 청산가능수량 | String | 19 | Y | 청산가능수량 |
| `lqd_psbl_qty_1` | 청산가능수량 | String | 19 | Y | 신규 TR 사용 필드 |
| `ord_psbl_qty` | 주문가능수량 | String | 19 | Y |  |
| `bass_idx` | 기준지수 | String | 23 | Y | 신규 TR 사용 필드 |

### 응답 예시

```json
{
  "output": {
    "max_ord_psbl_qty": "996",
    "lqd_psbl_qty": "0",
    "ord_psbl_qty": "996"
  },
  "rt_cd": "0",
  "msg_cd": "KIOK0510",
  "msg1": "조회가 완료되었습니다                                                           "
}
```

