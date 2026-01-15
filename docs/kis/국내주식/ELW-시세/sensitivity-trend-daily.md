# ELW 민감도 추이(일별) [국내주식-176]

> [국내주식] ELW 시세

ELW 민감도 추이(일별) API입니다.
한국투자 HTS(eFriend Plus) > [0283] ELW 민감도 추이 화면의 "일자별" 민감도추이 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `a64dc948-de6c-4e7a-988b-9769ac8fd5b2` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/elw/v1/quotations/sensitivity-trend-daily` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `미지원` |
| **TR ID (실전)** | `FHPEW02830200` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-05-03
- **최종 수정일**: 2025-05-07

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials G... |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | FHPEW02830200 |
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
| `FID_INPUT_ISCD` | 입력종목코드 | String | 12 | Y | ex)(58J438(KBJ438삼성전자풋) |

### 요청 예시

```json
FID_COND_MRKT_DIV_CODE:W
FID_INPUT_ISCD:57K281
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
| `elw_prpr` | ELW현재가 | String | 10 | Y |  |
| `prdy_vrss` | 전일대비 | String | 10 | Y |  |
| `prdy_vrss_sign` | 전일대비부호 | String | 1 | Y |  |
| `prdy_ctrt` | 전일대비율 | String | 82 | Y |  |
| `hts_thpr` | HTS이론가 | String | 112 | Y |  |
| `delta_val` | 델타값 | String | 114 | Y |  |
| `gama` | 감마 | String | 84 | Y |  |
| `theta` | 세타 | String | 84 | Y |  |
| `vega` | 베가 | String | 84 | Y |  |
| `rho` | 로우 | String | 84 | Y |  |

### 응답 예시

```json
{
    "output": [
        {
            "stck_bsop_date": "20240507",
            "elw_prpr": "25",
            "prdy_vrss": "-20",
            "prdy_vrss_sign": "5",
            "prdy_ctrt": "-44.44",
            "hts_thpr": "20.39",
            "delta_val": "-0.4034",
            "gama": "0.0000",
            "theta": "0.5843",
            "vega": "0.9954",
            "rho": "-0.3529"
        },
        {
            "stck_bsop_date": "20240503",
            "elw_prpr": "45",
            "prdy_vrss": "0",
            "prdy_vrss_sign": "3",
            "prdy_ctrt": "0.00",
            "hts_thpr": "39.43",
            "delta_val": "-0.5792",
            "gama": "0.0000",
            "theta": "0.5531",
            "vega": "0.9786",
            "rho": "-0.5143"
        },
        {
            "stck_bsop_date": "20240502",
            "elw_prpr": "45",
            "prdy_vrss": "0",
            "prdy_vrss_sign": "3",
            "prdy_ctrt": "0.00",
            "hts_thpr": "37.16",
            "delta_val": "-0.5529",
            "gama": "0.0000",
            "theta": "0.5859",
            "vega": "1.0136",
            "rho": "-0.5143"
        },
        {
            "stck_bsop_date": "20240430",
            "elw_prpr": "45",
            "prdy_vrss": "-5",
            "prdy_vrss_sign": "5",
            "prdy_ctrt": "-10.00",
            "hts_thpr": "39.30",
            "delta_val": "-0.5847",
            "gama": "0.0000",
            "theta": "0.4979",
            "vega": "1.0113",
            "rho": "-0.5579"
        },
        {
            "stck_bsop_date": "20240429",
            "elw_prpr": "50",
            "prdy_vrss": "0",
            "prdy_vrss_sign": "3",
            "prdy_ctrt": "0.00",
            "hts_thpr": "44.66",
            "delta_val": "-0.6211",
            "gama": "0.0000",
            "theta": "0.4599",
            "vega": "0.9938",
            "rho": "-0.6106"
        },
        {
            "stck_bsop_date": "20240426",
            "elw_prpr": "50",
            "prdy_vrss": "0",
            "prdy_vrss_sign": "3",
            "prdy_ctrt": "0.00",
            "hts_thpr": "44.96",
            "delta_val": "-0.6202",
            "gama": "0.0000",
            "theta": "0.4439",
            "vega": "1.0115",
            "rho": "-0.6308"
        },
        {
            "stck_bsop_date": "20240425",
            "elw_prpr": "50",
            "prdy_vrss": "5",
            "prdy_vrss_sign": "2",
            "prdy_ctrt": "11.11",
            "hts_thpr": "47.92",
            "delta_val": "-0.6534",
            "gama": "0.0000",
            "theta": "0.3673",
            "vega": "0.9917",
            "rho": "-0.6802"
        },
        {
            "stck_bsop_date": "20240424",
            "elw_prpr": "45",
            "prdy_vrss": "-10",
            "prdy_vrss_sign": "5",
            "prdy_ctrt": "-18.18",
            "hts_thpr": "33.74",
            "delta_val": "-0.5173",
            "gama": "0.0000",
            "theta": "0.5516",
            "vega": "1.1208",
            "rho": "-0.5781"
        },
        {
            "stck_bsop_date": "20240423",
            "elw_prpr": "55",
            "prdy_vrss": "-5",
            "prdy_vrss_sign": "5",
            "prdy_ctrt": "-8.33",
            "hts_thpr": "53.36",
            "delta_val": "-0.6933",
            "gama": "0.0000",
            "theta": "0.3086",
            "vega": "0.9632",
            "rho": "-0.7635"
        },
        {
            "stck_bsop_date": "20240422",
            "elw_prpr": "60",
            "prdy_vrss": "15",
            "prdy_vrss_sign": "2",
            "prdy_ctrt": "33.33",
            "hts_thpr": "49.10",
            "delta_val": "-0.6135",
            "gama": "0.0000",
            "theta": "0.4786",
            "vega": "1.0740",
            "rho": "-0.7166"
        },
        {
            "stck_bsop_date": "20240419",
            "elw_prpr": "45",
            "prdy_vrss": "10",
            "prdy_vrss_sign": "2",
            "prdy_ctrt": "28.57",
            "hts_thpr": "38.76",
            "delta_val": "-0.5727",
            "gama": "0.0000",
            "theta": "0.4045",
            "vega": "1.1391",
            "rho": "-0.6851"
        },
        {
            "stck_bsop_date": "20240418",
            "elw_prpr": "35",
            "prdy_vrss": "0",
            "prdy_vrss_sign": "3",
            "prdy_ctrt": "0.00",
            "hts_thpr": "28.22",
            "delta_val": "-0.4785",
            "gama": "0.0000",
            "theta": "0.4284",
            "vega": "1.2033",
            "rho": "-0.5988"
        },
        {
            "stck_bsop_date": "20240417",
            "elw_prpr": "35",
            "prdy_vrss": "0",
            "prdy_vrss_sign": "3",
            "prdy_ctrt": "0.00",
            "hts_thpr": "31.87",
            "delta_val": "-0.5156",
            "gama": "0.0000",
            "theta": "0.3620",
            "vega": "1.2100",
            "rho": "-0.6539"
        },
        {
            "stck_bsop_date": "20240416",
            "elw_prpr": "35",
            "prdy_vrss": "10",
            "prdy_vrss_sign": "2",
            "prdy_ctrt": "40.00",
            "hts_thpr": "26.58",
            "delta_val": "-0.4591",
            "gama": "0.0000",
            "theta": "0.4314",
            "vega": "1.2378",
            "rho": "-0.6115"
        },...
    ],
    "rt_cd": "0",
    "msg_cd": "MCA00000",
    "msg1": "정상처리 되었습니다."
}
```

