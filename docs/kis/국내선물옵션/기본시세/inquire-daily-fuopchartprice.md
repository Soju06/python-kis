# 선물옵션기간별시세(일/주/월/년)[v1_국내선물-008]

> [국내선물옵션] 기본시세

(지수)선물옵션 기간별시세 데이터(일/주/월/년) 조회 (최대 100건 조회)
실전계좌의 경우, 한 번의 호출에 최대 100건까지 확인 가능하며, 이후의 값은 연속조회를 통해 확인하실 수 있습니다. 
모의계좌의 경우, 한 번의 호출에 최대 100건까지 확인 가능하며, 이후의 값은 연속조회를 통해 확인하실 수 있습니다.

[국내선물-008 v1] 선물옵션기간별시세(일/주/월/년)

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `77de2a74-b26c-40ca-a5b7-f87e2ef64f9f` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-futureoption/v1/quotations/inquire-daily-fuopchartprice` |
| **Content-Type** | `` |
| **요청 포맷** | `` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `https://openapivts.koreainvestment.com:29443` |
| **TR ID** | `FHKIF03020100` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2022-05-26
- **최종 수정일**: 2025-04-30

## 요청 (Request)

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | N | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token 일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials Gr... |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appsecret (절대 노출되지 않도록 주의해주세요.) |
| `tr_id` | 거래ID | String | 13 | Y | [실전/모의투자] FHKIF03020100 |
| `custtype` | 고객타입 | String | 1 | N | B : 법인 P : 개인 |

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `FID_COND_MRKT_DIV_CODE` | FID 조건 시장 분류 코드 | String | 2 | Y | F: 지수선물, O:지수옵션 JF: 주식선물, JO:주식옵션, CF: 상품선물(금), 금리선물(국채), 통화선물(달러) CM: 야간선물, EU: 야간옵션 |
| `FID_INPUT_ISCD` | 종목코드 | String | 12 | Y | 종목번호 (지수선물:6자리, 지수옵션 9자리) |
| `FID_INPUT_DATE_1` | 조회 시작일자 | String | 10 | Y | 조회 시작일자 (ex. 20220401) |
| `FID_INPUT_DATE_2` | 조회 종료일자  | String | 10 | Y | 조회 종료일자 (ex. 20220524)  ※ 주(W), 월(M), 년(Y) 봉 조회 시에 아래 참고 ㅁ FID_INPUT_DATE_2 가 현재일 까지일때 . 주봉 조회 : ... |
| `FID_PERIOD_DIV_CODE` | 기간분류코드 | String | 32 | Y | D:일봉 W:주봉, M:월봉, Y:년봉 |

### 요청 예시

```json
"input": {
            "fid_cond_mrkt_div_code": "F",
            "fid_input_date_1": "20220401",
            "fid_input_date_2": "20220524",
            "fid_input_iscd": "101S06",
            "fid_period_div_code": "D"
        }
```

