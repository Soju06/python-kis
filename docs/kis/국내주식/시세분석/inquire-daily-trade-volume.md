# 종목별일별매수매도체결량 [v1_국내주식-056]

> [국내주식] 시세분석

종목별일별매수매도체결량 API입니다. 실전계좌의 경우, 한 번의 호출에 최대 100건까지 확인 가능합니다.
국내주식 종목의 일별 매수체결량, 매도체결량 데이터를 확인할 수 있습니다.

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `abc1a594-7f67-4a6b-9f02-67310c435b61` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/quotations/inquire-daily-trade-volume` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID** | `FHKST03010800`, `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-01-26
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
| `tr_id` | 거래ID | String | 13 | Y | FHKST03010800 |
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
| `FID_COND_MRKT_DIV_CODE` | FID 조건 시장 분류 코드 | String | 2 | Y | J: KRX, NX: NXT, UN: 통합 |
| `FID_INPUT_ISCD` | FID 입력 종목코드 | String | 12 | Y | 005930 |
| `FID_INPUT_DATE_1` | FID 입력 날짜1 | String | 10 | Y | from |
| `FID_INPUT_DATE_2` | FID 입력 날짜2 | String | 10 | Y | to |
| `FID_PERIOD_DIV_CODE` | FID 기간 분류 코드 | String | 32 | Y | D |

### 요청 예시

```json
{
  "fid_cond_mrkt_div_code": "J",
  "fid_input_iscd": "005930",
  "fid_input_date_1": "20240101",
  "fid_input_date_2": "20240126",
  "fid_period_div_code": "D"
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
| `output1` | 응답상세 | String |  | Y |  |
| `shnu_cnqn_smtn` | 매수 체결량 합계 | String | 18 | Y |  |
| `seln_cnqn_smtn` | 매도 체결량 합계 | String | 18 | Y |  |
| `output2` | 응답상세2 | Object |  | Y | array |
| `stck_bsop_date` | 거래상태정보 | String | 8 | Y |  |
| `total_seln_qty` | 총 매도 수량	 | String | 18 | Y |  |
| `total_shnu_qty` | 총 매수 수량 | String | 18 | Y |  |

### 응답 예시

```json
{
  "output1": {
    "shnu_cnqn_smtn": "4520816",
    "seln_cnqn_smtn": "5285722"
  },
  "output2": [
    {
      "stck_bsop_date": "20240126",
      "total_seln_qty": "5285722",
      "total_shnu_qty": "4520816"
    },
    {
      "stck_bsop_date": "20240125",
      "total_seln_qty": "5610781",
      "total_shnu_qty": "4008095"
    },
    {
      "stck_bsop_date": "20240124",
      "total_seln_qty": "7001409",
      "total_shnu_qty": "4628223"
    },
    {
      "stck_bsop_date": "20240123",
      "total_seln_qty": "6929612",
      "total_shnu_qty": "6221072"
    },
    {
      "stck_bsop_date": "20240122",
      "total_seln_qty": "9304203",
      "total_shnu_qty": "8269298"
    },
    {
      "stck_bsop_date": "20240119",
      "total_seln_qty": "7937786",
      "total_shnu_qty": "12024544"
    },
    {
      "stck_bsop_date": "20240118",
      "total_seln_qty": "7130130",
      "total_shnu_qty": "8051305"
    },
    {
      "stck_bsop_date": "20240117",
      "total_seln_qty": "12448352",
      "total_shnu_qty": "7781842"
    },
    {
      "stck_bsop_date": "20240116",
      "total_seln_qty": "7231456",
      "total_shnu_qty": "5660392"
    },
    {
      "stck_bsop_date": "20240115",
      "total_seln_qty": "5146657",
      "total_shnu_qty": "6242907"
    },
    {
      "stck_bsop_date": "20240112",
      "total_seln_qty": "6112124",
      "total_shnu_qty": "5706461"
    },
    {
      "stck_bsop_date": "20240111",
      "total_seln_qty": "10835895",
      "total_shnu_qty": "10905905"
    },
    {
      "stck_bsop_date": "20240110",
      "total_seln_qty": "12367976",
      "total_shnu_qty": "6256368"
    },
    {
      "stck_bsop_date": "20240109",
      "total_seln_qty": "16376304",
      "total_shnu_qty": "7458947"
    },
    {
      "stck_bsop_date": "20240108",
      "total_seln_qty": "5318849",
      "total_shnu_qty": "4631085"
    },
    {
      "stck_bsop_date": "20240105",
      "total_seln_qty": "4907468",
      "total_shnu_qty": "5219184"
    },
    {
      "stck_bsop_date": "20240104",
      "total_seln_qty": "6041013",
      "total_shnu_qty": "7038798"
    },
    {
      "stck_bsop_date": "20240103",
      "total_seln_qty": "12066549",
      "total_shnu_qty": "7713276"
    },
    {
      "stck_bsop_date": "20240102",
      "total_seln_qty": "5855872",
      "total_shnu_qty": "9333762"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```
