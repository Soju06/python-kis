# (야간)선물옵션 주문체결 내역조회 [국내선물-009]

> [국내선물옵션] 주문/계좌

(야간)선물옵션 주문체결 내역조회 API입니다.

(야간)선물옵션 주문체결 내역조회 [국내선물-009]

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `b5f12325-af4e-4fcd-a8b2-c8047dd317d2` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-futureoption/v1/trading/inquire-ngt-ccnl` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `(구) JTCE5005R (신) STTN5201R` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2022-09-23T15:07:18+09:00
- **최종 수정일**: 2025-06-06T18:09:37+09:00

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials Grant 절차를 준용)  법인(Access token 유효기간 3개월, Refresh token 유효기간 1년, OAuth 2.0의 Authorization Code Grant 절차를 준용) |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | (구) JTCE5005R (신) STTN5201R |
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
| `STRT_ORD_DT` | 시작주문일자 | String | 8 | Y |  |
| `END_ORD_DT` | 종료주문일자 | String | 8 | Y | 조회하려는 마지막 일자 다음일자로 조회 (ex. 20221011 까지의 내역을 조회하고자 할 경우,  20221012로 종료주문일자 설정) |
| `SLL_BUY_DVSN_CD` | 매도매수구분코드 | String | 2 | Y | 공란 : default (00: 전체 ,01 : 매도, 02 : 매수) |
| `CCLD_NCCS_DVSN` | 체결미체결구분 | String | 2 | Y | 00 : 전체 01 : 체결 02 : 미체결 |
| `SORT_SQN` | 정렬순서 | String | 2 | Y | 공란 : default (DS : 정순, 그외 : 역순) |
| `STRT_ODNO` | 시작주문번호 | String | 10 | Y | 공란 : default |
| `PDNO` | 상품번호 | String | 12 | Y | 공란 : default |
| `MKET_ID_CD` | 시장ID코드 | String | 3 | Y | 공란 : default |
| `FUOP_DVSN_CD` | 선물옵션구분코드 | String | 2 | Y | 공란 : 전체, 01 : 선물, 02 : 옵션 |
| `SCRN_DVSN` | 화면구분 | String | 2 | Y | 02(Default) |
| `CTX_AREA_FK200` | 연속조회검색조건200 | String | 200 | Y | 공란 : 최초 조회시 이전 조회 Output CTX_AREA_FK200값 : 다음페이지 조회시(2번째부터) |
| `CTX_AREA_NK200` | 연속조회키200 | String | 200 | Y | 공란 : 최초 조회시 이전 조회 Output CTX_AREA_NK200값 : 다음페이지 조회시(2번째부터) |

### 요청 예시

```json
{
  "CANO": "80012345",
  "ACNT_PRDT_CD": "03",
  "STRT_ORD_DT": "20220730",
  "END_ORD_DT": "20221214",
  "SLL_BUY_DVSN_CD": "00",
  "CCLD_NCCS_DVSN": "00",
  "SORT_SQN": "DS",
  "STRT_ODNO": "",
  "PDNO": "",
  "MKET_ID_CD": "00",
  "FUOP_DVSN_CD": "",
  "SCRN_DVSN": "00",
  "CTX_AREA_FK200": "",
  "CTX_AREA_NK200": ""
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
| `output2` | 응답상세1 | String |   | Y |  |
| `tot_ord_qty` | 총주문수량 | String | 10 | Y |  |
| `tot_ccld_qty` | 총체결수량 | String | 10 | Y |  |
| `tot_ccld_qty_SMTL` | 총체결수량 | String | 19 | Y | 신규 TR 사용 필드 |
| `tot_ccld_amt` | 총체결금액 | String | 19 | Y |  |
| `tot_ccld_amt_SMTL` | 총체결금액 | String | 11 | Y | 신규 TR 사용 필드 |
| `fee` | 수수료 | String | 19 | Y |  |
| `ctac_tlno` | 연락전화번호 | String | 20 | Y | 신규 TR 사용 필드 |
| `output1` | 응답상세2 | Object |   | Y | 시간별체결 정보 |
| `ord_gno_brno` | 주문채번지점번호 | String | 5 | Y |  |
| `cano` | 종합계좌번호 | String | 8 | Y |  |
| `csac_name` | 종합계좌명 | String | 60 | Y |  |
| `acnt_prdt_cd` | 계좌상품코드 | String | 2 | Y |  |
| `ord_dt` | 주문일자 | String | 8 | Y |  |
| `odno` | 주문번호 | String | 10 | Y |  |
| `orgn_odno` | 원주문번호 | String | 10 | Y |  |
| `sll_buy_dvsn_cd` | 매도매수구분코드 | String | 2 | Y |  |
| `trad_dvsn_name` | 매매구분명 | String | 60 | Y |  |
| `nmpr_type_name` | 호가유형명 | String | 60 | Y |  |
| `pdno` | 상품번호 | String | 12 | Y |  |
| `prdt_name` | 상품명 | String | 60 | Y |  |
| `prdt_type_cd` | 상품유형코드 | String | 3 | Y |  |
| `ord_qty` | 주문수량 | String | 10 | Y |  |
| `ord_idx4` | 주문지수 | String | 20 | Y | 신규 TR 사용 필드 |
| `qty` | 잔량 | String | 10 | Y |  |
| `ord_tmd` | 주문시각 | String | 6 | Y |  |
| `tot_ccld_qty` | 총체결수량 | String | 10 | Y |  |
| `avg_idx` | 평균지수 | String | 19 | Y |  |
| `tot_ccld_amt` | 총체결금액 | String | 19 | Y |  |
| `rjct_qty` | 거부수량 | String | 10 | Y |  |
| `ingr_trad_rjct_rson_cd` | 장내매매거부사유코드 | String | 5 | Y |  |
| `ingr_trad_rjct_rson_name` | 장내매매거부사유명 | String | 60 | Y |  |
| `ord_stfno` | 주문직원번호 | String | 6 | Y |  |
| `sprd_item_yn` | 스프레드종목여부 | String | 1 | Y |  |
| `ord_ip_addr` | 주문IP주소 | String | 200 | Y |  |

### 응답 예시

```json
{
  "ctx_area_fk200": "81012345^03^20221214^20221214^DS^                                                                                                                                                                       ",
  "ctx_area_nk200": "                                                                                                                                                                                                        ",
  "output1": [],
  "output2": {
    "tot_ord_qty": "0",
    "tot_ccld_qty": "0",
    "tot_ccld_amt": "0",
    "fee": "0"
  },
  "rt_cd": "0",
  "msg_cd": "KIOK0560",
  "msg1": "조회할 내용이 없습니다                                                          "
}
```

