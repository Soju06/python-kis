# 주식현재가 당일시간대별체결[v1_국내주식-023]

> [국내주식] 기본시세

주식현재가 당일시간대별체결 API입니다.

주식현재가 당일시간대별체결[v1_국내주식-023]

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `81b30d9e-1bce-439f-9cf0-56f0ea1a4f95` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/quotations/inquire-time-itemconclusion` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `https://openapivts.koreainvestment.com:29443` |
| **TR ID (실전)** | `FHPST01060000` |
| **TR ID (모의)** | `FHPST01060000` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2022-06-17T16:14:13+09:00
- **최종 수정일**: 2025-04-30T10:14:45+09:00

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials Grant 절차를 준용)  법인(Access token 유효기간 3개월, Refresh token 유효기간 1년, OAuth 2.0의 Authorization Code Grant 절차를 준용) |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | FHPST01060000 |
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
| `FID_COND_MRKT_DIV_CODE` | 조건 시장 분류 코드 | String | 2 | Y | J:KRX, NX:NXT, UN:통합 |
| `FID_INPUT_ISCD` | 입력 종목코드 | String | 12 | Y | 종목코드 (ex 005930 삼성전자) |
| `FID_INPUT_HOUR_1` | 입력 시간1 | String | 10 | Y | 입력시간 |

### 요청 예시

```json
"input": {
            "fid_cond_mrkt_div_code": "J",
            "fid_input_hour_1": "141200",
            "fid_input_iscd": "000660"
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
| `output1` | 응답상세 | String |   | Y | single |
| `stck_prpr` | 주식 현재가 | String | 10 | Y |  |
| `prdy_vrss` | 전일 대비  | String | 10 | Y |  |
| `prdy_vrss_sign` | 전일 대비 부호 | String | 1 | Y |  |
| `prdy_ctrt` | 전일 대비율 | String | 11 | Y |  |
| `acml_vol` | 누적 거래량 | String | 18 | Y |  |
| `prdy_vol` | 전일 거래량 | String | 18 | Y |  |
| `rprs_mrkt_kor_name` | 대표 시장 한글 명 | String | 40 | Y |  |
| `output2` | 응답상세 | String |   | Y | single |
| `stck_cntg_hour` | 주식 체결 시간 | String | 6 | Y |  |
| `stck_pbpr` | 주식 현재가 | String | 10 | Y |  |
| `prdy_vrss` | 전일 대비  | String | 10 | Y |  |
| `prdy_vrss_sign` | 전일 대비 부호 | String | 1 | Y |  |
| `prdy_ctrt` | 전일 대비율  | String | 11 | Y |  |
| `askp` | 매도호가 | String | 10 | Y |  |
| `bidp` | 매수호가 | String | 10 | Y |  |
| `tday_rltv` | 당일 체결강도 | String | 14 | Y |  |
| `acml_vol` | 누적 거래량 | String | 18 | Y |  |
| `cnqn` | 체결량 | String | 18 | Y |  |

### 응답 예시

```json
"output1": {
            "acml_vol": "2315529",
            "prdy_ctrt": "-2.80",
            "prdy_vol": "1638006",
            "prdy_vrss": "-3000",
            "prdy_vrss_sign": "5",
            "rprs_mrkt_kor_name": "KOSPI200",
            "stck_prpr": "104000"
        },
        "output2": [
            {
                "acml_vol": "1979727",
                "askp": "105000",
                "bidp": "104500",
                "cnqn": "20",
                "prdy_ctrt": "-2.34",
                "prdy_vrss": "-2500",
                "prdy_vrss_sign": "5",
                "stck_cntg_hour": "141159",
                "stck_prpr": "104500",
                "tday_rltv": "42.43"
            },
            {
                "acml_vol": "1979707",
                "askp": "105000",
                "bidp": "104500",
                "cnqn": "4",
                "prdy_ctrt": "-2.34",
                "prdy_vrss": "-2500",
                "prdy_vrss_sign": "5",
                "stck_cntg_hour": "141158",
                "stck_prpr": "104500",
                "tday_rltv": "42.43"
            },
....
            {
                "acml_vol": "1979079",
                "askp": "105000",
                "bidp": "104500",
                "cnqn": "92",
                "prdy_ctrt": "-2.34",
                "prdy_vrss": "-2500",
                "prdy_vrss_sign": "5",
                "stck_cntg_hour": "141142",
                "stck_prpr": "104500",
                "tday_rltv": "42.44"
            }
        ],
        "rt_cd": "0"
```

