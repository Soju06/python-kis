# 국내주식 관심종목등록 상위[v1_국내주식-102]

> [국내주식] 순위분석

국내주식 관심종목등록 상위 API입니다.
한국투자 HTS(eFriend Plus) > [0180] 관심종목등록상위 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.
최대 30건 확인 가능하며, 다음 조회가 불가합니다.

※ 30건 이상의 목록 조회가 필요한 경우, 대안으로 종목조건검색 API를 이용해서 원하는 종목 100개까지 검색할 수 있는 기능을 제공하고 있습니다.
종목조건검색 API는 HTS(efriend Plus) [0110] 조건검색에서 등록 및 서버저장한 나의 조건 목록을 확인할 수 있는 API로,
자세한 사용 방법은 공지사항 - [조건검색 필독] 조건검색 API 이용안내 참고 부탁드립니다.


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `f2921c05-8b93-4a13-a0d8-6132be010066` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/ranking/top-interest-stock` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `FHPST01800000` |
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
| `tr_id` | 거래ID | String | 13 | Y | FHPST01800000 |
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
| `fid_input_iscd_2` | 입력 필수값2 | String | 12 | Y | 000000 : 필수입력값 |
| `fid_cond_mrkt_div_code` | 조건 시장 분류 코드 | String | 2 | Y | 시장구분코드 (J:KRX, NX:NXT) |
| `fid_cond_scr_div_code` | 조건 화면 분류 코드 | String | 5 | Y | Unique key(20180) |
| `fid_input_iscd` | 업종 코드 | String | 12 | Y | 0000:전체, 0001:거래소, 1001:코스닥, 2001:코스피200 |
| `fid_trgt_cls_code` | 대상 구분 코드 | String | 2 | Y | 0 : 전체 |
| `fid_trgt_exls_cls_code` | 대상 제외 구분 코드 | String | 2 | Y | 0 : 전체 |
| `fid_input_price_1` | 입력 가격1 | String | 2 | Y | 입력값 없을때 전체 (가격 ~) |
| `fid_input_price_2` | 입력 가격2 | String | 2 | Y | 입력값 없을때 전체 (~ 가격) |
| `fid_vol_cnt` | 거래량 수 | String | 12 | Y | 입력값 없을때 전체 (거래량 ~) |
| `fid_div_cls_code` | 분류 구분 코드 | String | 12 | Y | 0: 전체 1: 관리종목 2: 투자주의 3: 투자경고 4: 투자위험예고 5: 투자위험 6: 보통주 7: 우선주 |
| `fid_input_cnt_1` | 순위 입력값 | String | 10 | Y | 순위검색 입력값(1: 1위부터, 10:10위부터) |

### 요청 예시

```json
{
  "fid_cond_mrkt_div_code": "J",
  "fid_cond_scr_div_code": "20180",
  "fid_input_iscd": "0000",
  "fid_trgt_exls_cls_code": "0",
  "fid_trgt_cls_code": "0",
  "fid_input_price_1": "",
  "fid_input_price_2": "",
  "fid_vol_cnt": "",
  "fid_div_cls_code": "0",
  "fid_input_iscd_2": "000000",
  "fid_input_cnt_1": "1"
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
| `mrkt_div_cls_name` | 시장 분류 구분 명 | String | 40 | Y |  |
| `mksc_shrn_iscd` | 유가증권 단축 종목코드 | String | 9 | Y |  |
| `hts_kor_isnm` | HTS 한글 종목명 | String | 40 | Y |  |
| `stck_prpr` | 주식 현재가 | String | 10 | Y |  |
| `prdy_vrss` | 전일 대비 | String | 10 | Y |  |
| `prdy_vrss_sign` | 전일 대비 부호 | String | 1 | Y |  |
| `prdy_ctrt` | 전일 대비율 | String | 82 | Y |  |
| `acml_vol` | 누적 거래량 | String | 18 | Y |  |
| `acml_tr_pbmn` | 누적 거래 대금 | String | 18 | Y |  |
| `askp` | 매도호가 | String | 10 | Y |  |
| `bidp` | 매수호가 | String | 10 | Y |  |
| `data_rank` | 데이터 순위 | String | 10 | Y |  |
| `inter_issu_reg_csnu` | 관심 종목 등록 건수 | String | 10 | Y |  |

### 응답 예시

```json
{
  "output": [
    {
      "mrkt_div_cls_name": "코스피",
      "mksc_shrn_iscd": "005930",
      "hts_kor_isnm": "삼성전자",
      "stck_prpr": "72700",
      "prdy_vrss": "400",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "0.55",
      "acml_vol": "4160099",
      "acml_tr_pbmn": "302366528800",
      "askp": "72800",
      "bidp": "72700",
      "data_rank": "1",
      "inter_issu_reg_csnu": "4316153"
    },
    {
      "mrkt_div_cls_name": "코스피",
      "mksc_shrn_iscd": "000660",
      "hts_kor_isnm": "SK하이닉스",
      "stck_prpr": "162900",
      "prdy_vrss": "1700",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "1.05",
      "acml_vol": "990751",
      "acml_tr_pbmn": "160519591000",
      "askp": "162900",
      "bidp": "162800",
      "data_rank": "2",
      "inter_issu_reg_csnu": "1173540"
    },
    {
      "mrkt_div_cls_name": "코스피",
      "mksc_shrn_iscd": "373220",
      "hts_kor_isnm": "LG에너지솔루션",
      "stck_prpr": "404500",
      "prdy_vrss": "6000",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "1.51",
      "acml_vol": "46060",
      "acml_tr_pbmn": "18601165500",
      "askp": "404500",
      "bidp": "404000",
      "data_rank": "3",
      "inter_issu_reg_csnu": "932490"
    },
    {
      "mrkt_div_cls_name": "코스피",
      "mksc_shrn_iscd": "207940",
      "hts_kor_isnm": "삼성바이오로직스",
      "stck_prpr": "869000",
      "prdy_vrss": "43000",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "5.21",
      "acml_vol": "102027",
      "acml_tr_pbmn": "87895574000",
      "askp": "869000",
      "bidp": "868000",
      "data_rank": "4",
      "inter_issu_reg_csnu": "587897"
    },
    {
      "mrkt_div_cls_name": "코스피",
      "mksc_shrn_iscd": "005380",
      "hts_kor_isnm": "현대차",
      "stck_prpr": "247000",
      "prdy_vrss": "3500",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "1.44",
      "acml_vol": "313743",
      "acml_tr_pbmn": "76616945500",
      "askp": "247000",
      "bidp": "246500",
      "data_rank": "5",
      "inter_issu_reg_csnu": "515079"
    },
    {
      "mrkt_div_cls_name": "코스피",
      "mksc_shrn_iscd": "005935",
      "hts_kor_isnm": "삼성전자우",
      "stck_prpr": "62400",
      "prdy_vrss": "400",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "0.65",
      "acml_vol": "222773",
      "acml_tr_pbmn": "13898135300",
      "askp": "62400",
      "bidp": "62300",
      "data_rank": "6",
      "inter_issu_reg_csnu": "510190"
    },
    {
      "mrkt_div_cls_name": "코스피",
      "mksc_shrn_iscd": "000270",
      "hts_kor_isnm": "기아",
      "stck_prpr": "127600",
      "prdy_vrss": "2600",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "2.08",
      "acml_vol": "601506",
      "acml_tr_pbmn": "75893598900",
      "askp": "127800",
      "bidp": "127600",
      "data_rank": "7",
      "inter_issu_reg_csnu": "502555"
    },
    {
      "mrkt_div_cls_name": "코스피",
      "mksc_shrn_iscd": "068270",
      "hts_kor_isnm": "셀트리온",
      "stck_prpr": "182300",
      "prdy_vrss": "1500",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "0.83",
      "acml_vol": "269213",
      "acml_tr_pbmn": "49066824700",
      "askp": "182300",
      "bidp": "182200",
      "data_rank": "8",
      "inter_issu_reg_csnu": "394234"
    },
    {
      "mrkt_div_cls_name": "코스피",
      "mksc_shrn_iscd": "005490",
      "hts_kor_isnm": "POSCO홀딩스",
      "stck_prpr": "437500",
      "prdy_vrss": "2500",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "0.57",
      "acml_vol": "164953",
      "acml_tr_pbmn": "71803903500",
      "askp": "437500",
      "bidp": "437000",
      "data_rank": "9",
      "inter_issu_reg_csnu": "367885"
    },
    {
      "mrkt_div_cls_name": "코스피",
      "mksc_shrn_iscd": "105560",
      "hts_kor_isnm": "KB금융",
      "stck_prpr": "73300",
      "prdy_vrss": "-2900",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-3.81",
      "acml_vol": "1098724",
      "acml_tr_pbmn": "80094554600",
      "askp": "73300",
      "bidp": "73200",
      "data_rank": "10",
      "inter_issu_reg_csnu": "307475"
    },
    {
      "mrkt_div_cls_name": "코스피",
      "mksc_shrn_iscd": "051910",
      "hts_kor_isnm": "LG화학",
      "stck_prpr": "439500",
      "prdy_vrss": "8500",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "1.97",
      "acml_vol": "76206",
      "acml_tr_pbmn": "33300157500",
      "askp": "440000",
      "bidp": "439500",
      "data_rank": "11",
      "inter_issu_reg_csnu": "304253"
    },
    {
      "mrkt_div_cls_name": "코스피",
      "mksc_shrn_iscd": "035420",
      "hts_kor_isnm": "NAVER",
      "stck_prpr": "184400",
      "prdy_vrss": "-1700",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-0.91",
      "acml_vol": "381339",
      "acml_tr_pbmn": "70460804100",
      "askp": "184400",
      "bidp": "184300",
      "data_rank": "12",
      "inter_issu_reg_csnu": "302242"
    },
    {
      "mrkt_div_cls_name": "코스피",
      "mksc_shrn_iscd": "006400",
      "hts_kor_isnm": "삼성SDI",
      "stck_prpr": "435500",
      "prdy_vrss": "10500",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "2.47",
      "acml_vol": "243109",
      "acml_tr_pbmn": "105190587500",
      "askp": "435500",
      "bidp": "435000",
      "data_rank": "13",
      "inter_issu_reg_csnu": "292249"
    },
    {
      "mrkt_div_cls_name": "코스피",
      "mksc_shrn_iscd": "028260",
      "hts_kor_isnm": "삼성물산",
      "stck_prpr": "152000",
      "prdy_vrss": "-2100",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-1.36",
      "acml_vol": "328745",
      "acml_tr_pbmn": "49869673600",
      "askp": "152100",
      "bidp": "152000",
      "data_rank": "14",
      "inter_issu_reg_csnu": "285997"
    },
    {
      "mrkt_div_cls_name": "코스피",
      "mksc_shrn_iscd": "055550",
      "hts_kor_isnm": "신한지주",
      "stck_prpr": "48550",
      "prdy_vrss": "-1050",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-2.12",
      "acml_vol": "962127",
      "acml_tr_pbmn": "46386742150",
      "askp": "48600",
      "bidp": "48550",
      "data_rank": "15",
      "inter_issu_reg_csnu": "254329"
    },
    {
      "mrkt_div_cls_name": "코스피",
      "mksc_shrn_iscd": "012330",
      "hts_kor_isnm": "현대모비스",
      "stck_prpr": "270000",
      "prdy_vrss": "1000",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "0.37",
      "acml_vol": "88500",
      "acml_tr_pbmn": "23747976000",
      "askp": "270000",
      "bidp": "269500",
      "data_rank": "16",
      "inter_issu_reg_csnu": "251932"
    },
    {
      "mrkt_div_cls_name": "코스닥",
      "mksc_shrn_iscd": "247540",
      "hts_kor_isnm": "에코프로비엠",
      "stck_prpr": "264000",
      "prdy_vrss": "7500",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "2.92",
      "acml_vol": "338076",
      "acml_tr_pbmn": "89005916500",
      "askp": "264500",
      "bidp": "264000",
      "data_rank": "17",
      "inter_issu_reg_csnu": "250860"
    },
    {
      "mrkt_div_cls_name": "코스피",
      "mksc_shrn_iscd": "003670",
      "hts_kor_isnm": "포스코퓨처엠",
      "stck_prpr": "317500",
      "prdy_vrss": "1000",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "0.32",
      "acml_vol": "113774",
      "acml_tr_pbmn": "36129162000",
      "askp": "318000",
      "bidp": "317500",
      "data_rank": "18",
      "inter_issu_reg_csnu": "245171"
    },
    {
      "mrkt_div_cls_name": "코스피",
      "mksc_shrn_iscd": "035720",
      "hts_kor_isnm": "카카오",
      "stck_prpr": "53100",
      "prdy_vrss": "-1000",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-1.85",
      "acml_vol": "432969",
      "acml_tr_pbmn": "23106491000",
      "askp": "53200",
      "bidp": "53100",
      "data_rank": "19",
      "inter_issu_reg_csnu": "240828"
    },
    {
      "mrkt_div_cls_name": "코스피",
      "mksc_shrn_iscd": "032830",
      "hts_kor_isnm": "삼성생명",
      "stck_prpr": "96100",
      "prdy_vrss": "-3000",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-3.03",
      "acml_vol": "264230",
      "acml_tr_pbmn": "25155009400",
      "askp": "96100",
      "bidp": "96000",
      "data_rank": "20",
      "inter_issu_reg_csnu": "198200"
    },
    {
      "mrkt_div_cls_name": "코스피",
      "mksc_shrn_iscd": "086790",
      "hts_kor_isnm": "하나금융지주",
      "stck_prpr": "61800",
      "prdy_vrss": "-300",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-0.48",
      "acml_vol": "819659",
      "acml_tr_pbmn": "50061945600",
      "askp": "61900",
      "bidp": "61800",
      "data_rank": "21",
      "inter_issu_reg_csnu": "181553"
    },
    {
      "mrkt_div_cls_name": "코스피",
      "mksc_shrn_iscd": "138040",
      "hts_kor_isnm": "메리츠금융지주",
      "stck_prpr": "82900",
      "prdy_vrss": "-300",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-0.36",
      "acml_vol": "196602",
      "acml_tr_pbmn": "16315808200",
      "askp": "82900",
      "bidp": "82800",
      "data_rank": "22",
      "inter_issu_reg_csnu": "169206"
    },
    {
      "mrkt_div_cls_name": "코스피",
      "mksc_shrn_iscd": "066570",
      "hts_kor_isnm": "LG전자",
      "stck_prpr": "97300",
      "prdy_vrss": "-1600",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-1.62",
      "acml_vol": "171039",
      "acml_tr_pbmn": "16760736900",
      "askp": "97300",
      "bidp": "97200",
      "data_rank": "23",
      "inter_issu_reg_csnu": "161848"
    },
    {
      "mrkt_div_cls_name": "코스닥",
      "mksc_shrn_iscd": "086520",
      "hts_kor_isnm": "에코프로",
      "stck_prpr": "607000",
      "prdy_vrss": "6000",
      "prdy_vrss_sign": "2",
      "prdy_ctrt": "1.00",
      "acml_vol": "69604",
      "acml_tr_pbmn": "42222166000",
      "askp": "608000",
      "bidp": "607000",
      "data_rank": "24",
      "inter_issu_reg_csnu": "160032"
    },
    {
      "mrkt_div_cls_name": "코스피",
      "mksc_shrn_iscd": "015760",
      "hts_kor_isnm": "한국전력",
      "stck_prpr": "24400",
      "prdy_vrss": "-450",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-1.81",
      "acml_vol": "916977",
      "acml_tr_pbmn": "22547360200",
      "askp": "24450",
      "bidp": "24400",
      "data_rank": "25",
      "inter_issu_reg_csnu": "159528"
    },
    {
      "mrkt_div_cls_name": "코스피",
      "mksc_shrn_iscd": "003550",
      "hts_kor_isnm": "LG",
      "stck_prpr": "90300",
      "prdy_vrss": "-4600",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-4.85",
      "acml_vol": "256392",
      "acml_tr_pbmn": "23167295200",
      "askp": "90400",
      "bidp": "90300",
      "data_rank": "26",
      "inter_issu_reg_csnu": "149279"
    },
    {
      "mrkt_div_cls_name": "코스피",
      "mksc_shrn_iscd": "000810",
      "hts_kor_isnm": "삼성화재",
      "stck_prpr": "306000",
      "prdy_vrss": "-3500",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-1.13",
      "acml_vol": "42010",
      "acml_tr_pbmn": "12806652000",
      "askp": "306500",
      "bidp": "306000",
      "data_rank": "27",
      "inter_issu_reg_csnu": "146625"
    },
    {
      "mrkt_div_cls_name": "코스피",
      "mksc_shrn_iscd": "034730",
      "hts_kor_isnm": "SK",
      "stck_prpr": "185100",
      "prdy_vrss": "-2200",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-1.17",
      "acml_vol": "33965",
      "acml_tr_pbmn": "6295027100",
      "askp": "185100",
      "bidp": "185000",
      "data_rank": "28",
      "inter_issu_reg_csnu": "137100"
    },
    {
      "mrkt_div_cls_name": "코스피",
      "mksc_shrn_iscd": "323410",
      "hts_kor_isnm": "카카오뱅크",
      "stck_prpr": "27950",
      "prdy_vrss": "-450",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-1.58",
      "acml_vol": "328422",
      "acml_tr_pbmn": "9190884150",
      "askp": "27950",
      "bidp": "27900",
      "data_rank": "29",
      "inter_issu_reg_csnu": "135444"
    },
    {
      "mrkt_div_cls_name": "코스닥",
      "mksc_shrn_iscd": "028300",
      "hts_kor_isnm": "HLB",
      "stck_prpr": "102200",
      "prdy_vrss": "-200",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-0.20",
      "acml_vol": "633944",
      "acml_tr_pbmn": "64667743200",
      "askp": "102200",
      "bidp": "102100",
      "data_rank": "30",
      "inter_issu_reg_csnu": "133952"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```

