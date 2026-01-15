# 해외주식 지정가체결내역조회 [해외주식-070]

> [해외주식] 주문/계좌

해외주식 TWAP, VWAP 주문에 대한 체결내역 조회 API로 지정가 주문번호조회 API를 수행 후 조회해야합니다


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `1187c231-1de6-4947-b942-bfca6b3d27e7` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/overseas-stock/v1/trading/inquire-algo-ccnl` |
| **Content-Type** | `application/json; charset=UTF-8` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `미지원` |
| **TR ID (실전)** | `TTTS6059R` |
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
| `content-type` | 컨텐츠타입 | String | 40 | N | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token 일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials Gr... |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appsecret (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | TTS6059R |
| `tr_cont` | 연속거래여부 | String | 1 | N | 공백 : 초기 조회 N : 다음 데이터 조회 (output header의 tr_cont가 M일 경우) |
| `custtype` | 고객타입 | String | 1 | Y | P : 개인 / B : 법인 |
| `seq_no` | 일련번호 | String | 3 | N | 법인 필수 : 001 |
| `phone_number` | 핸드폰번호 | String | 12 | N | [법인 필수] 제휴사APP을 사용하는 경우 사용자(회원) 핸드폰번호 ex) 01011112222 (하이픈 등 구분값 제거) |
| `ip_addr` | IP주소 | String | 12 | N | [법인 필수] 사용자(회원)의 IP Address |
| `gt_uid` | Global UID | String | 32 | N | [법인 전용] 거래고유번호로 사용하므로 거래별로 UNIQUE해야 함 |

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `CANO` | 계좌번호 | String | 8 | Y | 종합계좌번호 8자리 |
| `ACNT_PRDT_CD` | 계좌상품코드 | String | 2 | Y | 상품코드 2자리 (주식계좌 : 01) |
| `ORD_DT` | 주문일자 | String | 8 | Y | 주문일자 (YYYYMMDD) |
| `ORD_GNO_BRNO` | 주문채번지점번호 | String | 5 | N |  |
| `ODNO` | 주문번호 | String | 10 | Y | 지정가주문번호 (TTTC6058R)에서 조회된 주문번호 입력 |
| `TTLZ_ICLD_YN` | 집계포함여부 | String | 1 | N |  |
| `CTX_AREA_NK200` | 연속조회키200 | String | 200 | N | 연속조회 시 사용 |
| `CTX_AREA_FK200` | 연속조회조건200 | String | 200 | N | 연속조회 시 사용 |

### 요청 예시

```json
CANO:12345678
ACNT_PRDT_CD:01
ORD_DT:20250523
ORD_GNO_BRNO:
ODNO:0031112345
TTLZ_ICLD_YN:
CTX_AREA_NK200:
CTX_AREA_FK200:
```

## 응답

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `tr_id` | 거래ID | String | 13 | Y | 거래ID |
| `tr_cont` | 연속거래여부 | String | 1 | N | F or M : 다음 데이터 있음 D or E : 마지막 데이터 |
| `gt_uid` | Global UID | String | 32 | N | [법인 전용] 거래고유번호로 사용하므로 거래별로 UNIQUE해야 함 |

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `rt_cd` | 성공 실패여부 | String | 1 | Y |  |
| `msg_cd` | 응답코드 | String | 8 | Y |  |
| `msg1` | 응답메시지 | String | 80 | Y |  |
| `output` | 응답상세 | Object |  | Y |  |
| `CCLD_SEQ` | 체결순번 | String | 4 | Y |  |
| `CCLD_BTWN` | 체결시간 | String | 6 | Y | HHMMSS |
| `PDNO` | 상품번호 | String | 12 | Y |  |
| `ITEM_NAME` | 종목명 | String | 60 | Y |  |
| `FT_CCLD_QTY` | FT체결수량 | String | 4 | N |  |
| `FT_CCLD_UNPR3` | FT체결단가 | String | 8 | Y |  |
| `FT_CCLD_AMT3` | FT체결금액 | String | 8 | N |  |
| `output3` | 응답상세3 | Object |  | Y |  |
| `ODNO` | 주문번호 | String | 10 | Y |  |
| `TRAD_DVSN_NAME` | 매매구분명 | String | 60 | Y |  |
| `PDNO` | 상품번호 | String | 12 | Y |  |
| `ITEM_NAME` | 종목명 | String | 60 | Y |  |
| `FT_ORD_QTY` | FT주문수량 | String | 4 | Y |  |
| `FT_ORD_UNPR3` | FT주문단가 | String | 8 | Y |  |
| `ORD_TMD` | 주문시각 | String | 6 | Y |  |
| `SPLT_BUY_ATTR_NAME` | 분할매수속성명 | String | 60 | Y |  |
| `FT_CCLD_QTY` | FT체결수량 | String | 4 | Y |  |
| `TR_CRCY` | 거래통화 | String | 3 | Y |  |
| `FT_CCLD_UNPR3` | FT체결단가 | String | 8 | Y |  |
| `FT_CCLD_AMT3` | FT체결금액 | String | 8 | Y |  |
| `CCLD_CNT` | 체결건수 | String | 4 | Y |  |

### 응답 예시

```json
{
  "ctx_area_nk200": "                                                                                                                                                                                                        ",
  "ctx_area_fk200": "20250523^^0031112345^                                                                                                                                                                                   ",
  "output1": [],
  "output2": {
    "odno": "0031112345",
    "trad_dvsn_name": "TWAP지정가매수",
    "pdno": "AAPL",
    "item_name": "애플",
    "ft_ord_qty": "10",
    "ft_ord_unpr3": "10.00000000",
    "ord_tmd": "173904",
    "splt_buy_attr_name": "00:00~04:00",
    "ft_ccld_qty": "0",
    "tr_crcy": "",
    "ft_ccld_unpr3": "0.00000000",
    "ft_ccld_amt3": "0.00000",
    "ccld_cnt": "0"
  },
  "rt_cd": "0",
  "msg_cd": "KIOK0560",
  "msg1": "조회할 내용이 없습니다                                                          "
}
```

