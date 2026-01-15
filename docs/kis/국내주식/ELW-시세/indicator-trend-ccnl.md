# ELW 투자지표추이(체결) [국내주식-172]

> [국내주식] ELW 시세

ELW 투자지표추이(체결) API입니다.
한국투자 HTS(eFriend Plus) > [0274] ELW 투자지표추이 화면에서 "시간별 비교추이" 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `937eb413-9db9-4479-887d-4cf172dcf344` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/elw/v1/quotations/indicator-trend-ccnl` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `미지원` |
| **TR ID** | `모의투자 미지원`, `FHPEW02740100` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-04-26
- **최종 수정일**: 2025-05-07

## 요청 (Request)

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials G... |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | FHPEW02740100 |
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
| `FID_COND_MRKT_DIV_CODE` | 조건시장분류코드 | String | 2 | Y | 시장구분코드 (W) |
| `FID_INPUT_ISCD` | 입력종목코드 | String | 12 | Y | ex) 58J297(KBJ297삼성전자콜) |

### 요청 예시

```json
FID_COND_MRKT_DIV_CODE:W
FID_INPUT_ISCD:57K281
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
| `stck_cntg_hour` | 주식체결시간 | String | 6 | Y |  |
| `elw_prpr` | ELW현재가 | String | 10 | Y |  |
| `prdy_vrss_sign` | 전일대비부호 | String | 1 | Y |  |
| `prdy_vrss` | 전일대비 | String | 10 | Y |  |
| `prdy_ctrt` | 전일대비율 | String | 82 | Y |  |
| `acml_vol` | 누적거래량 | String | 18 | Y |  |
| `lvrg_val` | 레버리지값 | String | 114 | Y |  |
| `gear` | 기어링 | String | 84 | Y |  |
| `tmvl_val` | 시간가치값 | String | 132 | Y |  |
| `invl_val` | 내재가치값 | String | 132 | Y |  |
| `prit` | 패리티 | String | 112 | Y |  |
| `apprch_rate` | 접근도 | String | 112 | Y |  |

### 응답 예시

