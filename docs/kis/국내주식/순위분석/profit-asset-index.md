# 국내주식 수익자산지표 순위[v1_국내주식-090]

> [국내주식] 순위분석

국내주식 수익자산지표 순위 API입니다.
한국투자 HTS(eFriend Plus) > [0173] 수익자산지표 순위 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.
최대 30건 확인 가능하며, 다음 조회가 불가합니다.

※ 30건 이상의 목록 조회가 필요한 경우, 대안으로 종목조건검색 API를 이용해서 원하는 종목 100개까지 검색할 수 있는 기능을 제공하고 있습니다.
종목조건검색 API는 HTS(efriend Plus) [0110] 조건검색에서 등록 및 서버저장한 나의 조건 목록을 확인할 수 있는 API로,
자세한 사용 방법은 공지사항 - [조건검색 필독] 조건검색 API 이용안내 참고 부탁드립니다.


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `7185c44d-0bc5-4c0f-b64d-71ac9ea796f1` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/ranking/profit-asset-index` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `FHPST01730000` |
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
| `tr_id` | 거래ID | String | 13 | Y | FHPST01730000 |
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
| `fid_cond_mrkt_div_code` | 조건 시장 분류 코드 | String | 2 | Y | 시장구분코드 (J:KRX, NX:NXT) |
| `fid_trgt_cls_code` | 대상 구분 코드 | String | 32 | Y | 0:전체 |
| `fid_cond_scr_div_code` | 조건 화면 분류 코드 | String | 5 | Y | Unique key( 20173 ) |
| `fid_input_iscd` | 입력 종목코드 | String | 12 | Y | 0000:전체, 0001:거래소, 1001:코스닥, 2001:코스피200 |
| `fid_div_cls_code` | 분류 구분 코드 | String | 2 | Y | 0:전체 |
| `fid_input_price_1` | 입력 가격1 | String | 12 | Y | 입력값 없을때 전체 (가격 ~) |
| `fid_input_price_2` | 입력 가격2 | String | 12 | Y | 입력값 없을때 전체 (~ 가격) |
| `fid_vol_cnt` | 거래량 수 | String | 12 | Y | 입력값 없을때 전체 (거래량 ~) |
| `fid_input_option_1` | 입력 옵션1 | String | 10 | Y | 회계연도 (2023) |
| `fid_input_option_2` | 입력 옵션2 | String | 10 | Y | 0: 1/4분기 , 1: 반기, 2: 3/4분기, 3: 결산 |
| `fid_rank_sort_cls_code` | 순위 정렬 구분 코드 | String | 2 | Y | 0:매출이익 1:영업이익 2:경상이익 3:당기순이익 4:자산총계 5:부채총계 6:자본총계 |
| `fid_blng_cls_code` | 소속 구분 코드 | String | 2 | Y | 0:전체 |
| `fid_trgt_exls_cls_code` | 대상 제외 구분 코드 | String | 32 | Y | 0:전체 |

### 요청 예시

```json
{
"fid_cond_mrkt_div_code":"J",
"fid_cond_scr_div_code":"20173",
"fid_input_iscd":"0000",
"fid_div_cls_code":"0",
"fid_input_price_1":"",
"fid_input_price_2":"",
"fid_vol_cnt":"",
"fid_input_option_1":"2023",
"fid_input_option_2":"0",
"fid_rank_sort_cls_code":"0",
"fid_blng_cls_code":"0",
"fid_trgt_exls_cls_code":"0",
"fid_trgt_cls_code":"0",
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
| `prdy_vrss_sign` | 전일 대비 부호 | String | 1 | Y |  |
| `mksc_shrn_iscd` | 유가증권 단축 종목코드 | String | 9 | Y |  |
| `stck_prpr` | 주식 현재가 | String | 10 | Y |  |
| `prdy_vrss` | 전일 대비 | String | 10 | Y |  |
| `prdy_ctrt` | 전일 대비율 | String | 82 | Y |  |
| `acml_vol` | 누적 거래량 | String | 18 | Y |  |
| `sale_totl_prfi` | 매출 총 이익 | String | 182 | Y |  |
| `bsop_prti` | 영업 이익 | String | 182 | Y |  |
| `op_prfi` | 경상 이익 | String | 182 | Y |  |
| `thtr_ntin` | 당기순이익 | String | 102 | Y |  |
| `total_aset` | 자산총계 | String | 102 | Y |  |
| `total_lblt` | 부채총계 | String | 102 | Y |  |
| `total_cptl` | 자본총계 | String | 102 | Y |  |
| `stac_month` | 결산 월 | String | 2 | Y |  |
| `stac_month_cls_code` | 결산 월 구분 코드 | String | 2 | Y |  |
| `iqry_csnu` | 조회 건수 | String | 10 | Y |  |

### 응답 예시

```json
{
  "output": [
    {
      "data_rank": "1",
      "hts_kor_isnm": "삼성전자",
      "mksc_shrn_iscd": "005930",
      "stck_prpr": "72800",
      "prdy_vrss": "500",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "0.69",
      "acml_vol": "3682788",
      "sale_totl_prfi": "177383.00",
      "bsop_prti": "6402.00",
      "op_prfi": "18264.00",
      "thtr_ntin": "15746.00",
      "total_aset": "4540918.00",
      "total_lblt": "942924.00",
      "total_cptl": "3597994.00",
      "stac_month": "12",
      "stac_month_cls_code": "0",
      "iqry_csnu": "2468"
    },
    {
      "data_rank": "2",
      "hts_kor_isnm": "현대차",
      "mksc_shrn_iscd": "005380",
      "stck_prpr": "246500",
      "prdy_vrss": "3000",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "1.23",
      "acml_vol": "264085",
      "sale_totl_prfi": "77220.00",
      "bsop_prti": "35927.00",
      "op_prfi": "45909.00",
      "thtr_ntin": "34194.00",
      "total_aset": "2643636.00",
      "total_lblt": "1704440.00",
      "total_cptl": "939195.00",
      "stac_month": "12",
      "stac_month_cls_code": "0",
      "iqry_csnu": "2468"
    },
    {
      "data_rank": "3",
      "hts_kor_isnm": "KT",
      "mksc_shrn_iscd": "030200",
      "stck_prpr": "38100",
      "prdy_vrss": "-150",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-0.39",
      "acml_vol": "98431",
      "sale_totl_prfi": "64437.00",
      "bsop_prti": "4861.00",
      "op_prfi": "4376.00",
      "thtr_ntin": "3096.00",
      "total_aset": "402144.00",
      "total_lblt": "220625.00",
      "total_cptl": "181520.00",
      "stac_month": "12",
      "stac_month_cls_code": "0",
      "iqry_csnu": "2468"
    },
    {
      "data_rank": "4",
      "hts_kor_isnm": "기아",
      "mksc_shrn_iscd": "000270",
      "stck_prpr": "127400",
      "prdy_vrss": "2400",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "1.92",
      "acml_vol": "505419",
      "sale_totl_prfi": "53734.00",
      "bsop_prti": "28740.00",
      "op_prfi": "31421.00",
      "thtr_ntin": "21198.00",
      "total_aset": "776127.00",
      "total_lblt": "375811.00",
      "total_cptl": "400316.00",
      "stac_month": "12",
      "stac_month_cls_code": "0",
      "iqry_csnu": "2468"
    },
    {
      "data_rank": "5",
      "hts_kor_isnm": "LG전자",
      "mksc_shrn_iscd": "066570",
      "stck_prpr": "97900",
      "prdy_vrss": "-1000",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-1.01",
      "acml_vol": "123952",
      "sale_totl_prfi": "51699.00",
      "bsop_prti": "14974.00",
      "op_prfi": "9337.00",
      "thtr_ntin": "5465.00",
      "total_aset": "574906.00",
      "total_lblt": "341309.00",
      "total_cptl": "233598.00",
      "stac_month": "12",
      "stac_month_cls_code": "0",
      "iqry_csnu": "2468"
    },
    {
      "data_rank": "6",
      "hts_kor_isnm": "SK텔레콤",
      "mksc_shrn_iscd": "017670",
      "stck_prpr": "52900",
      "prdy_vrss": "-200",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-0.38",
      "acml_vol": "145002",
      "sale_totl_prfi": "43722.00",
      "bsop_prti": "4948.00",
      "op_prfi": "4209.00",
      "thtr_ntin": "3025.00",
      "total_aset": "305397.00",
      "total_lblt": "182230.00",
      "total_cptl": "123167.00",
      "stac_month": "12",
      "stac_month_cls_code": "0",
      "iqry_csnu": "2468"
    },
    {
      "data_rank": "7",
      "hts_kor_isnm": "삼성화재",
      "mksc_shrn_iscd": "000810",
      "stck_prpr": "307500",
      "prdy_vrss": "-2000",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-0.65",
      "acml_vol": "38892",
      "sale_totl_prfi": "40846.00",
      "bsop_prti": "8333.00",
      "op_prfi": "8593.00",
      "thtr_ntin": "6133.00",
      "total_aset": "814661.00",
      "total_lblt": "682398.00",
      "total_cptl": "132264.00",
      "stac_month": "12",
      "stac_month_cls_code": "0",
      "iqry_csnu": "2468"
    },
    {
      "data_rank": "8",
      "hts_kor_isnm": "DB손해보험",
      "mksc_shrn_iscd": "005830",
      "stck_prpr": "99700",
      "prdy_vrss": "-2200",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-2.16",
      "acml_vol": "60493",
      "sale_totl_prfi": "35945.00",
      "bsop_prti": "6782.00",
      "op_prfi": "6873.00",
      "thtr_ntin": "5274.00",
      "total_aset": "550956.00",
      "total_lblt": "457981.00",
      "total_cptl": "92975.00",
      "stac_month": "12",
      "stac_month_cls_code": "0",
      "iqry_csnu": "2468"
    },
    {
      "data_rank": "9",
      "hts_kor_isnm": "LG유플러스",
      "mksc_shrn_iscd": "032640",
      "stck_prpr": "9990",
      "prdy_vrss": "-70",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-0.70",
      "acml_vol": "242577",
      "sale_totl_prfi": "35413.00",
      "bsop_prti": "2602.00",
      "op_prfi": "2110.00",
      "thtr_ntin": "1551.00",
      "total_aset": "200178.00",
      "total_lblt": "115891.00",
      "total_cptl": "84287.00",
      "stac_month": "12",
      "stac_month_cls_code": "0",
      "iqry_csnu": "2468"
    },
    {
      "data_rank": "10",
      "hts_kor_isnm": "현대해상",
      "mksc_shrn_iscd": "001450",
      "stck_prpr": "33850",
      "prdy_vrss": "-650",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-1.88",
      "acml_vol": "157602",
      "sale_totl_prfi": "32220.00",
      "bsop_prti": "2861.00",
      "op_prfi": "2769.00",
      "thtr_ntin": "2136.00",
      "total_aset": "430393.00",
      "total_lblt": "364840.00",
      "total_cptl": "65552.00",
      "stac_month": "12",
      "stac_month_cls_code": "0",
      "iqry_csnu": "2468"
    },
    {
      "data_rank": "11",
      "hts_kor_isnm": "SK",
      "mksc_shrn_iscd": "034730",
      "stck_prpr": "185100",
      "prdy_vrss": "-2200",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-1.17",
      "acml_vol": "31227",
      "sale_totl_prfi": "30209.00",
      "bsop_prti": "11304.00",
      "op_prfi": "148.00",
      "thtr_ntin": "-66.00",
      "total_aset": "1977927.00",
      "total_lblt": "1239833.00",
      "total_cptl": "738094.00",
      "stac_month": "12",
      "stac_month_cls_code": "0",
      "iqry_csnu": "2468"
    },
    {
      "data_rank": "12",
      "hts_kor_isnm": "흥국화재",
      "mksc_shrn_iscd": "000540",
      "stck_prpr": "4500",
      "prdy_vrss": "-125",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-2.70",
      "acml_vol": "92773",
      "sale_totl_prfi": "29739.00",
      "bsop_prti": "1860.00",
      "op_prfi": "1868.00",
      "thtr_ntin": "1475.00",
      "total_aset": "139661.00",
      "total_lblt": "132461.00",
      "total_cptl": "7200.00",
      "stac_month": "12",
      "stac_month_cls_code": "1",
      "iqry_csnu": "2468"
    },
    {
      "data_rank": "13",
      "hts_kor_isnm": "KB금융",
      "mksc_shrn_iscd": "105560",
      "stck_prpr": "73000",
      "prdy_vrss": "-3200",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-4.20",
      "acml_vol": "999009",
      "sale_totl_prfi": "27856.00",
      "bsop_prti": "21250.00",
      "op_prfi": "20289.00",
      "thtr_ntin": "14992.00",
      "total_aset": "6914356.00",
      "total_lblt": "6351955.00",
      "total_cptl": "562402.00",
      "stac_month": "12",
      "stac_month_cls_code": "0",
      "iqry_csnu": "2468"
    },
    {
      "data_rank": "14",
      "hts_kor_isnm": "CJ",
      "mksc_shrn_iscd": "001040",
      "stck_prpr": "109700",
      "prdy_vrss": "500",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "0.46",
      "acml_vol": "216421",
      "sale_totl_prfi": "26296.00",
      "bsop_prti": "3293.00",
      "op_prfi": "1272.00",
      "thtr_ntin": "117.00",
      "total_aset": "489176.00",
      "total_lblt": "310436.00",
      "total_cptl": "178740.00",
      "stac_month": "12",
      "stac_month_cls_code": "0",
      "iqry_csnu": "2468"
    },
    {
      "data_rank": "15",
      "hts_kor_isnm": "신한지주",
      "mksc_shrn_iscd": "055550",
      "stck_prpr": "48700",
      "prdy_vrss": "-900",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-1.81",
      "acml_vol": "907017",
      "sale_totl_prfi": "25738.00",
      "bsop_prti": "17562.00",
      "op_prfi": "18568.00",
      "thtr_ntin": "14143.00",
      "total_aset": "6761756.00",
      "total_lblt": "6203801.00",
      "total_cptl": "557955.00",
      "stac_month": "12",
      "stac_month_cls_code": "0",
      "iqry_csnu": "2468"
    },
    {
      "data_rank": "16",
      "hts_kor_isnm": "삼성생명",
      "mksc_shrn_iscd": "032830",
      "stck_prpr": "96000",
      "prdy_vrss": "-3100",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-3.13",
      "acml_vol": "233938",
      "sale_totl_prfi": "23550.00",
      "bsop_prti": "8818.00",
      "op_prfi": "9564.00",
      "thtr_ntin": "7391.00",
      "total_aset": "2997953.00",
      "total_lblt": "2599820.00",
      "total_cptl": "398133.00",
      "stac_month": "12",
      "stac_month_cls_code": "0",
      "iqry_csnu": "2468"
    },
    {
      "data_rank": "17",
      "hts_kor_isnm": "LG화학",
      "mksc_shrn_iscd": "051910",
      "stck_prpr": "439000",
      "prdy_vrss": "8000",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "1.86",
      "acml_vol": "66448",
      "sale_totl_prfi": "23251.00",
      "bsop_prti": "6907.00",
      "op_prfi": "9160.00",
      "thtr_ntin": "6691.00",
      "total_aset": "708960.00",
      "total_lblt": "324919.00",
      "total_cptl": "384041.00",
      "stac_month": "12",
      "stac_month_cls_code": "0",
      "iqry_csnu": "2468"
    },
    {
      "data_rank": "18",
      "hts_kor_isnm": "롯데손해보험",
      "mksc_shrn_iscd": "000400",
      "stck_prpr": "2920",
      "prdy_vrss": "55",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "1.92",
      "acml_vol": "365380",
      "sale_totl_prfi": "23071.00",
      "bsop_prti": "-765.00",
      "op_prfi": "-845.00",
      "thtr_ntin": "-631.00",
      "total_aset": "179258.00",
      "total_lblt": "174772.00",
      "total_cptl": "4486.00",
      "stac_month": "12",
      "stac_month_cls_code": "1",
      "iqry_csnu": "2468"
    },
    {
      "data_rank": "19",
      "hts_kor_isnm": "한화",
      "mksc_shrn_iscd": "000880",
      "stck_prpr": "28600",
      "prdy_vrss": "650",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "2.33",
      "acml_vol": "123355",
      "sale_totl_prfi": "22992.00",
      "bsop_prti": "13738.00",
      "op_prfi": "16434.00",
      "thtr_ntin": "11553.00",
      "total_aset": "2018543.00",
      "total_lblt": "1675732.00",
      "total_cptl": "342811.00",
      "stac_month": "12",
      "stac_month_cls_code": "0",
      "iqry_csnu": "2468"
    },
    {
      "data_rank": "20",
      "hts_kor_isnm": "한화생명",
      "mksc_shrn_iscd": "088350",
      "stck_prpr": "3170",
      "prdy_vrss": "-80",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-2.46",
      "acml_vol": "926965",
      "sale_totl_prfi": "22965.00",
      "bsop_prti": "7619.00",
      "op_prfi": "6103.00",
      "thtr_ntin": "4635.00",
      "total_aset": "1469270.00",
      "total_lblt": "1305749.00",
      "total_cptl": "163521.00",
      "stac_month": "12",
      "stac_month_cls_code": "0",
      "iqry_csnu": "2468"
    },
    {
      "data_rank": "21",
      "hts_kor_isnm": "NAVER",
      "mksc_shrn_iscd": "035420",
      "stck_prpr": "184600",
      "prdy_vrss": "-1500",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-0.81",
      "acml_vol": "338155",
      "sale_totl_prfi": "22804.00",
      "bsop_prti": "3305.00",
      "op_prfi": "1166.00",
      "thtr_ntin": "437.00",
      "total_aset": "357733.00",
      "total_lblt": "116494.00",
      "total_cptl": "241239.00",
      "stac_month": "12",
      "stac_month_cls_code": "0",
      "iqry_csnu": "2468"
    },
    {
      "data_rank": "22",
      "hts_kor_isnm": "우리금융지주",
      "mksc_shrn_iscd": "316140",
      "stck_prpr": "14740",
      "prdy_vrss": "-490",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-3.22",
      "acml_vol": "1903659",
      "sale_totl_prfi": "22188.00",
      "bsop_prti": "12520.00",
      "op_prfi": "12703.00",
      "thtr_ntin": "9466.00",
      "total_aset": "4780793.00",
      "total_lblt": "4454756.00",
      "total_cptl": "326036.00",
      "stac_month": "12",
      "stac_month_cls_code": "0",
      "iqry_csnu": "2468"
    },
    {
      "data_rank": "23",
      "hts_kor_isnm": "하나금융지주",
      "mksc_shrn_iscd": "086790",
      "stck_prpr": "61700",
      "prdy_vrss": "-400",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-0.64",
      "acml_vol": "731232",
      "sale_totl_prfi": "21750.00",
      "bsop_prti": "15188.00",
      "op_prfi": "14958.00",
      "thtr_ntin": "11095.00",
      "total_aset": "5877306.00",
      "total_lblt": "5491426.00",
      "total_cptl": "385880.00",
      "stac_month": "12",
      "stac_month_cls_code": "0",
      "iqry_csnu": "2468"
    },
    {
      "data_rank": "24",
      "hts_kor_isnm": "이마트",
      "mksc_shrn_iscd": "139480",
      "stck_prpr": "69800",
      "prdy_vrss": "-500",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-0.71",
      "acml_vol": "38727",
      "sale_totl_prfi": "19974.00",
      "bsop_prti": "137.00",
      "op_prfi": "53.00",
      "thtr_ntin": "27.00",
      "total_aset": "329952.00",
      "total_lblt": "196451.00",
      "total_cptl": "133500.00",
      "stac_month": "12",
      "stac_month_cls_code": "0",
      "iqry_csnu": "2468"
    },
    {
      "data_rank": "25",
      "hts_kor_isnm": "기업은행",
      "mksc_shrn_iscd": "024110",
      "stck_prpr": "15150",
      "prdy_vrss": "-100",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-0.66",
      "acml_vol": "937861",
      "sale_totl_prfi": "19482.00",
      "bsop_prti": "9156.00",
      "op_prfi": "9371.00",
      "thtr_ntin": "7233.00",
      "total_aset": "4378441.00",
      "total_lblt": "4079864.00",
      "total_cptl": "298577.00",
      "stac_month": "12",
      "stac_month_cls_code": "0",
      "iqry_csnu": "2468"
    },
    {
      "data_rank": "26",
      "hts_kor_isnm": "GS",
      "mksc_shrn_iscd": "078930",
      "stck_prpr": "49150",
      "prdy_vrss": "-250",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-0.51",
      "acml_vol": "19800",
      "sale_totl_prfi": "17946.00",
      "bsop_prti": "10625.00",
      "op_prfi": "10055.00",
      "thtr_ntin": "5211.00",
      "total_aset": "345250.00",
      "total_lblt": "178336.00",
      "total_cptl": "166914.00",
      "stac_month": "12",
      "stac_month_cls_code": "0",
      "iqry_csnu": "2468"
    },
    {
      "data_rank": "27",
      "hts_kor_isnm": "카카오",
      "mksc_shrn_iscd": "035720",
      "stck_prpr": "53500",
      "prdy_vrss": "-600",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-1.11",
      "acml_vol": "370033",
      "sale_totl_prfi": "17403.00",
      "bsop_prti": "711.00",
      "op_prfi": "733.00",
      "thtr_ntin": "638.00",
      "total_aset": "255864.00",
      "total_lblt": "102841.00",
      "total_cptl": "153023.00",
      "stac_month": "12",
      "stac_month_cls_code": "0",
      "iqry_csnu": "2468"
    },
    {
      "data_rank": "28",
      "hts_kor_isnm": "롯데쇼핑",
      "mksc_shrn_iscd": "023530",
      "stck_prpr": "73300",
      "prdy_vrss": "-300",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-0.41",
      "acml_vol": "11381",
      "sale_totl_prfi": "16117.00",
      "bsop_prti": "1125.00",
      "op_prfi": "1051.00",
      "thtr_ntin": "578.00",
      "total_aset": "318847.00",
      "total_lblt": "208468.00",
      "total_cptl": "110379.00",
      "stac_month": "12",
      "stac_month_cls_code": "0",
      "iqry_csnu": "2468"
    },
    {
      "data_rank": "29",
      "hts_kor_isnm": "삼성물산",
      "mksc_shrn_iscd": "028260",
      "stck_prpr": "151000",
      "prdy_vrss": "-3100",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-2.01",
      "acml_vol": "281396",
      "sale_totl_prfi": "15087.00",
      "bsop_prti": "6405.00",
      "op_prfi": "9179.00",
      "thtr_ntin": "7519.00",
      "total_aset": "618621.00",
      "total_lblt": "275928.00",
      "total_cptl": "342693.00",
      "stac_month": "12",
      "stac_month_cls_code": "0",
      "iqry_csnu": "2468"
    },
    {
      "data_rank": "30",
      "hts_kor_isnm": "CJ제일제당",
      "mksc_shrn_iscd": "097950",
      "stck_prpr": "291000",
      "prdy_vrss": "3500",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "1.22",
      "acml_vol": "5733",
      "sale_totl_prfi": "14572.00",
      "bsop_prti": "2528.00",
      "op_prfi": "993.00",
      "thtr_ntin": "493.00",
      "total_aset": "305950.00",
      "total_lblt": "188033.00",
      "total_cptl": "117916.00",
      "stac_month": "12",
      "stac_month_cls_code": "0",
      "iqry_csnu": "2468"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```

