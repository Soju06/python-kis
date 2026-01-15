# 국내 증시자금 종합 [국내주식-193]

> [국내주식] 시세분석

국내 증시자금 종합 API입니다. 
한국투자 HTS(eFriend Plus) > [0470] 증시자금 종합 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다. (단위: 억원)

※ 해당자료는 금융투자협회의 자료를 제공하고 있으며, 오류와 지연이 발생할 수 있습니다.
※ 위 정보에 의한 투자판단의 최종책임은 정보이용자에게 있으며, 당사와 한국금융투자협회는 어떠한 법적인 책임도 지지 않사오니 투자에 참고로만 이용하시기 바랍니다.

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `b8c4fb5f-c3ef-4f6c-bfab-5471f43fb0ae` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/quotations/mktfunds` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `미지원` |
| **TR ID** | `FHKST649100C0`, `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-05-03
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
| `tr_id` | 거래ID | String | 13 | Y | FHKST649100C0 |
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
| `FID_INPUT_DATE_1` | 입력날짜1 | String | 10 | Y |  |

### 요청 예시

```json
FID_INPUT_DATE_1:20240503
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
| `bsop_date` | 영업일자 | String | 8 | Y |  |
| `bstp_nmix_prpr` | 업종지수현재가 | String | 112 | Y |  |
| `bstp_nmix_prdy_vrss` | 업종지수전일대비 | String | 112 | Y |  |
| `prdy_vrss_sign` | 전일대비부호 | String | 1 | Y | 1. 상한 2. 상승 3. 보합 4. 하한 5. 하락 |
| `prdy_ctrt` | 전일대비율 | String | 82 | Y |  |
| `hts_avls` | HTS시가총액 | String | 18 | Y | 단위: 백만원 |
| `cust_dpmn_amt` | 고객예탁금금액 | String | 18 | Y | 단위: 억원 |
| `cust_dpmn_amt_prdy_vrss` | 고객예탁금금액전일대비 | String | 18 | Y |  |
| `amt_tnrt` | 금액회전율 | String | 84 | Y |  |
| `uncl_amt` | 미수금액 | String | 18 | Y | 단위: 억원 |
| `crdt_loan_rmnd` | 신용융자잔고 | String | 18 | Y | 단위: 억원 |
| `futs_tfam_amt` | 선물예수금금액 | String | 18 | Y | 단위: 억원 |
| `sttp_amt` | 주식형금액 | String | 18 | Y | 단위: 억원 |
| `mxtp_amt` | 혼합형금액 | String | 18 | Y | 단위: 억원 |
| `bntp_amt` | 채권형금액 | String | 18 | Y | 단위: 억원 |
| `mmf_amt` | MMF금액 | String | 18 | Y | 단위: 억원 |
| `secu_lend_amt` | 담보대출잔고금액 | String | 18 | Y | 단위: 억원 |

### 응답 예시

```json
{
    "output": [
        {
            "bsop_date": "20240430",
            "bstp_nmix_prpr": "2692.06",
            "bstp_nmix_prdy_vrss": "4.62",
            "prdy_vrss_sign": "2",
            "prdy_ctrt": "100.17",
            "hts_avls": "2193843858",
            "cust_dpmn_amt": "572306",
            "cust_dpmn_amt_prdy_vrss": "4435",
            "amt_tnrt": "33.87",
            "uncl_amt": "9289",
            "crdt_loan_rmnd": "191730",
            "futs_tfam_amt": "112724",
            "sttp_amt": "1112330",
            "mxtp_amt": "264052",
            "bntp_amt": "1497053",
            "mmf_amt": "1971372",
            "secu_lend_amt": "199663"
        },
        {
            "bsop_date": "20240429",
            "bstp_nmix_prpr": "2687.44",
            "bstp_nmix_prdy_vrss": "31.11",
            "prdy_vrss_sign": "2",
            "prdy_ctrt": "101.17",
            "hts_avls": "2189691726",
            "cust_dpmn_amt": "567872",
            "cust_dpmn_amt_prdy_vrss": "2770",
            "amt_tnrt": "31.81",
            "uncl_amt": "9770",
            "crdt_loan_rmnd": "191876",
            "futs_tfam_amt": "114477",
            "sttp_amt": "1108725",
            "mxtp_amt": "264014",
            "bntp_amt": "1490082",
            "mmf_amt": "1995789",
            "secu_lend_amt": "205197"
        },
        {
            "bsop_date": "20240426",
            "bstp_nmix_prpr": "2656.33",
            "bstp_nmix_prdy_vrss": "27.71",
            "prdy_vrss_sign": "2",
            "prdy_ctrt": "101.05",
            "hts_avls": "2164477451",
            "cust_dpmn_amt": "565102",
            "cust_dpmn_amt_prdy_vrss": "8389",
            "amt_tnrt": "32.27",
            "uncl_amt": "9224",
            "crdt_loan_rmnd": "190610",
            "futs_tfam_amt": "114228",
            "sttp_amt": "1099696",
            "mxtp_amt": "263514",
            "bntp_amt": "1486148",
            "mmf_amt": "2014269",
            "secu_lend_amt": "200841"
        },
        {
            "bsop_date": "20240425",
            "bstp_nmix_prpr": "2628.62",
            "bstp_nmix_prdy_vrss": "-47.13",
            "prdy_vrss_sign": "5",
            "prdy_ctrt": "98.24",
            "hts_avls": "2142440795",
            "cust_dpmn_amt": "556713",
            "cust_dpmn_amt_prdy_vrss": "9753",
            "amt_tnrt": "30.55",
            "uncl_amt": "9460",
            "crdt_loan_rmnd": "190653",
            "futs_tfam_amt": "119102",
            "sttp_amt": "1091640",
            "mxtp_amt": "263032",
            "bntp_amt": "1486119",
            "mmf_amt": "2034032",
            "secu_lend_amt": "197721"
        },
        {
            "bsop_date": "20240424",
            "bstp_nmix_prpr": "2675.75",
            "bstp_nmix_prdy_vrss": "52.73",
            "prdy_vrss_sign": "2",
            "prdy_ctrt": "102.01",
            "hts_avls": "2180629130",
            "cust_dpmn_amt": "546960",
            "cust_dpmn_amt_prdy_vrss": "-11693",
            "amt_tnrt": "33.20",
            "uncl_amt": "9503",
            "crdt_loan_rmnd": "189912",
            "futs_tfam_amt": "118058",
            "sttp_amt": "1095621",
            "mxtp_amt": "262947",
            "bntp_amt": "1484163",
            "mmf_amt": "2055945",
            "secu_lend_amt": "199263"
        },
        {
            "bsop_date": "20240423",
            "bstp_nmix_prpr": "2623.02",
            "bstp_nmix_prdy_vrss": "-6.42",
            "prdy_vrss_sign": "5",
            "prdy_ctrt": "99.76",
            "hts_avls": "2137640963",
            "cust_dpmn_amt": "558653",
            "cust_dpmn_amt_prdy_vrss": "-7143",
            "amt_tnrt": "31.04",
            "uncl_amt": "9454",
            "crdt_loan_rmnd": "190361",
            "futs_tfam_amt": "117715",
            "sttp_amt": "1083125",
            "mxtp_amt": "262801",
            "bntp_amt": "1481191",
            "mmf_amt": "2059132",
            "secu_lend_amt": "198055"
        },
        {
            "bsop_date": "20240422",
            "bstp_nmix_prpr": "2629.44",
            "bstp_nmix_prdy_vrss": "37.58",
            "prdy_vrss_sign": "2",
            "prdy_ctrt": "101.45",
            "hts_avls": "2143157216",
            "cust_dpmn_amt": "565797",
            "cust_dpmn_amt_prdy_vrss": "11043",
            "amt_tnrt": "33.64",
            "uncl_amt": "9312",
            "crdt_loan_rmnd": "190326",
            "futs_tfam_amt": "118954",
            "sttp_amt": "1085224",
            "mxtp_amt": "262713",
            "bntp_amt": "1477973",
            "mmf_amt": "2083552",
            "secu_lend_amt": "197038"
        },
        {
            "bsop_date": "20240419",
            "bstp_nmix_prpr": "2591.86",
            "bstp_nmix_prdy_vrss": "-42.84",
            "prdy_vrss_sign": "5",
            "prdy_ctrt": "98.37",
            "hts_avls": "2113960518",
            "cust_dpmn_amt": "554754",
            "cust_dpmn_amt_prdy_vrss": "4154",
            "amt_tnrt": "41.58",
            "uncl_amt": "9806",
            "crdt_loan_rmnd": "190624",
            "futs_tfam_amt": "119487",
            "sttp_amt": "1083386",
            "mxtp_amt": "262645",
            "bntp_amt": "1475873",
            "mmf_amt": "2087866",
            "secu_lend_amt": "198926"
        },
        {
            "bsop_date": "20240418",
            "bstp_nmix_prpr": "2634.70",
            "bstp_nmix_prdy_vrss": "50.52",
            "prdy_vrss_sign": "2",
            "prdy_ctrt": "101.95",
            "hts_avls": "2148591607",
            "cust_dpmn_amt": "550600",
            "cust_dpmn_amt_prdy_vrss": "-2090",
            "amt_tnrt": "33.32",
            "uncl_amt": "9932",
            "crdt_loan_rmnd": "191816",
            "futs_tfam_amt": "115974",
            "sttp_amt": "1088431",
            "mxtp_amt": "261979",
            "bntp_amt": "1472540",
            "mmf_amt": "2096220",
            "secu_lend_amt": "199652"
        },
        {
            "bsop_date": "20240417",
            "bstp_nmix_prpr": "2584.18",
            "bstp_nmix_prdy_vrss": "-25.45",
            "prdy_vrss_sign": "5",
            "prdy_ctrt": "99.02",
            "hts_avls": "2108636206",
            "cust_dpmn_amt": "552690",
            "cust_dpmn_amt_prdy_vrss": "-23278",
            "amt_tnrt": "32.09",
            "uncl_amt": "9653",
            "crdt_loan_rmnd": "194102",
            "futs_tfam_amt": "114956",
            "sttp_amt": "1086475",
            "mxtp_amt": "261671",
            "bntp_amt": "1472499",
            "mmf_amt": "2109537",
            "secu_lend_amt": "198961"
        },
        {
            "bsop_date": "20240416",
            "bstp_nmix_prpr": "2609.63",
            "bstp_nmix_prdy_vrss": "-60.80",
            "prdy_vrss_sign": "5",
            "prdy_ctrt": "97.72",
            "hts_avls": "2129095534",
            "cust_dpmn_amt": "575969",
            "cust_dpmn_amt_prdy_vrss": "9287",
            "amt_tnrt": "35.91",
            "uncl_amt": "9583",
            "crdt_loan_rmnd": "193485",
            "futs_tfam_amt": "116520",
            "sttp_amt": "1092931",
            "mxtp_amt": "261632",
            "bntp_amt": "1471604",
            "mmf_amt": "2083522",
            "secu_lend_amt": "198067"
        },...
        {
            "bsop_date": "20231204",
            "bstp_nmix_prpr": "2514.95",
            "bstp_nmix_prdy_vrss": "9.94",
            "prdy_vrss_sign": "2",
            "prdy_ctrt": "100.40",
            "hts_avls": "2012605764",
            "cust_dpmn_amt": "483930",
            "cust_dpmn_amt_prdy_vrss": "-2751",
            "amt_tnrt": "39.82",
            "uncl_amt": "9477",
            "crdt_loan_rmnd": "172738",
            "futs_tfam_amt": "111758",
            "sttp_amt": "1020141",
            "mxtp_amt": "241287",
            "bntp_amt": "1372663",
            "mmf_amt": "1937326",
            "secu_lend_amt": "212773"
        }
    ],
    "rt_cd": "0",
    "msg_cd": "MCA00000",
    "msg1": "정상처리 되었습니다."
}
```
