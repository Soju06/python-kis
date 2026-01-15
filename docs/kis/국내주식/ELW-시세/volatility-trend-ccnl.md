# ELW 변동성추이(체결) [국내주식-177]

> [국내주식] ELW 시세

ELW 변동성 추이(체결) API입니다. 
한국투자 HTS(eFriend Plus) > [0284] ELW 변동성 추이 화면의 "시간별" 변동성 추이 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `40403e7f-bd31-4e12-ae87-553e7be28b12` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/elw/v1/quotations/volatility-trend-ccnl` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `FHPEW02840100` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-04-12
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
| `tr_id` | 거래ID | String | 13 | Y | FHPEW02840100 |
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
| `FID_COND_MRKT_DIV_CODE` | 조건시장분류코드 | String | 2 | Y | W(Unique key) |
| `FID_INPUT_ISCD` | 입력종목코드 | String | 12 | Y | ex) 58J297(KBJ297삼성전자콜) |

### 요청 예시

```json
FID_COND_MRKT_DIV_CODE:W
FID_INPUT_ISCD:58J540
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
| `output` | 응답상세 | Object |   | Y |  |
| `stck_cntg_hour` | 주식체결시간 | String | 6 | Y |  |
| `elw_prpr` | ELW현재가 | String | 10 | Y |  |
| `prdy_vrss` | 전일대비 | String | 10 | Y |  |
| `prdy_vrss_sign` | 전일대비부호 | String | 1 | Y |  |
| `prdy_ctrt` | 전일대비율 | String | 82 | Y |  |
| `bidp` | 매수호가 | String | 10 | Y |  |
| `askp` | 매도호가 | String | 10 | Y |  |
| `acml_vol` | 누적거래량 | String | 18 | Y |  |
| `hts_ints_vltl` | HTS내재변동성 | String | 114 | Y |  |

### 응답 예시

