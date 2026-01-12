# 선물옵션 주문[v1_국내선물-001]

> [국내선물옵션] 주문/계좌

​선물옵션 주문 API입니다.
* 선물옵션 운영시간 외 API 호출 시 애러가 발생하오니 운영시간을 확인해주세요.

※ POST API의 경우 BODY값의 key값들을 대문자로 작성하셔야 합니다.
   (EX. "CANO" : "12345678", "ACNT_PRDT_CD": "01",...)

※ 종목코드 마스터파일 파이썬 정제코드는 한국투자증권 Github 참고 부탁드립니다.
   https://github.com/koreainvestment/open-trading-api/tree/main/stocks_info

[국내선물-001 v1] 선물옵션주문

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `73a1bb73-fd91-4d70-bba1-f3241f12e7ff` |
| **HTTP Method** | `POST` |
| **URL** | `/uapi/domestic-futureoption/v1/trading/order` |
| **Content-Type** | `application/json; charset=UTF-8` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `https://openapivts.koreainvestment.com:29443` |
| **TR ID** | `(주간 매수/매도) TTTO1101U (야간 매수/매도) (구) JTCE1001U (신) STTN1101U`, `(주간 매수/매도) VTTO1101U (야간은 모의투자 미제공)` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2021-12-15
- **최종 수정일**: 2025-06-23

## 요청 (Request)

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | N | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials G... |
| `appkey` | 앱키  | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appsecret (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | [실전투자] TTTO1101U : 선물 옵션 매수 매도 주문 주간 (구) JTCE1001U : 선물 옵션 매수 매도 주문 야간 (신) STTN1101U : 선물 옵션 매수 매... |
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
| `SLL_BUY_DVSN_CD` | 매도매수구분코드 | String | 2 | Y | 01 : 매도 02 : 매수 |
| `SHTN_PDNO` | 단축상품번호 | String | 12 | Y | 종목번호 선물 6자리 (예: 101S03) 옵션 9자리 (예: 201S03370) |
| `ORD_QTY` | 주문수량 | String | 10 | Y |  |
| `UNIT_PRICE` | 주문가격1 | String | 23 | Y | 시장가나 최유리 지정가인 경우 0으로 입력 |
| `NMPR_TYPE_CD` | 호가유형코드 | String | 2 | N | ※ ORD_DVSN_CD(주문구분코드)를 입력한 경우 ""(공란)으로 입력해도 됨 01 : 지정가 02 : 시장가  03 : 조건부 04 : 최유리 |
| `KRX_NMPR_CNDT_CD` | 한국거래소호가조건코드 | String | 1 | N | ※ ORD_DVSN_CD(주문구분코드)를 입력한 경우 ""(공란)으로 입력해도 됨 0 : 없음 3 : IOC 4 : FOK |
| `CTAC_TLNO` | 연락전화번호 | String | 20 | N | 고객의 연락 가능한 전화번호 |
| `FUOP_ITEM_DVSN_CD` | 선물옵션종목구분코드 | String | 2 | N | 공란(Default) |
| `ORD_DVSN_CD` | 주문구분코드 | String | 2 | Y | 01 : 지정가 02 : 시장가 03 : 조건부 04 : 최유리, 10 : 지정가(IOC) 11 : 지정가(FOK) 12 : 시장가(IOC) 13 : 시장가(FOK) 14 :... |

### 요청 예시

```json
{
  "ORD_PRCS_DVSN_CD": "02",
  "CANO": "810XXXXX",
  "ACNT_PRDT_CD": "03",
  "SLL_BUY_DVSN_CD": "02",
  "SHTN_PDNO": "167R12",
  "ORD_QTY": "1",
  "UNIT_PRICE": "123",
  "NMPR_TYPE_CD": "",
  "KRX_NMPR_CNDT_CD": "",
  "CTAC_TLNO": "",
  "FUOP_ITEM_DVSN_CD": "",
  "ORD_DVSN_CD": "01"
}
```

## 응답 (Response)

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
| `ORD_GNO_BRNO` | 주문채번지점번호 | String | 5 | Y | 계좌 개설 시 관리점으로 선택한 영업점의 고유번호 |
| `ODNO` | 주문번호 | String | 10 | Y | 접수한 주문의 일련번호 |

### 응답 예시

```json
{
  "rt_cd": "0",
  "msg_cd": "APBK0029",
  "msg1": "주문전송이 정상적으로 처리되었습니다.",
  "output": {
    "ACNT_NAME": "류민수",
    "TRAD_DVSN_NAME": "매도",
    "ITEM_NAME": "코스피200 F 202203",
    "ORD_TMD": "131604",
    "ORD_GNO_BRNO": "06010",
    "ODNO": "0000007045"
  }
}
```
