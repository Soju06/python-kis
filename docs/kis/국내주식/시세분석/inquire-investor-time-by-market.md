# 시장별 투자자매매동향(시세)[v1_국내주식-074]

> [국내주식] 시세분석

시장별 투자자매매동향(시세성) API입니다.
한국투자 HTS(eFriend Plus) > [0403] 시장별 시간동향 의 상단 표 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `e5c6c050-e63f-4ab7-b339-d1a645d3239b` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/quotations/inquire-investor-time-by-market` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `FHPTJ04030000` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-02-23
- **최종 수정일**: 2025-05-14

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials G... |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | FHPTJ04030000 |
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
| `fid_input_iscd` | 시장구분 | String | 12 | Y | 코스피: KSP, 코스닥:KSQ, 선물,콜옵션,풋옵션 : K2I, 주식선물:999, ETF: ETF, ELW:ELW, ETN: ETN,  미니: MKI, 위클리월 : WKM,... |
| `fid_input_iscd_2` | 업종구분 | String | 8 | Y | - fid_input_iscd: KSP(코스피) 혹은 KSQ(코스닥)인 경우 코스피(0001_종합, .…0027_제조업 ) 코스닥(1001_종합, …. 1041_IT부품) .... |

### 요청 예시

```json
{
  "FID_INPUT_ISCD": "KSP",
  "FID_INPUT_ISCD_2": "0001"
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
| `output` | 응답상세 | String |   | Y |  |
| `frgn_seln_vol` | 외국인 매도 거래량 | String | 18 | Y |  |
| `frgn_shnu_vol` | 외국인 매수2 거래량 | String | 18 | Y |  |
| `frgn_ntby_qty` | 외국인 순매수 수량 | String | 12 | Y |  |
| `frgn_seln_tr_pbmn` | 외국인 매도 거래 대금 | String | 18 | Y |  |
| `frgn_shnu_tr_pbmn` | 외국인 매수2 거래 대금 | String | 18 | Y |  |
| `frgn_ntby_tr_pbmn` | 외국인 순매수 거래 대금 | String | 18 | Y |  |
| `prsn_seln_vol` | 개인 매도 거래량 | String | 18 | Y |  |
| `prsn_shnu_vol` | 개인 매수2 거래량 | String | 18 | Y |  |
| `prsn_ntby_qty` | 개인 순매수 수량 | String | 12 | Y |  |
| `prsn_seln_tr_pbmn` | 개인 매도 거래 대금 | String | 18 | Y |  |
| `prsn_shnu_tr_pbmn` | 개인 매수2 거래 대금 | String | 18 | Y |  |
| `prsn_ntby_tr_pbmn` | 개인 순매수 거래 대금 | String | 18 | Y |  |
| `orgn_seln_vol` | 기관계 매도 거래량 | String | 18 | Y |  |
| `orgn_shnu_vol` | 기관계 매수2 거래량 | String | 18 | Y |  |
| `orgn_ntby_qty` | 기관계 순매수 수량 | String | 18 | Y |  |
| `orgn_seln_tr_pbmn` | 기관계 매도 거래 대금 | String | 18 | Y |  |
| `orgn_shnu_tr_pbmn` | 기관계 매수2 거래 대금 | String | 18 | Y |  |
| `orgn_ntby_tr_pbmn` | 기관계 순매수 거래 대금 | String | 18 | Y |  |
| `scrt_seln_vol` | 증권 매도 거래량 | String | 18 | Y |  |
| `scrt_shnu_vol` | 증권 매수2 거래량 | String | 18 | Y |  |
| `scrt_ntby_qty` | 증권 순매수 수량 | String | 12 | Y |  |
| `scrt_seln_tr_pbmn` | 증권 매도 거래 대금 | String | 18 | Y |  |
| `scrt_shnu_tr_pbmn` | 증권 매수2 거래 대금 | String | 18 | Y |  |
| `scrt_ntby_tr_pbmn` | 증권 순매수 거래 대금 | String | 18 | Y |  |
| `ivtr_seln_vol` | 투자신탁 매도 거래량 | String | 18 | Y |  |
| `ivtr_shnu_vol` | 투자신탁 매수2 거래량 | String | 18 | Y |  |
| `ivtr_ntby_qty` | 투자신탁 순매수 수량 | String | 12 | Y |  |
| `ivtr_seln_tr_pbmn` | 투자신탁 매도 거래 대금 | String | 18 | Y |  |
| `ivtr_shnu_tr_pbmn` | 투자신탁 매수2 거래 대금 | String | 18 | Y |  |
| `ivtr_ntby_tr_pbmn` | 투자신탁 순매수 거래 대금 | String | 18 | Y |  |
| `pe_fund_seln_tr_pbmn` | 사모 펀드 매도 거래 대금 | String | 18 | Y |  |
| `pe_fund_seln_vol` | 사모 펀드 매도 거래량 | String | 18 | Y |  |
| `pe_fund_ntby_vol` | 사모 펀드 순매수 거래량 | String | 18 | Y |  |
| `pe_fund_shnu_tr_pbmn` | 사모 펀드 매수2 거래 대금 | String | 18 | Y |  |
| `pe_fund_shnu_vol` | 사모 펀드 매수2 거래량 | String | 18 | Y |  |
| `pe_fund_ntby_tr_pbmn` | 사모 펀드 순매수 거래 대금 | String | 18 | Y |  |
| `bank_seln_vol` | 은행 매도 거래량 | String | 18 | Y |  |
| `bank_shnu_vol` | 은행 매수2 거래량 | String | 18 | Y |  |
| `bank_ntby_qty` | 은행 순매수 수량 | String | 12 | Y |  |
| `bank_seln_tr_pbmn` | 은행 매도 거래 대금 | String | 18 | Y |  |
| `bank_shnu_tr_pbmn` | 은행 매수2 거래 대금 | String | 18 | Y |  |
| `bank_ntby_tr_pbmn` | 은행 순매수 거래 대금 | String | 18 | Y |  |
| `insu_seln_vol` | 보험 매도 거래량 | String | 18 | Y |  |
| `insu_shnu_vol` | 보험 매수2 거래량 | String | 18 | Y |  |
| `insu_ntby_qty` | 보험 순매수 수량 | String | 12 | Y |  |
| `insu_seln_tr_pbmn` | 보험 매도 거래 대금 | String | 18 | Y |  |
| `insu_shnu_tr_pbmn` | 보험 매수2 거래 대금 | String | 18 | Y |  |
| `insu_ntby_tr_pbmn` | 보험 순매수 거래 대금 | String | 18 | Y |  |
| `mrbn_seln_vol` | 종금 매도 거래량 | String | 18 | Y |  |
| `mrbn_shnu_vol` | 종금 매수2 거래량 | String | 18 | Y |  |
| `mrbn_ntby_qty` | 종금 순매수 수량 | String | 12 | Y |  |
| `mrbn_seln_tr_pbmn` | 종금 매도 거래 대금 | String | 18 | Y |  |
| `mrbn_shnu_tr_pbmn` | 종금 매수2 거래 대금 | String | 18 | Y |  |
| `mrbn_ntby_tr_pbmn` | 종금 순매수 거래 대금 | String | 18 | Y |  |
| `fund_seln_vol` | 기금 매도 거래량 | String | 18 | Y |  |
| `fund_shnu_vol` | 기금 매수2 거래량 | String | 18 | Y |  |
| `fund_ntby_qty` | 기금 순매수 수량 | String | 12 | Y |  |
| `fund_seln_tr_pbmn` | 기금 매도 거래 대금 | String | 18 | Y |  |
| `fund_shnu_tr_pbmn` | 기금 매수2 거래 대금 | String | 18 | Y |  |
| `fund_ntby_tr_pbmn` | 기금 순매수 거래 대금 | String | 18 | Y |  |
| `etc_orgt_seln_vol` | 기타 단체 매도 거래량 | String | 18 | Y |  |
| `etc_orgt_shnu_vol` | 기타 단체 매수2 거래량 | String | 18 | Y |  |
| `etc_orgt_ntby_vol` | 기타 단체 순매수 거래량 | String | 18 | Y |  |
| `etc_orgt_seln_tr_pbmn` | 기타 단체 매도 거래 대금 | String | 18 | Y |  |
| `etc_orgt_shnu_tr_pbmn` | 기타 단체 매수2 거래 대금 | String | 18 | Y |  |
| `etc_orgt_ntby_tr_pbmn` | 기타 단체 순매수 거래 대금 | String | 18 | Y |  |
| `etc_corp_seln_vol` | 기타 법인 매도 거래량 | String | 18 | Y |  |
| `etc_corp_shnu_vol` | 기타 법인 매수2 거래량 | String | 18 | Y |  |
| `etc_corp_ntby_vol` | 기타 법인 순매수 거래량 | String | 18 | Y |  |
| `etc_corp_seln_tr_pbmn` | 기타 법인 매도 거래 대금 | String | 18 | Y |  |
| `etc_corp_shnu_tr_pbmn` | 기타 법인 매수2 거래 대금 | String | 18 | Y |  |
| `etc_corp_ntby_tr_pbmn` | 기타 법인 순매수 거래 대금 | String | 18 | Y |  |

### 응답 예시

```json
{
  "output": [
    {
      "frgn_seln_vol": "75588",
      "frgn_shnu_vol": "70298",
      "frgn_ntby_qty": "-5290",
      "frgn_seln_tr_pbmn": "2818983",
      "frgn_shnu_tr_pbmn": "2967639",
      "frgn_ntby_tr_pbmn": "148656",
      "prsn_seln_vol": "294375",
      "prsn_shnu_vol": "300449",
      "prsn_ntby_qty": "6074",
      "prsn_seln_tr_pbmn": "5131230",
      "prsn_shnu_tr_pbmn": "5020361",
      "prsn_ntby_tr_pbmn": "-110869",
      "orgn_seln_vol": "36911",
      "orgn_shnu_vol": "37631",
      "orgn_ntby_qty": "720",
      "orgn_seln_tr_pbmn": "2110371",
      "orgn_shnu_tr_pbmn": "2054839",
      "orgn_ntby_tr_pbmn": "-55532",
      "scrt_seln_vol": "8493",
      "scrt_shnu_vol": "12126",
      "scrt_ntby_qty": "3633",
      "scrt_seln_tr_pbmn": "384357",
      "scrt_shnu_tr_pbmn": "472598",
      "scrt_ntby_tr_pbmn": "88241",
      "ivtr_seln_vol": "4086",
      "ivtr_shnu_vol": "3964",
      "ivtr_ntby_qty": "-122",
      "ivtr_seln_tr_pbmn": "177374",
      "ivtr_shnu_tr_pbmn": "165434",
      "ivtr_ntby_tr_pbmn": "-11940",
      "pe_fund_seln_tr_pbmn": "213413",
      "pe_fund_seln_vol": "4833",
      "pe_fund_ntby_vol": "-1804",
      "pe_fund_shnu_tr_pbmn": "115551",
      "pe_fund_shnu_vol": "3029",
      "pe_fund_ntby_tr_pbmn": "-97861",
      "bank_seln_vol": "245",
      "bank_shnu_vol": "51",
      "bank_ntby_qty": "-193",
      "bank_seln_tr_pbmn": "13382",
      "bank_shnu_tr_pbmn": "2873",
      "bank_ntby_tr_pbmn": "-10509",
      "insu_seln_vol": "1653",
      "insu_shnu_vol": "1050",
      "insu_ntby_qty": "-603",
      "insu_seln_tr_pbmn": "79782",
      "insu_shnu_tr_pbmn": "50378",
      "insu_ntby_tr_pbmn": "-29404",
      "mrbn_seln_vol": "230",
      "mrbn_shnu_vol": "310",
      "mrbn_ntby_qty": "80",
      "mrbn_seln_tr_pbmn": "10393",
      "mrbn_shnu_tr_pbmn": "11896",
      "mrbn_ntby_tr_pbmn": "1502",
      "fund_seln_vol": "17372",
      "fund_shnu_vol": "17101",
      "fund_ntby_qty": "-271",
      "fund_seln_tr_pbmn": "1231671",
      "fund_shnu_tr_pbmn": "1236109",
      "fund_ntby_tr_pbmn": "4439",
      "etc_orgt_seln_vol": "0",
      "etc_orgt_shnu_vol": "0",
      "etc_orgt_ntby_vol": "0",
      "etc_orgt_seln_tr_pbmn": "0",
      "etc_orgt_shnu_tr_pbmn": "0",
      "etc_orgt_ntby_tr_pbmn": "0",
      "etc_corp_seln_vol": "5061",
      "etc_corp_shnu_vol": "3558",
      "etc_corp_ntby_vol": "-1503",
      "etc_corp_seln_tr_pbmn": "95856",
      "etc_corp_shnu_tr_pbmn": "113601",
      "etc_corp_ntby_tr_pbmn": "17745"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```

