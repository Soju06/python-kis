# 해외주식 종목/지수/환율기간별시세(일/주/월/년)[v1_해외주식-012]

> [해외주식] 기본시세

해외주식 종목/지수/환율기간별시세(일/주/월/년) API입니다.

해외지수 당일 시세의 경우 지연시세 or 종가시세가 제공됩니다.

※ 해당 API로 미국주식 조회 시, 다우30, 나스닥100, S&P500 종목만 조회 가능합니다.
   더 많은 미국주식 종목 시세를 이용할 시에는, 해외주식기간별시세 API 사용 부탁드립니다.

[v1_해외주식-012] 해외지수/환율기간별시세(일/주/월/년)

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `da63a88a-e288-426f-9498-42db0b537bf3` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/overseas-price/v1/quotations/inquire-daily-chartprice` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `https://openapivts.koreainvestment.com:29443` |
| **TR ID (실전)** | `FHKST03030100` |
| **TR ID (모의)** | `FHKST03030100` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2022-07-01
- **최종 수정일**: 2025-04-30

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | N | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials G... |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | [실전투자/모의투자] FHKST03030100 |
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
| `FID_COND_MRKT_DIV_CODE` | FID 조건 시장 분류 코드 | String | 2 | Y | N: 해외지수, X 환율, I: 국채, S:금선물 |
| `FID_INPUT_ISCD` | FID 입력 종목코드 | String | 12 | Y | 종목코드 ※ 해외주식 마스터 코드 참조  (포럼 > FAQ > 종목정보 다운로드(해외) > 해외지수)  ※ 해당 API로 미국주식 조회 시, 다우30, 나스닥100, S&P5... |
| `FID_INPUT_DATE_1` | FID 입력 날짜1 | String | 10 | Y | 시작일자(YYYYMMDD) |
| `FID_INPUT_DATE_2` | FID 입력 날짜2 | String | 10 | Y | 종료일자(YYYYMMDD) |
| `FID_PERIOD_DIV_CODE` | FID 기간 분류 코드 | String | 32 | Y | D:일, W:주, M:월, Y:년 |

### 요청 예시

```json
"input": {
            "fid_cond_mrkt_div_code": "N",
            "fid_input_date_1": "20220401",
            "fid_input_date_2": "20220613",
            "fid_input_iscd": ".DJI",
            "fid_period_div_code": "D"
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
| `output1` | 응답상세1 | String |   | N | 기본정보 |
| `ovrs_nmix_prdy_vrss` |  전일 대비 | String | 16 | N | 16(11.4) 정수부분 11자리, 소수부분 4자리 |
| `prdy_vrss_sign` | 전일 대비 부호 | String | 1 | N |  |
| `prdy_ctrt` | 전일 대비율 | String | 11 | N | 11(8.2) 정수부분 8자리, 소수부분 2자리 |
| `ovrs_nmix_prdy_clpr` | 전일 종가 | String | 16 | N | 16(11.4) 정수부분 11자리, 소수부분 4자리 |
| `acml_vol` | 누적 거래량 | String | 18 | N |  |
| `hts_kor_isnm` | HTS 한글 종목명 | String | 40 | N |  |
| `ovrs_nmix_prpr` | 현재가 | String | 16 | N | 16(11.4) 정수부분 11자리, 소수부분 4자리 |
| `stck_shrn_iscd` | 단축 종목코드 | String | 9 | N |  |
| `prdy_vol` | 전일 거래량 | String | 18 | N |  |
| `ovrs_prod_oprc` | 시가 | String | 16 | N | 16(11.4) 정수부분 11자리, 소수부분 4자리 |
| `ovrs_prod_hgpr` | 최고가 | String | 16 | N | 16(11.4) 정수부분 11자리, 소수부분 4자리 |
| `ovrs_prod_lwpr` | 최저가 | String | 16 | N | 16(11.4) 정수부분 11자리, 소수부분 4자리 |
| `output2` | 응답상세2 | Object |   | N | 일자별 정보 |
| `stck_bsop_date` | 영업 일자 | String | 8 | N |  |
| `ovrs_nmix_prpr` | 현재가 | String | 16 | N | 16(11.4) 정수부분 11자리, 소수부분 4자리 |
| `ovrs_nmix_oprc` | 시가 | String | 16 | N | 16(11.4) 정수부분 11자리, 소수부분 4자리 |
| `ovrs_nmix_hgpr` | 최고가 | String | 16 | N | 16(11.4) 정수부분 11자리, 소수부분 4자리 |
| `ovrs_nmix_lwpr` | 최저가 | String | 16 | N | 16(11.4) 정수부분 11자리, 소수부분 4자리 |
| `acml_vol` | 누적 거래량 | String | 18 | N |  |
| `mod_yn` | 변경 여부 | String | 1 | N |  |

### 응답 예시

```json
"output1": {
            "acml_vol": "397268510",
            "hts_kor_isnm": "다우존스 산업지수",
            "ovrs_nmix_prdy_clpr": "31029.31",
            "ovrs_nmix_prdy_vrss": "-253.88",
            "ovrs_nmix_prpr": "30775.43",
            "ovrs_prod_hgpr": "30979.85",
            "ovrs_prod_lwpr": "30431.87",
            "ovrs_prod_oprc": "30790.00",
            "prdy_ctrt": "-0.82",
            "prdy_vrss_sign": "5",
            "stck_shrn_iscd": ".DJI"
        },
        "output2": [
            {
                "acml_vol": "480501460",
                "mod_yn": "N",
                "ovrs_nmix_hgpr": "31144.91",
                "ovrs_nmix_lwpr": "30373.72",
                "ovrs_nmix_oprc": "31144.91",
                "ovrs_nmix_prpr": "30516.74",
                "stck_bsop_date": "20220613"
            },
....
            {
                "acml_vol": "346813590",
                "mod_yn": "N",
                "ovrs_nmix_hgpr": "34847.91",
                "ovrs_nmix_lwpr": "34538.25",
                "ovrs_nmix_oprc": "34740.89",
                "ovrs_nmix_prpr": "34818.27",
                "stck_bsop_date": "20220401"
            }
```

