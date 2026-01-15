# 종목별 일별 대차거래추이 [국내주식-135]

> [국내주식] 시세분석

종목별 일별 대차거래추이 API입니다.
한 번의 조회에 최대 100건까지 조회 가능하며, start_date, end_date 를 수정하여 다음 조회가 가능합니다.

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `3ed0247e-d717-43ed-85e9-51f952844687` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/quotations/daily-loan-trans` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `미지원` |
| **TR ID** | `모의투자 미지원`, `HHPST074500C0` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-05-03
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
| `tr_id` | 거래ID | String | 13 | Y | HHPST074500C0 |
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
| `MRKT_DIV_CLS_CODE` | 조회구분 | String | 1 | Y | 1(코스피), 2(코스닥), 3(종목) |
| `MKSC_SHRN_ISCD` | 종목코드 | String | 9 | Y | 종목코드 |
| `START_DATE` | 조회시작일시 | String | 8 | Y | 조회기간 ~ |
| `END_DATE` | 조회종료일시 | String | 8 | Y | ~ 조회기간 |
| `CTS` | 이전조회KEY | String | 8 | Y |  |

### 요청 예시

```json
mrkt_div_cls_code:1
mksc_shrn_iscd:005930
start_date:20240401
end_date:20240430
cts:
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
| `output1` | 응답상세 | Object |   | Y | array |
| `bsop_date` | 일자 | String | 8 | Y |  |
| `stck_prpr` | 주식 종가 | String | 10 | Y |  |
| `prdy_vrss_sign` | 전일 대비 부호 | String | 1 | Y |  |
| `prdy_vrss` | 전일 대비 | String | 10 | Y |  |
| `prdy_ctrt` | 전일 대비율 | String | 8 | Y |  |
| `acml_vol` | 누적 거래량 | String | 18 | Y |  |
| `new_stcn` | 당일 증가 주수 (체결) | String | 16 | Y |  |
| `rdmp_stcn` | 당일 감소 주수 (상환) | String | 16 | Y |  |
| `prdy_rmnd_vrss` | 대차거래 증감 | String | 16 | Y |  |
| `rmnd_stcn` | 당일 잔고 주수 | String | 16 | Y |  |
| `rmnd_amt` | 당일 잔고 금액 | String | 20 | Y |  |

### 응답 예시

