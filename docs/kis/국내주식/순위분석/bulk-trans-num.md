# 국내주식 대량체결건수 상위[국내주식-107]

> [국내주식] 순위분석

국내주식 대량체결건수 상위 API입니다.
한국투자 HTS(eFriend Plus) > [0169] 대량체결건수 상위 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.
최대 30건 확인 가능하며, 다음 조회가 불가합니다.

※ 30건 이상의 목록 조회가 필요한 경우, 대안으로 종목조건검색 API를 이용해서 원하는 종목 100개까지 검색할 수 있는 기능을 제공하고 있습니다.
종목조건검색 API는 HTS(efriend Plus) [0110] 조건검색에서 등록 및 서버저장한 나의 조건 목록을 확인할 수 있는 API로,
자세한 사용 방법은 공지사항 - [조건검색 필독] 조건검색 API 이용안내 참고 부탁드립니다.


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `7bdbff93-1334-496f-a9b8-7da6032f7407` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/ranking/bulk-trans-num` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `FHKST190900C0` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-03-15T09:29:56+09:00
- **최종 수정일**: 2025-05-14T14:43:42+09:00

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials Grant 절차를 준용)  법인(Access token 유효기간 3개월, Refresh token 유효기간 1년, OAuth 2.0의 Authorization Code Grant 절차를 준용) |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | FHKST190900C0 |
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
| `fid_aply_rang_prc_2` | 적용 범위 가격2 | String | 18 | Y | ~ 가격 |
| `fid_cond_mrkt_div_code` | 조건 시장 분류 코드 | String | 2 | Y | 시장구분코드 (J:KRX, NX:NXT) |
| `fid_cond_scr_div_code` | 조건 화면 분류 코드 | String | 5 | Y | Unique key(11909) |
| `fid_input_iscd` | 입력 종목코드 | String | 12 | Y | 0000:전체, 0001:거래소, 1001:코스닥, 2001:코스피200, 4001: KRX100 |
| `fid_rank_sort_cls_code` | 순위 정렬 구분 코드 | String | 2 | Y | 0:매수상위, 1:매도상위 |
| `fid_div_cls_code` | 분류 구분 코드 | String | 2 | Y | 0:전체 |
| `fid_input_price_1` | 입력 가격1 | String | 12 | Y | 건별금액 ~ |
| `fid_aply_rang_prc_1` | 적용 범위 가격1 | String | 18 | Y | 가격 ~ |
| `fid_input_iscd_2` | 입력 종목코드2 | String | 8 | Y | 공백:전체종목, 개별종목 조회시 종목코드 (000660) |
| `fid_trgt_exls_cls_code` | 대상 제외 구분 코드 | String | 32 | Y | 0:전체 |
| `fid_trgt_cls_code` | 대상 구분 코드 | String | 32 | Y | 0:전체 |
| `fid_vol_cnt` |  거래량 수 | String | 12 | Y | 거래량 ~ |

### 요청 예시

```json
{
  "output": [
    {
      "mksc_shrn_iscd": "000660",
      "data_rank": "1",
      "hts_kor_isnm": "SK하이닉스",
      "stck_prpr": "162600",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "1400",
      "prdy_ctrt": "0.87",
      "acml_vol": "1593227",
      "shnu_cntg_csnu": "3172",
      "seln_cntg_csnu": "2104",
      "ntby_cnqn": "1068"
    },
    {
      "mksc_shrn_iscd": "207940",
      "data_rank": "2",
      "hts_kor_isnm": "삼성바이오로직스",
      "stck_prpr": "869000",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "43000",
      "prdy_ctrt": "5.21",
      "acml_vol": "140772",
      "shnu_cntg_csnu": "1446",
      "seln_cntg_csnu": "725",
      "ntby_cnqn": "721"
    },
    {
      "mksc_shrn_iscd": "006400",
      "data_rank": "3",
      "hts_kor_isnm": "삼성SDI",
      "stck_prpr": "444000",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "19000",
      "prdy_ctrt": "4.47",
      "acml_vol": "441633",
      "shnu_cntg_csnu": "2167",
      "seln_cntg_csnu": "1488",
      "ntby_cnqn": "679"
    },
    {
      "mksc_shrn_iscd": "007660",
      "data_rank": "4",
      "hts_kor_isnm": "이수페타시스",
      "stck_prpr": "37150",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "3700",
      "prdy_ctrt": "11.06",
      "acml_vol": "7737796",
      "shnu_cntg_csnu": "2920",
      "seln_cntg_csnu": "2361",
      "ntby_cnqn": "559"
    },
    {
      "mksc_shrn_iscd": "112040",
      "data_rank": "5",
      "hts_kor_isnm": "위메이드",
      "stck_prpr": "67100",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "10900",
      "prdy_ctrt": "19.40",
      "acml_vol": "3088002",
      "shnu_cntg_csnu": "2150",
      "seln_cntg_csnu": "1697",
      "ntby_cnqn": "453"
    },
    {
      "mksc_shrn_iscd": "457190",
      "data_rank": "6",
      "hts_kor_isnm": "이수스페셜티케미컬",
      "stck_prpr": "389500",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "47000",
      "prdy_ctrt": "13.72",
      "acml_vol": "671298",
      "shnu_cntg_csnu": "2582",
      "seln_cntg_csnu": "2201",
      "ntby_cnqn": "381"
    },
    {
      "mksc_shrn_iscd": "454910",
      "data_rank": "7",
      "hts_kor_isnm": "두산로보틱스",
      "stck_prpr": "92900",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "5800",
      "prdy_ctrt": "6.66",
      "acml_vol": "1169659",
      "shnu_cntg_csnu": "1214",
      "seln_cntg_csnu": "836",
      "ntby_cnqn": "378"
    },
    {
      "mksc_shrn_iscd": "441540",
      "data_rank": "8",
      "hts_kor_isnm": "HANARO Fn조선해운",
      "stck_prpr": "10610",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "245",
      "prdy_ctrt": "2.36",
      "acml_vol": "2423370",
      "shnu_cntg_csnu": "458",
      "seln_cntg_csnu": "82",
      "ntby_cnqn": "376"
    },
    {
      "mksc_shrn_iscd": "066970",
      "data_rank": "9",
      "hts_kor_isnm": "엘앤에프",
      "stck_prpr": "174700",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "12500",
      "prdy_ctrt": "7.71",
      "acml_vol": "424191",
      "shnu_cntg_csnu": "676",
      "seln_cntg_csnu": "328",
      "ntby_cnqn": "348"
    },
    {
      "mksc_shrn_iscd": "006260",
      "data_rank": "10",
      "hts_kor_isnm": "LS",
      "stck_prpr": "111000",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "6900",
      "prdy_ctrt": "6.63",
      "acml_vol": "475967",
      "shnu_cntg_csnu": "831",
      "seln_cntg_csnu": "510",
      "ntby_cnqn": "321"
    },
    {
      "mksc_shrn_iscd": "247540",
      "data_rank": "11",
      "hts_kor_isnm": "에코프로비엠",
      "stck_prpr": "265500",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "9000",
      "prdy_ctrt": "3.51",
      "acml_vol": "484949",
      "shnu_cntg_csnu": "1320",
      "seln_cntg_csnu": "1004",
      "ntby_cnqn": "316"
    },
    {
      "mksc_shrn_iscd": "051910",
      "data_rank": "12",
      "hts_kor_isnm": "LG화학",
      "stck_prpr": "441500",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "10500",
      "prdy_ctrt": "2.44",
      "acml_vol": "119939",
      "shnu_cntg_csnu": "708",
      "seln_cntg_csnu": "399",
      "ntby_cnqn": "309"
    },
    {
      "mksc_shrn_iscd": "196170",
      "data_rank": "13",
      "hts_kor_isnm": "알테오젠",
      "stck_prpr": "209500",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "5000",
      "prdy_ctrt": "2.44",
      "acml_vol": "1859846",
      "shnu_cntg_csnu": "3637",
      "seln_cntg_csnu": "3379",
      "ntby_cnqn": "258"
    },
    {
      "mksc_shrn_iscd": "042660",
      "data_rank": "14",
      "hts_kor_isnm": "한화오션",
      "stck_prpr": "28850",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "1850",
      "prdy_ctrt": "6.85",
      "acml_vol": "3370897",
      "shnu_cntg_csnu": "1112",
      "seln_cntg_csnu": "856",
      "ntby_cnqn": "256"
    },
    {
      "mksc_shrn_iscd": "000270",
      "data_rank": "15",
      "hts_kor_isnm": "기아",
      "stck_prpr": "127500",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "2500",
      "prdy_ctrt": "2.00",
      "acml_vol": "866368",
      "shnu_cntg_csnu": "1342",
      "seln_cntg_csnu": "1110",
      "ntby_cnqn": "232"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
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
| `prdy_vrss_sign` | 전일 대비 부호 | String | 1 | Y |  |
| `prdy_vrss` | 전일 대비 | String | 10 | Y |  |
| `prdy_ctrt` | 전일 대비율 | String | 82 | Y |  |
| `acml_vol` | 누적 거래량 | String | 18 | Y |  |
| `shnu_cntg_csnu` | 매수2 체결 건수 | String | 10 | Y |  |
| `seln_cntg_csnu` | 매도 체결 건수 | String | 10 | Y |  |
| `ntby_cnqn` | 순매수 체결량 | String | 18 | Y |  |

### 응답 예시

```json
{
  "output": [
    {
      "mksc_shrn_iscd": "000660",
      "data_rank": "1",
      "hts_kor_isnm": "SK하이닉스",
      "stck_prpr": "162600",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "1400",
      "prdy_ctrt": "0.87",
      "acml_vol": "1593227",
      "shnu_cntg_csnu": "3172",
      "seln_cntg_csnu": "2104",
      "ntby_cnqn": "1068"
    },
    {
      "mksc_shrn_iscd": "207940",
      "data_rank": "2",
      "hts_kor_isnm": "삼성바이오로직스",
      "stck_prpr": "869000",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "43000",
      "prdy_ctrt": "5.21",
      "acml_vol": "140772",
      "shnu_cntg_csnu": "1446",
      "seln_cntg_csnu": "725",
      "ntby_cnqn": "721"
    },
    {
      "mksc_shrn_iscd": "006400",
      "data_rank": "3",
      "hts_kor_isnm": "삼성SDI",
      "stck_prpr": "444000",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "19000",
      "prdy_ctrt": "4.47",
      "acml_vol": "441633",
      "shnu_cntg_csnu": "2167",
      "seln_cntg_csnu": "1488",
      "ntby_cnqn": "679"
    },
    {
      "mksc_shrn_iscd": "007660",
      "data_rank": "4",
      "hts_kor_isnm": "이수페타시스",
      "stck_prpr": "37150",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "3700",
      "prdy_ctrt": "11.06",
      "acml_vol": "7737796",
      "shnu_cntg_csnu": "2920",
      "seln_cntg_csnu": "2361",
      "ntby_cnqn": "559"
    },
    {
      "mksc_shrn_iscd": "112040",
      "data_rank": "5",
      "hts_kor_isnm": "위메이드",
      "stck_prpr": "67100",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "10900",
      "prdy_ctrt": "19.40",
      "acml_vol": "3088002",
      "shnu_cntg_csnu": "2150",
      "seln_cntg_csnu": "1697",
      "ntby_cnqn": "453"
    },
    {
      "mksc_shrn_iscd": "457190",
      "data_rank": "6",
      "hts_kor_isnm": "이수스페셜티케미컬",
      "stck_prpr": "389500",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "47000",
      "prdy_ctrt": "13.72",
      "acml_vol": "671298",
      "shnu_cntg_csnu": "2582",
      "seln_cntg_csnu": "2201",
      "ntby_cnqn": "381"
    },
    {
      "mksc_shrn_iscd": "454910",
      "data_rank": "7",
      "hts_kor_isnm": "두산로보틱스",
      "stck_prpr": "92900",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "5800",
      "prdy_ctrt": "6.66",
      "acml_vol": "1169659",
      "shnu_cntg_csnu": "1214",
      "seln_cntg_csnu": "836",
      "ntby_cnqn": "378"
    },
    {
      "mksc_shrn_iscd": "441540",
      "data_rank": "8",
      "hts_kor_isnm": "HANARO Fn조선해운",
      "stck_prpr": "10610",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "245",
      "prdy_ctrt": "2.36",
      "acml_vol": "2423370",
      "shnu_cntg_csnu": "458",
      "seln_cntg_csnu": "82",
      "ntby_cnqn": "376"
    },
    {
      "mksc_shrn_iscd": "066970",
      "data_rank": "9",
      "hts_kor_isnm": "엘앤에프",
      "stck_prpr": "174700",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "12500",
      "prdy_ctrt": "7.71",
      "acml_vol": "424191",
      "shnu_cntg_csnu": "676",
      "seln_cntg_csnu": "328",
      "ntby_cnqn": "348"
    },
    {
      "mksc_shrn_iscd": "006260",
      "data_rank": "10",
      "hts_kor_isnm": "LS",
      "stck_prpr": "111000",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "6900",
      "prdy_ctrt": "6.63",
      "acml_vol": "475967",
      "shnu_cntg_csnu": "831",
      "seln_cntg_csnu": "510",
      "ntby_cnqn": "321"
    },
    {
      "mksc_shrn_iscd": "247540",
      "data_rank": "11",
      "hts_kor_isnm": "에코프로비엠",
      "stck_prpr": "265500",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "9000",
      "prdy_ctrt": "3.51",
      "acml_vol": "484949",
      "shnu_cntg_csnu": "1320",
      "seln_cntg_csnu": "1004",
      "ntby_cnqn": "316"
    },
    {
      "mksc_shrn_iscd": "051910",
      "data_rank": "12",
      "hts_kor_isnm": "LG화학",
      "stck_prpr": "441500",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "10500",
      "prdy_ctrt": "2.44",
      "acml_vol": "119939",
      "shnu_cntg_csnu": "708",
      "seln_cntg_csnu": "399",
      "ntby_cnqn": "309"
    },
    {
      "mksc_shrn_iscd": "196170",
      "data_rank": "13",
      "hts_kor_isnm": "알테오젠",
      "stck_prpr": "209500",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "5000",
      "prdy_ctrt": "2.44",
      "acml_vol": "1859846",
      "shnu_cntg_csnu": "3637",
      "seln_cntg_csnu": "3379",
      "ntby_cnqn": "258"
    },
    {
      "mksc_shrn_iscd": "042660",
      "data_rank": "14",
      "hts_kor_isnm": "한화오션",
      "stck_prpr": "28850",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "1850",
      "prdy_ctrt": "6.85",
      "acml_vol": "3370897",
      "shnu_cntg_csnu": "1112",
      "seln_cntg_csnu": "856",
      "ntby_cnqn": "256"
    },
    {
      "mksc_shrn_iscd": "000270",
      "data_rank": "15",
      "hts_kor_isnm": "기아",
      "stck_prpr": "127500",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "2500",
      "prdy_ctrt": "2.00",
      "acml_vol": "866368",
      "shnu_cntg_csnu": "1342",
      "seln_cntg_csnu": "1110",
      "ntby_cnqn": "232"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```

