# 기간별손익일별합산조회[v1_국내주식-052]

> [국내주식] 주문/계좌

기간별손익일별합산조회 API입니다.
한국투자 HTS(eFriend Plus) > [0856] 기간별 매매손익 화면 에서 "일별" 클릭 시의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `9748985e-43bc-4b8f-be73-cd9434666099` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/trading/inquire-period-profit` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `TTTC8708R` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-02-16
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
| `tr_id` | 거래ID | String | 13 | Y | TTTC8708R |
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
| `ACNT_PRDT_CD` | 계좌상품코드 | String | 2 | Y |  |
| `CANO` | 종합계좌번호 | String | 8 | Y |  |
| `INQR_STRT_DT` | 조회시작일자 | String | 8 | Y |  |
| `PDNO` | 상품번호 | String | 12 | Y | ""공란입력 시, 전체 |
| `CTX_AREA_NK100` | 연속조회키100 | String | 100 | Y |  |
| `INQR_END_DT` | 조회종료일자 | String | 8 | Y |  |
| `SORT_DVSN` | 정렬구분 | String | 2 | Y | 00: 최근 순, 01: 과거 순, 02: 최근 순 |
| `INQR_DVSN` | 조회구분 | String | 2 | Y | 00 입력 |
| `CBLC_DVSN` | 잔고구분 | String | 2 | Y | 00: 전체 |
| `CTX_AREA_FK100` | 연속조회검색조건100 | String | 100 | Y |  |

### 요청 예시

```json
{
  "CANO": "12345678",
  "ACNT_PRDT_CD": "01",
  "PDNO": "",
  "INQR_STRT_DT": "20230101",
  "INQR_END_DT": "20240220",
  "SORT_DVSN": "00",
  "INQR_DVSN": "00",
  "CBLC_DVSN": "00",
  "CTX_AREA_FK100": "",
  "CTX_AREA_NK100": ""
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
| `output1` | 응답상세 | Object |   | Y | array |
| `trad_dt` | 매매일자 | String | 8 | Y |  |
| `buy_amt` | 매수금액 | String | 19 | Y |  |
| `sll_amt` | 매도금액 | String | 19 | Y |  |
| `rlzt_pfls` | 실현손익 | String | 19 | Y |  |
| `fee` | 수수료 | String | 19 | Y |  |
| `loan_int` | 대출이자 | String | 19 | Y |  |
| `tl_tax` | 제세금 | String | 19 | Y |  |
| `pfls_rt` | 손익률 | String | 238 | Y |  |
| `sll_qty1` | 매도수량1 | String | 19 | Y |  |
| `buy_qty1` | 매수수량1 | String | 9 | Y |  |
| `output2` | 응답상세2 | String |   | Y |  |
| `sll_qty_smtl` | 매도수량합계 | String | 19 | Y |  |
| `sll_tr_amt_smtl` | 매도거래금액합계 | String | 19 | Y |  |
| `sll_fee_smtl` | 매도수수료합계 | String | 19 | Y |  |
| `sll_tltx_smtl` | 매도제세금합계 | String | 19 | Y |  |
| `sll_excc_amt_smtl` | 매도정산금액합계 | String | 19 | Y |  |
| `buy_qty_smtl` | 매수수량합계 | String | 19 | Y |  |
| `buy_tr_amt_smtl` | 매수거래금액합계 | String | 19 | Y |  |
| `buy_fee_smtl` | 매수수수료합계 | String | 19 | Y |  |
| `buy_tax_smtl` | 매수제세금합계 | String | 19 | Y |  |
| `buy_excc_amt_smtl` | 매수정산금액합계 | String | 19 | Y |  |
| `tot_qty` | 총수량 | String | 10 | Y |  |
| `tot_tr_amt` | 총거래금액 | String | 19 | Y |  |
| `tot_fee` | 총수수료 | String | 19 | Y |  |
| `tot_tltx` | 총제세금 | String | 19 | Y |  |
| `tot_excc_amt` | 총정산금액 | String | 19 | Y |  |
| `tot_rlzt_pfls` | 총실현손익 | String | 19 | Y | ※ HTS[0856] 기간별 매매손익 '일별' 화면의 우측 하단 '총손익률' 항목은  기간별매매손익현황조회(TTTC8715R) > output2 > tot_pftrt(총수익률... |
| `loan_int` | 대출이자 | String | 19 | Y |  |

### 응답 예시

```json
{
  "ctx_area_fk100": "                                                                                                    ",
  "ctx_area_nk100": "                                                                                                    ",
  "output1": [
    {
      "trad_dt": "20240220",
      "buy_amt": "116697331",
      "sll_amt": "96455",
      "rlzt_pfls": "22991",
      "fee": "0",
      "loan_int": "0",
      "tl_tax": "0",
      "pfls_rt": "31.29560057",
      "sll_qty1": "8",
      "buy_qty1": "2003"
    }
  ],
  "output2": {
    "sll_qty_smtl": "8",
    "sll_tr_amt_smtl": "96455",
    "sll_fee_smtl": "0",
    "sll_tltx_smtl": "0",
    "sll_excc_amt_smtl": "96455",
    "buy_qty_smtl": "2003",
    "buy_tr_amt_smtl": "116697331",
    "buy_fee_smtl": "0",
    "buy_tax_smtl": "0",
    "buy_excc_amt_smtl": "116697331",
    "tot_qty": "2011",
    "tot_tr_amt": "116793786",
    "tot_fee": "0",
    "tot_tltx": "0",
    "tot_excc_amt": "116793786",
    "tot_rlzt_pfls": "22991",
    "loan_int": "0"
  },
  "rt_cd": "0",
  "msg_cd": "KIOK0510",
  "msg1": "조회가 완료되었습니다                                                           "
}
```

