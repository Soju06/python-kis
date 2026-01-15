# 변동성완화장치(VI) 현황 [v1_국내주식-055]

> [국내주식] 업종/기타

HTS(eFriend Plus) [0139] 변동성 완화장치(VI) 현황 데이터를 확인할 수 있는 API입니다.

최근 30건까지 확인 가능합니다.


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `f54caf9c-65db-42ee-aa7e-a337c5a41778` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/quotations/inquire-vi-status` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `FHPST01390000` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-01-26
- **최종 수정일**: 2025-05-07

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials G... |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | FHPST01390000 |
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
| `FID_DIV_CLS_CODE` | FID 분류 구분 코드 | String | 2 | Y | 0:전체 1:상승 2:하락 |
| `FID_COND_SCR_DIV_CODE` | FID 조건 화면 분류 코드 | String | 5 | Y | 20139 |
| `FID_MRKT_CLS_CODE` | FID 시장 구분 코드 | String | 2 | Y | 0:전체 K:거래소 Q:코스닥 |
| `FID_INPUT_ISCD` | FID 입력 종목코드 | String | 12 | Y |  |
| `FID_RANK_SORT_CLS_CODE` | FID 순위 정렬 구분 코드 | String | 2 | Y | 0:전체1:정적2:동적3:정적&동적 |
| `FID_INPUT_DATE_1` | FID 입력 날짜1 | String | 10 | Y | 영업일 |
| `FID_TRGT_CLS_CODE` | FID 대상 구분 코드 | String | 32 | Y |  |
| `FID_TRGT_EXLS_CLS_CODE` | FID 대상 제외 구분 코드 | String | 32 | Y |  |

### 요청 예시

```json
{
  "fid_cond_scr_div_code": "20139",
  "fid_mrkt_cls_code": "0",
  "fid_input_iscd": "",
  "fid_rank_sort_cls_code": "0",
  "fid_input_date_1": "20240126",
  "fid_trgt_cls_code": "",
  "fid_trgt_exls_cls_code": "",
  "fid_div_cls_code": "0"
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
| `output` | 응답상세 | String |   | Y |  |
| `hts_kor_isnm` | HTS 한글 종목명 | String | 40 | Y |  |
| `mksc_shrn_iscd` | 유가증권 단축 종목코드 | String | 9 | Y |  |
| `vi_cls_code` | VI발동상태 | String | 1 | Y | Y: 발동 / N: 해제 |
| `bsop_date` | 영업 일자 | String | 8 | Y |  |
| `cntg_vi_hour` | VI발동시간 | String | 6 | Y | VI발동시간 |
| `vi_cncl_hour` | VI해제시간 | String | 6 | Y | VI해제시간 |
| `vi_kind_code` | VI종류코드 | String | 1 | Y | 1:정적 2:동적 3:정적&동적 |
| `vi_prc` | VI발동가격 | String | 10 | Y |  |
| `vi_stnd_prc` | 정적VI발동기준가격 | String | 10 | Y |  |
| `vi_dprt` | 정적VI발동괴리율 | String | 82 | Y | % |
| `vi_dmc_stnd_prc` | 동적VI발동기준가격 | String | 10 | Y |  |
| `vi_dmc_dprt` | 동적VI발동괴리율 | String | 82 | Y | % |
| `vi_count` | VI발동횟수 | String | 7 | Y |  |

### 응답 예시

```json
{
  "output": [
    {
      "hts_kor_isnm": "KODEX Fn멀티팩터",
      "mksc_shrn_iscd": "337120",
      "vi_cls_code": "N",
      "bsop_date": "20240126",
      "cntg_vi_hour": "174012",
      "vi_cncl_hour": "174212",
      "vi_kind_code": "2",
      "vi_prc": "12135",
      "vi_stnd_prc": "0",
      "vi_dprt": "0.00",
      "vi_dmc_stnd_prc": "13275",
      "vi_dmc_dprt": "-8.59",
      "vi_count": "2"
    },
    {
      "hts_kor_isnm": "루멘스",
      "mksc_shrn_iscd": "038060",
      "vi_cls_code": "N",
      "bsop_date": "20240126",
      "cntg_vi_hour": "174008",
      "vi_cncl_hour": "174210",
      "vi_kind_code": "2",
      "vi_prc": "1337",
      "vi_stnd_prc": "0",
      "vi_dprt": "0.00",
      "vi_dmc_stnd_prc": "1241",
      "vi_dmc_dprt": "7.74",
      "vi_count": "1"
    },
    {
      "hts_kor_isnm": "DL건설",
      "mksc_shrn_iscd": "001880",
      "vi_cls_code": "N",
      "bsop_date": "20240126",
      "cntg_vi_hour": "173030",
      "vi_cncl_hour": "173234",
      "vi_kind_code": "2",
      "vi_prc": "14000",
      "vi_stnd_prc": "0",
      "vi_dprt": "0.00",
      "vi_dmc_stnd_prc": "14990",
      "vi_dmc_dprt": "-6.60",
      "vi_count": "2"
    },
    {
      "hts_kor_isnm": "성창기업지주",
      "mksc_shrn_iscd": "000180",
      "vi_cls_code": "N",
      "bsop_date": "20240126",
      "cntg_vi_hour": "173030",
      "vi_cncl_hour": "173224",
      "vi_kind_code": "2",
      "vi_prc": "1860",
      "vi_stnd_prc": "0",
      "vi_dprt": "0.00",
      "vi_dmc_stnd_prc": "1992",
      "vi_dmc_dprt": "-6.63",
      "vi_count": "2"
    },
    {
      "hts_kor_isnm": "성창기업지주",
      "mksc_shrn_iscd": "000180",
      "vi_cls_code": "N",
      "bsop_date": "20240126",
      "cntg_vi_hour": "172030",
      "vi_cncl_hour": "172204",
      "vi_kind_code": "2",
      "vi_prc": "1992",
      "vi_stnd_prc": "0",
      "vi_dprt": "0.00",
      "vi_dmc_stnd_prc": "1857",
      "vi_dmc_dprt": "7.27",
      "vi_count": "1"
    },
    {
      "hts_kor_isnm": "유아이디",
      "mksc_shrn_iscd": "069330",
      "vi_cls_code": "N",
      "bsop_date": "20240126",
      "cntg_vi_hour": "172030",
      "vi_cncl_hour": "172234",
      "vi_kind_code": "2",
      "vi_prc": "1640",
      "vi_stnd_prc": "0",
      "vi_dprt": "0.00",
      "vi_dmc_stnd_prc": "1490",
      "vi_dmc_dprt": "10.07",
      "vi_count": "1"
    },
    {
      "hts_kor_isnm": "뷰웍스",
      "mksc_shrn_iscd": "100120",
      "vi_cls_code": "N",
      "bsop_date": "20240126",
      "cntg_vi_hour": "172010",
      "vi_cncl_hour": "172208",
      "vi_kind_code": "2",
      "vi_prc": "27700",
      "vi_stnd_prc": "0",
      "vi_dprt": "0.00",
      "vi_dmc_stnd_prc": "29700",
      "vi_dmc_dprt": "-6.73",
      "vi_count": "2"
    },
    {
      "hts_kor_isnm": "TIGER 미국배당+3%프리미엄다우존스",
      "mksc_shrn_iscd": "458750",
      "vi_cls_code": "N",
      "bsop_date": "20240126",
      "cntg_vi_hour": "171030",
      "vi_cncl_hour": "171212",
      "vi_kind_code": "2",
      "vi_prc": "11700",
      "vi_stnd_prc": "0",
      "vi_dprt": "0.00",
      "vi_dmc_stnd_prc": "10675",
      "vi_dmc_dprt": "9.60",
      "vi_count": "1"
    },
    {
      "hts_kor_isnm": "아스타",
      "mksc_shrn_iscd": "246720",
      "vi_cls_code": "N",
      "bsop_date": "20240126",
      "cntg_vi_hour": "171030",
      "vi_cncl_hour": "171253",
      "vi_kind_code": "2",
      "vi_prc": "5100",
      "vi_stnd_prc": "0",
      "vi_dprt": "0.00",
      "vi_dmc_stnd_prc": "5490",
      "vi_dmc_dprt": "-7.10",
      "vi_count": "2"
    },
    {
      "hts_kor_isnm": "제일전기공업",
      "mksc_shrn_iscd": "199820",
      "vi_cls_code": "N",
      "bsop_date": "20240126",
      "cntg_vi_hour": "170030",
      "vi_cncl_hour": "170232",
      "vi_kind_code": "2",
      "vi_prc": "10050",
      "vi_stnd_prc": "0",
      "vi_dprt": "0.00",
      "vi_dmc_stnd_prc": "9350",
      "vi_dmc_dprt": "7.49",
      "vi_count": "1"
    },
    {
      "hts_kor_isnm": "파인디지털",
      "mksc_shrn_iscd": "038950",
      "vi_cls_code": "N",
      "bsop_date": "20240126",
      "cntg_vi_hour": "170030",
      "vi_cncl_hour": "170244",
      "vi_kind_code": "2",
      "vi_prc": "5200",
      "vi_stnd_prc": "0",
      "vi_dprt": "0.00",
      "vi_dmc_stnd_prc": "4800",
      "vi_dmc_dprt": "8.33",
      "vi_count": "1"
    },
    {
      "hts_kor_isnm": "엔시트론",
      "mksc_shrn_iscd": "101400",
      "vi_cls_code": "N",
      "bsop_date": "20240126",
      "cntg_vi_hour": "170013",
      "vi_cncl_hour": "170218",
      "vi_kind_code": "2",
      "vi_prc": "644",
      "vi_stnd_prc": "0",
      "vi_dprt": "0.00",
      "vi_dmc_stnd_prc": "604",
      "vi_dmc_dprt": "6.62",
      "vi_count": "1"
    },
    {
      "hts_kor_isnm": "TIGER 2차전지TOP10",
      "mksc_shrn_iscd": "364980",
      "vi_cls_code": "N",
      "bsop_date": "20240126",
      "cntg_vi_hour": "165030",
      "vi_cncl_hour": "165250",
      "vi_kind_code": "2",
      "vi_prc": "12450",
      "vi_stnd_prc": "0",
      "vi_dprt": "0.00",
      "vi_dmc_stnd_prc": "13740",
      "vi_dmc_dprt": "-9.39",
      "vi_count": "2"
    },
    {
      "hts_kor_isnm": "지니너스",
      "mksc_shrn_iscd": "389030",
      "vi_cls_code": "N",
      "bsop_date": "20240126",
      "cntg_vi_hour": "165030",
      "vi_cncl_hour": "165222",
      "vi_kind_code": "2",
      "vi_prc": "2270",
      "vi_stnd_prc": "0",
      "vi_dprt": "0.00",
      "vi_dmc_stnd_prc": "2125",
      "vi_dmc_dprt": "6.82",
      "vi_count": "1"
    },
    {
      "hts_kor_isnm": "패션플랫폼",
      "mksc_shrn_iscd": "225590",
      "vi_cls_code": "N",
      "bsop_date": "20240126",
      "cntg_vi_hour": "165030",
      "vi_cncl_hour": "165228",
      "vi_kind_code": "2",
      "vi_prc": "1263",
      "vi_stnd_prc": "0",
      "vi_dprt": "0.00",
      "vi_dmc_stnd_prc": "1153",
      "vi_dmc_dprt": "9.54",
      "vi_count": "1"
    },
    {
      "hts_kor_isnm": "씨엔플러스",
      "mksc_shrn_iscd": "115530",
      "vi_cls_code": "N",
      "bsop_date": "20240126",
      "cntg_vi_hour": "165030",
      "vi_cncl_hour": "165240",
      "vi_kind_code": "2",
      "vi_prc": "344",
      "vi_stnd_prc": "0",
      "vi_dprt": "0.00",
      "vi_dmc_stnd_prc": "368",
      "vi_dmc_dprt": "-6.52",
      "vi_count": "2"
    },
    {
      "hts_kor_isnm": "케이비제22호스팩",
      "mksc_shrn_iscd": "436530",
      "vi_cls_code": "N",
      "bsop_date": "20240126",
      "cntg_vi_hour": "164030",
      "vi_cncl_hour": "164208",
      "vi_kind_code": "2",
      "vi_prc": "4455",
      "vi_stnd_prc": "0",
      "vi_dprt": "0.00",
      "vi_dmc_stnd_prc": "4795",
      "vi_dmc_dprt": "-7.09",
      "vi_count": "2"
    },
    {
      "hts_kor_isnm": "제너셈",
      "mksc_shrn_iscd": "217190",
      "vi_cls_code": "N",
      "bsop_date": "20240126",
      "cntg_vi_hour": "164030",
      "vi_cncl_hour": "164230",
      "vi_kind_code": "2",
      "vi_prc": "14980",
      "vi_stnd_prc": "0",
      "vi_dprt": "0.00",
      "vi_dmc_stnd_prc": "15990",
      "vi_dmc_dprt": "-6.32",
      "vi_count": "2"
    },
    {
      "hts_kor_isnm": "아스타",
      "mksc_shrn_iscd": "246720",
      "vi_cls_code": "N",
      "bsop_date": "20240126",
      "cntg_vi_hour": "163030",
      "vi_cncl_hour": "163220",
      "vi_kind_code": "2",
      "vi_prc": "5550",
      "vi_stnd_prc": "0",
      "vi_dprt": "0.00",
      "vi_dmc_stnd_prc": "5090",
      "vi_dmc_dprt": "9.04",
      "vi_count": "1"
    },
    {
      "hts_kor_isnm": "세니젠",
      "mksc_shrn_iscd": "188260",
      "vi_cls_code": "N",
      "bsop_date": "20240126",
      "cntg_vi_hour": "163030",
      "vi_cncl_hour": "163252",
      "vi_kind_code": "2",
      "vi_prc": "3955",
      "vi_stnd_prc": "0",
      "vi_dprt": "0.00",
      "vi_dmc_stnd_prc": "4230",
      "vi_dmc_dprt": "-6.50",
      "vi_count": "2"
    },
    {
      "hts_kor_isnm": "KODEX Fn멀티팩터",
      "mksc_shrn_iscd": "337120",
      "vi_cls_code": "N",
      "bsop_date": "20240126",
      "cntg_vi_hour": "163024",
      "vi_cncl_hour": "163250",
      "vi_kind_code": "2",
      "vi_prc": "13280",
      "vi_stnd_prc": "0",
      "vi_dprt": "0.00",
      "vi_dmc_stnd_prc": "12075",
      "vi_dmc_dprt": "9.98",
      "vi_count": "1"
    },
    {
      "hts_kor_isnm": "ES큐브",
      "mksc_shrn_iscd": "050120",
      "vi_cls_code": "N",
      "bsop_date": "20240126",
      "cntg_vi_hour": "163017",
      "vi_cncl_hour": "163228",
      "vi_kind_code": "2",
      "vi_prc": "3055",
      "vi_stnd_prc": "0",
      "vi_dprt": "0.00",
      "vi_dmc_stnd_prc": "2860",
      "vi_dmc_dprt": "6.82",
      "vi_count": "1"
    },
    {
      "hts_kor_isnm": "무학",
      "mksc_shrn_iscd": "033920",
      "vi_cls_code": "N",
      "bsop_date": "20240126",
      "cntg_vi_hour": "162030",
      "vi_cncl_hour": "162241",
      "vi_kind_code": "2",
      "vi_prc": "5220",
      "vi_stnd_prc": "0",
      "vi_dprt": "0.00",
      "vi_dmc_stnd_prc": "4880",
      "vi_dmc_dprt": "6.97",
      "vi_count": "1"
    },
    {
      "hts_kor_isnm": "아이씨에이치",
      "mksc_shrn_iscd": "368600",
      "vi_cls_code": "N",
      "bsop_date": "20240126",
      "cntg_vi_hour": "162030",
      "vi_cncl_hour": "162210",
      "vi_kind_code": "2",
      "vi_prc": "5860",
      "vi_stnd_prc": "0",
      "vi_dprt": "0.00",
      "vi_dmc_stnd_prc": "5460",
      "vi_dmc_dprt": "7.33",
      "vi_count": "1"
    },
    {
      "hts_kor_isnm": "KBSTAR 2차전지TOP10",
      "mksc_shrn_iscd": "465330",
      "vi_cls_code": "N",
      "bsop_date": "20240126",
      "cntg_vi_hour": "162030",
      "vi_cncl_hour": "162217",
      "vi_kind_code": "2",
      "vi_prc": "14475",
      "vi_stnd_prc": "0",
      "vi_dprt": "0.00",
      "vi_dmc_stnd_prc": "13485",
      "vi_dmc_dprt": "7.34",
      "vi_count": "1"
    },
    {
      "hts_kor_isnm": "제너셈",
      "mksc_shrn_iscd": "217190",
      "vi_cls_code": "N",
      "bsop_date": "20240126",
      "cntg_vi_hour": "162030",
      "vi_cncl_hour": "162232",
      "vi_kind_code": "2",
      "vi_prc": "15990",
      "vi_stnd_prc": "0",
      "vi_dprt": "0.00",
      "vi_dmc_stnd_prc": "14910",
      "vi_dmc_dprt": "7.24",
      "vi_count": "1"
    },
    {
      "hts_kor_isnm": "알엔투테크놀로지",
      "mksc_shrn_iscd": "148250",
      "vi_cls_code": "N",
      "bsop_date": "20240126",
      "cntg_vi_hour": "162030",
      "vi_cncl_hour": "162212",
      "vi_kind_code": "2",
      "vi_prc": "5390",
      "vi_stnd_prc": "0",
      "vi_dprt": "0.00",
      "vi_dmc_stnd_prc": "4915",
      "vi_dmc_dprt": "9.66",
      "vi_count": "1"
    },
    {
      "hts_kor_isnm": "엑서지21",
      "mksc_shrn_iscd": "043090",
      "vi_cls_code": "N",
      "bsop_date": "20240126",
      "cntg_vi_hour": "162030",
      "vi_cncl_hour": "162206",
      "vi_kind_code": "2",
      "vi_prc": "463",
      "vi_stnd_prc": "0",
      "vi_dprt": "0.00",
      "vi_dmc_stnd_prc": "507",
      "vi_dmc_dprt": "-8.68",
      "vi_count": "2"
    },
    {
      "hts_kor_isnm": "DL건설",
      "mksc_shrn_iscd": "001880",
      "vi_cls_code": "N",
      "bsop_date": "20240126",
      "cntg_vi_hour": "162028",
      "vi_cncl_hour": "162214",
      "vi_kind_code": "2",
      "vi_prc": "15010",
      "vi_stnd_prc": "0",
      "vi_dprt": "0.00",
      "vi_dmc_stnd_prc": "14000",
      "vi_dmc_dprt": "7.21",
      "vi_count": "1"
    },
    {
      "hts_kor_isnm": "뷰웍스",
      "mksc_shrn_iscd": "100120",
      "vi_cls_code": "N",
      "bsop_date": "20240126",
      "cntg_vi_hour": "162015",
      "vi_cncl_hour": "162207",
      "vi_kind_code": "2",
      "vi_prc": "27600",
      "vi_stnd_prc": "0",
      "vi_dprt": "0.00",
      "vi_dmc_stnd_prc": "29700",
      "vi_dmc_dprt": "-7.07",
      "vi_count": "1"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```

