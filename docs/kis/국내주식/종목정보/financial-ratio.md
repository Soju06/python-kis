# 국내주식 재무비율[v1_국내주식-080]

> [국내주식] 종목정보

국내주식 재무비율 API입니다.
한국투자 HTS(eFriend Plus) > [0635] 재무분석종합 화면의 우측의 '재무 비율' 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `26c5165d-1910-4467-aed9-7213524b7546` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/finance/financial-ratio` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID** | `모의투자 미지원`, `FHKST66430300` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-02-29
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
| `tr_id` | 거래ID | String | 13 | Y | FHKST66430300 |
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
| `FID_DIV_CLS_CODE` | 분류 구분 코드 | String | 2 | Y | 0: 년, 1: 분기 |
| `fid_cond_mrkt_div_code` | 조건 시장 분류 코드 | String | 2 | Y | J |
| `fid_input_iscd` | 입력 종목코드 | String | 12 | Y | 000660 : 종목코드 |

### 요청 예시

```json
{
  "fid_cond_mrkt_div_code": "J",
  "fid_input_iscd": "005930",
  "fid_div_cls_code": "1"
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
| `output` | 응답상세 | Object |   | Y | array |
| `stac_yymm` | 결산 년월 | String | 6 | Y |  |
| `grs` | 매출액 증가율 | String | 124 | Y |  |
| `bsop_prfi_inrt` | 영업 이익 증가율 | String | 124 | Y | 적자지속, 흑자전환, 적자전환인 경우 0으로 표시 |
| `ntin_inrt` | 순이익 증가율 | String | 124 | Y |  |
| `roe_val` | ROE 값 | String | 132 | Y |  |
| `eps` | EPS | String | 112 | Y |  |
| `sps` | 주당매출액 | String | 18 | Y |  |
| `bps` | BPS | String | 112 | Y |  |
| `rsrv_rate` | 유보 비율 | String | 84 | Y |  |
| `lblt_rate` | 부채 비율 | String | 84 | Y |  |

### 응답 예시

```json
{
  "output": [
    {
      "stac_yymm": "202312",
      "grs": "-14.33",
      "bsop_prfi_inrt": "-84.86",
      "ntin_inrt": "-72.17",
      "roe_val": "4.14",
      "eps": "2131.00",
      "sps": "38120",
      "bps": "52002.00",
      "rsrv_rate": "39256.91",
      "lblt_rate": "25.36"
    },
    {
      "stac_yymm": "202309",
      "grs": "-17.52",
      "bsop_prfi_inrt": "-90.42",
      "ntin_inrt": "-71.26",
      "roe_val": "3.22",
      "eps": "1244.00",
      "sps": "37522",
      "bps": "52068.00",
      "rsrv_rate": "39306.65",
      "lblt_rate": "24.89"
    },
    {
      "stac_yymm": "202306",
      "grs": "-20.15",
      "bsop_prfi_inrt": "-95.36",
      "ntin_inrt": "-85.29",
      "roe_val": "1.70",
      "eps": "434.00",
      "sps": "36437",
      "bps": "51385.00",
      "rsrv_rate": "38789.91",
      "lblt_rate": "24.80"
    },
    {
      "stac_yymm": "202303",
      "grs": "-18.05",
      "bsop_prfi_inrt": "-95.47",
      "ntin_inrt": "-86.10",
      "roe_val": "1.61",
      "eps": "206.00",
      "sps": "37538",
      "bps": "51529.00",
      "rsrv_rate": "38898.83",
      "lblt_rate": "26.21"
    },
    {
      "stac_yymm": "202212",
      "grs": "8.09",
      "bsop_prfi_inrt": "-15.99",
      "ntin_inrt": "39.46",
      "roe_val": "17.07",
      "eps": "8057.00",
      "sps": "44494",
      "bps": "50817.00",
      "rsrv_rate": "38360.25",
      "lblt_rate": "26.41"
    },
    {
      "stac_yymm": "202209",
      "grs": "14.15",
      "bsop_prfi_inrt": "3.45",
      "ntin_inrt": "9.44",
      "roe_val": "13.18",
      "eps": "4597.00",
      "sps": "45494",
      "bps": "49387.00",
      "rsrv_rate": "37277.71",
      "lblt_rate": "36.35"
    },
    {
      "stac_yymm": "202206",
      "grs": "20.09",
      "bsop_prfi_inrt": "28.56",
      "ntin_inrt": "33.66",
      "roe_val": "14.36",
      "eps": "3251.00",
      "sps": "45633",
      "bps": "46937.00",
      "rsrv_rate": "35423.75",
      "lblt_rate": "36.64"
    },
    {
      "stac_yymm": "202203",
      "grs": "18.95",
      "bsop_prfi_inrt": "50.50",
      "ntin_inrt": "58.57",
      "roe_val": "14.77",
      "eps": "1638.00",
      "sps": "45803",
      "bps": "45106.00",
      "rsrv_rate": "34037.84",
      "lblt_rate": "39.34"
    },
    {
      "stac_yymm": "202112",
      "grs": "18.07",
      "bsop_prfi_inrt": "43.45",
      "ntin_inrt": "51.12",
      "roe_val": "13.92",
      "eps": "5777.00",
      "sps": "41163",
      "bps": "43611.00",
      "rsrv_rate": "32906.47",
      "lblt_rate": "39.92"
    },
    {
      "stac_yymm": "202109",
      "grs": "15.85",
      "bsop_prfi_inrt": "40.15",
      "ntin_inrt": "46.81",
      "roe_val": "13.72",
      "eps": "4211.00",
      "sps": "39855",
      "bps": "42447.00",
      "rsrv_rate": "32025.54",
      "lblt_rate": "38.30"
    },
    {
      "stac_yymm": "202106",
      "grs": "19.18",
      "bsop_prfi_inrt": "50.41",
      "ntin_inrt": "60.69",
      "roe_val": "12.21",
      "eps": "2435.00",
      "sps": "38000",
      "bps": "40361.00",
      "rsrv_rate": "30446.66",
      "lblt_rate": "36.29"
    },
    {
      "stac_yymm": "202103",
      "grs": "18.19",
      "bsop_prfi_inrt": "45.53",
      "ntin_inrt": "46.20",
      "roe_val": "10.64",
      "eps": "1044.00",
      "sps": "38505",
      "bps": "39126.00",
      "rsrv_rate": "29511.49",
      "lblt_rate": "43.23"
    },
    {
      "stac_yymm": "202012",
      "grs": "2.78",
      "bsop_prfi_inrt": "29.62",
      "ntin_inrt": "21.48",
      "roe_val": "9.99",
      "eps": "3841.00",
      "sps": "34862",
      "bps": "39406.00",
      "rsrv_rate": "29723.53",
      "lblt_rate": "37.07"
    },
    {
      "stac_yymm": "202009",
      "grs": "2.78",
      "bsop_prfi_inrt": "30.76",
      "ntin_inrt": "19.92",
      "roe_val": "10.02",
      "eps": "2892.00",
      "sps": "34401",
      "bps": "39446.00",
      "rsrv_rate": "29753.81",
      "lblt_rate": "36.09"
    },
    {
      "stac_yymm": "202006",
      "grs": "-0.20",
      "bsop_prfi_inrt": "13.74",
      "ntin_inrt": "2.11",
      "roe_val": "8.04",
      "eps": "1528.00",
      "sps": "31885",
      "bps": "38534.00",
      "rsrv_rate": "29063.37",
      "lblt_rate": "32.67"
    },
    {
      "stac_yymm": "202003",
      "grs": "5.61",
      "bsop_prfi_inrt": "3.43",
      "ntin_inrt": "-3.15",
      "roe_val": "7.62",
      "eps": "720.00",
      "sps": "32579",
      "bps": "38053.00",
      "rsrv_rate": "28699.75",
      "lblt_rate": "34.19"
    },
    {
      "stac_yymm": "201912",
      "grs": "-5.48",
      "bsop_prfi_inrt": "-52.84",
      "ntin_inrt": "-50.98",
      "roe_val": "8.69",
      "eps": "3166.00",
      "sps": "33919",
      "bps": "37528.00",
      "rsrv_rate": "28302.40",
      "lblt_rate": "34.12"
    },
    {
      "stac_yymm": "201909",
      "grs": "-7.58",
      "bsop_prfi_inrt": "-57.14",
      "ntin_inrt": "-53.98",
      "roe_val": "8.76",
      "eps": "2396.00",
      "sps": "33471",
      "bps": "37600.00",
      "rsrv_rate": "28356.77",
      "lblt_rate": "34.14"
    },
    {
      "stac_yymm": "201906",
      "grs": "-8.85",
      "bsop_prfi_inrt": "-57.95",
      "ntin_inrt": "-55.02",
      "roe_val": "8.30",
      "eps": "1498.00",
      "sps": "31950",
      "bps": "36789.00",
      "rsrv_rate": "27742.76",
      "lblt_rate": "33.05"
    },
    {
      "stac_yymm": "201903",
      "grs": "-13.50",
      "bsop_prfi_inrt": "-60.15",
      "ntin_inrt": "-56.85",
      "roe_val": "8.41",
      "eps": "752.00",
      "sps": "30848",
      "bps": "36142.00",
      "rsrv_rate": "27253.31",
      "lblt_rate": "36.27"
    },
    {
      "stac_yymm": "201812",
      "grs": "1.75",
      "bsop_prfi_inrt": "9.77",
      "ntin_inrt": "5.12",
      "roe_val": "19.63",
      "eps": "6024.00",
      "sps": "33458",
      "bps": "35342.00",
      "rsrv_rate": "26648.22",
      "lblt_rate": "36.97"
    },
    {
      "stac_yymm": "201809",
      "grs": "6.28",
      "bsop_prfi_inrt": "24.91",
      "ntin_inrt": "19.88",
      "roe_val": "21.47",
      "eps": "4853.00",
      "sps": "33572",
      "bps": "32685.00",
      "rsrv_rate": "26568.28",
      "lblt_rate": "39.28"
    },
    {
      "stac_yymm": "201806",
      "grs": "6.72",
      "bsop_prfi_inrt": "27.32",
      "ntin_inrt": "21.31",
      "roe_val": "20.88",
      "eps": "3082.00",
      "sps": "32482",
      "bps": "31483.00",
      "rsrv_rate": "25587.24",
      "lblt_rate": "36.70"
    },
    {
      "stac_yymm": "201803",
      "grs": "19.82",
      "bsop_prfi_inrt": "58.03",
      "ntin_inrt": "52.11",
      "roe_val": "21.96",
      "eps": "1583.00",
      "sps": "33017",
      "bps": "30146.00",
      "rsrv_rate": "24496.79",
      "lblt_rate": "39.96"
    },
    {
      "stac_yymm": "201712",
      "grs": "18.68",
      "bsop_prfi_inrt": "83.46",
      "ntin_inrt": "85.63",
      "roe_val": "21.01",
      "eps": "5421.00",
      "sps": "31414",
      "bps": "28971.00",
      "rsrv_rate": "23681.42",
      "lblt_rate": "40.68"
    },
    {
      "stac_yymm": "201709",
      "grs": "16.87",
      "bsop_prfi_inrt": "92.30",
      "ntin_inrt": "91.40",
      "roe_val": "20.06",
      "eps": "3804.00",
      "sps": "30021",
      "bps": "28305.00",
      "rsrv_rate": "23266.64",
      "lblt_rate": "40.76"
    },
    {
      "stac_yymm": "201706",
      "grs": "10.75",
      "bsop_prfi_inrt": "61.71",
      "ntin_inrt": "68.81",
      "roe_val": "19.25",
      "eps": "2328.00",
      "sps": "28399",
      "bps": "26828.00",
      "rsrv_rate": "22216.19",
      "lblt_rate": "38.31"
    },
    {
      "stac_yymm": "201703",
      "grs": "1.54",
      "bsop_prfi_inrt": "48.27",
      "ntin_inrt": "46.29",
      "roe_val": "16.21",
      "eps": "929.00",
      "sps": "25087",
      "bps": "24184.00",
      "rsrv_rate": "21617.29",
      "lblt_rate": "39.20"
    },
    {
      "stac_yymm": "201612",
      "grs": "0.60",
      "bsop_prfi_inrt": "10.70",
      "ntin_inrt": "19.23",
      "roe_val": "12.48",
      "eps": "2735.00",
      "sps": "24632",
      "bps": "24340.00",
      "rsrv_rate": "21757.56",
      "lblt_rate": "35.87"
    },
    {
      "stac_yymm": "201609",
      "grs": "0.81",
      "bsop_prfi_inrt": "-1.24",
      "ntin_inrt": "-1.25",
      "roe_val": "11.94",
      "eps": "1881.00",
      "sps": "24033",
      "bps": "22708.00",
      "rsrv_rate": "20291.88",
      "lblt_rate": "36.17"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```
