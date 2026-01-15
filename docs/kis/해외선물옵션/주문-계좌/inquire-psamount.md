# 해외선물옵션 주문가능조회 [v1_해외선물-006]

> [해외선물옵션] 주문/계좌

해외선물옵션 주문가능조회 API입니다.

해외선물옵션 주문가능조회 [v1_해외선물-006]

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `fbe60d47-02bd-4d48-8169-e0df9e74c57c` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/overseas-futureoption/v1/trading/inquire-psamount` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID** | `OTFM3304R`, `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2022-08-05
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
| `tr_id` | 거래ID | String | 13 | Y | OTFM3304R |
| `tr_cont` | 연속 거래 여부 | String | 1 | N | tr_cont를 이용한 다음조회 불가 API |
| `custtype` | 고객 타입 | String | 1 | Y | B : 법인 / P : 개인 |
| `seq_no` | 일련번호 | String | 2 | N | 법인 : "001" / default   개인: "" |
| `mac_address` | 맥주소 | String | 12 | N | 법인고객 혹은 개인고객의 Mac address 값 |
| `phone_number` | 핸드폰번호 | String | 12 | N | [법인 필수] 제휴사APP을 사용하는 경우 사용자(회원) 핸드폰번호  ex) 01011112222 (하이픈 등 구분값 제거) |
| `ip_addr` | 접속 단말 공인 IP | String | 12 | N | [법인 필수] 사용자(회원)의 IP Address |
| `gt_uid` | Global UID | String | 32 | N | [법인 전용] 거래고유번호로 사용하므로 거래별로 UNIQUE해야 함 |

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `CANO` | 종합계좌번호 | String | 8 | Y | 계좌번호 체계(8-2)의 앞 8자리 |
| `ACNT_PRDT_CD` | 계좌상품코드 | String | 2 | Y | 계좌번호 체계(8-2)의 뒤 2자리 |
| `OVRS_FUTR_FX_PDNO` | 해외선물FX상품번호 | String | 32 | Y |  |
| `SLL_BUY_DVSN_CD` | 매도매수구분코드 | String | 2 | Y | 01 : 매도 / 02 : 매수 |
| `FM_ORD_PRIC` | FM주문가격 | String | 20 | Y | N |
| `ECIS_RSVN_ORD_YN` | 행사예약주문여부 | String | 1 | Y | N |

### 요청 예시

```json
{
  "CANO": "80012345",
  "ACNT_PRDT_CD": "08",
  "OVRS_FUTR_FX_PDNO": "6AU22",
  "SLL_BUY_DVSN_CD": "02",
  "FM_ORD_PRIC": "",
  "ECIS_RSVN_ORD_YN": ""
}
```

## 응답 (Response)

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `tr_id` | 거래ID | String | 13 | Y | 요청한 tr_id |
| `tr_cont` | 연속 거래 여부 | String | 1 | N | tr_cont를 이용한 다음조회 불가 API |
| `gt_uid` | Global UID | String | 32 | N | [법인 전용] 거래고유번호로 사용하므로 거래별로 UNIQUE해야 함 |

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `rt_cd` | 성공 실패 여부 | String | 1 | Y |  |
| `msg_cd` | 응답코드 | String | 8 | Y |  |
| `msg1` | 응답메세지 | String | 80 | Y |  |
| `output` | 응답상세1 | String |  | N |  |
| `cano` | 종합계좌번호 | String | 8 | N |  |
| `acnt_prdt_cd` | 계좌상품코드 | String | 2 | N |  |
| `ovrs_futr_fx_pdno` | 해외선물FX상품번호 | String | 32 | N |  |
| `crcy_cd` | 통화코드 | String | 3 | N |  |
| `sll_buy_dvsn_cd` | 매도매수구분코드 | String | 2 | N |  |
| `fm_ustl_qty` | FM미결제수량 | String | 10 | N |  |
| `fm_lqd_psbl_qty` | FM청산가능수량 | String | 10 | N |  |
| `fm_new_ord_psbl_qty` | FM신규주문가능수량 | String | 10 | N |  |
| `fm_tot_ord_psbl_qty` | FM총주문가능수량 | String | 10 | N |  |
| `fm_mkpr_tot_ord_psbl_qty` | FM시장가총주문가능수량 | String | 10 | N |  |

### 응답 예시

```json
{
  "output": {
    "cano": "80012345",
    "acnt_prdt_cd": "08",
    "ovrs_futr_fx_pdno": "6AU22",
    "crcy_cd": "",
    "sll_buy_dvsn_cd": "02",
    "fm_ustl_qty": "0",
    "fm_lqd_psbl_qty": "0",
    "fm_new_ord_psbl_qty": "3717",
    "fm_tot_ord_psbl_qty": "3717",
    "fm_mkpr_tot_ord_psbl_qty": "3717"
  },
  "rt_cd": "0",
  "msg_cd": "KIOK0510",
  "msg1": "조회가 완료되었습니다                                                           "
}
```
