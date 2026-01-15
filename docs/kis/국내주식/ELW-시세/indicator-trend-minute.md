# ELW 투자지표추이(분별) [국내주식-174]

> [국내주식] ELW 시세

ELW 투자지표추이(분별) API입니다.
한국투자 HTS(eFriend Plus) > [0274] ELW 투자지표추이 화면 데이터의 "분별 비교추이" 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `4af6e358-255c-4e4e-b691-388610068216` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/elw/v1/quotations/indicator-trend-minute` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `미지원` |
| **TR ID** | `모의투자 미지원`, `FHPEW02740300` |

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
| `tr_id` | 거래ID | String | 13 | Y | FHPEW02740300 |
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
| `FID_HOUR_CLS_CODE` | 시간구분코드 | String | 5 | Y | '60(1분), 180(3분), 300(5분), 600(10분), 1800(30분), 3600(60분), 7200(60분) ' |
| `FID_PW_DATA_INCU_YN` | 과거데이터 포함 여부 | String | 2 | Y | N(과거데이터포함X),Y(과거데이터포함O) |

### 요청 예시

```json
FID_COND_MRKT_DIV_CODE:W
FID_INPUT_ISCD:57K281
FID_HOUR_CLS_CODE:60
FID_PW_DATA_INCU_YN:Y
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
| `stck_bsop_date` | 주식영업일자 | String | 8 | Y |  |
| `stck_cntg_hour` | 주식체결시간 | String | 6 | Y |  |
| `elw_prpr` | ELW현재가 | String | 10 | Y |  |
| `elw_oprc` | ELW시가2 | String | 10 | Y |  |
| `elw_hgpr` | ELW최고가 | String | 10 | Y |  |
| `elw_lwpr` | ELW최저가 | String | 10 | Y |  |
| `lvrg_val` | 레버리지값 | String | 114 | Y |  |
| `gear` | 기어링 | String | 84 | Y |  |
| `prmm_val` | 프리미엄값 | String | 114 | Y |  |
| `invl_val` | 내재가치값 | String | 132 | Y |  |
| `prit` | 패리티 | String | 112 | Y |  |
| `acml_vol` | 누적거래량 | String | 18 | Y |  |
| `cntg_vol` | 체결거래량 | String | 18 | Y |  |

### 응답 예시

