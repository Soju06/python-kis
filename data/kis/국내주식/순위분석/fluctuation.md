# 국내주식 등락률 순위[v1_국내주식-088]

> [국내주식] 순위분석

국내주식 등락률 순위 API입니다. 
한국투자 HTS(eFriend Plus) > [0170] 등락률 순위 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.
최대 30건 확인 가능하며, 다음 조회가 불가합니다.

※ 30건 이상의 목록 조회가 필요한 경우, 대안으로 종목조건검색 API를 이용해서 원하는 종목 100개까지 검색할 수 있는 기능을 제공하고 있습니다.
종목조건검색 API는 HTS(efriend Plus) [0110] 조건검색에서 등록 및 서버저장한 나의 조건 목록을 확인할 수 있는 API로,
자세한 사용 방법은 공지사항 - [조건검색 필독] 조건검색 API 이용안내 참고 부탁드립니다.


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `c3b78a4a-de38-43fb-a78d-4018b1ea4d4f` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/ranking/fluctuation` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `FHPST01700000` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-03-15T09:16:35+09:00
- **최종 수정일**: 2025-06-24T14:08:15+09:00

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials Grant 절차를 준용)  법인(Access token 유효기간 3개월, Refresh token 유효기간 1년, OAuth 2.0의 Authorization Code Grant 절차를 준용) |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | FHPST01700000 |
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
| `fid_rsfl_rate2` | 등락 비율2 | String | 132 | Y | 공백 입력 시 전체 (~ 비율 |
| `fid_cond_mrkt_div_code` | 조건 시장 분류 코드 | String | 2 | Y | 시장구분코드 (J:KRX, NX:NXT) |
| `fid_cond_scr_div_code` | 조건 화면 분류 코드 | String | 5 | Y | Unique key( 20170 ) |
| `fid_input_iscd` | 입력 종목코드 | String | 12 | Y | 0000(전체) 코스피(0001), 코스닥(1001), 코스피200(2001) |
| `fid_rank_sort_cls_code` | 순위 정렬 구분 코드 | String | 2 | Y | 0:상승율순 1:하락율순 2:시가대비상승율 3:시가대비하락율 4:변동율 |
| `fid_input_cnt_1` | 입력 수1 | String | 12 | Y | 0:전체 , 누적일수 입력 |
| `fid_prc_cls_code` | 가격 구분 코드 | String | 2 | Y | 'fid_rank_sort_cls_code :0 상승율 순일때 (0:저가대비, 1:종가대비) fid_rank_sort_cls_code :1 하락율 순일때 (0:고가대비, 1:종가대비) fid_rank_sort_cls_code : 기타 (0:전체)' |
| `fid_input_price_1` | 입력 가격1 | String | 12 | Y | 공백 입력 시 전체 (가격 ~) |
| `fid_input_price_2` | 입력 가격2 | String | 12 | Y | 공백 입력 시 전체 (~ 가격) |
| `fid_vol_cnt` | 거래량 수 | String | 12 | Y | 공백 입력 시 전체 (거래량 ~) |
| `fid_trgt_cls_code` | 대상 구분 코드 | String | 32 | Y | 0:전체 |
| `fid_trgt_exls_cls_code` | 대상 제외 구분 코드 | String | 32 | Y | 0:전체 |
| `fid_div_cls_code` | 분류 구분 코드 | String | 2 | Y | 0:전체 |
| `fid_rsfl_rate1` | 등락 비율1 | String | 132 | Y | 공백 입력 시 전체 (비율 ~) |

### 요청 예시

```json
{
  "fid_cond_mrkt_div_code": "J",
  "fid_cond_scr_div_code": "20170",
  "fid_input_iscd": "0000",
  "fid_rank_sort_cls_code": "0",
  "fid_input_cnt_1": "0",
  "fid_prc_cls_code": "0",
  "fid_input_price_1": "",
  "fid_input_price_2": "",
  "fid_vol_cnt": "",
  "fid_trgt_cls_code": "0",
  "fid_trgt_exls_cls_code": "0",
  "fid_div_cls_code": "0",
  "fid_rsfl_rate1": "",
  "fid_rsfl_rate2": ""
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
| `stck_hgpr` | 주식 최고가 | String | 10 | Y |  |
| `hgpr_hour` | 최고가 시간 | String | 6 | Y |  |
| `acml_hgpr_date` | 누적 최고가 일자 | String | 8 | Y |  |
| `stck_lwpr` | 주식 최저가 | String | 10 | Y |  |
| `lwpr_hour` | 최저가 시간 | String | 6 | Y |  |
| `acml_lwpr_date` | 누적 최저가 일자 | String | 8 | Y |  |
| `lwpr_vrss_prpr_rate` | 최저가 대비 현재가 비율 | String | 84 | Y |  |
| `dsgt_date_clpr_vrss_prpr_rate` | 지정 일자 종가 대비 현재가 비 | String | 84 | Y |  |
| `cnnt_ascn_dynu` | 연속 상승 일수 | String | 5 | Y |  |
| `hgpr_vrss_prpr_rate` | 최고가 대비 현재가 비율 | String | 84 | Y |  |
| `cnnt_down_dynu` | 연속 하락 일수 | String | 5 | Y |  |
| `oprc_vrss_prpr_sign` | 시가2 대비 현재가 부호 | String | 1 | Y |  |
| `oprc_vrss_prpr` | 시가2 대비 현재가 | String | 10 | Y |  |
| `oprc_vrss_prpr_rate` | 시가2 대비 현재가 비율 | String | 84 | Y |  |
| `prd_rsfl` | 기간 등락 | String | 10 | Y |  |
| `prd_rsfl_rate` | 기간 등락 비율 | String | 84 | Y |  |

### 응답 예시

```json
{
  "output": [
    {
      "stck_shrn_iscd": "000040",
      "data_rank": "1",
      "hts_kor_isnm": "KR모터스",
      "stck_prpr": "1821",
      "prdy_vrss": "197",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "12.13",
      "acml_vol": "2267183",
      "stck_hgpr": "1861",
      "hgpr_hour": "100214",
      "acml_hgpr_date": "20240318",
      "stck_lwpr": "1301",
      "lwpr_hour": "090239",
      "acml_lwpr_date": "20240318",
      "lwpr_vrss_prpr_rate": "39.97",
      "dsgt_date_clpr_vrss_prpr_rate": "12.13",
      "cnnt_ascn_dynu": "1",
      "hgpr_vrss_prpr_rate": "-2.15",
      "cnnt_down_dynu": "0",
      "oprc_vrss_prpr_sign": "2",
      "oprc_vrss_prpr": "0",
      "oprc_vrss_prpr_rate": "0.00",
      "prd_rsfl": "0",
      "prd_rsfl_rate": "0.00"
    },
    {
      "stck_shrn_iscd": "032800",
      "data_rank": "2",
      "hts_kor_isnm": "판타지오",
      "stck_prpr": "406",
      "prdy_vrss": "75",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "22.66",
      "acml_vol": "36313396",
      "stck_hgpr": "419",
      "hgpr_hour": "095020",
      "acml_hgpr_date": "20240318",
      "stck_lwpr": "332",
      "lwpr_hour": "090015",
      "acml_lwpr_date": "20240318",
      "lwpr_vrss_prpr_rate": "22.29",
      "dsgt_date_clpr_vrss_prpr_rate": "22.66",
      "cnnt_ascn_dynu": "1",
      "hgpr_vrss_prpr_rate": "-3.10",
      "cnnt_down_dynu": "1",
      "oprc_vrss_prpr_sign": "2",
      "oprc_vrss_prpr": "0",
      "oprc_vrss_prpr_rate": "0.00",
      "prd_rsfl": "0",
      "prd_rsfl_rate": "0.00"
    },
    {
      "stck_shrn_iscd": "018000",
      "data_rank": "3",
      "hts_kor_isnm": "유니슨",
      "stck_prpr": "1233",
      "prdy_vrss": "215",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "21.12",
      "acml_vol": "2436474",
      "stck_hgpr": "1233",
      "hgpr_hour": "100301",
      "acml_hgpr_date": "20240318",
      "stck_lwpr": "1014",
      "lwpr_hour": "090026",
      "acml_lwpr_date": "20240318",
      "lwpr_vrss_prpr_rate": "21.60",
      "dsgt_date_clpr_vrss_prpr_rate": "21.12",
      "cnnt_ascn_dynu": "1",
      "hgpr_vrss_prpr_rate": "0.00",
      "cnnt_down_dynu": "1",
      "oprc_vrss_prpr_sign": "2",
      "oprc_vrss_prpr": "0",
      "oprc_vrss_prpr_rate": "0.00",
      "prd_rsfl": "0",
      "prd_rsfl_rate": "0.00"
    },
    {
      "stck_shrn_iscd": "083790",
      "data_rank": "4",
      "hts_kor_isnm": "CG인바이츠",
      "stck_prpr": "4025",
      "prdy_vrss": "645",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "19.08",
      "acml_vol": "1666447",
      "stck_hgpr": "4075",
      "hgpr_hour": "092027",
      "acml_hgpr_date": "20240318",
      "stck_lwpr": "3460",
      "lwpr_hour": "090005",
      "acml_lwpr_date": "20240318",
      "lwpr_vrss_prpr_rate": "16.33",
      "dsgt_date_clpr_vrss_prpr_rate": "19.08",
      "cnnt_ascn_dynu": "2",
      "hgpr_vrss_prpr_rate": "-1.23",
      "cnnt_down_dynu": "0",
      "oprc_vrss_prpr_sign": "2",
      "oprc_vrss_prpr": "0",
      "oprc_vrss_prpr_rate": "0.00",
      "prd_rsfl": "0",
      "prd_rsfl_rate": "0.00"
    },
    {
      "stck_shrn_iscd": "237690",
      "data_rank": "5",
      "hts_kor_isnm": "에스티팜",
      "stck_prpr": "93400",
      "prdy_vrss": "15800",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "20.36",
      "acml_vol": "1368523",
      "stck_hgpr": "95000",
      "hgpr_hour": "092731",
      "acml_hgpr_date": "20240318",
      "stck_lwpr": "80400",
      "lwpr_hour": "090025",
      "acml_lwpr_date": "20240318",
      "lwpr_vrss_prpr_rate": "16.17",
      "dsgt_date_clpr_vrss_prpr_rate": "20.36",
      "cnnt_ascn_dynu": "3",
      "hgpr_vrss_prpr_rate": "-1.68",
      "cnnt_down_dynu": "0",
      "oprc_vrss_prpr_sign": "2",
      "oprc_vrss_prpr": "0",
      "oprc_vrss_prpr_rate": "0.00",
      "prd_rsfl": "0",
      "prd_rsfl_rate": "0.00"
    },
    {
      "stck_shrn_iscd": "065150",
      "data_rank": "6",
      "hts_kor_isnm": "대산F&B",
      "stck_prpr": "239",
      "prdy_vrss": "33",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "16.02",
      "acml_vol": "5046848",
      "stck_hgpr": "267",
      "hgpr_hour": "094747",
      "acml_hgpr_date": "20240318",
      "stck_lwpr": "206",
      "lwpr_hour": "090024",
      "acml_lwpr_date": "20240318",
      "lwpr_vrss_prpr_rate": "16.02",
      "dsgt_date_clpr_vrss_prpr_rate": "16.02",
      "cnnt_ascn_dynu": "3",
      "hgpr_vrss_prpr_rate": "-10.49",
      "cnnt_down_dynu": "0",
      "oprc_vrss_prpr_sign": "2",
      "oprc_vrss_prpr": "0",
      "oprc_vrss_prpr_rate": "0.00",
      "prd_rsfl": "0",
      "prd_rsfl_rate": "0.00"
    },
    {
      "stck_shrn_iscd": "008600",
      "data_rank": "7",
      "hts_kor_isnm": "윌비스",
      "stck_prpr": "596",
      "prdy_vrss": "66",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "12.45",
      "acml_vol": "3819993",
      "stck_hgpr": "620",
      "hgpr_hour": "094852",
      "acml_hgpr_date": "20240318",
      "stck_lwpr": "516",
      "lwpr_hour": "090106",
      "acml_lwpr_date": "20240318",
      "lwpr_vrss_prpr_rate": "15.50",
      "dsgt_date_clpr_vrss_prpr_rate": "12.45",
      "cnnt_ascn_dynu": "3",
      "hgpr_vrss_prpr_rate": "-3.87",
      "cnnt_down_dynu": "0",
      "oprc_vrss_prpr_sign": "2",
      "oprc_vrss_prpr": "0",
      "oprc_vrss_prpr_rate": "0.00",
      "prd_rsfl": "0",
      "prd_rsfl_rate": "0.00"
    },
    {
      "stck_shrn_iscd": "219130",
      "data_rank": "8",
      "hts_kor_isnm": "타이거일렉",
      "stck_prpr": "37700",
      "prdy_vrss": "4700",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "14.24",
      "acml_vol": "188206",
      "stck_hgpr": "38350",
      "hgpr_hour": "095838",
      "acml_hgpr_date": "20240318",
      "stck_lwpr": "32650",
      "lwpr_hour": "090031",
      "acml_lwpr_date": "20240318",
      "lwpr_vrss_prpr_rate": "15.47",
      "dsgt_date_clpr_vrss_prpr_rate": "14.24",
      "cnnt_ascn_dynu": "1",
      "hgpr_vrss_prpr_rate": "-1.69",
      "cnnt_down_dynu": "0",
      "oprc_vrss_prpr_sign": "2",
      "oprc_vrss_prpr": "0",
      "oprc_vrss_prpr_rate": "0.00",
      "prd_rsfl": "0",
      "prd_rsfl_rate": "0.00"
    },
    {
      "stck_shrn_iscd": "004380",
      "data_rank": "9",
      "hts_kor_isnm": "삼익THK",
      "stck_prpr": "17290",
      "prdy_vrss": "2100",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "13.82",
      "acml_vol": "2290984",
      "stck_hgpr": "17720",
      "hgpr_hour": "095642",
      "acml_hgpr_date": "20240318",
      "stck_lwpr": "15050",
      "lwpr_hour": "090319",
      "acml_lwpr_date": "20240318",
      "lwpr_vrss_prpr_rate": "14.88",
      "dsgt_date_clpr_vrss_prpr_rate": "13.82",
      "cnnt_ascn_dynu": "5",
      "hgpr_vrss_prpr_rate": "-2.43",
      "cnnt_down_dynu": "0",
      "oprc_vrss_prpr_sign": "2",
      "oprc_vrss_prpr": "0",
      "oprc_vrss_prpr_rate": "0.00",
      "prd_rsfl": "0",
      "prd_rsfl_rate": "0.00"
    },
    {
      "stck_shrn_iscd": "321370",
      "data_rank": "10",
      "hts_kor_isnm": "센서뷰",
      "stck_prpr": "5020",
      "prdy_vrss": "920",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "22.44",
      "acml_vol": "4923442",
      "stck_hgpr": "5300",
      "hgpr_hour": "092639",
      "acml_hgpr_date": "20240318",
      "stck_lwpr": "4400",
      "lwpr_hour": "090004",
      "acml_lwpr_date": "20240318",
      "lwpr_vrss_prpr_rate": "14.09",
      "dsgt_date_clpr_vrss_prpr_rate": "22.44",
      "cnnt_ascn_dynu": "1",
      "hgpr_vrss_prpr_rate": "-5.28",
      "cnnt_down_dynu": "1",
      "oprc_vrss_prpr_sign": "2",
      "oprc_vrss_prpr": "0",
      "oprc_vrss_prpr_rate": "0.00",
      "prd_rsfl": "0",
      "prd_rsfl_rate": "0.00"
    },
    {
      "stck_shrn_iscd": "010660",
      "data_rank": "11",
      "hts_kor_isnm": "화천기계",
      "stck_prpr": "7470",
      "prdy_vrss": "1210",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "19.33",
      "acml_vol": "9426161",
      "stck_hgpr": "7740",
      "hgpr_hour": "091704",
      "acml_hgpr_date": "20240318",
      "stck_lwpr": "6610",
      "lwpr_hour": "090030",
      "acml_lwpr_date": "20240318",
      "lwpr_vrss_prpr_rate": "13.01",
      "dsgt_date_clpr_vrss_prpr_rate": "19.33",
      "cnnt_ascn_dynu": "2",
      "hgpr_vrss_prpr_rate": "-3.49",
      "cnnt_down_dynu": "0",
      "oprc_vrss_prpr_sign": "2",
      "oprc_vrss_prpr": "0",
      "oprc_vrss_prpr_rate": "0.00",
      "prd_rsfl": "0",
      "prd_rsfl_rate": "0.00"
    },
    {
      "stck_shrn_iscd": "062970",
      "data_rank": "12",
      "hts_kor_isnm": "피피아이",
      "stck_prpr": "1989",
      "prdy_vrss": "232",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "13.20",
      "acml_vol": "2246815",
      "stck_hgpr": "2150",
      "hgpr_hour": "093356",
      "acml_hgpr_date": "20240318",
      "stck_lwpr": "1776",
      "lwpr_hour": "090028",
      "acml_lwpr_date": "20240318",
      "lwpr_vrss_prpr_rate": "11.99",
      "dsgt_date_clpr_vrss_prpr_rate": "13.20",
      "cnnt_ascn_dynu": "1",
      "hgpr_vrss_prpr_rate": "-7.49",
      "cnnt_down_dynu": "1",
      "oprc_vrss_prpr_sign": "2",
      "oprc_vrss_prpr": "0",
      "oprc_vrss_prpr_rate": "0.00",
      "prd_rsfl": "0",
      "prd_rsfl_rate": "0.00"
    },
    {
      "stck_shrn_iscd": "060230",
      "data_rank": "13",
      "hts_kor_isnm": "소니드",
      "stck_prpr": "2440",
      "prdy_vrss": "345",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "16.47",
      "acml_vol": "1266350",
      "stck_hgpr": "2500",
      "hgpr_hour": "090948",
      "acml_hgpr_date": "20240318",
      "stck_lwpr": "2180",
      "lwpr_hour": "090032",
      "acml_lwpr_date": "20240318",
      "lwpr_vrss_prpr_rate": "11.93",
      "dsgt_date_clpr_vrss_prpr_rate": "16.47",
      "cnnt_ascn_dynu": "1",
      "hgpr_vrss_prpr_rate": "-2.40",
      "cnnt_down_dynu": "0",
      "oprc_vrss_prpr_sign": "2",
      "oprc_vrss_prpr": "0",
      "oprc_vrss_prpr_rate": "0.00",
      "prd_rsfl": "0",
      "prd_rsfl_rate": "0.00"
    },
    {
      "stck_shrn_iscd": "073570",
      "data_rank": "14",
      "hts_kor_isnm": "리튬포어스",
      "stck_prpr": "6240",
      "prdy_vrss": "840",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "15.56",
      "acml_vol": "2650262",
      "stck_hgpr": "6390",
      "hgpr_hour": "094423",
      "acml_hgpr_date": "20240318",
      "stck_lwpr": "5580",
      "lwpr_hour": "090050",
      "acml_lwpr_date": "20240318",
      "lwpr_vrss_prpr_rate": "11.83",
      "dsgt_date_clpr_vrss_prpr_rate": "15.56",
      "cnnt_ascn_dynu": "1",
      "hgpr_vrss_prpr_rate": "-2.35",
      "cnnt_down_dynu": "3",
      "oprc_vrss_prpr_sign": "2",
      "oprc_vrss_prpr": "0",
      "oprc_vrss_prpr_rate": "0.00",
      "prd_rsfl": "0",
      "prd_rsfl_rate": "0.00"
    },
    {
      "stck_shrn_iscd": "066910",
      "data_rank": "15",
      "hts_kor_isnm": "손오공",
      "stck_prpr": "3745",
      "prdy_vrss": "415",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "12.46",
      "acml_vol": "1612034",
      "stck_hgpr": "3850",
      "hgpr_hour": "094324",
      "acml_hgpr_date": "20240318",
      "stck_lwpr": "3355",
      "lwpr_hour": "090035",
      "acml_lwpr_date": "20240318",
      "lwpr_vrss_prpr_rate": "11.62",
      "dsgt_date_clpr_vrss_prpr_rate": "12.46",
      "cnnt_ascn_dynu": "5",
      "hgpr_vrss_prpr_rate": "-2.73",
      "cnnt_down_dynu": "0",
      "oprc_vrss_prpr_sign": "2",
      "oprc_vrss_prpr": "0",
      "oprc_vrss_prpr_rate": "0.00",
      "prd_rsfl": "0",
      "prd_rsfl_rate": "0.00"
    },
    {
      "stck_shrn_iscd": "217620",
      "data_rank": "16",
      "hts_kor_isnm": "디딤이앤에프",
      "stck_prpr": "415",
      "prdy_vrss": "-26",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-5.90",
      "acml_vol": "3239066",
      "stck_hgpr": "419",
      "hgpr_hour": "093956",
      "acml_hgpr_date": "20240318",
      "stck_lwpr": "372",
      "lwpr_hour": "091151",
      "acml_lwpr_date": "20240318",
      "lwpr_vrss_prpr_rate": "11.56",
      "dsgt_date_clpr_vrss_prpr_rate": "-5.90",
      "cnnt_ascn_dynu": "0",
      "hgpr_vrss_prpr_rate": "-0.95",
      "cnnt_down_dynu": "3",
      "oprc_vrss_prpr_sign": "2",
      "oprc_vrss_prpr": "0",
      "oprc_vrss_prpr_rate": "0.00",
      "prd_rsfl": "0",
      "prd_rsfl_rate": "0.00"
    },
    {
      "stck_shrn_iscd": "103590",
      "data_rank": "17",
      "hts_kor_isnm": "일진전기",
      "stck_prpr": "17340",
      "prdy_vrss": "2660",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "18.12",
      "acml_vol": "9389511",
      "stck_hgpr": "18500",
      "hgpr_hour": "092900",
      "acml_hgpr_date": "20240318",
      "stck_lwpr": "15570",
      "lwpr_hour": "090345",
      "acml_lwpr_date": "20240318",
      "lwpr_vrss_prpr_rate": "11.37",
      "dsgt_date_clpr_vrss_prpr_rate": "18.12",
      "cnnt_ascn_dynu": "4",
      "hgpr_vrss_prpr_rate": "-6.27",
      "cnnt_down_dynu": "0",
      "oprc_vrss_prpr_sign": "2",
      "oprc_vrss_prpr": "0",
      "oprc_vrss_prpr_rate": "0.00",
      "prd_rsfl": "0",
      "prd_rsfl_rate": "0.00"
    },
    {
      "stck_shrn_iscd": "224060",
      "data_rank": "18",
      "hts_kor_isnm": "더코디",
      "stck_prpr": "6230",
      "prdy_vrss": "760",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "13.89",
      "acml_vol": "646297",
      "stck_hgpr": "7110",
      "hgpr_hour": "091332",
      "acml_hgpr_date": "20240318",
      "stck_lwpr": "5600",
      "lwpr_hour": "090030",
      "acml_lwpr_date": "20240318",
      "lwpr_vrss_prpr_rate": "11.25",
      "dsgt_date_clpr_vrss_prpr_rate": "13.89",
      "cnnt_ascn_dynu": "2",
      "hgpr_vrss_prpr_rate": "-12.38",
      "cnnt_down_dynu": "0",
      "oprc_vrss_prpr_sign": "2",
      "oprc_vrss_prpr": "0",
      "oprc_vrss_prpr_rate": "0.00",
      "prd_rsfl": "0",
      "prd_rsfl_rate": "0.00"
    },
    {
      "stck_shrn_iscd": "064800",
      "data_rank": "19",
      "hts_kor_isnm": "젬백스링크",
      "stck_prpr": "3275",
      "prdy_vrss": "195",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "6.33",
      "acml_vol": "723313",
      "stck_hgpr": "3310",
      "hgpr_hour": "100240",
      "acml_hgpr_date": "20240318",
      "stck_lwpr": "2945",
      "lwpr_hour": "090021",
      "acml_lwpr_date": "20240318",
      "lwpr_vrss_prpr_rate": "11.21",
      "dsgt_date_clpr_vrss_prpr_rate": "6.33",
      "cnnt_ascn_dynu": "2",
      "hgpr_vrss_prpr_rate": "-1.06",
      "cnnt_down_dynu": "0",
      "oprc_vrss_prpr_sign": "2",
      "oprc_vrss_prpr": "0",
      "oprc_vrss_prpr_rate": "0.00",
      "prd_rsfl": "0",
      "prd_rsfl_rate": "0.00"
    },
    {
      "stck_shrn_iscd": "383310",
      "data_rank": "20",
      "hts_kor_isnm": "에코프로에이치엔",
      "stck_prpr": "80400",
      "prdy_vrss": "8700",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "12.13",
      "acml_vol": "629737",
      "stck_hgpr": "82900",
      "hgpr_hour": "094050",
      "acml_hgpr_date": "20240318",
      "stck_lwpr": "72300",
      "lwpr_hour": "090018",
      "acml_lwpr_date": "20240318",
      "lwpr_vrss_prpr_rate": "11.20",
      "dsgt_date_clpr_vrss_prpr_rate": "12.13",
      "cnnt_ascn_dynu": "1",
      "hgpr_vrss_prpr_rate": "-3.02",
      "cnnt_down_dynu": "2",
      "oprc_vrss_prpr_sign": "2",
      "oprc_vrss_prpr": "0",
      "oprc_vrss_prpr_rate": "0.00",
      "prd_rsfl": "0",
      "prd_rsfl_rate": "0.00"
    },
    {
      "stck_shrn_iscd": "101390",
      "data_rank": "21",
      "hts_kor_isnm": "아이엠",
      "stck_prpr": "8570",
      "prdy_vrss": "-480",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-5.30",
      "acml_vol": "389587",
      "stck_hgpr": "9500",
      "hgpr_hour": "090436",
      "acml_hgpr_date": "20240318",
      "stck_lwpr": "7710",
      "lwpr_hour": "094503",
      "acml_lwpr_date": "20240318",
      "lwpr_vrss_prpr_rate": "11.15",
      "dsgt_date_clpr_vrss_prpr_rate": "-5.30",
      "cnnt_ascn_dynu": "3",
      "hgpr_vrss_prpr_rate": "-9.79",
      "cnnt_down_dynu": "1",
      "oprc_vrss_prpr_sign": "2",
      "oprc_vrss_prpr": "0",
      "oprc_vrss_prpr_rate": "0.00",
      "prd_rsfl": "0",
      "prd_rsfl_rate": "0.00"
    },
    {
      "stck_shrn_iscd": "196170",
      "data_rank": "22",
      "hts_kor_isnm": "알테오젠",
      "stck_prpr": "221000",
      "prdy_vrss": "16500",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "8.07",
      "acml_vol": "1045024",
      "stck_hgpr": "224000",
      "hgpr_hour": "093639",
      "acml_hgpr_date": "20240318",
      "stck_lwpr": "199500",
      "lwpr_hour": "090416",
      "acml_lwpr_date": "20240318",
      "lwpr_vrss_prpr_rate": "10.78",
      "dsgt_date_clpr_vrss_prpr_rate": "8.07",
      "cnnt_ascn_dynu": "1",
      "hgpr_vrss_prpr_rate": "-1.34",
      "cnnt_down_dynu": "1",
      "oprc_vrss_prpr_sign": "2",
      "oprc_vrss_prpr": "0",
      "oprc_vrss_prpr_rate": "0.00",
      "prd_rsfl": "0",
      "prd_rsfl_rate": "0.00"
    },
    {
      "stck_shrn_iscd": "388790",
      "data_rank": "23",
      "hts_kor_isnm": "라이콤",
      "stck_prpr": "2105",
      "prdy_vrss": "200",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "10.50",
      "acml_vol": "770420",
      "stck_hgpr": "2175",
      "hgpr_hour": "092044",
      "acml_hgpr_date": "20240318",
      "stck_lwpr": "1908",
      "lwpr_hour": "090040",
      "acml_lwpr_date": "20240318",
      "lwpr_vrss_prpr_rate": "10.32",
      "dsgt_date_clpr_vrss_prpr_rate": "10.50",
      "cnnt_ascn_dynu": "2",
      "hgpr_vrss_prpr_rate": "-3.22",
      "cnnt_down_dynu": "0",
      "oprc_vrss_prpr_sign": "2",
      "oprc_vrss_prpr": "0",
      "oprc_vrss_prpr_rate": "0.00",
      "prd_rsfl": "0",
      "prd_rsfl_rate": "0.00"
    },
    {
      "stck_shrn_iscd": "452300",
      "data_rank": "24",
      "hts_kor_isnm": "캡스톤파트너스",
      "stck_prpr": "4805",
      "prdy_vrss": "435",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "9.95",
      "acml_vol": "804742",
      "stck_hgpr": "4990",
      "hgpr_hour": "094904",
      "acml_hgpr_date": "20240318",
      "stck_lwpr": "4360",
      "lwpr_hour": "090206",
      "acml_lwpr_date": "20240318",
      "lwpr_vrss_prpr_rate": "10.21",
      "dsgt_date_clpr_vrss_prpr_rate": "9.95",
      "cnnt_ascn_dynu": "1",
      "hgpr_vrss_prpr_rate": "-3.71",
      "cnnt_down_dynu": "2",
      "oprc_vrss_prpr_sign": "2",
      "oprc_vrss_prpr": "0",
      "oprc_vrss_prpr_rate": "0.00",
      "prd_rsfl": "0",
      "prd_rsfl_rate": "0.00"
    },
    {
      "stck_shrn_iscd": "214430",
      "data_rank": "25",
      "hts_kor_isnm": "아이쓰리시스템",
      "stck_prpr": "36900",
      "prdy_vrss": "4500",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "13.89",
      "acml_vol": "417441",
      "stck_hgpr": "39000",
      "hgpr_hour": "091455",
      "acml_hgpr_date": "20240318",
      "stck_lwpr": "33500",
      "lwpr_hour": "090026",
      "acml_lwpr_date": "20240318",
      "lwpr_vrss_prpr_rate": "10.15",
      "dsgt_date_clpr_vrss_prpr_rate": "13.89",
      "cnnt_ascn_dynu": "1",
      "hgpr_vrss_prpr_rate": "-5.38",
      "cnnt_down_dynu": "4",
      "oprc_vrss_prpr_sign": "2",
      "oprc_vrss_prpr": "0",
      "oprc_vrss_prpr_rate": "0.00",
      "prd_rsfl": "0",
      "prd_rsfl_rate": "0.00"
    },
    {
      "stck_shrn_iscd": "276730",
      "data_rank": "26",
      "hts_kor_isnm": "제주맥주",
      "stck_prpr": "1500",
      "prdy_vrss": "156",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "11.61",
      "acml_vol": "3075893",
      "stck_hgpr": "1550",
      "hgpr_hour": "090617",
      "acml_hgpr_date": "20240318",
      "stck_lwpr": "1365",
      "lwpr_hour": "090109",
      "acml_lwpr_date": "20240318",
      "lwpr_vrss_prpr_rate": "9.89",
      "dsgt_date_clpr_vrss_prpr_rate": "11.61",
      "cnnt_ascn_dynu": "2",
      "hgpr_vrss_prpr_rate": "-3.23",
      "cnnt_down_dynu": "0",
      "oprc_vrss_prpr_sign": "2",
      "oprc_vrss_prpr": "0",
      "oprc_vrss_prpr_rate": "0.00",
      "prd_rsfl": "0",
      "prd_rsfl_rate": "0.00"
    },
    {
      "stck_shrn_iscd": "009620",
      "data_rank": "27",
      "hts_kor_isnm": "삼보산업",
      "stck_prpr": "1103",
      "prdy_vrss": "102",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "10.19",
      "acml_vol": "2834656",
      "stck_hgpr": "1149",
      "hgpr_hour": "091655",
      "acml_hgpr_date": "20240318",
      "stck_lwpr": "1005",
      "lwpr_hour": "090018",
      "acml_lwpr_date": "20240318",
      "lwpr_vrss_prpr_rate": "9.75",
      "dsgt_date_clpr_vrss_prpr_rate": "10.19",
      "cnnt_ascn_dynu": "2",
      "hgpr_vrss_prpr_rate": "-4.00",
      "cnnt_down_dynu": "0",
      "oprc_vrss_prpr_sign": "2",
      "oprc_vrss_prpr": "0",
      "oprc_vrss_prpr_rate": "0.00",
      "prd_rsfl": "0",
      "prd_rsfl_rate": "0.00"
    },
    {
      "stck_shrn_iscd": "457190",
      "data_rank": "28",
      "hts_kor_isnm": "이수스페셜티케미컬",
      "stck_prpr": "389000",
      "prdy_vrss": "46500",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "13.58",
      "acml_vol": "335026",
      "stck_hgpr": "389000",
      "hgpr_hour": "100301",
      "acml_hgpr_date": "20240318",
      "stck_lwpr": "356000",
      "lwpr_hour": "090551",
      "acml_lwpr_date": "20240318",
      "lwpr_vrss_prpr_rate": "9.27",
      "dsgt_date_clpr_vrss_prpr_rate": "13.58",
      "cnnt_ascn_dynu": "2",
      "hgpr_vrss_prpr_rate": "0.00",
      "cnnt_down_dynu": "0",
      "oprc_vrss_prpr_sign": "2",
      "oprc_vrss_prpr": "0",
      "oprc_vrss_prpr_rate": "0.00",
      "prd_rsfl": "0",
      "prd_rsfl_rate": "0.00"
    },
    {
      "stck_shrn_iscd": "005110",
      "data_rank": "29",
      "hts_kor_isnm": "한창",
      "stck_prpr": "1270",
      "prdy_vrss": "104",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "8.92",
      "acml_vol": "1155830",
      "stck_hgpr": "1388",
      "hgpr_hour": "091801",
      "acml_hgpr_date": "20240318",
      "stck_lwpr": "1164",
      "lwpr_hour": "090107",
      "acml_lwpr_date": "20240318",
      "lwpr_vrss_prpr_rate": "9.11",
      "dsgt_date_clpr_vrss_prpr_rate": "8.92",
      "cnnt_ascn_dynu": "1",
      "hgpr_vrss_prpr_rate": "-8.50",
      "cnnt_down_dynu": "1",
      "oprc_vrss_prpr_sign": "2",
      "oprc_vrss_prpr": "0",
      "oprc_vrss_prpr_rate": "0.00",
      "prd_rsfl": "0",
      "prd_rsfl_rate": "0.00"
    },
    {
      "stck_shrn_iscd": "288330",
      "data_rank": "30",
      "hts_kor_isnm": "브릿지바이오테라퓨틱스",
      "stck_prpr": "3455",
      "prdy_vrss": "250",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "7.80",
      "acml_vol": "111007",
      "stck_hgpr": "3595",
      "hgpr_hour": "092107",
      "acml_hgpr_date": "20240318",
      "stck_lwpr": "3175",
      "lwpr_hour": "090157",
      "acml_lwpr_date": "20240318",
      "lwpr_vrss_prpr_rate": "8.82",
      "dsgt_date_clpr_vrss_prpr_rate": "7.80",
      "cnnt_ascn_dynu": "1",
      "hgpr_vrss_prpr_rate": "-3.89",
      "cnnt_down_dynu": "0",
      "oprc_vrss_prpr_sign": "2",
      "oprc_vrss_prpr": "0",
      "oprc_vrss_prpr_rate": "0.00",
      "prd_rsfl": "0",
      "prd_rsfl_rate": "0.00"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```

