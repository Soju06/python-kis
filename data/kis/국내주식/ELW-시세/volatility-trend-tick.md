# ELW 변동성 추이(틱) [국내주식-180]

> [국내주식] ELW 시세

ELW 변동성 추이(틱) API입니다.
한국투자 HTS(eFriend Plus) > [0284] ELW 변동성 추이 화면의 "틱 차트" 변동성 추이 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `f1ce6099-5bf2-4b4e-915e-e0c7020af4bf` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/elw/v1/quotations/volatility-trend-tick` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `미지원` |
| **TR ID (실전)** | `FHPEW02840400` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-05-03T12:45:26+09:00
- **최종 수정일**: 2025-05-07T09:37:38+09:00

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials Grant 절차를 준용)  법인(Access token 유효기간 3개월, Refresh token 유효기간 1년, OAuth 2.0의 Authorization Code Grant 절차를 준용) |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | FHPEW02840400 |
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
FID_INPUT_ISCD:57K281
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
| `bsop_date` | 주식영업일자 | String | 8 | Y |  |
| `stck_cntg_hour` | ELW현재가 | String | 6 | Y |  |
| `elw_prpr` | 전일대비 | String | 10 | Y |  |
| `hts_ints_vltl` | 전일대비부호 | String | 114 | Y |  |

### 응답 예시

```json
{
  "output": [
    {
      "bsop_date": "20240507",
      "stck_cntg_hour": "150619",
      "elw_prpr": "25",
      "hts_ints_vltl": "33.03"
    },
    {
      "bsop_date": "20240507",
      "stck_cntg_hour": "150032",
      "elw_prpr": "25",
      "hts_ints_vltl": "28.44"
    },
    {
      "bsop_date": "20240507",
      "stck_cntg_hour": "150031",
      "elw_prpr": "25",
      "hts_ints_vltl": "28.44"
    },
    {
      "bsop_date": "20240507",
      "stck_cntg_hour": "145743",
      "elw_prpr": "25",
      "hts_ints_vltl": "33.44"
    },
    {
      "bsop_date": "20240507",
      "stck_cntg_hour": "145743",
      "elw_prpr": "25",
      "hts_ints_vltl": "33.44"
    },
    {
      "bsop_date": "20240507",
      "stck_cntg_hour": "133437",
      "elw_prpr": "25",
      "hts_ints_vltl": "32.47"
    },
    {
      "bsop_date": "20240507",
      "stck_cntg_hour": "133434",
      "elw_prpr": "25",
      "hts_ints_vltl": "32.47"
    },
    {
      "bsop_date": "20240507",
      "stck_cntg_hour": "132342",
      "elw_prpr": "25",
      "hts_ints_vltl": "31.60"
    },
    {
      "bsop_date": "20240507",
      "stck_cntg_hour": "093016",
      "elw_prpr": "30",
      "hts_ints_vltl": "28.62"
    },
    {
      "bsop_date": "20240507",
      "stck_cntg_hour": "092952",
      "elw_prpr": "25",
      "hts_ints_vltl": "28.62"
    },
    {
      "bsop_date": "20240507",
      "stck_cntg_hour": "091704",
      "elw_prpr": "30",
      "hts_ints_vltl": "33.03"
    },
    {
      "bsop_date": "20240507",
      "stck_cntg_hour": "090900",
      "elw_prpr": "30",
      "hts_ints_vltl": "33.02"
    },
    {
      "bsop_date": "20240507",
      "stck_cntg_hour": "090735",
      "elw_prpr": "30",
      "hts_ints_vltl": "28.59"
    },
    {
      "bsop_date": "20240507",
      "stck_cntg_hour": "090712",
      "elw_prpr": "30",
      "hts_ints_vltl": "28.59"
    },
    {
      "bsop_date": "20240507",
      "stck_cntg_hour": "090710",
      "elw_prpr": "30",
      "hts_ints_vltl": "28.59"
    },
    {
      "bsop_date": "20240507",
      "stck_cntg_hour": "090555",
      "elw_prpr": "30",
      "hts_ints_vltl": "33.46"
    },
    {
      "bsop_date": "20240507",
      "stck_cntg_hour": "090553",
      "elw_prpr": "30",
      "hts_ints_vltl": "33.46"
    },
    {
      "bsop_date": "20240507",
      "stck_cntg_hour": "090511",
      "elw_prpr": "30",
      "hts_ints_vltl": "33.46"
    },
    {
      "bsop_date": "20240507",
      "stck_cntg_hour": "090445",
      "elw_prpr": "30",
      "hts_ints_vltl": "36.51"
    },
    {
      "bsop_date": "20240507",
      "stck_cntg_hour": "090445",
      "elw_prpr": "30",
      "hts_ints_vltl": "36.51"
    },
    {
      "bsop_date": "20240507",
      "stck_cntg_hour": "090445",
      "elw_prpr": "30",
      "hts_ints_vltl": "36.51"
    },
    {
      "bsop_date": "20240507",
      "stck_cntg_hour": "090320",
      "elw_prpr": "35",
      "hts_ints_vltl": "36.51"
    },
    {
      "bsop_date": "20240507",
      "stck_cntg_hour": "090030",
      "elw_prpr": "40",
      "hts_ints_vltl": "32.97"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```

