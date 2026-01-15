# 주식당일분봉조회[v1_국내주식-022]

> [국내주식] 기본시세

주식당일분봉조회 API입니다. 
실전계좌/모의계좌의 경우, 한 번의 호출에 최대 30건까지 확인 가능합니다.

※ 당일 분봉 데이터만 제공됩니다. (전일자 분봉 미제공)

※ input > FID_INPUT_HOUR_1 에 미래일시 입력 시에 현재가로 조회됩니다.
ex) 오전 10시에 113000 입력 시에 오전 10시~11시30분 사이의 데이터가 오전 10시 값으로 조회됨

※ output2의 첫번째 배열의 체결량(cntg_vol)은 첫체결이 발생되기 전까지는 이전 분봉의 체결량이 해당 위치에 표시됩니다. 
해당 분봉의 첫 체결이 발생되면 해당 이전분 체결량이 두번째 배열로 이동되면서 새로운 체결량으로 업데이트됩니다.

주식당일분봉조회[v1_국내주식-022]

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `eddbb36a-1d55-461a-b242-3067ba1e5640` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/quotations/inquire-time-itemchartprice` |
| **Content-Type** | `application/json; charset=UTF-8` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `https://openapivts.koreainvestment.com:29443` |
| **TR ID (실전)** | `FHKST03010200` |
| **TR ID (모의)** | `FHKST03010200` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2022-09-02
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
| `tr_id` | 거래ID | String | 13 | Y | FHKST03010200 |
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
| `FID_PW_DATA_INCU_YN` | 과거 데이터 포함 여부  | String | 2 | Y |  |
| `FID_ETC_CLS_CODE` | 기타 구분 코드 | String | 2 | Y |  |

### 요청 예시

```json
{
  "fid_cond_mrkt_div_code": "J",
  "fid_etc_cls_code": "",
  "fid_input_hour_1": "100000",
  "fid_input_iscd": "000660",
  "fid_pw_data_incu_yn": "Y"
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
| `output1` | 응답상세 | String |   | Y |  |
| `prdy_vrss` | 전일 대비 | String | 10 | Y | 전일 대비 변동 (+-변동차이) |
| `prdy_vrss_sign` | 전일 대비 부호 | String | 1 | Y | 전일 대비 부호 |
| `prdy_ctrt` | 전일 대비율 | String | 10 | Y | 소수점 두자리까지 제공 |
| `stck_prdy_clpr` | 전일대비 종가 | String | 10 | Y | 전일대비 종가 |
| `acml_vol` | 누적 거래량 | String | 18 | Y | 누적 거래량 |
| `acml_tr_pbmn` | 누적 거래대금 | String | 18 | Y | 누적 거래대금 |
| `hts_kor_isnm` | 한글 종목명 | String | 40 | Y | 한글 종목명 (HTS 기준) |
| `stck_prpr` | 주식 현재가 | String | 10 | Y | 주식 현재가 |
| `output2` | 응답상세 | Object |   | Y | Array |
| `stck_bsop_date` | 주식 영업일자 | String | 8 | Y | 주식 영업일자 |
| `stck_cntg_hour` | 주식 체결시간 | String | 6 | Y | 주식 체결시간 |
| `stck_prpr` | 주식 현재가 | String | 10 | Y | 주식 현재가 |
| `stck_oprc` | 주식 시가 | String | 10 | Y | 주식 시가 |
| `stck_hgpr` | 주식 최고가 | String | 10 | Y | 주식 최고가 |
| `stck_lwpr` | 주식 최저가 | String | 10 | Y | 주식 최저가 |
| `cntg_vol` | 체결 거래량 | String | 18 | Y |  |
| `acml_tr_pbmn` | 누적 거래대금 | String | 18 | Y |  |

### 응답 예시

```json
{
        "output1": {
            "acml_tr_pbmn": "96910660000",
            "acml_vol": "1046883",
            "hts_kor_isnm": "SK하이닉스",
            "prdy_ctrt": "-0.11",
            "prdy_vrss": "-100",
            "prdy_vrss_sign": "5",
            "stck_prdy_clpr": "92400",
            "stck_prpr": "92300"
        },
        "output2": [
            {
                "acml_tr_pbmn": "55858827400",
                "cntg_vol": "1383",
                "stck_bsop_date": "20220902",
                "stck_cntg_hour": "100000",
                "stck_hgpr": "92500",
                "stck_lwpr": "92400",
                "stck_oprc": "92400",
                "stck_prpr": "92500"
            },
            {
                "acml_tr_pbmn": "55731000300",
                "cntg_vol": "1564",
                "stck_bsop_date": "20220902",
                "stck_cntg_hour": "095900",
                "stck_hgpr": "92500",
                "stck_lwpr": "92400",
                "stck_oprc": "92500",
                "stck_prpr": "92400"
                              "stck_hgpr": "93300",
                "stck_lwpr": "93100",
                "stck_oprc": "93100",
                "stck_prpr": "93200"
            }
            ......
        ],
        "rt_cd": "0",
         "msg_cd": "MCA00000",
         "msg1": "정상처리 되었습니다!"
 }
```

