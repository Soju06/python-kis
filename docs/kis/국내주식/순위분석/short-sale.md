# 국내주식 공매도 상위종목[국내주식-133]

> [국내주식] 순위분석

공매도 상위종목 API입니다. 
한국투자 HTS(eFriend Plus) > [0482] 공매도 상위 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.
최대 30건 확인 가능하며, 다음 조회가 불가합니다.

※ 30건 이상의 목록 조회가 필요한 경우, 대안으로 종목조건검색 API를 이용해서 원하는 종목 100개까지 검색할 수 있는 기능을 제공하고 있습니다.
종목조건검색 API는 HTS(efriend Plus) [0110] 조건검색에서 등록 및 서버저장한 나의 조건 목록을 확인할 수 있는 API로,
자세한 사용 방법은 공지사항 - [조건검색 필독] 조건검색 API 이용안내 참고 부탁드립니다.

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `4745d669-557b-413c-aa0b-522e620cd832` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/ranking/short-sale` |
| **Content-Type** | `` |
| **요청 포맷** | `` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `미지원` |
| **TR ID** | `FHPST04820000`, `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-03-27
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
| `tr_id` | 거래ID | String | 13 | Y | FHPST04820000 |
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
| `FID_APLY_RANG_VOL` | FID 적용 범위 거래량 | String | 18 | Y | 공백 |
| `FID_COND_MRKT_DIV_CODE` | 조건 시장 분류 코드 | String | 2 | Y | 시장구분코드 (주식 J) |
| `FID_COND_SCR_DIV_CODE` | 조건 화면 분류 코드 | String | 5 | Y | Unique key(20482) |
| `FID_INPUT_ISCD` | 입력 종목코드 | String | 12 | Y | 0000:전체, 0001:코스피, 1001:코스닥, 2001:코스피200, 4001: KRX100, 3003: 코스닥150 |
| `FID_PERIOD_DIV_CODE` | 조회구분 (일/월) | String | 32 | Y | 조회구분 (일/월) D: 일, M:월 |
| `FID_INPUT_CNT_1` | 조회가간(일수 | String | 12 | Y | '조회가간(일수): 조회구분(D) 0:1일, 1:2일, 2:3일, 3:4일, 4:1주일, 9:2주일, 14:3주일,  조회구분(M) 1:1개월,  2:2개월, 3:3개월' |
| `FID_TRGT_EXLS_CLS_CODE` | 대상 제외 구분 코드 | String | 32 | Y | 공백 |
| `FID_TRGT_CLS_CODE` | FID 대상 구분 코드 | String | 32 | Y | 공백 |
| `FID_APLY_RANG_PRC_1` | FID 적용 범위 가격1 | String | 18 | Y | 가격 ~ |
| `FID_APLY_RANG_PRC_2` | FID 적용 범위 가격2 | String | 18 | Y | ~ 가격 |

### 요청 예시

```json
fid_cond_mrkt_div_code:J
fid_cond_scr_div_code:20482
fid_input_iscd:0000
fid_period_div_code:D
fid_input_cnt_1:000000000000
fid_trgt_exls_cls_code:0
fid_trgt_cls_code:0
fid_aply_rang_prc_1:
fid_aply_rang_prc_2:
fid_aply_rang_vol:0
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
| `hts_kor_isnm` | HTS 한글 종목명 | String | 40 | Y |  |
| `stck_prpr` | 주식 현재가 | String | 10 | Y |  |
| `prdy_vrss` | 전일 대비 | String | 10 | Y |  |
| `prdy_vrss_sign` | 전일 대비 부호 | String | 1 | Y |  |
| `prdy_ctrt` | 전일 대비율 | String | 82 | Y |  |
| `acml_vol` | 누적 거래량 | String | 18 | Y |  |
| `acml_tr_pbmn` | 누적 거래 대금 | String | 18 | Y |  |
| `ssts_cntg_qty` | 공매도 체결 수량 | String | 12 | Y |  |
| `ssts_vol_rlim` | 공매도 거래량 비중 | String | 62 | Y |  |
| `ssts_tr_pbmn` | 공매도 거래 대금 | String | 18 | Y |  |
| `ssts_tr_pbmn_rlim` | 공매도 거래대금 비중 | String | 62 | Y |  |
| `stnd_date1` | 기준 일자1 | String | 8 | Y |  |
| `stnd_date2` | 기준 일자2 | String | 8 | Y |  |
| `avrg_prc` | 평균가격 | String | 11 | Y |  |

### 응답 예시

```json
{
  "output": [
    {
      "mksc_shrn_iscd": "138930",
      "hts_kor_isnm": "BNK금융지주",
      "stck_prpr": "7760",
      "prdy_vrss": "-10",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-0.13",
      "acml_vol": "874160",
      "acml_tr_pbmn": "6842692780",
      "ssts_cntg_qty": "64031",
      "ssts_vol_rlim": "7.32",
      "ssts_tr_pbmn": "499643430",
      "ssts_tr_pbmn_rlim": "7.30",
      "stnd_date1": "20240329",
      "stnd_date2": "20240329",
      "avrg_prc": "7803"
    },
    {
      "mksc_shrn_iscd": "024110",
      "hts_kor_isnm": "기업은행",
      "stck_prpr": "13230",
      "prdy_vrss": "-270",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-2.00",
      "acml_vol": "2940414",
      "acml_tr_pbmn": "39892800710",
      "ssts_cntg_qty": "42457",
      "ssts_vol_rlim": "1.44",
      "ssts_tr_pbmn": "573293240",
      "ssts_tr_pbmn_rlim": "1.44",
      "stnd_date1": "0",
      "stnd_date2": "0",
      "avrg_prc": "13502"
    },
    {
      "mksc_shrn_iscd": "067310",
      "hts_kor_isnm": "하나마이크론",
      "stck_prpr": "29300",
      "prdy_vrss": "650",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "2.27",
      "acml_vol": "7785025",
      "acml_tr_pbmn": "219228491967",
      "ssts_cntg_qty": "41626",
      "ssts_vol_rlim": "0.53",
      "ssts_tr_pbmn": "1195641050",
      "ssts_tr_pbmn_rlim": "0.55",
      "stnd_date1": "0",
      "stnd_date2": "0",
      "avrg_prc": "28723"
    },
    {
      "mksc_shrn_iscd": "139130",
      "hts_kor_isnm": "DGB금융지주",
      "stck_prpr": "8480",
      "prdy_vrss": "-70",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-0.82",
      "acml_vol": "646804",
      "acml_tr_pbmn": "5579590090",
      "ssts_cntg_qty": "41615",
      "ssts_vol_rlim": "6.43",
      "ssts_tr_pbmn": "357709910",
      "ssts_tr_pbmn_rlim": "6.41",
      "stnd_date1": "0",
      "stnd_date2": "0",
      "avrg_prc": "8595"
    },
    {
      "mksc_shrn_iscd": "316140",
      "hts_kor_isnm": "우리금융지주",
      "stck_prpr": "14050",
      "prdy_vrss": "-270",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-1.89",
      "acml_vol": "2158189",
      "acml_tr_pbmn": "30895435840",
      "ssts_cntg_qty": "39928",
      "ssts_vol_rlim": "1.85",
      "ssts_tr_pbmn": "570341910",
      "ssts_tr_pbmn_rlim": "1.85",
      "stnd_date1": "0",
      "stnd_date2": "0",
      "avrg_prc": "14284"
    },
    {
      "mksc_shrn_iscd": "005930",
      "hts_kor_isnm": "삼성전자",
      "stck_prpr": "82800",
      "prdy_vrss": "400",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "0.49",
      "acml_vol": "27126366",
      "acml_tr_pbmn": "2224901311700",
      "ssts_cntg_qty": "39325",
      "ssts_vol_rlim": "0.14",
      "ssts_tr_pbmn": "3236734600",
      "ssts_tr_pbmn_rlim": "0.15",
      "stnd_date1": "0",
      "stnd_date2": "0",
      "avrg_prc": "82307"
    },
    {
      "mksc_shrn_iscd": "00680K",
      "hts_kor_isnm": "미래에셋증권2우B",
      "stck_prpr": "3590",
      "prdy_vrss": "-85",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-2.31",
      "acml_vol": "521897",
      "acml_tr_pbmn": "1920418685",
      "ssts_cntg_qty": "27624",
      "ssts_vol_rlim": "5.29",
      "ssts_tr_pbmn": "101602075",
      "ssts_tr_pbmn_rlim": "5.29",
      "stnd_date1": "0",
      "stnd_date2": "0",
      "avrg_prc": "3678"
    },
    {
      "mksc_shrn_iscd": "088350",
      "hts_kor_isnm": "한화생명",
      "stck_prpr": "2835",
      "prdy_vrss": "0",
      "prdy_vrss_sign": "3",
      "prdy_ctrt": "0.00",
      "acml_vol": "2781608",
      "acml_tr_pbmn": "7916471305",
      "ssts_cntg_qty": "25456",
      "ssts_vol_rlim": "0.92",
      "ssts_tr_pbmn": "72204695",
      "ssts_tr_pbmn_rlim": "0.91",
      "stnd_date1": "0",
      "stnd_date2": "0",
      "avrg_prc": "2836"
    },
    {
      "mksc_shrn_iscd": "005940",
      "hts_kor_isnm": "NH투자증권",
      "stck_prpr": "11350",
      "prdy_vrss": "-350",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-2.99",
      "acml_vol": "750616",
      "acml_tr_pbmn": "8827218780",
      "ssts_cntg_qty": "24915",
      "ssts_vol_rlim": "3.32",
      "ssts_tr_pbmn": "292457920",
      "ssts_tr_pbmn_rlim": "3.31",
      "stnd_date1": "0",
      "stnd_date2": "0",
      "avrg_prc": "11738"
    },
    {
      "mksc_shrn_iscd": "032640",
      "hts_kor_isnm": "LG유플러스",
      "stck_prpr": "9990",
      "prdy_vrss": "20",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "0.20",
      "acml_vol": "796940",
      "acml_tr_pbmn": "7972130660",
      "ssts_cntg_qty": "23173",
      "ssts_vol_rlim": "2.91",
      "ssts_tr_pbmn": "231604320",
      "ssts_tr_pbmn_rlim": "2.91",
      "stnd_date1": "0",
      "stnd_date2": "0",
      "avrg_prc": "9994"
    },
    {
      "mksc_shrn_iscd": "007660",
      "hts_kor_isnm": "이수페타시스",
      "stck_prpr": "41950",
      "prdy_vrss": "-350",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-0.83",
      "acml_vol": "5735235",
      "acml_tr_pbmn": "247424365700",
      "ssts_cntg_qty": "20252",
      "ssts_vol_rlim": "0.35",
      "ssts_tr_pbmn": "861494300",
      "ssts_tr_pbmn_rlim": "0.35",
      "stnd_date1": "0",
      "stnd_date2": "0",
      "avrg_prc": "42538"
    },
    {
      "mksc_shrn_iscd": "175330",
      "hts_kor_isnm": "JB금융지주",
      "stck_prpr": "12680",
      "prdy_vrss": "-520",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-3.94",
      "acml_vol": "275866",
      "acml_tr_pbmn": "3642365310",
      "ssts_cntg_qty": "19076",
      "ssts_vol_rlim": "6.91",
      "ssts_tr_pbmn": "251554220",
      "ssts_tr_pbmn_rlim": "6.91",
      "stnd_date1": "0",
      "stnd_date2": "0",
      "avrg_prc": "13186"
    },
    {
      "mksc_shrn_iscd": "353200",
      "hts_kor_isnm": "대덕전자",
      "stck_prpr": "26850",
      "prdy_vrss": "2300",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "9.37",
      "acml_vol": "959488",
      "acml_tr_pbmn": "23364959800",
      "ssts_cntg_qty": "18988",
      "ssts_vol_rlim": "1.98",
      "ssts_tr_pbmn": "465048200",
      "ssts_tr_pbmn_rlim": "1.99",
      "stnd_date1": "0",
      "stnd_date2": "0",
      "avrg_prc": "24491"
    },
    {
      "mksc_shrn_iscd": "403870",
      "hts_kor_isnm": "HPSP",
      "stck_prpr": "52000",
      "prdy_vrss": "-1100",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-2.07",
      "acml_vol": "1821358",
      "acml_tr_pbmn": "96690901900",
      "ssts_cntg_qty": "14408",
      "ssts_vol_rlim": "0.79",
      "ssts_tr_pbmn": "764718100",
      "ssts_tr_pbmn_rlim": "0.79",
      "stnd_date1": "0",
      "stnd_date2": "0",
      "avrg_prc": "53075"
    },
    {
      "mksc_shrn_iscd": "003540",
      "hts_kor_isnm": "대신증권",
      "stck_prpr": "15540",
      "prdy_vrss": "-100",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-0.64",
      "acml_vol": "106254",
      "acml_tr_pbmn": "1670379320",
      "ssts_cntg_qty": "13935",
      "ssts_vol_rlim": "13.11",
      "ssts_tr_pbmn": "218404520",
      "ssts_tr_pbmn_rlim": "13.08",
      "stnd_date1": "0",
      "stnd_date2": "0",
      "avrg_prc": "15673"
    },
    {
      "mksc_shrn_iscd": "000660",
      "hts_kor_isnm": "SK하이닉스",
      "stck_prpr": "185900",
      "prdy_vrss": "2900",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "1.58",
      "acml_vol": "3035080",
      "acml_tr_pbmn": "550258980100",
      "ssts_cntg_qty": "13524",
      "ssts_vol_rlim": "0.45",
      "ssts_tr_pbmn": "2459992400",
      "ssts_tr_pbmn_rlim": "0.45",
      "stnd_date1": "0",
      "stnd_date2": "0",
      "avrg_prc": "181898"
    },
    {
      "mksc_shrn_iscd": "095340",
      "hts_kor_isnm": "ISC",
      "stck_prpr": "95500",
      "prdy_vrss": "-2500",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-2.55",
      "acml_vol": "387100",
      "acml_tr_pbmn": "37858878700",
      "ssts_cntg_qty": "11023",
      "ssts_vol_rlim": "2.85",
      "ssts_tr_pbmn": "1080996600",
      "ssts_tr_pbmn_rlim": "2.86",
      "stnd_date1": "0",
      "stnd_date2": "0",
      "avrg_prc": "98067"
    },
    {
      "mksc_shrn_iscd": "005935",
      "hts_kor_isnm": "삼성전자우",
      "stck_prpr": "68000",
      "prdy_vrss": "0",
      "prdy_vrss_sign": "3",
      "prdy_ctrt": "0.00",
      "acml_vol": "1792197",
      "acml_tr_pbmn": "121695607500",
      "ssts_cntg_qty": "10863",
      "ssts_vol_rlim": "0.61",
      "ssts_tr_pbmn": "739454700",
      "ssts_tr_pbmn_rlim": "0.61",
      "stnd_date1": "0",
      "stnd_date2": "0",
      "avrg_prc": "68070"
    },
    {
      "mksc_shrn_iscd": "036540",
      "hts_kor_isnm": "SFA반도체",
      "stck_prpr": "6100",
      "prdy_vrss": "70",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "1.16",
      "acml_vol": "2015142",
      "acml_tr_pbmn": "12201512130",
      "ssts_cntg_qty": "10781",
      "ssts_vol_rlim": "0.53",
      "ssts_tr_pbmn": "65141390",
      "ssts_tr_pbmn_rlim": "0.53",
      "stnd_date1": "0",
      "stnd_date2": "0",
      "avrg_prc": "6042"
    },
    {
      "mksc_shrn_iscd": "029780",
      "hts_kor_isnm": "삼성카드",
      "stck_prpr": "37200",
      "prdy_vrss": "-650",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-1.72",
      "acml_vol": "124920",
      "acml_tr_pbmn": "4724311400",
      "ssts_cntg_qty": "10618",
      "ssts_vol_rlim": "8.50",
      "ssts_tr_pbmn": "400737650",
      "ssts_tr_pbmn_rlim": "8.48",
      "stnd_date1": "0",
      "stnd_date2": "0",
      "avrg_prc": "37741"
    },
    {
      "mksc_shrn_iscd": "003690",
      "hts_kor_isnm": "코리안리",
      "stck_prpr": "8350",
      "prdy_vrss": "50",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "0.60",
      "acml_vol": "511433",
      "acml_tr_pbmn": "4226681430",
      "ssts_cntg_qty": "10065",
      "ssts_vol_rlim": "1.97",
      "ssts_tr_pbmn": "83410590",
      "ssts_tr_pbmn_rlim": "1.97",
      "stnd_date1": "0",
      "stnd_date2": "0",
      "avrg_prc": "8287"
    },
    {
      "mksc_shrn_iscd": "030000",
      "hts_kor_isnm": "제일기획",
      "stck_prpr": "19110",
      "prdy_vrss": "330",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "1.76",
      "acml_vol": "216890",
      "acml_tr_pbmn": "4081885780",
      "ssts_cntg_qty": "10014",
      "ssts_vol_rlim": "4.62",
      "ssts_tr_pbmn": "188337710",
      "ssts_tr_pbmn_rlim": "4.61",
      "stnd_date1": "0",
      "stnd_date2": "0",
      "avrg_prc": "18807"
    },
    {
      "mksc_shrn_iscd": "090350",
      "hts_kor_isnm": "노루페인트",
      "stck_prpr": "9960",
      "prdy_vrss": "270",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "2.79",
      "acml_vol": "168269",
      "acml_tr_pbmn": "1640849400",
      "ssts_cntg_qty": "9186",
      "ssts_vol_rlim": "5.46",
      "ssts_tr_pbmn": "89164490",
      "ssts_tr_pbmn_rlim": "5.43",
      "stnd_date1": "0",
      "stnd_date2": "0",
      "avrg_prc": "9706"
    },
    {
      "mksc_shrn_iscd": "086790",
      "hts_kor_isnm": "하나금융지주",
      "stck_prpr": "56600",
      "prdy_vrss": "-1100",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-1.91",
      "acml_vol": "740105",
      "acml_tr_pbmn": "43037308100",
      "ssts_cntg_qty": "8114",
      "ssts_vol_rlim": "1.10",
      "ssts_tr_pbmn": "471499600",
      "ssts_tr_pbmn_rlim": "1.10",
      "stnd_date1": "0",
      "stnd_date2": "0",
      "avrg_prc": "58109"
    },
    {
      "mksc_shrn_iscd": "042700",
      "hts_kor_isnm": "한미반도체",
      "stck_prpr": "140400",
      "prdy_vrss": "6700",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "5.01",
      "acml_vol": "4188468",
      "acml_tr_pbmn": "562948611100",
      "ssts_cntg_qty": "7927",
      "ssts_vol_rlim": "0.19",
      "ssts_tr_pbmn": "1061391800",
      "ssts_tr_pbmn_rlim": "0.19",
      "stnd_date1": "0",
      "stnd_date2": "0",
      "avrg_prc": "133895"
    },
    {
      "mksc_shrn_iscd": "055550",
      "hts_kor_isnm": "신한지주",
      "stck_prpr": "45500",
      "prdy_vrss": "-500",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-1.09",
      "acml_vol": "1377596",
      "acml_tr_pbmn": "63828246950",
      "ssts_cntg_qty": "7790",
      "ssts_vol_rlim": "0.57",
      "ssts_tr_pbmn": "360468750",
      "ssts_tr_pbmn_rlim": "0.56",
      "stnd_date1": "0",
      "stnd_date2": "0",
      "avrg_prc": "46273"
    },
    {
      "mksc_shrn_iscd": "044450",
      "hts_kor_isnm": "KSS해운",
      "stck_prpr": "8220",
      "prdy_vrss": "20",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "0.24",
      "acml_vol": "42700",
      "acml_tr_pbmn": "353638500",
      "ssts_cntg_qty": "7617",
      "ssts_vol_rlim": "17.84",
      "ssts_tr_pbmn": "62980890",
      "ssts_tr_pbmn_rlim": "17.81",
      "stnd_date1": "0",
      "stnd_date2": "0",
      "avrg_prc": "8268"
    },
    {
      "mksc_shrn_iscd": "300720",
      "hts_kor_isnm": "한일시멘트",
      "stck_prpr": "12180",
      "prdy_vrss": "-120",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-0.98",
      "acml_vol": "28707",
      "acml_tr_pbmn": "354558700",
      "ssts_cntg_qty": "7547",
      "ssts_vol_rlim": "26.29",
      "ssts_tr_pbmn": "93090530",
      "ssts_tr_pbmn_rlim": "26.26",
      "stnd_date1": "0",
      "stnd_date2": "0",
      "avrg_prc": "12334"
    },
    {
      "mksc_shrn_iscd": "105560",
      "hts_kor_isnm": "KB금융",
      "stck_prpr": "68800",
      "prdy_vrss": "-700",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-1.01",
      "acml_vol": "1004163",
      "acml_tr_pbmn": "70541592600",
      "ssts_cntg_qty": "7255",
      "ssts_vol_rlim": "0.72",
      "ssts_tr_pbmn": "508167300",
      "ssts_tr_pbmn_rlim": "0.72",
      "stnd_date1": "0",
      "stnd_date2": "0",
      "avrg_prc": "70043"
    },
    {
      "mksc_shrn_iscd": "017670",
      "hts_kor_isnm": "SK텔레콤",
      "stck_prpr": "52000",
      "prdy_vrss": "-500",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-0.95",
      "acml_vol": "382896",
      "acml_tr_pbmn": "20200687400",
      "ssts_cntg_qty": "6834",
      "ssts_vol_rlim": "1.78",
      "ssts_tr_pbmn": "359735100",
      "ssts_tr_pbmn_rlim": "1.78",
      "stnd_date1": "0",
      "stnd_date2": "0",
      "avrg_prc": "52639"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```
