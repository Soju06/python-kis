# 국내업종 구분별전체시세[v1_국내주식-066]

> [국내주식] 업종/기타

국내업종 구분별전체시세 API입니다.
한국투자 HTS(eFriend Plus) > [0214] 업종 전체시세 화면 의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `27bef4b4-cf83-4698-8f1e-16138cb09817` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/quotations/inquire-index-category-price` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `FHPUP02140000` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-02-16
- **최종 수정일**: 2025-05-14

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials G... |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | FHPUP02140000 |
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
| `FID_COND_MRKT_DIV_CODE` | FID 조건 시장 분류 코드 | String | 2 | Y | 시장구분코드 (업종 U) |
| `FID_INPUT_ISCD` | FID 입력 종목코드 | String | 12 | Y | 코스피(0001), 코스닥(1001), 코스피200(2001) ... 포탈 (FAQ : 종목정보 다운로드(국내) - 업종코드 참조) |
| `FID_COND_SCR_DIV_CODE` | FID 조건 화면 분류 코드 | String | 5 | Y | Unique key( 20214 ) |
| `FID_MRKT_CLS_CODE` | FID 시장 구분 코드 | String | 2 | Y | 시장구분코드(K:거래소, Q:코스닥, K2:코스피200) |
| `FID_BLNG_CLS_CODE` | FID 소속 구분 코드 | String | 2 | Y | 시장구분코드에 따라 아래와 같이 입력 시장구분코드(K:거래소) 0:전업종, 1:기타구분, 2:자본금구분 3:상업별구분 시장구분코드(Q:코스닥) 0:전업종, 1:기타구분, 2:... |

### 요청 예시

```json
{
  "fid_cond_mrkt_div_code": "U",
  "fid_input_iscd": "0001",
  "fid_cond_scr_div_code": "20214",
  "fid_mrkt_cls_code": "K2",
  "fid_blng_cls_code": "0"
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
| `output1` | 응답상세1 | String |   | Y |  |
| `bstp_nmix_prpr` | 업종 지수 현재가 | String | 112 | Y |  |
| `bstp_nmix_prdy_vrss` | 업종 지수 전일 대비 | String | 112 | Y |  |
| `prdy_vrss_sign` | 전일 대비 부호 | String | 1 | Y |  |
| `bstp_nmix_prdy_ctrt` | 업종 지수 전일 대비율 | String | 82 | Y |  |
| `acml_vol` | 누적 거래량 | String | 18 | Y |  |
| `acml_tr_pbmn` | 누적 거래 대금 | String | 18 | Y |  |
| `bstp_nmix_oprc` | 업종 지수 시가2 | String | 112 | Y |  |
| `bstp_nmix_hgpr` | 업종 지수 최고가 | String | 112 | Y |  |
| `bstp_nmix_lwpr` | 업종 지수 최저가 | String | 112 | Y |  |
| `prdy_vol` | 전일 거래량 | String | 18 | Y |  |
| `ascn_issu_cnt` | 상승 종목 수 | String | 7 | Y |  |
| `down_issu_cnt` | 하락 종목 수 | String | 7 | Y |  |
| `stnr_issu_cnt` | 보합 종목 수 | String | 7 | Y |  |
| `uplm_issu_cnt` | 상한 종목 수 | String | 7 | Y |  |
| `lslm_issu_cnt` | 하한 종목 수 | String | 7 | Y |  |
| `prdy_tr_pbmn` | 전일 거래 대금 | String | 18 | Y |  |
| `dryy_bstp_nmix_hgpr_date` | 연중업종지수최고가일자 | String | 8 | Y |  |
| `dryy_bstp_nmix_hgpr` | 연중업종지수최고가 | String | 112 | Y |  |
| `dryy_bstp_nmix_lwpr` | 연중업종지수최저가 | String | 112 | Y |  |
| `dryy_bstp_nmix_lwpr_date` | 연중업종지수최저가일자 | String | 8 | Y |  |
| `output2` | 응답상세2 | Object |   | Y | array |
| `bstp_cls_code` | 업종 구분 코드 | String | 4 | Y |  |
| `hts_kor_isnm` | HTS 한글 종목명 | String | 40 | Y |  |
| `bstp_nmix_prpr` | 업종 지수 현재가 | String | 112 | Y |  |
| `bstp_nmix_prdy_vrss` | 업종 지수 전일 대비 | String | 112 | Y |  |
| `prdy_vrss_sign` | 전일 대비 부호 | String | 1 | Y |  |
| `bstp_nmix_prdy_ctrt` | 업종 지수 전일 대비율 | String | 82 | Y |  |
| `acml_vol` | 누적 거래량 | String | 18 | Y |  |
| `acml_tr_pbmn` | 누적 거래 대금 | String | 18 | Y |  |
| `acml_vol_rlim` | 누적 거래량 비중 | String | 72 | Y |  |
| `acml_tr_pbmn_rlim` | 누적 거래 대금 비중 | String | 72 | Y |  |

### 응답 예시

```json
{
  "output1": {
    "bstp_nmix_prpr": "2648.76",
    "bstp_nmix_prdy_vrss": "34.96",
    "prdy_vrss_sign": "2",
    "bstp_nmix_prdy_ctrt": "1.34",
    "acml_vol": "584715",
    "acml_tr_pbmn": "10001487",
    "bstp_nmix_oprc": "2635.63",
    "bstp_nmix_hgpr": "2648.76",
    "bstp_nmix_lwpr": "2625.01",
    "prdy_vol": "621363",
    "ascn_issu_cnt": "628",
    "down_issu_cnt": "250",
    "stnr_issu_cnt": "58",
    "uplm_issu_cnt": "0",
    "lslm_issu_cnt": "0",
    "prdy_tr_pbmn": "10691024",
    "dryy_bstp_nmix_hgpr_date": "20240102",
    "dryy_bstp_nmix_hgpr": "2675.80",
    "dryy_bstp_nmix_lwpr": "2429.12",
    "dryy_bstp_nmix_lwpr_date": "20240118"
  },
  "output2": [
    {
      "bstp_cls_code": "2001",
      "hts_kor_isnm": "KOSPI200",
      "bstp_nmix_prpr": "355.52",
      "bstp_nmix_prdy_vrss": "4.31",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.23",
      "acml_vol": "118963",
      "acml_tr_pbmn": "7078909",
      "acml_vol_rlim": "100.00",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2007",
      "hts_kor_isnm": "KOSPI100",
      "bstp_nmix_prpr": "2691.34",
      "bstp_nmix_prdy_vrss": "33.27",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.25",
      "acml_vol": "76784",
      "acml_tr_pbmn": "6124444",
      "acml_vol_rlim": "64.54",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2008",
      "hts_kor_isnm": "KOSPI50",
      "bstp_nmix_prpr": "2478.39",
      "bstp_nmix_prdy_vrss": "28.83",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.18",
      "acml_vol": "52269",
      "acml_tr_pbmn": "5222300",
      "acml_vol_rlim": "43.94",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2039",
      "hts_kor_isnm": "K커뮤니케이션서비스",
      "bstp_nmix_prpr": "1850.38",
      "bstp_nmix_prdy_vrss": "3.14",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "0.17",
      "acml_vol": "5893",
      "acml_tr_pbmn": "477398",
      "acml_vol_rlim": "4.95",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2009",
      "hts_kor_isnm": "K건설",
      "bstp_nmix_prpr": "325.34",
      "bstp_nmix_prdy_vrss": "8.08",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "2.55",
      "acml_vol": "6636",
      "acml_tr_pbmn": "225841",
      "acml_vol_rlim": "5.58",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2010",
      "hts_kor_isnm": "K중공업",
      "bstp_nmix_prpr": "322.92",
      "bstp_nmix_prdy_vrss": "3.37",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.05",
      "acml_vol": "9613",
      "acml_tr_pbmn": "203930",
      "acml_vol_rlim": "8.08",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2011",
      "hts_kor_isnm": "K철강소재",
      "bstp_nmix_prpr": "884.98",
      "bstp_nmix_prdy_vrss": "35.05",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "4.12",
      "acml_vol": "4814",
      "acml_tr_pbmn": "456186",
      "acml_vol_rlim": "4.05",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2012",
      "hts_kor_isnm": "K에너지화학",
      "bstp_nmix_prpr": "1385.94",
      "bstp_nmix_prdy_vrss": "45.89",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "3.42",
      "acml_vol": "7623",
      "acml_tr_pbmn": "833756",
      "acml_vol_rlim": "6.41",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2013",
      "hts_kor_isnm": "K정보기술",
      "bstp_nmix_prpr": "3233.61",
      "bstp_nmix_prdy_vrss": "42.48",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.33",
      "acml_vol": "20799",
      "acml_tr_pbmn": "1899061",
      "acml_vol_rlim": "17.48",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2014",
      "hts_kor_isnm": "K금융",
      "bstp_nmix_prpr": "780.59",
      "bstp_nmix_prdy_vrss": "27.94",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "3.71",
      "acml_vol": "23753",
      "acml_tr_pbmn": "672909",
      "acml_vol_rlim": "19.97",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2015",
      "hts_kor_isnm": "K생활소비재",
      "bstp_nmix_prpr": "793.68",
      "bstp_nmix_prdy_vrss": "12.81",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.64",
      "acml_vol": "4244",
      "acml_tr_pbmn": "288488",
      "acml_vol_rlim": "3.57",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2016",
      "hts_kor_isnm": "K경기소비재",
      "bstp_nmix_prpr": "1724.67",
      "bstp_nmix_prdy_vrss": "42.88",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "2.55",
      "acml_vol": "10060",
      "acml_tr_pbmn": "1004566",
      "acml_vol_rlim": "8.46",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2017",
      "hts_kor_isnm": "K산업재",
      "bstp_nmix_prpr": "633.49",
      "bstp_nmix_prdy_vrss": "6.82",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.09",
      "acml_vol": "23323",
      "acml_tr_pbmn": "823914",
      "acml_vol_rlim": "19.61",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2018",
      "hts_kor_isnm": "K헬스케어",
      "bstp_nmix_prpr": "1840.09",
      "bstp_nmix_prdy_vrss": "14.36",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "0.79",
      "acml_vol": "2204",
      "acml_tr_pbmn": "192860",
      "acml_vol_rlim": "1.85",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2019",
      "hts_kor_isnm": "K고배당",
      "bstp_nmix_prpr": "3173.16",
      "bstp_nmix_prdy_vrss": "86.09",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "2.79",
      "acml_vol": "41569",
      "acml_tr_pbmn": "2859723",
      "acml_vol_rlim": "34.94",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2021",
      "hts_kor_isnm": "K200가치저변동성",
      "bstp_nmix_prpr": "5446.64",
      "bstp_nmix_prdy_vrss": "120.03",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "2.25",
      "acml_vol": "86859",
      "acml_tr_pbmn": "4469357",
      "acml_vol_rlim": "73.01",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2022",
      "hts_kor_isnm": "K200중소형주",
      "bstp_nmix_prpr": "1221.07",
      "bstp_nmix_prdy_vrss": "22.17",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.85",
      "acml_vol": "42179",
      "acml_tr_pbmn": "954465",
      "acml_vol_rlim": "35.46",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2023",
      "hts_kor_isnm": "K200경기방어소비재",
      "bstp_nmix_prpr": "903.55",
      "bstp_nmix_prdy_vrss": "8.98",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.00",
      "acml_vol": "8450",
      "acml_tr_pbmn": "550010",
      "acml_vol_rlim": "7.10",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2024",
      "hts_kor_isnm": "K200에너지화학 레버리지",
      "bstp_nmix_prpr": "836.53",
      "bstp_nmix_prdy_vrss": "53.55",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "6.84",
      "acml_vol": "0",
      "acml_tr_pbmn": "0",
      "acml_vol_rlim": "0.00",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2025",
      "hts_kor_isnm": "K200정보기술 레버리지",
      "bstp_nmix_prpr": "4350.42",
      "bstp_nmix_prdy_vrss": "112.40",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "2.65",
      "acml_vol": "0",
      "acml_tr_pbmn": "0",
      "acml_vol_rlim": "0.00",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2026",
      "hts_kor_isnm": "K200금융 레버리지",
      "bstp_nmix_prpr": "517.48",
      "bstp_nmix_prdy_vrss": "35.72",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "7.41",
      "acml_vol": "0",
      "acml_tr_pbmn": "0",
      "acml_vol_rlim": "0.00",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2027",
      "hts_kor_isnm": "K200경기소비재 레버리지",
      "bstp_nmix_prpr": "989.98",
      "bstp_nmix_prdy_vrss": "47.94",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "5.09",
      "acml_vol": "0",
      "acml_tr_pbmn": "0",
      "acml_vol_rlim": "0.00",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2035",
      "hts_kor_isnm": "코스피200 TR",
      "bstp_nmix_prpr": "449.66",
      "bstp_nmix_prdy_vrss": "5.45",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.23",
      "acml_vol": "0",
      "acml_tr_pbmn": "0",
      "acml_vol_rlim": "0.00",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2036",
      "hts_kor_isnm": "코스피200 NTR",
      "bstp_nmix_prpr": "433.34",
      "bstp_nmix_prdy_vrss": "5.25",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.23",
      "acml_vol": "0",
      "acml_tr_pbmn": "0",
      "acml_vol_rlim": "0.00",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2028",
      "hts_kor_isnm": "K200건설 레버리지",
      "bstp_nmix_prpr": "204.06",
      "bstp_nmix_prdy_vrss": "9.87",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "5.08",
      "acml_vol": "0",
      "acml_tr_pbmn": "0",
      "acml_vol_rlim": "0.00",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2029",
      "hts_kor_isnm": "K200중공업 레버리지",
      "bstp_nmix_prpr": "169.43",
      "bstp_nmix_prdy_vrss": "3.48",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "2.10",
      "acml_vol": "0",
      "acml_tr_pbmn": "0",
      "acml_vol_rlim": "0.00",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2030",
      "hts_kor_isnm": "K200헬스케어 레버리지",
      "bstp_nmix_prpr": "659.07",
      "bstp_nmix_prdy_vrss": "10.14",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.56",
      "acml_vol": "0",
      "acml_tr_pbmn": "0",
      "acml_vol_rlim": "0.00",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2040",
      "hts_kor_isnm": "코스피200 초대형 제외지수",
      "bstp_nmix_prpr": "256.52",
      "bstp_nmix_prdy_vrss": "4.70",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.87",
      "acml_vol": "105736",
      "acml_tr_pbmn": "6115607",
      "acml_vol_rlim": "88.88",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2037",
      "hts_kor_isnm": "코스피200 예측 고배당 50",
      "bstp_nmix_prpr": "1989.88",
      "bstp_nmix_prdy_vrss": "49.77",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "2.57",
      "acml_vol": "22491",
      "acml_tr_pbmn": "1659649",
      "acml_vol_rlim": "18.91",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2038",
      "hts_kor_isnm": "코스피200 예측 배당성장 50",
      "bstp_nmix_prpr": "1661.50",
      "bstp_nmix_prdy_vrss": "33.18",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "2.04",
      "acml_vol": "39463",
      "acml_tr_pbmn": "2424471",
      "acml_vol_rlim": "33.17",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2041",
      "hts_kor_isnm": "K200 정보기술 TR",
      "bstp_nmix_prpr": "3742.21",
      "bstp_nmix_prdy_vrss": "49.16",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.33",
      "acml_vol": "0",
      "acml_tr_pbmn": "0",
      "acml_vol_rlim": "0.00",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2042",
      "hts_kor_isnm": "K200 금융 TR",
      "bstp_nmix_prpr": "1192.40",
      "bstp_nmix_prdy_vrss": "42.68",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "3.71",
      "acml_vol": "0",
      "acml_tr_pbmn": "0",
      "acml_vol_rlim": "0.00",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2044",
      "hts_kor_isnm": "K200 에너지화학 TR",
      "bstp_nmix_prpr": "1786.68",
      "bstp_nmix_prdy_vrss": "59.16",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "3.42",
      "acml_vol": "0",
      "acml_tr_pbmn": "0",
      "acml_vol_rlim": "0.00",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2045",
      "hts_kor_isnm": "K200 생활소비재 TR",
      "bstp_nmix_prpr": "1031.76",
      "bstp_nmix_prdy_vrss": "16.65",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.64",
      "acml_vol": "0",
      "acml_tr_pbmn": "0",
      "acml_vol_rlim": "0.00",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2046",
      "hts_kor_isnm": "K200 건설 TR",
      "bstp_nmix_prpr": "386.22",
      "bstp_nmix_prdy_vrss": "9.59",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "2.55",
      "acml_vol": "0",
      "acml_tr_pbmn": "0",
      "acml_vol_rlim": "0.00",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2047",
      "hts_kor_isnm": "K200 중공업 TR",
      "bstp_nmix_prpr": "356.92",
      "bstp_nmix_prdy_vrss": "3.72",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.05",
      "acml_vol": "0",
      "acml_tr_pbmn": "0",
      "acml_vol_rlim": "0.00",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2048",
      "hts_kor_isnm": "K200 철강소재 TR",
      "bstp_nmix_prpr": "1172.71",
      "bstp_nmix_prdy_vrss": "46.45",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "4.12",
      "acml_vol": "0",
      "acml_tr_pbmn": "0",
      "acml_vol_rlim": "0.00",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2049",
      "hts_kor_isnm": "K200 산업재 TR",
      "bstp_nmix_prpr": "753.63",
      "bstp_nmix_prdy_vrss": "8.11",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.09",
      "acml_vol": "0",
      "acml_tr_pbmn": "0",
      "acml_vol_rlim": "0.00",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2050",
      "hts_kor_isnm": "K200 헬스케어 TR",
      "bstp_nmix_prpr": "1966.27",
      "bstp_nmix_prdy_vrss": "15.34",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "0.79",
      "acml_vol": "0",
      "acml_tr_pbmn": "0",
      "acml_vol_rlim": "0.00",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2051",
      "hts_kor_isnm": "K200 커뮤니케이션서비스 TR",
      "bstp_nmix_prpr": "2355.58",
      "bstp_nmix_prdy_vrss": "4.00",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "0.17",
      "acml_vol": "0",
      "acml_tr_pbmn": "0",
      "acml_vol_rlim": "0.00",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2224",
      "hts_kor_isnm": "K200 비중상한 30%",
      "bstp_nmix_prpr": "355.08",
      "bstp_nmix_prdy_vrss": "4.37",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.25",
      "acml_vol": "118963",
      "acml_tr_pbmn": "7078909",
      "acml_vol_rlim": "100.00",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2225",
      "hts_kor_isnm": "K200 비중상한 30%  TR",
      "bstp_nmix_prpr": "449.00",
      "bstp_nmix_prdy_vrss": "5.53",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.25",
      "acml_vol": "0",
      "acml_tr_pbmn": "0",
      "acml_vol_rlim": "0.00",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2226",
      "hts_kor_isnm": "K200 비중상한 30%  NTR",
      "bstp_nmix_prpr": "432.91",
      "bstp_nmix_prdy_vrss": "5.33",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.25",
      "acml_vol": "0",
      "acml_tr_pbmn": "0",
      "acml_vol_rlim": "0.00",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2227",
      "hts_kor_isnm": "K200 비중상한 25%",
      "bstp_nmix_prpr": "351.32",
      "bstp_nmix_prdy_vrss": "4.69",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.35",
      "acml_vol": "118963",
      "acml_tr_pbmn": "7078909",
      "acml_vol_rlim": "100.00",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2228",
      "hts_kor_isnm": "K200 비중상한 25%  TR",
      "bstp_nmix_prpr": "444.32",
      "bstp_nmix_prdy_vrss": "5.93",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.35",
      "acml_vol": "0",
      "acml_tr_pbmn": "0",
      "acml_vol_rlim": "0.00",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2230",
      "hts_kor_isnm": "K200 비중상한 25%  NTR",
      "bstp_nmix_prpr": "428.34",
      "bstp_nmix_prdy_vrss": "5.72",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.35",
      "acml_vol": "0",
      "acml_tr_pbmn": "0",
      "acml_vol_rlim": "0.00",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2232",
      "hts_kor_isnm": "K200 비중상한 20%",
      "bstp_nmix_prpr": "341.02",
      "bstp_nmix_prdy_vrss": "4.89",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.45",
      "acml_vol": "118963",
      "acml_tr_pbmn": "7078909",
      "acml_vol_rlim": "100.00",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2233",
      "hts_kor_isnm": "K200 비중상한 20%  TR",
      "bstp_nmix_prpr": "430.39",
      "bstp_nmix_prdy_vrss": "6.17",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.45",
      "acml_vol": "0",
      "acml_tr_pbmn": "0",
      "acml_vol_rlim": "0.00",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2235",
      "hts_kor_isnm": "K200 비중상한 20%  NTR",
      "bstp_nmix_prpr": "415.42",
      "bstp_nmix_prdy_vrss": "5.96",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.46",
      "acml_vol": "0",
      "acml_tr_pbmn": "0",
      "acml_vol_rlim": "0.00",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2043",
      "hts_kor_isnm": "K200 경기소비재 TR",
      "bstp_nmix_prpr": "2152.99",
      "bstp_nmix_prdy_vrss": "53.53",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "2.55",
      "acml_vol": "0",
      "acml_tr_pbmn": "0",
      "acml_vol_rlim": "0.00",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2284",
      "hts_kor_isnm": "코스피 200 선물지수 TWAP형",
      "bstp_nmix_prpr": "1786.47",
      "bstp_nmix_prdy_vrss": "18.33",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.04",
      "acml_vol": "0",
      "acml_tr_pbmn": "0",
      "acml_vol_rlim": "0.00",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2285",
      "hts_kor_isnm": "코스피 200 선물 TWAP 인버스지수",
      "bstp_nmix_prpr": "2555.41",
      "bstp_nmix_prdy_vrss": "-26.53",
      "prdy_vrss_sign": "5",
      "bstp_nmix_prdy_ctrt": "-1.03",
      "acml_vol": "0",
      "acml_tr_pbmn": "0",
      "acml_vol_rlim": "0.00",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2286",
      "hts_kor_isnm": "코스피 200 선물 TWAP 레버리지",
      "bstp_nmix_prpr": "1448.92",
      "bstp_nmix_prdy_vrss": "29.55",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "2.08",
      "acml_vol": "0",
      "acml_tr_pbmn": "0",
      "acml_vol_rlim": "0.00",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2287",
      "hts_kor_isnm": "코스피 200 선물 TWAP 인버스-2X",
      "bstp_nmix_prpr": "2598.71",
      "bstp_nmix_prdy_vrss": "-54.80",
      "prdy_vrss_sign": "5",
      "bstp_nmix_prdy_ctrt": "-2.07",
      "acml_vol": "0",
      "acml_tr_pbmn": "0",
      "acml_vol_rlim": "0.00",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2751",
      "hts_kor_isnm": "F-K200 에너지/화학",
      "bstp_nmix_prpr": "1201.20",
      "bstp_nmix_prdy_vrss": "34.48",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "2.96",
      "acml_vol": "0",
      "acml_tr_pbmn": "0",
      "acml_vol_rlim": "0.00",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2752",
      "hts_kor_isnm": "F-K200 정보기술",
      "bstp_nmix_prpr": "2051.35",
      "bstp_nmix_prdy_vrss": "18.30",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "0.90",
      "acml_vol": "0",
      "acml_tr_pbmn": "0",
      "acml_vol_rlim": "0.00",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2753",
      "hts_kor_isnm": "F-K200 금융",
      "bstp_nmix_prpr": "1291.69",
      "bstp_nmix_prdy_vrss": "40.86",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "3.27",
      "acml_vol": "0",
      "acml_tr_pbmn": "0",
      "acml_vol_rlim": "0.00",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2754",
      "hts_kor_isnm": "F-K200 경기소비재",
      "bstp_nmix_prpr": "1121.37",
      "bstp_nmix_prdy_vrss": "17.42",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.58",
      "acml_vol": "0",
      "acml_tr_pbmn": "0",
      "acml_vol_rlim": "0.00",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2755",
      "hts_kor_isnm": "F-K200 건설",
      "bstp_nmix_prpr": "1218.34",
      "bstp_nmix_prdy_vrss": "25.51",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "2.14",
      "acml_vol": "0",
      "acml_tr_pbmn": "0",
      "acml_vol_rlim": "0.00",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2756",
      "hts_kor_isnm": "F-K200 중공업",
      "bstp_nmix_prpr": "962.17",
      "bstp_nmix_prdy_vrss": "8.96",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "0.94",
      "acml_vol": "0",
      "acml_tr_pbmn": "0",
      "acml_vol_rlim": "0.00",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2757",
      "hts_kor_isnm": "F-K200 헬스케어",
      "bstp_nmix_prpr": "963.71",
      "bstp_nmix_prdy_vrss": "2.84",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "0.30",
      "acml_vol": "0",
      "acml_tr_pbmn": "0",
      "acml_vol_rlim": "0.00",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2758",
      "hts_kor_isnm": "F-K200 생활소비재",
      "bstp_nmix_prpr": "637.56",
      "bstp_nmix_prdy_vrss": "1.77",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "0.28",
      "acml_vol": "0",
      "acml_tr_pbmn": "0",
      "acml_vol_rlim": "0.00",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2759",
      "hts_kor_isnm": "F-K200 철강/소재",
      "bstp_nmix_prpr": "903.55",
      "bstp_nmix_prdy_vrss": "0.00",
      "prdy_vrss_sign": "3",
      "bstp_nmix_prdy_ctrt": "0.00",
      "acml_vol": "0",
      "acml_tr_pbmn": "0",
      "acml_vol_rlim": "0.00",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2760",
      "hts_kor_isnm": "F-K200 산업재",
      "bstp_nmix_prpr": "1031.59",
      "bstp_nmix_prdy_vrss": "7.80",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "0.76",
      "acml_vol": "0",
      "acml_tr_pbmn": "0",
      "acml_vol_rlim": "0.00",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2761",
      "hts_kor_isnm": "F-K200 에너지/화학  레버리지",
      "bstp_nmix_prpr": "1039.81",
      "bstp_nmix_prdy_vrss": "58.10",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "5.92",
      "acml_vol": "0",
      "acml_tr_pbmn": "0",
      "acml_vol_rlim": "0.00",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2762",
      "hts_kor_isnm": "F-K200 정보기술  레버리지",
      "bstp_nmix_prpr": "3228.56",
      "bstp_nmix_prdy_vrss": "57.34",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.81",
      "acml_vol": "0",
      "acml_tr_pbmn": "0",
      "acml_vol_rlim": "0.00",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2763",
      "hts_kor_isnm": "F-K200 금융  레버리지",
      "bstp_nmix_prpr": "1311.74",
      "bstp_nmix_prdy_vrss": "80.53",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "6.54",
      "acml_vol": "0",
      "acml_tr_pbmn": "0",
      "acml_vol_rlim": "0.00",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2764",
      "hts_kor_isnm": "F-K200 경기소비재  레버리지",
      "bstp_nmix_prpr": "1001.75",
      "bstp_nmix_prdy_vrss": "30.72",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "3.16",
      "acml_vol": "0",
      "acml_tr_pbmn": "0",
      "acml_vol_rlim": "0.00",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2765",
      "hts_kor_isnm": "F-K200 건설  레버리지",
      "bstp_nmix_prpr": "976.07",
      "bstp_nmix_prdy_vrss": "40.10",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "4.28",
      "acml_vol": "0",
      "acml_tr_pbmn": "0",
      "acml_vol_rlim": "0.00",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2766",
      "hts_kor_isnm": "F-K200 중공업  레버리지",
      "bstp_nmix_prpr": "532.58",
      "bstp_nmix_prdy_vrss": "9.86",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.89",
      "acml_vol": "0",
      "acml_tr_pbmn": "0",
      "acml_vol_rlim": "0.00",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2767",
      "hts_kor_isnm": "F-K200 헬스케어  레버리지",
      "bstp_nmix_prpr": "610.89",
      "bstp_nmix_prdy_vrss": "3.63",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "0.60",
      "acml_vol": "0",
      "acml_tr_pbmn": "0",
      "acml_vol_rlim": "0.00",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2768",
      "hts_kor_isnm": "F-K200 생활소비재  레버리지",
      "bstp_nmix_prpr": "376.44",
      "bstp_nmix_prdy_vrss": "2.12",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "0.57",
      "acml_vol": "0",
      "acml_tr_pbmn": "0",
      "acml_vol_rlim": "0.00",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2769",
      "hts_kor_isnm": "F-K200 철강/소재  레버리지",
      "bstp_nmix_prpr": "546.02",
      "bstp_nmix_prdy_vrss": "0.04",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "0.01",
      "acml_vol": "0",
      "acml_tr_pbmn": "0",
      "acml_vol_rlim": "0.00",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2770",
      "hts_kor_isnm": "F-K200 산업재  레버리지",
      "bstp_nmix_prpr": "868.46",
      "bstp_nmix_prdy_vrss": "13.10",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.53",
      "acml_vol": "0",
      "acml_tr_pbmn": "0",
      "acml_vol_rlim": "0.00",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2771",
      "hts_kor_isnm": "F-K200 에너지/화학  인버스",
      "bstp_nmix_prpr": "607.50",
      "bstp_nmix_prdy_vrss": "-18.44",
      "prdy_vrss_sign": "5",
      "bstp_nmix_prdy_ctrt": "-2.95",
      "acml_vol": "0",
      "acml_tr_pbmn": "0",
      "acml_vol_rlim": "0.00",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2772",
      "hts_kor_isnm": "F-K200 정보기술  인버스",
      "bstp_nmix_prpr": "379.71",
      "bstp_nmix_prdy_vrss": "-3.41",
      "prdy_vrss_sign": "5",
      "bstp_nmix_prdy_ctrt": "-0.89",
      "acml_vol": "0",
      "acml_tr_pbmn": "0",
      "acml_vol_rlim": "0.00",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2773",
      "hts_kor_isnm": "F-K200 금융  인버스",
      "bstp_nmix_prpr": "615.73",
      "bstp_nmix_prdy_vrss": "-20.73",
      "prdy_vrss_sign": "5",
      "bstp_nmix_prdy_ctrt": "-3.26",
      "acml_vol": "0",
      "acml_tr_pbmn": "0",
      "acml_vol_rlim": "0.00",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2774",
      "hts_kor_isnm": "F-K200 경기소비재  인버스",
      "bstp_nmix_prpr": "713.85",
      "bstp_nmix_prdy_vrss": "-11.38",
      "prdy_vrss_sign": "5",
      "bstp_nmix_prdy_ctrt": "-1.57",
      "acml_vol": "0",
      "acml_tr_pbmn": "0",
      "acml_vol_rlim": "0.00",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2775",
      "hts_kor_isnm": "F-K200 건설  인버스",
      "bstp_nmix_prpr": "551.53",
      "bstp_nmix_prdy_vrss": "-12.00",
      "prdy_vrss_sign": "5",
      "bstp_nmix_prdy_ctrt": "-2.13",
      "acml_vol": "0",
      "acml_tr_pbmn": "0",
      "acml_vol_rlim": "0.00",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2776",
      "hts_kor_isnm": "F-K200 중공업  인버스",
      "bstp_nmix_prpr": "613.84",
      "bstp_nmix_prdy_vrss": "-5.77",
      "prdy_vrss_sign": "5",
      "bstp_nmix_prdy_ctrt": "-0.93",
      "acml_vol": "0",
      "acml_tr_pbmn": "0",
      "acml_vol_rlim": "0.00",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2777",
      "hts_kor_isnm": "F-K200 헬스케어  인버스",
      "bstp_nmix_prpr": "698.18",
      "bstp_nmix_prdy_vrss": "-2.01",
      "prdy_vrss_sign": "5",
      "bstp_nmix_prdy_ctrt": "-0.29",
      "acml_vol": "0",
      "acml_tr_pbmn": "0",
      "acml_vol_rlim": "0.00",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2778",
      "hts_kor_isnm": "F-K200 생활소비재  인버스",
      "bstp_nmix_prpr": "1469.54",
      "bstp_nmix_prdy_vrss": "-3.97",
      "prdy_vrss_sign": "5",
      "bstp_nmix_prdy_ctrt": "-0.27",
      "acml_vol": "0",
      "acml_tr_pbmn": "0",
      "acml_vol_rlim": "0.00",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2779",
      "hts_kor_isnm": "F-K200 철강/소재  인버스",
      "bstp_nmix_prpr": "753.46",
      "bstp_nmix_prdy_vrss": "0.07",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "0.01",
      "acml_vol": "0",
      "acml_tr_pbmn": "0",
      "acml_vol_rlim": "0.00",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2780",
      "hts_kor_isnm": "F-K200 산업재  선물 인버스",
      "bstp_nmix_prpr": "798.93",
      "bstp_nmix_prdy_vrss": "-6.06",
      "prdy_vrss_sign": "5",
      "bstp_nmix_prdy_ctrt": "-0.75",
      "acml_vol": "0",
      "acml_tr_pbmn": "0",
      "acml_vol_rlim": "0.00",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2781",
      "hts_kor_isnm": "F-K200 에너지/화학  인버스-2X",
      "bstp_nmix_prpr": "207.08",
      "bstp_nmix_prdy_vrss": "-12.99",
      "prdy_vrss_sign": "5",
      "bstp_nmix_prdy_ctrt": "-5.90",
      "acml_vol": "0",
      "acml_tr_pbmn": "0",
      "acml_vol_rlim": "0.00",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2782",
      "hts_kor_isnm": "F-K200 정보기술  인버스-2X",
      "bstp_nmix_prpr": "86.70",
      "bstp_nmix_prdy_vrss": "-1.58",
      "prdy_vrss_sign": "5",
      "bstp_nmix_prdy_ctrt": "-1.79",
      "acml_vol": "0",
      "acml_tr_pbmn": "0",
      "acml_vol_rlim": "0.00",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2783",
      "hts_kor_isnm": "F-K200 금융  인버스-2X",
      "bstp_nmix_prpr": "232.04",
      "bstp_nmix_prdy_vrss": "-16.20",
      "prdy_vrss_sign": "5",
      "bstp_nmix_prdy_ctrt": "-6.53",
      "acml_vol": "0",
      "acml_tr_pbmn": "0",
      "acml_vol_rlim": "0.00",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2784",
      "hts_kor_isnm": "F-K200 경기소비재  인버스-2X",
      "bstp_nmix_prpr": "310.97",
      "bstp_nmix_prdy_vrss": "-10.11",
      "prdy_vrss_sign": "5",
      "bstp_nmix_prdy_ctrt": "-3.15",
      "acml_vol": "0",
      "acml_tr_pbmn": "0",
      "acml_vol_rlim": "0.00",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2785",
      "hts_kor_isnm": "F-K200 건설  인버스-2X",
      "bstp_nmix_prpr": "158.06",
      "bstp_nmix_prdy_vrss": "-7.05",
      "prdy_vrss_sign": "5",
      "bstp_nmix_prdy_ctrt": "-4.27",
      "acml_vol": "0",
      "acml_tr_pbmn": "0",
      "acml_vol_rlim": "0.00",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2786",
      "hts_kor_isnm": "F-K200 중공업  인버스-2X",
      "bstp_nmix_prpr": "172.11",
      "bstp_nmix_prdy_vrss": "-3.29",
      "prdy_vrss_sign": "5",
      "bstp_nmix_prdy_ctrt": "-1.88",
      "acml_vol": "0",
      "acml_tr_pbmn": "0",
      "acml_vol_rlim": "0.00",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2787",
      "hts_kor_isnm": "F-K200 헬스케어  인버스-2X",
      "bstp_nmix_prpr": "254.68",
      "bstp_nmix_prdy_vrss": "-1.50",
      "prdy_vrss_sign": "5",
      "bstp_nmix_prdy_ctrt": "-0.59",
      "acml_vol": "0",
      "acml_tr_pbmn": "0",
      "acml_vol_rlim": "0.00",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2788",
      "hts_kor_isnm": "F-K200 생활소비재  인버스-2X",
      "bstp_nmix_prpr": "1562.88",
      "bstp_nmix_prdy_vrss": "-8.62",
      "prdy_vrss_sign": "5",
      "bstp_nmix_prdy_ctrt": "-0.55",
      "acml_vol": "0",
      "acml_tr_pbmn": "0",
      "acml_vol_rlim": "0.00",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2789",
      "hts_kor_isnm": "F-K200 철강/소재  인버스-2X",
      "bstp_nmix_prpr": "298.75",
      "bstp_nmix_prdy_vrss": "0.02",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "0.01",
      "acml_vol": "0",
      "acml_tr_pbmn": "0",
      "acml_vol_rlim": "0.00",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2790",
      "hts_kor_isnm": "F-K200 산업재  인버스-2X",
      "bstp_nmix_prpr": "404.69",
      "bstp_nmix_prdy_vrss": "-6.23",
      "prdy_vrss_sign": "5",
      "bstp_nmix_prdy_ctrt": "-1.52",
      "acml_vol": "0",
      "acml_tr_pbmn": "0",
      "acml_vol_rlim": "0.00",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2501",
      "hts_kor_isnm": "K200선물",
      "bstp_nmix_prpr": "1785.82",
      "bstp_nmix_prdy_vrss": "18.32",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.04",
      "acml_vol": "0",
      "acml_tr_pbmn": "0",
      "acml_vol_rlim": "0.00",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2502",
      "hts_kor_isnm": "F-K200 인버스",
      "bstp_nmix_prpr": "552.50",
      "bstp_nmix_prdy_vrss": "-5.73",
      "prdy_vrss_sign": "5",
      "bstp_nmix_prdy_ctrt": "-1.03",
      "acml_vol": "0",
      "acml_tr_pbmn": "0",
      "acml_vol_rlim": "0.00",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2505",
      "hts_kor_isnm": "K200커버드콜 5% OTM",
      "bstp_nmix_prpr": "351.22",
      "bstp_nmix_prdy_vrss": "3.87",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.11",
      "acml_vol": "0",
      "acml_tr_pbmn": "0",
      "acml_vol_rlim": "0.00",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2506",
      "hts_kor_isnm": "K200프로텍티브풋 5% OTM",
      "bstp_nmix_prpr": "164.55",
      "bstp_nmix_prdy_vrss": "1.74",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.07",
      "acml_vol": "0",
      "acml_tr_pbmn": "0",
      "acml_vol_rlim": "0.00",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "6282",
      "hts_kor_isnm": "코스피 200 NTR 고정배당 8 포인트 지수",
      "bstp_nmix_prpr": "350.56",
      "bstp_nmix_prdy_vrss": "4.23",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.22",
      "acml_vol": "0",
      "acml_tr_pbmn": "0",
      "acml_vol_rlim": "0.00",
      "acml_tr_pbmn_rlim": ""
    },
    {
      "bstp_cls_code": "2705",
      "hts_kor_isnm": "F-K200 인버스-2X",
      "bstp_nmix_prpr": "263.40",
      "bstp_nmix_prdy_vrss": "-5.55",
      "prdy_vrss_sign": "5",
      "bstp_nmix_prdy_ctrt": "-2.06",
      "acml_vol": "0",
      "acml_tr_pbmn": "0",
      "acml_vol_rlim": "0.00",
      "acml_tr_pbmn_rlim": ""
    }
  ],
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```

