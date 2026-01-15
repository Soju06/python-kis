# 해외주식 일별거래내역 [해외주식-063]

> [해외주식] 주문/계좌

해외주식 일별거래내역 API입니다.
한국투자 HTS(eFriend Plus) > [0828] 해외증권 일별거래내역 화면 의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

※ 체결가격, 매매금액, 정산금액, 수수료 원화금액은 국내 결제일까지는 예상환율로 적용되고, 국내 결제일 익일부터 확정환율로 적용됨으로 금액이 변경될 수 있습니다.
※ 해외증권 투자 및 업무문의 안내: 한국투자증권 해외투자지원부 02)3276-5300

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `8e874fea-8e55-464d-b535-75df64fc3048` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/overseas-stock/v1/trading/inquire-period-trans` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID** | `모의투자 미지원`, `CTOS4001R` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-05-24
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
| `tr_id` | 거래ID | String | 13 | Y | CTOS4001R |
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
| `CANO` | 종합계좌번호 | String | 8 | Y |  |
| `ACNT_PRDT_CD` | 계좌상품코드 | String | 2 | Y |  |
| `ERLM_STRT_DT` | 등록시작일자 | String | 8 | Y | 입력날짜 ~ (ex) 20240420) |
| `ERLM_END_DT` | 등록종료일자 | String | 8 | Y | ~입력날짜 (ex) 20240520) |
| `OVRS_EXCG_CD` | 해외거래소코드 | String | 4 | Y | 공백 |
| `PDNO` | 상품번호 | String | 12 | Y | 공백 (전체조회), 개별종목 조회는 상품번호입력 |
| `SLL_BUY_DVSN_CD` | 매도매수구분코드 | String | 2 | Y | 00(전체), 01(매도), 02(매수) |
| `LOAN_DVSN_CD` | 대출구분코드 | String | 2 | Y | 공백 |
| `CTX_AREA_FK100` | 연속조회검색조건100 | String | 100 | Y | 공백 |
| `CTX_AREA_NK100` | 연속조회키100 | String | 100 | Y | 공백 |

### 요청 예시

```json
CANO:12345678
ACNT_PRDT_CD:01
ERLM_STRT_DT:20240101
ERLM_END_DT:20240528
OVRS_EXCG_CD:
PDNO:
SLL_BUY_DVSN_CD:00
LOAN_DVSN_CD:
CTX_AREA_FK100:
CTX_AREA_NK100:
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
| `ctx_area_fk100` | 연속조회검색조건100 | String | 100 | Y |  |
| `ctx_area_nk100` | 연속조회키100 | String | 100 | Y |  |
| `output1` | 응답상세 | Object |   | Y | array |
| `trad_dt` | 매매일자 | String | 8 | Y |  |
| `sttl_dt` | 결제일자 | String | 8 | Y |  |
| `sll_buy_dvsn_cd` | 매도매수구분코드 | String | 2 | Y |  |
| `sll_buy_dvsn_name` | 매도매수구분명 | String | 4 | Y |  |
| `pdno` | 상품번호 | String | 12 | Y |  |
| `ovrs_item_name` | 해외종목명 | String | 60 | Y |  |
| `ccld_qty` | 체결수량 | String | 10 | Y |  |
| `amt_unit_ccld_qty` | 금액단위체결수량 | String | 188 | Y |  |
| `ft_ccld_unpr2` | FT체결단가2 | String | 238 | Y |  |
| `ovrs_stck_ccld_unpr` | 해외주식체결단가 | String | 238 | Y |  |
| `tr_frcr_amt2` | 거래외화금액2 | String | 236 | Y |  |
| `tr_amt` | 거래금액 | String | 19 | Y |  |
| `frcr_excc_amt_1` | 외화정산금액1 | String | 236 | Y |  |
| `wcrc_excc_amt` | 원화정산금액 | String | 19 | Y |  |
| `dmst_frcr_fee1` | 국내외화수수료1 | String | 235 | Y |  |
| `frcr_fee1` | 외화수수료1 | String | 236 | Y |  |
| `dmst_wcrc_fee` | 국내원화수수료 | String | 19 | Y |  |
| `ovrs_wcrc_fee` | 해외원화수수료 | String | 19 | Y |  |
| `crcy_cd` | 통화코드 | String | 3 | Y |  |
| `std_pdno` | 표준상품번호 | String | 12 | Y |  |
| `erlm_exrt` | 등록환율 | String | 238 | Y |  |
| `loan_dvsn_cd` | 대출구분코드 | String | 2 | Y |  |
| `loan_dvsn_name` | 대출구분명 | String | 60 | Y |  |
| `output2` | 응답상세 | String |   | Y |  |
| `frcr_buy_amt_smtl` | 외화매수금액합계 | String | 236 | Y |  |
| `frcr_sll_amt_smtl` | 외화매도금액합계 | String | 236 | Y |  |
| `dmst_fee_smtl` | 국내수수료합계 | String | 256 | Y |  |
| `ovrs_fee_smtl` | 해외수수료합계 | String | 236 | Y |  |

### 응답 예시

