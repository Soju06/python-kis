# 해외지수분봉조회[v1_해외주식-031]

> [해외주식] 기본시세

해외지수분봉조회 API입니다.
실전계좌의 경우, 최근 102건까지 확인 가능합니다.

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `81269474-9c66-404f-bdfe-4bb472975330` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/overseas-price/v1/quotations/inquire-time-indexchartprice` |
| **Content-Type** | `` |
| **요청 포맷** | `` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID** | `FHKST03030200`, `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2023-07-21
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
| `tr_id` | 거래ID | String | 13 | Y | FHKST03030200 |
| `tr_cont` | 연속 거래 여부 | String | 1 | N | tr_cont를 이용한 다음조회 불가 API |
| `custtype` | 고객 타입 | String | 1 | N | B : 법인  P : 개인 |
| `seq_no` | 일련번호 | String | 2 | N | [법인 필수] 001 |
| `mac_address` | 맥주소 | String | 12 | N | 법인고객 혹은 개인고객의 Mac address 값 |
| `phone_number` | 핸드폰번호 | String | 12 | N | [법인 필수] 제휴사APP을 사용하는 경우 사용자(회원) 핸드폰번호  ex) 01011112222 (하이픈 등 구분값 제거) |
| `ip_addr` | 접속 단말 공인 IP | String | 12 | N | [법인 필수] 사용자(회원)의 IP Address |
| `gt_uid` | Global UID | String | 32 | N | [법인 전용] 거래고유번호로 사용하므로 거래별로 UNIQUE해야 함 |

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `FID_COND_MRKT_DIV_CODE` | 조건 시장 분류 코드 | String | 2 | Y | N 해외지수 X 환율 KX 원화환율 |
| `FID_INPUT_ISCD` | 입력 종목코드 | String | 12 | Y | 종목번호(ex. TSLA) |
| `FID_HOUR_CLS_CODE` | 시간 구분 코드 | String | 5 | Y | 0: 정규장, 1: 시간외 |
| `FID_PW_DATA_INCU_YN` | 과거 데이터 포함 여부 | String | 2 | Y | Y/N |

### 요청 예시

