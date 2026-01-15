# 퇴직연금 매수가능조회[v1_국내주식-034]

> [국내주식] 주문/계좌

​※ 55번 계좌(DC가입자계좌)의 경우 해당 API 이용이 불가합니다.
KIS Developers API의 경우 HTS ID에 반드시 연결되어있어야만 API 신청 및 앱정보 발급이 가능한 서비스로 개발되어서 실물계좌가 아닌 55번 계좌는 API 이용이 불가능한 점 양해 부탁드립니다.


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `64e81099-cb25-4f86-86d9-b53e6ed7d1a8` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/trading/pension/inquire-psbl-order` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `TTTC0503R` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2022-10-28
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
| `tr_id` | 거래ID | String | 13 | Y | TTTC0503R |
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
| `CANO` | 종합계좌번호 | String | 8 | Y |  |
| `ACNT_PRDT_CD` | 계좌상품코드 | String | 2 | Y | 29 |
| `PDNO` | 상품번호 | String | 12 | Y |  |
| `ACCA_DVSN_CD` | 적립금구분코드 | String | 2 | Y | 00 |
| `CMA_EVLU_AMT_ICLD_YN` | CMA평가금액포함여부 | String | 1 | Y |  |
| `ORD_DVSN` | 주문구분 | String | 2 | Y | 00 : 지정가 / 01 : 시장가 |
| `ORD_UNPR` | 주문단가 | String | 19 | Y |  |

### 요청 예시

```json
{
  "CANO": "63512345",
  "ACNT_PRDT_CD": "29",
  "PDNO": "029513",
  "ORD_UNPR": "55000",
  "ORD_DVSN": "00",
  "CMA_EVLU_AMT_ICLD_YN": "N",
  "ACCA_DVSN_CD": "00"
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
| `rt_cd` | 성공 실패 여부 | String | 1 | Y |  |
| `msg_cd` | 응답코드 | String | 8 | Y |  |
| `msg1` | 응답메세지 | String | 80 | Y |  |
| `output` | 응답상세1 | String |   | Y |  |
| `ord_psbl_cash` | 주문가능현금 | String | 19 | Y |  |
| `ruse_psbl_amt` | 재사용가능금액 | String | 19 | Y |  |
| `psbl_qty_calc_unpr` | 가능수량계산단가 | String | 19 | Y |  |
| `max_buy_amt` | 최대매수금액 | String | 19 | Y |  |
| `max_buy_qty` | 최대매수수량 | String | 10 | Y |  |

### 응답 예시

```json
{
  "output": {
    "ord_psbl_cash": "11054042",
    "ruse_psbl_amt": "0",
    "psbl_qty_calc_unpr": "55000",
    "max_buy_amt": "11054042",
    "max_buy_qty": "200"
  },
  "rt_cd": "0",
  "msg_cd": "KIOK0510",
  "msg1": "조회가 완료되었습니다                                                           "
}
```

