# 국내주식 시간외잔량 순위[v1_국내주식-093]

> [국내주식] 순위분석

국내주식 시간외잔량 순위 API입니다.
한국투자 HTS(eFriend Plus) > [0176] 시간외잔량 상위 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.
최대 30건 확인 가능하며, 다음 조회가 불가합니다.

※ 30건 이상의 목록 조회가 필요한 경우, 대안으로 종목조건검색 API를 이용해서 원하는 종목 100개까지 검색할 수 있는 기능을 제공하고 있습니다.
종목조건검색 API는 HTS(efriend Plus) [0110] 조건검색에서 등록 및 서버저장한 나의 조건 목록을 확인할 수 있는 API로,
자세한 사용 방법은 공지사항 - [조건검색 필독] 조건검색 API 이용안내 참고 부탁드립니다.


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `4490b65c-3c6e-4e8b-b525-f5b48fe88710` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/ranking/after-hour-balance` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `FHPST01760000` |
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
| `tr_id` | 거래ID | String | 13 | Y | FHPST01760000 |
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
| `fid_input_price_1` | 입력 가격1 | String | 12 | Y | 입력값 없을때 전체 (가격 ~) |
| `fid_cond_mrkt_div_code` | 조건 시장 분류 코드 | String | 2 | Y | 시장구분코드 (주식 J) |
| `fid_cond_scr_div_code` | 조건 화면 분류 코드 | String | 5 | Y | Unique key( 20176 ) |
| `fid_rank_sort_cls_code` | 순위 정렬 구분 코드 | String | 2 | Y | 1: 장전 시간외, 2: 장후 시간외, 3:매도잔량, 4:매수잔량 |
| `fid_div_cls_code` | 분류 구분 코드 | String | 2 | Y | 0 : 전체 |
| `fid_input_iscd` | 입력 종목코드 | String | 12 | Y | 0000:전체, 0001:거래소, 1001:코스닥, 2001:코스피200 |
| `fid_trgt_exls_cls_code` | 대상 제외 구분 코드 | String | 32 | Y | 0 : 전체 |
| `fid_trgt_cls_code` | 대상 구분 코드 | String | 32 | Y | 0 : 전체 |
| `fid_vol_cnt` | 거래량 수 | String | 12 | Y | 입력값 없을때 전체 (거래량 ~) |
| `fid_input_price_2` | 입력 가격2 | String | 12 | Y | 입력값 없을때 전체 (~ 가격) |

### 요청 예시

```json
{
"fid_cond_mrkt_div_code":"J",
"fid_cond_scr_div_code":"20176",
"fid_rank_sort_cls_code":"1",
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
| `stck_shrn_iscd` | 주식 단축 종목코드 | String | 9 | Y |  |
| `data_rank` | 데이터 순위 | String | 10 | Y |  |
| `hts_kor_isnm` | HTS 한글 종목명 | String | 40 | Y |  |
| `stck_prpr` | 주식 현재가 | String | 10 | Y |  |
| `prdy_vrss` | 전일 대비 | String | 10 | Y |  |
| `prdy_vrss_sign` | 전일 대비 부호 | String | 1 | Y |  |
| `prdy_ctrt` | 전일 대비율 | String | 82 | Y |  |
| `ovtm_total_askp_rsqn` | 시간외 총 매도호가 잔량 | String | 12 | Y |  |
| `ovtm_total_bidp_rsqn` | 시간외 총 매수호가 잔량 | String | 12 | Y |  |
| `mkob_otcp_vol` | 장개시전 시간외종가 거래량 | String | 18 | Y |  |
| `mkfa_otcp_vol` | 장종료후 시간외종가 거래량 | String | 18 | Y |  |

### 응답 예시

```json
{
  "output": [
    {
      "stck_shrn_iscd": "252670",
      "data_rank": "1",
      "hts_kor_isnm": "KODEX 200선물인버스2X",
      "stck_prpr": "2170",
      "prdy_vrss": "-10",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-0.46",
      "ovtm_total_askp_rsqn": "0",
      "ovtm_total_bidp_rsqn": "0",
      "mkob_otcp_vol": "451685",
      "mkfa_otcp_vol": "0"
    },
    {
      "stck_shrn_iscd": "255220",
      "data_rank": "2",
      "hts_kor_isnm": "SG",
      "stck_prpr": "2565",
      "prdy_vrss": "-200",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-7.23",
      "ovtm_total_askp_rsqn": "0",
      "ovtm_total_bidp_rsqn": "0",
      "mkob_otcp_vol": "216921",
      "mkfa_otcp_vol": "0"
    },
    {
      "stck_shrn_iscd": "001470",
      "data_rank": "3",
      "hts_kor_isnm": "삼부토건",
      "stck_prpr": "2535",
      "prdy_vrss": "-155",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-5.76",
      "ovtm_total_askp_rsqn": "0",
      "ovtm_total_bidp_rsqn": "0",
      "mkob_otcp_vol": "77285",
      "mkfa_otcp_vol": "0"
    },
    {
      "stck_shrn_iscd": "253590",
      "data_rank": "4",
      "hts_kor_isnm": "네오셈",
      "stck_prpr": "15850",
      "prdy_vrss": "-200",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-1.25",
      "ovtm_total_askp_rsqn": "0",
      "ovtm_total_bidp_rsqn": "0",
      "mkob_otcp_vol": "45191",
      "mkfa_otcp_vol": "0"
    },
    {
      "stck_shrn_iscd": "065450",
      "data_rank": "5",
      "hts_kor_isnm": "빅텍",
      "stck_prpr": "5180",
      "prdy_vrss": "80",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "1.57",
      "ovtm_total_askp_rsqn": "0",
      "ovtm_total_bidp_rsqn": "0",
      "mkob_otcp_vol": "39634",
      "mkfa_otcp_vol": "0"
    },
    {
      "stck_shrn_iscd": "001780",
      "data_rank": "6",
      "hts_kor_isnm": "알루코",
      "stck_prpr": "3580",
      "prdy_vrss": "-30",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-0.83",
      "ovtm_total_askp_rsqn": "0",
      "ovtm_total_bidp_rsqn": "0",
      "mkob_otcp_vol": "36447",
      "mkfa_otcp_vol": "0"
    },
    {
      "stck_shrn_iscd": "043100",
      "data_rank": "7",
      "hts_kor_isnm": "솔고바이오",
      "stck_prpr": "524",
      "prdy_vrss": "-9",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-1.69",
      "ovtm_total_askp_rsqn": "0",
      "ovtm_total_bidp_rsqn": "0",
      "mkob_otcp_vol": "33361",
      "mkfa_otcp_vol": "0"
    },
    {
      "stck_shrn_iscd": "109610",
      "data_rank": "8",
      "hts_kor_isnm": "에스와이",
      "stck_prpr": "4700",
      "prdy_vrss": "-145",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-2.99",
      "ovtm_total_askp_rsqn": "0",
      "ovtm_total_bidp_rsqn": "0",
      "mkob_otcp_vol": "32283",
      "mkfa_otcp_vol": "0"
    },
    {
      "stck_shrn_iscd": "012170",
      "data_rank": "9",
      "hts_kor_isnm": "아센디오",
      "stck_prpr": "1071",
      "prdy_vrss": "5",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "0.47",
      "ovtm_total_askp_rsqn": "0",
      "ovtm_total_bidp_rsqn": "0",
      "mkob_otcp_vol": "27599",
      "mkfa_otcp_vol": "0"
    },
    {
      "stck_shrn_iscd": "033170",
      "data_rank": "10",
      "hts_kor_isnm": "시그네틱스",
      "stck_prpr": "1998",
      "prdy_vrss": "123",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "6.56",
      "ovtm_total_askp_rsqn": "0",
      "ovtm_total_bidp_rsqn": "0",
      "mkob_otcp_vol": "22443",
      "mkfa_otcp_vol": "0"
    },
    {
      "stck_shrn_iscd": "114800",
      "data_rank": "11",
      "hts_kor_isnm": "KODEX 인버스",
      "stck_prpr": "4265",
      "prdy_vrss": "-10",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-0.23",
      "ovtm_total_askp_rsqn": "0",
      "ovtm_total_bidp_rsqn": "0",
      "mkob_otcp_vol": "21052",
      "mkfa_otcp_vol": "0"
    },
    {
      "stck_shrn_iscd": "032800",
      "data_rank": "12",
      "hts_kor_isnm": "판타지오",
      "stck_prpr": "398",
      "prdy_vrss": "67",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "20.24",
      "ovtm_total_askp_rsqn": "0",
      "ovtm_total_bidp_rsqn": "0",
      "mkob_otcp_vol": "16326",
      "mkfa_otcp_vol": "0"
    },
    {
      "stck_shrn_iscd": "317850",
      "data_rank": "13",
      "hts_kor_isnm": "대모",
      "stck_prpr": "9430",
      "prdy_vrss": "-230",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-2.38",
      "ovtm_total_askp_rsqn": "0",
      "ovtm_total_bidp_rsqn": "0",
      "mkob_otcp_vol": "15514",
      "mkfa_otcp_vol": "0"
    },
    {
      "stck_shrn_iscd": "357250",
      "data_rank": "14",
      "hts_kor_isnm": "미래에셋맵스리츠",
      "stck_prpr": "3260",
      "prdy_vrss": "-20",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-0.61",
      "ovtm_total_askp_rsqn": "0",
      "ovtm_total_bidp_rsqn": "0",
      "mkob_otcp_vol": "12500",
      "mkfa_otcp_vol": "0"
    },
    {
      "stck_shrn_iscd": "066790",
      "data_rank": "15",
      "hts_kor_isnm": "씨씨에스",
      "stck_prpr": "5450",
      "prdy_vrss": "0",
      "prdy_vrss_sign": "3",
      "prdy_ctrt": "0.00",
      "ovtm_total_askp_rsqn": "0",
      "ovtm_total_bidp_rsqn": "0",
      "mkob_otcp_vol": "10989",
      "mkfa_otcp_vol": "0"
    },
    {
      "stck_shrn_iscd": "039980",
      "data_rank": "16",
      "hts_kor_isnm": "폴라리스AI",
      "stck_prpr": "2690",
      "prdy_vrss": "-55",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-2.00",
      "ovtm_total_askp_rsqn": "0",
      "ovtm_total_bidp_rsqn": "0",
      "mkob_otcp_vol": "10086",
      "mkfa_otcp_vol": "0"
    },
    {
      "stck_shrn_iscd": "162300",
      "data_rank": "17",
      "hts_kor_isnm": "신스틸",
      "stck_prpr": "3795",
      "prdy_vrss": "-70",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-1.81",
      "ovtm_total_askp_rsqn": "0",
      "ovtm_total_bidp_rsqn": "0",
      "mkob_otcp_vol": "9970",
      "mkfa_otcp_vol": "0"
    },
    {
      "stck_shrn_iscd": "007460",
      "data_rank": "18",
      "hts_kor_isnm": "에이프로젠",
      "stck_prpr": "1079",
      "prdy_vrss": "7",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "0.65",
      "ovtm_total_askp_rsqn": "0",
      "ovtm_total_bidp_rsqn": "0",
      "mkob_otcp_vol": "9859",
      "mkfa_otcp_vol": "0"
    },
    {
      "stck_shrn_iscd": "033230",
      "data_rank": "19",
      "hts_kor_isnm": "인성정보",
      "stck_prpr": "4465",
      "prdy_vrss": "15",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "0.34",
      "ovtm_total_askp_rsqn": "0",
      "ovtm_total_bidp_rsqn": "0",
      "mkob_otcp_vol": "9773",
      "mkfa_otcp_vol": "0"
    },
    {
      "stck_shrn_iscd": "251340",
      "data_rank": "20",
      "hts_kor_isnm": "KODEX 코스닥150선물인버스",
      "stck_prpr": "3315",
      "prdy_vrss": "-65",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-1.92",
      "ovtm_total_askp_rsqn": "0",
      "ovtm_total_bidp_rsqn": "0",
      "mkob_otcp_vol": "9049",
      "mkfa_otcp_vol": "0"
    },
    {
      "stck_shrn_iscd": "232140",
      "data_rank": "21",
      "hts_kor_isnm": "와이아이케이",
      "stck_prpr": "7300",
      "prdy_vrss": "80",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "1.11",
      "ovtm_total_askp_rsqn": "0",
      "ovtm_total_bidp_rsqn": "0",
      "mkob_otcp_vol": "8832",
      "mkfa_otcp_vol": "0"
    },
    {
      "stck_shrn_iscd": "219550",
      "data_rank": "22",
      "hts_kor_isnm": "디와이디",
      "stck_prpr": "1014",
      "prdy_vrss": "-19",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-1.84",
      "ovtm_total_askp_rsqn": "0",
      "ovtm_total_bidp_rsqn": "0",
      "mkob_otcp_vol": "8557",
      "mkfa_otcp_vol": "0"
    },
    {
      "stck_shrn_iscd": "032680",
      "data_rank": "23",
      "hts_kor_isnm": "소프트센",
      "stck_prpr": "732",
      "prdy_vrss": "-5",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-0.68",
      "ovtm_total_askp_rsqn": "0",
      "ovtm_total_bidp_rsqn": "0",
      "mkob_otcp_vol": "8371",
      "mkfa_otcp_vol": "0"
    },
    {
      "stck_shrn_iscd": "256840",
      "data_rank": "24",
      "hts_kor_isnm": "한국비엔씨",
      "stck_prpr": "7240",
      "prdy_vrss": "90",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "1.26",
      "ovtm_total_askp_rsqn": "0",
      "ovtm_total_bidp_rsqn": "0",
      "mkob_otcp_vol": "7590",
      "mkfa_otcp_vol": "0"
    },
    {
      "stck_shrn_iscd": "112040",
      "data_rank": "25",
      "hts_kor_isnm": "위메이드",
      "stck_prpr": "60800",
      "prdy_vrss": "4600",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "8.19",
      "ovtm_total_askp_rsqn": "0",
      "ovtm_total_bidp_rsqn": "0",
      "mkob_otcp_vol": "7258",
      "mkfa_otcp_vol": "0"
    },
    {
      "stck_shrn_iscd": "357430",
      "data_rank": "26",
      "hts_kor_isnm": "마스턴프리미어리츠",
      "stck_prpr": "3045",
      "prdy_vrss": "-10",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-0.33",
      "ovtm_total_askp_rsqn": "0",
      "ovtm_total_bidp_rsqn": "0",
      "mkob_otcp_vol": "6870",
      "mkfa_otcp_vol": "0"
    },
    {
      "stck_shrn_iscd": "264850",
      "data_rank": "27",
      "hts_kor_isnm": "이랜시스",
      "stck_prpr": "7650",
      "prdy_vrss": "-10",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-0.13",
      "ovtm_total_askp_rsqn": "0",
      "ovtm_total_bidp_rsqn": "0",
      "mkob_otcp_vol": "6177",
      "mkfa_otcp_vol": "0"
    },
    {
      "stck_shrn_iscd": "113810",
      "data_rank": "28",
      "hts_kor_isnm": "디젠스",
      "stck_prpr": "1033",
      "prdy_vrss": "3",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "0.29",
      "ovtm_total_askp_rsqn": "0",
      "ovtm_total_bidp_rsqn": "0",
      "mkob_otcp_vol": "5874",
      "mkfa_otcp_vol": "0"
    },
    {
      "stck_shrn_iscd": "001440",
      "data_rank": "29",
      "hts_kor_isnm": "대한전선",
      "stck_prpr": "11080",
      "prdy_vrss": "980",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "9.70",
      "ovtm_total_askp_rsqn": "0",
      "ovtm_total_bidp_rsqn": "0",
      "mkob_otcp_vol": "5792",
      "mkfa_otcp_vol": "0"
    },
    {
      "stck_shrn_iscd": "418620",
      "data_rank": "30",
      "hts_kor_isnm": "이에이트",
      "stck_prpr": "23000",
      "prdy_vrss": "0",
      "prdy_vrss_sign": "3",
      "prdy_ctrt": "0.00",
      "ovtm_total_askp_rsqn": "0",
      "ovtm_total_bidp_rsqn": "0",
      "mkob_otcp_vol": "5486",
      "mkfa_otcp_vol": "0"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```