```json
{
  "output2": [
    {
      "bsop_date": "20240430",
      "stck_prpr": "2692.06",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "4.62",
      "prdy_ctrt": "0.17",
      "acml_vol": "460083500",
      "new_stcn": "14379227",
      "rdmp_stcn": "13993603",
      "prdy_rmnd_vrss": "385624",
      "rmnd_stcn": "947521840",
      "rmnd_amt": "47504735"
    },
    {
      "bsop_date": "20240429",
      "stck_prpr": "2687.44",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "31.11",
      "prdy_ctrt": "1.17",
      "acml_vol": "470546000",
      "new_stcn": "6028334",
      "rdmp_stcn": "13437664",
      "prdy_rmnd_vrss": "-7409330",
      "rmnd_stcn": "947136216",
      "rmnd_amt": "47367356"
    },
    {
      "bsop_date": "20240426",
      "stck_prpr": "2656.33",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "27.71",
      "prdy_ctrt": "1.05",
      "acml_vol": "450520700",
      "new_stcn": "14406990",
      "rdmp_stcn": "12079739",
      "prdy_rmnd_vrss": "2327251",
      "rmnd_stcn": "954545546",
      "rmnd_amt": "46874865"
    },
    {
      "bsop_date": "20240425",
      "stck_prpr": "2628.62",
      "prdy_vrss_sign": "5",
      "prdy_vrss": "-47.13",
      "prdy_ctrt": "-1.76",
      "acml_vol": "334062400",
      "new_stcn": "4765719",
      "rdmp_stcn": "13112635",
      "prdy_rmnd_vrss": "-8346916",
      "rmnd_stcn": "952231269",
      "rmnd_amt": "46089010"
    },
    {
      "bsop_date": "20240424",
      "stck_prpr": "2675.75",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "52.73",
      "prdy_ctrt": "2.01",
      "acml_vol": "325739600",
      "new_stcn": "19649840",
      "rdmp_stcn": "8993910",
      "prdy_rmnd_vrss": "10655930",
      "rmnd_stcn": "960577194",
      "rmnd_amt": "47488544"
    },
    {
      "bsop_date": "20240423",
      "stck_prpr": "2623.02",
      "prdy_vrss_sign": "5",
      "prdy_vrss": "-6.42",
      "prdy_ctrt": "-0.24",
      "acml_vol": "430275800",
      "new_stcn": "7802761",
      "rdmp_stcn": "7414164",
      "prdy_rmnd_vrss": "388597",
      "rmnd_stcn": "949921264",
      "rmnd_amt": "46108475"
    },
    {
      "bsop_date": "20240422",
      "stck_prpr": "2629.44",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "37.58",
      "prdy_ctrt": "1.45",
      "acml_vol": "401892200",
      "new_stcn": "10841550",
      "rdmp_stcn": "18150018",
      "prdy_rmnd_vrss": "-7308468",
      "rmnd_stcn": "949532667",
      "rmnd_amt": "46211861"
    },
    {
      "bsop_date": "20240419",
      "stck_prpr": "2591.86",
      "prdy_vrss_sign": "5",
      "prdy_vrss": "-42.84",
      "prdy_ctrt": "-1.63",
      "acml_vol": "809473400",
      "new_stcn": "8657583",
      "rdmp_stcn": "12304586",
      "prdy_rmnd_vrss": "-3647003",
      "rmnd_stcn": "956841135",
      "rmnd_amt": "45225405"
    },
    {
      "bsop_date": "20240418",
      "stck_prpr": "2634.70",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "50.52",
      "prdy_ctrt": "1.95",
      "acml_vol": "478786200",
      "new_stcn": "13218317",
      "rdmp_stcn": "16631496",
      "prdy_rmnd_vrss": "-3413179",
      "rmnd_stcn": "960488138",
      "rmnd_amt": "46007513"
    },
    {
      "bsop_date": "20240417",
      "stck_prpr": "2584.18",
      "prdy_vrss_sign": "5",
      "prdy_vrss": "-25.45",
      "prdy_ctrt": "-0.98",
      "acml_vol": "414348100",
      "new_stcn": "13838612",
      "rdmp_stcn": "9001120",
      "prdy_rmnd_vrss": "4837492",
      "rmnd_stcn": "963901317",
      "rmnd_amt": "45199389"
    },
    {
      "bsop_date": "20240416",
      "stck_prpr": "2609.63",
      "prdy_vrss_sign": "5",
      "prdy_vrss": "-60.80",
      "prdy_ctrt": "-2.28",
      "acml_vol": "570212100",
      "new_stcn": "8029982",
      "rdmp_stcn": "9662633",
      "prdy_rmnd_vrss": "-1632651",
      "rmnd_stcn": "959063825",
      "rmnd_amt": "45461648"
    },
    {
      "bsop_date": "20240415",
      "stck_prpr": "2670.43",
      "prdy_vrss_sign": "5",
      "prdy_vrss": "-11.39",
      "prdy_ctrt": "-0.42",
      "acml_vol": "561950000",
      "new_stcn": "13418896",
      "rdmp_stcn": "9863897",
      "prdy_rmnd_vrss": "3554999",
      "rmnd_stcn": "960696476",
      "rmnd_amt": "46397052"
    },
    {
      "bsop_date": "20240412",
      "stck_prpr": "2681.82",
      "prdy_vrss_sign": "5",
      "prdy_vrss": "-25.14",
      "prdy_ctrt": "-0.93",
      "acml_vol": "514575300",
      "new_stcn": "16291814",
      "rdmp_stcn": "6220088",
      "prdy_rmnd_vrss": "10071726",
      "rmnd_stcn": "957141477",
      "rmnd_amt": "46559127"
    },
    {
      "bsop_date": "20240411",
      "stck_prpr": "2706.96",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "1.80",
      "prdy_ctrt": "0.07",
      "acml_vol": "561333400",
      "new_stcn": "14878420",
      "rdmp_stcn": "10305585",
      "prdy_rmnd_vrss": "4572835",
      "rmnd_stcn": "947069751",
      "rmnd_amt": "46395176"
    },
    {
      "bsop_date": "20240409",
      "stck_prpr": "2705.16",
      "prdy_vrss_sign": "5",
      "prdy_vrss": "-12.49",
      "prdy_ctrt": "-0.46",
      "acml_vol": "470183700",
      "new_stcn": "10784436",
      "rdmp_stcn": "6933242",
      "prdy_rmnd_vrss": "3851194",
      "rmnd_stcn": "942496916",
      "rmnd_amt": "46082940"
    },
    {
      "bsop_date": "20240408",
      "stck_prpr": "2717.65",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "3.44",
      "prdy_ctrt": "0.13",
      "acml_vol": "620652500",
      "new_stcn": "16939713",
      "rdmp_stcn": "12571632",
      "prdy_rmnd_vrss": "4368081",
      "rmnd_stcn": "938645722",
      "rmnd_amt": "46069590"
    },
    {
      "bsop_date": "20240405",
      "stck_prpr": "2714.21",
      "prdy_vrss_sign": "5",
      "prdy_vrss": "-27.79",
      "prdy_ctrt": "-1.01",
      "acml_vol": "621030600",
      "new_stcn": "5614441",
      "rdmp_stcn": "11701229",
      "prdy_rmnd_vrss": "-6086788",
      "rmnd_stcn": "934277641",
      "rmnd_amt": "45207497"
    },
    {
      "bsop_date": "20240404",
      "stck_prpr": "2742.00",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "35.03",
      "prdy_ctrt": "1.29",
      "acml_vol": "477952800",
      "new_stcn": "12221690",
      "rdmp_stcn": "5093795",
      "prdy_rmnd_vrss": "7127895",
      "rmnd_stcn": "940364429",
      "rmnd_amt": "45926211"
    },
    {
      "bsop_date": "20240403",
      "stck_prpr": "2706.97",
      "prdy_vrss_sign": "5",
      "prdy_vrss": "-46.19",
      "prdy_ctrt": "-1.68",
      "acml_vol": "640806300",
      "new_stcn": "14817975",
      "rdmp_stcn": "15348355",
      "prdy_rmnd_vrss": "-530380",
      "rmnd_stcn": "933236534",
      "rmnd_amt": "44837956"
    },
    {
      "bsop_date": "20240402",
      "stck_prpr": "2753.16",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "5.30",
      "prdy_ctrt": "0.19",
      "acml_vol": "630392900",
      "new_stcn": "12689747",
      "rdmp_stcn": "9723610",
      "prdy_rmnd_vrss": "2966137",
      "rmnd_stcn": "933766914",
      "rmnd_amt": "45180305"
    },
    {
      "bsop_date": "20240401",
      "stck_prpr": "2747.86",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "1.23",
      "prdy_ctrt": "0.04",
      "acml_vol": "397600500",
      "new_stcn": "8654205",
      "rdmp_stcn": "9951822",
      "prdy_rmnd_vrss": "-1297617",
      "rmnd_stcn": "930800777",
      "rmnd_amt": "45158153"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```