## 응답 (Response)

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `tr_id` | 거래ID | String | 13 | Y | 요청한 tr_id |
| `gt_uid` | Global UID | String | 32 | Y | [법인 전용] 거래고유번호로 사용하므로 거래별로 UNIQUE해야 함 |

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `rt_cd` | 성공 실패 여부 | String | 1 | Y | 0 : 성공  0 이외의 값 : 실패 |
| `msg_cd` | 응답코드 | String | 8 | Y | 응답코드 |
| `msg1` | 응답메세지 | String | 80 | Y | 응답메세지 |
| `output1` | 상세기본정보 | String | 1 | Y | 상세기본정보 |
| `-futs_prdy_vrss` | 전일 대비 | String | 14 | Y | 전일 대비 |
| `-prdy_vrss_sign` | 전일 대비 부호 | String | 1 | Y | 전일 대비 부호 |
| `-futs_prdy_ctrt` | 선물 전일 대비율 | String | 11 | Y | 선물 전일 대비율 |
| `-futs_prdy_clpr` | 선물 전일 종가 | String | 14 | Y | 선물 전일 종가 |
| `-acml_vol` | 누적 거래량 | String | 18 | Y | 누적 거래량 |
| `-acml_tr_pbmn` | 누적 거래 대금 | String | 18 | Y | 누적 거래 대금 |
| `-hts_kor_isnm` | HTS 한글 종목명 | String | 40 | Y | HTS 한글 종목명 |
| `-futs_prpr` | 현재가 | String | 14 | Y | 현재가 |
| `-futs_shrn_iscd` | 단축 종목코드 | String | 9 | Y | 단축 종목코드 |
| `-prdy_vol` | 전일 거래량 | String | 18 | Y | 전일 거래량 |
| `-futs_mxpr` | 상한가 | String | 14 | Y | 상한가 |
| `-futs_llam` | 하한가 | String | 14 | Y | 하한가 |
| `-futs_oprc` | 시가 | String | 14 | Y | 시가 |
| `-futs_hgpr` | 최고가 | String | 14 | Y | 최고가 |
| `-futs_lwpr` | 최저가 | String | 14 | Y | 최저가 |
| `-futs_prdy_oprc` | 전일 시가 | String | 14 | Y | 전일 시가 |
| `-futs_prdy_hgpr` | 전일 최고가 | String | 14 | Y | 전일 최고가 |
| `-futs_prdy_lwpr` | 전일 최저가 | String | 14 | Y | 전일 최저가 |
| `-futs_askp` | 매도호가 | String | 14 | Y | 매도호가 |
| `-futs_bidp` | 매수호가 | String | 14 | Y | 매수호가 |
| `-basis` | 베이시스 | String | 12 | Y | 베이시스 |
| `-kospi200_nmix` | KOSPI200 지수 | String | 14 | Y | KOSPI200 지수 |
| `-kospi200_prdy_vrss` | KOSPI200 전일 대비 | String | 14 | Y | KOSPI200 전일 대비 |
| `-kospi200_prdy_ctrt` | KOSPI200 전일 대비율 | String | 11 | Y | KOSPI200 전일 대비율 |
| `-kospi200_prdy_vrss_sign` | 전일 대비 부호 | String | 1 | Y | 전일 대비 부호 |
| `-hts_otst_stpl_qty` | HTS 미결제 약정 수량 | String | 18 | Y | HTS 미결제 약정 수량 |
| `-otst_stpl_qty_icdc` | 미결제 약정 수량 증감 | String | 10 | Y | 미결제 약정 수량 증감 |
| `-tday_rltv` | 당일 체결강도 | String | 14 | Y | 당일 체결강도 |
| `-hts_thpr` | HTS 이론가 | String | 14 | Y | HTS 이론가 |
| `-dprt` | 괴리율 | String | 11 | Y | 괴리율 |
| `output2` | 기간별 조회데이터 (배열) | String | 1 | Y | 기간별 조회데이터 (배열) |
| `-stck_bsop_date` | 영업 일자 | String | 8 | Y | 영업 일자 |
| `-futs_prpr` | 현재가 | String | 14 | Y | 현재가 |
| `-futs_oprc` | 시가  | String | 14 | Y | 시가 |
| `-futs_hgpr` | 최고가 | String | 14 | Y | 최고가 |
| `-futs_lwpr` | 최저가 | String | 14 | Y | 최저가 |
| `-acml_vol` | 누적 거래량 | String | 18 | Y | 누적 거래량 |
| `-acml_tr_pbmn` | 누적 거래 대금 | String | 18 | Y | 누적 거래 대금 |
| `-mod_yn` | 변경 여부 | String | 1 | Y | 변경 여부 |

### 응답 예시

```json
"output1": {
            "acml_tr_pbmn": "15491417875",
            "acml_vol": "178446",
            "basis": "0.28",
            "dprt": "-0.14",
            "futs_askp": "344.70",
            "futs_bidp": "344.65",
            "futs_hgpr": "349.75",
            "futs_llam": "322.65",
            "futs_lwpr": "344.65",
            "futs_mxpr": "378.75",
            "futs_oprc": "348.85",
            "futs_prdy_clpr": "350.70",
            "futs_prdy_ctrt": "-1.71",
            "futs_prdy_hgpr": "351.85",
            "futs_prdy_lwpr": "348.65",
            "futs_prdy_oprc": "351.55",
            "futs_prdy_vrss": "-6.00",
            "futs_prpr": "344.70",
            "futs_shrn_iscd": "101S06",
            "hts_kor_isnm": "F 202206",
            "hts_otst_stpl_qty": "297901",
            "hts_thpr": "345.17",
            "kospi200_nmix": "344.89",
            "otst_stpl_qty_icdc": "4348",
            "prdy_vol": "222987",
            "prdy_vrss_sign": "5",
            "tday_rltv": "92.20"
        },
        "output2": [
            {
                "acml_tr_pbmn": "15491417875",
                "acml_vol": "178446",
                "futs_hgpr": "349.75",
                "futs_lwpr": "344.65",
                "futs_oprc": "348.85",
                "futs_prpr": "344.70",
                "mod_yn": "N",
                "stck_bsop_date": "20220524"
            },
....
```
