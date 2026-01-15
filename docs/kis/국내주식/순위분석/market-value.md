# 국내주식 시장가치 순위[v1_국내주식-096]

> [국내주식] 순위분석

국내주식 시장가치 순위 API입니다.
한국투자 HTS(eFriend Plus) > [0179] 시장가치순위 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.
최대 30건 확인 가능하며, 다음 조회가 불가합니다.

※ 30건 이상의 목록 조회가 필요한 경우, 대안으로 종목조건검색 API를 이용해서 원하는 종목 100개까지 검색할 수 있는 기능을 제공하고 있습니다.
종목조건검색 API는 HTS(efriend Plus) [0110] 조건검색에서 등록 및 서버저장한 나의 조건 목록을 확인할 수 있는 API로,
자세한 사용 방법은 공지사항 - [조건검색 필독] 조건검색 API 이용안내 참고 부탁드립니다.


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `dfd2502e-0d5c-4999-8a24-84ff15a74696` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/ranking/market-value` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `FHPST01790000` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-03-15
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
| `tr_id` | 거래ID | String | 13 | Y | FHPST01790000 |
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
| `fid_trgt_cls_code` | 대상 구분 코드 | String | 32 | Y | 0 : 전체 |
| `fid_cond_mrkt_div_code` | 조건 시장 분류 코드 | String | 2 | Y | 시장구분코드 (J:KRX, NX:NXT) |
| `fid_cond_scr_div_code` | 조건 화면 분류 코드 | String | 5 | Y | Unique key( 20179 ) |
| `fid_input_iscd` | 입력 종목코드 | String | 12 | Y | 0000:전체, 0001:거래소, 1001:코스닥, 2001:코스피200 |
| `fid_div_cls_code` | 분류 구분 코드 | String | 2 | Y | 0: 전체, 1:관리종목, 2:투자주의, 3:투자경고, 4:투자위험예고, 5:투자위험, 6:보톧주, 7:우선주 |
| `fid_input_price_1` | 입력 가격1 | String | 12 | Y | 입력값 없을때 전체 (가격 ~) |
| `fid_input_price_2` | 입력 가격2 | String | 12 | Y | 입력값 없을때 전체 (~ 가격) |
| `fid_vol_cnt` | 거래량 수 | String | 12 | Y | 입력값 없을때 전체 (거래량 ~) |
| `fid_input_option_1` | 입력 옵션1 | String | 10 | Y | 회계연도 입력 (ex 2023) |
| `fid_input_option_2` | 입력 옵션2 | String | 10 | Y | 0: 1/4분기 , 1: 반기, 2: 3/4분기, 3: 결산 |
| `fid_rank_sort_cls_code` | 순위 정렬 구분 코드 | String | 2 | Y | '가치분석(23:PER, 24:PBR, 25:PCR, 26:PSR, 27: EPS, 28:EVA, 29: EBITDA, 30: EV/EBITDA, 31:EBITDA/금융비율' |
| `fid_blng_cls_code` | 소속 구분 코드 | String | 2 | Y | 0 : 전체 |
| `fid_trgt_exls_cls_code` | 대상 제외 구분 코드 | String | 32 | Y | 0 : 전체 |

### 요청 예시

```json
{
  "fid_cond_mrkt_div_code": "J",
  "fid_cond_scr_div_code": "20179",
  "fid_input_iscd": "0000",
  "fid_div_cls_code": "0",
  "fid_input_price_1": "",
  "fid_input_price_2": "",
  "fid_vol_cnt": "",
  "fid_input_option_1": "2023",
  "fid_input_option_2": "3",
  "fid_rank_sort_cls_code": "23",
  "fid_blng_cls_code": "0",
  "fid_trgt_exls_cls_code": "0",
  "fid_trgt_cls_code": "0"
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
| `output` | 응답상세 | Object |   | Y | array |
| `data_rank` | 데이터 순위 | String | 10 | Y |  |
| `hts_kor_isnm` | HTS 한글 종목명 | String | 40 | Y |  |
| `mksc_shrn_iscd` | 유가증권 단축 종목코드 | String | 9 | Y |  |
| `stck_prpr` | 주식 현재가 | String | 10 | Y |  |
| `prdy_vrss` | 전일 대비 | String | 10 | Y |  |
| `prdy_vrss_sign` | 전일 대비 부호 | String | 1 | Y |  |
| `prdy_ctrt` | 전일 대비율 | String | 82 | Y |  |
| `acml_vol` | 누적 거래량 | String | 18 | Y |  |
| `per` | PER | String | 82 | Y |  |
| `pbr` | PBR | String | 82 | Y |  |
| `pcr` | PCR | String | 82 | Y |  |
| `psr` | PSR | String | 82 | Y |  |
| `eps` | EPS | String | 112 | Y |  |
| `eva` | EVA | String | 82 | Y |  |
| `ebitda` | EBITDA | String | 82 | Y |  |
| `pv_div_ebitda` | PV DIV EBITDA | String | 82 | Y |  |
| `ebitda_div_fnnc_expn` | EBITDA DIV 금융비용 | String | 82 | Y |  |
| `stac_month` | 결산 월 | String | 2 | Y |  |
| `stac_month_cls_code` | 결산 월 구분 코드 | String | 2 | Y |  |
| `iqry_csnu` | 조회 건수 | String | 10 | Y |  |

### 응답 예시

```json
{
  "output": [
    {
      "data_rank": "1",
      "hts_kor_isnm": "효성",
      "mksc_shrn_iscd": "004800",
      "stck_prpr": "57800",
      "prdy_vrss": "-400",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-0.69",
      "acml_vol": "7453",
      "per": "19266.67",
      "pbr": "0.49",
      "pcr": "11.19",
      "psr": "0.35",
      "eps": "300",
      "eva": "-812.00",
      "ebitda": "2031.00",
      "pv_div_ebitda": "12.98",
      "ebitda_div_fnnc_expn": "0.02",
      "stac_month": "12",
      "stac_month_cls_code": "0",
      "iqry_csnu": "1773"
    },
    {
      "data_rank": "2",
      "hts_kor_isnm": "에이엘티",
      "mksc_shrn_iscd": "172670",
      "stck_prpr": "21450",
      "prdy_vrss": "50",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "0.23",
      "acml_vol": "28989",
      "per": "10725.00",
      "pbr": "1.87",
      "pcr": "10.63",
      "psr": "3.68",
      "eps": "200",
      "eva": "0.00",
      "ebitda": "170.00",
      "pv_div_ebitda": "0.00",
      "ebitda_div_fnnc_expn": "0.05",
      "stac_month": "12",
      "stac_month_cls_code": "1",
      "iqry_csnu": "1773"
    },
    {
      "data_rank": "3",
      "hts_kor_isnm": "한싹",
      "mksc_shrn_iscd": "430690",
      "stck_prpr": "14450",
      "prdy_vrss": "-170",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-1.16",
      "acml_vol": "11549",
      "per": "4816.67",
      "pbr": "2.44",
      "pcr": "171.76",
      "psr": "3.74",
      "eps": "300",
      "eva": "0.00",
      "ebitda": "1.00",
      "pv_div_ebitda": "0.00",
      "ebitda_div_fnnc_expn": "0.00",
      "stac_month": "12",
      "stac_month_cls_code": "1",
      "iqry_csnu": "1773"
    },
    {
      "data_rank": "4",
      "hts_kor_isnm": "파버나인",
      "mksc_shrn_iscd": "177830",
      "stck_prpr": "3565",
      "prdy_vrss": "5",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "0.14",
      "acml_vol": "7838",
      "per": "1188.33",
      "pbr": "0.61",
      "pcr": "6.37",
      "psr": "0.40",
      "eps": "300",
      "eva": "0.00",
      "ebitda": "83.00",
      "pv_div_ebitda": "0.00",
      "ebitda_div_fnnc_expn": "0.03",
      "stac_month": "12",
      "stac_month_cls_code": "1",
      "iqry_csnu": "1773"
    },
    {
      "data_rank": "5",
      "hts_kor_isnm": "카카오페이",
      "mksc_shrn_iscd": "377300",
      "stck_prpr": "39800",
      "prdy_vrss": "-150",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-0.38",
      "acml_vol": "49767",
      "per": "1170.59",
      "pbr": "2.84",
      "pcr": "102.25",
      "psr": "8.90",
      "eps": "3400",
      "eva": "0.00",
      "ebitda": "-6.00",
      "pv_div_ebitda": "0.00",
      "ebitda_div_fnnc_expn": "0.00",
      "stac_month": "12",
      "stac_month_cls_code": "1",
      "iqry_csnu": "1773"
    },
    {
      "data_rank": "6",
      "hts_kor_isnm": "디케이티",
      "mksc_shrn_iscd": "290550",
      "stck_prpr": "9030",
      "prdy_vrss": "0",
      "prdy_vrss_sign": "3",
      "prdy_ctrt": "0.00",
      "acml_vol": "5782",
      "per": "752.50",
      "pbr": "1.28",
      "pcr": "18.89",
      "psr": "0.60",
      "eps": "1200",
      "eva": "0.00",
      "ebitda": "180.00",
      "pv_div_ebitda": "0.00",
      "ebitda_div_fnnc_expn": "0.09",
      "stac_month": "12",
      "stac_month_cls_code": "1",
      "iqry_csnu": "1773"
    },
    {
      "data_rank": "7",
      "hts_kor_isnm": "키움제6호스팩",
      "mksc_shrn_iscd": "413600",
      "stck_prpr": "2125",
      "prdy_vrss": "-25",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-1.16",
      "acml_vol": "3455",
      "per": "708.33",
      "pbr": "1.11",
      "pcr": "689.94",
      "psr": "0.00",
      "eps": "300",
      "eva": "0.00",
      "ebitda": "-1.00",
      "pv_div_ebitda": "0.00",
      "ebitda_div_fnnc_expn": "0.00",
      "stac_month": "12",
      "stac_month_cls_code": "1",
      "iqry_csnu": "1773"
    },
    {
      "data_rank": "8",
      "hts_kor_isnm": "네온테크",
      "mksc_shrn_iscd": "306620",
      "stck_prpr": "2740",
      "prdy_vrss": "30",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "1.11",
      "acml_vol": "30166",
      "per": "685.00",
      "pbr": "2.33",
      "pcr": "46.94",
      "psr": "1.63",
      "eps": "400",
      "eva": "0.00",
      "ebitda": "18.00",
      "pv_div_ebitda": "0.00",
      "ebitda_div_fnnc_expn": "0.01",
      "stac_month": "12",
      "stac_month_cls_code": "1",
      "iqry_csnu": "1773"
    },
    {
      "data_rank": "9",
      "hts_kor_isnm": "한올바이오파마",
      "mksc_shrn_iscd": "009420",
      "stck_prpr": "36900",
      "prdy_vrss": "900",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "2.50",
      "acml_vol": "241062",
      "per": "550.75",
      "pbr": "9.67",
      "pcr": "285.34",
      "psr": "14.29",
      "eps": "6700",
      "eva": "-67.00",
      "ebitda": "55.00",
      "pv_div_ebitda": "423.99",
      "ebitda_div_fnnc_expn": "0.87",
      "stac_month": "12",
      "stac_month_cls_code": "0",
      "iqry_csnu": "1773"
    },
    {
      "data_rank": "10",
      "hts_kor_isnm": "IBKS제20호스팩",
      "mksc_shrn_iscd": "439730",
      "stck_prpr": "2595",
      "prdy_vrss": "0",
      "prdy_vrss_sign": "3",
      "prdy_ctrt": "0.00",
      "acml_vol": "730",
      "per": "519.00",
      "pbr": "1.33",
      "pcr": "571.59",
      "psr": "0.00",
      "eps": "500",
      "eva": "0.00",
      "ebitda": "0.00",
      "pv_div_ebitda": "0.00",
      "ebitda_div_fnnc_expn": "0.00",
      "stac_month": "12",
      "stac_month_cls_code": "1",
      "iqry_csnu": "1773"
    },
    {
      "data_rank": "11",
      "hts_kor_isnm": "에코프로머티",
      "mksc_shrn_iscd": "450080",
      "stck_prpr": "151300",
      "prdy_vrss": "1100",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "0.73",
      "acml_vol": "140199",
      "per": "514.63",
      "pbr": "27.87",
      "pcr": "221.45",
      "psr": "12.06",
      "eps": "29400",
      "eva": "266.00",
      "ebitda": "596.00",
      "pv_div_ebitda": "4.36",
      "ebitda_div_fnnc_expn": "0.05",
      "stac_month": "12",
      "stac_month_cls_code": "1",
      "iqry_csnu": "1773"
    },
    {
      "data_rank": "12",
      "hts_kor_isnm": "씨씨에스",
      "mksc_shrn_iscd": "066790",
      "stck_prpr": "5460",
      "prdy_vrss": "10",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "0.18",
      "acml_vol": "5892226",
      "per": "496.36",
      "pbr": "10.52",
      "pcr": "74.99",
      "psr": "15.94",
      "eps": "1100",
      "eva": "0.00",
      "ebitda": "28.00",
      "pv_div_ebitda": "0.00",
      "ebitda_div_fnnc_expn": "0.10",
      "stac_month": "12",
      "stac_month_cls_code": "1",
      "iqry_csnu": "1773"
    },
    {
      "data_rank": "13",
      "hts_kor_isnm": "로보스타",
      "mksc_shrn_iscd": "090360",
      "stck_prpr": "34800",
      "prdy_vrss": "650",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "1.90",
      "acml_vol": "131404",
      "per": "490.14",
      "pbr": "3.77",
      "pcr": "151.06",
      "psr": "3.30",
      "eps": "7100",
      "eva": "-39.00",
      "ebitda": "27.00",
      "pv_div_ebitda": "108.07",
      "ebitda_div_fnnc_expn": "1.71",
      "stac_month": "12",
      "stac_month_cls_code": "0",
      "iqry_csnu": "1773"
    },
    {
      "data_rank": "14",
      "hts_kor_isnm": "두산퓨얼셀",
      "mksc_shrn_iscd": "336260",
      "stck_prpr": "20300",
      "prdy_vrss": "510",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "2.58",
      "acml_vol": "188218",
      "per": "431.91",
      "pbr": "3.17",
      "pcr": "102.57",
      "psr": "5.32",
      "eps": "4700",
      "eva": "-492.00",
      "ebitda": "196.00",
      "pv_div_ebitda": "118.06",
      "ebitda_div_fnnc_expn": "0.04",
      "stac_month": "12",
      "stac_month_cls_code": "1",
      "iqry_csnu": "1773"
    },
    {
      "data_rank": "15",
      "hts_kor_isnm": "가온칩스",
      "mksc_shrn_iscd": "399720",
      "stck_prpr": "101900",
      "prdy_vrss": "400",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "0.39",
      "acml_vol": "223999",
      "per": "415.92",
      "pbr": "20.38",
      "pcr": "152.86",
      "psr": "20.56",
      "eps": "24500",
      "eva": "0.00",
      "ebitda": "49.00",
      "pv_div_ebitda": "0.00",
      "ebitda_div_fnnc_expn": "0.23",
      "stac_month": "12",
      "stac_month_cls_code": "1",
      "iqry_csnu": "1773"
    },
    {
      "data_rank": "16",
      "hts_kor_isnm": "미래나노텍",
      "mksc_shrn_iscd": "095500",
      "stck_prpr": "20200",
      "prdy_vrss": "1530",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "8.19",
      "acml_vol": "976189",
      "per": "412.24",
      "pbr": "2.34",
      "pcr": "41.51",
      "psr": "0.94",
      "eps": "4900",
      "eva": "0.00",
      "ebitda": "226.00",
      "pv_div_ebitda": "0.00",
      "ebitda_div_fnnc_expn": "0.04",
      "stac_month": "12",
      "stac_month_cls_code": "1",
      "iqry_csnu": "1773"
    },
    {
      "data_rank": "17",
      "hts_kor_isnm": "디와이피엔에프",
      "mksc_shrn_iscd": "104460",
      "stck_prpr": "20000",
      "prdy_vrss": "-500",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-2.44",
      "acml_vol": "12543",
      "per": "350.88",
      "pbr": "1.90",
      "pcr": "64.19",
      "psr": "1.59",
      "eps": "5700",
      "eva": "0.00",
      "ebitda": "43.00",
      "pv_div_ebitda": "0.00",
      "ebitda_div_fnnc_expn": "0.03",
      "stac_month": "12",
      "stac_month_cls_code": "1",
      "iqry_csnu": "1773"
    },
    {
      "data_rank": "18",
      "hts_kor_isnm": "바이오니아",
      "mksc_shrn_iscd": "064550",
      "stck_prpr": "30150",
      "prdy_vrss": "150",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "0.50",
      "acml_vol": "79014",
      "per": "350.58",
      "pbr": "3.27",
      "pcr": "65.17",
      "psr": "2.93",
      "eps": "8600",
      "eva": "0.00",
      "ebitda": "158.00",
      "pv_div_ebitda": "0.00",
      "ebitda_div_fnnc_expn": "0.20",
      "stac_month": "12",
      "stac_month_cls_code": "1",
      "iqry_csnu": "1773"
    },
    {
      "data_rank": "19",
      "hts_kor_isnm": "픽셀플러스",
      "mksc_shrn_iscd": "087600",
      "stck_prpr": "9780",
      "prdy_vrss": "30",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "0.31",
      "acml_vol": "31501",
      "per": "326.00",
      "pbr": "0.77",
      "pcr": "45.96",
      "psr": "1.27",
      "eps": "3000",
      "eva": "-20.00",
      "ebitda": "44.00",
      "pv_div_ebitda": "14.29",
      "ebitda_div_fnnc_expn": "1.00",
      "stac_month": "12",
      "stac_month_cls_code": "1",
      "iqry_csnu": "1773"
    },
    {
      "data_rank": "20",
      "hts_kor_isnm": "한국제12호스팩",
      "mksc_shrn_iscd": "458610",
      "stck_prpr": "2195",
      "prdy_vrss": "0",
      "prdy_vrss_sign": "3",
      "prdy_ctrt": "0.00",
      "acml_vol": "9418",
      "per": "313.57",
      "pbr": "1.10",
      "pcr": "302.76",
      "psr": "0.00",
      "eps": "700",
      "eva": "0.00",
      "ebitda": "0.00",
      "pv_div_ebitda": "0.00",
      "ebitda_div_fnnc_expn": "0.00",
      "stac_month": "12",
      "stac_month_cls_code": "0",
      "iqry_csnu": "1773"
    },
    {
      "data_rank": "21",
      "hts_kor_isnm": "유진스팩8호",
      "mksc_shrn_iscd": "413630",
      "stck_prpr": "3630",
      "prdy_vrss": "-80",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-2.16",
      "acml_vol": "181731",
      "per": "302.50",
      "pbr": "1.95",
      "pcr": "300.25",
      "psr": "0.00",
      "eps": "1200",
      "eva": "0.00",
      "ebitda": "-1.00",
      "pv_div_ebitda": "0.00",
      "ebitda_div_fnnc_expn": "0.00",
      "stac_month": "12",
      "stac_month_cls_code": "1",
      "iqry_csnu": "1773"
    },
    {
      "data_rank": "22",
      "hts_kor_isnm": "라온텍",
      "mksc_shrn_iscd": "418420",
      "stck_prpr": "6310",
      "prdy_vrss": "120",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "1.94",
      "acml_vol": "39277",
      "per": "300.48",
      "pbr": "23.99",
      "pcr": "229.71",
      "psr": "16.44",
      "eps": "2100",
      "eva": "3.00",
      "ebitda": "5.00",
      "pv_div_ebitda": "0.00",
      "ebitda_div_fnnc_expn": "0.14",
      "stac_month": "12",
      "stac_month_cls_code": "1",
      "iqry_csnu": "1773"
    },
    {
      "data_rank": "23",
      "hts_kor_isnm": "에프엔에스테크",
      "mksc_shrn_iscd": "083500",
      "stck_prpr": "12240",
      "prdy_vrss": "0",
      "prdy_vrss_sign": "3",
      "prdy_ctrt": "0.00",
      "acml_vol": "60455",
      "per": "291.43",
      "pbr": "1.57",
      "pcr": "28.61",
      "psr": "2.81",
      "eps": "4200",
      "eva": "0.00",
      "ebitda": "25.00",
      "pv_div_ebitda": "0.00",
      "ebitda_div_fnnc_expn": "0.03",
      "stac_month": "12",
      "stac_month_cls_code": "1",
      "iqry_csnu": "1773"
    },
    {
      "data_rank": "24",
      "hts_kor_isnm": "삼아알미늄",
      "mksc_shrn_iscd": "006110",
      "stck_prpr": "91500",
      "prdy_vrss": "400",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "0.44",
      "acml_vol": "17642",
      "per": "284.16",
      "pbr": "5.22",
      "pcr": "76.02",
      "psr": "4.80",
      "eps": "32200",
      "eva": "0.00",
      "ebitda": "133.00",
      "pv_div_ebitda": "0.00",
      "ebitda_div_fnnc_expn": "0.07",
      "stac_month": "12",
      "stac_month_cls_code": "1",
      "iqry_csnu": "1773"
    },
    {
      "data_rank": "25",
      "hts_kor_isnm": "하나기술",
      "mksc_shrn_iscd": "299030",
      "stck_prpr": "64900",
      "prdy_vrss": "1400",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "2.20",
      "acml_vol": "56036",
      "per": "276.17",
      "pbr": "4.68",
      "pcr": "85.46",
      "psr": "4.52",
      "eps": "23500",
      "eva": "0.00",
      "ebitda": "-23.00",
      "pv_div_ebitda": "0.00",
      "ebitda_div_fnnc_expn": "0.00",
      "stac_month": "12",
      "stac_month_cls_code": "1",
      "iqry_csnu": "1773"
    },
    {
      "data_rank": "26",
      "hts_kor_isnm": "특수건설",
      "mksc_shrn_iscd": "026150",
      "stck_prpr": "7600",
      "prdy_vrss": "-30",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-0.39",
      "acml_vol": "19735",
      "per": "271.43",
      "pbr": "1.24",
      "pcr": "13.64",
      "psr": "0.58",
      "eps": "2800",
      "eva": "0.00",
      "ebitda": "75.00",
      "pv_div_ebitda": "0.00",
      "ebitda_div_fnnc_expn": "0.08",
      "stac_month": "12",
      "stac_month_cls_code": "1",
      "iqry_csnu": "1773"
    },
    {
      "data_rank": "27",
      "hts_kor_isnm": "경보제약",
      "mksc_shrn_iscd": "214390",
      "stck_prpr": "6890",
      "prdy_vrss": "220",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "3.30",
      "acml_vol": "62124",
      "per": "265.00",
      "pbr": "1.15",
      "pcr": "13.13",
      "psr": "0.84",
      "eps": "2600",
      "eva": "-119.00",
      "ebitda": "133.00",
      "pv_div_ebitda": "22.24",
      "ebitda_div_fnnc_expn": "0.08",
      "stac_month": "12",
      "stac_month_cls_code": "1",
      "iqry_csnu": "1773"
    },
    {
      "data_rank": "28",
      "hts_kor_isnm": "교보11호스팩",
      "mksc_shrn_iscd": "397880",
      "stck_prpr": "3425",
      "prdy_vrss": "0",
      "prdy_vrss_sign": "0",
      "prdy_ctrt": "0.00",
      "acml_vol": "0",
      "per": "263.46",
      "pbr": "1.75",
      "pcr": "253.89",
      "psr": "0.00",
      "eps": "1300",
      "eva": "0.00",
      "ebitda": "0.00",
      "pv_div_ebitda": "0.00",
      "ebitda_div_fnnc_expn": "0.00",
      "stac_month": "12",
      "stac_month_cls_code": "1",
      "iqry_csnu": "1773"
    },
    {
      "data_rank": "29",
      "hts_kor_isnm": "오스테오닉",
      "mksc_shrn_iscd": "226400",
      "stck_prpr": "4910",
      "prdy_vrss": "-70",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-1.41",
      "acml_vol": "71736",
      "per": "258.42",
      "pbr": "1.98",
      "pcr": "31.94",
      "psr": "3.82",
      "eps": "1900",
      "eva": "0.00",
      "ebitda": "45.00",
      "pv_div_ebitda": "0.00",
      "ebitda_div_fnnc_expn": "0.07",
      "stac_month": "12",
      "stac_month_cls_code": "1",
      "iqry_csnu": "1773"
    },
    {
      "data_rank": "30",
      "hts_kor_isnm": "유진스팩7호",
      "mksc_shrn_iscd": "388800",
      "stck_prpr": "2440",
      "prdy_vrss": "0",
      "prdy_vrss_sign": "0",
      "prdy_ctrt": "0.00",
      "acml_vol": "0",
      "per": "244.00",
      "pbr": "1.36",
      "pcr": "254.17",
      "psr": "0.00",
      "eps": "1000",
      "eva": "0.00",
      "ebitda": "-1.00",
      "pv_div_ebitda": "0.00",
      "ebitda_div_fnnc_expn": "0.00",
      "stac_month": "12",
      "stac_month_cls_code": "1",
      "iqry_csnu": "1773"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```

