# 선물옵션기간약정수수료일별[v1_국내선물-017]

> [국내선물옵션] 주문/계좌

선물옵션기간약정수수료일별 API입니다.

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `2bb020d7-ae3f-4f65-88ac-e9f598544825` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-futureoption/v1/trading/inquire-daily-amount-fee` |
| **Content-Type** | `` |
| **요청 포맷** | `` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID** | `모의투자 미지원`, `CTFO6119R` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2023-09-22
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
| `tr_id` | 거래ID | String | 13 | Y | CTFO6119R |
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
| `INQR_STRT_DAY` | 조회시작일 | String | 8 | Y | 조회시작일(YYYYMMDD) |
| `INQR_END_DAY` | 조회종료일 | String | 8 | Y | 조회종료일(YYYYMMDD) |
| `CTX_AREA_FK200` | 연속조회검색조건200 | String | 200 | Y | 연속조회검색조건200 |
| `CTX_AREA_NK200` | 연속조회키200 | String | 200 | Y | 연속조회키200 |

### 요청 예시

```json
{
  "CANO": "12345678",
  "ACNT_PRDT_CD": "03",
  "INQR_STRT_DAY": "20230901",
  "INQR_END_DAY": "20230920",
  "CTX_AREA_FK200": "",
  "CTX_AREA_NK200": ""
}
```

## 응답 (Response)

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
| `output1` | 응답상세 | String |   | Y | array |
| `ord_dt` | 주문일자 | String | 8 | Y |  |
| `pdno` | 상품번호 | String | 12 | Y |  |
| `item_name` | 종목명 | String | 60 | Y |  |
| `sll_agrm_amt` | 매도약정금액 | String | 19 | Y |  |
| `sll_fee` | 매도수수료 | String | 19 | Y |  |
| `buy_agrm_amt` | 매수약정금액 | String | 19 | Y |  |
| `buy_fee` | 매수수수료 | String | 19 | Y |  |
| `tot_fee_smtl` | 총수수료합계 | String | 19 | Y |  |
| `trad_pfls` | 매매손익 | String | 19 | Y |  |
| `output2` | 응답상세2 | String |   | Y |  |
| `futr_agrm` | 선물약정 | String | 19 | Y |  |
| `futr_agrm_amt` | 선물약정금액 | String | 19 | Y |  |
| `futr_agrm_amt_smtl` | 선물약정금액합계 | String | 19 | Y |  |
| `futr_sll_fee_smtl` | 선물매도수수료합계 | String | 19 | Y |  |
| `futr_buy_fee_smtl` | 선물매수수수료합계 | String | 19 | Y |  |
| `futr_fee_smtl` | 선물수수료합계 | String | 19 | Y |  |
| `opt_agrm` | 옵션약정 | String | 19 | Y |  |
| `opt_agrm_amt` | 옵션약정금액 | String | 19 | Y |  |
| `opt_agrm_amt_smtl` | 옵션약정금액합계 | String | 19 | Y |  |
| `opt_sll_fee_smtl` | 옵션매도수수료합계 | String | 19 | Y |  |
| `opt_buy_fee_smtl` | 옵션매수수수료합계 | String | 19 | Y |  |
| `opt_fee_smtl` | 옵션수수료합계 | String | 19 | Y |  |
| `prdt_futr_agrm` | 상품선물약정 | String | 19 | Y |  |
| `prdt_fuop` | 상품선물옵션 | String | 19 | Y |  |
| `prdt_futr_evlu_amt` | 상품선물평가금액 | String | 8 | Y |  |
| `futr_fee` | 선물수수료 | String | 19 | Y |  |
| `opt_fee` | 옵션수수료 | String | 19 | Y |  |
| `fee` | 수수료 | String | 19 | Y |  |
| `sll_agrm_amt` | 매도약정금액 | String | 19 | Y |  |
| `buy_agrm_amt` | 매수약정금액 | String | 19 | Y |  |
| `agrm_amt_smtl` | 약정금액합계 | String | 19 | Y |  |
| `sll_fee` | 매도수수료 | String | 19 | Y |  |
| `buy_fee` | 매수수수료 | String | 19 | Y |  |
| `fee_smtl` | 수수료합계 | String | 19 | Y |  |
| `trad_pfls_smtl` | 매매손익합계 | String | 19 | Y |  |

### 응답 예시

```json
{
  "ctx_area_fk200": "12345678!^03!^20230901!^20230920                                                                                                                                                                        ",
  "ctx_area_nk200": " !^                                                                                                                                                                                                     ",
  "output1": [
    {
      "ord_dt": "20230901",
      "pdno": "KR4101T90003",
      "item_name": "F 202309",
      "sll_agrm_amt": "0",
      "sll_fee": "0",
      "buy_agrm_amt": "0",
      "buy_fee": "0",
      "tot_fee_smtl": "0",
      "trad_pfls": "0"
    },
    {
      "ord_dt": "20230904",
      "pdno": "KR4101T90003",
      "item_name": "F 202309",
      "sll_agrm_amt": "0",
      "sll_fee": "0",
      "buy_agrm_amt": "0",
      "buy_fee": "0",
      "tot_fee_smtl": "0",
      "trad_pfls": "0"
    },
    {
      "ord_dt": "20230905",
      "pdno": "KR4101T90003",
      "item_name": "F 202309",
      "sll_agrm_amt": "0",
      "sll_fee": "0",
      "buy_agrm_amt": "0",
      "buy_fee": "0",
      "tot_fee_smtl": "0",
      "trad_pfls": "0"
    },
    {
      "ord_dt": "20230906",
      "pdno": "KR4101T90003",
      "item_name": "F 202309",
      "sll_agrm_amt": "0",
      "sll_fee": "0",
      "buy_agrm_amt": "0",
      "buy_fee": "0",
      "tot_fee_smtl": "0",
      "trad_pfls": "0"
    },
    {
      "ord_dt": "20230907",
      "pdno": "KR4101T90003",
      "item_name": "F 202309",
      "sll_agrm_amt": "0",
      "sll_fee": "0",
      "buy_agrm_amt": "0",
      "buy_fee": "0",
      "tot_fee_smtl": "0",
      "trad_pfls": "0"
    },
    {
      "ord_dt": "20230908",
      "pdno": "KR4101T90003",
      "item_name": "F 202309",
      "sll_agrm_amt": "0",
      "sll_fee": "0",
      "buy_agrm_amt": "0",
      "buy_fee": "0",
      "tot_fee_smtl": "0",
      "trad_pfls": "0"
    },
    {
      "ord_dt": "20230911",
      "pdno": "KR4101T90003",
      "item_name": "F 202309",
      "sll_agrm_amt": "0",
      "sll_fee": "0",
      "buy_agrm_amt": "0",
      "buy_fee": "0",
      "tot_fee_smtl": "0",
      "trad_pfls": "0"
    },
    {
      "ord_dt": "20230914",
      "pdno": "KR4101T90003",
      "item_name": "F 202309",
      "sll_agrm_amt": "0",
      "sll_fee": "0",
      "buy_agrm_amt": "0",
      "buy_fee": "0",
      "tot_fee_smtl": "0",
      "trad_pfls": "0"
    },
    {
      "ord_dt": "20230920",
      "pdno": "KR4101TC0008",
      "item_name": "F 202312",
      "sll_agrm_amt": "0",
      "sll_fee": "0",
      "buy_agrm_amt": "419375000",
      "buy_fee": "41140",
      "tot_fee_smtl": "41140",
      "trad_pfls": "0"
    },
    {
      "ord_dt": "20230920",
      "pdno": "KR4201TA3409",
      "item_name": "C 202310 340.0",
      "sll_agrm_amt": "0",
      "sll_fee": "0",
      "buy_agrm_amt": "700000",
      "buy_fee": "2750",
      "tot_fee_smtl": "2750",
      "trad_pfls": "0"
    }
  ],
  "output2": {
    "futr_agrm": "0",
    "futr_agrm_amt": "419375000",
    "futr_agrm_amt_smtl": "419375000",
    "futr_sll_fee_smtl": "0",
    "futr_buy_fee_smtl": "41140",
    "futr_fee_smtl": "41140",
    "opt_agrm": "0",
    "opt_agrm_amt": "700000",
    "opt_agrm_amt_smtl": "700000",
    "opt_sll_fee_smtl": "0",
    "opt_buy_fee_smtl": "2750",
    "opt_fee_smtl": "2750",
    "prdt_futr_agrm": "0",
    "prdt_fuop": "0",
    "prdt_futr_evlu_amt": "0",
    "futr_fee": "0",
    "opt_fee": "0",
    "fee": "0",
    "sll_agrm_amt": "0",
    "buy_agrm_amt": "420075000",
    "agrm_amt_smtl": "420075000",
    "sll_fee": "0",
    "buy_fee": "43890",
    "fee_smtl": "43890",
    "trad_pfls_smtl": "0"
  },
  "rt_cd": "0",
  "msg_cd": "KIOK0460",
  "msg1": "조회 되었습니다. (마지막 자료)                                                  "
}
```
