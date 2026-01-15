# 해외주식 지정가주문번호조회  [해외주식-071]

> [해외주식] 주문/계좌

TWAP, VWAP 주문에 대한 주문번호를 조회하는 API


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `f737550b-909d-4b5d-ba03-568c8a06b5b1` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/overseas-stock/v1/trading/algo-ordno` |
| **Content-Type** | `application/json; charset=utf-8` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `미지원` |
| **TR ID (실전)** | `TTTS6058R` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2025-05-23
- **최종 수정일**: 2025-05-23

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token 일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials Gr... |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | Y | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | TTTS6058R |
| `tr_cont` | 연속거래여부 | String | 1 | N | 공백 : 초기 조회 N : 다음 데이터 조회 (output header의 tr_cont가 M일 경우) |
| `custtype` | 고객타입 | String | 1 | Y | B : 법인 P : 개인 |
| `seq_no` | 일련번호 | String | 3 | N | [법인 필수] 001 |
| `phone_number` | 핸드폰번호 | String | 12 | N | [법인 필수] 제휴사APP을 사용하는 경우 사용자(회원) 핸드폰번호 ex) 01011112222 (하이픈 등 구분값 제거) |
| `ip_addr` | IP주소 | String | 12 | N | [법인 필수] 사용자(회원)의 IP Address |
| `gt_uid` | Global UID | String | 32 | N | [법인 전용] 거래고유번호로 사용하므로 거래별로 UNIQUE해야 함 |

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `TRAD_DT` | 거래일자 | String | 8 | Y | YYYYMMDD |
| `CANO` | 계좌번호 | String | 8 | Y | 종합계좌번호 (8자리) |
| `ACNO_PRDT_CD` | 계좌상품코드 | String | 2 | Y | 계좌상품코드 (2자리) : 주식계좌는 01 |
| `CTX_AREA_NK200` | 연속조회키200 | String | 200 | N |  |
| `CTX_AREA_FK200` | 연속조회조건200 | String | 200 | N |  |

### 요청 예시

```json
CANO:12345678
ACNT_PRDT_CD:01
TRAD_DT:20250523
CTX_AREA_NK200:
CTX_AREA_FK200:
```

## 응답

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `tr_id` | 거래ID | String | 13 | Y |  |
| `tr_cont` | 연속거래여부 | String | 1 | N | F or M : 다음 데이터 있음 D or E : 마지막 데이터 |
| `gt_uid` | Global UID | String | 32 | N | [법인 전용] 거래고유번호로 사용하므로 거래별로 UNIQUE해야 함 |

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `output` | 응답상세 | Object |  | Y |  |
| `odno` | 주문번호 | String | 10 | Y |  |
| `trad_dvsn_name` | 매매구분명 | String | 60 | Y |  |
| `pdno` | 상품번호 | String | 12 | Y |  |
| `item_name` | 종목명 | String | 60 | Y |  |
| `ft_ord_qty` | FT주문수량 | String | 4 | Y |  |
| `ft_ord_unpr3` | FT주문단가 | String | 8 | Y |  |
| `splt_buy_attr_name` | 분할매수속성명 | String | 60 | Y |  |
| `ft_ccld_qty` | FT체결수량 | String | 4 | Y |  |
| `ord_gno_brno` | 주문채번지점번호 | String | 5 | N |  |
| `rt_cd` | 성공 실패 여부 | String | 1 | Y | 0 : 성공 0 이외의 값 : 실패 |
| `msg_cd` | 응답코드 | String | 8 | Y |  |
| `msg1` | 응답메세지 | String | 80 | Y |  |
| `ctx_area_fk200` | 연속조회검색조건200 | String | 200 | Y |  |
| `ctx_area_nk200` | 연속조회키200 | String | 200 | Y |  |

### 응답 예시

```json
{
  "ctx_area_nk200": "                                                                                                                                                                                                        ",
  "ctx_area_fk200": "20250523^12345678^01^                                                                                                                                                                                   ",
  "output": [],
  "rt_cd": "0",
  "msg_cd": "KIOK0560",
  "msg1": "조회할 내용이 없습니다                                                          "
}
```

