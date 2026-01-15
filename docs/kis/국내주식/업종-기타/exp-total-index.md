# 국내주식 예상체결 전체지수[국내주식-122]

> [국내주식] 업종/기타

국내주식 예상체결 전체지수 API입니다.
한국투자 HTS(eFriend Plus) > [0185] 예상체결 전체지수 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `7d1b2345-32f8-463b-9f41-8b4602387d52` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/quotations/exp-total-index` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID** | `모의투자 미지원`, `FHKUP11750000` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-03-15
- **최종 수정일**: 2025-05-14

## 요청 (Request)

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials G... |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | FHKUP11750000 |
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
| `fid_mrkt_cls_code` | 시장 구분 코드 | String | 2 | Y | 0:전체 K:거래소 Q:코스닥 |
| `fid_cond_mrkt_div_code` | 조건 시장 분류 코드 | String | 2 | Y | 시장구분코드 (업종 U) |
| `fid_cond_scr_div_code` | 조건 화면 분류 코드 | String | 5 | Y | Unique key(11175) |
| `fid_input_iscd` | 입력 종목코드 | String | 12 | Y | 0000:전체, 0001:거래소, 1001:코스닥, 2001:코스피200, 4001: KRX100 |
| `fid_mkop_cls_code` | 장운영 구분 코드 | String | 2 | Y | 1:장시작전, 2:장마감 |

### 요청 예시

```json
{
  "fid_cond_mrkt_div_code": "U",
  "fid_cond_scr_div_code": "11175",
  "fid_input_iscd": "1001",
  "fid_mkop_cls_code": "1",
  "fid_mrkt_cls_code": "K"
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
| `output1` | 응답상세 | String |   | Y |  |
| `bstp_nmix_prpr` | 업종 지수 현재가 | String | 112 | Y |  |
| `bstp_nmix_prdy_vrss` | 업종 지수 전일 대비 | String | 112 | Y |  |
| `prdy_vrss_sign` | 전일 대비 부호 | String | 1 | Y |  |
| `prdy_ctrt` | 전일 대비율 | String | 82 | Y |  |
| `acml_vol` | 누적 거래량 | String | 18 | Y |  |
| `ascn_issu_cnt` | 상승 종목 수 | String | 7 | Y |  |
| `down_issu_cnt` | 하락 종목 수 | String | 7 | Y |  |
| `stnr_issu_cnt` | 보합 종목 수 | String | 7 | Y |  |
| `bstp_cls_code` | 업종 구분 코드 | String | 4 | Y |  |
| `output2` | 응답상세 | Object |   | Y | array |
| `hts_kor_isnm` | HTS 한글 종목명 | String | 40 | Y |  |
| `bstp_nmix_prpr` | 업종 지수 현재가 | String | 112 | Y |  |
| `bstp_nmix_prdy_vrss` | 업종 지수 전일 대비 | String | 112 | Y |  |
| `prdy_vrss_sign` | 전일 대비 부호 | String | 1 | Y |  |
| `bstp_nmix_prdy_ctrt` | 업종 지수 전일 대비율 | String | 82 | Y |  |
| `acml_vol` | 누적 거래량 | String | 18 | Y |  |
| `nmix_sdpr` | 지수 기준가 | String | 112 | Y |  |
| `ascn_issu_cnt` | 상승 종목 수 | String | 7 | Y |  |
| `stnr_issu_cnt` | 보합 종목 수 | String | 7 | Y |  |
| `down_issu_cnt` | 하락 종목 수 | String | 7 | Y |  |

### 응답 예시

```json
{
  "output1": {
    "bstp_nmix_prpr": "883.03",
    "bstp_nmix_prdy_vrss": "2.57",
    "prdy_vrss_sign": "2",
    "prdy_ctrt": "0.29",
    "acml_vol": "10611",
    "ascn_issu_cnt": "513",
    "down_issu_cnt": "571",
    "stnr_issu_cnt": "498"
  },
  "output2": [
    {
      "bstp_cls_code": "0001",
      "hts_kor_isnm": "종합",
      "bstp_nmix_prpr": "2676.62",
      "bstp_nmix_prdy_vrss": "9.78",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "0.37",
      "acml_vol": "5151",
      "nmix_sdpr": "2666.84",
      "ascn_issu_cnt": "409",
      "stnr_issu_cnt": "249",
      "down_issu_cnt": "225"
    },
    {
      "bstp_cls_code": "2001",
      "hts_kor_isnm": "KOSPI200",
      "bstp_nmix_prpr": "360.44",
      "bstp_nmix_prdy_vrss": "1.05",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "0.29",
      "acml_vol": "1687",
      "nmix_sdpr": "359.39",
      "ascn_issu_cnt": "148",
      "stnr_issu_cnt": "35",
      "down_issu_cnt": "17"
    },
    {
      "bstp_cls_code": "2039",
      "hts_kor_isnm": "K커뮤니케이션서비스",
      "bstp_nmix_prpr": "1766.78",
      "bstp_nmix_prdy_vrss": "9.03",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "0.51",
      "acml_vol": "42",
      "nmix_sdpr": "1757.75",
      "ascn_issu_cnt": "7",
      "stnr_issu_cnt": "2",
      "down_issu_cnt": "1"
    },
    {
      "bstp_cls_code": "2009",
      "hts_kor_isnm": "K건설",
      "bstp_nmix_prpr": "320.87",
      "bstp_nmix_prdy_vrss": "0.09",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "0.03",
      "acml_vol": "76",
      "nmix_sdpr": "320.78",
      "ascn_issu_cnt": "3",
      "stnr_issu_cnt": "6",
      "down_issu_cnt": "1"
    },
    {
      "bstp_cls_code": "2010",
      "hts_kor_isnm": "K중공업",
      "bstp_nmix_prpr": "366.27",
      "bstp_nmix_prdy_vrss": "5.35",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.48",
      "acml_vol": "457",
      "nmix_sdpr": "360.92",
      "ascn_issu_cnt": "12",
      "stnr_issu_cnt": "0",
      "down_issu_cnt": "1"
    },
    {
      "bstp_cls_code": "2011",
      "hts_kor_isnm": "K철강소재",
      "bstp_nmix_prpr": "857.19",
      "bstp_nmix_prdy_vrss": "6.34",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "0.75",
      "acml_vol": "45",
      "nmix_sdpr": "850.85",
      "ascn_issu_cnt": "7",
      "stnr_issu_cnt": "3",
      "down_issu_cnt": "1"
    },
    {
      "bstp_cls_code": "2012",
      "hts_kor_isnm": "K에너지화학",
      "bstp_nmix_prpr": "1349.16",
      "bstp_nmix_prdy_vrss": "8.62",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "0.64",
      "acml_vol": "33",
      "nmix_sdpr": "1340.54",
      "ascn_issu_cnt": "22",
      "stnr_issu_cnt": "4",
      "down_issu_cnt": "2"
    },
    {
      "bstp_cls_code": "2013",
      "hts_kor_isnm": "K정보기술",
      "bstp_nmix_prpr": "3334.19",
      "bstp_nmix_prdy_vrss": "3.80",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "0.11",
      "acml_vol": "546",
      "nmix_sdpr": "3330.39",
      "ascn_issu_cnt": "8",
      "stnr_issu_cnt": "3",
      "down_issu_cnt": "2"
    },
    {
      "bstp_cls_code": "2014",
      "hts_kor_isnm": "K금융",
      "bstp_nmix_prpr": "832.71",
      "bstp_nmix_prdy_vrss": "-2.77",
      "prdy_vrss_sign": "5",
      "bstp_nmix_prdy_ctrt": "-0.33",
      "acml_vol": "208",
      "nmix_sdpr": "835.48",
      "ascn_issu_cnt": "12",
      "stnr_issu_cnt": "7",
      "down_issu_cnt": "3"
    },
    {
      "bstp_cls_code": "2015",
      "hts_kor_isnm": "K생활소비재",
      "bstp_nmix_prpr": "807.22",
      "bstp_nmix_prdy_vrss": "5.94",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "0.74",
      "acml_vol": "39",
      "nmix_sdpr": "801.28",
      "ascn_issu_cnt": "20",
      "stnr_issu_cnt": "3",
      "down_issu_cnt": "1"
    },
    {
      "bstp_cls_code": "2016",
      "hts_kor_isnm": "K경기소비재",
      "bstp_nmix_prpr": "1771.78",
      "bstp_nmix_prdy_vrss": "9.87",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "0.56",
      "acml_vol": "71",
      "nmix_sdpr": "1761.91",
      "ascn_issu_cnt": "26",
      "stnr_issu_cnt": "4",
      "down_issu_cnt": "0"
    },
    {
      "bstp_cls_code": "2017",
      "hts_kor_isnm": "K산업재",
      "bstp_nmix_prpr": "638.85",
      "bstp_nmix_prdy_vrss": "3.52",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "0.55",
      "acml_vol": "144",
      "nmix_sdpr": "635.33",
      "ascn_issu_cnt": "19",
      "stnr_issu_cnt": "1",
      "down_issu_cnt": "3"
    },
    {
      "bstp_cls_code": "2018",
      "hts_kor_isnm": "K헬스케어",
      "bstp_nmix_prpr": "1880.59",
      "bstp_nmix_prdy_vrss": "7.50",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "0.40",
      "acml_vol": "25",
      "nmix_sdpr": "1873.09",
      "ascn_issu_cnt": "12",
      "stnr_issu_cnt": "2",
      "down_issu_cnt": "2"
    },
    {
      "bstp_cls_code": "0163",
      "hts_kor_isnm": "고배당50",
      "bstp_nmix_prpr": "3012.54",
      "bstp_nmix_prdy_vrss": "2.40",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "0.08",
      "acml_vol": "654",
      "nmix_sdpr": "3010.14",
      "ascn_issu_cnt": "0",
      "stnr_issu_cnt": "0",
      "down_issu_cnt": "0"
    },
    {
      "bstp_cls_code": "0164",
      "hts_kor_isnm": "배당성장50",
      "bstp_nmix_prpr": "3697.71",
      "bstp_nmix_prdy_vrss": "14.09",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "0.38",
      "acml_vol": "557",
      "nmix_sdpr": "3683.62",
      "ascn_issu_cnt": "0",
      "stnr_issu_cnt": "0",
      "down_issu_cnt": "0"
    },
    {
      "bstp_cls_code": "0165",
      "hts_kor_isnm": "우선주",
      "bstp_nmix_prpr": "3159.80",
      "bstp_nmix_prdy_vrss": "3.00",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "0.10",
      "acml_vol": "27",
      "nmix_sdpr": "3156.80",
      "ascn_issu_cnt": "0",
      "stnr_issu_cnt": "0",
      "down_issu_cnt": "0"
    },
    {
      "bstp_cls_code": "2180",
      "hts_kor_isnm": "코스피 200 ESG 지수",
      "bstp_nmix_prpr": "408.37",
      "bstp_nmix_prdy_vrss": "0.89",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "0.22",
      "acml_vol": "1068",
      "nmix_sdpr": "407.48",
      "ascn_issu_cnt": "0",
      "stnr_issu_cnt": "0",
      "down_issu_cnt": "0"
    },
    {
      "bstp_cls_code": "2040",
      "hts_kor_isnm": "코스피200 초대형 제외지수",
      "bstp_nmix_prpr": "261.99",
      "bstp_nmix_prdy_vrss": "0.79",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "0.30",
      "acml_vol": "1276",
      "nmix_sdpr": "261.20",
      "ascn_issu_cnt": "0",
      "stnr_issu_cnt": "0",
      "down_issu_cnt": "0"
    },
    {
      "bstp_cls_code": "2037",
      "hts_kor_isnm": "코스피200 예측 고배당 50",
      "bstp_nmix_prpr": "2034.64",
      "bstp_nmix_prdy_vrss": "7.50",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "0.37",
      "acml_vol": "227",
      "nmix_sdpr": "2027.14",
      "ascn_issu_cnt": "0",
      "stnr_issu_cnt": "0",
      "down_issu_cnt": "0"
    },
    {
      "bstp_cls_code": "2038",
      "hts_kor_isnm": "코스피200 예측 배당성장 50",
      "bstp_nmix_prpr": "1710.41",
      "bstp_nmix_prdy_vrss": "9.08",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "0.53",
      "acml_vol": "581",
      "nmix_sdpr": "1701.33",
      "ascn_issu_cnt": "0",
      "stnr_issu_cnt": "0",
      "down_issu_cnt": "0"
    },
    {
      "bstp_cls_code": "2224",
      "hts_kor_isnm": "K200 비중상한 30%",
      "bstp_nmix_prpr": "360.08",
      "bstp_nmix_prdy_vrss": "1.06",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "0.30",
      "acml_vol": "1687",
      "nmix_sdpr": "359.02",
      "ascn_issu_cnt": "0",
      "stnr_issu_cnt": "0",
      "down_issu_cnt": "0"
    },
    {
      "bstp_cls_code": "2227",
      "hts_kor_isnm": "K200 비중상한 25%",
      "bstp_nmix_prpr": "356.69",
      "bstp_nmix_prdy_vrss": "1.04",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "0.29",
      "acml_vol": "1687",
      "nmix_sdpr": "355.65",
      "ascn_issu_cnt": "0",
      "stnr_issu_cnt": "0",
      "down_issu_cnt": "0"
    },
    {
      "bstp_cls_code": "2232",
      "hts_kor_isnm": "K200 비중상한 20%",
      "bstp_nmix_prpr": "346.65",
      "bstp_nmix_prdy_vrss": "1.02",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "0.30",
      "acml_vol": "1687",
      "nmix_sdpr": "345.63",
      "ascn_issu_cnt": "0",
      "stnr_issu_cnt": "0",
      "down_issu_cnt": "0"
    },
    {
      "bstp_cls_code": "0244",
      "hts_kor_isnm": "코스피200제외 코스피지수",
      "bstp_nmix_prpr": "3337.06",
      "bstp_nmix_prdy_vrss": "10.34",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "0.31",
      "acml_vol": "3373",
      "nmix_sdpr": "3326.72",
      "ascn_issu_cnt": "0",
      "stnr_issu_cnt": "0",
      "down_issu_cnt": "0"
    },
    {
      "bstp_cls_code": "2283",
      "hts_kor_isnm": "코스피 200 기후변화지수",
      "bstp_nmix_prpr": "1580.49",
      "bstp_nmix_prdy_vrss": "4.56",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "0.29",
      "acml_vol": "1639",
      "nmix_sdpr": "1575.93",
      "ascn_issu_cnt": "0",
      "stnr_issu_cnt": "0",
      "down_issu_cnt": "0"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```
