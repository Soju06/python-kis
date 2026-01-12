# 국내주식 시간외등락율순위 [국내주식-138]

> [국내주식] 순위분석

국내주식 시간외등락율순위 API입니다. 
한국투자 HTS(eFriend Plus) > [0234] 시간외 등락률순위 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.
최대 30건 확인 가능하며, 다음 조회가 불가합니다.

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `f5c2c9d8-8d11-4a70-8694-1b71e3fc3640` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/ranking/overtime-fluctuation` |
| **Content-Type** | `` |
| **요청 포맷** | `` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID** | `모의투자 미지원`, `FHPST02340000` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-04-12
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
| `tr_id` | 거래ID | String | 13 | Y | FHPST02340000 |
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
| `FID_COND_MRKT_DIV_CODE` | 조건 시장 분류 코드 | String | 2 | Y | 시장구분코드 (J: 주식) |
| `FID_MRKT_CLS_CODE` | 시장 구분 코드 | String | 2 | Y | 공백 입력 |
| `FID_COND_SCR_DIV_CODE` | 조건 화면 분류 코드 | String | 5 | Y | Unique key(20234) |
| `FID_INPUT_ISCD` | 입력 종목코드 | String | 12 | Y | 0000(전체), 0001(코스피), 1001(코스닥) |
| `FID_DIV_CLS_CODE` | 분류 구분 코드 | String | 2 | Y | 1(상한가), 2(상승률), 3(보합),4(하한가),5(하락률) |
| `FID_INPUT_PRICE_1` | 입력 가격1 | String | 12 | Y | 입력값 없을때 전체 (가격 ~) |
| `FID_INPUT_PRICE_2` | 입력 가격2 | String | 12 | Y | 입력값 없을때 전체 (~ 가격) |
| `FID_VOL_CNT` | 거래량 수 | String | 12 | Y | 입력값 없을때 전체 (거래량 ~) |
| `FID_TRGT_CLS_CODE` | 대상 구분 코드 | String | 32 | Y | 공백 입력 |
| `FID_TRGT_EXLS_CLS_CODE` | 대상 제외 구분 코드 | String | 32 | Y | 공백 입력 |

### 요청 예시

```json
fid_cond_mrkt_div_code:J
fid_mrkt_cls_code:
fid_cond_scr_div_code:20234
fid_input_iscd:0000
fid_div_cls_code:2
fid_input_price_1:
fid_input_price_2:
fid_vol_cnt:
fid_trgt_cls_code:
fid_trgt_exls_cls_code:
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
| `output1` | 응답상세 | String |   | Y |  |
| `ovtm_untp_uplm_issu_cnt` | 시간외 단일가 상한 종목 수              | String | 7 | Y |  |
| `ovtm_untp_ascn_issu_cnt` | 시간외 단일가 상승 종목 수          | String | 7 | Y |  |
| `ovtm_untp_stnr_issu_cnt` | 시간외 단일가 보합 종목 수       | String | 7 | Y |  |
| `ovtm_untp_lslm_issu_cnt` | 시간외 단일가 하한 종목 수           | String | 7 | Y |  |
| `ovtm_untp_down_issu_cnt` | 시간외 단일가 하락 종목 수               | String | 7 | Y |  |
| `ovtm_untp_acml_vol` | 시간외 단일가 누적 거래량   | String | 19 | Y |  |
| `ovtm_untp_acml_tr_pbmn` |  시간외 단일가 누적 거래대금  | String | 19 | Y |  |
| `ovtm_untp_exch_vol` | 시간외 단일가 거래소 거래량 | String | 18 | Y |  |
| `ovtm_untp_exch_tr_pbmn` | 시간외 단일가 거래소 거래대금 | String | 18 | Y |  |
| `ovtm_untp_kosdaq_vol` | 시간외 단일가 KOSDAQ 거래량               | String | 18 | Y |  |
| `ovtm_untp_kosdaq_tr_pbmn` | 시간외 단일가 KOSDAQ 거래대금          | String | 18 | Y |  |
| `output2` | 응답상세 | Object |   | Y | array |
| `mksc_shrn_iscd` | 유가증권 단축 종목코드 | String | 9 | Y |  |
| `hts_kor_isnm` | HTS 한글 종목명 | String | 40 | Y |  |
| `ovtm_untp_prpr` | 시간외 단일가 현재가 | String | 10 | Y |  |
| `ovtm_untp_prdy_vrss` | 시간외 단일가 전일 대비 | String | 10 | Y |  |
| `ovtm_untp_prdy_vrss_sign` | 시간외 단일가 전일 대비 부호 | String | 1 | Y |  |
| `ovtm_untp_prdy_ctrt` | 시간외 단일가 전일 대비율 | String | 82 | Y |  |
| `ovtm_untp_askp1` | 시간외 단일가 매도호가1        | String | 10 | Y |  |
| `ovtm_untp_seln_rsqn` | 시간외 단일가 매도 잔량        | String | 12 | Y |  |
| `ovtm_untp_bidp1` | 시간외 단일가 매수호가1        | String | 10 | Y |  |
| `ovtm_untp_shnu_rsqn` | 시간외 단일가 매수 잔량        | String | 12 | Y |  |
| `ovtm_untp_vol` | 시간외 단일가 거래량 | String | 18 | Y |  |
| `ovtm_vrss_acml_vol_rlim` | 시간외 대비 누적 거래량 비중   | String | 52 | Y |  |
| `stck_prpr` | 주식 현재가 | String | 10 | Y |  |
| `acml_vol` | 누적 거래량 | String | 18 | Y |  |
| `bidp` | 매수호가 | String | 10 | Y |  |
| `askp` | 매도호가 | String | 10 | Y |  |

