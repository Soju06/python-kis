# 국내주식 당사매매종목 상위[v1_국내주식-104]

> [국내주식] 순위분석

국내주식 당사매매종목 상위 API입니다.
한국투자 HTS(eFriend Plus) > [0186] 당사매매종목 상위 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.
최대 30건 확인 가능하며, 다음 조회가 불가합니다.

※ 30건 이상의 목록 조회가 필요한 경우, 대안으로 종목조건검색 API를 이용해서 원하는 종목 100개까지 검색할 수 있는 기능을 제공하고 있습니다.
종목조건검색 API는 HTS(efriend Plus) [0110] 조건검색에서 등록 및 서버저장한 나의 조건 목록을 확인할 수 있는 API로,
자세한 사용 방법은 공지사항 - [조건검색 필독] 조건검색 API 이용안내 참고 부탁드립니다.

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `c02e3f30-5d71-4156-a039-3976f4d485f8` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/ranking/traded-by-company` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID** | `모의투자 미지원`, `FHPST01860000` |

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
| `tr_id` | 거래ID | String | 13 | Y | FHPST01860000 |
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
| `fid_trgt_exls_cls_code` | 대상 제외 구분 코드 | String | 32 | Y | 0: 전체 |
| `fid_cond_mrkt_div_code` | 조건 시장 분류 코드 | String | 2 | Y | 시장구분코드 (J:KRX, NX:NXT) |
| `fid_cond_scr_div_code` | 조건 화면 분류 코드 | String | 5 | Y | Unique key(20186) |
| `fid_div_cls_code` | 분류 구분 코드 | String | 2 | Y | 0:전체, 1:관리종목, 2:투자주의, 3:투자경고, 4:투자위험예고, 5:투자위험, 6:보통주, 7:우선주 |
| `fid_rank_sort_cls_code` | 순위 정렬 구분 코드 | String | 2 | Y | 0:매도상위,1:매수상위 |
| `fid_input_date_1` | 입력 날짜1 | String | 10 | Y | 기간~ |
| `fid_input_date_2` | 입력 날짜2 | String | 10 | Y | ~기간 |
| `fid_input_iscd` | 입력 종목코드 | String | 12 | Y | 0000:전체, 0001:거래소, 1001:코스닥, 2001:코스피200, 4001: KRX100 |
| `fid_trgt_cls_code` | 대상 구분 코드 | String | 32 | Y | 0: 전체 |
| `fid_aply_rang_vol` | 적용 범위 거래량 | String | 18 | Y | 0: 전체, 100: 100주 이상 |
| `fid_aply_rang_prc_2` | 적용 범위 가격2 | String | 18 | Y | ~ 가격 |
| `fid_aply_rang_prc_1` | 적용 범위 가격1 | String | 18 | Y | 가격 ~ |

### 요청 예시

```json
{
  "fid_cond_mrkt_div_code": "J",
  "fid_cond_scr_div_code": "20186",
  "fid_div_cls_code": "0",
  "fid_rank_sort_cls_code": "0",
  "fid_input_date_1": "20240314",
  "fid_input_date_2": "20240315",
  "fid_input_iscd": "0000",
  "fid_trgt_cls_code": "0",
  "fid_trgt_exls_cls_code": "0",
  "fid_aply_rang_prc_1": "",
  "fid_aply_rang_prc_2": "",
  "fid_aply_rang_vol": "0"
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
| `data_rank` | 데이터 순위 | String | 10 | Y |  |
| `mksc_shrn_iscd` | 유가증권 단축 종목코드 | String | 9 | Y |  |
| `hts_kor_isnm` | HTS 한글 종목명 | String | 40 | Y |  |
| `stck_prpr` | 주식 현재가 | String | 10 | Y |  |
| `prdy_vrss_sign` | 전일 대비 부호 | String | 1 | Y |  |
| `prdy_vrss` | 전일 대비 | String | 10 | Y |  |
| `prdy_ctrt` | 전일 대비율 | String | 82 | Y |  |
| `acml_vol` | 누적 거래량 | String | 18 | Y |  |
| `acml_tr_pbmn` | 누적 거래 대금 | String | 18 | Y |  |
| `seln_cnqn_smtn` | 매도 체결량 합계 | String | 18 | Y |  |
| `shnu_cnqn_smtn` | 매수2 체결량 합계 | String | 18 | Y |  |
| `ntby_cnqn` | 순매수 체결량 | String | 18 | Y |  |

### 응답 예시

```json
{
  "output": [
    {
      "data_rank": "1",
      "mksc_shrn_iscd": "Q530036",
      "hts_kor_isnm": "삼성 인버스 2X WTI원유 선물 ETN",
      "stck_prpr": "92",
      "prdy_vrss_sign": "3",
      "prdy_vrss": "0",
      "prdy_ctrt": "0.00",
      "acml_vol": "5800370",
      "acml_tr_pbmn": "533513365",
      "seln_cnqn_smtn": "8248448",
      "shnu_cnqn_smtn": "4633200",
      "ntby_cnqn": "-3615248"
    },
    {
      "data_rank": "2",
      "mksc_shrn_iscd": "252670",
      "hts_kor_isnm": "KODEX 200선물인버스2X",
      "stck_prpr": "2175",
      "prdy_vrss_sign": "5",
      "prdy_vrss": "-5",
      "prdy_ctrt": "-0.23",
      "acml_vol": "55781783",
      "acml_tr_pbmn": "121550061085",
      "seln_cnqn_smtn": "27416314",
      "shnu_cnqn_smtn": "25991495",
      "ntby_cnqn": "-1424819"
    },
    {
      "data_rank": "3",
      "mksc_shrn_iscd": "025320",
      "hts_kor_isnm": "시노펙스",
      "stck_prpr": "10860",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "830",
      "prdy_ctrt": "8.28",
      "acml_vol": "4687707",
      "acml_tr_pbmn": "49125642180",
      "seln_cnqn_smtn": "5824623",
      "shnu_cnqn_smtn": "4909381",
      "ntby_cnqn": "-915242"
    },
    {
      "data_rank": "4",
      "mksc_shrn_iscd": "290690",
      "hts_kor_isnm": "소룩스",
      "stck_prpr": "2550",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "80",
      "prdy_ctrt": "3.24",
      "acml_vol": "2932021",
      "acml_tr_pbmn": "7432512210",
      "seln_cnqn_smtn": "1297638",
      "shnu_cnqn_smtn": "485714",
      "ntby_cnqn": "-811924"
    },
    {
      "data_rank": "5",
      "mksc_shrn_iscd": "453850",
      "hts_kor_isnm": "ACE 미국30년국채액티브(H)",
      "stck_prpr": "8555",
      "prdy_vrss_sign": "5",
      "prdy_vrss": "-15",
      "prdy_ctrt": "-0.18",
      "acml_vol": "535802",
      "acml_tr_pbmn": "4573586665",
      "seln_cnqn_smtn": "1416392",
      "shnu_cnqn_smtn": "622450",
      "ntby_cnqn": "-793942"
    },
    {
      "data_rank": "6",
      "mksc_shrn_iscd": "217620",
      "hts_kor_isnm": "디딤이앤에프",
      "stck_prpr": "422",
      "prdy_vrss_sign": "5",
      "prdy_vrss": "-19",
      "prdy_ctrt": "-4.31",
      "acml_vol": "4011940",
      "acml_tr_pbmn": "1603037358",
      "seln_cnqn_smtn": "3775356",
      "shnu_cnqn_smtn": "3104696",
      "ntby_cnqn": "-670660"
    },
    {
      "data_rank": "7",
      "mksc_shrn_iscd": "122630",
      "hts_kor_isnm": "KODEX 레버리지",
      "stck_prpr": "18620",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "75",
      "prdy_ctrt": "0.40",
      "acml_vol": "8919461",
      "acml_tr_pbmn": "165416410545",
      "seln_cnqn_smtn": "4396350",
      "shnu_cnqn_smtn": "3776614",
      "ntby_cnqn": "-619736"
    },
    {
      "data_rank": "8",
      "mksc_shrn_iscd": "900300",
      "hts_kor_isnm": "오가닉티코스메틱",
      "stck_prpr": "79",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "2",
      "prdy_ctrt": "2.60",
      "acml_vol": "1282716",
      "acml_tr_pbmn": "99560857",
      "seln_cnqn_smtn": "813110",
      "shnu_cnqn_smtn": "263052",
      "ntby_cnqn": "-550058"
    },
    {
      "data_rank": "9",
      "mksc_shrn_iscd": "003620",
      "hts_kor_isnm": "KG모빌리티",
      "stck_prpr": "7850",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "10",
      "prdy_ctrt": "0.13",
      "acml_vol": "154906",
      "acml_tr_pbmn": "1216385130",
      "seln_cnqn_smtn": "463658",
      "shnu_cnqn_smtn": "72251",
      "ntby_cnqn": "-391407"
    },
    {
      "data_rank": "10",
      "mksc_shrn_iscd": "271050",
      "hts_kor_isnm": "KODEX WTI원유선물인버스(H)",
      "stck_prpr": "4185",
      "prdy_vrss_sign": "5",
      "prdy_vrss": "-15",
      "prdy_ctrt": "-0.36",
      "acml_vol": "133001",
      "acml_tr_pbmn": "557302930",
      "seln_cnqn_smtn": "479478",
      "shnu_cnqn_smtn": "94195",
      "ntby_cnqn": "-385283"
    },
    {
      "data_rank": "11",
      "mksc_shrn_iscd": "227950",
      "hts_kor_isnm": "엔투텍",
      "stck_prpr": "787",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "1",
      "prdy_ctrt": "0.13",
      "acml_vol": "531903",
      "acml_tr_pbmn": "421143789",
      "seln_cnqn_smtn": "978263",
      "shnu_cnqn_smtn": "593139",
      "ntby_cnqn": "-385124"
    },
    {
      "data_rank": "12",
      "mksc_shrn_iscd": "003410",
      "hts_kor_isnm": "쌍용C&E",
      "stck_prpr": "7000",
      "prdy_vrss_sign": "3",
      "prdy_vrss": "0",
      "prdy_ctrt": "0.00",
      "acml_vol": "150020",
      "acml_tr_pbmn": "1050492840",
      "seln_cnqn_smtn": "605368",
      "shnu_cnqn_smtn": "221741",
      "ntby_cnqn": "-383627"
    },
    {
      "data_rank": "13",
      "mksc_shrn_iscd": "446770",
      "hts_kor_isnm": "ACE 글로벌반도체TOP4 Plus SOLACTIVE",
      "stck_prpr": "21540",
      "prdy_vrss_sign": "5",
      "prdy_vrss": "-210",
      "prdy_ctrt": "-0.97",
      "acml_vol": "121124",
      "acml_tr_pbmn": "2608030145",
      "seln_cnqn_smtn": "557891",
      "shnu_cnqn_smtn": "202444",
      "ntby_cnqn": "-355447"
    },
    {
      "data_rank": "14",
      "mksc_shrn_iscd": "012170",
      "hts_kor_isnm": "아센디오",
      "stck_prpr": "1066",
      "prdy_vrss_sign": "3",
      "prdy_vrss": "0",
      "prdy_ctrt": "0.00",
      "acml_vol": "2719320",
      "acml_tr_pbmn": "2937797895",
      "seln_cnqn_smtn": "4579213",
      "shnu_cnqn_smtn": "4278634",
      "ntby_cnqn": "-300579"
    },
    {
      "data_rank": "15",
      "mksc_shrn_iscd": "305720",
      "hts_kor_isnm": "KODEX 2차전지산업",
      "stck_prpr": "22090",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "290",
      "prdy_ctrt": "1.33",
      "acml_vol": "476994",
      "acml_tr_pbmn": "10501325940",
      "seln_cnqn_smtn": "669969",
      "shnu_cnqn_smtn": "381247",
      "ntby_cnqn": "-288722"
    },
    {
      "data_rank": "16",
      "mksc_shrn_iscd": "455850",
      "hts_kor_isnm": "SOL AI반도체소부장",
      "stck_prpr": "14950",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "180",
      "prdy_ctrt": "1.22",
      "acml_vol": "317328",
      "acml_tr_pbmn": "4715313100",
      "seln_cnqn_smtn": "513395",
      "shnu_cnqn_smtn": "228189",
      "ntby_cnqn": "-285206"
    },
    {
      "data_rank": "17",
      "mksc_shrn_iscd": "018000",
      "hts_kor_isnm": "유니슨",
      "stck_prpr": "1168",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "150",
      "prdy_ctrt": "14.73",
      "acml_vol": "5280049",
      "acml_tr_pbmn": "6263011909",
      "seln_cnqn_smtn": "407197",
      "shnu_cnqn_smtn": "124444",
      "ntby_cnqn": "-282753"
    },
    {
      "data_rank": "18",
      "mksc_shrn_iscd": "096350",
      "hts_kor_isnm": "대창솔루션",
      "stck_prpr": "498",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "4",
      "prdy_ctrt": "0.81",
      "acml_vol": "442715",
      "acml_tr_pbmn": "220176716",
      "seln_cnqn_smtn": "502574",
      "shnu_cnqn_smtn": "246358",
      "ntby_cnqn": "-256216"
    },
    {
      "data_rank": "19",
      "mksc_shrn_iscd": "474590",
      "hts_kor_isnm": "WOORI 반도체밸류체인액티브",
      "stck_prpr": "11080",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "95",
      "prdy_ctrt": "0.86",
      "acml_vol": "18",
      "acml_tr_pbmn": "198175",
      "seln_cnqn_smtn": "248406",
      "shnu_cnqn_smtn": "3999",
      "ntby_cnqn": "-244407"
    },
    {
      "data_rank": "20",
      "mksc_shrn_iscd": "007460",
      "hts_kor_isnm": "에이프로젠",
      "stck_prpr": "1084",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "12",
      "prdy_ctrt": "1.12",
      "acml_vol": "5282705",
      "acml_tr_pbmn": "5806140076",
      "seln_cnqn_smtn": "3418267",
      "shnu_cnqn_smtn": "3192395",
      "ntby_cnqn": "-225872"
    },
    {
      "data_rank": "21",
      "mksc_shrn_iscd": "088350",
      "hts_kor_isnm": "한화생명",
      "stck_prpr": "3185",
      "prdy_vrss_sign": "5",
      "prdy_vrss": "-65",
      "prdy_ctrt": "-2.00",
      "acml_vol": "1005843",
      "acml_tr_pbmn": "3216904250",
      "seln_cnqn_smtn": "795617",
      "shnu_cnqn_smtn": "589311",
      "ntby_cnqn": "-206306"
    },
    {
      "data_rank": "22",
      "mksc_shrn_iscd": "323230",
      "hts_kor_isnm": "엠에프엠코리아",
      "stck_prpr": "608",
      "prdy_vrss_sign": "5",
      "prdy_vrss": "-2",
      "prdy_ctrt": "-0.33",
      "acml_vol": "701312",
      "acml_tr_pbmn": "425004195",
      "seln_cnqn_smtn": "1357154",
      "shnu_cnqn_smtn": "1169986",
      "ntby_cnqn": "-187168"
    },
    {
      "data_rank": "23",
      "mksc_shrn_iscd": "053030",
      "hts_kor_isnm": "바이넥스",
      "stck_prpr": "18030",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "1570",
      "prdy_ctrt": "9.54",
      "acml_vol": "7593833",
      "acml_tr_pbmn": "133713682520",
      "seln_cnqn_smtn": "1770115",
      "shnu_cnqn_smtn": "1590560",
      "ntby_cnqn": "-179555"
    },
    {
      "data_rank": "24",
      "mksc_shrn_iscd": "287410",
      "hts_kor_isnm": "제이시스메디칼",
      "stck_prpr": "7690",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "60",
      "prdy_ctrt": "0.79",
      "acml_vol": "171896",
      "acml_tr_pbmn": "1326481640",
      "seln_cnqn_smtn": "298796",
      "shnu_cnqn_smtn": "128249",
      "ntby_cnqn": "-170547"
    },
    {
      "data_rank": "25",
      "mksc_shrn_iscd": "462330",
      "hts_kor_isnm": "KODEX 2차전지산업레버리지",
      "stck_prpr": "4690",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "100",
      "prdy_ctrt": "2.18",
      "acml_vol": "1042444",
      "acml_tr_pbmn": "4855711260",
      "seln_cnqn_smtn": "648426",
      "shnu_cnqn_smtn": "481012",
      "ntby_cnqn": "-167414"
    },
    {
      "data_rank": "26",
      "mksc_shrn_iscd": "034220",
      "hts_kor_isnm": "LG디스플레이",
      "stck_prpr": "11060",
      "prdy_vrss_sign": "5",
      "prdy_vrss": "-120",
      "prdy_ctrt": "-1.07",
      "acml_vol": "208580",
      "acml_tr_pbmn": "2314630570",
      "seln_cnqn_smtn": "430800",
      "shnu_cnqn_smtn": "277677",
      "ntby_cnqn": "-153123"
    },
    {
      "data_rank": "27",
      "mksc_shrn_iscd": "316140",
      "hts_kor_isnm": "우리금융지주",
      "stck_prpr": "14780",
      "prdy_vrss_sign": "5",
      "prdy_vrss": "-450",
      "prdy_ctrt": "-2.95",
      "acml_vol": "2032465",
      "acml_tr_pbmn": "30023382510",
      "seln_cnqn_smtn": "898309",
      "shnu_cnqn_smtn": "745834",
      "ntby_cnqn": "-152475"
    },
    {
      "data_rank": "28",
      "mksc_shrn_iscd": "091170",
      "hts_kor_isnm": "KODEX 은행",
      "stck_prpr": "8480",
      "prdy_vrss_sign": "5",
      "prdy_vrss": "-185",
      "prdy_ctrt": "-2.14",
      "acml_vol": "633020",
      "acml_tr_pbmn": "5343176250",
      "seln_cnqn_smtn": "657061",
      "shnu_cnqn_smtn": "506916",
      "ntby_cnqn": "-150145"
    },
    {
      "data_rank": "29",
      "mksc_shrn_iscd": "015590",
      "hts_kor_isnm": "KIB플러그에너지",
      "stck_prpr": "377",
      "prdy_vrss_sign": "5",
      "prdy_vrss": "-2",
      "prdy_ctrt": "-0.53",
      "acml_vol": "1338633",
      "acml_tr_pbmn": "505056784",
      "seln_cnqn_smtn": "517713",
      "shnu_cnqn_smtn": "370216",
      "ntby_cnqn": "-147497"
    },
    {
      "data_rank": "30",
      "mksc_shrn_iscd": "004870",
      "hts_kor_isnm": "티웨이홀딩스",
      "stck_prpr": "465",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "9",
      "prdy_ctrt": "1.97",
      "acml_vol": "34028",
      "acml_tr_pbmn": "15695619",
      "seln_cnqn_smtn": "186276",
      "shnu_cnqn_smtn": "39824",
      "ntby_cnqn": "-146452"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```
