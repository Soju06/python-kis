# 주식현재가 시간외일자별주가[v1_국내주식-026]

> [국내주식] 기본시세

주식현재가 시간외일자별주가 API입니다.  (최근일 30건만 조회 가능)

주식현재가 시간외일자별주가[v1_국내주식-026]

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `4ea57616-0e63-4f8c-a607-f096f1304183` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/quotations/inquire-daily-overtimeprice` |
| **Content-Type** | `` |
| **요청 포맷** | `` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `https://openapivts.koreainvestment.com:29443` |
| **TR ID** | `FHPST02320000` |

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
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요!) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | [실전투자/모의투자] FHPST02320000 |
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
| `FID_COND_MRKT_DIV_CODE` | FID 조건 시장 분류 코드 | String | 2 | Y | J : 주식, ETF, ETN |
| `FID_INPUT_ISCD` | FID 입력 종목코드 | String | 12 | Y | 종목번호 (6자리) ETN의 경우, Q로 시작 (EX. Q500001) |

### 요청 예시

```json
'"input": {'
                '"fid_cond_mrkt_div_code":"J"'
                ','
                '"fid_input_iscd":"000660"'
            '}'
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
| `ovtm_untp_prdy_ctrt` | 시간외 단일가 전일 대비율 | String | 11 | N | 11(8.2) |
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
| `ovtm_untp_antc_cntg_ctrt` | 시간외 단일가 예상 체결 대비율 | String | 11 | N | 11(8.2) |
| `ovtm_untp_antc_vol` | 시간외 단일가 예상 거래량 | String | 18 | N |  |
| `output2` | 응답상세2 | Object |   | N | Array 일자별 정보 |
| `stck_bsop_date` | 주식 영업 일자 | String | 8 | N |  |
| `ovtm_untp_prpr` | 시간외 단일가 현재가 | String | 10 | N |  |
| `ovtm_untp_prdy_vrss` | 시간외 단일가 전일 대비 | String | 10 | N |  |
| `ovtm_untp_prdy_vrss_sign` | 시간외 단일가 전일 대비 부호 | String | 1 | N |  |
| `ovtm_untp_prdy_ctrt` | 시간외 단일가 전일 대비율 | String | 11 | N | 11(8.2) |
| `ovtm_untp_vol` | 시간외 단일가 거래량 | String | 18 | N |  |
| `stck_clpr` | 주식 종가 | String | 10 | N |  |
| `prdy_vrss` | 전일 대비 | String | 10 | N |  |
| `prdy_vrss_sign` | 전일 대비 부호 | String | 1 | N |  |
| `prdy_ctrt` | 전일 대비율 | String | 11 | N | 11(8.2) |
| `acml_vol` | 누적 거래량 | String | 18 | N |  |
| `ovtm_untp_tr_pbmn` | 시간외 단일가 거래대금 | String | 18 | N |  |

### 응답 예시

```json
"output1": {
            "ovtm_untp_antc_cnpr": "0",
            "ovtm_untp_antc_cntg_ctrt": "0.00",
            "ovtm_untp_antc_cntg_vrss": "0",
            "ovtm_untp_antc_cntg_vrss_sign": "3",
            "ovtm_untp_antc_vol": "0",
            "ovtm_untp_hgpr": "106000",
            "ovtm_untp_llam": "95000",
            "ovtm_untp_lwpr": "105500",
            "ovtm_untp_mxpr": "116000",
            "ovtm_untp_oprc": "0",
            "ovtm_untp_prdy_ctrt": "0.47",
            "ovtm_untp_prdy_vrss": "500",
            "ovtm_untp_prdy_vrss_sign": "2",
            "ovtm_untp_prpr": "106000",
            "ovtm_untp_tr_pbmn": "1348318000",
            "ovtm_untp_vol": "12740"
        },
        "output2": [
            {
                "acml_vol": "4640744",
                "ovtm_untp_prdy_ctrt": "0.47",
                "ovtm_untp_prdy_vrss": "500",
                "ovtm_untp_prdy_vrss_sign": "2",
                "ovtm_untp_prpr": "106000",
                "ovtm_untp_tr_pbmn": "1348318000",
                "ovtm_untp_vol": "12740",
                "prdy_ctrt": "-0.47",
                "prdy_vrss": "-500",
                "prdy_vrss_sign": "5",
                "stck_bsop_date": "20220609",
                "stck_clpr": "105500"
            },
            {
                "acml_vol": "3075530",
                "ovtm_untp_prdy_ctrt": "0.47",
                "ovtm_untp_prdy_vrss": "500",
                "ovtm_untp_prdy_vrss_sign": "2",
                "ovtm_untp_prpr": "106500",
                "ovtm_untp_tr_pbmn": "1882068000",
                "ovtm_untp_vol": "17672",
                "prdy_ctrt": "1.92",
                "prdy_vrss": "2000",
......
            {
                "acml_vol": "2969516",
                "ovtm_untp_prdy_ctrt": "0.00",
                "ovtm_untp_prdy_vrss": "0",
                "ovtm_untp_prdy_vrss_sign": "3",
                "ovtm_untp_prpr": "111000",
                "ovtm_untp_tr_pbmn": "2273650500",
                "ovtm_untp_vol": "20565",
                "prdy_ctrt": "2.78",
                "prdy_vrss": "3000",
                "prdy_vrss_sign": "2",
                "stck_bsop_date": "20220426",
                "stck_clpr": "111000"
            }
        ],
        "rt_cd": "0"
```
