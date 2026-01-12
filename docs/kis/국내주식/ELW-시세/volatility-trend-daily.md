# ELW 변동성 추이(일별) [국내주식-178]

> [국내주식] ELW 시세

ELW 변동성 추이(일별) API입니다.
한국투자 HTS(eFriend Plus) > [0284] ELW 변동성 추이 화면의 "일별" 변동성 추이 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `5bd31e17-ea4d-4e76-8e03-f8dfb3be25e7` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/elw/v1/quotations/volatility-trend-daily` |
| **Content-Type** | `` |
| **요청 포맷** | `` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `미지원` |
| **TR ID** | `FHPEW02840200`, `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-04-26
- **최종 수정일**: 2025-05-07

## 요청 (Request)

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials G... |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | FHPEW02840200 |
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
| `FID_COND_MRKT_DIV_CODE` | 조건시장분류코드 | String | 2 | Y | 시장구분코드 (W) |
| `FID_INPUT_ISCD` | 입력종목코드 | String | 12 | Y | ex) 58J297(KBJ297삼성전자콜) |

### 요청 예시

```json
FID_COND_MRKT_DIV_CODE:W
FID_INPUT_ISCD:57JS61
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
| `output` | 응답상세 | Object |   | Y | array |
| `stck_bsop_date` | 주식 영업 일자 | String | 8 | Y |  |
| `elw_prpr` | ELW 현재가 | String | 10 | Y |  |
| `prdy_vrss` | 전일대비 | String | 10 | Y |  |
| `prdy_vrss_sign` | 전일대비부호 | String | 1 | Y |  |
| `prdy_ctrt` | 전일대비율 | String | 8 | Y |  |
| `elw_oprc` | elw 시가2 | String | 10 | Y |  |
| `elw_hgpr` | elw 최고가 | String | 10 | Y |  |
| `elw_lwpr` | elw 최저가 | String | 10 | Y |  |
| `acml_vol` | 누적 거래량 | String | 18 | Y |  |
| `d10_hist_vltl` | 10일 역사적 변동성 | String | 11 | Y |  |
| `d20_hist_vltl` | 20일 역사적 변동성 | String | 11 | Y |  |
| `d30_hist_vltl` | 30일 역사적 변동성 | String | 11 | Y |  |
| `d60_hist_vltl` | 60일 역사적 변동성 | String | 11 | Y |  |
| `d90_hist_vltl` | 90일 역사적 변동성 | String | 11 | Y |  |
| `hts_ints_vltl` | HTS 내재 변동성 | String | 11 | Y |  |

### 응답 예시

```json
{
    "output": [
        {
            "stck_bsop_date": "20240503",
            "elw_prpr": "5",
            "prdy_vrss": "0",
            "prdy_vrss_sign": "3",
            "prdy_ctrt": "0.00",
            "elw_oprc": "5",
            "elw_hgpr": "5",
            "elw_lwpr": "5",
            "acml_vol": "76410",
            "d10_hist_vltl": "21.05",
            "d20_hist_vltl": "20.32",
            "d30_hist_vltl": "19.58",
            "d60_hist_vltl": "17.91",
            "d90_hist_vltl": "18.33",
            "hts_ints_vltl": "23.37"
        },
        {
            "stck_bsop_date": "20240502",
            "elw_prpr": "5",
            "prdy_vrss": "-15",
            "prdy_vrss_sign": "5",
            "prdy_ctrt": "-75.00",
            "elw_oprc": "20",
            "elw_hgpr": "20",
            "elw_lwpr": "5",
            "acml_vol": "6509850",
            "d10_hist_vltl": "23.00",
            "d20_hist_vltl": "21.31",
            "d30_hist_vltl": "20.17",
            "d60_hist_vltl": "19.07",
            "d90_hist_vltl": "18.33",
            "hts_ints_vltl": "20.16"
        },
        {
            "stck_bsop_date": "20240430",
            "elw_prpr": "20",
            "prdy_vrss": "-5",
            "prdy_vrss_sign": "5",
            "prdy_ctrt": "-20.00",
            "elw_oprc": "25",
            "elw_hgpr": "25",
            "elw_lwpr": "15",
            "acml_vol": "1839420",
            "d10_hist_vltl": "23.69",
            "d20_hist_vltl": "21.39",
            "d30_hist_vltl": "20.42",
            "d60_hist_vltl": "19.43",
            "d90_hist_vltl": "18.33",
            "hts_ints_vltl": "23.45"
        },
        {
            "stck_bsop_date": "20240429",
            "elw_prpr": "25",
            "prdy_vrss": "-40",
            "prdy_vrss_sign": "5",
            "prdy_ctrt": "-61.54",
            "elw_oprc": "35",
            "elw_hgpr": "40",
            "elw_lwpr": "25",
            "acml_vol": "3301030",
            "d10_hist_vltl": "26.85",
            "d20_hist_vltl": "21.38",
            "d30_hist_vltl": "20.48",
            "d60_hist_vltl": "19.44",
            "d90_hist_vltl": "18.37",
            "hts_ints_vltl": "21.85"
        },
        {
            "stck_bsop_date": "20240426",
            "elw_prpr": "65",
            "prdy_vrss": "-70",
            "prdy_vrss_sign": "5",
            "prdy_ctrt": "-51.85",
            "elw_oprc": "65",
            "elw_hgpr": "95",
            "elw_lwpr": "50",
            "acml_vol": "11476800",
            "d10_hist_vltl": "26.51",
            "d20_hist_vltl": "21.14",
            "d30_hist_vltl": "21.13",
            "d60_hist_vltl": "19.34",
            "d90_hist_vltl": "18.45",
            "hts_ints_vltl": "22.04"
        },
        {
            "stck_bsop_date": "20240425",
            "elw_prpr": "135",
            "prdy_vrss": "80",
            "prdy_vrss_sign": "2",
            "prdy_ctrt": "145.45",
            "elw_oprc": "100",
            "elw_hgpr": "135",
            "elw_lwpr": "85",
            "acml_vol": "16588080",
            "d10_hist_vltl": "26.14",
            "d20_hist_vltl": "20.66",
            "d30_hist_vltl": "21.01",
            "d60_hist_vltl": "19.30",
            "d90_hist_vltl": "18.39",
            "hts_ints_vltl": "21.20"
        },
        {
            "stck_bsop_date": "20240424",
            "elw_prpr": "55",
            "prdy_vrss": "-115",
            "prdy_vrss_sign": "5",
            "prdy_ctrt": "-67.65",
            "elw_oprc": "75",
            "elw_hgpr": "75",
            "elw_lwpr": "50",
            "acml_vol": "8909400",
            "d10_hist_vltl": "23.99",
            "d20_hist_vltl": "19.38",
            "d30_hist_vltl": "20.25",
            "d60_hist_vltl": "18.86",
            "d90_hist_vltl": "18.11",
            "hts_ints_vltl": "20.73"
        },
        {
            "stck_bsop_date": "20240423",
            "elw_prpr": "170",
            "prdy_vrss": "-20",
            "prdy_vrss_sign": "5",
            "prdy_ctrt": "-10.53",
            "elw_oprc": "180",
            "elw_hgpr": "200",
            "elw_lwpr": "145",
            "acml_vol": "44577440",
            "d10_hist_vltl": "21.44",
            "d20_hist_vltl": "18.18",
            "d30_hist_vltl": "19.40",
            "d60_hist_vltl": "18.35",
            "d90_hist_vltl": "17.77",
            "hts_ints_vltl": "20.33"
        },
        {
            "stck_bsop_date": "20240422",
            "elw_prpr": "190",
            "prdy_vrss": "-210",
            "prdy_vrss_sign": "5",
            "prdy_ctrt": "-52.50",
            "elw_oprc": "265",
            "elw_hgpr": "305",
            "elw_lwpr": "190",
            "acml_vol": "79163330",
            "d10_hist_vltl": "21.44",
            "d20_hist_vltl": "18.25",
            "d30_hist_vltl": "19.58",
            "d60_hist_vltl": "18.37",
            "d90_hist_vltl": "17.88",
            "hts_ints_vltl": "21.25"
        },
        {
            "stck_bsop_date": "20240419",
            "elw_prpr": "400",
            "prdy_vrss": "215",
            "prdy_vrss_sign": "2",
            "prdy_ctrt": "116.22",
            "elw_oprc": "290",
            "elw_hgpr": "725",
            "elw_lwpr": "285",
            "acml_vol": "63410060",
            "d10_hist_vltl": "21.22",
            "d20_hist_vltl": "17.73",
            "d30_hist_vltl": "19.66",
            "d60_hist_vltl": "18.26",
            "d90_hist_vltl": "17.76",
            "hts_ints_vltl": "24.18"
        },
        {
            "stck_bsop_date": "20240418",
            "elw_prpr": "185",
            "prdy_vrss": "-165",
            "prdy_vrss_sign": "5",
            "prdy_ctrt": "-47.14",
            "elw_oprc": "295",
            "elw_hgpr": "325",
            "elw_lwpr": "180",
            "acml_vol": "35347180",
            "d10_hist_vltl": "20.69",
            "d20_hist_vltl": "19.36",
            "d30_hist_vltl": "18.92",
            "d60_hist_vltl": "17.87",
            "d90_hist_vltl": "17.50",
            "hts_ints_vltl": "21.30"
        },
        {
            "stck_bsop_date": "20240417",
            "elw_prpr": "350",
            "prdy_vrss": "80",
            "prdy_vrss_sign": "2",
            "prdy_ctrt": "29.63",
            "elw_oprc": "235",
            "elw_hgpr": "350",
            "elw_lwpr": "215",
            "acml_vol": "68687230",
            "d10_hist_vltl": "20.70",
            "d20_hist_vltl": "19.25",
            "d30_hist_vltl": "18.23",
            "d60_hist_vltl": "17.87",
            "d90_hist_vltl": "17.33",
            "hts_ints_vltl": "21.02"
        },
        {
            "stck_bsop_date": "20240416",
            "elw_prpr": "270",
            "prdy_vrss": "170",
            "prdy_vrss_sign": "2",
            "prdy_ctrt": "170.00",
            "elw_oprc": "180",
            "elw_hgpr": "320",
            "elw_lwpr": "165",
            "acml_vol": "45554270",
            "d10_hist_vltl": "20.10",
            "d20_hist_vltl": "19.26",
            "d30_hist_vltl": "18.17",
            "d60_hist_vltl": "17.74",
            "d90_hist_vltl": "17.24",
            "hts_ints_vltl": "21.23"
        },
        {
            "stck_bsop_date": "20240415",
            "elw_prpr": "100",
            "prdy_vrss": "0",
            "prdy_vrss_sign": "3",
            "prdy_ctrt": "0.00",
            "elw_oprc": "140",
            "elw_hgpr": "195",
            "elw_lwpr": "100",
            "acml_vol": "16103560",
            "d10_hist_vltl": "15.63",
            "d20_hist_vltl": "17.28",
            "d30_hist_vltl": "17.35",
            "d60_hist_vltl": "17.87",
            "d90_hist_vltl": "16.86",
            "hts_ints_vltl": "19.64"
        },
        {
            "stck_bsop_date": "20240412",
            "elw_prpr": "100",
            "prdy_vrss": "-5",
            "prdy_vrss_sign": "5",
            "prdy_ctrt": "-4.76",
            "elw_oprc": "85",
            "elw_hgpr": "120",
            "elw_lwpr": "80",
            "acml_vol": "5222010",
            "d10_hist_vltl": "15.51",
            "d20_hist_vltl": "18.67",
            "d30_hist_vltl": "17.31",
            "d60_hist_vltl": "18.05",
            "d90_hist_vltl": "16.86",
            "hts_ints_vltl": "20.27"
        },
        {
            "stck_bsop_date": "20240411",
            "elw_prpr": "105",
            "prdy_vrss": "5",
            "prdy_vrss_sign": "2",
            "prdy_ctrt": "5.00",
            "elw_oprc": "125",
            "elw_hgpr": "160",
            "elw_lwpr": "90",
            "acml_vol": "2031830",
            "d10_hist_vltl": "14.74",
            "d20_hist_vltl": "18.70",
            "d30_hist_vltl": "17.41",
            "d60_hist_vltl": "17.96",
            "d90_hist_vltl": "16.79",
            "hts_ints_vltl": "22.02"
        },
        {
            "stck_bsop_date": "20240409",
            "elw_prpr": "100",
            "prdy_vrss": "10",
            "prdy_vrss_sign": "2",
            "prdy_ctrt": "11.11",
            "elw_oprc": "65",
            "elw_hgpr": "100",
            "elw_lwpr": "60",
            "acml_vol": "999560",
            "d10_hist_vltl": "14.75",
            "d20_hist_vltl": "18.80",
            "d30_hist_vltl": "17.56",
            "d60_hist_vltl": "18.00",
            "d90_hist_vltl": "16.90",
            "hts_ints_vltl": "20.93"
        },
        {
            "stck_bsop_date": "20240408",
            "elw_prpr": "90",
            "prdy_vrss": "-20",
            "prdy_vrss_sign": "5",
            "prdy_ctrt": "-18.18",
            "elw_oprc": "95",
            "elw_hgpr": "95",
            "elw_lwpr": "75",
            "acml_vol": "159080",
            "d10_hist_vltl": "15.41",
            "d20_hist_vltl": "18.88",
            "d30_hist_vltl": "17.65",
            "d60_hist_vltl": "17.96",
            "d90_hist_vltl": "16.87",
            "hts_ints_vltl": "21.04"
        },
        {
            "stck_bsop_date": "20240405",
            "elw_prpr": "110",
            "prdy_vrss": "40",
            "prdy_vrss_sign": "2",
            "prdy_ctrt": "57.14",
            "elw_oprc": "95",
            "elw_hgpr": "115",
            "elw_lwpr": "80",
            "acml_vol": "562130",
            "d10_hist_vltl": "15.60",
            "d20_hist_vltl": "19.16",
            "d30_hist_vltl": "17.65",
            "d60_hist_vltl": "18.05",
            "d90_hist_vltl": "16.93",
            "hts_ints_vltl": "21.19"
        },
        {
            "stck_bsop_date": "20240404",
            "elw_prpr": "70",
            "prdy_vrss": "-30",
            "prdy_vrss_sign": "5",
            "prdy_ctrt": "-30.00",
            "elw_oprc": "70",
            "elw_hgpr": "70",
            "elw_lwpr": "60",
            "acml_vol": "1086750",
            "d10_hist_vltl": "14.58",
            "d20_hist_vltl": "19.40",
            "d30_hist_vltl": "17.41",
            "d60_hist_vltl": "17.94",
            "d90_hist_vltl": "16.83",
            "hts_ints_vltl": "20.35"
        },
        {
            "stck_bsop_date": "20240403",
            "elw_prpr": "100",
            "prdy_vrss": "0",
            "prdy_vrss_sign": "3",
            "prdy_ctrt": "0.00",
            "elw_oprc": "75",
            "elw_hgpr": "100",
            "elw_lwpr": "75",
            "acml_vol": "305570",
            "d10_hist_vltl": "19.05",
            "d20_hist_vltl": "18.53",
            "d30_hist_vltl": "16.79",
            "d60_hist_vltl": "17.67",
            "d90_hist_vltl": "16.62",
            "hts_ints_vltl": "18.85"
        },
        {
            "stck_bsop_date": "20240402",
            "elw_prpr": "100",
            "prdy_vrss": "30",
            "prdy_vrss_sign": "2",
            "prdy_ctrt": "42.86",
            "elw_oprc": "65",
            "elw_hgpr": "100",
            "elw_lwpr": "55",
            "acml_vol": "1056250",
            "d10_hist_vltl": "18.75",
            "d20_hist_vltl": "17.42",
            "d30_hist_vltl": "16.29",
            "d60_hist_vltl": "17.29",
            "d90_hist_vltl": "16.39",
            "hts_ints_vltl": "21.66"
        },
        {
            "stck_bsop_date": "20240401",
            "elw_prpr": "70",
            "prdy_vrss": "-15",
            "prdy_vrss_sign": "5",
            "prdy_ctrt": "-17.65",
            "elw_oprc": "60",
            "elw_hgpr": "120",
            "elw_lwpr": "60",
            "acml_vol": "839440",
            "d10_hist_vltl": "19.44",
            "d20_hist_vltl": "17.67",
            "d30_hist_vltl": "16.80",
            "d60_hist_vltl": "17.35",
            "d90_hist_vltl": "16.40",
            "hts_ints_vltl": "18.57"
        },...
        {
            "stck_bsop_date": "20231206",
            "elw_prpr": "1775",
            "prdy_vrss": "65",
            "prdy_vrss_sign": "2",
            "prdy_ctrt": "3.80",
            "elw_oprc": "1775",
            "elw_hgpr": "1775",
            "elw_lwpr": "1775",
            "acml_vol": "20",
            "d10_hist_vltl": "11.54",
            "d20_hist_vltl": "12.91",
            "d30_hist_vltl": "22.19",
            "d60_hist_vltl": "19.42",
            "d90_hist_vltl": "0.00",
            "hts_ints_vltl": "10.60"
        }
    ],
    "rt_cd": "0",
    "msg_cd": "MCA00000",
    "msg1": "정상처리 되었습니다."
}
```
