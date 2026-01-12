# 국내주식 이격도 순위[v1_국내주식-095]

> [국내주식] 순위분석

국내주식 이격도 순위 API입니다.
한국투자 HTS(eFriend Plus) > [0178] 이격도 순위 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.
최대 30건 확인 가능하며, 다음 조회가 불가합니다.

※ 30건 이상의 목록 조회가 필요한 경우, 대안으로 종목조건검색 API를 이용해서 원하는 종목 100개까지 검색할 수 있는 기능을 제공하고 있습니다.
종목조건검색 API는 HTS(efriend Plus) [0110] 조건검색에서 등록 및 서버저장한 나의 조건 목록을 확인할 수 있는 API로,
자세한 사용 방법은 공지사항 - [조건검색 필독] 조건검색 API 이용안내 참고 부탁드립니다.

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `5b33c1b2-bd6b-449d-9923-3f0439912c87` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/ranking/disparity` |
| **Content-Type** | `` |
| **요청 포맷** | `` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID** | `모의투자 미지원`, `FHPST01780000` |

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
| `tr_id` | 거래ID | String | 13 | Y | FHPST01780000 |
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
| `fid_cond_scr_div_code` | 조건 화면 분류 코드 | String | 5 | Y | Unique key( 20178 ) |
| `fid_div_cls_code` | 분류 구분 코드 | String | 2 | Y | 0: 전체, 1:관리종목, 2:투자주의, 3:투자경고, 4:투자위험예고, 5:투자위험, 6:보톧주, 7:우선주 |
| `fid_rank_sort_cls_code` | 순위 정렬 구분 코드 | String | 2 | Y | 0: 이격도상위순, 1:이격도하위순 |
| `fid_hour_cls_code` | 시간 구분 코드 | String | 5 | Y | 5:이격도5, 10:이격도10, 20:이격도20, 60:이격도60, 120:이격도120 |
| `fid_input_iscd` | 입력 종목코드 | String | 12 | Y | 0000:전체, 0001:거래소, 1001:코스닥, 2001:코스피200 |
| `fid_trgt_cls_code` | 대상 구분 코드 | String | 32 | Y | 0 : 전체 |
| `fid_trgt_exls_cls_code` | 대상 제외 구분 코드 | String | 32 | Y | 0 : 전체 |
| `fid_input_price_1` | 입력 가격1 | String | 12 | Y | 입력값 없을때 전체 (가격 ~) |
| `fid_vol_cnt` | 거래량 수 | String | 12 | Y | 입력값 없을때 전체 (거래량 ~) |

### 요청 예시

```json
{
  "fid_cond_mrkt_div_code": "J",
  "fid_cond_scr_div_code": "20178",
  "fid_div_cls_code": "0",
  "fid_rank_sort_cls_code": "0",
  "fid_hour_cls_code": "0000",
  "fid_input_iscd": "0000",
  "fid_trgt_cls_code": "0",
  "fid_trgt_exls_cls_code": "0",
  "fid_input_price_1": "",
  "fid_input_price_2": "",
  "fid_vol_cnt": ""
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
| `output` | 응답상세 | Object |   | Y | array |
| `mksc_shrn_iscd` | 유가증권 단축 종목코드 | String | 9 | Y |  |
| `data_rank` | 데이터 순위 | String | 10 | Y |  |
| `hts_kor_isnm` | HTS 한글 종목명 | String | 40 | Y |  |
| `stck_prpr` | 주식 현재가 | String | 10 | Y |  |
| `prdy_vrss` | 전일 대비 | String | 10 | Y |  |
| `prdy_ctrt` | 전일 대비율 | String | 82 | Y |  |
| `prdy_vrss_sign` | 전일 대비 부호 | String | 1 | Y |  |
| `acml_vol` | 누적 거래량 | String | 18 | Y |  |
| `d5_dsrt` | 5일 이격도 | String | 112 | Y |  |
| `d10_dsrt` | 10일 이격도 | String | 112 | Y |  |
| `d20_dsrt` | 20일 이격도 | String | 112 | Y |  |
| `d60_dsrt` | 60일 이격도 | String | 112 | Y |  |
| `d120_dsrt` | 120일 이격도 | String | 112 | Y |  |

### 응답 예시

```json
{
  "output": [
    {
      "mksc_shrn_iscd": "199800",
      "data_rank": "1",
      "hts_kor_isnm": "툴젠",
      "stck_prpr": "76100",
      "prdy_vrss": "17500",
      "prdy_ctrt": "29.86",
      "prdy_vrss_sign": "1",
      "acml_vol": "333421",
      "d5_dsrt": "126.92",
      "d10_dsrt": "137.66",
      "d20_dsrt": "143.04",
      "d60_dsrt": "134.37",
      "d120_dsrt": "146.59"
    },
    {
      "mksc_shrn_iscd": "032800",
      "data_rank": "2",
      "hts_kor_isnm": "판타지오",
      "stck_prpr": "394",
      "prdy_vrss": "63",
      "prdy_ctrt": "19.03",
      "prdy_vrss_sign": "2",
      "acml_vol": "42856944",
      "d5_dsrt": "125.32",
      "d10_dsrt": "154.75",
      "d20_dsrt": "181.27",
      "d60_dsrt": "183.38",
      "d120_dsrt": "169.90"
    },
    {
      "mksc_shrn_iscd": "083790",
      "data_rank": "3",
      "hts_kor_isnm": "CG인바이츠",
      "stck_prpr": "4235",
      "prdy_vrss": "855",
      "prdy_ctrt": "25.30",
      "prdy_vrss_sign": "2",
      "acml_vol": "3067053",
      "d5_dsrt": "123.18",
      "d10_dsrt": "121.02",
      "d20_dsrt": "118.13",
      "d60_dsrt": "138.02",
      "d120_dsrt": "145.73"
    },
    {
      "mksc_shrn_iscd": "237690",
      "data_rank": "4",
      "hts_kor_isnm": "에스티팜",
      "stck_prpr": "96400",
      "prdy_vrss": "18800",
      "prdy_ctrt": "24.23",
      "prdy_vrss_sign": "2",
      "acml_vol": "1694242",
      "d5_dsrt": "121.72",
      "d10_dsrt": "127.83",
      "d20_dsrt": "138.42",
      "d60_dsrt": "147.80",
      "d120_dsrt": "142.70"
    },
    {
      "mksc_shrn_iscd": "010660",
      "data_rank": "5",
      "hts_kor_isnm": "화천기계",
      "stck_prpr": "7250",
      "prdy_vrss": "990",
      "prdy_ctrt": "15.81",
      "prdy_vrss_sign": "2",
      "acml_vol": "10506735",
      "d5_dsrt": "120.59",
      "d10_dsrt": "135.12",
      "d20_dsrt": "149.55",
      "d60_dsrt": "179.64",
      "d120_dsrt": "175.87"
    },
    {
      "mksc_shrn_iscd": "103590",
      "data_rank": "6",
      "hts_kor_isnm": "일진전기",
      "stck_prpr": "17370",
      "prdy_vrss": "2690",
      "prdy_ctrt": "18.32",
      "prdy_vrss_sign": "2",
      "acml_vol": "10956331",
      "d5_dsrt": "119.93",
      "d10_dsrt": "128.02",
      "d20_dsrt": "142.95",
      "d60_dsrt": "149.68",
      "d120_dsrt": "144.38"
    },
    {
      "mksc_shrn_iscd": "276730",
      "data_rank": "7",
      "hts_kor_isnm": "제주맥주",
      "stck_prpr": "1492",
      "prdy_vrss": "148",
      "prdy_ctrt": "11.01",
      "prdy_vrss_sign": "2",
      "acml_vol": "3304408",
      "d5_dsrt": "116.44",
      "d10_dsrt": "127.45",
      "d20_dsrt": "137.72",
      "d60_dsrt": "150.64",
      "d120_dsrt": "147.72"
    },
    {
      "mksc_shrn_iscd": "189330",
      "data_rank": "8",
      "hts_kor_isnm": "씨이랩",
      "stck_prpr": "17130",
      "prdy_vrss": "-70",
      "prdy_ctrt": "-0.41",
      "prdy_vrss_sign": "5",
      "acml_vol": "552497",
      "d5_dsrt": "116.28",
      "d10_dsrt": "131.23",
      "d20_dsrt": "137.29",
      "d60_dsrt": "145.68",
      "d120_dsrt": "143.29"
    },
    {
      "mksc_shrn_iscd": "255220",
      "data_rank": "9",
      "hts_kor_isnm": "SG",
      "stck_prpr": "2550",
      "prdy_vrss": "-215",
      "prdy_ctrt": "-7.78",
      "prdy_vrss_sign": "5",
      "acml_vol": "16959683",
      "d5_dsrt": "116.25",
      "d10_dsrt": "128.68",
      "d20_dsrt": "143.81",
      "d60_dsrt": "155.60",
      "d120_dsrt": "176.12"
    },
    {
      "mksc_shrn_iscd": "101000",
      "data_rank": "10",
      "hts_kor_isnm": "상상인인더스트리",
      "stck_prpr": "3510",
      "prdy_vrss": "55",
      "prdy_ctrt": "1.59",
      "prdy_vrss_sign": "2",
      "acml_vol": "679073",
      "d5_dsrt": "115.96",
      "d10_dsrt": "134.74",
      "d20_dsrt": "149.26",
      "d60_dsrt": "154.00",
      "d120_dsrt": "159.79"
    },
    {
      "mksc_shrn_iscd": "060230",
      "data_rank": "11",
      "hts_kor_isnm": "소니드",
      "stck_prpr": "2570",
      "prdy_vrss": "475",
      "prdy_ctrt": "22.67",
      "prdy_vrss_sign": "2",
      "acml_vol": "3807050",
      "d5_dsrt": "115.71",
      "d10_dsrt": "115.45",
      "d20_dsrt": "105.64",
      "d60_dsrt": "121.17",
      "d120_dsrt": "110.82"
    },
    {
      "mksc_shrn_iscd": "073570",
      "data_rank": "12",
      "hts_kor_isnm": "리튬포어스",
      "stck_prpr": "6870",
      "prdy_vrss": "1470",
      "prdy_ctrt": "27.22",
      "prdy_vrss_sign": "2",
      "acml_vol": "5384918",
      "d5_dsrt": "115.58",
      "d10_dsrt": "112.84",
      "d20_dsrt": "118.04",
      "d60_dsrt": "113.48",
      "d120_dsrt": "93.27"
    },
    {
      "mksc_shrn_iscd": "036220",
      "data_rank": "13",
      "hts_kor_isnm": "오상헬스케어",
      "stck_prpr": "25300",
      "prdy_vrss": "100",
      "prdy_ctrt": "0.40",
      "prdy_vrss_sign": "2",
      "acml_vol": "175169",
      "d5_dsrt": "115.47",
      "d10_dsrt": "202.87",
      "d20_dsrt": "287.60",
      "d60_dsrt": "385.34",
      "d120_dsrt": "327.55"
    },
    {
      "mksc_shrn_iscd": "321370",
      "data_rank": "14",
      "hts_kor_isnm": "센서뷰",
      "stck_prpr": "4890",
      "prdy_vrss": "790",
      "prdy_ctrt": "19.27",
      "prdy_vrss_sign": "2",
      "acml_vol": "5626573",
      "d5_dsrt": "114.73",
      "d10_dsrt": "117.60",
      "d20_dsrt": "112.33",
      "d60_dsrt": "102.91",
      "d120_dsrt": "108.28"
    },
    {
      "mksc_shrn_iscd": "030350",
      "data_rank": "15",
      "hts_kor_isnm": "드래곤플라이",
      "stck_prpr": "614",
      "prdy_vrss": "-7",
      "prdy_ctrt": "-1.13",
      "prdy_vrss_sign": "5",
      "acml_vol": "13499054",
      "d5_dsrt": "114.72",
      "d10_dsrt": "119.64",
      "d20_dsrt": "116.56",
      "d60_dsrt": "103.46",
      "d120_dsrt": "105.08"
    },
    {
      "mksc_shrn_iscd": "066910",
      "data_rank": "16",
      "hts_kor_isnm": "손오공",
      "stck_prpr": "3800",
      "prdy_vrss": "470",
      "prdy_ctrt": "14.11",
      "prdy_vrss_sign": "2",
      "acml_vol": "2211703",
      "d5_dsrt": "114.25",
      "d10_dsrt": "125.60",
      "d20_dsrt": "132.42",
      "d60_dsrt": "132.81",
      "d120_dsrt": "148.85"
    },
    {
      "mksc_shrn_iscd": "115530",
      "data_rank": "17",
      "hts_kor_isnm": "씨엔플러스",
      "stck_prpr": "340",
      "prdy_vrss": "-5",
      "prdy_ctrt": "-1.45",
      "prdy_vrss_sign": "5",
      "acml_vol": "9226496",
      "d5_dsrt": "114.17",
      "d10_dsrt": "117.16",
      "d20_dsrt": "110.16",
      "d60_dsrt": "103.26",
      "d120_dsrt": "92.59"
    },
    {
      "mksc_shrn_iscd": "219130",
      "data_rank": "18",
      "hts_kor_isnm": "타이거일렉",
      "stck_prpr": "38550",
      "prdy_vrss": "5550",
      "prdy_ctrt": "16.82",
      "prdy_vrss_sign": "2",
      "acml_vol": "306979",
      "d5_dsrt": "112.98",
      "d10_dsrt": "115.90",
      "d20_dsrt": "119.17",
      "d60_dsrt": "147.68",
      "d120_dsrt": "168.89"
    },
    {
      "mksc_shrn_iscd": "053030",
      "data_rank": "19",
      "hts_kor_isnm": "바이넥스",
      "stck_prpr": "18190",
      "prdy_vrss": "1730",
      "prdy_ctrt": "10.51",
      "prdy_vrss_sign": "2",
      "acml_vol": "6841463",
      "d5_dsrt": "112.84",
      "d10_dsrt": "128.02",
      "d20_dsrt": "143.73",
      "d60_dsrt": "174.00",
      "d120_dsrt": "198.06"
    },
    {
      "mksc_shrn_iscd": "008600",
      "data_rank": "20",
      "hts_kor_isnm": "윌비스",
      "stck_prpr": "575",
      "prdy_vrss": "45",
      "prdy_ctrt": "8.49",
      "prdy_vrss_sign": "2",
      "acml_vol": "4543051",
      "d5_dsrt": "112.83",
      "d10_dsrt": "115.30",
      "d20_dsrt": "111.54",
      "d60_dsrt": "97.44",
      "d120_dsrt": "97.79"
    },
    {
      "mksc_shrn_iscd": "091970",
      "data_rank": "21",
      "hts_kor_isnm": "나노캠텍",
      "stck_prpr": "777",
      "prdy_vrss": "123",
      "prdy_ctrt": "18.81",
      "prdy_vrss_sign": "2",
      "acml_vol": "1580766",
      "d5_dsrt": "112.12",
      "d10_dsrt": "110.95",
      "d20_dsrt": "103.11",
      "d60_dsrt": "88.09",
      "d120_dsrt": "83.87"
    },
    {
      "mksc_shrn_iscd": "000680",
      "data_rank": "22",
      "hts_kor_isnm": "LS네트웍스",
      "stck_prpr": "5350",
      "prdy_vrss": "-290",
      "prdy_ctrt": "-5.14",
      "prdy_vrss_sign": "5",
      "acml_vol": "7951524",
      "d5_dsrt": "112.04",
      "d10_dsrt": "121.22",
      "d20_dsrt": "123.64",
      "d60_dsrt": "121.96",
      "d120_dsrt": "121.76"
    },
    {
      "mksc_shrn_iscd": "010640",
      "data_rank": "23",
      "hts_kor_isnm": "진양폴리",
      "stck_prpr": "6700",
      "prdy_vrss": "560",
      "prdy_ctrt": "9.12",
      "prdy_vrss_sign": "2",
      "acml_vol": "330657",
      "d5_dsrt": "111.74",
      "d10_dsrt": "116.85",
      "d20_dsrt": "119.33",
      "d60_dsrt": "113.49",
      "d120_dsrt": "104.66"
    },
    {
      "mksc_shrn_iscd": "000150",
      "data_rank": "24",
      "hts_kor_isnm": "두산",
      "stck_prpr": "150400",
      "prdy_vrss": "5400",
      "prdy_ctrt": "3.72",
      "prdy_vrss_sign": "2",
      "acml_vol": "205583",
      "d5_dsrt": "111.71",
      "d10_dsrt": "126.98",
      "d20_dsrt": "140.65",
      "d60_dsrt": "158.32",
      "d120_dsrt": "164.12"
    },
    {
      "mksc_shrn_iscd": "119860",
      "data_rank": "25",
      "hts_kor_isnm": "커넥트웨이브",
      "stck_prpr": "15270",
      "prdy_vrss": "10",
      "prdy_ctrt": "0.07",
      "prdy_vrss_sign": "2",
      "acml_vol": "196410",
      "d5_dsrt": "111.46",
      "d10_dsrt": "113.09",
      "d20_dsrt": "110.40",
      "d60_dsrt": "106.56",
      "d120_dsrt": "120.72"
    },
    {
      "mksc_shrn_iscd": "105740",
      "data_rank": "26",
      "hts_kor_isnm": "디케이락",
      "stck_prpr": "9420",
      "prdy_vrss": "1070",
      "prdy_ctrt": "12.81",
      "prdy_vrss_sign": "2",
      "acml_vol": "3498003",
      "d5_dsrt": "111.40",
      "d10_dsrt": "115.50",
      "d20_dsrt": "115.86",
      "d60_dsrt": "111.85",
      "d120_dsrt": "106.17"
    },
    {
      "mksc_shrn_iscd": "219550",
      "data_rank": "27",
      "hts_kor_isnm": "디와이디",
      "stck_prpr": "1010",
      "prdy_vrss": "-23",
      "prdy_ctrt": "-2.23",
      "prdy_vrss_sign": "5",
      "acml_vol": "1923238",
      "d5_dsrt": "111.14",
      "d10_dsrt": "118.50",
      "d20_dsrt": "128.36",
      "d60_dsrt": "126.66",
      "d120_dsrt": "113.85"
    },
    {
      "mksc_shrn_iscd": "001040",
      "data_rank": "28",
      "hts_kor_isnm": "CJ",
      "stck_prpr": "111100",
      "prdy_vrss": "1900",
      "prdy_ctrt": "1.74",
      "prdy_vrss_sign": "2",
      "acml_vol": "234342",
      "d5_dsrt": "111.06",
      "d10_dsrt": "113.97",
      "d20_dsrt": "113.04",
      "d60_dsrt": "115.40",
      "d120_dsrt": "120.89"
    },
    {
      "mksc_shrn_iscd": "110020",
      "data_rank": "29",
      "hts_kor_isnm": "전진바이오팜",
      "stck_prpr": "8690",
      "prdy_vrss": "680",
      "prdy_ctrt": "8.49",
      "prdy_vrss_sign": "2",
      "acml_vol": "173087",
      "d5_dsrt": "110.79",
      "d10_dsrt": "111.85",
      "d20_dsrt": "110.95",
      "d60_dsrt": "103.49",
      "d120_dsrt": "109.97"
    },
    {
      "mksc_shrn_iscd": "001440",
      "data_rank": "30",
      "hts_kor_isnm": "대한전선",
      "stck_prpr": "10990",
      "prdy_vrss": "890",
      "prdy_ctrt": "8.81",
      "prdy_vrss_sign": "2",
      "acml_vol": "6305591",
      "d5_dsrt": "110.76",
      "d10_dsrt": "115.88",
      "d20_dsrt": "116.62",
      "d60_dsrt": "118.40",
      "d120_dsrt": "109.38"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```
