# 업종 분봉조회[v1_국내주식-045]

> [국내주식] 업종/기타

업종분봉조회 API입니다.
실전계좌의 경우, 한 번의 호출에 최대 102건까지 확인 가능합니다.

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `5613b629-b622-4a22-8175-31a4376c36b4` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/quotations/inquire-time-indexchartprice` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID** | `모의투자 미지원`, `FHKUP03500200` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2023-08-18
- **최종 수정일**: 2025-05-14

## 요청 (Request)

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials G... |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | FHKUP03500200 |
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
| `FID_COND_MRKT_DIV_CODE` | FID 조건 시장 분류 코드 | String | 2 | Y | U |
| `FID_ETC_CLS_CODE` | FID 기타 구분 코드 | String | 12 | Y | 0: 기본 1:장마감,시간외 제외 |
| `FID_INPUT_ISCD` | FID 입력 종목코드 | String | 12 | Y | 0001 : 종합 0002 : 대형주 ... 포탈 (FAQ : 종목정보 다운로드(국내) - 업종코드 참조) |
| `FID_INPUT_HOUR_1` | FID 입력 시간1 | String | 12 | Y | 30, 60 -> 1분, 600-> 10분, 3600 -> 1시간 |
| `FID_PW_DATA_INCU_YN` | FID 과거 데이터 포함 여부 | String | 12 | Y | Y (과거) / N (당일) |

### 요청 예시

```json
{
  "FID_COND_MRKT_DIV_CODE": "U",
  "FID_INPUT_ISCD": "1001",
  "FID_INPUT_HOUR_1": "120",
  "FID_PW_DATA_INCU_YN": "Y",
  "FID_ETC_CLS_CODE": "0"
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
| `Output1` | 응답상세 | Object |   | Y |  |
| `bstp_nmix_prdy_vrss` | 업종 지수 전일 대비 | String | 112 | Y |  |
| `prdy_vrss_sign` | 전일 대비 부호 | String | 1 | Y |  |
| `bstp_nmix_prdy_ctrt` | 업종 지수 전일 대비율 | String | 82 | Y |  |
| `prdy_nmix` | 전일 지수 | String | 112 | Y |  |
| `acml_vol` | 누적 거래량 | String | 18 | Y |  |
| `acml_tr_pbmn` | 누적 거래 대금 | String | 18 | Y |  |
| `hts_kor_isnm` | HTS 한글 종목명 | String | 40 | Y |  |
| `bstp_nmix_prpr` | 업종 지수 현재가 | String | 112 | Y |  |
| `bstp_cls_code` | 업종 구분 코드 | String | 4 | Y |  |
| `prdy_vol` | 전일 거래량 | String | 18 | Y |  |
| `bstp_nmix_oprc` | 업종 지수 시가2 | String | 112 | Y |  |
| `bstp_nmix_hgpr` | 업종 지수 최고가 | String | 112 | Y |  |
| `bstp_nmix_lwpr` | 업종 지수 최저가 | String | 112 | Y |  |
| `futs_prdy_oprc` | 선물 전일 시가 | String | 112 | Y |  |
| `futs_prdy_hgpr` | 선물 전일 최고가 | String | 112 | Y |  |
| `futs_prdy_lwpr` | 선물 전일 최저가 | String | 112 | Y |  |
| `Output2` | 응답상세2 | String |   | Y | array |
| `stck_bsop_date` | 주식 영업 일자 | String | 8 | Y |  |
| `stck_cntg_hour` | 주식 체결 시간 | String | 6 | Y |  |
| `bstp_nmix_prpr` | 업종 지수 현재가 | String | 112 | Y |  |
| `bstp_nmix_oprc` | 업종 지수 시가2 | String | 112 | Y |  |
| `bstp_nmix_hgpr` | 업종 지수 최고가 | String | 112 | Y |  |
| `bstp_nmix_lwpr` | 업종 지수 최저가 | String | 112 | Y |  |
| `cntg_vol` | 체결 거래량 | String | 18 | Y |  |
| `acml_tr_pbmn` | 누적 거래 대금 | String | 18 | Y |  |

### 응답 예시

```json
{
  "output1": {
    "bstp_nmix_prdy_vrss": "-3.68",
    "prdy_vrss_sign": "5",
    "bstp_nmix_prdy_ctrt": "-0.44",
    "prdy_nmix": "837.24",
    "acml_vol": "554702",
    "acml_tr_pbmn": "5740155",
    "hts_kor_isnm": "KOSDAQ",
    "bstp_nmix_prpr": "833.56",
    "bstp_cls_code": "1001",
    "prdy_vol": "1238780",
    "bstp_nmix_oprc": "841.21",
    "bstp_nmix_hgpr": "841.21",
    "bstp_nmix_lwpr": "830.09",
    "futs_prdy_oprc": "818.76",
    "futs_prdy_hgpr": "839.52",
    "futs_prdy_lwpr": "817.06"
  },
  "output2": [
    {
      "stck_bsop_date": "20240129",
      "stck_cntg_hour": "103200",
      "bstp_nmix_prpr": "833.56",
      "bstp_nmix_oprc": "834.07",
      "bstp_nmix_hgpr": "834.07",
      "bstp_nmix_lwpr": "833.56",
      "cntg_vol": "4618",
      "acml_tr_pbmn": "5740155"
    },
    {
      "stck_bsop_date": "20240129",
      "stck_cntg_hour": "103000",
      "bstp_nmix_prpr": "833.99",
      "bstp_nmix_oprc": "834.29",
      "bstp_nmix_hgpr": "834.29",
      "bstp_nmix_lwpr": "833.89",
      "cntg_vol": "4601",
      "acml_tr_pbmn": "5689290"
    },
    {
      "stck_bsop_date": "20240129",
      "stck_cntg_hour": "102800",
      "bstp_nmix_prpr": "834.24",
      "bstp_nmix_oprc": "833.47",
      "bstp_nmix_hgpr": "834.32",
      "bstp_nmix_lwpr": "833.44",
      "cntg_vol": "4978",
      "acml_tr_pbmn": "5635506"
    },
    {
      "stck_bsop_date": "20240129",
      "stck_cntg_hour": "102600",
      "bstp_nmix_prpr": "833.46",
      "bstp_nmix_oprc": "832.36",
      "bstp_nmix_hgpr": "833.46",
      "bstp_nmix_lwpr": "832.36",
      "cntg_vol": "5033",
      "acml_tr_pbmn": "5581000"
    },
    {
      "stck_bsop_date": "20240129",
      "stck_cntg_hour": "102400",
      "bstp_nmix_prpr": "832.48",
      "bstp_nmix_oprc": "832.92",
      "bstp_nmix_hgpr": "832.92",
      "bstp_nmix_lwpr": "832.47",
      "cntg_vol": "5239",
      "acml_tr_pbmn": "5518332"
    },
    {
      "stck_bsop_date": "20240129",
      "stck_cntg_hour": "102200",
      "bstp_nmix_prpr": "832.85",
      "bstp_nmix_oprc": "832.77",
      "bstp_nmix_hgpr": "832.87",
      "bstp_nmix_lwpr": "832.69",
      "cntg_vol": "6042",
      "acml_tr_pbmn": "5455651"
    },
    {
      "stck_bsop_date": "20240129",
      "stck_cntg_hour": "102000",
      "bstp_nmix_prpr": "832.74",
      "bstp_nmix_oprc": "832.55",
      "bstp_nmix_hgpr": "833.25",
      "bstp_nmix_lwpr": "832.55",
      "cntg_vol": "6301",
      "acml_tr_pbmn": "5372736"
    },
    {
      "stck_bsop_date": "20240129",
      "stck_cntg_hour": "101800",
      "bstp_nmix_prpr": "832.83",
      "bstp_nmix_oprc": "832.51",
      "bstp_nmix_hgpr": "832.83",
      "bstp_nmix_lwpr": "832.22",
      "cntg_vol": "5676",
      "acml_tr_pbmn": "5284172"
    },
    {
      "stck_bsop_date": "20240129",
      "stck_cntg_hour": "101600",
      "bstp_nmix_prpr": "832.50",
      "bstp_nmix_oprc": "832.27",
      "bstp_nmix_hgpr": "832.62",
      "bstp_nmix_lwpr": "832.09",
      "cntg_vol": "4771",
      "acml_tr_pbmn": "5219827"
    },
    {
      "stck_bsop_date": "20240129",
      "stck_cntg_hour": "101400",
      "bstp_nmix_prpr": "832.44",
      "bstp_nmix_oprc": "832.03",
      "bstp_nmix_hgpr": "832.52",
      "bstp_nmix_lwpr": "832.03",
      "cntg_vol": "6639",
      "acml_tr_pbmn": "5167005"
    },
    {
      "stck_bsop_date": "20240129",
      "stck_cntg_hour": "101200",
      "bstp_nmix_prpr": "832.11",
      "bstp_nmix_oprc": "831.98",
      "bstp_nmix_hgpr": "832.24",
      "bstp_nmix_lwpr": "831.75",
      "cntg_vol": "6946",
      "acml_tr_pbmn": "5093186"
    },
    {
      "stck_bsop_date": "20240129",
      "stck_cntg_hour": "101000",
      "bstp_nmix_prpr": "832.23",
      "bstp_nmix_oprc": "831.36",
      "bstp_nmix_hgpr": "832.23",
      "bstp_nmix_lwpr": "831.35",
      "cntg_vol": "6579",
      "acml_tr_pbmn": "5011060"
    },
    {
      "stck_bsop_date": "20240129",
      "stck_cntg_hour": "100800",
      "bstp_nmix_prpr": "831.22",
      "bstp_nmix_oprc": "831.05",
      "bstp_nmix_hgpr": "831.22",
      "bstp_nmix_lwpr": "830.55",
      "cntg_vol": "6837",
      "acml_tr_pbmn": "4928657"
    },
    {
      "stck_bsop_date": "20240129",
      "stck_cntg_hour": "100600",
      "bstp_nmix_prpr": "830.98",
      "bstp_nmix_oprc": "831.46",
      "bstp_nmix_hgpr": "831.54",
      "bstp_nmix_lwpr": "830.98",
      "cntg_vol": "6694",
      "acml_tr_pbmn": "4854815"
    },
    {
      "stck_bsop_date": "20240129",
      "stck_cntg_hour": "100400",
      "bstp_nmix_prpr": "831.76",
      "bstp_nmix_oprc": "830.79",
      "bstp_nmix_hgpr": "831.76",
      "bstp_nmix_lwpr": "830.79",
      "cntg_vol": "6839",
      "acml_tr_pbmn": "4781557"
    },
    {
      "stck_bsop_date": "20240129",
      "stck_cntg_hour": "100200",
      "bstp_nmix_prpr": "830.92",
      "bstp_nmix_oprc": "831.17",
      "bstp_nmix_hgpr": "831.21",
      "bstp_nmix_lwpr": "830.71",
      "cntg_vol": "9589",
      "acml_tr_pbmn": "4724555"
    },
    {
      "stck_bsop_date": "20240129",
      "stck_cntg_hour": "100000",
      "bstp_nmix_prpr": "831.14",
      "bstp_nmix_oprc": "831.32",
      "bstp_nmix_hgpr": "831.52",
      "bstp_nmix_lwpr": "830.90",
      "cntg_vol": "8688",
      "acml_tr_pbmn": "4652376"
    },
    {
      "stck_bsop_date": "20240129",
      "stck_cntg_hour": "095800",
      "bstp_nmix_prpr": "831.56",
      "bstp_nmix_oprc": "831.32",
      "bstp_nmix_hgpr": "831.76",
      "bstp_nmix_lwpr": "831.32",
      "cntg_vol": "6519",
      "acml_tr_pbmn": "4568901"
    },
    {
      "stck_bsop_date": "20240129",
      "stck_cntg_hour": "095600",
      "bstp_nmix_prpr": "831.43",
      "bstp_nmix_oprc": "830.68",
      "bstp_nmix_hgpr": "831.43",
      "bstp_nmix_lwpr": "830.52",
      "cntg_vol": "7474",
      "acml_tr_pbmn": "4497224"
    },
    {
      "stck_bsop_date": "20240129",
      "stck_cntg_hour": "095400",
      "bstp_nmix_prpr": "830.50",
      "bstp_nmix_oprc": "831.46",
      "bstp_nmix_hgpr": "831.46",
      "bstp_nmix_lwpr": "830.50",
      "cntg_vol": "9190",
      "acml_tr_pbmn": "4423313"
    },
    {
      "stck_bsop_date": "20240129",
      "stck_cntg_hour": "095200",
      "bstp_nmix_prpr": "831.57",
      "bstp_nmix_oprc": "831.45",
      "bstp_nmix_hgpr": "831.59",
      "bstp_nmix_lwpr": "831.38",
      "cntg_vol": "7701",
      "acml_tr_pbmn": "4324541"
    },
    {
      "stck_bsop_date": "20240129",
      "stck_cntg_hour": "095000",
      "bstp_nmix_prpr": "831.60",
      "bstp_nmix_oprc": "831.45",
      "bstp_nmix_hgpr": "831.82",
      "bstp_nmix_lwpr": "831.39",
      "cntg_vol": "7529",
      "acml_tr_pbmn": "4247753"
    },
    {
      "stck_bsop_date": "20240129",
      "stck_cntg_hour": "094800",
      "bstp_nmix_prpr": "831.57",
      "bstp_nmix_oprc": "831.71",
      "bstp_nmix_hgpr": "831.76",
      "bstp_nmix_lwpr": "831.47",
      "cntg_vol": "7754",
      "acml_tr_pbmn": "4165554"
    },
    {
      "stck_bsop_date": "20240129",
      "stck_cntg_hour": "094600",
      "bstp_nmix_prpr": "831.77",
      "bstp_nmix_oprc": "830.50",
      "bstp_nmix_hgpr": "831.91",
      "bstp_nmix_lwpr": "830.44",
      "cntg_vol": "9213",
      "acml_tr_pbmn": "4076635"
    },
    {
      "stck_bsop_date": "20240129",
      "stck_cntg_hour": "094400",
      "bstp_nmix_prpr": "830.26",
      "bstp_nmix_oprc": "830.57",
      "bstp_nmix_hgpr": "830.67",
      "bstp_nmix_lwpr": "830.09",
      "cntg_vol": "7201",
      "acml_tr_pbmn": "3971601"
    },
    {
      "stck_bsop_date": "20240129",
      "stck_cntg_hour": "094200",
      "bstp_nmix_prpr": "830.53",
      "bstp_nmix_oprc": "831.03",
      "bstp_nmix_hgpr": "831.21",
      "bstp_nmix_lwpr": "830.48",
      "cntg_vol": "7992",
      "acml_tr_pbmn": "3886154"
    },
    {
      "stck_bsop_date": "20240129",
      "stck_cntg_hour": "094000",
      "bstp_nmix_prpr": "830.98",
      "bstp_nmix_oprc": "831.26",
      "bstp_nmix_hgpr": "831.26",
      "bstp_nmix_lwpr": "830.32",
      "cntg_vol": "9912",
      "acml_tr_pbmn": "3790733"
    },
    {
      "stck_bsop_date": "20240129",
      "stck_cntg_hour": "093800",
      "bstp_nmix_prpr": "831.32",
      "bstp_nmix_oprc": "832.07",
      "bstp_nmix_hgpr": "832.07",
      "bstp_nmix_lwpr": "831.27",
      "cntg_vol": "9575",
      "acml_tr_pbmn": "3663618"
    },
    {
      "stck_bsop_date": "20240129",
      "stck_cntg_hour": "093600",
      "bstp_nmix_prpr": "832.24",
      "bstp_nmix_oprc": "831.34",
      "bstp_nmix_hgpr": "832.30",
      "bstp_nmix_lwpr": "831.34",
      "cntg_vol": "10164",
      "acml_tr_pbmn": "3561037"
    },
    {
      "stck_bsop_date": "20240129",
      "stck_cntg_hour": "093400",
      "bstp_nmix_prpr": "831.44",
      "bstp_nmix_oprc": "832.64",
      "bstp_nmix_hgpr": "832.64",
      "bstp_nmix_lwpr": "831.44",
      "cntg_vol": "11415",
      "acml_tr_pbmn": "3447235"
    },
    {
      "stck_bsop_date": "20240129",
      "stck_cntg_hour": "093200",
      "bstp_nmix_prpr": "832.53",
      "bstp_nmix_oprc": "833.45",
      "bstp_nmix_hgpr": "833.66",
      "bstp_nmix_lwpr": "832.53",
      "cntg_vol": "11522",
      "acml_tr_pbmn": "3316543"
    },
    {
      "stck_bsop_date": "20240129",
      "stck_cntg_hour": "093000",
      "bstp_nmix_prpr": "833.58",
      "bstp_nmix_oprc": "833.59",
      "bstp_nmix_hgpr": "834.05",
      "bstp_nmix_lwpr": "833.36",
      "cntg_vol": "11105",
      "acml_tr_pbmn": "3203362"
    },
    {
      "stck_bsop_date": "20240129",
      "stck_cntg_hour": "092800",
      "bstp_nmix_prpr": "833.97",
      "bstp_nmix_oprc": "832.91",
      "bstp_nmix_hgpr": "833.97",
      "bstp_nmix_lwpr": "832.36",
      "cntg_vol": "15502",
      "acml_tr_pbmn": "3071005"
    },
    {
      "stck_bsop_date": "20240129",
      "stck_cntg_hour": "092600",
      "bstp_nmix_prpr": "833.08",
      "bstp_nmix_oprc": "835.04",
      "bstp_nmix_hgpr": "835.04",
      "bstp_nmix_lwpr": "833.00",
      "cntg_vol": "15656",
      "acml_tr_pbmn": "2928429"
    },
    {
      "stck_bsop_date": "20240129",
      "stck_cntg_hour": "092400",
      "bstp_nmix_prpr": "834.63",
      "bstp_nmix_oprc": "833.51",
      "bstp_nmix_hgpr": "834.98",
      "bstp_nmix_lwpr": "833.51",
      "cntg_vol": "16851",
      "acml_tr_pbmn": "2747155"
    },
    {
      "stck_bsop_date": "20240129",
      "stck_cntg_hour": "092200",
      "bstp_nmix_prpr": "833.45",
      "bstp_nmix_oprc": "835.50",
      "bstp_nmix_hgpr": "835.50",
      "bstp_nmix_lwpr": "833.45",
      "cntg_vol": "16696",
      "acml_tr_pbmn": "2583365"
    },
    {
      "stck_bsop_date": "20240129",
      "stck_cntg_hour": "092000",
      "bstp_nmix_prpr": "835.91",
      "bstp_nmix_oprc": "835.96",
      "bstp_nmix_hgpr": "836.14",
      "bstp_nmix_lwpr": "835.76",
      "cntg_vol": "16008",
      "acml_tr_pbmn": "2424467"
    },
    {
      "stck_bsop_date": "20240129",
      "stck_cntg_hour": "091800",
      "bstp_nmix_prpr": "836.05",
      "bstp_nmix_oprc": "838.39",
      "bstp_nmix_hgpr": "838.39",
      "bstp_nmix_lwpr": "835.98",
      "cntg_vol": "16778",
      "acml_tr_pbmn": "2260216"
    },
    {
      "stck_bsop_date": "20240129",
      "stck_cntg_hour": "091600",
      "bstp_nmix_prpr": "838.24",
      "bstp_nmix_oprc": "837.19",
      "bstp_nmix_hgpr": "838.70",
      "bstp_nmix_lwpr": "837.19",
      "cntg_vol": "17379",
      "acml_tr_pbmn": "2098721"
    },
    {
      "stck_bsop_date": "20240129",
      "stck_cntg_hour": "091400",
      "bstp_nmix_prpr": "836.82",
      "bstp_nmix_oprc": "836.88",
      "bstp_nmix_hgpr": "837.94",
      "bstp_nmix_lwpr": "836.48",
      "cntg_vol": "19020",
      "acml_tr_pbmn": "1934637"
    },
    {
      "stck_bsop_date": "20240129",
      "stck_cntg_hour": "091200",
      "bstp_nmix_prpr": "836.73",
      "bstp_nmix_oprc": "837.87",
      "bstp_nmix_hgpr": "838.34",
      "bstp_nmix_lwpr": "836.73",
      "cntg_vol": "27881",
      "acml_tr_pbmn": "1781817"
    },
    {
      "stck_bsop_date": "20240129",
      "stck_cntg_hour": "091000",
      "bstp_nmix_prpr": "837.70",
      "bstp_nmix_oprc": "837.68",
      "bstp_nmix_hgpr": "837.72",
      "bstp_nmix_lwpr": "837.38",
      "cntg_vol": "16983",
      "acml_tr_pbmn": "1606668"
    },
    {
      "stck_bsop_date": "20240129",
      "stck_cntg_hour": "090800",
      "bstp_nmix_prpr": "837.87",
      "bstp_nmix_oprc": "840.59",
      "bstp_nmix_hgpr": "840.59",
      "bstp_nmix_lwpr": "837.87",
      "cntg_vol": "21991",
      "acml_tr_pbmn": "1441148"
    },
    {
      "stck_bsop_date": "20240129",
      "stck_cntg_hour": "090600",
      "bstp_nmix_prpr": "840.98",
      "bstp_nmix_oprc": "839.46",
      "bstp_nmix_hgpr": "841.17",
      "bstp_nmix_lwpr": "839.46",
      "cntg_vol": "20366",
      "acml_tr_pbmn": "1234692"
    },
    {
      "stck_bsop_date": "20240129",
      "stck_cntg_hour": "090400",
      "bstp_nmix_prpr": "839.42",
      "bstp_nmix_oprc": "836.70",
      "bstp_nmix_hgpr": "839.42",
      "bstp_nmix_lwpr": "836.70",
      "cntg_vol": "27395",
      "acml_tr_pbmn": "1007681"
    },
    {
      "stck_bsop_date": "20240129",
      "stck_cntg_hour": "090200",
      "bstp_nmix_prpr": "836.69",
      "bstp_nmix_oprc": "838.54",
      "bstp_nmix_hgpr": "838.54",
      "bstp_nmix_lwpr": "835.19",
      "cntg_vol": "31941",
      "acml_tr_pbmn": "754939"
    },
    {
      "stck_bsop_date": "20240129",
      "stck_cntg_hour": "090000",
      "bstp_nmix_prpr": "838.62",
      "bstp_nmix_oprc": "841.21",
      "bstp_nmix_hgpr": "841.21",
      "bstp_nmix_lwpr": "838.42",
      "cntg_vol": "33919",
      "acml_tr_pbmn": "422108"
    },
    {
      "stck_bsop_date": "20240126",
      "stck_cntg_hour": "999999",
      "bstp_nmix_prpr": "837.24",
      "bstp_nmix_oprc": "837.24",
      "bstp_nmix_hgpr": "837.24",
      "bstp_nmix_lwpr": "837.24",
      "cntg_vol": "21566",
      "acml_tr_pbmn": "11242548"
    },
    {
      "stck_bsop_date": "20240126",
      "stck_cntg_hour": "888888",
      "bstp_nmix_prpr": "837.24",
      "bstp_nmix_oprc": "837.24",
      "bstp_nmix_hgpr": "837.24",
      "bstp_nmix_lwpr": "837.24",
      "cntg_vol": "42",
      "acml_tr_pbmn": "11058431"
    },
    {
      "stck_bsop_date": "20240126",
      "stck_cntg_hour": "153200",
      "bstp_nmix_prpr": "837.20",
      "bstp_nmix_oprc": "837.19",
      "bstp_nmix_hgpr": "837.20",
      "bstp_nmix_lwpr": "837.19",
      "cntg_vol": "126",
      "acml_tr_pbmn": "11057509"
    },
    {
      "stck_bsop_date": "20240126",
      "stck_cntg_hour": "153000",
      "bstp_nmix_prpr": "837.19",
      "bstp_nmix_oprc": "836.97",
      "bstp_nmix_hgpr": "837.25",
      "bstp_nmix_lwpr": "836.97",
      "cntg_vol": "17043",
      "acml_tr_pbmn": "11056788"
    },
    {
      "stck_bsop_date": "20240126",
      "stck_cntg_hour": "152800",
      "bstp_nmix_prpr": "836.97",
      "bstp_nmix_oprc": "836.97",
      "bstp_nmix_hgpr": "836.97",
      "bstp_nmix_lwpr": "836.97",
      "cntg_vol": "0",
      "acml_tr_pbmn": "10792443"
    },
    {
      "stck_bsop_date": "20240126",
      "stck_cntg_hour": "152600",
      "bstp_nmix_prpr": "836.97",
      "bstp_nmix_oprc": "836.97",
      "bstp_nmix_hgpr": "836.97",
      "bstp_nmix_lwpr": "836.97",
      "cntg_vol": "0",
      "acml_tr_pbmn": "10792443"
    },
    {
      "stck_bsop_date": "20240126",
      "stck_cntg_hour": "152400",
      "bstp_nmix_prpr": "836.97",
      "bstp_nmix_oprc": "836.97",
      "bstp_nmix_hgpr": "836.97",
      "bstp_nmix_lwpr": "836.97",
      "cntg_vol": "0",
      "acml_tr_pbmn": "10792443"
    },
    {
      "stck_bsop_date": "20240126",
      "stck_cntg_hour": "152200",
      "bstp_nmix_prpr": "836.97",
      "bstp_nmix_oprc": "836.97",
      "bstp_nmix_hgpr": "836.97",
      "bstp_nmix_lwpr": "836.97",
      "cntg_vol": "0",
      "acml_tr_pbmn": "10792443"
    },
    {
      "stck_bsop_date": "20240126",
      "stck_cntg_hour": "152000",
      "bstp_nmix_prpr": "836.97",
      "bstp_nmix_oprc": "836.97",
      "bstp_nmix_hgpr": "836.97",
      "bstp_nmix_lwpr": "836.97",
      "cntg_vol": "1000",
      "acml_tr_pbmn": "10792443"
    },
    {
      "stck_bsop_date": "20240126",
      "stck_cntg_hour": "151800",
      "bstp_nmix_prpr": "837.01",
      "bstp_nmix_oprc": "836.79",
      "bstp_nmix_hgpr": "837.05",
      "bstp_nmix_lwpr": "836.49",
      "cntg_vol": "8328",
      "acml_tr_pbmn": "10784186"
    },
    {
      "stck_bsop_date": "20240126",
      "stck_cntg_hour": "151600",
      "bstp_nmix_prpr": "836.90",
      "bstp_nmix_oprc": "836.72",
      "bstp_nmix_hgpr": "836.93",
      "bstp_nmix_lwpr": "836.64",
      "cntg_vol": "6227",
      "acml_tr_pbmn": "10699895"
    },
    {
      "stck_bsop_date": "20240126",
      "stck_cntg_hour": "151400",
      "bstp_nmix_prpr": "836.86",
      "bstp_nmix_oprc": "836.63",
      "bstp_nmix_hgpr": "836.96",
      "bstp_nmix_lwpr": "836.57",
      "cntg_vol": "5728",
      "acml_tr_pbmn": "10633883"
    },
    {
      "stck_bsop_date": "20240126",
      "stck_cntg_hour": "151200",
      "bstp_nmix_prpr": "836.70",
      "bstp_nmix_oprc": "836.71",
      "bstp_nmix_hgpr": "836.84",
      "bstp_nmix_lwpr": "836.44",
      "cntg_vol": "6163",
      "acml_tr_pbmn": "10578452"
    },
    {
      "stck_bsop_date": "20240126",
      "stck_cntg_hour": "151000",
      "bstp_nmix_prpr": "836.83",
      "bstp_nmix_oprc": "836.97",
      "bstp_nmix_hgpr": "836.98",
      "bstp_nmix_lwpr": "836.69",
      "cntg_vol": "4617",
      "acml_tr_pbmn": "10523064"
    },
    {
      "stck_bsop_date": "20240126",
      "stck_cntg_hour": "150800",
      "bstp_nmix_prpr": "836.92",
      "bstp_nmix_oprc": "836.97",
      "bstp_nmix_hgpr": "837.02",
      "bstp_nmix_lwpr": "836.70",
      "cntg_vol": "4728",
      "acml_tr_pbmn": "10472083"
    },
    {
      "stck_bsop_date": "20240126",
      "stck_cntg_hour": "150600",
      "bstp_nmix_prpr": "836.97",
      "bstp_nmix_oprc": "836.70",
      "bstp_nmix_hgpr": "837.06",
      "bstp_nmix_lwpr": "836.70",
      "cntg_vol": "4719",
      "acml_tr_pbmn": "10420811"
    },
    {
      "stck_bsop_date": "20240126",
      "stck_cntg_hour": "150400",
      "bstp_nmix_prpr": "836.66",
      "bstp_nmix_oprc": "836.19",
      "bstp_nmix_hgpr": "836.92",
      "bstp_nmix_lwpr": "836.19",
      "cntg_vol": "4377",
      "acml_tr_pbmn": "10372366"
    },
    {
      "stck_bsop_date": "20240126",
      "stck_cntg_hour": "150200",
      "bstp_nmix_prpr": "836.29",
      "bstp_nmix_oprc": "836.18",
      "bstp_nmix_hgpr": "836.38",
      "bstp_nmix_lwpr": "836.18",
      "cntg_vol": "4261",
      "acml_tr_pbmn": "10320188"
    },
    {
      "stck_bsop_date": "20240126",
      "stck_cntg_hour": "150000",
      "bstp_nmix_prpr": "836.28",
      "bstp_nmix_oprc": "836.24",
      "bstp_nmix_hgpr": "836.44",
      "bstp_nmix_lwpr": "836.20",
      "cntg_vol": "4420",
      "acml_tr_pbmn": "10273218"
    },
    {
      "stck_bsop_date": "20240126",
      "stck_cntg_hour": "145800",
      "bstp_nmix_prpr": "836.43",
      "bstp_nmix_oprc": "837.13",
      "bstp_nmix_hgpr": "837.18",
      "bstp_nmix_lwpr": "836.43",
      "cntg_vol": "4215",
      "acml_tr_pbmn": "10218137"
    },
    {
      "stck_bsop_date": "20240126",
      "stck_cntg_hour": "145600",
      "bstp_nmix_prpr": "837.23",
      "bstp_nmix_oprc": "837.95",
      "bstp_nmix_hgpr": "838.01",
      "bstp_nmix_lwpr": "837.23",
      "cntg_vol": "4978",
      "acml_tr_pbmn": "10166106"
    },
    {
      "stck_bsop_date": "20240126",
      "stck_cntg_hour": "145400",
      "bstp_nmix_prpr": "837.89",
      "bstp_nmix_oprc": "837.66",
      "bstp_nmix_hgpr": "837.96",
      "bstp_nmix_lwpr": "837.66",
      "cntg_vol": "5102",
      "acml_tr_pbmn": "10110923"
    },
    {
      "stck_bsop_date": "20240126",
      "stck_cntg_hour": "145200",
      "bstp_nmix_prpr": "837.66",
      "bstp_nmix_oprc": "837.41",
      "bstp_nmix_hgpr": "837.66",
      "bstp_nmix_lwpr": "837.22",
      "cntg_vol": "3840",
      "acml_tr_pbmn": "10055054"
    },
    {
      "stck_bsop_date": "20240126",
      "stck_cntg_hour": "145000",
      "bstp_nmix_prpr": "837.58",
      "bstp_nmix_oprc": "837.24",
      "bstp_nmix_hgpr": "837.71",
      "bstp_nmix_lwpr": "837.24",
      "cntg_vol": "4172",
      "acml_tr_pbmn": "10008690"
    },
    {
      "stck_bsop_date": "20240126",
      "stck_cntg_hour": "144800",
      "bstp_nmix_prpr": "837.37",
      "bstp_nmix_oprc": "837.80",
      "bstp_nmix_hgpr": "837.80",
      "bstp_nmix_lwpr": "837.23",
      "cntg_vol": "4593",
      "acml_tr_pbmn": "9966720"
    },
    {
      "stck_bsop_date": "20240126",
      "stck_cntg_hour": "144600",
      "bstp_nmix_prpr": "837.66",
      "bstp_nmix_oprc": "837.72",
      "bstp_nmix_hgpr": "837.89",
      "bstp_nmix_lwpr": "837.61",
      "cntg_vol": "5105",
      "acml_tr_pbmn": "9916624"
    },
    {
      "stck_bsop_date": "20240126",
      "stck_cntg_hour": "144400",
      "bstp_nmix_prpr": "837.72",
      "bstp_nmix_oprc": "837.55",
      "bstp_nmix_hgpr": "837.72",
      "bstp_nmix_lwpr": "837.42",
      "cntg_vol": "4214",
      "acml_tr_pbmn": "9861241"
    },
    {
      "stck_bsop_date": "20240126",
      "stck_cntg_hour": "144200",
      "bstp_nmix_prpr": "837.50",
      "bstp_nmix_oprc": "837.55",
      "bstp_nmix_hgpr": "837.68",
      "bstp_nmix_lwpr": "837.35",
      "cntg_vol": "3357",
      "acml_tr_pbmn": "9819268"
    },
    {
      "stck_bsop_date": "20240126",
      "stck_cntg_hour": "144000",
      "bstp_nmix_prpr": "837.56",
      "bstp_nmix_oprc": "837.93",
      "bstp_nmix_hgpr": "838.04",
      "bstp_nmix_lwpr": "837.56",
      "cntg_vol": "3515",
      "acml_tr_pbmn": "9783824"
    },
    {
      "stck_bsop_date": "20240126",
      "stck_cntg_hour": "143800",
      "bstp_nmix_prpr": "837.96",
      "bstp_nmix_oprc": "837.49",
      "bstp_nmix_hgpr": "837.96",
      "bstp_nmix_lwpr": "837.49",
      "cntg_vol": "4026",
      "acml_tr_pbmn": "9745091"
    },
    {
      "stck_bsop_date": "20240126",
      "stck_cntg_hour": "143600",
      "bstp_nmix_prpr": "837.50",
      "bstp_nmix_oprc": "837.47",
      "bstp_nmix_hgpr": "837.59",
      "bstp_nmix_lwpr": "837.25",
      "cntg_vol": "4327",
      "acml_tr_pbmn": "9702397"
    },
    {
      "stck_bsop_date": "20240126",
      "stck_cntg_hour": "143400",
      "bstp_nmix_prpr": "837.44",
      "bstp_nmix_oprc": "837.19",
      "bstp_nmix_hgpr": "837.44",
      "bstp_nmix_lwpr": "836.97",
      "cntg_vol": "3352",
      "acml_tr_pbmn": "9664056"
    },
    {
      "stck_bsop_date": "20240126",
      "stck_cntg_hour": "143200",
      "bstp_nmix_prpr": "837.19",
      "bstp_nmix_oprc": "837.00",
      "bstp_nmix_hgpr": "837.19",
      "bstp_nmix_lwpr": "836.85",
      "cntg_vol": "3969",
      "acml_tr_pbmn": "9626091"
    },
    {
      "stck_bsop_date": "20240126",
      "stck_cntg_hour": "143000",
      "bstp_nmix_prpr": "836.85",
      "bstp_nmix_oprc": "836.27",
      "bstp_nmix_hgpr": "836.85",
      "bstp_nmix_lwpr": "836.10",
      "cntg_vol": "4263",
      "acml_tr_pbmn": "9584077"
    },
    {
      "stck_bsop_date": "20240126",
      "stck_cntg_hour": "142800",
      "bstp_nmix_prpr": "836.18",
      "bstp_nmix_oprc": "835.52",
      "bstp_nmix_hgpr": "836.24",
      "bstp_nmix_lwpr": "835.52",
      "cntg_vol": "4294",
      "acml_tr_pbmn": "9542286"
    },
    {
      "stck_bsop_date": "20240126",
      "stck_cntg_hour": "142600",
      "bstp_nmix_prpr": "835.62",
      "bstp_nmix_oprc": "835.41",
      "bstp_nmix_hgpr": "835.66",
      "bstp_nmix_lwpr": "835.41",
      "cntg_vol": "3538",
      "acml_tr_pbmn": "9501271"
    },
    {
      "stck_bsop_date": "20240126",
      "stck_cntg_hour": "142400",
      "bstp_nmix_prpr": "835.44",
      "bstp_nmix_oprc": "835.54",
      "bstp_nmix_hgpr": "835.68",
      "bstp_nmix_lwpr": "835.37",
      "cntg_vol": "3291",
      "acml_tr_pbmn": "9469724"
    },
    {
      "stck_bsop_date": "20240126",
      "stck_cntg_hour": "142200",
      "bstp_nmix_prpr": "835.48",
      "bstp_nmix_oprc": "835.60",
      "bstp_nmix_hgpr": "835.60",
      "bstp_nmix_lwpr": "835.28",
      "cntg_vol": "3640",
      "acml_tr_pbmn": "9433016"
    },
    {
      "stck_bsop_date": "20240126",
      "stck_cntg_hour": "142000",
      "bstp_nmix_prpr": "835.70",
      "bstp_nmix_oprc": "835.57",
      "bstp_nmix_hgpr": "835.72",
      "bstp_nmix_lwpr": "835.51",
      "cntg_vol": "4522",
      "acml_tr_pbmn": "9401939"
    },
    {
      "stck_bsop_date": "20240126",
      "stck_cntg_hour": "141800",
      "bstp_nmix_prpr": "835.54",
      "bstp_nmix_oprc": "835.99",
      "bstp_nmix_hgpr": "836.00",
      "bstp_nmix_lwpr": "835.34",
      "cntg_vol": "3266",
      "acml_tr_pbmn": "9365741"
    },
    {
      "stck_bsop_date": "20240126",
      "stck_cntg_hour": "141600",
      "bstp_nmix_prpr": "835.98",
      "bstp_nmix_oprc": "836.29",
      "bstp_nmix_hgpr": "836.37",
      "bstp_nmix_lwpr": "835.98",
      "cntg_vol": "4813",
      "acml_tr_pbmn": "9334612"
    },
    {
      "stck_bsop_date": "20240126",
      "stck_cntg_hour": "141400",
      "bstp_nmix_prpr": "836.34",
      "bstp_nmix_oprc": "835.77",
      "bstp_nmix_hgpr": "836.34",
      "bstp_nmix_lwpr": "835.77",
      "cntg_vol": "4714",
      "acml_tr_pbmn": "9284831"
    },
    {
      "stck_bsop_date": "20240126",
      "stck_cntg_hour": "141200",
      "bstp_nmix_prpr": "835.79",
      "bstp_nmix_oprc": "835.74",
      "bstp_nmix_hgpr": "835.98",
      "bstp_nmix_lwpr": "835.58",
      "cntg_vol": "4125",
      "acml_tr_pbmn": "9238577"
    },
    {
      "stck_bsop_date": "20240126",
      "stck_cntg_hour": "141000",
      "bstp_nmix_prpr": "835.74",
      "bstp_nmix_oprc": "835.45",
      "bstp_nmix_hgpr": "835.74",
      "bstp_nmix_lwpr": "835.45",
      "cntg_vol": "4232",
      "acml_tr_pbmn": "9193950"
    },
    {
      "stck_bsop_date": "20240126",
      "stck_cntg_hour": "140800",
      "bstp_nmix_prpr": "835.10",
      "bstp_nmix_oprc": "835.07",
      "bstp_nmix_hgpr": "835.32",
      "bstp_nmix_lwpr": "835.00",
      "cntg_vol": "3639",
      "acml_tr_pbmn": "9151925"
    },
    {
      "stck_bsop_date": "20240126",
      "stck_cntg_hour": "140600",
      "bstp_nmix_prpr": "835.10",
      "bstp_nmix_oprc": "835.09",
      "bstp_nmix_hgpr": "835.23",
      "bstp_nmix_lwpr": "834.96",
      "cntg_vol": "4277",
      "acml_tr_pbmn": "9115282"
    },
    {
      "stck_bsop_date": "20240126",
      "stck_cntg_hour": "140400",
      "bstp_nmix_prpr": "835.15",
      "bstp_nmix_oprc": "835.11",
      "bstp_nmix_hgpr": "835.27",
      "bstp_nmix_lwpr": "835.08",
      "cntg_vol": "4475",
      "acml_tr_pbmn": "9068253"
    },
    {
      "stck_bsop_date": "20240126",
      "stck_cntg_hour": "140200",
      "bstp_nmix_prpr": "835.06",
      "bstp_nmix_oprc": "834.84",
      "bstp_nmix_hgpr": "835.08",
      "bstp_nmix_lwpr": "834.65",
      "cntg_vol": "5444",
      "acml_tr_pbmn": "9029494"
    },
    {
      "stck_bsop_date": "20240126",
      "stck_cntg_hour": "140000",
      "bstp_nmix_prpr": "834.89",
      "bstp_nmix_oprc": "833.23",
      "bstp_nmix_hgpr": "834.89",
      "bstp_nmix_lwpr": "833.14",
      "cntg_vol": "7096",
      "acml_tr_pbmn": "8979885"
    },
    {
      "stck_bsop_date": "20240126",
      "stck_cntg_hour": "135800",
      "bstp_nmix_prpr": "833.24",
      "bstp_nmix_oprc": "833.42",
      "bstp_nmix_hgpr": "833.42",
      "bstp_nmix_lwpr": "833.10",
      "cntg_vol": "6187",
      "acml_tr_pbmn": "8916527"
    },
    {
      "stck_bsop_date": "20240126",
      "stck_cntg_hour": "135600",
      "bstp_nmix_prpr": "833.59",
      "bstp_nmix_oprc": "834.41",
      "bstp_nmix_hgpr": "834.43",
      "bstp_nmix_lwpr": "833.59",
      "cntg_vol": "8204",
      "acml_tr_pbmn": "8861652"
    },
    {
      "stck_bsop_date": "20240126",
      "stck_cntg_hour": "135400",
      "bstp_nmix_prpr": "834.42",
      "bstp_nmix_oprc": "834.61",
      "bstp_nmix_hgpr": "834.74",
      "bstp_nmix_lwpr": "834.42",
      "cntg_vol": "6831",
      "acml_tr_pbmn": "8787250"
    },
    {
      "stck_bsop_date": "20240126",
      "stck_cntg_hour": "135200",
      "bstp_nmix_prpr": "834.83",
      "bstp_nmix_oprc": "834.77",
      "bstp_nmix_hgpr": "835.15",
      "bstp_nmix_lwpr": "834.54",
      "cntg_vol": "5100",
      "acml_tr_pbmn": "8747544"
    },
    {
      "stck_bsop_date": "20240126",
      "stck_cntg_hour": "135000",
      "bstp_nmix_prpr": "834.71",
      "bstp_nmix_oprc": "834.97",
      "bstp_nmix_hgpr": "835.00",
      "bstp_nmix_lwpr": "834.59",
      "cntg_vol": "4921",
      "acml_tr_pbmn": "8707064"
    },
    {
      "stck_bsop_date": "20240126",
      "stck_cntg_hour": "134800",
      "bstp_nmix_prpr": "835.01",
      "bstp_nmix_oprc": "835.12",
      "bstp_nmix_hgpr": "835.24",
      "bstp_nmix_lwpr": "835.01",
      "cntg_vol": "5332",
      "acml_tr_pbmn": "8667443"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```
