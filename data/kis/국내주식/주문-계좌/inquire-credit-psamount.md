# 신용매수가능조회[v1_국내주식-042]

> [국내주식] 주문/계좌

신용매수가능조회 API입니다.
신용매수주문 시 주문가능수량과 금액을 확인하실 수 있습니다.


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `262e63bf-95bd-4540-b252-092d36df750a` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/trading/inquire-credit-psamount` |
| **Content-Type** | `application/json; charset=utf-8` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `TTTC8909R` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2023-02-24T12:36:30+09:00
- **최종 수정일**: 2025-04-30T10:10:15+09:00

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials Grant 절차를 준용)  법인(Access token 유효기간 3개월, Refresh token 유효기간 1년, OAuth 2.0의 Authorization Code Grant 절차를 준용) |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | TTTC8909R |
| `tr_cont` | 연속 거래 여부 | String | 1 | N | tr_cont를 이용한 다음조회 불가 API |
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
| `PDNO` | 상품번호 | String | 12 | Y | 종목코드(6자리) |
| `ORD_UNPR` | 주문단가 | String | 19 | Y | 1주당 가격  * 장전 시간외, 장후 시간외, 시장가의 경우 1주당 가격을 공란으로 비우지 않음 "0"으로 입력 권고 |
| `ORD_DVSN` | 주문구분 | String | 2 | Y | 00 : 지정가  01 : 시장가  02 : 조건부지정가  03 : 최유리지정가  04 : 최우선지정가  05 : 장전 시간외  06 : 장후 시간외  07 : 시간외 단일가  등 |
| `CRDT_TYPE` | 신용유형 | String | 2 | Y | 21 : 자기융자신규  23 : 유통융자신규  26 : 유통대주상환  28 : 자기대주상환  25 : 자기융자상환  27 : 유통융자상환  22 : 유통대주신규  24 : 자기대주신규 |
| `CMA_EVLU_AMT_ICLD_YN` | CMA평가금액포함여부 | String | 1 | Y | Y/N |
| `OVRS_ICLD_YN` | 해외포함여부 | String | 1 | Y | Y/N |

### 요청 예시

```json
{
  "CANO": "12345678",
  "ACNT_PRDT_CD": "01",
  "PDNO": "005930",
  "ORD_UNPR": "55000",
  "ORD_DVSN": "01",
  "CRDT_TYPE": "21",
  "CMA_EVLU_AMT_ICLD_YN": "N",
  "OVRS_ICLD_YN": "N"
}
```

## 응답

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
| `rt_cd` | 성공 실패 여부 | String | 1 | Y | 0 : 성공 0 이외의 값 : 실패 |
| `msg_cd` | 응답코드 | String | 8 | Y | 응답코드 |
| `msg1` | 응답메세지 | String | 80 | Y | 응답메시지 |
| `output` | 응답상세 | String |   | Y |  |
| `ord_psbl_cash` | 주문가능현금 | String | 19 | Y |  |
| `ord_psbl_sbst` | 주문가능대용 | String | 19 | Y |  |
| `ruse_psbl_amt` | 재사용가능금액 | String | 19 | Y |  |
| `fund_rpch_chgs` | 펀드환매대금 | String | 19 | Y |  |
| `psbl_qty_calc_unpr` | 가능수량계산단가 | String | 19 | Y |  |
| `nrcvb_buy_amt` | 미수없는매수금액 | String | 19 | Y |  |
| `nrcvb_buy_qty` | 미수없는매수수량 | String | 10 | Y |  |
| `max_buy_amt` | 최대매수금액 | String | 19 | Y |  |
| `max_buy_qty` | 최대매수수량 | String | 10 | Y |  |
| `cma_evlu_amt` | CMA평가금액 | String | 19 | Y |  |
| `ovrs_re_use_amt_wcrc` | 해외재사용금액원화 | String | 19 | Y |  |
| `ord_psbl_frcr_amt_wcrc` | 주문가능외화금액원화 | String | 19 | Y |  |

### 응답 예시

```json
{
  "output": {
    "ord_psbl_cash": "99965177664",
    "ord_psbl_sbst": "156772560",
    "ruse_psbl_amt": "0",
    "fund_rpch_chgs": "0",
    "psbl_qty_calc_unpr": "69200",
    "nrcvb_buy_amt": "0",
    "nrcvb_buy_qty": "0",
    "max_buy_amt": "0",
    "max_buy_qty": "0",
    "cma_evlu_amt": "0",
    "ovrs_re_use_amt_wcrc": "0",
    "ord_psbl_frcr_amt_wcrc": "157998704172856"
  },
  "rt_cd": "0",
  "msg_cd": "KIOK0510",
  "msg1": "조회가 완료되었습니다                                                           "
}
```

