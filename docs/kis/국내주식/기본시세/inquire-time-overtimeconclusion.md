# 주식현재가 시간외시간별체결[v1_국내주식-025]

> [국내주식] 기본시세

주식현재가 시간외시간별체결 API입니다.

주식현재가 시간외시간별체결[v1_국내주식-025]

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `3dfc942e-0ed3-4c81-9e8d-9a96f1c5c669` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/quotations/inquire-time-overtimeconclusion` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `https://openapivts.koreainvestment.com:29443` |
| **TR ID** | `FHPST02310000` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2022-06-17
- **최종 수정일**: 2025-04-30

## 요청 (Request)

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | N | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials G... |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | [실전투자/모의투자] FHPST02310000 |
| `tr_cont` | 연속 거래 여부 | String | 1 | N | tr_cont를 이용한 다음조회 불가 API |
| `custtype` | 고객 타입 | String | 1 | N | B : 법인  P : 개인 |
| `seq_no` | 일련번호 | String | 2 | N | [법인 필수] 001 |
| `mac_address` | 맥주소 | String | 12 | N | 법인고객 혹은 개인고객의 Mac address 값 |
| `phone_number` | 핸드폰번호 | String | 12 | N | [법인 필수] 제휴사APP을 사용하는 경우 사용자(회원) 핸드폰번호  ex) 01011112222 (하이픈 등 구분값 제거) |
| `ip_addr` | 접속 단말 공인 IP | String | 12 | N | [법인 필수] 사용자(회원)의 IP Address |
| `gt_uid` | Global UID | String | 32 | N | [법인 전용] 거래고유번호로 사용하므로 거래별로 UNIQUE해야 함 |

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `FID_COND_MRKT_DIV_CODE` | 조건 시장 분류 코드 | String | 2 | Y | J : 주식, ETF, ETN |
| `FID_INPUT_ISCD` | 입력 종목코드 | String | 12 | Y | 종목번호 (6자리) ETN의 경우, Q로 시작 (EX. Q500001) |
| `FID_HOUR_CLS_CODE` | 시간 구분 코드 | String | 5 | Y | 1 : 시간외 (Default) |

### 요청 예시

```json
"input": {
            "fid_cond_mrkt_div_code": "J",
            "fid_hour_CLS_CODE": "1",
            "fid_input_iscd": "018000"
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
| `output1` | 응답상세1 | String |   | N | 기본정보 |
| `ovtm_untp_prpr` | 시간외 단일가 현재가 | String | 10 | N |  |
| `ovtm_untp_prdy_vrss` | 시간외 단일가 전일 대비 | String | 10 | N |  |
| `ovtm_untp_prdy_vrss_sign` | 시간외 단일가 전일 대비 부호 | String | 1 | N |  |
| `ovtm_untp_prdy_ctrt` | 시간외 단일가 전일 대비율 | String | 11 | N |  |
| `ovtm_untp_vol` | 시간외 단일가 거래량 | String | 18 | N |  |
| `ovtm_untp_tr_pbmn` | 시간외 단일가 거래 대금 | String | 18 | N |  |
| `ovtm_untp_mxpr` | 시간외 단일가 상한가 | String | 18 | N |  |
| `ovtm_untp_llam` | 시간외 단일가 하한가 | String | 18 | N |  |
| `ovtm_untp_oprc` | 시간외 단일가 시가2 | String | 10 | N |  |
| `ovtm_untp_hgpr` | 시간외 단일가 최고가 | String | 10 | N |  |
| `ovtm_untp_lwpr` | 시간외 단일가 최저가 | String | 10 | N |  |
| `ovtm_untp_antc_cnpr` | 시간외 단일가 예상 체결가 | String | 10 | N |  |
| `ovtm_untp_antc_cntg_vrss` | 시간외 단일가 예상 체결 대비 | String | 10 | N |  |
| `ovtm_untp_antc_cntg_vrss_sign` | 시간외 단일가 예상 체결 대비 | String | 1 | N |  |
| `ovtm_untp_antc_cntg_ctrt` | 시간외 단일가 예상 체결 대비율 | String | 11 | N |  |
| `ovtm_untp_antc_vol` | 시간외 단일가 예상 거래량 | String | 18 | N |  |
| `uplm_sign` | 상한 부호 | String | 1 | N |  |
| `lslm_sign` | 하한 부호 | String | 1 | N |  |
| `output2` | 응답상세2 | Object |   | N | Array 시간별체결 정보 |
| `stck_cntg_hour` | 주식 체결 시간 | String | 6 | N |  |
| `stck_prpr` | 주식 현재가 | String | 10 | N |  |
| `prdy_vrss` | 전일 대비 | String | 10 | N |  |
| `prdy_vrss_sign` | 전일 대비 부호 | String | 1 | N |  |
| `prdy_ctrt` | 전일 대비율 | String | 11 | N |  |
| `askp` | 매도호가 | String | 10 | N |  |
| `bidp` | 매수호가 | String | 10 | N |  |
| `acml_vol` | 누적 거래량 | String | 18 | N |  |
| `cntg_vol` | 체결 거래량 | String | 18 | N |  |

### 응답 예시

```json
"output1": {
            "lslm_sign": "4",
            "ovtm_untp_antc_cnpr": "0",
            "ovtm_untp_antc_cntg_ctrt": "0.00",
            "ovtm_untp_antc_cntg_vrss": "0",
            "ovtm_untp_antc_cntg_vrss_sign": "3",
            "ovtm_untp_antc_vol": "0",
            "ovtm_untp_hgpr": "2900",
            "ovtm_untp_llam": "2615",
            "ovtm_untp_lwpr": "2835",
            "ovtm_untp_mxpr": "3195",
            "ovtm_untp_oprc": "2900",
            "ovtm_untp_prdy_ctrt": "-2.41",
            "ovtm_untp_prdy_vrss": "-70",
            "ovtm_untp_prdy_vrss_sign": "5",
            "ovtm_untp_prpr": "2835",
            "ovtm_untp_tr_pbmn": "194135625",
            "ovtm_untp_vol": "68086",
            "uplm_sign": "1"
        },
        "output2": [
            {
                "acml_vol": "68086",
                "askp": "2840",
                "bidp": "2835",
                "cntg_vol": "12865",
                "prdy_ctrt": "-2.41",
                "prdy_vrss": "-70",
                "prdy_vrss_sign": "5",
                "stck_cntg_hour": "180025",
                "stck_prpr": "2835"
            },
            {
                "acml_vol": "55221",
                "askp": "2840",
                "bidp": "2835",
                "cntg_vol": "6852",
                "prdy_ctrt": "-2.24",
                "prdy_vrss": "-65",
                "prdy_vrss_sign": "5",
                "stck_cntg_hour": "175026",
                "stck_prpr": "2840"
            },
....
            {
                "acml_vol": "668",
                "askp": "2900",
                "bidp": "2895",
                "cntg_vol": "668",
                "prdy_ctrt": "-0.17",
                "prdy_vrss": "-5",
                "prdy_vrss_sign": "5",
                "stck_cntg_hour": "161022",
                "stck_prpr": "2900"
            }
        ],
        "rt_cd": "0"
```