```json
{
  "ctx_area_fk100": "12345678!^01!^20240101!^20240528!^!^                                                                ",
  "ctx_area_nk100": "                                                                                                    ",
  "output1": [
    {
      "trad_dt": "20240116",
      "sttl_dt": "20240118",
      "sll_buy_dvsn_cd": "01",
      "sll_buy_dvsn_name": "매도",
      "pdno": "AAPL",
      "ovrs_item_name": "애플",
      "ccld_qty": "1",
      "amt_unit_ccld_qty": "1.00000000",
      "ft_ccld_unpr2": "2.94000000",
      "ovrs_stck_ccld_unpr": "0.00000000",
      "tr_frcr_amt2": "2.940000",
      "tr_amt": "0",
      "frcr_excc_amt_1": "2.940000",
      "wcrc_excc_amt": "0",
      "dmst_frcr_fee1": "0.00000",
      "frcr_fee1": "0.000000",
      "dmst_wcrc_fee": "0",
      "ovrs_wcrc_fee": "0",
      "crcy_cd": "USD",
      "std_pdno": "US0378331005",
      "erlm_exrt": "0.00000000",
      "loan_dvsn_cd": "01",
      "loan_dvsn_name": "현금"
    },
    {
      "trad_dt": "20240116",
      "sttl_dt": "20240118",
      "sll_buy_dvsn_cd": "02",
      "sll_buy_dvsn_name": "매수",
      "pdno": "USAS",
      "ovrs_item_name": "아메리카스 골드 앤드 실버",
      "ccld_qty": "1",
      "amt_unit_ccld_qty": "1.00000000",
      "ft_ccld_unpr2": "0.62000000",
      "ovrs_stck_ccld_unpr": "0.00000000",
      "tr_frcr_amt2": "0.620000",
      "tr_amt": "0",
      "frcr_excc_amt_1": "0.620000",
      "wcrc_excc_amt": "0",
      "dmst_frcr_fee1": "0.00000",
      "frcr_fee1": "0.000000",
      "dmst_wcrc_fee": "0",
      "ovrs_wcrc_fee": "0",
      "crcy_cd": "USD",
      "std_pdno": "CA03062D1006",
      "erlm_exrt": "0.00000000",
      "loan_dvsn_cd": "01",
      "loan_dvsn_name": "현금"
    },
    {
      "trad_dt": "20240118",
      "sttl_dt": "20240122",
      "sll_buy_dvsn_cd": "02",
      "sll_buy_dvsn_name": "매수",
      "pdno": "TSLA",
      "ovrs_item_name": "테슬라",
      "ccld_qty": "1",
      "amt_unit_ccld_qty": "1.00000000",
      "ft_ccld_unpr2": "12.20000000",
      "ovrs_stck_ccld_unpr": "16283.34000000",
      "tr_frcr_amt2": "12.200000",
      "tr_amt": "16283",
      "frcr_excc_amt_1": "12.200000",
      "wcrc_excc_amt": "16283",
      "dmst_frcr_fee1": "0.00000",
      "frcr_fee1": "0.000000",
      "dmst_wcrc_fee": "0",
      "ovrs_wcrc_fee": "0",
      "crcy_cd": "USD",
      "std_pdno": "US88160R1014",
      "erlm_exrt": "1334.70000000",
      "loan_dvsn_cd": "01",
      "loan_dvsn_name": "현금"
    },
    {
      "trad_dt": "20240118",
      "sttl_dt": "20240122",
      "sll_buy_dvsn_cd": "02",
      "sll_buy_dvsn_name": "매수",
      "pdno": "PG",
      "ovrs_item_name": "프록터 앤드 갬블",
      "ccld_qty": "5",
      "amt_unit_ccld_qty": "5.00000000",
      "ft_ccld_unpr2": "149.20000000",
      "ovrs_stck_ccld_unpr": "199137.24000000",
      "tr_frcr_amt2": "746.000000",
      "tr_amt": "995686",
      "frcr_excc_amt_1": "746.000000",
      "wcrc_excc_amt": "995686",
      "dmst_frcr_fee1": "0.00000",
      "frcr_fee1": "0.000000",
      "dmst_wcrc_fee": "0",
      "ovrs_wcrc_fee": "0",
      "crcy_cd": "USD",
      "std_pdno": "US7427181091",
      "erlm_exrt": "1334.70000000",
      "loan_dvsn_cd": "01",
      "loan_dvsn_name": "현금"
    },
    {
      "trad_dt": "20240118",
      "sttl_dt": "20240122",
      "sll_buy_dvsn_cd": "02",
      "sll_buy_dvsn_name": "매수",
      "pdno": "6758",
      "ovrs_item_name": "[6758]소니",
      "ccld_qty": "99",
      "amt_unit_ccld_qty": "99.00000000",
      "ft_ccld_unpr2": "14260.50000000",
      "ovrs_stck_ccld_unpr": "129281.41480000",
      "tr_frcr_amt2": "1411789.000000",
      "tr_amt": "12798855",
      "frcr_excc_amt_1": "1415742.000000",
      "wcrc_excc_amt": "12834691",
      "dmst_frcr_fee1": "2824.00000",
      "frcr_fee1": "1129.000000",
      "dmst_wcrc_fee": "25601",
      "ovrs_wcrc_fee": "10235",
      "crcy_cd": "JPY",
      "std_pdno": "JP3435000009",
      "erlm_exrt": "9.06570000",
      "loan_dvsn_cd": "01",
      "loan_dvsn_name": "현금"
    }
  ],
  "output2": {
    "frcr_buy_amt_smtl": "13810824.000000",
    "frcr_sll_amt_smtl": "0.000000",
    "dmst_fee_smtl": "25601.000000",
    "ovrs_fee_smtl": "10235.000000"
  },
  "rt_cd": "0",
  "msg_cd": "KIOK0460",
  "msg1": "조회 되었습니다. (마지막 자료)                                                  "
}
```
