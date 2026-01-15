# 국내주식 신고/신저근접종목 상위[v1_국내주식-105]

> [국내주식] 순위분석

국내주식 신고/신저근접종목 상위 API입니다.
한국투자 HTS(eFriend Plus) > [0187] 신고/신저 근접종목 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.
최대 30건 확인 가능하며, 다음 조회가 불가합니다.

※ 30건 이상의 목록 조회가 필요한 경우, 대안으로 종목조건검색 API를 이용해서 원하는 종목 100개까지 검색할 수 있는 기능을 제공하고 있습니다.
종목조건검색 API는 HTS(efriend Plus) [0110] 조건검색에서 등록 및 서버저장한 나의 조건 목록을 확인할 수 있는 API로,
자세한 사용 방법은 공지사항 - [조건검색 필독] 조건검색 API 이용안내 참고 부탁드립니다.


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `72e63cb2-2ab1-41a0-8ab9-62cbeaa5eea0` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/ranking/near-new-highlow` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `FHPST01870000` |
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
| `tr_id` | 거래ID | String | 13 | Y | FHPST01870000 |
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
| `fid_aply_rang_vol` | 적용 범위 거래량 | String | 18 | Y | 0: 전체, 100: 100주 이상 |
| `fid_cond_mrkt_div_code` | 조건 시장 분류 코드 | String | 2 | Y | 시장구분코드 (주식 J) |
| `fid_cond_scr_div_code` | 조건 화면 분류 코드 | String | 5 | Y | Unique key(20187) |
| `fid_div_cls_code` | 분류 구분 코드 | String | 2 | Y | 0:전체, 1:관리종목, 2:투자주의, 3:투자경고 |
| `fid_input_cnt_1` | 입력 수1 | String | 2 | Y | 괴리율 최소 |
| `fid_input_cnt_2` | 입력 수2 | String | 10 | Y | 괴리율 최대 |
| `fid_prc_cls_code` | 가격 구분 코드 | String | 10 | Y | 0:신고근접, 1:신저근접 |
| `fid_input_iscd` |  입력 종목코드 | String | 12 | Y | 0000:전체, 0001:거래소, 1001:코스닥, 2001:코스피200, 4001: KRX100 |
| `fid_trgt_cls_code` | 대상 구분 코드 | String | 32 | Y | 0: 전체 |
| `fid_trgt_exls_cls_code` | 대상 제외 구분 코드 | String | 32 | Y | 0:전체, 1:관리종목, 2:투자주의, 3:투자경고, 4:투자위험예고, 5:투자위험, 6:보통주, 7:우선주 |
| `fid_aply_rang_prc_1` | 적용 범위 가격1 | String | 18 | Y | 가격 ~ |
| `fid_aply_rang_prc_2` | 적용 범위 가격2 | String | 18 | Y | ~ 가격 |

### 요청 예시

```json
{
  "fid_cond_mrkt_div_code": "J",
  "fid_cond_scr_div_code": "20187",
  "fid_div_cls_code": "0",
  "fid_input_cnt_1": "",
  "fid_input_cnt_2": "",
  "fid_prc_cls_code": "0",
  "fid_input_iscd": "0000",
  "fid_trgt_cls_code": "0",
  "fid_trgt_exls_cls_code": "0",
  "fid_aply_rang_prc_1": "",
  "fid_aply_rang_prc_2": "",
  "fid_aply_rang_vol": "0"
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
| `hts_kor_isnm` | HTS 한글 종목명 | String | 40 | Y |  |
| `mksc_shrn_iscd` | 유가증권 단축 종목코드 | String | 9 | Y |  |
| `stck_prpr` | 주식 현재가 | String | 10 | Y |  |
| `prdy_vrss_sign` | 전일 대비 부호 | String | 1 | Y |  |
| `prdy_vrss` | 전일 대비 | String | 10 | Y |  |
| `prdy_ctrt` | 전일 대비율 | String | 82 | Y |  |
| `askp` | 매도호가 | String | 10 | Y |  |
| `askp_rsqn1` | 매도호가 잔량1 | String | 12 | Y |  |
| `bidp` | 매수호가 | String | 10 | Y |  |
| `bidp_rsqn1` | 매수호가 잔량1 | String | 12 | Y |  |
| `acml_vol` | 누적 거래량 | String | 18 | Y |  |
| `new_hgpr` | 신 최고가 | String | 10 | Y |  |
| `hprc_near_rate` | 고가 근접 비율 | String | 84 | Y |  |
| `new_lwpr` | 신 최저가 | String | 10 | Y |  |
| `lwpr_near_rate` | 저가 근접 비율 | String | 84 | Y |  |
| `stck_sdpr` | 주식 기준가 | String | 10 | Y |  |

### 응답 예시

```json
{
  "output": [
    {
      "hts_kor_isnm": "IHQ",
      "mksc_shrn_iscd": "003560",
      "stck_prpr": "10760",
      "prdy_vrss_sign": "0",
      "prdy_vrss": "0",
      "prdy_ctrt": "0.00",
      "askp": "0",
      "askp_rsqn1": "0",
      "bidp": "0",
      "bidp_rsqn1": "0",
      "acml_vol": "0",
      "new_hgpr": "10760",
      "hprc_near_rate": "0.00",
      "new_lwpr": "185",
      "lwpr_near_rate": "-98.28",
      "stck_sdpr": "10760"
    },
    {
      "hts_kor_isnm": "선도전기",
      "mksc_shrn_iscd": "007610",
      "stck_prpr": "3000",
      "prdy_vrss_sign": "0",
      "prdy_vrss": "0",
      "prdy_ctrt": "0.00",
      "askp": "0",
      "askp_rsqn1": "0",
      "bidp": "0",
      "bidp_rsqn1": "0",
      "acml_vol": "0",
      "new_hgpr": "3000",
      "hprc_near_rate": "0.00",
      "new_lwpr": "3000",
      "lwpr_near_rate": "0.00",
      "stck_sdpr": "3000"
    },
    {
      "hts_kor_isnm": "청호ICT",
      "mksc_shrn_iscd": "012600",
      "stck_prpr": "2490",
      "prdy_vrss_sign": "0",
      "prdy_vrss": "0",
      "prdy_ctrt": "0.00",
      "askp": "0",
      "askp_rsqn1": "0",
      "bidp": "0",
      "bidp_rsqn1": "0",
      "acml_vol": "0",
      "new_hgpr": "2490",
      "hprc_near_rate": "0.00",
      "new_lwpr": "2490",
      "lwpr_near_rate": "0.00",
      "stck_sdpr": "2490"
    },
    {
      "hts_kor_isnm": "광림",
      "mksc_shrn_iscd": "014200",
      "stck_prpr": "1006",
      "prdy_vrss_sign": "0",
      "prdy_vrss": "0",
      "prdy_ctrt": "0.00",
      "askp": "0",
      "askp_rsqn1": "0",
      "bidp": "0",
      "bidp_rsqn1": "0",
      "acml_vol": "0",
      "new_hgpr": "1006",
      "hprc_near_rate": "0.00",
      "new_lwpr": "1006",
      "lwpr_near_rate": "0.00",
      "stck_sdpr": "1006"
    },
    {
      "hts_kor_isnm": "비케이탑스",
      "mksc_shrn_iscd": "030790",
      "stck_prpr": "904",
      "prdy_vrss_sign": "0",
      "prdy_vrss": "0",
      "prdy_ctrt": "0.00",
      "askp": "0",
      "askp_rsqn1": "0",
      "bidp": "0",
      "bidp_rsqn1": "0",
      "acml_vol": "0",
      "new_hgpr": "904",
      "hprc_near_rate": "0.00",
      "new_lwpr": "904",
      "lwpr_near_rate": "0.00",
      "stck_sdpr": "904"
    },
    {
      "hts_kor_isnm": "더라미",
      "mksc_shrn_iscd": "032860",
      "stck_prpr": "3640",
      "prdy_vrss_sign": "0",
      "prdy_vrss": "0",
      "prdy_ctrt": "0.00",
      "askp": "0",
      "askp_rsqn1": "0",
      "bidp": "0",
      "bidp_rsqn1": "0",
      "acml_vol": "0",
      "new_hgpr": "3640",
      "hprc_near_rate": "0.00",
      "new_lwpr": "3640",
      "lwpr_near_rate": "0.00",
      "stck_sdpr": "3640"
    },
    {
      "hts_kor_isnm": "KH 필룩스",
      "mksc_shrn_iscd": "033180",
      "stck_prpr": "6630",
      "prdy_vrss_sign": "0",
      "prdy_vrss": "0",
      "prdy_ctrt": "0.00",
      "askp": "0",
      "askp_rsqn1": "0",
      "bidp": "0",
      "bidp_rsqn1": "0",
      "acml_vol": "0",
      "new_hgpr": "6630",
      "hprc_near_rate": "0.00",
      "new_lwpr": "325",
      "lwpr_near_rate": "-95.10",
      "stck_sdpr": "6630"
    },
    {
      "hts_kor_isnm": "좋은사람들",
      "mksc_shrn_iscd": "033340",
      "stck_prpr": "2110",
      "prdy_vrss_sign": "0",
      "prdy_vrss": "0",
      "prdy_ctrt": "0.00",
      "askp": "0",
      "askp_rsqn1": "0",
      "bidp": "0",
      "bidp_rsqn1": "0",
      "acml_vol": "0",
      "new_hgpr": "2110",
      "hprc_near_rate": "0.00",
      "new_lwpr": "2110",
      "lwpr_near_rate": "0.00",
      "stck_sdpr": "2110"
    },
    {
      "hts_kor_isnm": "한국테크놀로지",
      "mksc_shrn_iscd": "053590",
      "stck_prpr": "334",
      "prdy_vrss_sign": "0",
      "prdy_vrss": "0",
      "prdy_ctrt": "0.00",
      "askp": "0",
      "askp_rsqn1": "0",
      "bidp": "0",
      "bidp_rsqn1": "0",
      "acml_vol": "0",
      "new_hgpr": "334",
      "hprc_near_rate": "0.00",
      "new_lwpr": "334",
      "lwpr_near_rate": "0.00",
      "stck_sdpr": "334"
    },
    {
      "hts_kor_isnm": "이노시스",
      "mksc_shrn_iscd": "056090",
      "stck_prpr": "1180",
      "prdy_vrss_sign": "0",
      "prdy_vrss": "0",
      "prdy_ctrt": "0.00",
      "askp": "0",
      "askp_rsqn1": "0",
      "bidp": "0",
      "bidp_rsqn1": "0",
      "acml_vol": "0",
      "new_hgpr": "1180",
      "hprc_near_rate": "0.00",
      "new_lwpr": "1180",
      "lwpr_near_rate": "0.00",
      "stck_sdpr": "1180"
    },
    {
      "hts_kor_isnm": "피에이치씨",
      "mksc_shrn_iscd": "057880",
      "stck_prpr": "17570",
      "prdy_vrss_sign": "0",
      "prdy_vrss": "0",
      "prdy_ctrt": "0.00",
      "askp": "0",
      "askp_rsqn1": "0",
      "bidp": "0",
      "bidp_rsqn1": "0",
      "acml_vol": "0",
      "new_hgpr": "17570",
      "hprc_near_rate": "0.00",
      "new_lwpr": "1740",
      "lwpr_near_rate": "-90.10",
      "stck_sdpr": "17570"
    },
    {
      "hts_kor_isnm": "아리온",
      "mksc_shrn_iscd": "058220",
      "stck_prpr": "275",
      "prdy_vrss_sign": "0",
      "prdy_vrss": "0",
      "prdy_ctrt": "0.00",
      "askp": "0",
      "askp_rsqn1": "0",
      "bidp": "0",
      "bidp_rsqn1": "0",
      "acml_vol": "0",
      "new_hgpr": "275",
      "hprc_near_rate": "0.00",
      "new_lwpr": "275",
      "lwpr_near_rate": "0.00",
      "stck_sdpr": "275"
    },
    {
      "hts_kor_isnm": "파나케이아",
      "mksc_shrn_iscd": "058530",
      "stck_prpr": "1620",
      "prdy_vrss_sign": "0",
      "prdy_vrss": "0",
      "prdy_ctrt": "0.00",
      "askp": "0",
      "askp_rsqn1": "0",
      "bidp": "0",
      "bidp_rsqn1": "0",
      "acml_vol": "0",
      "new_hgpr": "1620",
      "hprc_near_rate": "0.00",
      "new_lwpr": "1620",
      "lwpr_near_rate": "0.00",
      "stck_sdpr": "1620"
    },
    {
      "hts_kor_isnm": "티엘아이",
      "mksc_shrn_iscd": "062860",
      "stck_prpr": "5800",
      "prdy_vrss_sign": "0",
      "prdy_vrss": "0",
      "prdy_ctrt": "0.00",
      "askp": "0",
      "askp_rsqn1": "0",
      "bidp": "0",
      "bidp_rsqn1": "0",
      "acml_vol": "0",
      "new_hgpr": "5800",
      "hprc_near_rate": "0.00",
      "new_lwpr": "5800",
      "lwpr_near_rate": "0.00",
      "stck_sdpr": "5800"
    },
    {
      "hts_kor_isnm": "녹원씨엔아이",
      "mksc_shrn_iscd": "065560",
      "stck_prpr": "11540",
      "prdy_vrss_sign": "0",
      "prdy_vrss": "0",
      "prdy_ctrt": "0.00",
      "askp": "0",
      "askp_rsqn1": "0",
      "bidp": "0",
      "bidp_rsqn1": "0",
      "acml_vol": "0",
      "new_hgpr": "11540",
      "hprc_near_rate": "0.00",
      "new_lwpr": "5770",
      "lwpr_near_rate": "-50.00",
      "stck_sdpr": "11540"
    },
    {
      "hts_kor_isnm": "버킷스튜디오",
      "mksc_shrn_iscd": "066410",
      "stck_prpr": "1153",
      "prdy_vrss_sign": "0",
      "prdy_vrss": "0",
      "prdy_ctrt": "0.00",
      "askp": "0",
      "askp_rsqn1": "0",
      "bidp": "0",
      "bidp_rsqn1": "0",
      "acml_vol": "0",
      "new_hgpr": "1153",
      "hprc_near_rate": "0.00",
      "new_lwpr": "1153",
      "lwpr_near_rate": "0.00",
      "stck_sdpr": "1153"
    },
    {
      "hts_kor_isnm": "국일제지",
      "mksc_shrn_iscd": "078130",
      "stck_prpr": "800",
      "prdy_vrss_sign": "0",
      "prdy_vrss": "0",
      "prdy_ctrt": "0.00",
      "askp": "0",
      "askp_rsqn1": "0",
      "bidp": "0",
      "bidp_rsqn1": "0",
      "acml_vol": "0",
      "new_hgpr": "800",
      "hprc_near_rate": "0.00",
      "new_lwpr": "800",
      "lwpr_near_rate": "0.00",
      "stck_sdpr": "800"
    },
    {
      "hts_kor_isnm": "세원이앤씨",
      "mksc_shrn_iscd": "091090",
      "stck_prpr": "1270",
      "prdy_vrss_sign": "0",
      "prdy_vrss": "0",
      "prdy_ctrt": "0.00",
      "askp": "0",
      "askp_rsqn1": "0",
      "bidp": "0",
      "bidp_rsqn1": "0",
      "acml_vol": "0",
      "new_hgpr": "1270",
      "hprc_near_rate": "0.00",
      "new_lwpr": "185",
      "lwpr_near_rate": "-85.43",
      "stck_sdpr": "1270"
    },
    {
      "hts_kor_isnm": "인바이오젠",
      "mksc_shrn_iscd": "101140",
      "stck_prpr": "9340",
      "prdy_vrss_sign": "0",
      "prdy_vrss": "0",
      "prdy_ctrt": "0.00",
      "askp": "0",
      "askp_rsqn1": "0",
      "bidp": "0",
      "bidp_rsqn1": "0",
      "acml_vol": "0",
      "new_hgpr": "9340",
      "hprc_near_rate": "0.00",
      "new_lwpr": "462",
      "lwpr_near_rate": "-95.05",
      "stck_sdpr": "9340"
    },
    {
      "hts_kor_isnm": "주성코퍼레이션",
      "mksc_shrn_iscd": "109070",
      "stck_prpr": "4100",
      "prdy_vrss_sign": "0",
      "prdy_vrss": "0",
      "prdy_ctrt": "0.00",
      "askp": "0",
      "askp_rsqn1": "0",
      "bidp": "0",
      "bidp_rsqn1": "0",
      "acml_vol": "0",
      "new_hgpr": "4100",
      "hprc_near_rate": "0.00",
      "new_lwpr": "4100",
      "lwpr_near_rate": "0.00",
      "stck_sdpr": "4100"
    },
    {
      "hts_kor_isnm": "KH 전자",
      "mksc_shrn_iscd": "111870",
      "stck_prpr": "2970",
      "prdy_vrss_sign": "0",
      "prdy_vrss": "0",
      "prdy_ctrt": "0.00",
      "askp": "0",
      "askp_rsqn1": "0",
      "bidp": "0",
      "bidp_rsqn1": "0",
      "acml_vol": "0",
      "new_hgpr": "2970",
      "hprc_near_rate": "0.00",
      "new_lwpr": "145",
      "lwpr_near_rate": "-95.12",
      "stck_sdpr": "2970"
    },
    {
      "hts_kor_isnm": "스마트솔루션즈",
      "mksc_shrn_iscd": "136510",
      "stck_prpr": "11600",
      "prdy_vrss_sign": "0",
      "prdy_vrss": "0",
      "prdy_ctrt": "0.00",
      "askp": "0",
      "askp_rsqn1": "0",
      "bidp": "0",
      "bidp_rsqn1": "0",
      "acml_vol": "0",
      "new_hgpr": "11600",
      "hprc_near_rate": "0.00",
      "new_lwpr": "11600",
      "lwpr_near_rate": "0.00",
      "stck_sdpr": "11600"
    },
    {
      "hts_kor_isnm": "비디아이",
      "mksc_shrn_iscd": "148140",
      "stck_prpr": "6140",
      "prdy_vrss_sign": "0",
      "prdy_vrss": "0",
      "prdy_ctrt": "0.00",
      "askp": "0",
      "askp_rsqn1": "0",
      "bidp": "0",
      "bidp_rsqn1": "0",
      "acml_vol": "0",
      "new_hgpr": "6140",
      "hprc_near_rate": "0.00",
      "new_lwpr": "640",
      "lwpr_near_rate": "-89.58",
      "stck_sdpr": "6140"
    },
    {
      "hts_kor_isnm": "인트로메딕",
      "mksc_shrn_iscd": "150840",
      "stck_prpr": "5850",
      "prdy_vrss_sign": "0",
      "prdy_vrss": "0",
      "prdy_ctrt": "0.00",
      "askp": "0",
      "askp_rsqn1": "0",
      "bidp": "0",
      "bidp_rsqn1": "0",
      "acml_vol": "0",
      "new_hgpr": "5850",
      "hprc_near_rate": "0.00",
      "new_lwpr": "5850",
      "lwpr_near_rate": "0.00",
      "stck_sdpr": "5850"
    },
    {
      "hts_kor_isnm": "이큐셀",
      "mksc_shrn_iscd": "160600",
      "stck_prpr": "3100",
      "prdy_vrss_sign": "0",
      "prdy_vrss": "0",
      "prdy_ctrt": "0.00",
      "askp": "0",
      "askp_rsqn1": "0",
      "bidp": "0",
      "bidp_rsqn1": "0",
      "acml_vol": "0",
      "new_hgpr": "3100",
      "hprc_near_rate": "0.00",
      "new_lwpr": "3100",
      "lwpr_near_rate": "0.00",
      "stck_sdpr": "3100"
    },
    {
      "hts_kor_isnm": "장원테크",
      "mksc_shrn_iscd": "174880",
      "stck_prpr": "2650",
      "prdy_vrss_sign": "0",
      "prdy_vrss": "0",
      "prdy_ctrt": "0.00",
      "askp": "0",
      "askp_rsqn1": "0",
      "bidp": "0",
      "bidp_rsqn1": "0",
      "acml_vol": "0",
      "new_hgpr": "2650",
      "hprc_near_rate": "0.00",
      "new_lwpr": "455",
      "lwpr_near_rate": "-82.83",
      "stck_sdpr": "2650"
    },
    {
      "hts_kor_isnm": "일월지엠엘",
      "mksc_shrn_iscd": "178780",
      "stck_prpr": "8650",
      "prdy_vrss_sign": "0",
      "prdy_vrss": "0",
      "prdy_ctrt": "0.00",
      "askp": "0",
      "askp_rsqn1": "0",
      "bidp": "0",
      "bidp_rsqn1": "0",
      "acml_vol": "0",
      "new_hgpr": "8650",
      "hprc_near_rate": "0.00",
      "new_lwpr": "8650",
      "lwpr_near_rate": "0.00",
      "stck_sdpr": "8650"
    },
    {
      "hts_kor_isnm": "이즈미디어",
      "mksc_shrn_iscd": "181340",
      "stck_prpr": "2705",
      "prdy_vrss_sign": "0",
      "prdy_vrss": "0",
      "prdy_ctrt": "0.00",
      "askp": "0",
      "askp_rsqn1": "0",
      "bidp": "0",
      "bidp_rsqn1": "0",
      "acml_vol": "0",
      "new_hgpr": "2705",
      "hprc_near_rate": "0.00",
      "new_lwpr": "2705",
      "lwpr_near_rate": "0.00",
      "stck_sdpr": "2705"
    },
    {
      "hts_kor_isnm": "KODEX 미국S&P500산업재(합성)",
      "mksc_shrn_iscd": "200030",
      "stck_prpr": "28335",
      "prdy_vrss_sign": "2",
      "prdy_vrss": "200",
      "prdy_ctrt": "0.71",
      "askp": "28330",
      "askp_rsqn1": "5000",
      "bidp": "28270",
      "bidp_rsqn1": "7",
      "acml_vol": "4998",
      "new_hgpr": "28335",
      "hprc_near_rate": "0.00",
      "new_lwpr": "21600",
      "lwpr_near_rate": "-23.77",
      "stck_sdpr": "28135"
    },
    {
      "hts_kor_isnm": "엔지스테크널러지",
      "mksc_shrn_iscd": "208860",
      "stck_prpr": "2205",
      "prdy_vrss_sign": "0",
      "prdy_vrss": "0",
      "prdy_ctrt": "0.00",
      "askp": "0",
      "askp_rsqn1": "0",
      "bidp": "0",
      "bidp_rsqn1": "0",
      "acml_vol": "0",
      "new_hgpr": "2205",
      "hprc_near_rate": "0.00",
      "new_lwpr": "2205",
      "lwpr_near_rate": "0.00",
      "stck_sdpr": "2205"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```

