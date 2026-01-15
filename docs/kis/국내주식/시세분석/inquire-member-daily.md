# 주식현재가 회원사 종목매매동향 [국내주식-197]

> [국내주식] 시세분석

주식현재가 회원사 종목매매동향 API입니다.
한국투자 HTS(eFriend Plus) > [0454] 증권사 종목매매동향 화면을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `50775574-8832-4db8-aeb5-51a32c8250ed` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/quotations/inquire-member-daily` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `미지원` |
| **TR ID (실전)** | `FHPST04540000` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-05-24
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
| `tr_id` | 거래ID | String | 13 | Y | FHPST04540000 |
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
| `FID_COND_MRKT_DIV_CODE` | 조건시장분류코드 | String | 2 | Y | J: KRX, NX: NXT, UN: 통합 |
| `FID_INPUT_ISCD` | 입력종목코드 | String | 12 | Y | 주식종목코드입력 |
| `FID_INPUT_ISCD_2` | 회원사코드 | String | 8 | Y | 회원사코드 (kis developers 포탈 사이트 포럼-> FAQ -> 종목정보 다운로드(국내) > 회원사 참조) |
| `FID_INPUT_DATE_1` | 입력날짜1 | String | 10 | Y | 날짜 ~ |
| `FID_INPUT_DATE_2` | 입력날짜2 | String | 10 | Y | ~ 날짜 |
| `FID_SCTN_CLS_CODE` | 구간구분코드 | String | 2 | Y | 공백 |

### 요청 예시

```json
FID_COND_MRKT_DIV_CODE:J
FID_INPUT_ISCD:136480
FID_INPUT_ISCD_2:00003
FID_INPUT_DATE_1:20240501
FID_INPUT_DATE_2:20240530
FID_SCTN_CLS_CODE:
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
| `output` | 응답상세 | Object |   | Y | array |
| `stck_bsop_date` | 주식영업일자 | String | 8 | Y |  |
| `total_seln_qty` | 총매도수량 | String | 18 | Y |  |
| `total_shnu_qty` | 총매수2수량 | String | 18 | Y |  |
| `ntby_qty` | 순매수수량 | String | 18 | Y |  |
| `stck_prpr` | 주식현재가 | String | 10 | Y |  |
| `prdy_vrss` | 전일대비 | String | 10 | Y |  |
| `prdy_vrss_sign` | 전일대비부호 | String | 1 | Y |  |
| `prdy_ctrt` | 전일대비율 | String | 82 | Y |  |
| `acml_vol` | 누적거래량 | String | 18 | Y |  |

### 응답 예시

