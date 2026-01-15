# 국내주식 예상체결 상승/하락상위[v1_국내주식-103]

> [국내주식] 순위분석

국내주식 예상체결 상승/하락상위 API입니다.
한국투자 HTS(eFriend Plus) > [0182] 예상체결 상승/하락상위 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.
최대 30건 확인 가능하며, 다음 조회가 불가합니다.

※ 30건 이상의 목록 조회가 필요한 경우, 대안으로 종목조건검색 API를 이용해서 원하는 종목 100개까지 검색할 수 있는 기능을 제공하고 있습니다.
종목조건검색 API는 HTS(efriend Plus) [0110] 조건검색에서 등록 및 서버저장한 나의 조건 목록을 확인할 수 있는 API로,
자세한 사용 방법은 공지사항 - [조건검색 필독] 조건검색 API 이용안내 참고 부탁드립니다.


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `05a719af-aa3c-46c7-a670-55f2f11654c2` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/ranking/exp-trans-updown` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `FHPST01820000` |
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
| `tr_id` | 거래ID | String | 13 | Y | FHPST01820000 |
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
| `fid_rank_sort_cls_code` | 순위 정렬 구분 코드 | String | 2 | Y | 0:상승률1:상승폭2:보합3:하락율4:하락폭5:체결량6:거래대금 |
| `fid_cond_mrkt_div_code` | 조건 시장 분류 코드 | String | 2 | Y | 시장구분코드 (주식 J) |
| `fid_cond_scr_div_code` | 조건 화면 분류 코드 | String | 5 | Y | Unique key(20182) |
| `fid_input_iscd` | 입력 종목코드 | String | 12 | Y | 0000:전체, 0001:거래소, 1001:코스닥, 2001:코스피200, 4001: KRX100 |
| `fid_div_cls_code` | 분류 구분 코드 | String | 2 | Y | 0:전체 1:보통주 2:우선주 |
| `fid_aply_rang_prc_1` | 적용 범위 가격1 | String | 18 | Y | 입력값 없을때 전체 (가격 ~) |
| `fid_vol_cnt` | 거래량 수 | String | 12 | Y | 입력값 없을때 전체 (거래량 ~) |
| `fid_pbmn` | 거래대금 | String | 18 | Y | 입력값 없을때 전체 (거래대금 ~) 천원단위 |
| `fid_blng_cls_code` | 소속 구분 코드 | String | 2 | Y | 0: 전체 |
| `fid_mkop_cls_code` | 장운영 구분 코드 | String | 2 | Y | 0:장전예상1:장마감예상 |

### 요청 예시

```json
{
  "fid_cond_mrkt_div_code": "J",
  "fid_cond_scr_div_code": "20182",
  "fid_input_iscd": "0000",
  "fid_div_cls_code": "0",
  "fid_aply_rang_prc_1": "",
  "fid_vol_cnt": "",
  "fid_pbmn": "",
  "fid_blng_cls_code": "0",
  "fid_mkop_cls_code": "0",
  "fid_rank_sort_cls_code": "0"
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
| `hts_kor_isnm` | HTS 한글 종목명 | String | 40 | Y |  |
| `stck_prpr` | 주식 현재가 | String | 10 | Y |  |
| `prdy_vrss` | 전일 대비 | String | 10 | Y |  |
| `prdy_vrss_sign` | 전일 대비 부호 | String | 1 | Y |  |
| `prdy_ctrt` | 전일 대비율 | String | 82 | Y |  |
| `stck_sdpr` | 주식 기준가 | String | 10 | Y |  |
| `seln_rsqn` | 매도 잔량 | String | 12 | Y |  |
| `askp` | 매도호가 | String | 10 | Y |  |
| `bidp` | 매수호가 | String | 10 | Y |  |
| `shnu_rsqn` | 매수2 잔량 | String | 12 | Y |  |
| `cntg_vol` | 체결 거래량 | String | 18 | Y |  |
| `antc_tr_pbmn` | 체결 거래대금 | String | 18 | Y |  |
| `total_askp_rsqn` | 총 매도호가 잔량 | String | 12 | Y |  |
| `total_bidp_rsqn` | 총 매수호가 잔량 | String | 12 | Y |  |

### 응답 예시

```json
{
  "output": [
    {
      "stck_shrn_iscd": "199800",
      "hts_kor_isnm": "툴젠",
      "stck_prpr": "76100",
      "prdy_vrss": "17500",
      "prdy_vrss_sign": "1",
      "prdy_ctrt": "29.86",
      "stck_sdpr": "58600",
      "seln_rsqn": "0",
      "askp": "0",
      "bidp": "76100",
      "shnu_rsqn": "49100",
      "cntg_vol": "51683",
      "antc_tr_pbmn": "3933076300",
      "total_askp_rsqn": "0",
      "total_bidp_rsqn": "67064"
    },
    {
      "stck_shrn_iscd": "378340",
      "hts_kor_isnm": "필에너지",
      "stck_prpr": "31800",
      "prdy_vrss": "3400",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "11.97",
      "stck_sdpr": "28400",
      "seln_rsqn": "10680",
      "askp": "31800",
      "bidp": "31750",
      "shnu_rsqn": "6215",
      "cntg_vol": "198612",
      "antc_tr_pbmn": "6315861600",
      "total_askp_rsqn": "14705",
      "total_bidp_rsqn": "71743"
    },
    {
      "stck_shrn_iscd": "115530",
      "hts_kor_isnm": "씨엔플러스",
      "stck_prpr": "386",
      "prdy_vrss": "41",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "11.88",
      "stck_sdpr": "345",
      "seln_rsqn": "3257",
      "askp": "386",
      "bidp": "385",
      "shnu_rsqn": "92624",
      "cntg_vol": "1150496",
      "antc_tr_pbmn": "72949040",
      "total_askp_rsqn": "33272",
      "total_bidp_rsqn": "173439"
    },
    {
      "stck_shrn_iscd": "Q580040",
      "hts_kor_isnm": "KB 인버스 2X KOSPI 200 선물 ETN",
      "stck_prpr": "13305",
      "prdy_vrss": "1205",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "9.96",
      "stck_sdpr": "12100",
      "seln_rsqn": "0",
      "askp": "0",
      "bidp": "12730",
      "shnu_rsqn": "69",
      "cntg_vol": "13",
      "antc_tr_pbmn": "172965",
      "total_askp_rsqn": "49927",
      "total_bidp_rsqn": "15061"
    },
    {
      "stck_shrn_iscd": "078150",
      "hts_kor_isnm": "HB테크놀러지",
      "stck_prpr": "2620",
      "prdy_vrss": "230",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "9.62",
      "stck_sdpr": "2390",
      "seln_rsqn": "53479",
      "askp": "2625",
      "bidp": "2620",
      "shnu_rsqn": "7114",
      "cntg_vol": "822185",
      "antc_tr_pbmn": "2154124700",
      "total_askp_rsqn": "332932",
      "total_bidp_rsqn": "206643"
    },
    {
      "stck_shrn_iscd": "094820",
      "hts_kor_isnm": "일진파워",
      "stck_prpr": "13470",
      "prdy_vrss": "1150",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "9.33",
      "stck_sdpr": "12320",
      "seln_rsqn": "7647",
      "askp": "13470",
      "bidp": "13460",
      "shnu_rsqn": "680",
      "cntg_vol": "46521",
      "antc_tr_pbmn": "626637870",
      "total_askp_rsqn": "6235",
      "total_bidp_rsqn": "8704"
    },
    {
      "stck_shrn_iscd": "193250",
      "hts_kor_isnm": "와이제이엠게임즈",
      "stck_prpr": "827",
      "prdy_vrss": "66",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "8.67",
      "stck_sdpr": "761",
      "seln_rsqn": "5014",
      "askp": "827",
      "bidp": "826",
      "shnu_rsqn": "41",
      "cntg_vol": "19093",
      "antc_tr_pbmn": "49621503",
      "total_askp_rsqn": "10094",
      "total_bidp_rsqn": "36639"
    },
    {
      "stck_shrn_iscd": "030350",
      "hts_kor_isnm": "드래곤플라이",
      "stck_prpr": "674",
      "prdy_vrss": "53",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "8.53",
      "stck_sdpr": "621",
      "seln_rsqn": "2351",
      "askp": "674",
      "bidp": "672",
      "shnu_rsqn": "2501",
      "cntg_vol": "1000046",
      "antc_tr_pbmn": "23279190",
      "total_askp_rsqn": "47302",
      "total_bidp_rsqn": "211603"
    },
    {
      "stck_shrn_iscd": "020760",
      "hts_kor_isnm": "일진디스플",
      "stck_prpr": "979",
      "prdy_vrss": "75",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "8.30",
      "stck_sdpr": "904",
      "seln_rsqn": "6015",
      "askp": "979",
      "bidp": "952",
      "shnu_rsqn": "220",
      "cntg_vol": "6214",
      "antc_tr_pbmn": "6083506",
      "total_askp_rsqn": "16585",
      "total_bidp_rsqn": "5613"
    },
    {
      "stck_shrn_iscd": "321370",
      "hts_kor_isnm": "센서뷰",
      "stck_prpr": "4420",
      "prdy_vrss": "320",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "7.80",
      "stck_sdpr": "4100",
      "seln_rsqn": "4038",
      "askp": "4420",
      "bidp": "4410",
      "shnu_rsqn": "291",
      "cntg_vol": "41019",
      "antc_tr_pbmn": "552669480",
      "total_askp_rsqn": "22631",
      "total_bidp_rsqn": "26665"
    },
    {
      "stck_shrn_iscd": "105740",
      "hts_kor_isnm": "디케이락",
      "stck_prpr": "8960",
      "prdy_vrss": "610",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "7.31",
      "stck_sdpr": "8350",
      "seln_rsqn": "1321",
      "askp": "8970",
      "bidp": "8960",
      "shnu_rsqn": "9811",
      "cntg_vol": "62727",
      "antc_tr_pbmn": "698595660",
      "total_askp_rsqn": "3450",
      "total_bidp_rsqn": "16822"
    },
    {
      "stck_shrn_iscd": "103590",
      "hts_kor_isnm": "일진전기",
      "stck_prpr": "15700",
      "prdy_vrss": "1020",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "6.95",
      "stck_sdpr": "14680",
      "seln_rsqn": "1163",
      "askp": "15710",
      "bidp": "15700",
      "shnu_rsqn": "8187",
      "cntg_vol": "111684",
      "antc_tr_pbmn": "959050680",
      "total_askp_rsqn": "3352",
      "total_bidp_rsqn": "50667"
    },
    {
      "stck_shrn_iscd": "101000",
      "hts_kor_isnm": "상상인인더스트리",
      "stck_prpr": "3690",
      "prdy_vrss": "235",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "6.80",
      "stck_sdpr": "3455",
      "seln_rsqn": "1078",
      "askp": "3690",
      "bidp": "3600",
      "shnu_rsqn": "408",
      "cntg_vol": "59127",
      "antc_tr_pbmn": "34685280",
      "total_askp_rsqn": "9513",
      "total_bidp_rsqn": "12837"
    },
    {
      "stck_shrn_iscd": "211050",
      "hts_kor_isnm": "인카금융서비스",
      "stck_prpr": "24000",
      "prdy_vrss": "1450",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "6.43",
      "stck_sdpr": "22550",
      "seln_rsqn": "823",
      "askp": "24000",
      "bidp": "22550",
      "shnu_rsqn": "122",
      "cntg_vol": "1958",
      "antc_tr_pbmn": "2436000",
      "total_askp_rsqn": "1066",
      "total_bidp_rsqn": "4599"
    },
    {
      "stck_shrn_iscd": "010660",
      "hts_kor_isnm": "화천기계",
      "stck_prpr": "6660",
      "prdy_vrss": "400",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "6.39",
      "stck_sdpr": "6260",
      "seln_rsqn": "1260",
      "askp": "6670",
      "bidp": "6660",
      "shnu_rsqn": "8959",
      "cntg_vol": "219634",
      "antc_tr_pbmn": "640185240",
      "total_askp_rsqn": "63618",
      "total_bidp_rsqn": "17278"
    },
    {
      "stck_shrn_iscd": "110020",
      "hts_kor_isnm": "전진바이오팜",
      "stck_prpr": "8500",
      "prdy_vrss": "490",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "6.12",
      "stck_sdpr": "8010",
      "seln_rsqn": "999",
      "askp": "8500",
      "bidp": "8240",
      "shnu_rsqn": "10",
      "cntg_vol": "11074",
      "antc_tr_pbmn": "94129000",
      "total_askp_rsqn": "15232",
      "total_bidp_rsqn": "8635"
    },
    {
      "stck_shrn_iscd": "095700",
      "hts_kor_isnm": "제넥신",
      "stck_prpr": "8790",
      "prdy_vrss": "500",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "6.03",
      "stck_sdpr": "8290",
      "seln_rsqn": "899",
      "askp": "8790",
      "bidp": "8750",
      "shnu_rsqn": "6640",
      "cntg_vol": "23275",
      "antc_tr_pbmn": "204587250",
      "total_askp_rsqn": "6140",
      "total_bidp_rsqn": "10924"
    },
    {
      "stck_shrn_iscd": "276730",
      "hts_kor_isnm": "제주맥주",
      "stck_prpr": "1425",
      "prdy_vrss": "81",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "6.03",
      "stck_sdpr": "1344",
      "seln_rsqn": "2279",
      "askp": "1427",
      "bidp": "1425",
      "shnu_rsqn": "4898",
      "cntg_vol": "74274",
      "antc_tr_pbmn": "105840450",
      "total_askp_rsqn": "33433",
      "total_bidp_rsqn": "12694"
    },
    {
      "stck_shrn_iscd": "161580",
      "hts_kor_isnm": "필옵틱스",
      "stck_prpr": "17020",
      "prdy_vrss": "950",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "5.91",
      "stck_sdpr": "16070",
      "seln_rsqn": "916",
      "askp": "17030",
      "bidp": "17020",
      "shnu_rsqn": "3118",
      "cntg_vol": "191675",
      "antc_tr_pbmn": "3262308500",
      "total_askp_rsqn": "13074",
      "total_bidp_rsqn": "22881"
    },
    {
      "stck_shrn_iscd": "000040",
      "hts_kor_isnm": "KR모터스",
      "stck_prpr": "1624",
      "prdy_vrss": "90",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "5.87",
      "stck_sdpr": "1624",
      "seln_rsqn": "7317",
      "askp": "1624",
      "bidp": "1623",
      "shnu_rsqn": "1",
      "cntg_vol": "78804",
      "antc_tr_pbmn": "49541596",
      "total_askp_rsqn": "4228",
      "total_bidp_rsqn": "4191"
    },
    {
      "stck_shrn_iscd": "234920",
      "hts_kor_isnm": "자이글",
      "stck_prpr": "8940",
      "prdy_vrss": "490",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "5.80",
      "stck_sdpr": "8450",
      "seln_rsqn": "230",
      "askp": "8940",
      "bidp": "8920",
      "shnu_rsqn": "85",
      "cntg_vol": "4391",
      "antc_tr_pbmn": "39255540",
      "total_askp_rsqn": "2307",
      "total_bidp_rsqn": "7692"
    },
    {
      "stck_shrn_iscd": "297890",
      "hts_kor_isnm": "HB솔루션",
      "stck_prpr": "4370",
      "prdy_vrss": "215",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "5.17",
      "stck_sdpr": "4155",
      "seln_rsqn": "7844",
      "askp": "4370",
      "bidp": "4365",
      "shnu_rsqn": "3918",
      "cntg_vol": "116931",
      "antc_tr_pbmn": "510988470",
      "total_askp_rsqn": "183035",
      "total_bidp_rsqn": "40374"
    },
    {
      "stck_shrn_iscd": "457190",
      "hts_kor_isnm": "이수스페셜티케미컬",
      "stck_prpr": "360000",
      "prdy_vrss": "17500",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "5.11",
      "stck_sdpr": "342500",
      "seln_rsqn": "144",
      "askp": "360500",
      "bidp": "360000",
      "shnu_rsqn": "73",
      "cntg_vol": "8151",
      "antc_tr_pbmn": "1575276500",
      "total_askp_rsqn": "5572",
      "total_bidp_rsqn": "1942"
    },
    {
      "stck_shrn_iscd": "060230",
      "hts_kor_isnm": "소니드",
      "stck_prpr": "2200",
      "prdy_vrss": "105",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "5.01",
      "stck_sdpr": "2095",
      "seln_rsqn": "296",
      "askp": "2200",
      "bidp": "2195",
      "shnu_rsqn": "630",
      "cntg_vol": "11412",
      "antc_tr_pbmn": "134993250",
      "total_askp_rsqn": "52480",
      "total_bidp_rsqn": "54345"
    },
    {
      "stck_shrn_iscd": "101670",
      "hts_kor_isnm": "하이드로리튬",
      "stck_prpr": "6490",
      "prdy_vrss": "300",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "4.85",
      "stck_sdpr": "6190",
      "seln_rsqn": "160",
      "askp": "6490",
      "bidp": "6480",
      "shnu_rsqn": "660",
      "cntg_vol": "39612",
      "antc_tr_pbmn": "734458480",
      "total_askp_rsqn": "97472",
      "total_bidp_rsqn": "88960"
    },
    {
      "stck_shrn_iscd": "303030",
      "hts_kor_isnm": "지니틱스",
      "stck_prpr": "2275",
      "prdy_vrss": "105",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "4.84",
      "stck_sdpr": "2170",
      "seln_rsqn": "922",
      "askp": "2275",
      "bidp": "2255",
      "shnu_rsqn": "6749",
      "cntg_vol": "9329",
      "antc_tr_pbmn": "21223475",
      "total_askp_rsqn": "24653",
      "total_bidp_rsqn": "32378"
    },
    {
      "stck_shrn_iscd": "017940",
      "hts_kor_isnm": "E1",
      "stck_prpr": "73800",
      "prdy_vrss": "3400",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "4.83",
      "stck_sdpr": "70400",
      "seln_rsqn": "306",
      "askp": "73800",
      "bidp": "73700",
      "shnu_rsqn": "24",
      "cntg_vol": "7337",
      "antc_tr_pbmn": "541470600",
      "total_askp_rsqn": "1165",
      "total_bidp_rsqn": "2062"
    },
    {
      "stck_shrn_iscd": "237690",
      "hts_kor_isnm": "에스티팜",
      "stck_prpr": "81300",
      "prdy_vrss": "3700",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "4.77",
      "stck_sdpr": "77600",
      "seln_rsqn": "834",
      "askp": "81400",
      "bidp": "81300",
      "shnu_rsqn": "312",
      "cntg_vol": "14128",
      "antc_tr_pbmn": "1147201200",
      "total_askp_rsqn": "9707",
      "total_bidp_rsqn": "10412"
    },
    {
      "stck_shrn_iscd": "082210",
      "hts_kor_isnm": "옵트론텍",
      "stck_prpr": "4300",
      "prdy_vrss": "185",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "4.50",
      "stck_sdpr": "4115",
      "seln_rsqn": "327",
      "askp": "4305",
      "bidp": "4300",
      "shnu_rsqn": "2099",
      "cntg_vol": "30755",
      "antc_tr_pbmn": "132246500",
      "total_askp_rsqn": "10418",
      "total_bidp_rsqn": "25612"
    },
    {
      "stck_shrn_iscd": "049120",
      "hts_kor_isnm": "파인디앤씨",
      "stck_prpr": "1385",
      "prdy_vrss": "59",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "4.45",
      "stck_sdpr": "1326",
      "seln_rsqn": "973",
      "askp": "1429",
      "bidp": "1385",
      "shnu_rsqn": "830",
      "cntg_vol": "442",
      "antc_tr_pbmn": "612170",
      "total_askp_rsqn": "4905",
      "total_bidp_rsqn": "8454"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```

