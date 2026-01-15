# NAV 비교추이(분)[v1_국내주식-070]

> [국내주식] 기본시세

NAV 비교추이(분) API입니다.
한국투자 HTS(eFriend Plus) > [0244] ETF/ETN 비교추이(NAV/IIV) 좌측 화면 "분별" 비교추이 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.
실전계좌의 경우, 한 번의 호출에 최근 30건까지 확인 가능합니다.


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `dd867a76-745d-4268-8ff8-b3e7f71e6e83` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/etfetn/v1/quotations/nav-comparison-time-trend` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `FHPST02440100` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-02-23
- **최종 수정일**: 2025-04-30

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials G... |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | FHPST02440100 |
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
| `fid_hour_cls_code` | FID 시간 구분 코드 | String | 5 | Y | 1분 :60, 3분: 180 … 120분:7200 |
| `fid_cond_mrkt_div_code` | FID 조건 시장 분류 코드 | String | 2 | Y | E - 고정값 |
| `fid_input_iscd` | FID 입력 종목코드 | String | 12 | Y | 종목코드 |

### 요청 예시

```json
{
  "fid_cond_mrkt_div_code": "E",
  "fid_input_iscd": "069500",
  "fid_hour_cls_code": "60"
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
| `output` | 응답상세 | Object |   | Y | array |
| `bsop_hour` | 영업 시간 | String | 6 | Y |  |
| `nav` | NAV | String | 112 | Y |  |
| `nav_prdy_vrss_sign` | NAV 전일 대비 부호 | String | 1 | Y |  |
| `nav_prdy_vrss` | NAV 전일 대비 | String | 112 | Y |  |
| `nav_prdy_ctrt` | NAV 전일 대비율 | String | 84 | Y |  |
| `nav_vrss_prpr` | NAV 대비 현재가 | String | 112 | Y |  |
| `dprt` | 괴리율 | String | 82 | Y |  |
| `stck_prpr` | 주식 현재가 | String | 10 | Y |  |
| `prdy_vrss` | 전일 대비 | String | 10 | Y |  |
| `prdy_vrss_sign` | 전일 대비 부호 | String | 1 | Y |  |
| `prdy_ctrt` | 전일 대비율 | String | 82 | Y |  |
| `acml_vol` | 누적 거래량 | String | 18 | Y |  |
| `cntg_vol` | 체결 거래량 | String | 18 | Y |  |

### 응답 예시

```json
{
  "output": [
    {
      "bsop_hour": "153000",
      "nav": "36127.30",
      "nav_prdy_vrss_sign": "2",
      "nav_prdy_vrss": "91.08",
      "nav_prdy_ctrt": "0.25",
      "nav_vrss_prpr": "-37.30",
      "dprt": "-0.10",
      "stck_prpr": "36090",
      "prdy_vrss": "110",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "0.31",
      "acml_vol": "3714732",
      "cntg_vol": "93993"
    },
    {
      "bsop_hour": "152900",
      "nav": "36170.22",
      "nav_prdy_vrss_sign": "2",
      "nav_prdy_vrss": "134.00",
      "nav_prdy_ctrt": "0.37",
      "nav_vrss_prpr": "-60.22",
      "dprt": "-0.17",
      "stck_prpr": "36110",
      "prdy_vrss": "130",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "0.36",
      "acml_vol": "3620739",
      "cntg_vol": "46"
    },
    {
      "bsop_hour": "152800",
      "nav": "36170.22",
      "nav_prdy_vrss_sign": "2",
      "nav_prdy_vrss": "134.00",
      "nav_prdy_ctrt": "0.37",
      "nav_vrss_prpr": "-60.22",
      "dprt": "-0.17",
      "stck_prpr": "36110",
      "prdy_vrss": "130",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "0.36",
      "acml_vol": "3620739",
      "cntg_vol": "46"
    },
    {
      "bsop_hour": "152700",
      "nav": "36170.22",
      "nav_prdy_vrss_sign": "2",
      "nav_prdy_vrss": "134.00",
      "nav_prdy_ctrt": "0.37",
      "nav_vrss_prpr": "-60.22",
      "dprt": "-0.17",
      "stck_prpr": "36110",
      "prdy_vrss": "130",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "0.36",
      "acml_vol": "3620739",
      "cntg_vol": "46"
    },
    {
      "bsop_hour": "152600",
      "nav": "36170.22",
      "nav_prdy_vrss_sign": "2",
      "nav_prdy_vrss": "134.00",
      "nav_prdy_ctrt": "0.37",
      "nav_vrss_prpr": "-60.22",
      "dprt": "-0.17",
      "stck_prpr": "36110",
      "prdy_vrss": "130",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "0.36",
      "acml_vol": "3620739",
      "cntg_vol": "46"
    },
    {
      "bsop_hour": "152500",
      "nav": "36170.22",
      "nav_prdy_vrss_sign": "2",
      "nav_prdy_vrss": "134.00",
      "nav_prdy_ctrt": "0.37",
      "nav_vrss_prpr": "-60.22",
      "dprt": "-0.17",
      "stck_prpr": "36110",
      "prdy_vrss": "130",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "0.36",
      "acml_vol": "3620739",
      "cntg_vol": "46"
    },
    {
      "bsop_hour": "152400",
      "nav": "36170.22",
      "nav_prdy_vrss_sign": "2",
      "nav_prdy_vrss": "134.00",
      "nav_prdy_ctrt": "0.37",
      "nav_vrss_prpr": "-60.22",
      "dprt": "-0.17",
      "stck_prpr": "36110",
      "prdy_vrss": "130",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "0.36",
      "acml_vol": "3620739",
      "cntg_vol": "46"
    },
    {
      "bsop_hour": "152300",
      "nav": "36170.22",
      "nav_prdy_vrss_sign": "2",
      "nav_prdy_vrss": "134.00",
      "nav_prdy_ctrt": "0.37",
      "nav_vrss_prpr": "-60.22",
      "dprt": "-0.17",
      "stck_prpr": "36110",
      "prdy_vrss": "130",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "0.36",
      "acml_vol": "3620739",
      "cntg_vol": "46"
    },
    {
      "bsop_hour": "152200",
      "nav": "36170.22",
      "nav_prdy_vrss_sign": "2",
      "nav_prdy_vrss": "134.00",
      "nav_prdy_ctrt": "0.37",
      "nav_vrss_prpr": "-60.22",
      "dprt": "-0.17",
      "stck_prpr": "36110",
      "prdy_vrss": "130",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "0.36",
      "acml_vol": "3620739",
      "cntg_vol": "46"
    },
    {
      "bsop_hour": "152100",
      "nav": "36170.22",
      "nav_prdy_vrss_sign": "2",
      "nav_prdy_vrss": "134.00",
      "nav_prdy_ctrt": "0.37",
      "nav_vrss_prpr": "-60.22",
      "dprt": "-0.17",
      "stck_prpr": "36110",
      "prdy_vrss": "130",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "0.36",
      "acml_vol": "3620739",
      "cntg_vol": "46"
    },
    {
      "bsop_hour": "152000",
      "nav": "36170.22",
      "nav_prdy_vrss_sign": "2",
      "nav_prdy_vrss": "134.00",
      "nav_prdy_ctrt": "0.37",
      "nav_vrss_prpr": "-60.22",
      "dprt": "-0.17",
      "stck_prpr": "36110",
      "prdy_vrss": "130",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "0.36",
      "acml_vol": "3620739",
      "cntg_vol": "46"
    },
    {
      "bsop_hour": "151900",
      "nav": "36160.15",
      "nav_prdy_vrss_sign": "2",
      "nav_prdy_vrss": "123.93",
      "nav_prdy_ctrt": "0.34",
      "nav_vrss_prpr": "-50.15",
      "dprt": "-0.14",
      "stck_prpr": "36110",
      "prdy_vrss": "130",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "0.36",
      "acml_vol": "3620739",
      "cntg_vol": "46"
    },
    {
      "bsop_hour": "151800",
      "nav": "36166.66",
      "nav_prdy_vrss_sign": "2",
      "nav_prdy_vrss": "130.44",
      "nav_prdy_ctrt": "0.36",
      "nav_vrss_prpr": "-51.66",
      "dprt": "-0.14",
      "stck_prpr": "36115",
      "prdy_vrss": "135",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "0.38",
      "acml_vol": "3600900",
      "cntg_vol": "67"
    },
    {
      "bsop_hour": "151700",
      "nav": "36138.90",
      "nav_prdy_vrss_sign": "2",
      "nav_prdy_vrss": "102.68",
      "nav_prdy_ctrt": "0.28",
      "nav_vrss_prpr": "-28.90",
      "dprt": "-0.08",
      "stck_prpr": "36110",
      "prdy_vrss": "130",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "0.36",
      "acml_vol": "3574190",
      "cntg_vol": "100"
    },
    {
      "bsop_hour": "151600",
      "nav": "36151.53",
      "nav_prdy_vrss_sign": "2",
      "nav_prdy_vrss": "115.31",
      "nav_prdy_ctrt": "0.32",
      "nav_vrss_prpr": "-36.53",
      "dprt": "-0.10",
      "stck_prpr": "36115",
      "prdy_vrss": "135",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "0.38",
      "acml_vol": "3566213",
      "cntg_vol": "127"
    },
    {
      "bsop_hour": "151500",
      "nav": "36148.81",
      "nav_prdy_vrss_sign": "2",
      "nav_prdy_vrss": "112.59",
      "nav_prdy_ctrt": "0.31",
      "nav_vrss_prpr": "-38.81",
      "dprt": "-0.11",
      "stck_prpr": "36110",
      "prdy_vrss": "130",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "0.36",
      "acml_vol": "3561650",
      "cntg_vol": "1"
    },
    {
      "bsop_hour": "151400",
      "nav": "36144.32",
      "nav_prdy_vrss_sign": "2",
      "nav_prdy_vrss": "108.10",
      "nav_prdy_ctrt": "0.30",
      "nav_vrss_prpr": "-34.32",
      "dprt": "-0.09",
      "stck_prpr": "36110",
      "prdy_vrss": "130",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "0.36",
      "acml_vol": "3554609",
      "cntg_vol": "20"
    },
    {
      "bsop_hour": "151300",
      "nav": "36153.81",
      "nav_prdy_vrss_sign": "2",
      "nav_prdy_vrss": "117.59",
      "nav_prdy_ctrt": "0.33",
      "nav_vrss_prpr": "-38.81",
      "dprt": "-0.11",
      "stck_prpr": "36115",
      "prdy_vrss": "135",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "0.38",
      "acml_vol": "3548014",
      "cntg_vol": "17"
    },
    {
      "bsop_hour": "151200",
      "nav": "36146.99",
      "nav_prdy_vrss_sign": "2",
      "nav_prdy_vrss": "110.77",
      "nav_prdy_ctrt": "0.31",
      "nav_vrss_prpr": "-36.99",
      "dprt": "-0.10",
      "stck_prpr": "36110",
      "prdy_vrss": "130",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "0.36",
      "acml_vol": "3531673",
      "cntg_vol": "5000"
    },
    {
      "bsop_hour": "151100",
      "nav": "36134.21",
      "nav_prdy_vrss_sign": "2",
      "nav_prdy_vrss": "97.99",
      "nav_prdy_ctrt": "0.27",
      "nav_vrss_prpr": "-34.21",
      "dprt": "-0.09",
      "stck_prpr": "36100",
      "prdy_vrss": "120",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "0.33",
      "acml_vol": "3508924",
      "cntg_vol": "1"
    },
    {
      "bsop_hour": "151000",
      "nav": "36125.95",
      "nav_prdy_vrss_sign": "2",
      "nav_prdy_vrss": "89.73",
      "nav_prdy_ctrt": "0.25",
      "nav_vrss_prpr": "-30.95",
      "dprt": "-0.09",
      "stck_prpr": "36095",
      "prdy_vrss": "115",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "0.32",
      "acml_vol": "3497610",
      "cntg_vol": "107"
    },
    {
      "bsop_hour": "150900",
      "nav": "36140.40",
      "nav_prdy_vrss_sign": "2",
      "nav_prdy_vrss": "104.18",
      "nav_prdy_ctrt": "0.29",
      "nav_vrss_prpr": "-40.40",
      "dprt": "-0.11",
      "stck_prpr": "36100",
      "prdy_vrss": "120",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "0.33",
      "acml_vol": "3465289",
      "cntg_vol": "1"
    },
    {
      "bsop_hour": "150800",
      "nav": "36142.41",
      "nav_prdy_vrss_sign": "2",
      "nav_prdy_vrss": "106.19",
      "nav_prdy_ctrt": "0.29",
      "nav_vrss_prpr": "-52.41",
      "dprt": "-0.15",
      "stck_prpr": "36090",
      "prdy_vrss": "110",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "0.31",
      "acml_vol": "3455837",
      "cntg_vol": "2"
    },
    {
      "bsop_hour": "150700",
      "nav": "36128.14",
      "nav_prdy_vrss_sign": "2",
      "nav_prdy_vrss": "91.92",
      "nav_prdy_ctrt": "0.25",
      "nav_vrss_prpr": "-38.14",
      "dprt": "-0.11",
      "stck_prpr": "36090",
      "prdy_vrss": "110",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "0.31",
      "acml_vol": "3443292",
      "cntg_vol": "6"
    },
    {
      "bsop_hour": "150600",
      "nav": "36143.67",
      "nav_prdy_vrss_sign": "2",
      "nav_prdy_vrss": "107.45",
      "nav_prdy_ctrt": "0.30",
      "nav_vrss_prpr": "-43.67",
      "dprt": "-0.12",
      "stck_prpr": "36100",
      "prdy_vrss": "120",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "0.33",
      "acml_vol": "3438545",
      "cntg_vol": "38"
    },
    {
      "bsop_hour": "150500",
      "nav": "36149.19",
      "nav_prdy_vrss_sign": "2",
      "nav_prdy_vrss": "112.97",
      "nav_prdy_ctrt": "0.31",
      "nav_vrss_prpr": "-49.19",
      "dprt": "-0.14",
      "stck_prpr": "36100",
      "prdy_vrss": "120",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "0.33",
      "acml_vol": "3429629",
      "cntg_vol": "1"
    },
    {
      "bsop_hour": "150400",
      "nav": "36144.80",
      "nav_prdy_vrss_sign": "2",
      "nav_prdy_vrss": "108.58",
      "nav_prdy_ctrt": "0.30",
      "nav_vrss_prpr": "-34.80",
      "dprt": "-0.11",
      "stck_prpr": "36110",
      "prdy_vrss": "125",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "0.35",
      "acml_vol": "3425274",
      "cntg_vol": "50"
    },
    {
      "bsop_hour": "150300",
      "nav": "36152.94",
      "nav_prdy_vrss_sign": "2",
      "nav_prdy_vrss": "116.72",
      "nav_prdy_ctrt": "0.32",
      "nav_vrss_prpr": "-42.94",
      "dprt": "-0.12",
      "stck_prpr": "36110",
      "prdy_vrss": "130",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "0.36",
      "acml_vol": "3417931",
      "cntg_vol": "10"
    },
    {
      "bsop_hour": "150200",
      "nav": "36152.33",
      "nav_prdy_vrss_sign": "2",
      "nav_prdy_vrss": "116.11",
      "nav_prdy_ctrt": "0.32",
      "nav_vrss_prpr": "-37.33",
      "dprt": "-0.08",
      "stck_prpr": "36115",
      "prdy_vrss": "145",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "0.40",
      "acml_vol": "3410977",
      "cntg_vol": "276"
    },
    {
      "bsop_hour": "150100",
      "nav": "36156.58",
      "nav_prdy_vrss_sign": "2",
      "nav_prdy_vrss": "120.36",
      "nav_prdy_ctrt": "0.33",
      "nav_vrss_prpr": "-46.58",
      "dprt": "-0.13",
      "stck_prpr": "36110",
      "prdy_vrss": "130",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "0.36",
      "acml_vol": "3400392",
      "cntg_vol": "5"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```

