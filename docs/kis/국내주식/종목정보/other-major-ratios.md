# 국내주식 기타주요비율[v1_국내주식-082]

> [국내주식] 종목정보

국내주식 기타주요비율 API입니다.
한국투자 HTS(eFriend Plus) > [0635] 재무분석종합 화면의 하단 '9. 기타주요비율' 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `fdb555c9-b958-48ad-a836-fd81f18ad73e` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/finance/other-major-ratios` |
| **Content-Type** | `` |
| **요청 포맷** | `` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID** | `FHKST66430500`, `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-02-29
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
| `tr_id` | 거래ID | String | 13 | Y | FHKST66430500 |
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
| `fid_input_iscd` | 입력 종목코드 | String | 12 | Y | 000660 : 종목코드 |
| `fid_div_cls_code` | 분류 구분 코드 | String | 2 | Y | 0: 년, 1: 분기 |
| `fid_cond_mrkt_div_code` | 조건 시장 분류 코드 | String | 2 | Y | J |

### 요청 예시

```json
{
  "fid_cond_mrkt_div_code": "J",
  "fid_input_iscd": "005930",
  "fid_div_cls_code": "1"
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
| `stac_yymm` | 결산 년월 | String | 6 | Y |  |
| `payout_rate` | 배당 성향 | String | 92 | Y | 비정상 출력되는 데이터로 무시 |
| `eva` | EVA | String | 82 | Y |  |
| `ebitda` | EBITDA | String | 82 | Y |  |
| `ev_ebitda` | EV_EBITDA | String | 82 | Y |  |

### 응답 예시

```json
{
  "output": [
    {
      "stac_yymm": "202309",
      "payout_rate": "-0.02",
      "eva": "0.00",
      "ebitda": "23464.00",
      "ev_ebitda": "0.00"
    },
    {
      "stac_yymm": "202306",
      "payout_rate": "-0.02",
      "eva": "0.00",
      "ebitda": "7851.00",
      "ev_ebitda": "0.00"
    },
    {
      "stac_yymm": "202303",
      "payout_rate": "-0.05",
      "eva": "0.00",
      "ebitda": "1574.00",
      "ev_ebitda": "0.00"
    },
    {
      "stac_yymm": "202212",
      "payout_rate": "0.05",
      "eva": "-18075.00",
      "ebitda": "209609.00",
      "ev_ebitda": "3.48"
    },
    {
      "stac_yymm": "202209",
      "payout_rate": "0.02",
      "eva": "0.00",
      "ebitda": "191549.00",
      "ev_ebitda": "0.00"
    },
    {
      "stac_yymm": "202206",
      "payout_rate": "0.02",
      "eva": "0.00",
      "ebitda": "139382.00",
      "ev_ebitda": "0.00"
    },
    {
      "stac_yymm": "202203",
      "payout_rate": "0.06",
      "eva": "0.00",
      "ebitda": "62600.00",
      "ev_ebitda": "0.00"
    },
    {
      "stac_yymm": "202112",
      "payout_rate": "0.01",
      "eva": "40178.00",
      "ebitda": "230671.00",
      "ev_ebitda": "4.59"
    },
    {
      "stac_yymm": "202109",
      "payout_rate": "0.02",
      "eva": "0.00",
      "ebitda": "160524.00",
      "ev_ebitda": "0.00"
    },
    {
      "stac_yymm": "202106",
      "payout_rate": "0.04",
      "eva": "0.00",
      "ebitda": "91711.00",
      "ev_ebitda": "0.00"
    },
    {
      "stac_yymm": "202103",
      "payout_rate": "0.12",
      "eva": "0.00",
      "ebitda": "38610.00",
      "ev_ebitda": "0.00"
    },
    {
      "stac_yymm": "202012",
      "payout_rate": "0.03",
      "eva": "3789.00",
      "ebitda": "147848.00",
      "ev_ebitda": "6.37"
    },
    {
      "stac_yymm": "202009",
      "payout_rate": "0.04",
      "eva": "0.00",
      "ebitda": "112945.00",
      "ev_ebitda": "0.00"
    },
    {
      "stac_yymm": "202006",
      "payout_rate": "0.06",
      "eva": "0.00",
      "ebitda": "75099.00",
      "ev_ebitda": "0.00"
    },
    {
      "stac_yymm": "202003",
      "payout_rate": "0.19",
      "eva": "0.00",
      "ebitda": "31351.00",
      "ev_ebitda": "0.00"
    },
    {
      "stac_yymm": "201912",
      "payout_rate": "0.06",
      "eva": "-24528.00",
      "ebitda": "113396.00",
      "ev_ebitda": "6.76"
    },
    {
      "stac_yymm": "201909",
      "payout_rate": "0.06",
      "eva": "0.00",
      "ebitda": "87849.00",
      "ev_ebitda": "0.00"
    },
    {
      "stac_yymm": "201906",
      "payout_rate": "0.07",
      "eva": "0.00",
      "ebitda": "61528.00",
      "ev_ebitda": "0.00"
    },
    {
      "stac_yymm": "201903",
      "payout_rate": "0.11",
      "eva": "0.00",
      "ebitda": "34045.00",
      "ev_ebitda": "0.00"
    },
    {
      "stac_yymm": "201812",
      "payout_rate": "0.01",
      "eva": "123025.00",
      "ebitda": "272721.00",
      "ev_ebitda": "1.62"
    },
    {
      "stac_yymm": "201809",
      "payout_rate": "0.01",
      "eva": "0.00",
      "ebitda": "210889.00",
      "ev_ebitda": "0.00"
    },
    {
      "stac_yymm": "201806",
      "payout_rate": "0.02",
      "eva": "0.00",
      "ebitda": "129647.00",
      "ev_ebitda": "0.00"
    },
    {
      "stac_yymm": "201803",
      "payout_rate": "0.04",
      "eva": "0.00",
      "ebitda": "58160.00",
      "ev_ebitda": "0.00"
    },
    {
      "stac_yymm": "201712",
      "payout_rate": "0.01",
      "eva": "77272.00",
      "ebitda": "187476.00",
      "ev_ebitda": "2.97"
    },
    {
      "stac_yymm": "201709",
      "payout_rate": "0.02",
      "eva": "0.00",
      "ebitda": "129433.00",
      "ev_ebitda": "0.00"
    },
    {
      "stac_yymm": "201706",
      "payout_rate": "0.03",
      "eva": "0.00",
      "ebitda": "78973.00",
      "ev_ebitda": "0.00"
    },
    {
      "stac_yymm": "201703",
      "payout_rate": "0.06",
      "eva": "0.00",
      "ebitda": "36327.00",
      "ev_ebitda": "0.00"
    },
    {
      "stac_yymm": "201612",
      "payout_rate": "0.04",
      "eva": "11971.00",
      "ebitda": "77332.00",
      "ev_ebitda": "4.23"
    },
    {
      "stac_yymm": "201609",
      "payout_rate": "0.09",
      "eva": "0.00",
      "ebitda": "50536.00",
      "ev_ebitda": "0.00"
    },
    {
      "stac_yymm": "201606",
      "payout_rate": "0.16",
      "eva": "0.00",
      "ebitda": "32197.00",
      "ev_ebitda": "0.00"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```
