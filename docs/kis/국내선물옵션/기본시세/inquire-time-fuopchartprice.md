# 선물옵션 분봉조회[v1_국내선물-012]

> [국내선물옵션] 기본시세

선물옵션 분봉조회 API입니다.
실전계좌의 경우, 한 번의 호출에 최대 102건까지 확인 가능하며, 
FID_INPUT_DATE_1(입력날짜), FID_INPUT_HOUR_1(입력시간)을 이용하여 다음조회 가능합니다.

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `86194480-c8f0-4b0b-9d3d-001c2fc33422` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-futureoption/v1/quotations/inquire-time-fuopchartprice` |
| **Content-Type** | `` |
| **요청 포맷** | `` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID** | `모의투자 미지원`, `FHKIF03020200` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2023-08-18
- **최종 수정일**: 2025-04-30

## 요청 (Request)

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials G... |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | FHKIF03020200 |
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
| `FID_COND_MRKT_DIV_CODE` | FID 조건 시장 분류 코드 | String | 2 | Y | F: 지수선물, O:지수옵션 JF: 주식선물, JO:주식옵션, CF: 상품선물(금), 금리선물(국채), 통화선물(달러) CM: 야간선물, EU: 야간옵션 |
| `FID_INPUT_ISCD` | FID 입력 종목코드 | String | 12 | Y | 종목번호 (지수선물:6자리, 지수옵션 9자리) |
| `FID_HOUR_CLS_CODE` | FID 시간 구분 코드 | String | 5 | Y | FID 시간 구분 코드(30: 30초, 60: 1분, 3600: 1시간) |
| `FID_PW_DATA_INCU_YN` | FID 과거 데이터 포함 여부 | String | 2 | Y | Y(과거) / N (당일) |
| `FID_FAKE_TICK_INCU_YN` | FID 허봉 포함 여부 | String | 2 | Y | N으로 입력 |
| `FID_INPUT_DATE_1` | FID 입력 날짜1 | String | 10 | Y | 입력 날짜 기준으로 이전 기간 조회(YYYYMMDD) ex) 20230908 입력 시, 2023년 9월 8일부터 일자 역순으로 조회 |
| `FID_INPUT_HOUR_1` | FID 입력 시간1 | String | 10 | Y | 입력 시간 기준으로 이전 시간 조회(HHMMSS) ex) 093000 입력 시, 오전 9시 30분부터 역순으로 분봉 조회  * CM(야간선물), EU(야간옵션)인 경우, 자정... |

### 요청 예시

```json
fid_cond_mrkt_div_code:F
fid_input_iscd:101V09
fid_hour_cls_code:30
fid_pw_data_incu_yn:N
fid_fake_tick_incu_yn:Y
fid_input_date_1:
fid_input_hour_1:
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
| `Output1` | 응답상세 | Object |   | Y |  |
| `futs_prdy_vrss` | 선물 전일 대비 | String | 11 | Y |  |
| `prdy_vrss_sign` | 전일 대비 부호 | String | 1 | Y |  |
| `futs_prdy_ctrt` | 선물 전일 대비율 | String | 8 | Y |  |
| `futs_prdy_clpr` | 선물 전일 종가 | String | 11 | Y |  |
| `prdy_nmix` | 전일 지수 | String | 11 | Y |  |
| `acml_vol` | 누적 거래량 | String | 18 | Y |  |
| `acml_tr_pbmn` | 누적 거래 대금 | String | 18 | Y |  |
| `hts_kor_isnm` | HTS 한글 종목명 | String | 40 | Y |  |
| `futs_prpr` | 선물 현재가 | String | 11 | Y |  |
| `futs_shrn_iscd` | 선물 단축 종목코드 | String | 9 | Y |  |
| `prdy_vol` | 전일 거래량 | String | 18 | Y |  |
| `futs_mxpr` | 선물 상한가 | String | 11 | Y |  |
| `futs_llam` | 선물 하한가 | String | 11 | Y |  |
| `futs_oprc` | 선물 시가2 | String | 11 | Y |  |
| `futs_hgpr` | 선물 최고가 | String | 11 | Y |  |
| `futs_lwpr` | 선물 최저가 | String | 11 | Y |  |
| `futs_prdy_oprc` | 선물 전일 시가 | String | 11 | Y |  |
| `futs_prdy_hgpr` | 선물 전일 최고가 | String | 11 | Y |  |
| `futs_prdy_lwpr` | 선물 전일 최저가 | String | 11 | Y |  |
| `futs_askp` | 선물 매도호가 | String | 11 | Y |  |
| `futs_bidp` | 선물 매수호가 | String | 11 | Y |  |
| `basis` | 베이시스 | String | 8 | Y |  |
| `kospi200_nmix` | KOSPI200 지수 | String | 11 | Y |  |
| `kospi200_prdy_vrss` | KOSPI200 전일 대비 | String | 18 | Y |  |
| `kospi200_prdy_ctrt` | KOSPI200 전일 대비율 | String | 8 | Y |  |
| `kospi200_prdy_vrss_sign` | KOSPI200 전일 대비 부호 | String | 1 | Y |  |
| `hts_otst_stpl_qty` | HTS 미결제 약정 수량 | String | 18 | Y |  |
| `otst_stpl_qty_icdc` | 미결제 약정 수량 증감 | String | 10 | Y |  |
| `tday_rltv` | 당일 체결강도 | String | 11 | Y |  |
| `hts_thpr` | HTS 이론가 | String | 11 | Y |  |
| `dprt` | 괴리율 | String | 8 | Y |  |
| `Output2` | 응답상세2 | String |   | Y | array |
| `stck_bsop_date` | 주식 영업 일자 | String | 8 | Y |  |
| `stck_cntg_hour` | 주식 체결 시간 | String | 6 | Y | CM(야간선물), EU(야간옵션)인 경우, 자정 이후 시간은 +24시간으로 표시 ex) "260000"인 경우, 오전 4시를 의미 |
| `futs_prpr` | 선물 현재가 | String | 11 | Y |  |
| `futs_oprc` | 선물 시가2 | String | 11 | Y |  |
| `futs_hgpr` | 선물 최고가 | String | 11 | Y |  |
| `futs_lwpr` | 선물 최저가 | String | 11 | Y |  |
| `cntg_vol` | 체결 거래량 | String | 18 | Y |  |
| `acml_tr_pbmn` | 누적 거래 대금 | String | 18 | Y |  |

