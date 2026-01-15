# 국내주식 체결강도 상위[v1_국내주식-101]

> [국내주식] 순위분석

국내주식 체결강도 상위 API입니다.
한국투자 HTS(eFriend Plus) > [0168] 체결강도 상위 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.
최대 30건 확인 가능하며, 다음 조회가 불가합니다.

※ 30건 이상의 목록 조회가 필요한 경우, 대안으로 종목조건검색 API를 이용해서 원하는 종목 100개까지 검색할 수 있는 기능을 제공하고 있습니다.
종목조건검색 API는 HTS(efriend Plus) [0110] 조건검색에서 등록 및 서버저장한 나의 조건 목록을 확인할 수 있는 API로,
자세한 사용 방법은 공지사항 - [조건검색 필독] 조건검색 API 이용안내 참고 부탁드립니다.


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `f2d34ad7-9fc4-40b8-b857-3825fd772c44` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/ranking/volume-power` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `FHPST01680000` |
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
| `tr_id` | 거래ID | String | 13 | Y | FHPST01680000 |
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
| `fid_trgt_exls_cls_code` | 대상 제외 구분 코드 | String | 10 | Y | 0 : 전체 |
| `fid_cond_mrkt_div_code` | 조건 시장 분류 코드 | String | 2 | Y | 시장구분코드 (J:KRX, NX:NXT) |
| `fid_cond_scr_div_code` | 조건 화면 분류 코드 | String | 5 | Y | Unique key( 20168 ) |
| `fid_input_iscd` | 입력 종목코드 | String | 12 | Y | 0000:전체, 0001:거래소, 1001:코스닥, 2001:코스피200 |
| `fid_div_cls_code` | 분류 구분 코드 | String | 2 | Y | 0: 전체,  1: 보통주 2: 우선주 |
| `fid_input_price_1` | 입력 가격1 | String | 12 | Y | 입력값 없을때 전체 (가격 ~) |
| `fid_input_price_2` | 입력 가격2 | String | 12 | Y | 입력값 없을때 전체 (~ 가격) |
| `fid_vol_cnt` | 거래량 수 | String | 12 | Y | 입력값 없을때 전체 (거래량 ~) |
| `fid_trgt_cls_code` | 대상 구분 코드 | String | 10 | Y | 0 : 전체 |

### 요청 예시

```json
{
  "fid_cond_mrkt_div_code": "J",
  "fid_cond_scr_div_code": "20168",
  "fid_input_iscd": "0000",
  "fid_div_cls_code": "0",
  "fid_input_price_1": "",
  "fid_input_price_2": "",
  "fid_vol_cnt": "",
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
| `stck_shrn_iscd` | 주식 단축 종목코드 | String | 9 | Y |  |
| `data_rank` | 데이터 순위 | String | 10 | Y |  |
| `hts_kor_isnm` | HTS 한글 종목명 | String | 40 | Y |  |
| `stck_prpr` | 주식 현재가 | String | 10 | Y |  |
| `prdy_vrss` | 전일 대비 | String | 10 | Y |  |
| `prdy_vrss_sign` | 전일 대비 부호 | String | 1 | Y |  |
| `prdy_ctrt` | 전일 대비율 | String | 82 | Y |  |
| `acml_vol` | 누적 거래량 | String | 18 | Y |  |
| `tday_rltv` | 당일 체결강도 | String | 112 | Y |  |
| `seln_cnqn_smtn` | 매도 체결량 합계 | String | 18 | Y |  |
| `shnu_cnqn_smtn` | 매수2 체결량 합계 | String | 18 | Y |  |

### 응답 예시

```json
{
  "output": [
    {
      "stck_shrn_iscd": "422260",
      "data_rank": "1",
      "hts_kor_isnm": "VITA MZ소비액티브",
      "stck_prpr": "7650",
      "prdy_vrss": "20",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "0.26",
      "acml_vol": "26424",
      "tday_rltv": "999.99",
      "seln_cnqn_smtn": "0",
      "shnu_cnqn_smtn": "26424"
    },
    {
      "stck_shrn_iscd": "452440",
      "data_rank": "2",
      "hts_kor_isnm": "VITA 밸류알파액티브",
      "stck_prpr": "11440",
      "prdy_vrss": "-45",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-0.39",
      "acml_vol": "23100",
      "tday_rltv": "999.99",
      "seln_cnqn_smtn": "0",
      "shnu_cnqn_smtn": "23100"
    },
    {
      "stck_shrn_iscd": "449680",
      "data_rank": "3",
      "hts_kor_isnm": "TIGER 한중전기차(합성)",
      "stck_prpr": "8945",
      "prdy_vrss": "200",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "2.29",
      "acml_vol": "12065",
      "tday_rltv": "999.99",
      "seln_cnqn_smtn": "0",
      "shnu_cnqn_smtn": "12063"
    },
    {
      "stck_shrn_iscd": "457940",
      "data_rank": "4",
      "hts_kor_isnm": "에스케이증권제10호스팩",
      "stck_prpr": "2335",
      "prdy_vrss": "-5",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-0.21",
      "acml_vol": "1011",
      "tday_rltv": "999.99",
      "seln_cnqn_smtn": "0",
      "shnu_cnqn_smtn": "1011"
    },
    {
      "stck_shrn_iscd": "442580",
      "data_rank": "5",
      "hts_kor_isnm": "ARIRANG 글로벌D램반도체iSelect",
      "stck_prpr": "17290",
      "prdy_vrss": "200",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "1.17",
      "acml_vol": "906",
      "tday_rltv": "999.99",
      "seln_cnqn_smtn": "0",
      "shnu_cnqn_smtn": "885"
    },
    {
      "stck_shrn_iscd": "458210",
      "data_rank": "6",
      "hts_kor_isnm": "히어로즈 CD금리액티브(합성)",
      "stck_prpr": "102975",
      "prdy_vrss": "0",
      "prdy_vrss_sign": "3",
      "prdy_ctrt": "0.00",
      "acml_vol": "663",
      "tday_rltv": "999.99",
      "seln_cnqn_smtn": "0",
      "shnu_cnqn_smtn": "663"
    },
    {
      "stck_shrn_iscd": "418210",
      "data_rank": "7",
      "hts_kor_isnm": "신한제10호스팩",
      "stck_prpr": "2420",
      "prdy_vrss": "40",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "1.68",
      "acml_vol": "618",
      "tday_rltv": "999.99",
      "seln_cnqn_smtn": "0",
      "shnu_cnqn_smtn": "618"
    },
    {
      "stck_shrn_iscd": "469790",
      "data_rank": "8",
      "hts_kor_isnm": "KOSEF K-테크TOP10",
      "stck_prpr": "11025",
      "prdy_vrss": "-10",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-0.09",
      "acml_vol": "612",
      "tday_rltv": "999.99",
      "seln_cnqn_smtn": "0",
      "shnu_cnqn_smtn": "612"
    },
    {
      "stck_shrn_iscd": "449580",
      "data_rank": "9",
      "hts_kor_isnm": "KBSTAR 미국빅데이터Top3채권혼합iSelect",
      "stck_prpr": "12170",
      "prdy_vrss": "45",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "0.37",
      "acml_vol": "463",
      "tday_rltv": "999.99",
      "seln_cnqn_smtn": "0",
      "shnu_cnqn_smtn": "463"
    },
    {
      "stck_shrn_iscd": "424140",
      "data_rank": "10",
      "hts_kor_isnm": "케이비제21호스팩",
      "stck_prpr": "2090",
      "prdy_vrss": "0",
      "prdy_vrss_sign": "3",
      "prdy_ctrt": "0.00",
      "acml_vol": "924",
      "tday_rltv": "999.99",
      "seln_cnqn_smtn": "0",
      "shnu_cnqn_smtn": "419"
    },
    {
      "stck_shrn_iscd": "Q570055",
      "data_rank": "11",
      "hts_kor_isnm": "한투 금 선물 ETN",
      "stck_prpr": "13530",
      "prdy_vrss": "-20",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-0.15",
      "acml_vol": "401",
      "tday_rltv": "999.99",
      "seln_cnqn_smtn": "0",
      "shnu_cnqn_smtn": "401"
    },
    {
      "stck_shrn_iscd": "433980",
      "data_rank": "12",
      "hts_kor_isnm": "KODEX TDF2040액티브",
      "stck_prpr": "12145",
      "prdy_vrss": "5",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "0.04",
      "acml_vol": "391",
      "tday_rltv": "999.99",
      "seln_cnqn_smtn": "0",
      "shnu_cnqn_smtn": "377"
    },
    {
      "stck_shrn_iscd": "474390",
      "data_rank": "13",
      "hts_kor_isnm": "SOL 국고채30년액티브",
      "stck_prpr": "49100",
      "prdy_vrss": "-135",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-0.27",
      "acml_vol": "307",
      "tday_rltv": "999.99",
      "seln_cnqn_smtn": "0",
      "shnu_cnqn_smtn": "307"
    },
    {
      "stck_shrn_iscd": "Q700009",
      "data_rank": "14",
      "hts_kor_isnm": "하나 레버리지 구리 선물 ETN(H)",
      "stck_prpr": "15195",
      "prdy_vrss": "50",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "0.33",
      "acml_vol": "302",
      "tday_rltv": "999.99",
      "seln_cnqn_smtn": "0",
      "shnu_cnqn_smtn": "302"
    },
    {
      "stck_shrn_iscd": "331910",
      "data_rank": "15",
      "hts_kor_isnm": "KOSEF Fn중소형",
      "stck_prpr": "21010",
      "prdy_vrss": "130",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "0.62",
      "acml_vol": "178",
      "tday_rltv": "999.99",
      "seln_cnqn_smtn": "0",
      "shnu_cnqn_smtn": "178"
    },
    {
      "stck_shrn_iscd": "334700",
      "data_rank": "16",
      "hts_kor_isnm": "KBSTAR 팔라듐선물인버스(H)",
      "stck_prpr": "5795",
      "prdy_vrss": "0",
      "prdy_vrss_sign": "3",
      "prdy_ctrt": "0.00",
      "acml_vol": "155",
      "tday_rltv": "999.99",
      "seln_cnqn_smtn": "0",
      "shnu_cnqn_smtn": "155"
    },
    {
      "stck_shrn_iscd": "453660",
      "data_rank": "17",
      "hts_kor_isnm": "KODEX 미국S&P500경기소비재",
      "stck_prpr": "12875",
      "prdy_vrss": "-50",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-0.39",
      "acml_vol": "102",
      "tday_rltv": "999.99",
      "seln_cnqn_smtn": "0",
      "shnu_cnqn_smtn": "101"
    },
    {
      "stck_shrn_iscd": "Q610054",
      "data_rank": "18",
      "hts_kor_isnm": "메리츠 블룸버그 -2X 천연가스 선물 ETN(H)",
      "stck_prpr": "93505",
      "prdy_vrss": "-505",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-0.54",
      "acml_vol": "100",
      "tday_rltv": "999.99",
      "seln_cnqn_smtn": "0",
      "shnu_cnqn_smtn": "100"
    },
    {
      "stck_shrn_iscd": "322150",
      "data_rank": "19",
      "hts_kor_isnm": "ACE 스마트하이베타",
      "stck_prpr": "13240",
      "prdy_vrss": "-70",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-0.53",
      "acml_vol": "91",
      "tday_rltv": "999.99",
      "seln_cnqn_smtn": "0",
      "shnu_cnqn_smtn": "91"
    },
    {
      "stck_shrn_iscd": "Q580057",
      "data_rank": "20",
      "hts_kor_isnm": "KB 일본 컨슈머 TOP 10 ETN",
      "stck_prpr": "11080",
      "prdy_vrss": "70",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "0.64",
      "acml_vol": "90",
      "tday_rltv": "999.99",
      "seln_cnqn_smtn": "0",
      "shnu_cnqn_smtn": "90"
    },
    {
      "stck_shrn_iscd": "Q580034",
      "data_rank": "21",
      "hts_kor_isnm": "KB 레버리지 FANG 플러스 ETN(H)",
      "stck_prpr": "37185",
      "prdy_vrss": "-420",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-1.12",
      "acml_vol": "76",
      "tday_rltv": "999.99",
      "seln_cnqn_smtn": "0",
      "shnu_cnqn_smtn": "76"
    },
    {
      "stck_shrn_iscd": "449780",
      "data_rank": "22",
      "hts_kor_isnm": "KOSEF 미국S&P500(H)",
      "stck_prpr": "13080",
      "prdy_vrss": "-50",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-0.38",
      "acml_vol": "106",
      "tday_rltv": "999.99",
      "seln_cnqn_smtn": "0",
      "shnu_cnqn_smtn": "65"
    },
    {
      "stck_shrn_iscd": "122260",
      "data_rank": "23",
      "hts_kor_isnm": "KOSEF 통안채1년",
      "stck_prpr": "103225",
      "prdy_vrss": "0",
      "prdy_vrss_sign": "3",
      "prdy_ctrt": "0.00",
      "acml_vol": "61",
      "tday_rltv": "999.99",
      "seln_cnqn_smtn": "0",
      "shnu_cnqn_smtn": "61"
    },
    {
      "stck_shrn_iscd": "Q700014",
      "data_rank": "24",
      "hts_kor_isnm": "하나 인버스 2X 콩 선물 ETN(H)",
      "stck_prpr": "10850",
      "prdy_vrss": "-85",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-0.78",
      "acml_vol": "55",
      "tday_rltv": "999.99",
      "seln_cnqn_smtn": "0",
      "shnu_cnqn_smtn": "55"
    },
    {
      "stck_shrn_iscd": "433220",
      "data_rank": "25",
      "hts_kor_isnm": "에셋플러스 글로벌대장장이액티브",
      "stck_prpr": "13855",
      "prdy_vrss": "5",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "0.04",
      "acml_vol": "54",
      "tday_rltv": "999.99",
      "seln_cnqn_smtn": "0",
      "shnu_cnqn_smtn": "54"
    },
    {
      "stck_shrn_iscd": "Q530014",
      "data_rank": "26",
      "hts_kor_isnm": "삼성 China A50 선물 ETN(H)",
      "stck_prpr": "14910",
      "prdy_vrss": "55",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "0.37",
      "acml_vol": "51",
      "tday_rltv": "999.99",
      "seln_cnqn_smtn": "0",
      "shnu_cnqn_smtn": "51"
    },
    {
      "stck_shrn_iscd": "411540",
      "data_rank": "27",
      "hts_kor_isnm": "SOL 200 Top10",
      "stck_prpr": "9005",
      "prdy_vrss": "130",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "1.46",
      "acml_vol": "48",
      "tday_rltv": "999.99",
      "seln_cnqn_smtn": "0",
      "shnu_cnqn_smtn": "46"
    },
    {
      "stck_shrn_iscd": "227830",
      "data_rank": "28",
      "hts_kor_isnm": "ARIRANG 코스피",
      "stck_prpr": "28060",
      "prdy_vrss": "90",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "0.32",
      "acml_vol": "41",
      "tday_rltv": "999.99",
      "seln_cnqn_smtn": "0",
      "shnu_cnqn_smtn": "41"
    },
    {
      "stck_shrn_iscd": "375760",
      "data_rank": "29",
      "hts_kor_isnm": "HANARO 탄소효율그린뉴딜",
      "stck_prpr": "9070",
      "prdy_vrss": "45",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "0.50",
      "acml_vol": "37",
      "tday_rltv": "999.99",
      "seln_cnqn_smtn": "0",
      "shnu_cnqn_smtn": "37"
    },
    {
      "stck_shrn_iscd": "395750",
      "data_rank": "30",
      "hts_kor_isnm": "ARIRANG ESG가치주액티브",
      "stck_prpr": "8445",
      "prdy_vrss": "35",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "0.42",
      "acml_vol": "36",
      "tday_rltv": "999.99",
      "seln_cnqn_smtn": "0",
      "shnu_cnqn_smtn": "36"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```