```json
{
  "FID_COND_MRKT_DIV_CODE": "N",
  "FID_INPUT_ISCD": "SPX",
  "FID_HOUR_CLS_CODE": "0",
  "FID_PW_DATA_INCU_YN": "Y"
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
| `output1` | 응답상세 | String |   | Y |  |
| `ovrs_nmix_prdy_vrss` | 해외 지수 전일 대비 | String | 114 | Y |  |
| `prdy_vrss_sign` | 전일 대비 부호 | String | 1 | Y |  |
| `hts_kor_isnm` | HTS 한글 종목명 | String | 40 | Y |  |
| `prdy_ctrt` | 전일 대비율 | String | 82 | Y |  |
| `ovrs_nmix_prdy_clpr` | 해외 지수 전일 종가 | String | 114 | Y |  |
| `acml_vol` | 누적 거래량 | String | 18 | Y |  |
| `ovrs_nmix_prpr` | 해외 지수 현재가 | String | 114 | Y |  |
| `stck_shrn_iscd` | 주식 단축 종목코드 | String | 9 | Y |  |
| `ovrs_prod_oprc` | 해외 상품 시가2 | String | 114 | Y | 시가 |
| `ovrs_prod_hgpr` | 해외 상품 최고가 | String | 114 | Y | 최고가 |
| `ovrs_prod_lwpr` | 해외 상품 최저가 | String | 114 | Y | 최저가 |
| `output2` | 응답상세2 | Object |   | Y | array |
| `stck_bsop_date` | 주식 영업 일자 | String | 8 | Y | 영업 일자 |
| `stck_cntg_hour` | 주식 체결 시간 | String | 6 | Y | 체결 시간 |
| `optn_prpr` | 옵션 현재가 | String | 112 | Y | 현재가 |
| `optn_oprc` | 옵션 시가2 | String | 112 | Y | 시가 |
| `optn_hgpr` | 옵션 최고가 | String | 112 | Y | 최고가 |
| `optn_lwpr` | 옵션 최저가 | String | 112 | Y | 최저가 |
| `cntg_vol` | 체결 거래량 | String | 18 | Y |  |

### 응답 예시

```json
{
  "output1": {
    "ovrs_nmix_prdy_vrss": "105.23",
    "prdy_vrss_sign": "2",
    "prdy_ctrt": "2.11",
    "ovrs_nmix_prdy_clpr": "4981.80",
    "acml_vol": "0",
    "hts_kor_isnm": "S&P500",
    "ovrs_nmix_prpr": "5087.03",
    "stck_shrn_iscd": "SPX",
    "ovrs_prod_oprc": "5038.83",
    "ovrs_prod_hgpr": "5094.39",
    "ovrs_prod_lwpr": "5038.83"
  },
  "output2": [
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "170600",
      "optn_prpr": "5087.03",
      "optn_oprc": "5087.03",
      "optn_hgpr": "5087.03",
      "optn_lwpr": "5087.03",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "162000",
      "optn_prpr": "5087.03",
      "optn_oprc": "5087.03",
      "optn_hgpr": "5087.03",
      "optn_lwpr": "5087.03",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "161900",
      "optn_prpr": "5087.03",
      "optn_oprc": "5087.03",
      "optn_hgpr": "5087.03",
      "optn_lwpr": "5087.03",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "161800",
      "optn_prpr": "5087.03",
      "optn_oprc": "5087.03",
      "optn_hgpr": "5087.03",
      "optn_lwpr": "5087.03",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "161700",
      "optn_prpr": "5087.03",
      "optn_oprc": "5087.03",
      "optn_hgpr": "5087.03",
      "optn_lwpr": "5087.03",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "161600",
      "optn_prpr": "5087.03",
      "optn_oprc": "5087.03",
      "optn_hgpr": "5087.03",
      "optn_lwpr": "5087.03",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "161500",
      "optn_prpr": "5087.03",
      "optn_oprc": "5087.03",
      "optn_hgpr": "5087.03",
      "optn_lwpr": "5087.03",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "161400",
      "optn_prpr": "5087.03",
      "optn_oprc": "5087.03",
      "optn_hgpr": "5087.03",
      "optn_lwpr": "5087.03",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "161300",
      "optn_prpr": "5087.03",
      "optn_oprc": "5087.03",
      "optn_hgpr": "5087.03",
      "optn_lwpr": "5087.03",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "161200",
      "optn_prpr": "5087.03",
      "optn_oprc": "5087.03",
      "optn_hgpr": "5087.03",
      "optn_lwpr": "5087.03",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "161100",
      "optn_prpr": "5087.03",
      "optn_oprc": "5087.03",
      "optn_hgpr": "5087.03",
      "optn_lwpr": "5087.03",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "161000",
      "optn_prpr": "5087.03",
      "optn_oprc": "5087.03",
      "optn_hgpr": "5087.03",
      "optn_lwpr": "5087.03",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "160900",
      "optn_prpr": "5087.03",
      "optn_oprc": "5087.03",
      "optn_hgpr": "5087.03",
      "optn_lwpr": "5087.03",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "160800",
      "optn_prpr": "5087.03",
      "optn_oprc": "5087.03",
      "optn_hgpr": "5087.03",
      "optn_lwpr": "5087.03",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "160700",
      "optn_prpr": "5087.03",
      "optn_oprc": "5087.03",
      "optn_hgpr": "5087.03",
      "optn_lwpr": "5087.03",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "160600",
      "optn_prpr": "5087.03",
      "optn_oprc": "5087.03",
      "optn_hgpr": "5087.03",
      "optn_lwpr": "5087.03",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "160500",
      "optn_prpr": "5087.03",
      "optn_oprc": "5087.03",
      "optn_hgpr": "5087.03",
      "optn_lwpr": "5087.03",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "160400",
      "optn_prpr": "5087.03",
      "optn_oprc": "5087.03",
      "optn_hgpr": "5087.03",
      "optn_lwpr": "5087.03",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "160300",
      "optn_prpr": "5087.03",
      "optn_oprc": "5087.03",
      "optn_hgpr": "5087.03",
      "optn_lwpr": "5087.03",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "160200",
      "optn_prpr": "5087.03",
      "optn_oprc": "5087.02",
      "optn_hgpr": "5087.03",
      "optn_lwpr": "5087.02",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "160100",
      "optn_prpr": "5087.02",
      "optn_oprc": "5087.02",
      "optn_hgpr": "5087.02",
      "optn_lwpr": "5087.02",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "160000",
      "optn_prpr": "5087.02",
      "optn_oprc": "5086.46",
      "optn_hgpr": "5087.02",
      "optn_lwpr": "5086.46",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "155900",
      "optn_prpr": "5086.19",
      "optn_oprc": "5086.73",
      "optn_hgpr": "5087.67",
      "optn_lwpr": "5085.72",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "155800",
      "optn_prpr": "5086.62",
      "optn_oprc": "5088.75",
      "optn_hgpr": "5088.75",
      "optn_lwpr": "5085.99",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "155700",
      "optn_prpr": "5088.55",
      "optn_oprc": "5090.37",
      "optn_hgpr": "5090.40",
      "optn_lwpr": "5087.35",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "155600",
      "optn_prpr": "5090.28",
      "optn_oprc": "5089.28",
      "optn_hgpr": "5090.28",
      "optn_lwpr": "5088.76",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "155500",
      "optn_prpr": "5089.37",
      "optn_oprc": "5087.89",
      "optn_hgpr": "5092.58",
      "optn_lwpr": "5087.89",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "155400",
      "optn_prpr": "5087.82",
      "optn_oprc": "5089.10",
      "optn_hgpr": "5089.17",
      "optn_lwpr": "5086.64",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "155300",
      "optn_prpr": "5089.13",
      "optn_oprc": "5087.97",
      "optn_hgpr": "5089.33",
      "optn_lwpr": "5087.53",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "155200",
      "optn_prpr": "5087.93",
      "optn_oprc": "5086.30",
      "optn_hgpr": "5088.03",
      "optn_lwpr": "5086.30",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "155100",
      "optn_prpr": "5086.19",
      "optn_oprc": "5087.40",
      "optn_hgpr": "5087.40",
      "optn_lwpr": "5085.22",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "155000",
      "optn_prpr": "5087.42",
      "optn_oprc": "5086.76",
      "optn_hgpr": "5088.79",
      "optn_lwpr": "5086.37",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "154900",
      "optn_prpr": "5086.81",
      "optn_oprc": "5086.47",
      "optn_hgpr": "5087.24",
      "optn_lwpr": "5086.09",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "154800",
      "optn_prpr": "5086.39",
      "optn_oprc": "5086.93",
      "optn_hgpr": "5087.27",
      "optn_lwpr": "5086.34",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "154700",
      "optn_prpr": "5086.85",
      "optn_oprc": "5087.45",
      "optn_hgpr": "5087.91",
      "optn_lwpr": "5086.78",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "154600",
      "optn_prpr": "5087.49",
      "optn_oprc": "5087.78",
      "optn_hgpr": "5088.12",
      "optn_lwpr": "5087.14",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "154500",
      "optn_prpr": "5087.71",
      "optn_oprc": "5087.73",
      "optn_hgpr": "5087.83",
      "optn_lwpr": "5086.98",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "154400",
      "optn_prpr": "5087.87",
      "optn_oprc": "5089.52",
      "optn_hgpr": "5090.29",
      "optn_lwpr": "5087.87",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "154300",
      "optn_prpr": "5089.44",
      "optn_oprc": "5092.13",
      "optn_hgpr": "5092.29",
      "optn_lwpr": "5089.41",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "154200",
      "optn_prpr": "5092.09",
      "optn_oprc": "5091.81",
      "optn_hgpr": "5092.86",
      "optn_lwpr": "5091.61",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "154100",
      "optn_prpr": "5091.82",
      "optn_oprc": "5091.07",
      "optn_hgpr": "5091.93",
      "optn_lwpr": "5090.69",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "154000",
      "optn_prpr": "5091.08",
      "optn_oprc": "5090.41",
      "optn_hgpr": "5091.10",
      "optn_lwpr": "5090.37",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "153900",
      "optn_prpr": "5090.27",
      "optn_oprc": "5089.71",
      "optn_hgpr": "5090.39",
      "optn_lwpr": "5089.00",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "153800",
      "optn_prpr": "5089.42",
      "optn_oprc": "5089.06",
      "optn_hgpr": "5090.42",
      "optn_lwpr": "5089.04",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "153700",
      "optn_prpr": "5089.02",
      "optn_oprc": "5088.11",
      "optn_hgpr": "5089.14",
      "optn_lwpr": "5088.02",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "153600",
      "optn_prpr": "5088.15",
      "optn_oprc": "5087.72",
      "optn_hgpr": "5088.24",
      "optn_lwpr": "5087.08",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "153500",
      "optn_prpr": "5087.69",
      "optn_oprc": "5085.66",
      "optn_hgpr": "5087.78",
      "optn_lwpr": "5085.03",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "153400",
      "optn_prpr": "5085.75",
      "optn_oprc": "5085.03",
      "optn_hgpr": "5086.00",
      "optn_lwpr": "5084.40",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "153300",
      "optn_prpr": "5085.00",
      "optn_oprc": "5084.04",
      "optn_hgpr": "5085.03",
      "optn_lwpr": "5083.99",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "153200",
      "optn_prpr": "5083.97",
      "optn_oprc": "5084.93",
      "optn_hgpr": "5085.65",
      "optn_lwpr": "5083.85",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "153100",
      "optn_prpr": "5085.05",
      "optn_oprc": "5087.11",
      "optn_hgpr": "5087.25",
      "optn_lwpr": "5085.05",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "153000",
      "optn_prpr": "5087.01",
      "optn_oprc": "5087.39",
      "optn_hgpr": "5087.74",
      "optn_lwpr": "5086.44",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "152900",
      "optn_prpr": "5087.30",
      "optn_oprc": "5089.37",
      "optn_hgpr": "5089.87",
      "optn_lwpr": "5087.27",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "152800",
      "optn_prpr": "5089.29",
      "optn_oprc": "5090.04",
      "optn_hgpr": "5090.04",
      "optn_lwpr": "5089.09",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "152700",
      "optn_prpr": "5090.04",
      "optn_oprc": "5089.97",
      "optn_hgpr": "5090.36",
      "optn_lwpr": "5089.24",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "152600",
      "optn_prpr": "5089.92",
      "optn_oprc": "5089.77",
      "optn_hgpr": "5090.02",
      "optn_lwpr": "5089.28",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "152500",
      "optn_prpr": "5089.68",
      "optn_oprc": "5089.07",
      "optn_hgpr": "5089.73",
      "optn_lwpr": "5088.87",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "152400",
      "optn_prpr": "5088.91",
      "optn_oprc": "5089.75",
      "optn_hgpr": "5089.75",
      "optn_lwpr": "5088.17",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "152300",
      "optn_prpr": "5089.78",
      "optn_oprc": "5089.37",
      "optn_hgpr": "5089.85",
      "optn_lwpr": "5088.89",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "152200",
      "optn_prpr": "5089.37",
      "optn_oprc": "5087.83",
      "optn_hgpr": "5089.39",
      "optn_lwpr": "5087.82",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "152100",
      "optn_prpr": "5087.72",
      "optn_oprc": "5087.44",
      "optn_hgpr": "5088.23",
      "optn_lwpr": "5087.44",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "152000",
      "optn_prpr": "5087.46",
      "optn_oprc": "5088.20",
      "optn_hgpr": "5088.51",
      "optn_lwpr": "5087.29",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "151900",
      "optn_prpr": "5088.08",
      "optn_oprc": "5087.59",
      "optn_hgpr": "5088.09",
      "optn_lwpr": "5087.11",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "151800",
      "optn_prpr": "5087.50",
      "optn_oprc": "5086.13",
      "optn_hgpr": "5087.79",
      "optn_lwpr": "5086.13",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "151700",
      "optn_prpr": "5086.13",
      "optn_oprc": "5086.15",
      "optn_hgpr": "5086.75",
      "optn_lwpr": "5085.64",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "151600",
      "optn_prpr": "5086.09",
      "optn_oprc": "5085.59",
      "optn_hgpr": "5086.77",
      "optn_lwpr": "5085.57",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "151500",
      "optn_prpr": "5085.52",
      "optn_oprc": "5085.34",
      "optn_hgpr": "5086.10",
      "optn_lwpr": "5085.11",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "151400",
      "optn_prpr": "5085.35",
      "optn_oprc": "5085.13",
      "optn_hgpr": "5085.38",
      "optn_lwpr": "5084.35",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "151300",
      "optn_prpr": "5085.09",
      "optn_oprc": "5084.68",
      "optn_hgpr": "5086.24",
      "optn_lwpr": "5084.65",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "151200",
      "optn_prpr": "5084.67",
      "optn_oprc": "5084.37",
      "optn_hgpr": "5084.72",
      "optn_lwpr": "5083.81",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "151100",
      "optn_prpr": "5084.39",
      "optn_oprc": "5084.85",
      "optn_hgpr": "5084.85",
      "optn_lwpr": "5084.26",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "151000",
      "optn_prpr": "5084.80",
      "optn_oprc": "5083.57",
      "optn_hgpr": "5084.80",
      "optn_lwpr": "5082.58",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "150900",
      "optn_prpr": "5083.58",
      "optn_oprc": "5084.67",
      "optn_hgpr": "5084.67",
      "optn_lwpr": "5083.33",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "150800",
      "optn_prpr": "5084.65",
      "optn_oprc": "5084.90",
      "optn_hgpr": "5085.29",
      "optn_lwpr": "5084.16",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "150700",
      "optn_prpr": "5084.71",
      "optn_oprc": "5086.41",
      "optn_hgpr": "5086.64",
      "optn_lwpr": "5084.15",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "150600",
      "optn_prpr": "5086.59",
      "optn_oprc": "5086.16",
      "optn_hgpr": "5087.41",
      "optn_lwpr": "5086.09",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "150500",
      "optn_prpr": "5086.16",
      "optn_oprc": "5086.06",
      "optn_hgpr": "5086.48",
      "optn_lwpr": "5085.66",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "150400",
      "optn_prpr": "5086.21",
      "optn_oprc": "5085.47",
      "optn_hgpr": "5086.24",
      "optn_lwpr": "5085.36",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "150300",
      "optn_prpr": "5085.34",
      "optn_oprc": "5083.47",
      "optn_hgpr": "5085.45",
      "optn_lwpr": "5083.47",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "150200",
      "optn_prpr": "5083.44",
      "optn_oprc": "5081.88",
      "optn_hgpr": "5084.21",
      "optn_lwpr": "5081.87",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "150100",
      "optn_prpr": "5081.85",
      "optn_oprc": "5082.40",
      "optn_hgpr": "5082.40",
      "optn_lwpr": "5081.02",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "150000",
      "optn_prpr": "5082.43",
      "optn_oprc": "5081.86",
      "optn_hgpr": "5082.59",
      "optn_lwpr": "5081.22",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "145900",
      "optn_prpr": "5081.86",
      "optn_oprc": "5081.31",
      "optn_hgpr": "5082.59",
      "optn_lwpr": "5081.26",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "145800",
      "optn_prpr": "5081.44",
      "optn_oprc": "5079.44",
      "optn_hgpr": "5081.97",
      "optn_lwpr": "5079.44",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "145700",
      "optn_prpr": "5079.46",
      "optn_oprc": "5080.86",
      "optn_hgpr": "5081.53",
      "optn_lwpr": "5079.36",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "145600",
      "optn_prpr": "5080.99",
      "optn_oprc": "5085.84",
      "optn_hgpr": "5085.86",
      "optn_lwpr": "5080.99",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "145500",
      "optn_prpr": "5085.87",
      "optn_oprc": "5085.68",
      "optn_hgpr": "5086.25",
      "optn_lwpr": "5085.52",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "145400",
      "optn_prpr": "5085.65",
      "optn_oprc": "5085.31",
      "optn_hgpr": "5085.65",
      "optn_lwpr": "5084.91",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "145300",
      "optn_prpr": "5085.31",
      "optn_oprc": "5085.00",
      "optn_hgpr": "5085.33",
      "optn_lwpr": "5084.55",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "145200",
      "optn_prpr": "5084.97",
      "optn_oprc": "5085.08",
      "optn_hgpr": "5085.53",
      "optn_lwpr": "5084.95",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "145100",
      "optn_prpr": "5085.12",
      "optn_oprc": "5083.58",
      "optn_hgpr": "5085.12",
      "optn_lwpr": "5083.58",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "145000",
      "optn_prpr": "5083.60",
      "optn_oprc": "5085.14",
      "optn_hgpr": "5085.16",
      "optn_lwpr": "5083.60",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "144900",
      "optn_prpr": "5085.18",
      "optn_oprc": "5085.61",
      "optn_hgpr": "5086.11",
      "optn_lwpr": "5084.90",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "144800",
      "optn_prpr": "5085.58",
      "optn_oprc": "5085.85",
      "optn_hgpr": "5085.97",
      "optn_lwpr": "5085.27",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "144700",
      "optn_prpr": "5085.82",
      "optn_oprc": "5086.21",
      "optn_hgpr": "5086.22",
      "optn_lwpr": "5084.99",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "144600",
      "optn_prpr": "5086.21",
      "optn_oprc": "5088.44",
      "optn_hgpr": "5088.44",
      "optn_lwpr": "5085.95",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "144500",
      "optn_prpr": "5088.44",
      "optn_oprc": "5087.92",
      "optn_hgpr": "5088.44",
      "optn_lwpr": "5087.88",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "144400",
      "optn_prpr": "5087.87",
      "optn_oprc": "5087.02",
      "optn_hgpr": "5088.13",
      "optn_lwpr": "5087.02",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "144300",
      "optn_prpr": "5087.11",
      "optn_oprc": "5086.53",
      "optn_hgpr": "5087.11",
      "optn_lwpr": "5086.29",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "144200",
      "optn_prpr": "5086.53",
      "optn_oprc": "5085.60",
      "optn_hgpr": "5086.61",
      "optn_lwpr": "5085.60",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "144100",
      "optn_prpr": "5085.53",
      "optn_oprc": "5086.30",
      "optn_hgpr": "5086.30",
      "optn_lwpr": "5085.20",
      "cntg_vol": "0"
    },
    {
      "stck_bsop_date": "20240222",
      "stck_cntg_hour": "144000",
      "optn_prpr": "5086.34",
      "optn_oprc": "5087.80",
      "optn_hgpr": "5087.80",
      "optn_lwpr": "5086.02",
      "cntg_vol": "0"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```