```json
{
  "output": [
    {
      "stck_cntg_hour": "125151",
      "elw_prpr": "40",
      "prdy_vrss_sign": "5",
      "prdy_vrss": "-5",
      "prdy_ctrt": "-11.11",
      "acml_vol": "827720",
      "lvrg_val": "-10.8818",
      "gear": "19.5700",
      "tmvl_val": "23.00",
      "invl_val": "17.00",
      "prit": "102.1700",
      "apprch_rate": "0.00"
    },
    {
      "stck_cntg_hour": "113228",
      "elw_prpr": "40",
      "prdy_vrss_sign": "5",
      "prdy_vrss": "-5",
      "prdy_ctrt": "-11.11",
      "acml_vol": "772020",
      "lvrg_val": "-10.7220",
      "gear": "19.5700",
      "tmvl_val": "23.00",
      "invl_val": "17.00",
      "prit": "102.1700",
      "apprch_rate": "0.00"
    },
    {
      "stck_cntg_hour": "112254",
      "elw_prpr": "40",
      "prdy_vrss_sign": "5",
      "prdy_vrss": "-5",
      "prdy_ctrt": "-11.11",
      "acml_vol": "762920",
      "lvrg_val": "-10.7587",
      "gear": "19.6000",
      "tmvl_val": "23.00",
      "invl_val": "17.00",
      "prit": "102.0400",
      "apprch_rate": "0.00"
    },
    {
      "stck_cntg_hour": "112254",
      "elw_prpr": "40",
      "prdy_vrss_sign": "5",
      "prdy_vrss": "-5",
      "prdy_ctrt": "-11.11",
      "acml_vol": "753820",
      "lvrg_val": "-10.7587",
      "gear": "19.6000",
      "tmvl_val": "23.00",
      "invl_val": "17.00",
      "prit": "102.0400",
      "apprch_rate": "0.00"
    },
    {
      "stck_cntg_hour": "112028",
      "elw_prpr": "40",
      "prdy_vrss_sign": "5",
      "prdy_vrss": "-5",
      "prdy_ctrt": "-11.11",
      "acml_vol": "707220",
      "lvrg_val": "-10.6040",
      "gear": "19.5700",
      "tmvl_val": "23.00",
      "invl_val": "17.00",
      "prit": "102.1700",
      "apprch_rate": "0.00"
    },
    {
      "stck_cntg_hour": "112028",
      "elw_prpr": "40",
      "prdy_vrss_sign": "5",
      "prdy_vrss": "-5",
      "prdy_ctrt": "-11.11",
      "acml_vol": "692220",
      "lvrg_val": "-10.6040",
      "gear": "19.5700",
      "tmvl_val": "23.00",
      "invl_val": "17.00",
      "prit": "102.1700",
      "apprch_rate": "0.00"
    },
    {
      "stck_cntg_hour": "111947",
      "elw_prpr": "40",
      "prdy_vrss_sign": "5",
      "prdy_vrss": "-5",
      "prdy_ctrt": "-11.11",
      "acml_vol": "651530",
      "lvrg_val": "-10.6040",
      "gear": "19.5700",
      "tmvl_val": "23.00",
      "invl_val": "17.00",
      "prit": "102.1700",
      "apprch_rate": "0.00"
    },
    {
      "stck_cntg_hour": "105955",
      "elw_prpr": "40",
      "prdy_vrss_sign": "5",
      "prdy_vrss": "-5",
      "prdy_ctrt": "-11.11",
      "acml_vol": "599740",
      "lvrg_val": "-10.7413",
      "gear": "19.5700",
      "tmvl_val": "23.00",
      "invl_val": "17.00",
      "prit": "102.1700",
      "apprch_rate": "0.00"
    },
    {
      "stck_cntg_hour": "105955",
      "elw_prpr": "40",
      "prdy_vrss_sign": "5",
      "prdy_vrss": "-5",
      "prdy_ctrt": "-11.11",
      "acml_vol": "559050",
      "lvrg_val": "-10.7413",
      "gear": "19.5700",
      "tmvl_val": "23.00",
      "invl_val": "17.00",
      "prit": "102.1700",
      "apprch_rate": "0.00"
    },
    {
      "stck_cntg_hour": "100603",
      "elw_prpr": "40",
      "prdy_vrss_sign": "5",
      "prdy_vrss": "-5",
      "prdy_ctrt": "-11.11",
      "acml_vol": "544050",
      "lvrg_val": "-10.6177",
      "gear": "19.6000",
      "tmvl_val": "24.00",
      "invl_val": "16.00",
      "prit": "102.0400",
      "apprch_rate": "0.00"
    },
    {
      "stck_cntg_hour": "100541",
      "elw_prpr": "40",
      "prdy_vrss_sign": "5",
      "prdy_vrss": "-5",
      "prdy_ctrt": "-11.11",
      "acml_vol": "544040",
      "lvrg_val": "-10.6177",
      "gear": "19.6000",
      "tmvl_val": "24.00",
      "invl_val": "16.00",
      "prit": "102.0400",
      "apprch_rate": "0.00"
    },
    {
      "stck_cntg_hour": "100540",
      "elw_prpr": "40",
      "prdy_vrss_sign": "5",
      "prdy_vrss": "-5",
      "prdy_ctrt": "-11.11",
      "acml_vol": "532200",
      "lvrg_val": "-10.6177",
      "gear": "19.6000",
      "tmvl_val": "24.00",
      "invl_val": "16.00",
      "prit": "102.0400",
      "apprch_rate": "0.00"
    },
    {
      "stck_cntg_hour": "100540",
      "elw_prpr": "40",
      "prdy_vrss_sign": "5",
      "prdy_vrss": "-5",
      "prdy_ctrt": "-11.11",
      "acml_vol": "531340",
      "lvrg_val": "-10.6177",
      "gear": "19.6000",
      "tmvl_val": "24.00",
      "invl_val": "16.00",
      "prit": "102.0400",
      "apprch_rate": "0.00"
    },
    {
      "stck_cntg_hour": "100507",
      "elw_prpr": "40",
      "prdy_vrss_sign": "5",
      "prdy_vrss": "-5",
      "prdy_ctrt": "-11.11",
      "acml_vol": "529040",
      "lvrg_val": "-10.6015",
      "gear": "19.5700",
      "tmvl_val": "23.00",
      "invl_val": "17.00",
      "prit": "102.1700",
      "apprch_rate": "0.00"
    },
    {
      "stck_cntg_hour": "100407",
      "elw_prpr": "40",
      "prdy_vrss_sign": "5",
      "prdy_vrss": "-5",
      "prdy_ctrt": "-11.11",
      "acml_vol": "514900",
      "lvrg_val": "-10.7188",
      "gear": "19.5700",
      "tmvl_val": "23.00",
      "invl_val": "17.00",
      "prit": "102.1700",
      "apprch_rate": "0.00"
    },
    {
      "stck_cntg_hour": "100347",
      "elw_prpr": "40",
      "prdy_vrss_sign": "5",
      "prdy_vrss": "-5",
      "prdy_ctrt": "-11.11",
      "acml_vol": "473340",
      "lvrg_val": "-10.7188",
      "gear": "19.5700",
      "tmvl_val": "23.00",
      "invl_val": "17.00",
      "prit": "102.1700",
      "apprch_rate": "0.00"
    },
    {
      "stck_cntg_hour": "095709",
      "elw_prpr": "40",
      "prdy_vrss_sign": "5",
      "prdy_vrss": "-5",
      "prdy_ctrt": "-11.11",
      "acml_vol": "472140",
      "lvrg_val": "-10.7387",
      "gear": "19.5700",
      "tmvl_val": "23.00",
      "invl_val": "17.00",
      "prit": "102.1700",
      "apprch_rate": "0.00"
    },
    {
      "stck_cntg_hour": "095709",
      "elw_prpr": "40",
      "prdy_vrss_sign": "5",
      "prdy_vrss": "-5",
      "prdy_ctrt": "-11.11",
      "acml_vol": "471730",
      "lvrg_val": "-10.7387",
      "gear": "19.5700",
      "tmvl_val": "23.00",
      "invl_val": "17.00",
      "prit": "102.1700",
      "apprch_rate": "0.00"
    },
    {
      "stck_cntg_hour": "095709",
      "elw_prpr": "40",
      "prdy_vrss_sign": "5",
      "prdy_vrss": "-5",
      "prdy_ctrt": "-11.11",
      "acml_vol": "431030",
      "lvrg_val": "-10.7387",
      "gear": "19.5700",
      "tmvl_val": "23.00",
      "invl_val": "17.00",
      "prit": "102.1700",
      "apprch_rate": "0.00"
    },
    {
      "stck_cntg_hour": "094251",
      "elw_prpr": "40",
      "prdy_vrss_sign": "5",
      "prdy_vrss": "-5",
      "prdy_ctrt": "-11.11",
      "acml_vol": "416030",
      "lvrg_val": "-10.7455",
      "gear": "19.6000",
      "tmvl_val": "23.00",
      "invl_val": "17.00",
      "prit": "102.0400",
      "apprch_rate": "0.00"
    },
    {
      "stck_cntg_hour": "094209",
      "elw_prpr": "40",
      "prdy_vrss_sign": "5",
      "prdy_vrss": "-5",
      "prdy_ctrt": "-11.11",
      "acml_vol": "414380",
      "lvrg_val": "-10.7290",
      "gear": "19.5700",
      "tmvl_val": "23.00",
      "invl_val": "17.00",
      "prit": "102.1700",
      "apprch_rate": "0.00"
    },
    {
      "stck_cntg_hour": "094209",
      "elw_prpr": "40",
      "prdy_vrss_sign": "5",
      "prdy_vrss": "-5",
      "prdy_ctrt": "-11.11",
      "acml_vol": "399380",
      "lvrg_val": "-10.7290",
      "gear": "19.5700",
      "tmvl_val": "23.00",
      "invl_val": "17.00",
      "prit": "102.1700",
      "apprch_rate": "0.00"
    },
    {
      "stck_cntg_hour": "094134",
      "elw_prpr": "40",
      "prdy_vrss_sign": "5",
      "prdy_vrss": "-5",
      "prdy_ctrt": "-11.11",
      "acml_vol": "358680",
      "lvrg_val": "-10.6168",
      "gear": "19.6000",
      "tmvl_val": "23.00",
      "invl_val": "17.00",
      "prit": "102.0400",
      "apprch_rate": "0.00"
    },
    {
      "stck_cntg_hour": "094134",
      "elw_prpr": "40",
      "prdy_vrss_sign": "5",
      "prdy_vrss": "-5",
      "prdy_ctrt": "-11.11",
      "acml_vol": "317980",
      "lvrg_val": "-10.6168",
      "gear": "19.6000",
      "tmvl_val": "23.00",
      "invl_val": "17.00",
      "prit": "102.0400",
      "apprch_rate": "0.00"
    },
    {
      "stck_cntg_hour": "094021",
      "elw_prpr": "40",
      "prdy_vrss_sign": "5",
      "prdy_vrss": "-5",
      "prdy_ctrt": "-11.11",
      "acml_vol": "302980",
      "lvrg_val": "-10.6006",
      "gear": "19.5700",
      "tmvl_val": "23.00",
      "invl_val": "17.00",
      "prit": "102.1700",
      "apprch_rate": "0.00"
    },
    {
      "stck_cntg_hour": "092950",
      "elw_prpr": "40",
      "prdy_vrss_sign": "5",
      "prdy_vrss": "-5",
      "prdy_ctrt": "-11.11",
      "acml_vol": "287980",
      "lvrg_val": "-10.8278",
      "gear": "19.5500",
      "tmvl_val": "22.00",
      "invl_val": "18.00",
      "prit": "102.3000",
      "apprch_rate": "0.00"
    },
    {
      "stck_cntg_hour": "092945",
      "elw_prpr": "40",
      "prdy_vrss_sign": "5",
      "prdy_vrss": "-5",
      "prdy_ctrt": "-11.11",
      "acml_vol": "287960",
      "lvrg_val": "-10.8278",
      "gear": "19.5500",
      "tmvl_val": "22.00",
      "invl_val": "18.00",
      "prit": "102.3000",
      "apprch_rate": "0.00"
    },
    {
      "stck_cntg_hour": "091933",
      "elw_prpr": "40",
      "prdy_vrss_sign": "5",
      "prdy_vrss": "-5",
      "prdy_ctrt": "-11.11",
      "acml_vol": "287950",
      "lvrg_val": "-10.8896",
      "gear": "19.6000",
      "tmvl_val": "23.00",
      "invl_val": "17.00",
      "prit": "102.0400",
      "apprch_rate": "0.00"
    },
    {
      "stck_cntg_hour": "091930",
      "elw_prpr": "40",
      "prdy_vrss_sign": "5",
      "prdy_vrss": "-5",
      "prdy_ctrt": "-11.11",
      "acml_vol": "232250",
      "lvrg_val": "-10.8896",
      "gear": "19.6000",
      "tmvl_val": "23.00",
      "invl_val": "17.00",
      "prit": "102.0400",
      "apprch_rate": "0.00"
    },
    {
      "stck_cntg_hour": "091653",
      "elw_prpr": "40",
      "prdy_vrss_sign": "5",
      "prdy_vrss": "-5",
      "prdy_ctrt": "-11.11",
      "acml_vol": "217250",
      "lvrg_val": "-10.7536",
      "gear": "19.6000",
      "tmvl_val": "23.00",
      "invl_val": "17.00",
      "prit": "102.0400",
      "apprch_rate": "0.00"
    },
    {
      "stck_cntg_hour": "091652",
      "elw_prpr": "40",
      "prdy_vrss_sign": "5",
      "prdy_vrss": "-5",
      "prdy_ctrt": "-11.11",
      "acml_vol": "176550",
      "lvrg_val": "-10.7536",
      "gear": "19.6000",
      "tmvl_val": "23.00",
      "invl_val": "17.00",
      "prit": "102.0400",
      "apprch_rate": "0.00"
    },
    {
      "stck_cntg_hour": "091434",
      "elw_prpr": "40",
      "prdy_vrss_sign": "5",
      "prdy_vrss": "-5",
      "prdy_ctrt": "-11.11",
      "acml_vol": "161550",
      "lvrg_val": "-10.5888",
      "gear": "19.5500",
      "tmvl_val": "24.00",
      "invl_val": "16.00",
      "prit": "102.3000",
      "apprch_rate": "0.00"
    },
    {
      "stck_cntg_hour": "091432",
      "elw_prpr": "40",
      "prdy_vrss_sign": "5",
      "prdy_vrss": "-5",
      "prdy_ctrt": "-11.11",
      "acml_vol": "160650",
      "lvrg_val": "-10.5888",
      "gear": "19.5500",
      "tmvl_val": "23.00",
      "invl_val": "17.00",
      "prit": "102.3000",
      "apprch_rate": "0.00"
    },
    {
      "stck_cntg_hour": "091314",
      "elw_prpr": "40",
      "prdy_vrss_sign": "5",
      "prdy_vrss": "-5",
      "prdy_ctrt": "-11.11",
      "acml_vol": "145650",
      "lvrg_val": "-10.7370",
      "gear": "19.5700",
      "tmvl_val": "23.00",
      "invl_val": "17.00",
      "prit": "102.1700",
      "apprch_rate": "0.00"
    },
    {
      "stck_cntg_hour": "091312",
      "elw_prpr": "40",
      "prdy_vrss_sign": "5",
      "prdy_vrss": "-5",
      "prdy_ctrt": "-11.11",
      "acml_vol": "130650",
      "lvrg_val": "-10.7370",
      "gear": "19.5700",
      "tmvl_val": "23.00",
      "invl_val": "17.00",
      "prit": "102.1700",
      "apprch_rate": "0.00"
    },
    {
      "stck_cntg_hour": "091006",
      "elw_prpr": "40",
      "prdy_vrss_sign": "5",
      "prdy_vrss": "-5",
      "prdy_ctrt": "-11.11",
      "acml_vol": "128890",
      "lvrg_val": "-12.0998",
      "gear": "22.3400",
      "tmvl_val": "23.00",
      "invl_val": "17.00",
      "prit": "102.3000",
      "apprch_rate": "0.00"
    },
    {
      "stck_cntg_hour": "090814",
      "elw_prpr": "35",
      "prdy_vrss_sign": "5",
      "prdy_vrss": "-10",
      "prdy_ctrt": "-22.22",
      "acml_vol": "108910",
      "lvrg_val": "-10.5019",
      "gear": "19.6000",
      "tmvl_val": "19.00",
      "invl_val": "16.00",
      "prit": "102.0400",
      "apprch_rate": "0.00"
    },
    {
      "stck_cntg_hour": "090800",
      "elw_prpr": "40",
      "prdy_vrss_sign": "5",
      "prdy_vrss": "-5",
      "prdy_ctrt": "-11.11",
      "acml_vol": "108900",
      "lvrg_val": "-10.4962",
      "gear": "19.6000",
      "tmvl_val": "24.00",
      "invl_val": "16.00",
      "prit": "102.0400",
      "apprch_rate": "0.00"
    },
    {
      "stck_cntg_hour": "090758",
      "elw_prpr": "40",
      "prdy_vrss_sign": "5",
      "prdy_vrss": "-5",
      "prdy_ctrt": "-11.11",
      "acml_vol": "55720",
      "lvrg_val": "-10.4962",
      "gear": "19.6000",
      "tmvl_val": "24.00",
      "invl_val": "16.00",
      "prit": "102.0400",
      "apprch_rate": "0.00"
    },
    {
      "stck_cntg_hour": "090729",
      "elw_prpr": "40",
      "prdy_vrss_sign": "5",
      "prdy_vrss": "-5",
      "prdy_ctrt": "-11.11",
      "acml_vol": "55710",
      "lvrg_val": "-10.4801",
      "gear": "19.5700",
      "tmvl_val": "23.00",
      "invl_val": "17.00",
      "prit": "102.1700",
      "apprch_rate": "0.00"
    },
    {
      "stck_cntg_hour": "090710",
      "elw_prpr": "40",
      "prdy_vrss_sign": "5",
      "prdy_vrss": "-5",
      "prdy_ctrt": "-11.11",
      "acml_vol": "20010",
      "lvrg_val": "-10.4801",
      "gear": "19.5700",
      "tmvl_val": "23.00",
      "invl_val": "17.00",
      "prit": "102.1700",
      "apprch_rate": "0.00"
    },
    {
      "stck_cntg_hour": "090504",
      "elw_prpr": "40",
      "prdy_vrss_sign": "5",
      "prdy_vrss": "-5",
      "prdy_ctrt": "-11.11",
      "acml_vol": "10",
      "lvrg_val": "-9.2509",
      "gear": "17.4600",
      "tmvl_val": "25.00",
      "invl_val": "15.00",
      "prit": "101.7800",
      "apprch_rate": "0.00"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```
