# 주식일별분봉조회 [국내주식-213]

> [국내주식] 기본시세

주식일별분봉조회 API입니다. 

실전계좌의 경우, 한 번의 호출에 최대 120건까지 확인 가능하며, 
FID_INPUT_DATE_1, FID_INPUT_HOUR_1 이용하여 과거일자 분봉조회 가능합니다.

※ 과거 분봉 조회 시, 당사 서버에서 보관하고 있는 만큼의 데이터만 확인이 가능합니다. (최대 1년 분봉 보관)


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `9fece97b-401f-4379-9e9d-4365b63c1126` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/quotations/inquire-time-dailychartprice` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `FHKST03010230` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-11-01T13:59:57+09:00
- **최종 수정일**: 2025-04-30T10:19:10+09:00

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials Grant 절차를 준용)  법인(Access token 유효기간 3개월, Refresh token 유효기간 1년, OAuth 2.0의 Authorization Code Grant 절차를 준용) |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | FHKST03010230 |
| `tr_cont` | 연속 거래 여부 | String | 1 | N | 공백 : 초기 조회  N : 다음 데이터 조회 (output header의 tr_cont가 M일 경우) |
| `custtype` | 고객 타입 | String | 1 | Y | B : 법인  P : 개인 |
| `seq_no` | 일련번호 | String | 2 | N | [법인 필수] 001 |
| `mac_address` | 맥주소 | String | 12 | N | 법인고객 혹은 개인고객의 Mac address 값 |
| `phone_number` | 핸드폰번호 | String | 12 | N | [법인 필수] 제휴사APP을 사용하는 경우 사용자(회원) 핸드폰번호  ex) 01011112222 (하이픈 등 구분값 제거) |
| `ip_addr` | 접속 단말 공인 IP | String | 12 | N | [법인 필수] 사용자(회원)의 IP Address |
| `gt_uid` | Global UID | String | 32 | N | [법인 전용] 거래고유번호로 사용하므로 거래별로 UNIQUE해야 함 |

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `FID_COND_MRKT_DIV_CODE` | 조건 시장 분류 코드 | String | 2 | Y | J:KRX, NX:NXT, UN:통합 |
| `FID_INPUT_ISCD` | 입력 종목코드 | String | 12 | Y | 종목코드 (ex 005930 삼성전자) |
| `FID_INPUT_HOUR_1` | 입력 시간1 | String | 10 | Y | 입력 시간(ex 13시 130000) |
| `FID_INPUT_DATE_1` | 입력 날짜1 | String | 2 | Y | 입력 날짜(20241023) |
| `FID_PW_DATA_INCU_YN` | 과거 데이터 포함 여부  | String | 2 | Y |  |
| `FID_FAKE_TICK_INCU_YN` | 허봉 포함 여부 | String | 2 | N | 공백 필수 입력 |

### 요청 예시

```json
FID_COND_MRKT_DIV_CODE:J
FID_INPUT_ISCD:005930
FID_INPUT_DATE_1:20241108
FID_INPUT_HOUR_1:140000
FID_PW_DATA_INCU_YN:Y
FID_FAKE_TICK_INCU_YN:N
```

## 응답

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `tr_id` | 거래ID | String | 13 | Y | 요청한 tr_id |
| `tr_cont` | 연속 거래 여부 | String | 1 | N | 공백 : 초기 조회  N : 다음 데이터 조회 (output header의 tr_cont가 M일 경우) |
| `gt_uid` | Global UID | String | 32 | N | [법인 전용] 거래고유번호로 사용하므로 거래별로 UNIQUE해야 함 |

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `rt_cd` | 성공 실패 여부 | String | 1 | Y |  |
| `msg_cd` | 응답코드 | String | 8 | Y |  |
| `msg1` | 응답메세지 | String | 80 | Y |  |
| `output1` | 응답상세 | String |   | Y |  |
| `prdy_vrss` | 전일 대비  | String | 10 | Y |  |
| `prdy_vrss_sign` | 전일 대비 부호 | String | 1 | Y |  |
| `prdy_ctrt` | 전일 대비율 | String | 11 | Y |  |
| `stck_prdy_clpr` | 주식 전일 종가 | String | 10 | Y |  |
| `acml_vol` | 누적 거래량 | String | 18 | Y |  |
| `acml_tr_pbmn` | 누적 거래 대금 | String | 18 | Y |  |
| `hts_kor_isnm` | HTS 한글 종목명 | String | 40 | Y |  |
| `stck_prpr` | 주식 현재가 | String | 10 | Y |  |
| `output2` | 응답상세 | Object |   | Y | array |
| `stck_bsop_date` | 주식 영업 일자 | String | 8 | Y |  |
| `stck_cntg_hour` | 주식 체결 시간 | String | 6 | Y |  |
| `stck_prpr` | 주식 현재가 | String | 10 | Y |  |
| `stck_oprc` | 주식 시가2 | String | 10 | Y |  |
| `stck_hgpr` | 주식 최고가 | String | 10 | Y |  |
| `stck_lwpr` | 주식 최저가 | String | 10 | Y |  |
| `cntg_vol` | 체결 거래량 | String | 18 | Y |  |
| `acml_tr_pbmn` | 누적 거래 대금 | String | 18 | Y |  |

### 응답 예시

```json
{
    "output1": {
        "prdy_vrss": "-500",
        "prdy_vrss_sign": "5",
        "prdy_ctrt": "-0.87",
        "stck_prdy_clpr": "57500",
        "acml_vol": "13531211",
        "acml_tr_pbmn": "779692013500",
        "hts_kor_isnm": "삼성전자",
        "stck_prpr": "57000"
    },
    "output2": [
        {
            "stck_bsop_date": "20241108",
            "stck_cntg_hour": "140000",
            "stck_prpr": "57300",
            "stck_oprc": "57300",
            "stck_hgpr": "57400",
            "stck_lwpr": "57200",
            "cntg_vol": "59047",
            "acml_tr_pbmn": "538940180600"
        },
        {
            "stck_bsop_date": "20241108",
            "stck_cntg_hour": "135900",
            "stck_prpr": "57300",
            "stck_oprc": "57400",
            "stck_hgpr": "57500",
            "stck_lwpr": "57300",
            "cntg_vol": "118619",
            "acml_tr_pbmn": "535556648100"
        },
		...
        {
            "stck_bsop_date": "20241108",
            "stck_cntg_hour": "120100",
            "stck_prpr": "57700",
            "stck_oprc": "57700",
            "stck_hgpr": "57800",
            "stck_lwpr": "57700",
            "cntg_vol": "3856",
            "acml_tr_pbmn": "357875441100"
        }
    ],
    "rt_cd": "0",
    "msg_cd": "MCA00000",
    "msg1": "정상처리 되었습니다."
}
```

