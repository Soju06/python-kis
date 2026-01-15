# 선물옵션 정정취소주문[v1_국내선물-002]

> [국내선물옵션] 주문/계좌

선물옵션 주문 건에 대하여 정정 및 취소하는 API입니다. 단, 이미 체결된 건은 정정 및 취소가 불가합니다.

※ POST API의 경우 BODY값의 key값들을 대문자로 작성하셔야 합니다.
   (EX. "CANO" : "12345678", "ACNT_PRDT_CD": "01",...)

[국내선물-002 v1] 선물옵션정정취소주문

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `a3c3305a-7624-4049-b0f3-6bcca689d1f5` |
| **HTTP Method** | `POST` |
| **URL** | `/uapi/domestic-futureoption/v1/trading/order-rvsecncl` |
| **Content-Type** | `application/json; charset=UTF-8` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `https://openapivts.koreainvestment.com:29443` |
| **TR ID (실전)** | `(주간 정정/취소) TTTO1103U (야간 정정/취소) (구) JTCE1002U (신) STTN1103U` |
| **TR ID (모의)** | `(주간 정정/취소) VTTO1103U (야간은 모의투자 미제공)` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2021-12-15
- **최종 수정일**: 2025-06-23

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | N | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials G... |
| `appkey` | 앱키  | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appsecret (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | [실전투자] TTTO1103U : 선물 옵션 정정 취소 주문 주간 (구) JTCE1002U : 선물 옵션 정정 취소 주문 야간 (신) STTN1103U : 선물 옵션 정정 취... |
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
| `ORD_PRCS_DVSN_CD` | 주문처리구분코드 | String | 2 | Y | 02 : 주문전송 |
| `CANO` | 종합계좌번호 | String | 8 | Y | 계좌번호 체계(8-2)의 앞 8자리 |
| `ACNT_PRDT_CD` | 계좌상품코드 | String | 2 | Y | 계좌번호 체계(8-2)의 뒤 2자리 |
| `RVSE_CNCL_DVSN_CD` | 정정취소구분코드 | String | 2 | Y | 01 : 정정 02 : 취소 |
| `ORGN_ODNO` | 원주문번호 | String | 10 | Y | 정정 혹은 취소할 주문의 번호 |
| `ORD_QTY` | 주문수량 | String | 10 | Y | [Header tr_id TTTO1103U(선물옵션 정정취소 주간)] 전량일경우 0으로 입력  [Header tr_id JTCE1002U(선물옵션 정정취소 야간)] 일부수량 ... |
| `UNIT_PRICE` | 주문가격1 | String | 23 | Y | 시장가나 최유리의 경우 0으로 입력 (취소 시에도 0 입력) |
| `NMPR_TYPE_CD` | 호가유형코드 | String | 2 | Y | 01 : 지정가 02 : 시장가 03 : 조건부 04 : 최유리 |
| `KRX_NMPR_CNDT_CD` | 한국거래소호가조건코드 | String | 1 | Y | 취소시 0으로 입력 정정시 0 : 없음 3 : IOC 4 : FOK |
| `RMN_QTY_YN` | 잔여수량여부 | String | 1 | Y | Y : 전량 N : 일부 |
| `FUOP_ITEM_DVSN_CD` | 선물옵션종목구분코드 | String | 2 | N | [Header tr_id TTTO1103U(선물옵션 정정취소 주간)] 공란(Default)  [Header tr_id JTCE1002U(선물옵션 정정취소 야간)] 01 : 선... |
| `ORD_DVSN_CD` | 주문구분코드 | String | 2 | Y | [정정] 01 : 지정가 02 : 시장가 03 : 조건부 04 : 최유리, 10 : 지정가(IOC) 11 : 지정가(FOK) 12 : 시장가(IOC) 13 : 시장가(FOK)... |

### 요청 예시

```json
{
  "ORD_PRCS_DVSN_CD": "02",
  "CANO": "810XXXXX",
  "ACNT_PRDT_CD": "03",
  "RVSE_CNCL_DVSN_CD": "02",
  "ORGN_ODNO": "0000005605",
  "ORD_QTY": "1",
  "UNIT_PRICE": "460.00",
  "NMPR_TYPE_CD": "",
  "KRX_NMPR_CNDT_CD": "",
  "RMN_QTY_YN": "N",
  "CTAC_TLNO": "000 00000000",
  "FUOP_ITEM_DVSN_CD": "",
  "ORD_DVSN_CD": "01"
}
```

## 응답

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `rt_cd` | 성공 실패 여부 | String | 1 | Y | 0 : 성공 0 이외의 값 : 실패 |
| `msg_cd` | 응답코드 | String | 8 | Y | 응답코드 |
| `msg1` | 응답메세지 | String | 80 | Y | 응답메세지 |
| `output` | 응답상세 | String |  | Y |  |
| `ACNT_NAME` | 계좌명 | String | 60 | Y | 계좌의 고객명 |
| `TRAD_DVSN_NAME` | 매매구분명 | String | 60 | Y | 매도/매수 등 구분값 |
| `ITEM_NAME` | 종목명 | String | 60 | Y | 주문 종목 명칭 |
| `ORD_TMD` | 주문시각 | String | 6 | Y | 주문 접수 시간 |
| `ORD_GNO_BRNO` | 주문채번지점번호  | String | 5 | Y | 계좌 개설 시 관리점으로 선택한 영업점의 고유번호 |
| `ORGN_ODNO` | 원주문번호 | String | 10 | Y | 정정 또는 취소 대상 주문의 일련번호 |
| `ODNO` | 주문번호  | String | 10 | Y | 접수한 주문(정정 또는 취소)의 일련번호 |

### 응답 예시

```json
{
  "ORD_PRCS_DVSN_CD": "주문처리 구분코드를 입력하세요.",
  "CANO": "종합계좌번호를 입력하세요.",
  "ACNT_PRDT_CD": "계좌상품코드를 입력하세요.",
  "RVSE_CNCL_DVSN_CD": "정정취소 구분코드를 입력하세요.",
  "ORGN_ODNO": "원주문번호를 입력하세요.",
  "ORD_QTY": "주문수량을 입력하세요.",
  "UNIT_PRICE": "주문가격1을 입력하세요.",
  "NMPR_TYPE_CD": "호가유형코드를 입력하세요.",
  "KRX_NMPR_CNDT_CD": "한국거래소호가조건코드를 입력하세요.",
  "RMN_QTY_YN": "잔여수량여부를 입력하세요.",
  "CTAC_TLNO": "연락전화번호를 입력하세요.",
  "FUOP_ITEM_DVSN_CD": "선물옵션종목쿠분코드를 입력하세요.",
  "ORD_DVSN_CD": "주문구분코드를 입력하세요."
}
```

