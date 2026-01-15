# 국내주식 시가총액 상위[v1_국내주식-091]

> [국내주식] 순위분석

국내주식 시가총액 상위 API입니다.
한국투자 HTS(eFriend Plus) > [0174] 시가총액 상위 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.
최대 30건 확인 가능하며, 다음 조회가 불가합니다.

※ 30건 이상의 목록 조회가 필요한 경우, 대안으로 종목조건검색 API를 이용해서 원하는 종목 100개까지 검색할 수 있는 기능을 제공하고 있습니다.
종목조건검색 API는 HTS(efriend Plus) [0110] 조건검색에서 등록 및 서버저장한 나의 조건 목록을 확인할 수 있는 API로,
자세한 사용 방법은 공지사항 - [조건검색 필독] 조건검색 API 이용안내 참고 부탁드립니다.


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `bdb401cd-03ea-4329-928d-18b3e9af066e` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/ranking/market-cap` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `FHPST01740000` |
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
| `tr_id` | 거래ID | String | 13 | Y | FHPST01740000 |
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
| `fid_input_price_2` | 입력 가격2 | String | 12 | Y | 입력값 없을때 전체 (~ 가격) |
| `fid_cond_mrkt_div_code` | 조건 시장 분류 코드 | String | 2 | Y | 시장구분코드 (J:KRX, NX:NXT) |
| `fid_cond_scr_div_code` | 조건 화면 분류 코드 | String | 5 | Y | Unique key( 20174 ) |
| `fid_div_cls_code` | 분류 구분 코드 | String | 2 | Y | 0: 전체,  1:보통주,  2:우선주 |
| `fid_input_iscd` | 입력 종목코드 | String | 12 | Y | 0000:전체, 0001:거래소, 1001:코스닥, 2001:코스피200 |
| `fid_trgt_cls_code` | 대상 구분 코드 | String | 32 | Y | 0 : 전체 |
| `fid_trgt_exls_cls_code` | 대상 제외 구분 코드 | String | 32 | Y | 0 : 전체 |
| `fid_input_price_1` | 입력 가격1 | String | 12 | Y | 입력값 없을때 전체 (가격 ~) |
| `fid_vol_cnt` | 거래량 수 | String | 12 | Y | 입력값 없을때 전체 (거래량 ~) |

### 요청 예시

```json
{
"fid_cond_mrkt_div_code":"J",
"fid_cond_scr_div_code":"20174",
"fid_div_cls_code":"0",
"fid_input_iscd":"0000",
"fid_trgt_cls_code":"0"
"fid_trgt_exls_cls_code":"0",
"fid_input_price_1":"",
"fid_input_price_2":"",
"fid_vol_cnt":"",
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
| `mksc_shrn_iscd` | 유가증권 단축 종목코드 | String | 9 | Y |  |
| `data_rank` | 데이터 순위 | String | 10 | Y |  |
| `hts_kor_isnm` | HTS 한글 종목명 | String | 40 | Y |  |
| `stck_prpr` | 주식 현재가 | String | 10 | Y |  |
| `prdy_vrss` | 전일 대비 | String | 10 | Y |  |
| `prdy_vrss_sign` | 전일 대비 부호 | String | 1 | Y |  |
| `prdy_ctrt` | 전일 대비율 | String | 82 | Y |  |
| `acml_vol` | 누적 거래량 | String | 18 | Y |  |
| `lstn_stcn` | 상장 주수 | String | 18 | Y |  |
| `stck_avls` | 시가 총액 | String | 18 | Y |  |
| `mrkt_whol_avls_rlim` | 시장 전체 시가총액 비중 | String | 52 | Y |  |

### 응답 예시

```json
{
  "output": [
    {
      "mksc_shrn_iscd": "005930",
      "data_rank": "1",
      "hts_kor_isnm": "삼성전자",
      "stck_prpr": "72700",
      "prdy_vrss": "400",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "0.55",
      "acml_vol": "3686661",
      "lstn_stcn": "5969782550",
      "stck_avls": "4340032",
      "mrkt_whol_avls_rlim": "15.77"
    },
    {
      "mksc_shrn_iscd": "000660",
      "data_rank": "2",
      "hts_kor_isnm": "SK하이닉스",
      "stck_prpr": "162300",
      "prdy_vrss": "1100",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "0.68",
      "acml_vol": "807093",
      "lstn_stcn": "728002365",
      "stck_avls": "1181548",
      "mrkt_whol_avls_rlim": "4.29"
    },
    {
      "mksc_shrn_iscd": "373220",
      "data_rank": "3",
      "hts_kor_isnm": "LG에너지솔루션",
      "stck_prpr": "404000",
      "prdy_vrss": "5500",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "1.38",
      "acml_vol": "43109",
      "lstn_stcn": "234000000",
      "stck_avls": "945360",
      "mrkt_whol_avls_rlim": "3.43"
    },
    {
      "mksc_shrn_iscd": "207940",
      "data_rank": "4",
      "hts_kor_isnm": "삼성바이오로직스",
      "stck_prpr": "863000",
      "prdy_vrss": "37000",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "4.48",
      "acml_vol": "95134",
      "lstn_stcn": "71174000",
      "stck_avls": "614232",
      "mrkt_whol_avls_rlim": "2.23"
    },
    {
      "mksc_shrn_iscd": "005380",
      "data_rank": "5",
      "hts_kor_isnm": "현대차",
      "stck_prpr": "246500",
      "prdy_vrss": "3000",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "1.23",
      "acml_vol": "264371",
      "lstn_stcn": "211531506",
      "stck_avls": "521425",
      "mrkt_whol_avls_rlim": "1.89"
    },
    {
      "mksc_shrn_iscd": "005935",
      "data_rank": "6",
      "hts_kor_isnm": "삼성전자우",
      "stck_prpr": "62500",
      "prdy_vrss": "500",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "0.81",
      "acml_vol": "198907",
      "lstn_stcn": "822886700",
      "stck_avls": "514304",
      "mrkt_whol_avls_rlim": "1.87"
    },
    {
      "mksc_shrn_iscd": "000270",
      "data_rank": "7",
      "hts_kor_isnm": "기아",
      "stck_prpr": "127400",
      "prdy_vrss": "2400",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "1.92",
      "acml_vol": "505817",
      "lstn_stcn": "402044203",
      "stck_avls": "512204",
      "mrkt_whol_avls_rlim": "1.86"
    },
    {
      "mksc_shrn_iscd": "068270",
      "data_rank": "8",
      "hts_kor_isnm": "셀트리온",
      "stck_prpr": "182000",
      "prdy_vrss": "1200",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "0.66",
      "acml_vol": "247817",
      "lstn_stcn": "218049762",
      "stck_avls": "396851",
      "mrkt_whol_avls_rlim": "1.44"
    },
    {
      "mksc_shrn_iscd": "005490",
      "data_rank": "9",
      "hts_kor_isnm": "POSCO홀딩스",
      "stck_prpr": "437000",
      "prdy_vrss": "2000",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "0.46",
      "acml_vol": "154280",
      "lstn_stcn": "84571230",
      "stck_avls": "369576",
      "mrkt_whol_avls_rlim": "1.34"
    },
    {
      "mksc_shrn_iscd": "051910",
      "data_rank": "10",
      "hts_kor_isnm": "LG화학",
      "stck_prpr": "438500",
      "prdy_vrss": "7500",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "1.74",
      "acml_vol": "66555",
      "lstn_stcn": "70592343",
      "stck_avls": "309547",
      "mrkt_whol_avls_rlim": "1.12"
    },
    {
      "mksc_shrn_iscd": "006400",
      "data_rank": "11",
      "hts_kor_isnm": "삼성SDI",
      "stck_prpr": "438000",
      "prdy_vrss": "13000",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "3.06",
      "acml_vol": "227802",
      "lstn_stcn": "68764530",
      "stck_avls": "301189",
      "mrkt_whol_avls_rlim": "1.09"
    },
    {
      "mksc_shrn_iscd": "035420",
      "data_rank": "12",
      "hts_kor_isnm": "NAVER",
      "stck_prpr": "184500",
      "prdy_vrss": "-1600",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-0.86",
      "acml_vol": "338579",
      "lstn_stcn": "162408594",
      "stck_avls": "299644",
      "mrkt_whol_avls_rlim": "1.09"
    },
    {
      "mksc_shrn_iscd": "105560",
      "data_rank": "13",
      "hts_kor_isnm": "KB금융",
      "stck_prpr": "73000",
      "prdy_vrss": "-3200",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-4.20",
      "acml_vol": "999671",
      "lstn_stcn": "403511072",
      "stck_avls": "294563",
      "mrkt_whol_avls_rlim": "1.07"
    },
    {
      "mksc_shrn_iscd": "028260",
      "data_rank": "14",
      "hts_kor_isnm": "삼성물산",
      "stck_prpr": "150900",
      "prdy_vrss": "-3200",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-2.08",
      "acml_vol": "281612",
      "lstn_stcn": "185591670",
      "stck_avls": "280058",
      "mrkt_whol_avls_rlim": "1.02"
    },
    {
      "mksc_shrn_iscd": "247540",
      "data_rank": "15",
      "hts_kor_isnm": "에코프로비엠",
      "stck_prpr": "265500",
      "prdy_vrss": "9000",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "3.51",
      "acml_vol": "305799",
      "lstn_stcn": "97801344",
      "stck_avls": "259663",
      "mrkt_whol_avls_rlim": "0.94"
    },
    {
      "mksc_shrn_iscd": "012330",
      "data_rank": "16",
      "hts_kor_isnm": "현대모비스",
      "stck_prpr": "269500",
      "prdy_vrss": "500",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "0.19",
      "acml_vol": "78633",
      "lstn_stcn": "93655094",
      "stck_avls": "252400",
      "mrkt_whol_avls_rlim": "0.92"
    },
    {
      "mksc_shrn_iscd": "055550",
      "data_rank": "17",
      "hts_kor_isnm": "신한지주",
      "stck_prpr": "48650",
      "prdy_vrss": "-950",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-1.92",
      "acml_vol": "910139",
      "lstn_stcn": "512759471",
      "stck_avls": "249457",
      "mrkt_whol_avls_rlim": "0.91"
    },
    {
      "mksc_shrn_iscd": "003670",
      "data_rank": "18",
      "hts_kor_isnm": "포스코퓨처엠",
      "stck_prpr": "319500",
      "prdy_vrss": "3000",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "0.95",
      "acml_vol": "105628",
      "lstn_stcn": "77463220",
      "stck_avls": "247495",
      "mrkt_whol_avls_rlim": "0.90"
    },
    {
      "mksc_shrn_iscd": "035720",
      "data_rank": "19",
      "hts_kor_isnm": "카카오",
      "stck_prpr": "53400",
      "prdy_vrss": "-700",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-1.29",
      "acml_vol": "370679",
      "lstn_stcn": "445153350",
      "stck_avls": "237712",
      "mrkt_whol_avls_rlim": "0.86"
    },
    {
      "mksc_shrn_iscd": "032830",
      "data_rank": "20",
      "hts_kor_isnm": "삼성생명",
      "stck_prpr": "95900",
      "prdy_vrss": "-3200",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-3.23",
      "acml_vol": "234134",
      "lstn_stcn": "200000000",
      "stck_avls": "191800",
      "mrkt_whol_avls_rlim": "0.70"
    },
    {
      "mksc_shrn_iscd": "086790",
      "data_rank": "21",
      "hts_kor_isnm": "하나금융지주",
      "stck_prpr": "61600",
      "prdy_vrss": "-500",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-0.81",
      "acml_vol": "731438",
      "lstn_stcn": "292356598",
      "stck_avls": "180092",
      "mrkt_whol_avls_rlim": "0.65"
    },
    {
      "mksc_shrn_iscd": "138040",
      "data_rank": "22",
      "hts_kor_isnm": "메리츠금융지주",
      "stck_prpr": "83100",
      "prdy_vrss": "-100",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-0.12",
      "acml_vol": "182179",
      "lstn_stcn": "203372114",
      "stck_avls": "169002",
      "mrkt_whol_avls_rlim": "0.61"
    },
    {
      "mksc_shrn_iscd": "086520",
      "data_rank": "23",
      "hts_kor_isnm": "에코프로",
      "stck_prpr": "609000",
      "prdy_vrss": "8000",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "1.33",
      "acml_vol": "64629",
      "lstn_stcn": "26627668",
      "stck_avls": "162162",
      "mrkt_whol_avls_rlim": "0.59"
    },
    {
      "mksc_shrn_iscd": "066570",
      "data_rank": "24",
      "hts_kor_isnm": "LG전자",
      "stck_prpr": "97900",
      "prdy_vrss": "-1000",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-1.01",
      "acml_vol": "123965",
      "lstn_stcn": "163647814",
      "stck_avls": "160211",
      "mrkt_whol_avls_rlim": "0.58"
    },
    {
      "mksc_shrn_iscd": "015760",
      "data_rank": "25",
      "hts_kor_isnm": "한국전력",
      "stck_prpr": "24500",
      "prdy_vrss": "-350",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-1.41",
      "acml_vol": "736259",
      "lstn_stcn": "641964077",
      "stck_avls": "157281",
      "mrkt_whol_avls_rlim": "0.57"
    },
    {
      "mksc_shrn_iscd": "000810",
      "data_rank": "26",
      "hts_kor_isnm": "삼성화재",
      "stck_prpr": "307000",
      "prdy_vrss": "-2500",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-0.81",
      "acml_vol": "38909",
      "lstn_stcn": "47374837",
      "stck_avls": "145441",
      "mrkt_whol_avls_rlim": "0.53"
    },
    {
      "mksc_shrn_iscd": "003550",
      "data_rank": "27",
      "hts_kor_isnm": "LG",
      "stck_prpr": "90100",
      "prdy_vrss": "-4800",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-5.06",
      "acml_vol": "232801",
      "lstn_stcn": "157300993",
      "stck_avls": "141728",
      "mrkt_whol_avls_rlim": "0.51"
    },
    {
      "mksc_shrn_iscd": "034730",
      "data_rank": "28",
      "hts_kor_isnm": "SK",
      "stck_prpr": "185000",
      "prdy_vrss": "-2300",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-1.23",
      "acml_vol": "31241",
      "lstn_stcn": "73198329",
      "stck_avls": "135417",
      "mrkt_whol_avls_rlim": "0.49"
    },
    {
      "mksc_shrn_iscd": "323410",
      "data_rank": "29",
      "hts_kor_isnm": "카카오뱅크",
      "stck_prpr": "28100",
      "prdy_vrss": "-300",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-1.06",
      "acml_vol": "289825",
      "lstn_stcn": "476916137",
      "stck_avls": "134013",
      "mrkt_whol_avls_rlim": "0.49"
    },
    {
      "mksc_shrn_iscd": "028300",
      "data_rank": "30",
      "hts_kor_isnm": "HLB",
      "stck_prpr": "101900",
      "prdy_vrss": "-500",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-0.49",
      "acml_vol": "595180",
      "lstn_stcn": "130812041",
      "stck_avls": "133297",
      "mrkt_whol_avls_rlim": "0.48"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```

