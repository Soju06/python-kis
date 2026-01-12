# 해외선물옵션 기간계좌손익 일별[해외선물-010]

> [해외선물옵션] 주문/계좌

해외선물옵션 기간계좌손익 일별 API입니다.

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `aab037bf-5ea2-4e25-99f1-c45d09f02a31` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/overseas-futureoption/v1/trading/inquire-period-ccld` |
| **Content-Type** | `application/json; charset=utf-8` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID** | `모의투자 미지원`, `OTFM3118R` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2022-10-07
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
| `tr_id` | 거래ID | String | 13 | Y | OTFM3118R |
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
| `INQR_TERM_FROM_DT` | 조회기간FROM일자 | String | 8 | Y |  |
| `INQR_TERM_TO_DT` | 조회기간TO일자 | String | 8 | Y |  |
| `CANO` | 종합계좌번호 | String | 8 | Y | 계좌번호 체계(8-2)의 앞 8자리 |
| `ACNT_PRDT_CD` | 계좌상품코드 | String | 2 | Y | 계좌번호 체계(8-2)의 뒤 2자리 |
| `CRCY_CD` | 통화코드 | String | 3 | Y | '%%% : 전체 TUS: TOT_USD  / TKR: TOT_KRW KRW: 한국  / USD: 미국 EUR: EUR   / HKD: 홍콩 CNY: 중국  / JPY: 일본' |
| `WHOL_TRSL_YN` | 전체환산여부 | String | 1 | Y | N |
| `FUOP_DVSN` | 선물옵션구분 | String | 2 | Y | 00:전체 / 01:선물 / 02:옵션 |
| `CTX_AREA_FK200` | 연속조회검색조건200 | String | 200 | Y |  |
| `CTX_AREA_NK200` | 연속조회키200 | String | 200 | Y |  |

### 요청 예시

```json
{
	"CANO":"80012345",
	"ACNT_PRDT_CD":"08",
	"INQR_TERM_FROM_DT":"20220901",
	"INQR_TERM_TO_DT":"20221117",
	"CRCY_CD":"%%%",
	"WHOL_TRSL_YN":"N",
	"FUOP_DVSN":"00",
	"CTX_AREA_FK100":"",
	"CTX_AREA_NK100":"",
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
| `output1` | 응답상세1 | Object |   | Y | Array |
| `cano` | 종합계좌번호 | String | 8 | Y |  |
| `acnt_prdt_cd` | 계좌상품코드 | String | 2 | N |  |
| `crcy_cd` | 통화코드 | String | 3 | Y |  |
| `fm_buy_qty` | FM매수수량 | String | 10 | Y |  |
| `fm_sll_qty` | FM매도수량 | String | 10 | Y |  |
| `fm_lqd_pfls_amt` | FM청산손익금액 | String | 20 | Y |  |
| `fm_fee` | FM수수료 | String | 20 | Y |  |
| `fm_net_pfls_amt` | FM순손익금액 | String | 20 | Y |  |
| `fm_ustl_buy_qty` | FM미결제매수수량 | String | 10 | Y |  |
| `fm_ustl_sll_qty` | FM미결제매도수량 | String | 10 | Y |  |
| `fm_ustl_evlu_pfls_amt` | FM미결제평가손익금액 | String | 20 | Y |  |
| `fm_ustl_evlu_pfls_amt2` | FM미결제평가손익금액2 | String | 20 | Y |  |
| `fm_ustl_evlu_pfls_icdc_amt` | FM미결제평가손익증감금액 | String | 20 | Y |  |
| `fm_ustl_agrm_amt` | FM미결제약정금액 | String | 20 | Y |  |
| `fm_opt_lqd_amt` | FM옵션청산금액 | String | 20 | Y |  |
| `output2` | 응답상세2 | Object |   | Y | Array |
| `cano` | 종합계좌번호 | String | 8 | Y |  |
| `acnt_prdt_cd` | 계좌상품코드 | String | 2 | Y |  |
| `ovrs_futr_fx_pdno` | 해외선물FX상품번호 | String | 32 | Y |  |
| `crcy_cd` | 통화코드 | String | 3 | Y |  |
| `fm_buy_qty` | FM매수수량 | String | 10 | Y |  |
| `fm_sll_qty` | FM매도수량 | String | 10 | Y |  |
| `fm_lqd_pfls_amt` | FM청산손익금액 | String | 20 | Y |  |
| `fm_fee` | FM수수료 | String | 20 | Y |  |
| `fm_net_pfls_amt` | FM순손익금액 | String | 20 | Y |  |
| `fm_ustl_buy_qty` | FM미결제매수수량 | String | 10 | Y |  |
| `fm_ustl_sll_qty` | FM미결제매도수량 | String | 10 | Y |  |
| `fm_ustl_evlu_pfls_amt` | FM미결제평가손익금액 | String | 20 | Y |  |
| `fm_ustl_evlu_pfls_amt2` | FM미결제평가손익금액2 | String | 20 | Y |  |
| `fm_ustl_evlu_pfls_icdc_amt` | FM미결제평가손익증감금액 | String | 20 | Y |  |
| `fm_ccld_avg_pric` | FM체결평균가격 | String | 20 | Y |  |
| `fm_ustl_agrm_amt` | FM미결제약정금액 | String | 20 | Y |  |
| `fm_opt_lqd_amt` | FM옵션청산금액 | String | 20 | Y |  |

### 응답 예시

```json
{
  "ctx_area_fk200": "                                                                                                                                                                                                        ",
  "ctx_area_nk200": "                                                                                                                                                                                                        ",
  "output1": [
    {
      "cano": "80012345",
      "acnt_prdt_cd": "08",
      "crcy_cd": "USD",
      "fm_buy_qty": "",
      "fm_sll_qty": "",
      "fm_lqd_pfls_amt": "0.00",
      "fm_fee": "0.00",
      "fm_net_pfls_amt": "129650.00",
      "fm_ustl_buy_qty": "5",
      "fm_ustl_sll_qty": "100",
      "fm_ustl_evlu_pfls_amt": "129650.00",
      "fm_ustl_evlu_pfls_amt2": "0.00",
      "fm_ustl_evlu_pfls_icdc_amt": "129650.00",
      "fm_ustl_agrm_amt": "13590493.75",
      "fm_opt_lqd_amt": "0.00"
    }
  ],
  "output2": [
    {
      "cano": "80012345",
      "acnt_prdt_cd": "08",
      "ovrs_futr_fx_pdno": "6AZ22",
      "crcy_cd": "USD",
      "fm_buy_qty": "",
      "fm_sll_qty": "",
      "fm_lqd_pfls_amt": "0.00",
      "fm_fee": "0.00",
      "fm_net_pfls_amt": "10850.00",
      "fm_ustl_buy_qty": "2",
      "fm_ustl_sll_qty": "",
      "fm_ustl_evlu_pfls_amt": "10850.00",
      "fm_ustl_evlu_pfls_amt2": "0.00",
      "fm_ustl_evlu_pfls_icdc_amt": "10850.00",
      "fm_ccld_avg_pric": "0.62950",
      "fm_ustl_agrm_amt": "125900.00",
      "fm_opt_lqd_amt": "0.00"
    },
    {
      "cano": "80012345",
      "acnt_prdt_cd": "08",
      "ovrs_futr_fx_pdno": "6BZ22",
      "crcy_cd": "USD",
      "fm_buy_qty": "",
      "fm_sll_qty": "",
      "fm_lqd_pfls_amt": "0.00",
      "fm_fee": "0.00",
      "fm_net_pfls_amt": "5656.25",
      "fm_ustl_buy_qty": "2",
      "fm_ustl_sll_qty": "",
      "fm_ustl_evlu_pfls_amt": "5656.25",
      "fm_ustl_evlu_pfls_amt2": "0.00",
      "fm_ustl_evlu_pfls_icdc_amt": "5656.25",
      "fm_ccld_avg_pric": "1.1898",
      "fm_ustl_agrm_amt": "148718.75",
      "fm_opt_lqd_amt": "0.00"
    },
    {
      "cano": "80012345",
      "acnt_prdt_cd": "08",
      "ovrs_futr_fx_pdno": "6JZ22",
      "crcy_cd": "USD",
      "fm_buy_qty": "",
      "fm_sll_qty": "",
      "fm_lqd_pfls_amt": "0.00",
      "fm_fee": "0.00",
      "fm_net_pfls_amt": "5706.25",
      "fm_ustl_buy_qty": "1",
      "fm_ustl_sll_qty": "",
      "fm_ustl_evlu_pfls_amt": "5706.25",
      "fm_ustl_evlu_pfls_amt2": "0.00",
      "fm_ustl_evlu_pfls_icdc_amt": "5706.25",
      "fm_ccld_avg_pric": "6925.0",
      "fm_ustl_agrm_amt": "86562.50",
      "fm_opt_lqd_amt": "0.00"
    },
    {
      "cano": "80012345",
      "acnt_prdt_cd": "08",
      "ovrs_futr_fx_pdno": "ZBZ22",
      "crcy_cd": "USD",
      "fm_buy_qty": "",
      "fm_sll_qty": "",
      "fm_lqd_pfls_amt": "0.00",
      "fm_fee": "0.00",
      "fm_net_pfls_amt": "107437.50",
      "fm_ustl_buy_qty": "",
      "fm_ustl_sll_qty": "100",
      "fm_ustl_evlu_pfls_amt": "107437.50",
      "fm_ustl_evlu_pfls_amt2": "0.00",
      "fm_ustl_evlu_pfls_icdc_amt": "107437.50",
      "fm_ccld_avg_pric": "132.293125",
      "fm_ustl_agrm_amt": "13229312.50",
      "fm_opt_lqd_amt": "0.00"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "KIOK0510",
  "msg1": "조회가 완료되었습니다                                                           "
}
```
