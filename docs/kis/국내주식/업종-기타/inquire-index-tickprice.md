# 국내업종 시간별지수(초)[국내주식-064]

> [국내주식] 업종/기타

국내업종 시간별지수(초) API입니다. 
한국투자 HTS(eFriend Plus) > [0211] 업종 시간별지수 화면에서 우측 '10초' 선택 시의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `a87c0275-f467-4199-866a-876a8fcdccb0` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/quotations/inquire-index-tickprice` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `미지원` |
| **TR ID** | `FHPUP02110100`, `모의투자 미지원` |

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
| `tr_id` | 거래ID | String | 13 | Y | FHPUP02110100 |
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
| `FID_INPUT_ISCD` | 입력 종목코드 | String | 12 | Y | 0001:거래소, 1001:코스닥, 2001:코스피200, 3003:KSQ150 |
| `FID_COND_MRKT_DIV_CODE` | 시장 분류 코드 | String | 2 | Y | 시장구분코드 (업종 U) |

### 요청 예시

```json
fid_cond_mrkt_div_code:U
fid_input_iscd:1001
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
| `stck_cntg_hour` | 주식 체결 시간 | String | 6 | Y |  |
| `bstp_nmix_prpr` | 업종 지수 현재가 | String | 112 | Y |  |
| `bstp_nmix_prdy_vrss` | 업종 지수 전일 대비 | String | 112 | Y |  |
| `prdy_vrss_sign` | 전일 대비 부호 | String | 1 | Y |  |
| `bstp_nmix_prdy_ctrt` | 업종 지수 전일 대비율 | String | 82 | Y |  |
| `acml_tr_pbmn` | 누적 거래 대금 | String | 18 | Y |  |
| `acml_vol` | 누적 거래량 | String | 18 | Y |  |
| `cntg_vol` | 체결 거래량 | String | 18 | Y |  |

### 응답 예시