```json
{
    "output": [
        {
            "stck_bsop_date": "20240503",
            "stck_cntg_hour": "131900",
            "elw_prpr": "40",
            "elw_oprc": "40",
            "elw_hgpr": "40",
            "elw_lwpr": "40",
            "lvrg_val": "-10.8818",
            "gear": "19.5700",
            "prmm_val": "5.1086",
            "invl_val": "17.00",
            "prit": "102.17",
            "acml_vol": "827720",
            "cntg_vol": "55700"
        },
        {
            "stck_bsop_date": "20240503",
            "stck_cntg_hour": "131800",
            "elw_prpr": "40",
            "elw_oprc": "40",
            "elw_hgpr": "40",
            "elw_lwpr": "40",
            "lvrg_val": "19.5700",
            "gear": "33.5300",
            "prmm_val": "5.1086",
            "invl_val": "17.00",
            "prit": "-10.72",
            "acml_vol": "772020",
            "cntg_vol": "0"
        },
        {
            "stck_bsop_date": "20240503",
            "stck_cntg_hour": "131700",
            "elw_prpr": "40",
            "elw_oprc": "40",
            "elw_hgpr": "40",
            "elw_lwpr": "40",
            "lvrg_val": "19.5700",
            "gear": "33.5300",
            "prmm_val": "5.1086",
            "invl_val": "17.00",
            "prit": "-10.72",
            "acml_vol": "772020",
            "cntg_vol": "0"
        },
        {
            "stck_bsop_date": "20240503",
            "stck_cntg_hour": "131600",
            "elw_prpr": "40",
            "elw_oprc": "40",
            "elw_hgpr": "40",
            "elw_lwpr": "40",
            "lvrg_val": "19.5700",
            "gear": "33.5300",
            "prmm_val": "5.1086",
            "invl_val": "17.00",
            "prit": "-10.72",
            "acml_vol": "772020",
            "cntg_vol": "0"
        },
        {
            "stck_bsop_date": "20240503",
            "stck_cntg_hour": "131500",
            "elw_prpr": "40",
            "elw_oprc": "40",
            "elw_hgpr": "40",
            "elw_lwpr": "40",
            "lvrg_val": "19.5700",
            "gear": "33.5300",
            "prmm_val": "5.1086",
            "invl_val": "17.00",
            "prit": "-10.72",
            "acml_vol": "772020",
            "cntg_vol": "0"
        },
        {
            "stck_bsop_date": "20240503",
            "stck_cntg_hour": "131400",
            "elw_prpr": "40",
            "elw_oprc": "40",
            "elw_hgpr": "40",
            "elw_lwpr": "40",
            "lvrg_val": "19.5700",
            "gear": "33.5300",
            "prmm_val": "5.1086",
            "invl_val": "17.00",
            "prit": "-10.72",
            "acml_vol": "772020",
            "cntg_vol": "0"
        },
        {
            "stck_bsop_date": "20240503",
            "stck_cntg_hour": "131300",
            "elw_prpr": "40",
            "elw_oprc": "40",
            "elw_hgpr": "40",
            "elw_lwpr": "40",
            "lvrg_val": "19.5700",
            "gear": "33.5300",
            "prmm_val": "5.1086",
            "invl_val": "17.00",
            "prit": "-10.72",
            "acml_vol": "772020",
            "cntg_vol": "0"
        },
        {
            "stck_bsop_date": "20240503",
            "stck_cntg_hour": "131200",
            "elw_prpr": "40",
            "elw_oprc": "40",
            "elw_hgpr": "40",
            "elw_lwpr": "40",
            "lvrg_val": "19.5700",
            "gear": "33.5300",
            "prmm_val": "5.1086",
            "invl_val": "17.00",
            "prit": "-10.72",
            "acml_vol": "772020",
            "cntg_vol": "0"
        },
        {
            "stck_bsop_date": "20240503",
            "stck_cntg_hour": "131100",
            "elw_prpr": "40",
            "elw_oprc": "40",
            "elw_hgpr": "40",
            "elw_lwpr": "40",
            "lvrg_val": "19.5700",
            "gear": "33.5300",
            "prmm_val": "5.1086",
            "invl_val": "17.00",
            "prit": "-10.72",
            "acml_vol": "772020",
            "cntg_vol": "0"
        },
        {
            "stck_bsop_date": "20240503",
            "stck_cntg_hour": "131000",
            "elw_prpr": "40",
            "elw_oprc": "40",
            "elw_hgpr": "40",
            "elw_lwpr": "40",
            "lvrg_val": "19.5700",
            "gear": "33.5300",
            "prmm_val": "5.1086",
            "invl_val": "17.00",
            "prit": "-10.72",
            "acml_vol": "772020",
            "cntg_vol": "0"
        },
        {
            "stck_bsop_date": "20240503",
            "stck_cntg_hour": "130900",
            "elw_prpr": "40",
            "elw_oprc": "40",
            "elw_hgpr": "40",
            "elw_lwpr": "40",
            "lvrg_val": "19.5700",
            "gear": "33.5300",
            "prmm_val": "5.1086",
            "invl_val": "17.00",
            "prit": "-10.72",
            "acml_vol": "772020",
            "cntg_vol": "0"
        },
        {
            "stck_bsop_date": "20240503",
            "stck_cntg_hour": "130800",
            "elw_prpr": "40",
            "elw_oprc": "40",
            "elw_hgpr": "40",
            "elw_lwpr": "40",
            "lvrg_val": "19.5700",
            "gear": "33.5300",
            "prmm_val": "5.1086",
            "invl_val": "17.00",
            "prit": "-10.72",
            "acml_vol": "772020",
            "cntg_vol": "0"
        },
        {
            "stck_bsop_date": "20240503",
            "stck_cntg_hour": "130700",
            "elw_prpr": "40",
            "elw_oprc": "40",
            "elw_hgpr": "40",
            "elw_lwpr": "40",
            "lvrg_val": "19.5700",
            "gear": "33.5300",
            "prmm_val": "5.1086",
            "invl_val": "17.00",
            "prit": "-10.72",
            "acml_vol": "772020",
            "cntg_vol": "0"
        },
        {
            "stck_bsop_date": "20240503",
            "stck_cntg_hour": "130600",
            "elw_prpr": "40",
            "elw_oprc": "40",
            "elw_hgpr": "40",
            "elw_lwpr": "40",
            "lvrg_val": "19.5700",
            "gear": "33.5300",
            "prmm_val": "5.1086",
            "invl_val": "17.00",
            "prit": "-10.72",
            "acml_vol": "772020",
            "cntg_vol": "0"
        },
        {
            "stck_bsop_date": "20240503",
            "stck_cntg_hour": "130500",
            "elw_prpr": "40",
            "elw_oprc": "40",
            "elw_hgpr": "40",
            "elw_lwpr": "40",
            "lvrg_val": "19.5700",
            "gear": "33.5300",
            "prmm_val": "5.1086",
            "invl_val": "17.00",
            "prit": "-10.72",
            "acml_vol": "772020",
            "cntg_vol": "0"
        },
        {
            "stck_bsop_date": "20240503",
            "stck_cntg_hour": "130400",
            "elw_prpr": "40",
            "elw_oprc": "40",
            "elw_hgpr": "40",
            "elw_lwpr": "40",
            "lvrg_val": "19.5700",
            "gear": "33.5300",
            "prmm_val": "5.1086",
            "invl_val": "17.00",
            "prit": "-10.72",
            "acml_vol": "772020",
            "cntg_vol": "0"
        },...
        {
            "stck_bsop_date": "20240503",
            "stck_cntg_hour": "114000",
            "elw_prpr": "40",
            "elw_oprc": "40",
            "elw_hgpr": "40",
            "elw_lwpr": "40",
            "lvrg_val": "19.5700",
            "gear": "33.5300",
            "prmm_val": "5.1086",
            "invl_val": "17.00",
            "prit": "-10.72",
            "acml_vol": "772020",
            "cntg_vol": "0"
        }
    ],
    "rt_cd": "0",
    "msg_cd": "MCA00000",
    "msg1": "정상처리 되었습니다."
}
```