```json
{
  "output": [
    {
      "stck_bsop_date": "20240530",
      "total_seln_qty": "55432",
      "total_shnu_qty": "81112",
      "ntby_qty": "25680",
      "stck_prpr": "3240",
      "prdy_vrss": "-65",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-1.97",
      "acml_vol": "862835"
    },
    {
      "stck_bsop_date": "20240529",
      "total_seln_qty": "53901",
      "total_shnu_qty": "130678",
      "ntby_qty": "76777",
      "stck_prpr": "3305",
      "prdy_vrss": "-30",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-0.90",
      "acml_vol": "974060"
    },
    {
      "stck_bsop_date": "20240528",
      "total_seln_qty": "139470",
      "total_shnu_qty": "209017",
      "ntby_qty": "69547",
      "stck_prpr": "3335",
      "prdy_vrss": "-30",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-0.89",
      "acml_vol": "1553914"
    },
    {
      "stck_bsop_date": "20240527",
      "total_seln_qty": "239813",
      "total_shnu_qty": "246930",
      "ntby_qty": "7117",
      "stck_prpr": "3365",
      "prdy_vrss": "-30",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-0.88",
      "acml_vol": "1750949"
    },
    {
      "stck_bsop_date": "20240524",
      "total_seln_qty": "1451049",
      "total_shnu_qty": "1526087",
      "ntby_qty": "75038",
      "stck_prpr": "3395",
      "prdy_vrss": "110",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "3.35",
      "acml_vol": "11758204"
    },
    {
      "stck_bsop_date": "20240523",
      "total_seln_qty": "120530",
      "total_shnu_qty": "159459",
      "ntby_qty": "38929",
      "stck_prpr": "3285",
      "prdy_vrss": "-40",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-1.20",
      "acml_vol": "1532424"
    },
    {
      "stck_bsop_date": "20240522",
      "total_seln_qty": "290601",
      "total_shnu_qty": "292948",
      "ntby_qty": "2347",
      "stck_prpr": "3325",
      "prdy_vrss": "60",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "1.84",
      "acml_vol": "2579194"
    },
    {
      "stck_bsop_date": "20240521",
      "total_seln_qty": "118718",
      "total_shnu_qty": "75046",
      "ntby_qty": "-43672",
      "stck_prpr": "3265",
      "prdy_vrss": "20",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "0.62",
      "acml_vol": "979173"
    },
    {
      "stck_bsop_date": "20240520",
      "total_seln_qty": "400866",
      "total_shnu_qty": "290925",
      "ntby_qty": "-109941",
      "stck_prpr": "3245",
      "prdy_vrss": "30",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "0.93",
      "acml_vol": "3346515"
    },
    {
      "stck_bsop_date": "20240517",
      "total_seln_qty": "316302",
      "total_shnu_qty": "397728",
      "ntby_qty": "81426",
      "stck_prpr": "3215",
      "prdy_vrss": "60",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "1.90",
      "acml_vol": "3089567"
    },
    {
      "stck_bsop_date": "20240516",
      "total_seln_qty": "107617",
      "total_shnu_qty": "82162",
      "ntby_qty": "-25455",
      "stck_prpr": "3155",
      "prdy_vrss": "-30",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-0.94",
      "acml_vol": "767201"
    },
    {
      "stck_bsop_date": "20240514",
      "total_seln_qty": "59559",
      "total_shnu_qty": "57909",
      "ntby_qty": "-1650",
      "stck_prpr": "3185",
      "prdy_vrss": "45",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "1.43",
      "acml_vol": "667569"
    },
    {
      "stck_bsop_date": "20240513",
      "total_seln_qty": "70787",
      "total_shnu_qty": "91304",
      "ntby_qty": "20517",
      "stck_prpr": "3140",
      "prdy_vrss": "-50",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-1.57",
      "acml_vol": "1291905"
    },
    {
      "stck_bsop_date": "20240510",
      "total_seln_qty": "227523",
      "total_shnu_qty": "160715",
      "ntby_qty": "-66808",
      "stck_prpr": "3190",
      "prdy_vrss": "45",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "1.43",
      "acml_vol": "1841506"
    },
    {
      "stck_bsop_date": "20240509",
      "total_seln_qty": "331604",
      "total_shnu_qty": "160679",
      "ntby_qty": "-170925",
      "stck_prpr": "3145",
      "prdy_vrss": "-15",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-0.47",
      "acml_vol": "2145427"
    },
    {
      "stck_bsop_date": "20240508",
      "total_seln_qty": "158034",
      "total_shnu_qty": "154720",
      "ntby_qty": "-3314",
      "stck_prpr": "3160",
      "prdy_vrss": "100",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "3.27",
      "acml_vol": "1915227"
    },
    {
      "stck_bsop_date": "20240507",
      "total_seln_qty": "23239",
      "total_shnu_qty": "52555",
      "ntby_qty": "29316",
      "stck_prpr": "3060",
      "prdy_vrss": "-10",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-0.33",
      "acml_vol": "351326"
    },
    {
      "stck_bsop_date": "20240503",
      "total_seln_qty": "66664",
      "total_shnu_qty": "94801",
      "ntby_qty": "28137",
      "stck_prpr": "3070",
      "prdy_vrss": "-15",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-0.49",
      "acml_vol": "420729"
    },
    {
      "stck_bsop_date": "20240502",
      "total_seln_qty": "46034",
      "total_shnu_qty": "46915",
      "ntby_qty": "881",
      "stck_prpr": "3085",
      "prdy_vrss": "30",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "0.98",
      "acml_vol": "473617"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```