```json
{
  "output": [
    {
      "stck_cntg_hour": "100520",
      "bstp_nmix_prpr": "916.59",
      "bstp_nmix_prdy_vrss": "11.09",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.22",
      "acml_tr_pbmn": "3818437",
      "acml_vol": "311514",
      "cntg_vol": "378"
    },
    {
      "stck_cntg_hour": "100510",
      "bstp_nmix_prpr": "916.56",
      "bstp_nmix_prdy_vrss": "11.06",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.22",
      "acml_tr_pbmn": "3814862",
      "acml_vol": "311136",
      "cntg_vol": "389"
    },
    {
      "stck_cntg_hour": "100500",
      "bstp_nmix_prpr": "916.60",
      "bstp_nmix_prdy_vrss": "11.10",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.23",
      "acml_tr_pbmn": "3811191",
      "acml_vol": "310747",
      "cntg_vol": "460"
    },
    {
      "stck_cntg_hour": "100450",
      "bstp_nmix_prpr": "916.71",
      "bstp_nmix_prdy_vrss": "11.21",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.24",
      "acml_tr_pbmn": "3806215",
      "acml_vol": "310287",
      "cntg_vol": "347"
    },
    {
      "stck_cntg_hour": "100440",
      "bstp_nmix_prpr": "916.71",
      "bstp_nmix_prdy_vrss": "11.21",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.24",
      "acml_tr_pbmn": "3802603",
      "acml_vol": "309940",
      "cntg_vol": "378"
    },
    {
      "stck_cntg_hour": "100430",
      "bstp_nmix_prpr": "916.87",
      "bstp_nmix_prdy_vrss": "11.37",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.26",
      "acml_tr_pbmn": "3798885",
      "acml_vol": "309562",
      "cntg_vol": "390"
    },
    {
      "stck_cntg_hour": "100420",
      "bstp_nmix_prpr": "916.87",
      "bstp_nmix_prdy_vrss": "11.37",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.26",
      "acml_tr_pbmn": "3793980",
      "acml_vol": "309172",
      "cntg_vol": "331"
    },
    {
      "stck_cntg_hour": "100410",
      "bstp_nmix_prpr": "916.69",
      "bstp_nmix_prdy_vrss": "11.19",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.24",
      "acml_tr_pbmn": "3789649",
      "acml_vol": "308841",
      "cntg_vol": "387"
    },
    {
      "stck_cntg_hour": "100400",
      "bstp_nmix_prpr": "916.47",
      "bstp_nmix_prdy_vrss": "10.97",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.21",
      "acml_tr_pbmn": "3784355",
      "acml_vol": "308454",
      "cntg_vol": "302"
    },
    {
      "stck_cntg_hour": "100350",
      "bstp_nmix_prpr": "916.69",
      "bstp_nmix_prdy_vrss": "11.19",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.24",
      "acml_tr_pbmn": "3779730",
      "acml_vol": "308152",
      "cntg_vol": "389"
    },
    {
      "stck_cntg_hour": "100340",
      "bstp_nmix_prpr": "916.64",
      "bstp_nmix_prdy_vrss": "11.14",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.23",
      "acml_tr_pbmn": "3774584",
      "acml_vol": "307763",
      "cntg_vol": "359"
    },
    {
      "stck_cntg_hour": "100330",
      "bstp_nmix_prpr": "916.94",
      "bstp_nmix_prdy_vrss": "11.44",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.26",
      "acml_tr_pbmn": "3769289",
      "acml_vol": "307404",
      "cntg_vol": "590"
    },
    {
      "stck_cntg_hour": "100320",
      "bstp_nmix_prpr": "916.86",
      "bstp_nmix_prdy_vrss": "11.36",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.25",
      "acml_tr_pbmn": "3764728",
      "acml_vol": "306814",
      "cntg_vol": "395"
    },
    {
      "stck_cntg_hour": "100310",
      "bstp_nmix_prpr": "916.76",
      "bstp_nmix_prdy_vrss": "11.26",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.24",
      "acml_tr_pbmn": "3758157",
      "acml_vol": "306419",
      "cntg_vol": "414"
    },
    {
      "stck_cntg_hour": "100300",
      "bstp_nmix_prpr": "917.03",
      "bstp_nmix_prdy_vrss": "11.53",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.27",
      "acml_tr_pbmn": "3753915",
      "acml_vol": "306005",
      "cntg_vol": "351"
    },
    {
      "stck_cntg_hour": "100250",
      "bstp_nmix_prpr": "917.08",
      "bstp_nmix_prdy_vrss": "11.58",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.28",
      "acml_tr_pbmn": "3749232",
      "acml_vol": "305654",
      "cntg_vol": "440"
    },
    {
      "stck_cntg_hour": "100240",
      "bstp_nmix_prpr": "917.18",
      "bstp_nmix_prdy_vrss": "11.68",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.29",
      "acml_tr_pbmn": "3741905",
      "acml_vol": "305214",
      "cntg_vol": "324"
    },
    {
      "stck_cntg_hour": "100230",
      "bstp_nmix_prpr": "917.27",
      "bstp_nmix_prdy_vrss": "11.77",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.30",
      "acml_tr_pbmn": "3737983",
      "acml_vol": "304890",
      "cntg_vol": "449"
    },
    {
      "stck_cntg_hour": "100220",
      "bstp_nmix_prpr": "917.31",
      "bstp_nmix_prdy_vrss": "11.81",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.30",
      "acml_tr_pbmn": "3732890",
      "acml_vol": "304441",
      "cntg_vol": "459"
    },
    {
      "stck_cntg_hour": "100210",
      "bstp_nmix_prpr": "916.61",
      "bstp_nmix_prdy_vrss": "11.11",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.23",
      "acml_tr_pbmn": "3725485",
      "acml_vol": "303982",
      "cntg_vol": "424"
    },
    {
      "stck_cntg_hour": "100200",
      "bstp_nmix_prpr": "916.64",
      "bstp_nmix_prdy_vrss": "11.14",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.23",
      "acml_tr_pbmn": "3720969",
      "acml_vol": "303558",
      "cntg_vol": "365"
    },
    {
      "stck_cntg_hour": "100150",
      "bstp_nmix_prpr": "916.76",
      "bstp_nmix_prdy_vrss": "11.26",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.24",
      "acml_tr_pbmn": "3716791",
      "acml_vol": "303193",
      "cntg_vol": "377"
    },
    {
      "stck_cntg_hour": "100140",
      "bstp_nmix_prpr": "916.49",
      "bstp_nmix_prdy_vrss": "10.99",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.21",
      "acml_tr_pbmn": "3712492",
      "acml_vol": "302816",
      "cntg_vol": "392"
    },
    {
      "stck_cntg_hour": "100130",
      "bstp_nmix_prpr": "916.49",
      "bstp_nmix_prdy_vrss": "10.99",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.21",
      "acml_tr_pbmn": "3707273",
      "acml_vol": "302424",
      "cntg_vol": "324"
    },
    {
      "stck_cntg_hour": "100120",
      "bstp_nmix_prpr": "916.60",
      "bstp_nmix_prdy_vrss": "11.10",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.23",
      "acml_tr_pbmn": "3702465",
      "acml_vol": "302100",
      "cntg_vol": "430"
    },
    {
      "stck_cntg_hour": "100110",
      "bstp_nmix_prpr": "916.55",
      "bstp_nmix_prdy_vrss": "11.05",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.22",
      "acml_tr_pbmn": "3698004",
      "acml_vol": "301670",
      "cntg_vol": "387"
    },
    {
      "stck_cntg_hour": "100100",
      "bstp_nmix_prpr": "916.33",
      "bstp_nmix_prdy_vrss": "10.83",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.20",
      "acml_tr_pbmn": "3692560",
      "acml_vol": "301283",
      "cntg_vol": "428"
    },
    {
      "stck_cntg_hour": "100050",
      "bstp_nmix_prpr": "916.43",
      "bstp_nmix_prdy_vrss": "10.93",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.21",
      "acml_tr_pbmn": "3687275",
      "acml_vol": "300855",
      "cntg_vol": "437"
    },
    {
      "stck_cntg_hour": "100040",
      "bstp_nmix_prpr": "916.79",
      "bstp_nmix_prdy_vrss": "11.29",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.25",
      "acml_tr_pbmn": "3681346",
      "acml_vol": "300418",
      "cntg_vol": "465"
    },
    {
      "stck_cntg_hour": "100030",
      "bstp_nmix_prpr": "917.01",
      "bstp_nmix_prdy_vrss": "11.51",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.27",
      "acml_tr_pbmn": "3676019",
      "acml_vol": "299953",
      "cntg_vol": "453"
    },
    {
      "stck_cntg_hour": "100020",
      "bstp_nmix_prpr": "916.77",
      "bstp_nmix_prdy_vrss": "11.27",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.24",
      "acml_tr_pbmn": "3669136",
      "acml_vol": "299500",
      "cntg_vol": "443"
    },
    {
      "stck_cntg_hour": "100010",
      "bstp_nmix_prpr": "916.76",
      "bstp_nmix_prdy_vrss": "11.26",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.24",
      "acml_tr_pbmn": "3663148",
      "acml_vol": "299057",
      "cntg_vol": "523"
    },
    {
      "stck_cntg_hour": "100000",
      "bstp_nmix_prpr": "916.49",
      "bstp_nmix_prdy_vrss": "10.99",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.21",
      "acml_tr_pbmn": "3656614",
      "acml_vol": "298534",
      "cntg_vol": "444"
    },
    {
      "stck_cntg_hour": "095950",
      "bstp_nmix_prpr": "916.60",
      "bstp_nmix_prdy_vrss": "11.10",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.23",
      "acml_tr_pbmn": "3651490",
      "acml_vol": "298090",
      "cntg_vol": "388"
    },
    {
      "stck_cntg_hour": "095940",
      "bstp_nmix_prpr": "916.84",
      "bstp_nmix_prdy_vrss": "11.34",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.25",
      "acml_tr_pbmn": "3646864",
      "acml_vol": "297702",
      "cntg_vol": "446"
    },
    {
      "stck_cntg_hour": "095930",
      "bstp_nmix_prpr": "916.90",
      "bstp_nmix_prdy_vrss": "11.40",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.26",
      "acml_tr_pbmn": "3642503",
      "acml_vol": "297256",
      "cntg_vol": "426"
    },
    {
      "stck_cntg_hour": "095920",
      "bstp_nmix_prpr": "917.04",
      "bstp_nmix_prdy_vrss": "11.54",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.27",
      "acml_tr_pbmn": "3638580",
      "acml_vol": "296830",
      "cntg_vol": "493"
    },
    {
      "stck_cntg_hour": "095910",
      "bstp_nmix_prpr": "916.99",
      "bstp_nmix_prdy_vrss": "11.49",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.27",
      "acml_tr_pbmn": "3634479",
      "acml_vol": "296337",
      "cntg_vol": "456"
    },
    {
      "stck_cntg_hour": "095900",
      "bstp_nmix_prpr": "917.02",
      "bstp_nmix_prdy_vrss": "11.52",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.27",
      "acml_tr_pbmn": "3629148",
      "acml_vol": "295881",
      "cntg_vol": "602"
    },
    {
      "stck_cntg_hour": "095850",
      "bstp_nmix_prpr": "917.16",
      "bstp_nmix_prdy_vrss": "11.66",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.29",
      "acml_tr_pbmn": "3621794",
      "acml_vol": "295279",
      "cntg_vol": "652"
    },
    {
      "stck_cntg_hour": "095840",
      "bstp_nmix_prpr": "917.35",
      "bstp_nmix_prdy_vrss": "11.85",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.31",
      "acml_tr_pbmn": "3616303",
      "acml_vol": "294627",
      "cntg_vol": "361"
    },
    {
      "stck_cntg_hour": "095830",
      "bstp_nmix_prpr": "917.33",
      "bstp_nmix_prdy_vrss": "11.83",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.31",
      "acml_tr_pbmn": "3612169",
      "acml_vol": "294266",
      "cntg_vol": "454"
    },
    {
      "stck_cntg_hour": "095820",
      "bstp_nmix_prpr": "917.37",
      "bstp_nmix_prdy_vrss": "11.87",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.31",
      "acml_tr_pbmn": "3607064",
      "acml_vol": "293812",
      "cntg_vol": "515"
    },
    {
      "stck_cntg_hour": "095810",
      "bstp_nmix_prpr": "917.32",
      "bstp_nmix_prdy_vrss": "11.82",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.31",
      "acml_tr_pbmn": "3601548",
      "acml_vol": "293297",
      "cntg_vol": "545"
    },
    {
      "stck_cntg_hour": "095800",
      "bstp_nmix_prpr": "917.20",
      "bstp_nmix_prdy_vrss": "11.70",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.29",
      "acml_tr_pbmn": "3594204",
      "acml_vol": "292752",
      "cntg_vol": "394"
    },
    {
      "stck_cntg_hour": "095750",
      "bstp_nmix_prpr": "917.37",
      "bstp_nmix_prdy_vrss": "11.87",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.31",
      "acml_tr_pbmn": "3588380",
      "acml_vol": "292358",
      "cntg_vol": "392"
    },
    {
      "stck_cntg_hour": "095740",
      "bstp_nmix_prpr": "917.29",
      "bstp_nmix_prdy_vrss": "11.79",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.30",
      "acml_tr_pbmn": "3583543",
      "acml_vol": "291966",
      "cntg_vol": "383"
    },
    {
      "stck_cntg_hour": "095730",
      "bstp_nmix_prpr": "917.16",
      "bstp_nmix_prdy_vrss": "11.66",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.29",
      "acml_tr_pbmn": "3578536",
      "acml_vol": "291583",
      "cntg_vol": "372"
    },
    {
      "stck_cntg_hour": "095720",
      "bstp_nmix_prpr": "917.09",
      "bstp_nmix_prdy_vrss": "11.59",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.28",
      "acml_tr_pbmn": "3573648",
      "acml_vol": "291211",
      "cntg_vol": "387"
    },
    {
      "stck_cntg_hour": "095710",
      "bstp_nmix_prpr": "917.12",
      "bstp_nmix_prdy_vrss": "11.62",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.28",
      "acml_tr_pbmn": "3568052",
      "acml_vol": "290824",
      "cntg_vol": "481"
    },
    {
      "stck_cntg_hour": "095700",
      "bstp_nmix_prpr": "916.83",
      "bstp_nmix_prdy_vrss": "11.33",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.25",
      "acml_tr_pbmn": "3562707",
      "acml_vol": "290343",
      "cntg_vol": "376"
    },
    {
      "stck_cntg_hour": "095650",
      "bstp_nmix_prpr": "916.72",
      "bstp_nmix_prdy_vrss": "11.22",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.24",
      "acml_tr_pbmn": "3558237",
      "acml_vol": "289967",
      "cntg_vol": "457"
    },
    {
      "stck_cntg_hour": "095640",
      "bstp_nmix_prpr": "916.76",
      "bstp_nmix_prdy_vrss": "11.26",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.24",
      "acml_tr_pbmn": "3552581",
      "acml_vol": "289510",
      "cntg_vol": "596"
    },
    {
      "stck_cntg_hour": "095630",
      "bstp_nmix_prpr": "917.30",
      "bstp_nmix_prdy_vrss": "11.80",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.30",
      "acml_tr_pbmn": "3544456",
      "acml_vol": "288914",
      "cntg_vol": "406"
    },
    {
      "stck_cntg_hour": "095620",
      "bstp_nmix_prpr": "917.51",
      "bstp_nmix_prdy_vrss": "12.01",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.33",
      "acml_tr_pbmn": "3538246",
      "acml_vol": "288508",
      "cntg_vol": "579"
    },
    {
      "stck_cntg_hour": "095610",
      "bstp_nmix_prpr": "917.52",
      "bstp_nmix_prdy_vrss": "12.02",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.33",
      "acml_tr_pbmn": "3532214",
      "acml_vol": "287929",
      "cntg_vol": "495"
    },
    {
      "stck_cntg_hour": "095600",
      "bstp_nmix_prpr": "917.61",
      "bstp_nmix_prdy_vrss": "12.11",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.34",
      "acml_tr_pbmn": "3526666",
      "acml_vol": "287434",
      "cntg_vol": "407"
    },
    {
      "stck_cntg_hour": "095550",
      "bstp_nmix_prpr": "917.64",
      "bstp_nmix_prdy_vrss": "12.14",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.34",
      "acml_tr_pbmn": "3521010",
      "acml_vol": "287027",
      "cntg_vol": "614"
    },
    {
      "stck_cntg_hour": "095540",
      "bstp_nmix_prpr": "917.58",
      "bstp_nmix_prdy_vrss": "12.08",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.33",
      "acml_tr_pbmn": "3514113",
      "acml_vol": "286413",
      "cntg_vol": "414"
    },
    {
      "stck_cntg_hour": "095530",
      "bstp_nmix_prpr": "917.70",
      "bstp_nmix_prdy_vrss": "12.20",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.35",
      "acml_tr_pbmn": "3507645",
      "acml_vol": "285999",
      "cntg_vol": "527"
    },
    {
      "stck_cntg_hour": "095520",
      "bstp_nmix_prpr": "917.44",
      "bstp_nmix_prdy_vrss": "11.94",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.32",
      "acml_tr_pbmn": "3501459",
      "acml_vol": "285472",
      "cntg_vol": "556"
    },
    {
      "stck_cntg_hour": "095510",
      "bstp_nmix_prpr": "917.61",
      "bstp_nmix_prdy_vrss": "12.11",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.34",
      "acml_tr_pbmn": "3495215",
      "acml_vol": "284916",
      "cntg_vol": "584"
    },
    {
      "stck_cntg_hour": "095500",
      "bstp_nmix_prpr": "917.09",
      "bstp_nmix_prdy_vrss": "11.59",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.28",
      "acml_tr_pbmn": "3485132",
      "acml_vol": "284332",
      "cntg_vol": "657"
    },
    {
      "stck_cntg_hour": "095450",
      "bstp_nmix_prpr": "916.99",
      "bstp_nmix_prdy_vrss": "11.49",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.27",
      "acml_tr_pbmn": "3478768",
      "acml_vol": "283675",
      "cntg_vol": "708"
    },
    {
      "stck_cntg_hour": "095440",
      "bstp_nmix_prpr": "916.84",
      "bstp_nmix_prdy_vrss": "11.34",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.25",
      "acml_tr_pbmn": "3473716",
      "acml_vol": "282967",
      "cntg_vol": "477"
    },
    {
      "stck_cntg_hour": "095430",
      "bstp_nmix_prpr": "916.94",
      "bstp_nmix_prdy_vrss": "11.44",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.26",
      "acml_tr_pbmn": "3468638",
      "acml_vol": "282490",
      "cntg_vol": "538"
    },
    {
      "stck_cntg_hour": "095420",
      "bstp_nmix_prpr": "916.65",
      "bstp_nmix_prdy_vrss": "11.15",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.23",
      "acml_tr_pbmn": "3463123",
      "acml_vol": "281952",
      "cntg_vol": "644"
    },
    {
      "stck_cntg_hour": "095410",
      "bstp_nmix_prpr": "916.52",
      "bstp_nmix_prdy_vrss": "11.02",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.22",
      "acml_tr_pbmn": "3456930",
      "acml_vol": "281308",
      "cntg_vol": "557"
    },
    {
      "stck_cntg_hour": "095400",
      "bstp_nmix_prpr": "916.28",
      "bstp_nmix_prdy_vrss": "10.78",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.19",
      "acml_tr_pbmn": "3451089",
      "acml_vol": "280751",
      "cntg_vol": "551"
    },
    {
      "stck_cntg_hour": "095350",
      "bstp_nmix_prpr": "916.31",
      "bstp_nmix_prdy_vrss": "10.81",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.19",
      "acml_tr_pbmn": "3445942",
      "acml_vol": "280200",
      "cntg_vol": "825"
    },
    {
      "stck_cntg_hour": "095340",
      "bstp_nmix_prpr": "916.25",
      "bstp_nmix_prdy_vrss": "10.75",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.19",
      "acml_tr_pbmn": "3440251",
      "acml_vol": "279375",
      "cntg_vol": "594"
    },
    {
      "stck_cntg_hour": "095330",
      "bstp_nmix_prpr": "916.47",
      "bstp_nmix_prdy_vrss": "10.97",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.21",
      "acml_tr_pbmn": "3433966",
      "acml_vol": "278781",
      "cntg_vol": "896"
    },
    {
      "stck_cntg_hour": "095320",
      "bstp_nmix_prpr": "916.56",
      "bstp_nmix_prdy_vrss": "11.06",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.22",
      "acml_tr_pbmn": "3423815",
      "acml_vol": "277885",
      "cntg_vol": "670"
    },
    {
      "stck_cntg_hour": "095310",
      "bstp_nmix_prpr": "916.81",
      "bstp_nmix_prdy_vrss": "11.31",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.25",
      "acml_tr_pbmn": "3416973",
      "acml_vol": "277215",
      "cntg_vol": "818"
    },
    {
      "stck_cntg_hour": "095300",
      "bstp_nmix_prpr": "916.85",
      "bstp_nmix_prdy_vrss": "11.35",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.25",
      "acml_tr_pbmn": "3409854",
      "acml_vol": "276397",
      "cntg_vol": "777"
    },
    {
      "stck_cntg_hour": "095250",
      "bstp_nmix_prpr": "917.09",
      "bstp_nmix_prdy_vrss": "11.59",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.28",
      "acml_tr_pbmn": "3404203",
      "acml_vol": "275620",
      "cntg_vol": "474"
    },
    {
      "stck_cntg_hour": "095240",
      "bstp_nmix_prpr": "916.99",
      "bstp_nmix_prdy_vrss": "11.49",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.27",
      "acml_tr_pbmn": "3398691",
      "acml_vol": "275146",
      "cntg_vol": "457"
    },
    {
      "stck_cntg_hour": "095230",
      "bstp_nmix_prpr": "916.96",
      "bstp_nmix_prdy_vrss": "11.46",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.27",
      "acml_tr_pbmn": "3392384",
      "acml_vol": "274689",
      "cntg_vol": "315"
    },
    {
      "stck_cntg_hour": "095220",
      "bstp_nmix_prpr": "916.84",
      "bstp_nmix_prdy_vrss": "11.34",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.25",
      "acml_tr_pbmn": "3387938",
      "acml_vol": "274374",
      "cntg_vol": "391"
    },
    {
      "stck_cntg_hour": "095210",
      "bstp_nmix_prpr": "916.96",
      "bstp_nmix_prdy_vrss": "11.46",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.27",
      "acml_tr_pbmn": "3383576",
      "acml_vol": "273983",
      "cntg_vol": "543"
    },
    {
      "stck_cntg_hour": "095200",
      "bstp_nmix_prpr": "917.01",
      "bstp_nmix_prdy_vrss": "11.51",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.27",
      "acml_tr_pbmn": "3377596",
      "acml_vol": "273440",
      "cntg_vol": "503"
    },
    {
      "stck_cntg_hour": "095150",
      "bstp_nmix_prpr": "916.94",
      "bstp_nmix_prdy_vrss": "11.44",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.26",
      "acml_tr_pbmn": "3373037",
      "acml_vol": "272937",
      "cntg_vol": "407"
    },
    {
      "stck_cntg_hour": "095140",
      "bstp_nmix_prpr": "916.73",
      "bstp_nmix_prdy_vrss": "11.23",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.24",
      "acml_tr_pbmn": "3365439",
      "acml_vol": "272530",
      "cntg_vol": "487"
    },
    {
      "stck_cntg_hour": "095130",
      "bstp_nmix_prpr": "916.63",
      "bstp_nmix_prdy_vrss": "11.13",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.23",
      "acml_tr_pbmn": "3359798",
      "acml_vol": "272043",
      "cntg_vol": "418"
    },
    {
      "stck_cntg_hour": "095120",
      "bstp_nmix_prpr": "916.74",
      "bstp_nmix_prdy_vrss": "11.24",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.24",
      "acml_tr_pbmn": "3354130",
      "acml_vol": "271625",
      "cntg_vol": "439"
    },
    {
      "stck_cntg_hour": "095110",
      "bstp_nmix_prpr": "916.73",
      "bstp_nmix_prdy_vrss": "11.23",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.24",
      "acml_tr_pbmn": "3347725",
      "acml_vol": "271186",
      "cntg_vol": "459"
    },
    {
      "stck_cntg_hour": "095100",
      "bstp_nmix_prpr": "916.94",
      "bstp_nmix_prdy_vrss": "11.44",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.26",
      "acml_tr_pbmn": "3340647",
      "acml_vol": "270727",
      "cntg_vol": "393"
    },
    {
      "stck_cntg_hour": "095050",
      "bstp_nmix_prpr": "916.85",
      "bstp_nmix_prdy_vrss": "11.35",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.25",
      "acml_tr_pbmn": "3335589",
      "acml_vol": "270334",
      "cntg_vol": "358"
    },
    {
      "stck_cntg_hour": "095040",
      "bstp_nmix_prpr": "916.85",
      "bstp_nmix_prdy_vrss": "11.35",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.25",
      "acml_tr_pbmn": "3330288",
      "acml_vol": "269976",
      "cntg_vol": "390"
    },
    {
      "stck_cntg_hour": "095030",
      "bstp_nmix_prpr": "916.88",
      "bstp_nmix_prdy_vrss": "11.38",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.26",
      "acml_tr_pbmn": "3325139",
      "acml_vol": "269586",
      "cntg_vol": "399"
    },
    {
      "stck_cntg_hour": "095020",
      "bstp_nmix_prpr": "916.94",
      "bstp_nmix_prdy_vrss": "11.44",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.26",
      "acml_tr_pbmn": "3320375",
      "acml_vol": "269187",
      "cntg_vol": "463"
    },
    {
      "stck_cntg_hour": "095010",
      "bstp_nmix_prpr": "916.95",
      "bstp_nmix_prdy_vrss": "11.45",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.26",
      "acml_tr_pbmn": "3315297",
      "acml_vol": "268724",
      "cntg_vol": "416"
    },
    {
      "stck_cntg_hour": "095000",
      "bstp_nmix_prpr": "916.97",
      "bstp_nmix_prdy_vrss": "11.47",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.27",
      "acml_tr_pbmn": "3310129",
      "acml_vol": "268308",
      "cntg_vol": "411"
    },
    {
      "stck_cntg_hour": "094950",
      "bstp_nmix_prpr": "916.82",
      "bstp_nmix_prdy_vrss": "11.32",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.25",
      "acml_tr_pbmn": "3304716",
      "acml_vol": "267897",
      "cntg_vol": "505"
    },
    {
      "stck_cntg_hour": "094940",
      "bstp_nmix_prpr": "917.01",
      "bstp_nmix_prdy_vrss": "11.51",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.27",
      "acml_tr_pbmn": "3299470",
      "acml_vol": "267392",
      "cntg_vol": "432"
    },
    {
      "stck_cntg_hour": "094930",
      "bstp_nmix_prpr": "917.16",
      "bstp_nmix_prdy_vrss": "11.66",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.29",
      "acml_tr_pbmn": "3294030",
      "acml_vol": "266960",
      "cntg_vol": "416"
    },
    {
      "stck_cntg_hour": "094920",
      "bstp_nmix_prpr": "917.05",
      "bstp_nmix_prdy_vrss": "11.55",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.28",
      "acml_tr_pbmn": "3286903",
      "acml_vol": "266544",
      "cntg_vol": "530"
    },
    {
      "stck_cntg_hour": "094910",
      "bstp_nmix_prpr": "917.14",
      "bstp_nmix_prdy_vrss": "11.64",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.29",
      "acml_tr_pbmn": "3280649",
      "acml_vol": "266014",
      "cntg_vol": "562"
    },
    {
      "stck_cntg_hour": "094900",
      "bstp_nmix_prpr": "917.06",
      "bstp_nmix_prdy_vrss": "11.56",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.28",
      "acml_tr_pbmn": "3274339",
      "acml_vol": "265452",
      "cntg_vol": "598"
    },
    {
      "stck_cntg_hour": "094850",
      "bstp_nmix_prpr": "917.37",
      "bstp_nmix_prdy_vrss": "11.87",
      "prdy_vrss_sign": "2",
      "bstp_nmix_prdy_ctrt": "1.31",
      "acml_tr_pbmn": "3265635",
      "acml_vol": "264854",
      "cntg_vol": "479"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```
