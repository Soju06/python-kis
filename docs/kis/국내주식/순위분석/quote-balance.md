# 국내주식 호가잔량 순위[국내주식-089]

> [국내주식] 순위분석

국내주식 호가잔량 순위 API입니다. 
한국투자 HTS(eFriend Plus) > [0172] 호가잔량 순위 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.
최대 30건 확인 가능하며, 다음 조회가 불가합니다.

※ 30건 이상의 목록 조회가 필요한 경우, 대안으로 종목조건검색 API를 이용해서 원하는 종목 100개까지 검색할 수 있는 기능을 제공하고 있습니다.
종목조건검색 API는 HTS(efriend Plus) [0110] 조건검색에서 등록 및 서버저장한 나의 조건 목록을 확인할 수 있는 API로,
자세한 사용 방법은 공지사항 - [조건검색 필독] 조건검색 API 이용안내 참고 부탁드립니다.


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `09dff633-6f3b-486a-b894-bbed4e77aaf6` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/ranking/quote-balance` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `FHPST01720000` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-03-15T09:23:35+09:00
- **최종 수정일**: 2025-05-14T14:40:18+09:00

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials Grant 절차를 준용)  법인(Access token 유효기간 3개월, Refresh token 유효기간 1년, OAuth 2.0의 Authorization Code Grant 절차를 준용) |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | FHPST01720000 |
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
| `fid_vol_cnt` | 거래량 수 | String | 12 | Y | 입력값 없을때 전체 (거래량 ~) |
| `fid_cond_mrkt_div_code` | 조건 시장 분류 코드 | String | 2 | Y | 시장구분코드 (J:KRX, NX:NXT) |
| `fid_cond_scr_div_code` | 조건 화면 분류 코드 | String | 5 | Y | Unique key( 20172 ) |
| `fid_input_iscd` | 입력 종목코드 | String | 12 | Y | 0000(전체) 코스피(0001), 코스닥(1001), 코스피200(2001) |
| `fid_rank_sort_cls_code` | 순위 정렬 구분 코드 | String | 2 | Y | 0: 순매수잔량순, 1:순매도잔량순, 2:매수비율순, 3:매도비율순 |
| `fid_div_cls_code` | 분류 구분 코드 | String | 2 | Y | 0:전체 |
| `fid_trgt_cls_code` | 대상 구분 코드 | String | 32 | Y | 0:전체 |
| `fid_trgt_exls_cls_code` | 대상 제외 구분 코드 | String | 32 | Y | 0:전체 |
| `fid_input_price_1` | 입력 가격1 | String | 12 | Y | 입력값 없을때 전체 (가격 ~) |
| `fid_input_price_2` | 입력 가격2 | String | 12 | Y | 입력값 없을때 전체 (~ 가격) |

### 요청 예시

```json
{
  "fid_cond_mrkt_div_code": "J",
  "fid_cond_scr_div_code": "20172",
  "fid_input_iscd": "0000",
  "fid_rank_sort_cls_code": "0",
  "fid_div_cls_code": "0",
  "fid_trgt_cls_code": "0",
  "fid_trgt_exls_cls_code": "0",
  "fid_input_price_1": "",
  "fid_input_price_2": "",
  "fid_vol_cnt": ""
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
| `total_askp_rsqn` | 총 매도호가 잔량 | String | 12 | Y |  |
| `total_bidp_rsqn` | 총 매수호가 잔량 | String | 12 | Y |  |
| `total_ntsl_bidp_rsqn` | 총 순 매수호가 잔량 | String | 12 | Y |  |
| `shnu_rsqn_rate` | 매수 잔량 비율 | String | 84 | Y |  |
| `seln_rsqn_rate` | 매도 잔량 비율 | String | 84 | Y |  |

### 응답 예시

```json
{
  "output": [
    {
      "mksc_shrn_iscd": "Q530036",
      "data_rank": "1",
      "hts_kor_isnm": "삼성 인버스 2X WTI원유 선물 ETN",
      "stck_prpr": "92",
      "prdy_vrss": "0",
      "prdy_vrss_sign": "3",
      "prdy_ctrt": "0.00",
      "acml_vol": "4019460",
      "total_askp_rsqn": "27327397",
      "total_bidp_rsqn": "59778444",
      "total_ntsl_bidp_rsqn": "32451047",
      "shnu_rsqn_rate": "68.63",
      "seln_rsqn_rate": "31.37"
    },
    {
      "mksc_shrn_iscd": "003410",
      "data_rank": "2",
      "hts_kor_isnm": "쌍용C&E",
      "stck_prpr": "7000",
      "prdy_vrss": "0",
      "prdy_vrss_sign": "3",
      "prdy_ctrt": "0.00",
      "acml_vol": "83785",
      "total_askp_rsqn": "238068",
      "total_bidp_rsqn": "22904795",
      "total_ntsl_bidp_rsqn": "22666727",
      "shnu_rsqn_rate": "98.97",
      "seln_rsqn_rate": "1.03"
    },
    {
      "mksc_shrn_iscd": "252670",
      "data_rank": "3",
      "hts_kor_isnm": "KODEX 200선물인버스2X",
      "stck_prpr": "2180",
      "prdy_vrss": "0",
      "prdy_vrss_sign": "3",
      "prdy_ctrt": "0.00",
      "acml_vol": "45344920",
      "total_askp_rsqn": "16674598",
      "total_bidp_rsqn": "26686853",
      "total_ntsl_bidp_rsqn": "10012255",
      "shnu_rsqn_rate": "61.55",
      "seln_rsqn_rate": "38.45"
    },
    {
      "mksc_shrn_iscd": "114800",
      "data_rank": "4",
      "hts_kor_isnm": "KODEX 인버스",
      "stck_prpr": "4275",
      "prdy_vrss": "0",
      "prdy_vrss_sign": "3",
      "prdy_ctrt": "0.00",
      "acml_vol": "4988727",
      "total_askp_rsqn": "5715746",
      "total_bidp_rsqn": "9303814",
      "total_ntsl_bidp_rsqn": "3588068",
      "shnu_rsqn_rate": "61.94",
      "seln_rsqn_rate": "38.06"
    },
    {
      "mksc_shrn_iscd": "018000",
      "data_rank": "5",
      "hts_kor_isnm": "유니슨",
      "stck_prpr": "1233",
      "prdy_vrss": "215",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "21.12",
      "acml_vol": "2436474",
      "total_askp_rsqn": "0",
      "total_bidp_rsqn": "2617859",
      "total_ntsl_bidp_rsqn": "2617859",
      "shnu_rsqn_rate": "100.00",
      "seln_rsqn_rate": "0.00"
    },
    {
      "mksc_shrn_iscd": "005930",
      "data_rank": "6",
      "hts_kor_isnm": "삼성전자",
      "stck_prpr": "72800",
      "prdy_vrss": "500",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "0.69",
      "acml_vol": "3310579",
      "total_askp_rsqn": "970901",
      "total_bidp_rsqn": "2358190",
      "total_ntsl_bidp_rsqn": "1387289",
      "shnu_rsqn_rate": "70.84",
      "seln_rsqn_rate": "29.16"
    },
    {
      "mksc_shrn_iscd": "251340",
      "data_rank": "7",
      "hts_kor_isnm": "KODEX 코스닥150선물인버스",
      "stck_prpr": "3315",
      "prdy_vrss": "-65",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-1.92",
      "acml_vol": "20976556",
      "total_askp_rsqn": "5821013",
      "total_bidp_rsqn": "6913597",
      "total_ntsl_bidp_rsqn": "1092584",
      "shnu_rsqn_rate": "54.29",
      "seln_rsqn_rate": "45.71"
    },
    {
      "mksc_shrn_iscd": "Q550074",
      "data_rank": "8",
      "hts_kor_isnm": "QV 블룸버그 2X 천연가스 선물 ETN(H)",
      "stck_prpr": "395",
      "prdy_vrss": "0",
      "prdy_vrss_sign": "3",
      "prdy_ctrt": "0.00",
      "acml_vol": "381899",
      "total_askp_rsqn": "156122",
      "total_bidp_rsqn": "1037967",
      "total_ntsl_bidp_rsqn": "881845",
      "shnu_rsqn_rate": "86.93",
      "seln_rsqn_rate": "13.07"
    },
    {
      "mksc_shrn_iscd": "Q500027",
      "data_rank": "9",
      "hts_kor_isnm": "신한 인버스 2X WTI원유 선물 ETN(H)",
      "stck_prpr": "81",
      "prdy_vrss": "0",
      "prdy_vrss_sign": "3",
      "prdy_ctrt": "0.00",
      "acml_vol": "535276",
      "total_askp_rsqn": "45614576",
      "total_bidp_rsqn": "46290045",
      "total_ntsl_bidp_rsqn": "675469",
      "shnu_rsqn_rate": "50.37",
      "seln_rsqn_rate": "49.63"
    },
    {
      "mksc_shrn_iscd": "900110",
      "data_rank": "10",
      "hts_kor_isnm": "이스트아시아홀딩스",
      "stck_prpr": "93",
      "prdy_vrss": "0",
      "prdy_vrss_sign": "3",
      "prdy_ctrt": "0.00",
      "acml_vol": "680301",
      "total_askp_rsqn": "1831739",
      "total_bidp_rsqn": "2470524",
      "total_ntsl_bidp_rsqn": "638785",
      "shnu_rsqn_rate": "57.42",
      "seln_rsqn_rate": "42.58"
    },
    {
      "mksc_shrn_iscd": "900280",
      "data_rank": "11",
      "hts_kor_isnm": "골든센츄리",
      "stck_prpr": "128",
      "prdy_vrss": "-1",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-0.78",
      "acml_vol": "742379",
      "total_askp_rsqn": "1028799",
      "total_bidp_rsqn": "1485157",
      "total_ntsl_bidp_rsqn": "456358",
      "shnu_rsqn_rate": "59.08",
      "seln_rsqn_rate": "40.92"
    },
    {
      "mksc_shrn_iscd": "001470",
      "data_rank": "12",
      "hts_kor_isnm": "삼부토건",
      "stck_prpr": "2535",
      "prdy_vrss": "-155",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-5.76",
      "acml_vol": "7133448",
      "total_askp_rsqn": "257260",
      "total_bidp_rsqn": "713292",
      "total_ntsl_bidp_rsqn": "456032",
      "shnu_rsqn_rate": "73.49",
      "seln_rsqn_rate": "26.51"
    },
    {
      "mksc_shrn_iscd": "252710",
      "data_rank": "13",
      "hts_kor_isnm": "TIGER 200선물인버스2X",
      "stck_prpr": "2310",
      "prdy_vrss": "5",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "0.22",
      "acml_vol": "1556254",
      "total_askp_rsqn": "314399",
      "total_bidp_rsqn": "757848",
      "total_ntsl_bidp_rsqn": "443449",
      "shnu_rsqn_rate": "70.68",
      "seln_rsqn_rate": "29.32"
    },
    {
      "mksc_shrn_iscd": "010140",
      "data_rank": "14",
      "hts_kor_isnm": "삼성중공업",
      "stck_prpr": "8930",
      "prdy_vrss": "80",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "0.90",
      "acml_vol": "6043474",
      "total_askp_rsqn": "176430",
      "total_bidp_rsqn": "487408",
      "total_ntsl_bidp_rsqn": "310978",
      "shnu_rsqn_rate": "73.42",
      "seln_rsqn_rate": "26.58"
    },
    {
      "mksc_shrn_iscd": "271050",
      "data_rank": "15",
      "hts_kor_isnm": "KODEX WTI원유선물인버스(H)",
      "stck_prpr": "4190",
      "prdy_vrss": "-10",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-0.24",
      "acml_vol": "106936",
      "total_askp_rsqn": "201253",
      "total_bidp_rsqn": "458790",
      "total_ntsl_bidp_rsqn": "257537",
      "shnu_rsqn_rate": "69.51",
      "seln_rsqn_rate": "30.49"
    },
    {
      "mksc_shrn_iscd": "453850",
      "data_rank": "16",
      "hts_kor_isnm": "ACE 미국30년국채액티브(H)",
      "stck_prpr": "8540",
      "prdy_vrss": "-30",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-0.35",
      "acml_vol": "413651",
      "total_askp_rsqn": "394820",
      "total_bidp_rsqn": "641051",
      "total_ntsl_bidp_rsqn": "246231",
      "shnu_rsqn_rate": "61.89",
      "seln_rsqn_rate": "38.11"
    },
    {
      "mksc_shrn_iscd": "031860",
      "data_rank": "17",
      "hts_kor_isnm": "에스유홀딩스",
      "stck_prpr": "200",
      "prdy_vrss": "5",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "2.56",
      "acml_vol": "3005608",
      "total_askp_rsqn": "592337",
      "total_bidp_rsqn": "834037",
      "total_ntsl_bidp_rsqn": "241700",
      "shnu_rsqn_rate": "58.47",
      "seln_rsqn_rate": "41.53"
    },
    {
      "mksc_shrn_iscd": "123310",
      "data_rank": "18",
      "hts_kor_isnm": "TIGER 인버스",
      "stck_prpr": "4790",
      "prdy_vrss": "0",
      "prdy_vrss_sign": "3",
      "prdy_ctrt": "0.00",
      "acml_vol": "61009",
      "total_askp_rsqn": "1040106",
      "total_bidp_rsqn": "1274948",
      "total_ntsl_bidp_rsqn": "234842",
      "shnu_rsqn_rate": "55.07",
      "seln_rsqn_rate": "44.93"
    },
    {
      "mksc_shrn_iscd": "066790",
      "data_rank": "19",
      "hts_kor_isnm": "씨씨에스",
      "stck_prpr": "5460",
      "prdy_vrss": "10",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "0.18",
      "acml_vol": "5044542",
      "total_askp_rsqn": "79481",
      "total_bidp_rsqn": "289718",
      "total_ntsl_bidp_rsqn": "210237",
      "shnu_rsqn_rate": "78.47",
      "seln_rsqn_rate": "21.53"
    },
    {
      "mksc_shrn_iscd": "152550",
      "data_rank": "20",
      "hts_kor_isnm": "한국ANKOR유전",
      "stck_prpr": "353",
      "prdy_vrss": "-5",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-1.40",
      "acml_vol": "439971",
      "total_askp_rsqn": "127722",
      "total_bidp_rsqn": "327363",
      "total_ntsl_bidp_rsqn": "199641",
      "shnu_rsqn_rate": "71.93",
      "seln_rsqn_rate": "28.07"
    },
    {
      "mksc_shrn_iscd": "007460",
      "data_rank": "21",
      "hts_kor_isnm": "에이프로젠",
      "stck_prpr": "1078",
      "prdy_vrss": "6",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "0.56",
      "acml_vol": "4547618",
      "total_askp_rsqn": "14915",
      "total_bidp_rsqn": "212791",
      "total_ntsl_bidp_rsqn": "197876",
      "shnu_rsqn_rate": "93.45",
      "seln_rsqn_rate": "6.55"
    },
    {
      "mksc_shrn_iscd": "016600",
      "data_rank": "22",
      "hts_kor_isnm": "큐캐피탈",
      "stck_prpr": "324",
      "prdy_vrss": "0",
      "prdy_vrss_sign": "3",
      "prdy_ctrt": "0.00",
      "acml_vol": "127470",
      "total_askp_rsqn": "56103",
      "total_bidp_rsqn": "251242",
      "total_ntsl_bidp_rsqn": "195139",
      "shnu_rsqn_rate": "81.75",
      "seln_rsqn_rate": "18.25"
    },
    {
      "mksc_shrn_iscd": "261260",
      "data_rank": "23",
      "hts_kor_isnm": "KODEX 미국달러선물인버스2X",
      "stck_prpr": "6350",
      "prdy_vrss": "-40",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-0.63",
      "acml_vol": "132188",
      "total_askp_rsqn": "208219",
      "total_bidp_rsqn": "394699",
      "total_ntsl_bidp_rsqn": "186480",
      "shnu_rsqn_rate": "65.46",
      "seln_rsqn_rate": "34.54"
    },
    {
      "mksc_shrn_iscd": "032640",
      "data_rank": "24",
      "hts_kor_isnm": "LG유플러스",
      "stck_prpr": "10000",
      "prdy_vrss": "-60",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-0.60",
      "acml_vol": "208413",
      "total_askp_rsqn": "69973",
      "total_bidp_rsqn": "241811",
      "total_ntsl_bidp_rsqn": "171838",
      "shnu_rsqn_rate": "77.56",
      "seln_rsqn_rate": "22.44"
    },
    {
      "mksc_shrn_iscd": "000890",
      "data_rank": "25",
      "hts_kor_isnm": "보해양조",
      "stck_prpr": "499",
      "prdy_vrss": "-1",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-0.20",
      "acml_vol": "33688",
      "total_askp_rsqn": "42161",
      "total_bidp_rsqn": "204169",
      "total_ntsl_bidp_rsqn": "162008",
      "shnu_rsqn_rate": "82.88",
      "seln_rsqn_rate": "17.12"
    },
    {
      "mksc_shrn_iscd": "115530",
      "data_rank": "26",
      "hts_kor_isnm": "씨엔플러스",
      "stck_prpr": "345",
      "prdy_vrss": "0",
      "prdy_vrss_sign": "3",
      "prdy_ctrt": "0.00",
      "acml_vol": "8657778",
      "total_askp_rsqn": "38681",
      "total_bidp_rsqn": "197775",
      "total_ntsl_bidp_rsqn": "159094",
      "shnu_rsqn_rate": "83.64",
      "seln_rsqn_rate": "16.36"
    },
    {
      "mksc_shrn_iscd": "475280",
      "data_rank": "27",
      "hts_kor_isnm": "ACE 8월만기자동연장회사채AA-이상액티브",
      "stck_prpr": "10065",
      "prdy_vrss": "-5",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-0.05",
      "acml_vol": "1029",
      "total_askp_rsqn": "43999",
      "total_bidp_rsqn": "202972",
      "total_ntsl_bidp_rsqn": "158973",
      "shnu_rsqn_rate": "82.18",
      "seln_rsqn_rate": "17.82"
    },
    {
      "mksc_shrn_iscd": "082660",
      "data_rank": "28",
      "hts_kor_isnm": "코스나인",
      "stck_prpr": "281",
      "prdy_vrss": "1",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "0.36",
      "acml_vol": "197620",
      "total_askp_rsqn": "68474",
      "total_bidp_rsqn": "220086",
      "total_ntsl_bidp_rsqn": "151612",
      "shnu_rsqn_rate": "76.27",
      "seln_rsqn_rate": "23.73"
    },
    {
      "mksc_shrn_iscd": "365590",
      "data_rank": "29",
      "hts_kor_isnm": "하이딥",
      "stck_prpr": "1419",
      "prdy_vrss": "-4",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-0.28",
      "acml_vol": "34996",
      "total_askp_rsqn": "2430",
      "total_bidp_rsqn": "150999",
      "total_ntsl_bidp_rsqn": "148569",
      "shnu_rsqn_rate": "98.42",
      "seln_rsqn_rate": "1.58"
    },
    {
      "mksc_shrn_iscd": "000680",
      "data_rank": "30",
      "hts_kor_isnm": "LS네트웍스",
      "stck_prpr": "5400",
      "prdy_vrss": "-240",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-4.26",
      "acml_vol": "6399421",
      "total_askp_rsqn": "103613",
      "total_bidp_rsqn": "248579",
      "total_ntsl_bidp_rsqn": "144966",
      "shnu_rsqn_rate": "70.58",
      "seln_rsqn_rate": "29.42"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```

