# 종목별 투자자매매동향(일별)

> [국내주식] 시세분석

국내주식 종목별 투자자매매동향(일별) API입니다.
한국투자 HTS(eFriend Plus) > [0416] 종목별 일별동향 화면 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

※ 단위 : 금액(백만원) 수량(주)


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `141f0f11-ef30-4e52-9388-a6e78502d5c2` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/quotations/investor-trade-by-stock-daily` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `FHPTJ04160001` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2025-08-12
- **최종 수정일**: 2025-08-28

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 40 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials G... |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | FHPTJ04160001 |
| `tr_cont` | 연속 거래 여부 | String | 1 | N | 공백 : 초기 조회  N : 다음 데이터 조회 (output header의 tr_cont가 M일 경우) |
| `custtype` | 고객 타입 | String | 1 | Y | B : 법인  P : 개인 |
| `seq_no` | 일련번호 | String | 2 | N | [법인 필수] 001 |
| `mac_address` | 맥주소 | String | 12 | N | 법인고객 혹은 개인고객의 Mac address 값 |
| `phone_number` | 핸드폰번호 | String | 12 | N | [법인 필수] 제휴사APP을 사용하는 경우 사용자(회원) 핸드폰번호  ex) 01011112222 (하이픈 등 구분값 제거) |
| `ip_addr` | 접속 단말 공인 IP | String | 12 | N | [법인 필수] 사용자(회원)의 IP Address |
| `gt_uid` | Global UID | String | 32 | N | [법인 필수] 거래고유번호로 사용하므로 거래별로 UNIQUE해야 함 |

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `FID_COND_MRKT_DIV_CODE` | 조건 시장 분류 코드 | String | 2 | Y | J:KRX, NX:NXT, UN:통합 |
| `FID_INPUT_ISCD` | 입력 종목코드 | String | 12 | Y | 종목번호 (6자리) |
| `FID_INPUT_DATE_1` | 입력 날짜1 | String | 10 | Y | 입력 날짜(20250812) (해당일 조회는 장 종료 후 정상 조회 가능) |
| `FID_ORG_ADJ_PRC` | 수정주가 원주가 가격 | String | 2 | Y | 공란 입력 |
| `FID_ETC_CLS_CODE` | 기타 구분 코드 | String | 2 | Y | 공란 입력 |

### 요청 예시

```json
FID_COND_MRKT_DIV_CODE:J
FID_INPUT_ISCD:005930
FID_INPUT_DATE_1:20250811
FID_ORG_ADJ_PRC:
FID_ETC_CLS_CODE:
```

## 응답

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `tr_id` | 거래ID | String | 13 | Y | 요청한 tr_id |
| `tr_cont` | 연속 거래 여부 | String | 1 | N | 공백 : 초기 조회  N : 다음 데이터 조회 (output header의 tr_cont가 M일 경우) |
| `gt_uid` | Global UID | String | 32 | N | [법인 필수] 거래고유번호로 사용하므로 거래별로 UNIQUE해야 함 |

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `rt_cd` | 성공 실패 여부 | String | 1 | Y |  |
| `msg_cd` | 응답코드 | String | 8 | Y |  |
| `msg1` | 응답메세지 | String | 80 | Y |  |
| `output1` | 응답상세 | String |   | Y |  |
| `stck_prpr` | 주식 현재가 | String | 10 | Y |  |
| `prdy_vrss` | 전일 대비 | String | 10 | Y |  |
| `prdy_vrss_sign` | 전일 대비 부호 | String | 1 | Y |  |
| `prdy_ctrt` | 전일 대비율 | String | 82 | Y |  |
| `acml_vol` | 누적 거래량 | String | 18 | Y |  |
| `prdy_vol` | 전일 거래량 | String | 18 | Y |  |
| `rprs_mrkt_kor_name` | 대표 시장 한글 명 | String | 40 | Y |  |
| `output2` | 응답상세 | Object |   | Y | array |
| `stck_bsop_date` | 주식 영업 일자 | String | 8 | Y |  |
| `stck_clpr` | 주식 종가 | String | 10 | Y |  |
| `prdy_vrss` | 전일 대비 | String | 10 | Y |  |
| `prdy_vrss_sign` | 전일 대비 부호 | String | 1 | Y |  |
| `prdy_ctrt` | 전일 대비율 | String | 82 | Y |  |
| `acml_vol` | 누적 거래량 | String | 18 | Y | 단위 : 주 |
| `acml_tr_pbmn` | 누적 거래 대금 | String | 18 | Y | 단위 : 백만원 |
| `stck_oprc` | 주식 시가2 | String | 10 | Y |  |
| `stck_hgpr` | 주식 최고가 | String | 10 | Y |  |
| `stck_lwpr` | 주식 최저가 | String | 10 | Y |  |
| `frgn_ntby_qty` | 외국인 순매수 수량 | String | 12 | Y | 단위 : 주 |
| `frgn_reg_ntby_qty` | 외국인 등록 순매수 수량 | String | 18 | Y |  |
| `frgn_nreg_ntby_qty` | 외국인 비등록 순매수 수량 | String | 18 | Y |  |
| `prsn_ntby_qty` | 개인 순매수 수량 | String | 12 | Y |  |
| `orgn_ntby_qty` | 기관계 순매수 수량 | String | 18 | Y |  |
| `scrt_ntby_qty` | 증권 순매수 수량 | String | 12 | Y |  |
| `ivtr_ntby_qty` | 투자신탁 순매수 수량 | String | 12 | Y |  |
| `pe_fund_ntby_vol` | 사모 펀드 순매수 거래량 | String | 18 | Y |  |
| `bank_ntby_qty` | 은행 순매수 수량 | String | 12 | Y |  |
| `insu_ntby_qty` | 보험 순매수 수량 | String | 12 | Y |  |
| `mrbn_ntby_qty` | 종금 순매수 수량 | String | 12 | Y |  |
| `fund_ntby_qty` | 기금 순매수 수량 | String | 12 | Y |  |
| `etc_ntby_qty` | 기타 순매수 수량 | String | 12 | Y |  |
| `etc_corp_ntby_vol` | 기타 법인 순매수 거래량 | String | 18 | Y |  |
| `etc_orgt_ntby_vol` | 기타 단체 순매수 거래량 | String | 18 | Y |  |
| `frgn_reg_ntby_pbmn` | 외국인 등록 순매수 대금 | String | 18 | Y | 단위 : 백만원 |
| `frgn_ntby_tr_pbmn` | 외국인 순매수 거래 대금 | String | 18 | Y |  |
| `frgn_nreg_ntby_pbmn` | 외국인 비등록 순매수 대금 | String | 18 | Y |  |
| `prsn_ntby_tr_pbmn` | 개인 순매수 거래 대금 | String | 18 | Y |  |
| `orgn_ntby_tr_pbmn` | 기관계 순매수 거래 대금 | String | 18 | Y |  |
| `scrt_ntby_tr_pbmn` | 증권 순매수 거래 대금 | String | 18 | Y |  |
| `pe_fund_ntby_tr_pbmn` | 사모 펀드 순매수 거래 대금 | String | 18 | Y |  |
| `ivtr_ntby_tr_pbmn` | 투자신탁 순매수 거래 대금 | String | 18 | Y |  |
| `bank_ntby_tr_pbmn` | 은행 순매수 거래 대금 | String | 18 | Y |  |
| `insu_ntby_tr_pbmn` | 보험 순매수 거래 대금 | String | 18 | Y |  |
| `mrbn_ntby_tr_pbmn` | 종금 순매수 거래 대금 | String | 18 | Y |  |
| `fund_ntby_tr_pbmn` | 기금 순매수 거래 대금 | String | 18 | Y |  |
| `etc_ntby_tr_pbmn` | 기타 순매수 거래 대금 | String | 18 | Y |  |
| `etc_corp_ntby_tr_pbmn` | 기타 법인 순매수 거래 대금 | String | 18 | Y |  |
| `etc_orgt_ntby_tr_pbmn` | 기타 단체 순매수 거래 대금 | String | 18 | Y |  |
| `frgn_seln_vol` | 외국인 매도 거래량 | String | 18 | Y |  |
| `frgn_shnu_vol` | 외국인 매수2 거래량 | String | 18 | Y |  |
| `frgn_seln_tr_pbmn` | 외국인 매도 거래 대금 | String | 18 | Y |  |
| `frgn_shnu_tr_pbmn` | 외국인 매수2 거래 대금 | String | 18 | Y |  |
| `frgn_reg_askp_qty` | 외국인 등록 매도 수량 | String | 18 | Y |  |
| `frgn_reg_bidp_qty` | 외국인 등록 매수 수량 | String | 18 | Y |  |
| `frgn_reg_askp_pbmn` | 외국인 등록 매도 대금 | String | 18 | Y |  |
| `frgn_reg_bidp_pbmn` | 외국인 등록 매수 대금 | String | 18 | Y |  |
| `frgn_nreg_askp_qty` | 외국인 비등록 매도 수량 | String | 18 | Y |  |
| `frgn_nreg_bidp_qty` | 외국인 비등록 매수 수량 | String | 18 | Y |  |
| `frgn_nreg_askp_pbmn` | 외국인 비등록 매도 대금 | String | 18 | Y |  |
| `frgn_nreg_bidp_pbmn` | 외국인 비등록 매수 대금 | String | 18 | Y |  |
| `prsn_seln_vol` | 개인 매도 거래량 | String | 18 | Y |  |
| `prsn_shnu_vol` | 개인 매수2 거래량 | String | 18 | Y |  |
| `prsn_seln_tr_pbmn` | 개인 매도 거래 대금 | String | 18 | Y |  |
| `prsn_shnu_tr_pbmn` | 개인 매수2 거래 대금 | String | 18 | Y |  |
| `orgn_seln_vol` | 기관계 매도 거래량 | String | 18 | Y |  |
| `orgn_shnu_vol` | 기관계 매수2 거래량 | String | 18 | Y |  |
| `orgn_seln_tr_pbmn` | 기관계 매도 거래 대금 | String | 18 | Y |  |
| `orgn_shnu_tr_pbmn` | 기관계 매수2 거래 대금 | String | 18 | Y |  |
| `scrt_seln_vol` | 증권 매도 거래량 | String | 18 | Y |  |
| `scrt_shnu_vol` | 증권 매수2 거래량 | String | 18 | Y |  |
| `scrt_seln_tr_pbmn` | 증권 매도 거래 대금 | String | 18 | Y |  |
| `scrt_shnu_tr_pbmn` | 증권 매수2 거래 대금 | String | 18 | Y |  |
| `ivtr_seln_vol` | 투자신탁 매도 거래량 | String | 18 | Y |  |
| `ivtr_shnu_vol` | 투자신탁 매수2 거래량 | String | 18 | Y |  |
| `ivtr_seln_tr_pbmn` | 투자신탁 매도 거래 대금 | String | 18 | Y |  |
| `ivtr_shnu_tr_pbmn` | 투자신탁 매수2 거래 대금 | String | 18 | Y |  |
| `pe_fund_seln_tr_pbmn` | 사모 펀드 매도 거래 대금 | String | 18 | Y |  |
| `pe_fund_seln_vol` | 사모 펀드 매도 거래량 | String | 18 | Y |  |
| `pe_fund_shnu_tr_pbmn` | 사모 펀드 매수2 거래 대금 | String | 18 | Y |  |
| `pe_fund_shnu_vol` | 사모 펀드 매수2 거래량 | String | 18 | Y |  |
| `bank_seln_vol` | 은행 매도 거래량 | String | 18 | Y |  |
| `bank_shnu_vol` | 은행 매수2 거래량 | String | 18 | Y |  |
| `bank_seln_tr_pbmn` | 은행 매도 거래 대금 | String | 18 | Y |  |
| `bank_shnu_tr_pbmn` | 은행 매수2 거래 대금 | String | 18 | Y |  |
| `insu_seln_vol` | 보험 매도 거래량 | String | 18 | Y |  |
| `insu_shnu_vol` | 보험 매수2 거래량 | String | 18 | Y |  |
| `insu_seln_tr_pbmn` | 보험 매도 거래 대금 | String | 18 | Y |  |
| `insu_shnu_tr_pbmn` | 보험 매수2 거래 대금 | String | 18 | Y |  |
| `mrbn_seln_vol` | 종금 매도 거래량 | String | 18 | Y |  |
| `mrbn_shnu_vol` | 종금 매수2 거래량 | String | 18 | Y |  |
| `mrbn_seln_tr_pbmn` | 종금 매도 거래 대금 | String | 18 | Y |  |
| `mrbn_shnu_tr_pbmn` | 종금 매수2 거래 대금 | String | 18 | Y |  |
| `fund_seln_vol` | 기금 매도 거래량 | String | 18 | Y |  |
| `fund_shnu_vol` | 기금 매수2 거래량 | String | 18 | Y |  |
| `fund_seln_tr_pbmn` | 기금 매도 거래 대금 | String | 18 | Y |  |
| `fund_shnu_tr_pbmn` | 기금 매수2 거래 대금 | String | 18 | Y |  |
| `etc_seln_vol` | 기타 매도 거래량 | String | 18 | Y |  |
| `etc_shnu_vol` | 기타 매수2 거래량 | String | 18 | Y |  |
| `etc_seln_tr_pbmn` | 기타 매도 거래 대금 | String | 18 | Y |  |
| `etc_shnu_tr_pbmn` | 기타 매수2 거래 대금 | String | 18 | Y |  |
| `etc_orgt_seln_vol` | 기타 단체 매도 거래량 | String | 18 | Y |  |
| `etc_orgt_shnu_vol` | 기타 단체 매수2 거래량 | String | 18 | Y |  |
| `etc_orgt_seln_tr_pbmn` | 기타 단체 매도 거래 대금 | String | 18 | Y |  |
| `etc_orgt_shnu_tr_pbmn` | 기타 단체 매수2 거래 대금 | String | 18 | Y |  |
| `etc_corp_seln_vol` | 기타 법인 매도 거래량 | String | 18 | Y |  |
| `etc_corp_shnu_vol` | 기타 법인 매수2 거래량 | String | 18 | Y |  |
| `etc_corp_seln_tr_pbmn` | 기타 법인 매도 거래 대금 | String | 18 | Y |  |
| `etc_corp_shnu_tr_pbmn` | 기타 법인 매수2 거래 대금 | String | 18 | Y |  |
| `bold_yn` | BOLD 여부 | String | 18 | Y |  |

### 응답 예시

```json
{
    "output1": {
        "stck_prpr": "71100",
        "prdy_vrss": "100",
        "prdy_vrss_sign": "2",
        "prdy_ctrt": "0.14",
        "acml_vol": "15797656",
        "prdy_vol": "11354253",
        "rprs_mrkt_kor_name": "KOSPI200"
    },
    "output2": [
        {
            "stck_bsop_date": "20250811",
            "stck_clpr": "71000",
            "prdy_vrss": "-800",
            "prdy_vrss_sign": "5",
            "prdy_ctrt": "-1.11",
            "acml_vol": "11354253",
            "acml_tr_pbmn": "808470078650",
            "stck_oprc": "72000",
            "stck_hgpr": "72100",
            "stck_lwpr": "70800",
            "frgn_ntby_qty": "-2029800",
            "frgn_reg_ntby_qty": "-2031350",
            "frgn_nreg_ntby_qty": "1550",
            "prsn_ntby_qty": "1686273",
            "orgn_ntby_qty": "-571822",
            "scrt_ntby_qty": "-44264",
            "ivtr_ntby_qty": "-205974",
            "pe_fund_ntby_vol": "-125032",
            "bank_ntby_qty": "2930",
            "insu_ntby_qty": "-85309",
            "mrbn_ntby_qty": "-737",
            "fund_ntby_qty": "-113436",
            "etc_ntby_qty": "915349",
            "etc_corp_ntby_vol": "915349",
            "etc_orgt_ntby_vol": "0",
            "frgn_reg_ntby_pbmn": "-144473",
            "frgn_ntby_tr_pbmn": "-144363",
            "frgn_nreg_ntby_pbmn": "110",
            "prsn_ntby_tr_pbmn": "120110",
            "orgn_ntby_tr_pbmn": "-40903",
            "scrt_ntby_tr_pbmn": "-3169",
            "pe_fund_ntby_tr_pbmn": "-8887",
            "ivtr_ntby_tr_pbmn": "-14641",
            "bank_ntby_tr_pbmn": "209",
            "insu_ntby_tr_pbmn": "-6061",
            "mrbn_ntby_tr_pbmn": "-52",
            "fund_ntby_tr_pbmn": "-8301",
            "etc_ntby_tr_pbmn": "65156",
            "etc_corp_ntby_tr_pbmn": "65156",
            "etc_orgt_ntby_tr_pbmn": "0",
            "frgn_seln_vol": "4557311",
            "frgn_shnu_vol": "2527511",
            "frgn_seln_tr_pbmn": "324535",
            "frgn_shnu_tr_pbmn": "180172",
            "frgn_reg_askp_qty": "4550828",
            "frgn_reg_bidp_qty": "2519478",
            "frgn_reg_askp_pbmn": "324074",
            "frgn_reg_bidp_pbmn": "179600",
            "frgn_nreg_askp_qty": "6483",
            "frgn_nreg_bidp_qty": "8033",
            "frgn_nreg_askp_pbmn": "461",
            "frgn_nreg_bidp_pbmn": "572",
            "prsn_seln_vol": "2003849",
            "prsn_shnu_vol": "3690122",
            "prsn_seln_tr_pbmn": "142680",
            "prsn_shnu_tr_pbmn": "262790",
            "orgn_seln_vol": "4694042",
            "orgn_shnu_vol": "4122220",
            "orgn_seln_tr_pbmn": "334201",
            "orgn_shnu_tr_pbmn": "293298",
            "scrt_seln_vol": "444582",
            "scrt_shnu_vol": "400318",
            "scrt_seln_tr_pbmn": "31639",
            "scrt_shnu_tr_pbmn": "28470",
            "ivtr_seln_vol": "282816",
            "ivtr_shnu_vol": "76842",
            "ivtr_seln_tr_pbmn": "20111",
            "ivtr_shnu_tr_pbmn": "5470",
            "pe_fund_seln_tr_pbmn": "13670",
            "pe_fund_seln_vol": "192157",
            "pe_fund_shnu_tr_pbmn": "4783",
            "pe_fund_shnu_vol": "67125",
            "bank_seln_vol": "6",
            "bank_shnu_vol": "2936",
            "bank_seln_tr_pbmn": "0",
            "bank_shnu_tr_pbmn": "209",
            "insu_seln_vol": "108700",
            "insu_shnu_vol": "23391",
            "insu_seln_tr_pbmn": "7728",
            "insu_shnu_tr_pbmn": "1666",
            "mrbn_seln_vol": "760",
            "mrbn_shnu_vol": "23",
            "mrbn_seln_tr_pbmn": "54",
            "mrbn_shnu_tr_pbmn": "2",
            "fund_seln_vol": "3665021",
            "fund_shnu_vol": "3551585",
            "fund_seln_tr_pbmn": "261000",
            "fund_shnu_tr_pbmn": "252699",
            "etc_seln_vol": "99051",
            "etc_shnu_vol": "1014400",
            "etc_seln_tr_pbmn": "7054",
            "etc_shnu_tr_pbmn": "72209",
            "etc_orgt_seln_vol": "0",
            "etc_orgt_shnu_vol": "0",
            "etc_orgt_seln_tr_pbmn": "0",
            "etc_orgt_shnu_tr_pbmn": "0",
            "etc_corp_seln_vol": "99051",
            "etc_corp_shnu_vol": "1014400",
            "etc_corp_seln_tr_pbmn": "7054",
            "etc_corp_shnu_tr_pbmn": "72209",
            "bold_yn": "N"
        },...
    ],
    "rt_cd": "0",
    "msg_cd": "MCA00000",
    "msg1": "정상처리 되었습니다."
}
```