### 응답 예시

```json
{
  "output1": {
    "ovtm_untp_uplm_issu_cnt": "2",
    "ovtm_untp_ascn_issu_cnt": "923",
    "ovtm_untp_stnr_issu_cnt": "634",
    "ovtm_untp_lslm_issu_cnt": "1",
    "ovtm_untp_down_issu_cnt": "731",
    "ovtm_untp_acml_vol": "30215421",
    "ovtm_untp_acml_tr_pbmn": "232960766966",
    "ovtm_untp_exch_vol": "15196593",
    "ovtm_untp_exch_tr_pbmn": "119450793021",
    "ovtm_untp_kosdaq_vol": "15018828",
    "ovtm_untp_kosdaq_tr_pbmn": "113509973945"
  },
  "output2": [
    {
      "mksc_shrn_iscd": "36328K",
      "hts_kor_isnm": "티와이홀딩스우",
      "ovtm_untp_prpr": "5880",
      "ovtm_untp_prdy_vrss": "530",
      "ovtm_untp_prdy_vrss_sign": "1",
      "ovtm_untp_prdy_ctrt": "9.91",
      "ovtm_untp_askp1": "0",
      "ovtm_untp_seln_rsqn": "0",
      "ovtm_untp_bidp1": "5880",
      "ovtm_untp_shnu_rsqn": "13465",
      "ovtm_untp_vol": "19288",
      "ovtm_vrss_acml_vol_rlim": "12.06",
      "stck_prpr": "5480",
      "acml_vol": "159997",
      "bidp": "5470",
      "askp": "5480"
    },
    {
      "mksc_shrn_iscd": "025950",
      "hts_kor_isnm": "동신건설",
      "ovtm_untp_prpr": "21000",
      "ovtm_untp_prdy_vrss": "1890",
      "ovtm_untp_prdy_vrss_sign": "1",
      "ovtm_untp_prdy_ctrt": "9.89",
      "ovtm_untp_askp1": "0",
      "ovtm_untp_seln_rsqn": "0",
      "ovtm_untp_bidp1": "21000",
      "ovtm_untp_shnu_rsqn": "27744",
      "ovtm_untp_vol": "46834",
      "ovtm_vrss_acml_vol_rlim": "12.37",
      "stck_prpr": "21250",
      "acml_vol": "378572",
      "bidp": "21150",
      "askp": "21250"
    },
    {
      "mksc_shrn_iscd": "465610",
      "hts_kor_isnm": "ACE 미국빅테크TOP7 Plus레버리지(합성)",
      "ovtm_untp_prpr": "16595",
      "ovtm_untp_prdy_vrss": "1465",
      "ovtm_untp_prdy_vrss_sign": "2",
      "ovtm_untp_prdy_ctrt": "9.68",
      "ovtm_untp_askp1": "16595",
      "ovtm_untp_seln_rsqn": "22",
      "ovtm_untp_bidp1": "15140",
      "ovtm_untp_shnu_rsqn": "623",
      "ovtm_untp_vol": "2",
      "ovtm_vrss_acml_vol_rlim": "0.01",
      "stck_prpr": "14430",
      "acml_vol": "26559",
      "bidp": "14430",
      "askp": "14450"
    },
    {
      "mksc_shrn_iscd": "201490",
      "hts_kor_isnm": "미투온",
      "ovtm_untp_prpr": "2785",
      "ovtm_untp_prdy_vrss": "245",
      "ovtm_untp_prdy_vrss_sign": "2",
      "ovtm_untp_prdy_ctrt": "9.65",
      "ovtm_untp_askp1": "2785",
      "ovtm_untp_seln_rsqn": "6957",
      "ovtm_untp_bidp1": "2540",
      "ovtm_untp_shnu_rsqn": "3182",
      "ovtm_untp_vol": "43772",
      "ovtm_vrss_acml_vol_rlim": "0.98",
      "stck_prpr": "2870",
      "acml_vol": "4444613",
      "bidp": "2870",
      "askp": "2880"
    },
    {
      "mksc_shrn_iscd": "448540",
      "hts_kor_isnm": "ACE 엔비디아채권혼합블룸버그",
      "ovtm_untp_prpr": "19690",
      "ovtm_untp_prdy_vrss": "1725",
      "ovtm_untp_prdy_vrss_sign": "2",
      "ovtm_untp_prdy_ctrt": "9.60",
      "ovtm_untp_askp1": "18945",
      "ovtm_untp_seln_rsqn": "47",
      "ovtm_untp_bidp1": "17980",
      "ovtm_untp_shnu_rsqn": "210",
      "ovtm_untp_vol": "21",
      "ovtm_vrss_acml_vol_rlim": "0.02",
      "stck_prpr": "17600",
      "acml_vol": "84622",
      "bidp": "17600",
      "askp": "17620"
    },
    {
      "mksc_shrn_iscd": "00499K",
      "hts_kor_isnm": "롯데지주우",
      "ovtm_untp_prpr": "38000",
      "ovtm_untp_prdy_vrss": "3300",
      "ovtm_untp_prdy_vrss_sign": "2",
      "ovtm_untp_prdy_ctrt": "9.51",
      "ovtm_untp_askp1": "38000",
      "ovtm_untp_seln_rsqn": "176",
      "ovtm_untp_bidp1": "34750",
      "ovtm_untp_shnu_rsqn": "60",
      "ovtm_untp_vol": "9",
      "ovtm_vrss_acml_vol_rlim": "64.29",
      "stck_prpr": "35150",
      "acml_vol": "14",
      "bidp": "34750",
      "askp": "35150"
    },
    {
      "mksc_shrn_iscd": "069140",
      "hts_kor_isnm": "누리플랜",
      "ovtm_untp_prpr": "1568",
      "ovtm_untp_prdy_vrss": "133",
      "ovtm_untp_prdy_vrss_sign": "2",
      "ovtm_untp_prdy_ctrt": "9.27",
      "ovtm_untp_askp1": "1552",
      "ovtm_untp_seln_rsqn": "4024",
      "ovtm_untp_bidp1": "1436",
      "ovtm_untp_shnu_rsqn": "2049",
      "ovtm_untp_vol": "1",
      "ovtm_vrss_acml_vol_rlim": "0.00",
      "stck_prpr": "1438",
      "acml_vol": "31055",
      "bidp": "1435",
      "askp": "1438"
    },
    {
      "mksc_shrn_iscd": "007530",
      "hts_kor_isnm": "와이엠",
      "ovtm_untp_prpr": "2900",
      "ovtm_untp_prdy_vrss": "240",
      "ovtm_untp_prdy_vrss_sign": "2",
      "ovtm_untp_prdy_ctrt": "9.02",
      "ovtm_untp_askp1": "2900",
      "ovtm_untp_seln_rsqn": "4398",
      "ovtm_untp_bidp1": "2660",
      "ovtm_untp_shnu_rsqn": "1065",
      "ovtm_untp_vol": "11",
      "ovtm_vrss_acml_vol_rlim": "0.57",
      "stck_prpr": "2710",
      "acml_vol": "1918",
      "bidp": "2680",
      "askp": "2710"
    },
    {
      "mksc_shrn_iscd": "310870",
      "hts_kor_isnm": "디와이씨",
      "ovtm_untp_prpr": "1517",
      "ovtm_untp_prdy_vrss": "124",
      "ovtm_untp_prdy_vrss_sign": "2",
      "ovtm_untp_prdy_ctrt": "8.90",
      "ovtm_untp_askp1": "1516",
      "ovtm_untp_seln_rsqn": "20512",
      "ovtm_untp_bidp1": "1393",
      "ovtm_untp_shnu_rsqn": "1233",
      "ovtm_untp_vol": "5",
      "ovtm_vrss_acml_vol_rlim": "0.02",
      "stck_prpr": "1406",
      "acml_vol": "27844",
      "bidp": "1399",
      "askp": "1406"
    },
    {
      "mksc_shrn_iscd": "019490",
      "hts_kor_isnm": "하이트론",
      "ovtm_untp_prpr": "1350",
      "ovtm_untp_prdy_vrss": "110",
      "ovtm_untp_prdy_vrss_sign": "2",
      "ovtm_untp_prdy_ctrt": "8.87",
      "ovtm_untp_askp1": "1350",
      "ovtm_untp_seln_rsqn": "15196",
      "ovtm_untp_bidp1": "1240",
      "ovtm_untp_shnu_rsqn": "937",
      "ovtm_untp_vol": "22",
      "ovtm_vrss_acml_vol_rlim": "0.07",
      "stck_prpr": "1224",
      "acml_vol": "33488",
      "bidp": "1224",
      "askp": "1230"
    },
    {
      "mksc_shrn_iscd": "115570",
      "hts_kor_isnm": "스타플렉스",
      "ovtm_untp_prpr": "2995",
      "ovtm_untp_prdy_vrss": "225",
      "ovtm_untp_prdy_vrss_sign": "2",
      "ovtm_untp_prdy_ctrt": "8.12",
      "ovtm_untp_askp1": "2985",
      "ovtm_untp_seln_rsqn": "448",
      "ovtm_untp_bidp1": "2540",
      "ovtm_untp_shnu_rsqn": "428",
      "ovtm_untp_vol": "1",
      "ovtm_vrss_acml_vol_rlim": "0.03",
      "stck_prpr": "2720",
      "acml_vol": "3138",
      "bidp": "2710",
      "askp": "2720"
    },
    {
      "mksc_shrn_iscd": "045660",
      "hts_kor_isnm": "에이텍",
      "ovtm_untp_prpr": "15810",
      "ovtm_untp_prdy_vrss": "1130",
      "ovtm_untp_prdy_vrss_sign": "2",
      "ovtm_untp_prdy_ctrt": "7.70",
      "ovtm_untp_askp1": "15810",
      "ovtm_untp_seln_rsqn": "6365",
      "ovtm_untp_bidp1": "15800",
      "ovtm_untp_shnu_rsqn": "1930",
      "ovtm_untp_vol": "93555",
      "ovtm_vrss_acml_vol_rlim": "18.30",
      "stck_prpr": "15430",
      "acml_vol": "511314",
      "bidp": "15430",
      "askp": "15470"
    },
    {
      "mksc_shrn_iscd": "215380",
      "hts_kor_isnm": "우정바이오",
      "ovtm_untp_prpr": "1783",
      "ovtm_untp_prdy_vrss": "127",
      "ovtm_untp_prdy_vrss_sign": "2",
      "ovtm_untp_prdy_ctrt": "7.67",
      "ovtm_untp_askp1": "1787",
      "ovtm_untp_seln_rsqn": "5766",
      "ovtm_untp_bidp1": "1600",
      "ovtm_untp_shnu_rsqn": "500",
      "ovtm_untp_vol": "1",
      "ovtm_vrss_acml_vol_rlim": "0.00",
      "stck_prpr": "1630",
      "acml_vol": "28468",
      "bidp": "1625",
      "askp": "1629"
    },
    {
      "mksc_shrn_iscd": "001130",
      "hts_kor_isnm": "대한제분",
      "ovtm_untp_prpr": "139000",
      "ovtm_untp_prdy_vrss": "9500",
      "ovtm_untp_prdy_vrss_sign": "2",
      "ovtm_untp_prdy_ctrt": "7.34",
      "ovtm_untp_askp1": "138900",
      "ovtm_untp_seln_rsqn": "6",
      "ovtm_untp_bidp1": "129700",
      "ovtm_untp_shnu_rsqn": "8",
      "ovtm_untp_vol": "7",
      "ovtm_vrss_acml_vol_rlim": "0.94",
      "stck_prpr": "131200",
      "acml_vol": "741",
      "bidp": "130000",
      "askp": "131000"
    },
    {
      "mksc_shrn_iscd": "003780",
      "hts_kor_isnm": "진양산업",
      "ovtm_untp_prpr": "6880",
      "ovtm_untp_prdy_vrss": "460",
      "ovtm_untp_prdy_vrss_sign": "2",
      "ovtm_untp_prdy_ctrt": "7.17",
      "ovtm_untp_askp1": "6900",
      "ovtm_untp_seln_rsqn": "1544",
      "ovtm_untp_bidp1": "6310",
      "ovtm_untp_shnu_rsqn": "1396",
      "ovtm_untp_vol": "1",
      "ovtm_vrss_acml_vol_rlim": "0.00",
      "stck_prpr": "6580",
      "acml_vol": "20468",
      "bidp": "6560",
      "askp": "6580"
    },
    {
      "mksc_shrn_iscd": "456490",
      "hts_kor_isnm": "교보14호스팩",
      "ovtm_untp_prpr": "2390",
      "ovtm_untp_prdy_vrss": "155",
      "ovtm_untp_prdy_vrss_sign": "2",
      "ovtm_untp_prdy_ctrt": "6.94",
      "ovtm_untp_askp1": "2390",
      "ovtm_untp_seln_rsqn": "7226",
      "ovtm_untp_bidp1": "2040",
      "ovtm_untp_shnu_rsqn": "6697",
      "ovtm_untp_vol": "9",
      "ovtm_vrss_acml_vol_rlim": "3.15",
      "stck_prpr": "2255",
      "acml_vol": "286",
      "bidp": "2240",
      "askp": "2255"
    },
    {
      "mksc_shrn_iscd": "051630",
      "hts_kor_isnm": "진양화학",
      "ovtm_untp_prpr": "3800",
      "ovtm_untp_prdy_vrss": "235",
      "ovtm_untp_prdy_vrss_sign": "2",
      "ovtm_untp_prdy_ctrt": "6.59",
      "ovtm_untp_askp1": "3695",
      "ovtm_untp_seln_rsqn": "7469",
      "ovtm_untp_bidp1": "3570",
      "ovtm_untp_shnu_rsqn": "1053",
      "ovtm_untp_vol": "36",
      "ovtm_vrss_acml_vol_rlim": "0.37",
      "stck_prpr": "3590",
      "acml_vol": "9742",
      "bidp": "3570",
      "askp": "3590"
    },
    {
      "mksc_shrn_iscd": "049120",
      "hts_kor_isnm": "파인디앤씨",
      "ovtm_untp_prpr": "1420",
      "ovtm_untp_prdy_vrss": "87",
      "ovtm_untp_prdy_vrss_sign": "2",
      "ovtm_untp_prdy_ctrt": "6.53",
      "ovtm_untp_askp1": "1418",
      "ovtm_untp_seln_rsqn": "387",
      "ovtm_untp_bidp1": "1325",
      "ovtm_untp_shnu_rsqn": "31266",
      "ovtm_untp_vol": "10",
      "ovtm_vrss_acml_vol_rlim": "1.10",
      "stck_prpr": "1368",
      "acml_vol": "906",
      "bidp": "1356",
      "askp": "1368"
    },
    {
      "mksc_shrn_iscd": "083470",
      "hts_kor_isnm": "이엠앤아이",
      "ovtm_untp_prpr": "2060",
      "ovtm_untp_prdy_vrss": "125",
      "ovtm_untp_prdy_vrss_sign": "2",
      "ovtm_untp_prdy_ctrt": "6.46",
      "ovtm_untp_askp1": "2055",
      "ovtm_untp_seln_rsqn": "972",
      "ovtm_untp_bidp1": "1841",
      "ovtm_untp_shnu_rsqn": "777",
      "ovtm_untp_vol": "26",
      "ovtm_vrss_acml_vol_rlim": "0.10",
      "stck_prpr": "1896",
      "acml_vol": "26871",
      "bidp": "1884",
      "askp": "1896"
    },
    {
      "mksc_shrn_iscd": "388420",
      "hts_kor_isnm": "KBSTAR 비메모리반도체액티브",
      "ovtm_untp_prpr": "14750",
      "ovtm_untp_prdy_vrss": "885",
      "ovtm_untp_prdy_vrss_sign": "2",
      "ovtm_untp_prdy_ctrt": "6.38",
      "ovtm_untp_askp1": "13870",
      "ovtm_untp_seln_rsqn": "1434",
      "ovtm_untp_bidp1": "12685",
      "ovtm_untp_shnu_rsqn": "220",
      "ovtm_untp_vol": "70",
      "ovtm_vrss_acml_vol_rlim": "0.02",
      "stck_prpr": "13415",
      "acml_vol": "377764",
      "bidp": "13400",
      "askp": "13415"
    },
    {
      "mksc_shrn_iscd": "133820",
      "hts_kor_isnm": "화인베스틸",
      "ovtm_untp_prpr": "1365",
      "ovtm_untp_prdy_vrss": "81",
      "ovtm_untp_prdy_vrss_sign": "2",
      "ovtm_untp_prdy_ctrt": "6.31",
      "ovtm_untp_askp1": "1365",
      "ovtm_untp_seln_rsqn": "8677",
      "ovtm_untp_bidp1": "1284",
      "ovtm_untp_shnu_rsqn": "242",
      "ovtm_untp_vol": "1",
      "ovtm_vrss_acml_vol_rlim": "0.00",
      "stck_prpr": "1285",
      "acml_vol": "20397",
      "bidp": "1285",
      "askp": "1293"
    },
    {
      "mksc_shrn_iscd": "049800",
      "hts_kor_isnm": "우진플라임",
      "ovtm_untp_prpr": "2870",
      "ovtm_untp_prdy_vrss": "170",
      "ovtm_untp_prdy_vrss_sign": "2",
      "ovtm_untp_prdy_ctrt": "6.30",
      "ovtm_untp_askp1": "2875",
      "ovtm_untp_seln_rsqn": "2633",
      "ovtm_untp_bidp1": "2680",
      "ovtm_untp_shnu_rsqn": "1305",
      "ovtm_untp_vol": "798",
      "ovtm_vrss_acml_vol_rlim": "9.24",
      "stck_prpr": "2695",
      "acml_vol": "8638",
      "bidp": "2685",
      "askp": "2690"
    },
    {
      "mksc_shrn_iscd": "045340",
      "hts_kor_isnm": "토탈소프트",
      "ovtm_untp_prpr": "5140",
      "ovtm_untp_prdy_vrss": "300",
      "ovtm_untp_prdy_vrss_sign": "2",
      "ovtm_untp_prdy_ctrt": "6.20",
      "ovtm_untp_askp1": "5150",
      "ovtm_untp_seln_rsqn": "4025",
      "ovtm_untp_bidp1": "5140",
      "ovtm_untp_shnu_rsqn": "8098",
      "ovtm_untp_vol": "5565",
      "ovtm_vrss_acml_vol_rlim": "4.73",
      "stck_prpr": "5030",
      "acml_vol": "117599",
      "bidp": "5000",
      "askp": "5030"
    },
    {
      "mksc_shrn_iscd": "300080",
      "hts_kor_isnm": "플리토",
      "ovtm_untp_prpr": "27550",
      "ovtm_untp_prdy_vrss": "1600",
      "ovtm_untp_prdy_vrss_sign": "2",
      "ovtm_untp_prdy_ctrt": "6.17",
      "ovtm_untp_askp1": "27550",
      "ovtm_untp_seln_rsqn": "5049",
      "ovtm_untp_bidp1": "27250",
      "ovtm_untp_shnu_rsqn": "712",
      "ovtm_untp_vol": "446",
      "ovtm_vrss_acml_vol_rlim": "1.30",
      "stck_prpr": "27000",
      "acml_vol": "34396",
      "bidp": "26950",
      "askp": "27000"
    },
    {
      "mksc_shrn_iscd": "359090",
      "hts_kor_isnm": "씨엔알리서치",
      "ovtm_untp_prpr": "2130",
      "ovtm_untp_prdy_vrss": "120",
      "ovtm_untp_prdy_vrss_sign": "2",
      "ovtm_untp_prdy_ctrt": "5.97",
      "ovtm_untp_askp1": "2130",
      "ovtm_untp_seln_rsqn": "495757",
      "ovtm_untp_bidp1": "2125",
      "ovtm_untp_shnu_rsqn": "129722",
      "ovtm_untp_vol": "1822458",
      "ovtm_vrss_acml_vol_rlim": "7.89",
      "stck_prpr": "2265",
      "acml_vol": "23096436",
      "bidp": "2265",
      "askp": "2270"
    },
    {
      "mksc_shrn_iscd": "442580",
      "hts_kor_isnm": "ARIRANG 글로벌D램반도체iSelect",
      "ovtm_untp_prpr": "19810",
      "ovtm_untp_prdy_vrss": "1080",
      "ovtm_untp_prdy_vrss_sign": "2",
      "ovtm_untp_prdy_ctrt": "5.77",
      "ovtm_untp_askp1": "0",
      "ovtm_untp_seln_rsqn": "0",
      "ovtm_untp_bidp1": "0",
      "ovtm_untp_shnu_rsqn": "0",
      "ovtm_untp_vol": "1",
      "ovtm_vrss_acml_vol_rlim": "0.02",
      "stck_prpr": "18365",
      "acml_vol": "4438",
      "bidp": "18300",
      "askp": "18365"
    },
    {
      "mksc_shrn_iscd": "368970",
      "hts_kor_isnm": "오에스피",
      "ovtm_untp_prpr": "4665",
      "ovtm_untp_prdy_vrss": "225",
      "ovtm_untp_prdy_vrss_sign": "2",
      "ovtm_untp_prdy_ctrt": "5.07",
      "ovtm_untp_askp1": "4565",
      "ovtm_untp_seln_rsqn": "1134",
      "ovtm_untp_bidp1": "4360",
      "ovtm_untp_shnu_rsqn": "1418",
      "ovtm_untp_vol": "21",
      "ovtm_vrss_acml_vol_rlim": "0.32",
      "stck_prpr": "4420",
      "acml_vol": "6585",
      "bidp": "4410",
      "askp": "4420"
    },
    {
      "mksc_shrn_iscd": "079950",
      "hts_kor_isnm": "인베니아",
      "ovtm_untp_prpr": "1150",
      "ovtm_untp_prdy_vrss": "55",
      "ovtm_untp_prdy_vrss_sign": "2",
      "ovtm_untp_prdy_ctrt": "5.02",
      "ovtm_untp_askp1": "1150",
      "ovtm_untp_seln_rsqn": "8268",
      "ovtm_untp_bidp1": "1095",
      "ovtm_untp_shnu_rsqn": "2322",
      "ovtm_untp_vol": "109",
      "ovtm_vrss_acml_vol_rlim": "0.77",
      "stck_prpr": "1084",
      "acml_vol": "14193",
      "bidp": "1084",
      "askp": "1090"
    },
    {
      "mksc_shrn_iscd": "214260",
      "hts_kor_isnm": "라파스",
      "ovtm_untp_prpr": "13970",
      "ovtm_untp_prdy_vrss": "650",
      "ovtm_untp_prdy_vrss_sign": "2",
      "ovtm_untp_prdy_ctrt": "4.88",
      "ovtm_untp_askp1": "13960",
      "ovtm_untp_seln_rsqn": "618",
      "ovtm_untp_bidp1": "13330",
      "ovtm_untp_shnu_rsqn": "468",
      "ovtm_untp_vol": "2",
      "ovtm_vrss_acml_vol_rlim": "0.05",
      "stck_prpr": "13460",
      "acml_vol": "4348",
      "bidp": "13350",
      "askp": "13450"
    },
    {
      "mksc_shrn_iscd": "126640",
      "hts_kor_isnm": "화신정공",
      "ovtm_untp_prpr": "1502",
      "ovtm_untp_prdy_vrss": "69",
      "ovtm_untp_prdy_vrss_sign": "2",
      "ovtm_untp_prdy_ctrt": "4.82",
      "ovtm_untp_askp1": "1499",
      "ovtm_untp_seln_rsqn": "2789",
      "ovtm_untp_bidp1": "1435",
      "ovtm_untp_shnu_rsqn": "5500",
      "ovtm_untp_vol": "1",
      "ovtm_vrss_acml_vol_rlim": "0.00",
      "stck_prpr": "1445",
      "acml_vol": "32541",
      "bidp": "1445",
      "askp": "1450"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```
