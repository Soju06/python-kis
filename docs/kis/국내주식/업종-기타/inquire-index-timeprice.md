# 국내업종 시간별지수(분)[국내주식-119]

> [국내주식] 업종/기타

국내업종 시간별지수(분) API입니다. 
한국투자 HTS(eFriend Plus) > [0211] 업종 시간별지수 화면에서 우측 '1분' 선택 시의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `1d150774-eafa-49f8-9e77-67099bc28771` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/quotations/inquire-index-timeprice` |
| **Content-Type** | `` |
| **요청 포맷** | `` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `미지원` |
| **TR ID** | `FHPUP02110200`, `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-03-27
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
| `tr_id` | 거래ID | String | 13 | Y | FHPUP02110200 |
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
| `FID_INPUT_HOUR_1` | ?입력 시간1 | String | 10 | Y | 초단위, 60(1분), 300(5분), 600(10분) |
| `FID_INPUT_ISCD` | 입력 종목코드 | String | 12 | Y | 0001:거래소, 1001:코스닥, 2001:코스피200, 3003:KSQ150 |
| `FID_COND_MRKT_DIV_CODE` | 조건 시장 분류 코드 | String | 2 | Y | 시장구분코드 (업종 U) |

### 요청 예시

```json
fid_cond_mrkt_div_code:U
fid_input_iscd:1001
fid_input_hour_1:120
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
| `bsop_hour` | 영업 시간 | String | 6 | Y |  |
| `bstp_nmix_prpr` | 업종 지수 현재가 | String | 112 | Y |  |
| `bstp_nmix_prdy_vrss` | 업종 지수 전일 대비 | String | 112 | Y |  |
| `prdy_vrss_sign` | 전일 대비 부호 | String | 1 | Y |  |
| `bstp_nmix_prdy_ctrt` | 업종 지수 전일 대비율 | String | 82 | Y |  |
| `acml_tr_pbmn` | 누적 거래 대금 | String | 18 | Y |  |
| `acml_vol` | 누적 거래량 | String | 18 | Y |  |
| `cntg_vol` | 체결 거래량 | String | 18 | Y |  |

### 응답 예시

```json
{
  "output": [
    {
      "bsop_hour": "100600",
      "bstp_nmix_prpr": "916.77",
      "bstp_nmix_prdy_vrss": "11.27",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.24",
      "acml_tr_pbmn": "3839797",
      "acml_vol": "313374",
      "cntg_vol": "870"
    },
    {
      "bsop_hour": "100400",
      "bstp_nmix_prpr": "916.65",
      "bstp_nmix_prdy_vrss": "11.15",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.23",
      "acml_tr_pbmn": "3829216",
      "acml_vol": "312504",
      "cntg_vol": "4352"
    },
    {
      "bsop_hour": "100200",
      "bstp_nmix_prpr": "916.69",
      "bstp_nmix_prdy_vrss": "11.19",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.24",
      "acml_tr_pbmn": "3779730",
      "acml_vol": "308152",
      "cntg_vol": "4959"
    },
    {
      "bsop_hour": "100000",
      "bstp_nmix_prpr": "916.76",
      "bstp_nmix_prdy_vrss": "11.26",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.24",
      "acml_tr_pbmn": "3716791",
      "acml_vol": "303193",
      "cntg_vol": "5103"
    },
    {
      "bsop_hour": "095800",
      "bstp_nmix_prpr": "916.60",
      "bstp_nmix_prdy_vrss": "11.10",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.23",
      "acml_tr_pbmn": "3651490",
      "acml_vol": "298090",
      "cntg_vol": "5732"
    },
    {
      "bsop_hour": "095600",
      "bstp_nmix_prpr": "917.37",
      "bstp_nmix_prdy_vrss": "11.87",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.31",
      "acml_tr_pbmn": "3588380",
      "acml_vol": "292358",
      "cntg_vol": "5331"
    },
    {
      "bsop_hour": "095400",
      "bstp_nmix_prpr": "917.64",
      "bstp_nmix_prdy_vrss": "12.14",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.34",
      "acml_tr_pbmn": "3521010",
      "acml_vol": "287027",
      "cntg_vol": "6827"
    },
    {
      "bsop_hour": "095200",
      "bstp_nmix_prpr": "916.31",
      "bstp_nmix_prdy_vrss": "10.81",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.19",
      "acml_tr_pbmn": "3445942",
      "acml_vol": "280200",
      "cntg_vol": "7263"
    },
    {
      "bsop_hour": "095000",
      "bstp_nmix_prpr": "916.94",
      "bstp_nmix_prdy_vrss": "11.44",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.26",
      "acml_tr_pbmn": "3373037",
      "acml_vol": "272937",
      "cntg_vol": "5040"
    },
    {
      "bsop_hour": "094800",
      "bstp_nmix_prpr": "916.82",
      "bstp_nmix_prdy_vrss": "11.32",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.25",
      "acml_tr_pbmn": "3304716",
      "acml_vol": "267897",
      "cntg_vol": "6828"
    },
    {
      "bsop_hour": "094600",
      "bstp_nmix_prpr": "916.74",
      "bstp_nmix_prdy_vrss": "11.24",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.24",
      "acml_tr_pbmn": "3222590",
      "acml_vol": "261069",
      "cntg_vol": "8510"
    },
    {
      "bsop_hour": "094400",
      "bstp_nmix_prpr": "914.70",
      "bstp_nmix_prdy_vrss": "9.20",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.02",
      "acml_tr_pbmn": "3137995",
      "acml_vol": "252559",
      "cntg_vol": "6781"
    },
    {
      "bsop_hour": "094200",
      "bstp_nmix_prpr": "914.33",
      "bstp_nmix_prdy_vrss": "8.83",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "0.98",
      "acml_tr_pbmn": "3073035",
      "acml_vol": "245778",
      "cntg_vol": "7274"
    },
    {
      "bsop_hour": "094000",
      "bstp_nmix_prpr": "914.00",
      "bstp_nmix_prdy_vrss": "8.50",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "0.94",
      "acml_tr_pbmn": "3001499",
      "acml_vol": "238504",
      "cntg_vol": "7439"
    },
    {
      "bsop_hour": "093800",
      "bstp_nmix_prpr": "913.15",
      "bstp_nmix_prdy_vrss": "7.65",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "0.84",
      "acml_tr_pbmn": "2908979",
      "acml_vol": "231065",
      "cntg_vol": "8180"
    },
    {
      "bsop_hour": "093600",
      "bstp_nmix_prpr": "912.23",
      "bstp_nmix_prdy_vrss": "6.73",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "0.74",
      "acml_tr_pbmn": "2815470",
      "acml_vol": "222885",
      "cntg_vol": "7271"
    },
    {
      "bsop_hour": "093400",
      "bstp_nmix_prpr": "911.14",
      "bstp_nmix_prdy_vrss": "5.64",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "0.62",
      "acml_tr_pbmn": "2729472",
      "acml_vol": "215614",
      "cntg_vol": "6032"
    },
    {
      "bsop_hour": "093200",
      "bstp_nmix_prpr": "911.12",
      "bstp_nmix_prdy_vrss": "5.62",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "0.62",
      "acml_tr_pbmn": "2640030",
      "acml_vol": "209582",
      "cntg_vol": "7254"
    },
    {
      "bsop_hour": "093000",
      "bstp_nmix_prpr": "910.35",
      "bstp_nmix_prdy_vrss": "4.85",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "0.54",
      "acml_tr_pbmn": "2542281",
      "acml_vol": "202328",
      "cntg_vol": "7789"
    },
    {
      "bsop_hour": "092800",
      "bstp_nmix_prpr": "911.05",
      "bstp_nmix_prdy_vrss": "5.55",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "0.61",
      "acml_tr_pbmn": "2420975",
      "acml_vol": "194539",
      "cntg_vol": "8109"
    },
    {
      "bsop_hour": "092600",
      "bstp_nmix_prpr": "911.91",
      "bstp_nmix_prdy_vrss": "6.41",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "0.71",
      "acml_tr_pbmn": "2312684",
      "acml_vol": "186430",
      "cntg_vol": "8233"
    },
    {
      "bsop_hour": "092400",
      "bstp_nmix_prpr": "912.18",
      "bstp_nmix_prdy_vrss": "6.68",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "0.74",
      "acml_tr_pbmn": "2210228",
      "acml_vol": "178197",
      "cntg_vol": "8295"
    },
    {
      "bsop_hour": "092200",
      "bstp_nmix_prpr": "912.13",
      "bstp_nmix_prdy_vrss": "6.63",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "0.73",
      "acml_tr_pbmn": "2106912",
      "acml_vol": "169902",
      "cntg_vol": "9285"
    },
    {
      "bsop_hour": "092000",
      "bstp_nmix_prpr": "910.92",
      "bstp_nmix_prdy_vrss": "5.42",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "0.60",
      "acml_tr_pbmn": "1980631",
      "acml_vol": "160617",
      "cntg_vol": "10198"
    },
    {
      "bsop_hour": "091800",
      "bstp_nmix_prpr": "910.87",
      "bstp_nmix_prdy_vrss": "5.37",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "0.59",
      "acml_tr_pbmn": "1836549",
      "acml_vol": "150419",
      "cntg_vol": "10738"
    },
    {
      "bsop_hour": "091600",
      "bstp_nmix_prpr": "910.99",
      "bstp_nmix_prdy_vrss": "5.49",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "0.61",
      "acml_tr_pbmn": "1700334",
      "acml_vol": "139681",
      "cntg_vol": "11517"
    },
    {
      "bsop_hour": "091400",
      "bstp_nmix_prpr": "909.83",
      "bstp_nmix_prdy_vrss": "4.33",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "0.48",
      "acml_tr_pbmn": "1572262",
      "acml_vol": "128164",
      "cntg_vol": "12918"
    },
    {
      "bsop_hour": "091200",
      "bstp_nmix_prpr": "909.84",
      "bstp_nmix_prdy_vrss": "4.34",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "0.48",
      "acml_tr_pbmn": "1430578",
      "acml_vol": "115246",
      "cntg_vol": "12623"
    },
    {
      "bsop_hour": "091000",
      "bstp_nmix_prpr": "910.28",
      "bstp_nmix_prdy_vrss": "4.78",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "0.53",
      "acml_tr_pbmn": "1296270",
      "acml_vol": "102623",
      "cntg_vol": "14403"
    },
    {
      "bsop_hour": "090800",
      "bstp_nmix_prpr": "909.65",
      "bstp_nmix_prdy_vrss": "4.15",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "0.46",
      "acml_tr_pbmn": "1143581",
      "acml_vol": "88220",
      "cntg_vol": "11854"
    },
    {
      "bsop_hour": "090600",
      "bstp_nmix_prpr": "909.95",
      "bstp_nmix_prdy_vrss": "4.45",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "0.49",
      "acml_tr_pbmn": "980294",
      "acml_vol": "76366",
      "cntg_vol": "12512"
    },
    {
      "bsop_hour": "090400",
      "bstp_nmix_prpr": "909.15",
      "bstp_nmix_prdy_vrss": "3.65",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "0.40",
      "acml_tr_pbmn": "805755",
      "acml_vol": "63854",
      "cntg_vol": "14223"
    },
    {
      "bsop_hour": "090200",
      "bstp_nmix_prpr": "908.43",
      "bstp_nmix_prdy_vrss": "2.93",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "0.32",
      "acml_tr_pbmn": "606769",
      "acml_vol": "49631",
      "cntg_vol": "21310"
    },
    {
      "bsop_hour": "090000",
      "bstp_nmix_prpr": "910.96",
      "bstp_nmix_prdy_vrss": "5.46",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "0.60",
      "acml_tr_pbmn": "347460",
      "acml_vol": "28321",
      "cntg_vol": "28321"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```