```json
{
  "output": [
    {
      "stck_cntg_hour": "150121",
      "elw_prpr": "45",
      "prdy_vrss": "-10",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-18.18",
      "bidp": "45",
      "askp": "50",
      "acml_vol": "52690",
      "hts_ints_vltl": "33.05"
    },
    {
      "stck_cntg_hour": "140354",
      "elw_prpr": "45",
      "prdy_vrss": "-10",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-18.18",
      "bidp": "45",
      "askp": "0",
      "acml_vol": "52680",
      "hts_ints_vltl": "31.96"
    },
    {
      "stck_cntg_hour": "140340",
      "elw_prpr": "45",
      "prdy_vrss": "-10",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-18.18",
      "bidp": "45",
      "askp": "0",
      "acml_vol": "47680",
      "hts_ints_vltl": "31.96"
    },
    {
      "stck_cntg_hour": "140334",
      "elw_prpr": "45",
      "prdy_vrss": "-10",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-18.18",
      "bidp": "45",
      "askp": "50",
      "acml_vol": "47670",
      "hts_ints_vltl": "31.96"
    },
    {
      "stck_cntg_hour": "140334",
      "elw_prpr": "45",
      "prdy_vrss": "-10",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-18.18",
      "bidp": "45",
      "askp": "50",
      "acml_vol": "42690",
      "hts_ints_vltl": "31.96"
    },
    {
      "stck_cntg_hour": "140334",
      "elw_prpr": "45",
      "prdy_vrss": "-10",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-18.18",
      "bidp": "45",
      "askp": "50",
      "acml_vol": "42680",
      "hts_ints_vltl": "31.96"
    },
    {
      "stck_cntg_hour": "140334",
      "elw_prpr": "45",
      "prdy_vrss": "-10",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-18.18",
      "bidp": "45",
      "askp": "50",
      "acml_vol": "37680",
      "hts_ints_vltl": "31.96"
    },
    {
      "stck_cntg_hour": "114800",
      "elw_prpr": "50",
      "prdy_vrss": "-5",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-9.09",
      "bidp": "50",
      "askp": "55",
      "acml_vol": "37670",
      "hts_ints_vltl": "33.49"
    },
    {
      "stck_cntg_hour": "114046",
      "elw_prpr": "50",
      "prdy_vrss": "-5",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-9.09",
      "bidp": "50",
      "askp": "55",
      "acml_vol": "32670",
      "hts_ints_vltl": "26.54"
    },
    {
      "stck_cntg_hour": "104344",
      "elw_prpr": "50",
      "prdy_vrss": "-5",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-9.09",
      "bidp": "50",
      "askp": "55",
      "acml_vol": "30170",
      "hts_ints_vltl": "32.33"
    },
    {
      "stck_cntg_hour": "104344",
      "elw_prpr": "50",
      "prdy_vrss": "-5",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-9.09",
      "bidp": "50",
      "askp": "55",
      "acml_vol": "27670",
      "hts_ints_vltl": "32.33"
    },
    {
      "stck_cntg_hour": "102100",
      "elw_prpr": "55",
      "prdy_vrss": "0",
      "prdy_vrss_sign": "3",
      "prdy_ctrt": "0.00",
      "bidp": "50",
      "askp": "55",
      "acml_vol": "17750",
      "hts_ints_vltl": "31.27"
    },
    {
      "stck_cntg_hour": "095235",
      "elw_prpr": "50",
      "prdy_vrss": "-5",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-9.09",
      "bidp": "45",
      "askp": "50",
      "acml_vol": "17730",
      "hts_ints_vltl": "27.36"
    },
    {
      "stck_cntg_hour": "095235",
      "elw_prpr": "50",
      "prdy_vrss": "-5",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-9.09",
      "bidp": "45",
      "askp": "50",
      "acml_vol": "17720",
      "hts_ints_vltl": "27.36"
    },
    {
      "stck_cntg_hour": "095235",
      "elw_prpr": "50",
      "prdy_vrss": "-5",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-9.09",
      "bidp": "45",
      "askp": "50",
      "acml_vol": "7810",
      "hts_ints_vltl": "27.36"
    },
    {
      "stck_cntg_hour": "091645",
      "elw_prpr": "50",
      "prdy_vrss": "-5",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-9.09",
      "bidp": "45",
      "askp": "50",
      "acml_vol": "7720",
      "hts_ints_vltl": "25.08"
    },
    {
      "stck_cntg_hour": "091645",
      "elw_prpr": "50",
      "prdy_vrss": "-5",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-9.09",
      "bidp": "45",
      "askp": "50",
      "acml_vol": "7630",
      "hts_ints_vltl": "25.08"
    },
    {
      "stck_cntg_hour": "091502",
      "elw_prpr": "50",
      "prdy_vrss": "-5",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-9.09",
      "bidp": "45",
      "askp": "50",
      "acml_vol": "7620",
      "hts_ints_vltl": "27.27"
    },
    {
      "stck_cntg_hour": "091222",
      "elw_prpr": "50",
      "prdy_vrss": "-5",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-9.09",
      "bidp": "50",
      "askp": "55",
      "acml_vol": "120",
      "hts_ints_vltl": "32.07"
    },
    {
      "stck_cntg_hour": "091222",
      "elw_prpr": "50",
      "prdy_vrss": "-5",
      "prdy_vrss_sign": "5",
      "prdy_ctrt": "-9.09",
      "bidp": "50",
      "askp": "55",
      "acml_vol": "110",
      "hts_ints_vltl": "32.07"
    },
    {
      "stck_cntg_hour": "090223",
      "elw_prpr": "55",
      "prdy_vrss": "0",
      "prdy_vrss_sign": "3",
      "prdy_ctrt": "0.00",
      "bidp": "55",
      "askp": "0",
      "acml_vol": "100",
      "hts_ints_vltl": "22.69"
    },
    {
      "stck_cntg_hour": "090223",
      "elw_prpr": "55",
      "prdy_vrss": "0",
      "prdy_vrss_sign": "3",
      "prdy_ctrt": "0.00",
      "bidp": "50",
      "askp": "55",
      "acml_vol": "10",
      "hts_ints_vltl": "22.69"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```