### 응답 예시

```json
{
    "output1": {
        "futs_prdy_vrss": "-0.30",
        "prdy_vrss_sign": "5",
        "futs_prdy_ctrt": "-0.08",
        "futs_prdy_clpr": "359.90",
        "prdy_nmix": "359.90",
        "acml_vol": "349",
        "acml_tr_pbmn": "31394925",
        "hts_kor_isnm": "F 202409",
        "futs_prpr": "359.60",
        "futs_shrn_iscd": "101V09",
        "prdy_vol": "721",
        "futs_mxpr": "388.65",
        "futs_llam": "331.15",
        "futs_oprc": "361.50",
        "futs_hgpr": "362.00",
        "futs_lwpr": "357.20",
        "futs_prdy_oprc": "364.95",
        "futs_prdy_hgpr": "365.30",
        "futs_prdy_lwpr": "358.60",
        "futs_askp": "359.65",
        "futs_bidp": "359.50",
        "basis": "4.06",
        "kospi200_nmix": "356.42",
        "hts_otst_stpl_qty": "11529",
        "otst_stpl_qty_icdc": "0",
        "tday_rltv": "78.97",
        "hts_thpr": "360.48",
        "dprt": "-0.25"
    },
    "output2": [
        {
            "stck_bsop_date": "20240417",
            "stck_cntg_hour": "141500",
            "futs_prpr": "359.60",
            "futs_oprc": "359.60",
            "futs_hgpr": "359.60",
            "futs_lwpr": "359.60",
            "cntg_vol": "0",
            "acml_tr_pbmn": "31394925"
        },
        {
            "stck_bsop_date": "20240417",
            "stck_cntg_hour": "141430",
            "futs_prpr": "359.60",
            "futs_oprc": "359.60",
            "futs_hgpr": "359.60",
            "futs_lwpr": "359.60",
            "cntg_vol": "0",
            "acml_tr_pbmn": "31394925"
        },
        {
            "stck_bsop_date": "20240417",
            "stck_cntg_hour": "141400",
            "futs_prpr": "359.60",
            "futs_oprc": "359.60",
            "futs_hgpr": "359.60",
            "futs_lwpr": "359.60",
            "cntg_vol": "0",
            "acml_tr_pbmn": "31394925"
        },
        {
            "stck_bsop_date": "20240417",
            "stck_cntg_hour": "141330",
            "futs_prpr": "359.60",
            "futs_oprc": "359.60",
            "futs_hgpr": "359.60",
            "futs_lwpr": "359.60",
            "cntg_vol": "0",
            "acml_tr_pbmn": "31394925"
        },...
    ],
    "rt_cd": "0",
    "msg_cd": "MCA00000",
    "msg1": "정상처리 되었습니다."
}
```
