# 국내주식 수익성비율[v1_국내주식-081]

> [국내주식] 종목정보

국내주식 수익성비율 API입니다.
한국투자 HTS(eFriend Plus) > [0635] 재무분석종합 화면의 하단 '4. 수익성비율' 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `a4275fc3-384b-4b24-bf3a-38b72786b5ab` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/finance/profit-ratio` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `FHKST66430400` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-02-29T09:28:38+09:00
- **최종 수정일**: 2025-05-14T13:19:20+09:00

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials Grant 절차를 준용)  법인(Access token 유효기간 3개월, Refresh token 유효기간 1년, OAuth 2.0의 Authorization Code Grant 절차를 준용) |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | FHKST66430400 |
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
| `FID_DIV_CLS_CODE` | 분류 구분 코드 | String | 2 | Y | 0: 년, 1: 분기 |
| `fid_cond_mrkt_div_code` | 조건 시장 분류 코드 | String | 2 | Y | J |

### 요청 예시

```json
{
  "fid_cond_mrkt_div_code": "J",
  "fid_input_iscd": "005930",
  "fid_div_cls_code": "1"
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
| `stac_yymm` | 결산 년월 | String | 6 | Y |  |
| `cptl_ntin_rate` | 총자본 순이익율 | String | 92 | Y |  |
| `self_cptl_ntin_inrt` | 자기자본 순이익율 | String | 92 | Y |  |
| `sale_ntin_rate` | 매출액 순이익율 | String | 92 | Y |  |
| `sale_totl_rate` | 매출액 총이익율 | String | 92 | Y |  |

### 응답 예시

```json
{
  "output": [
    {
      "stac_yymm": "202312",
      "cptl_ntin_rate": "3.43",
      "self_cptl_ntin_inrt": "4.14",
      "sale_ntin_rate": "5.98",
      "sale_totl_rate": "30.33"
    },
    {
      "stac_yymm": "202309",
      "cptl_ntin_rate": "2.70",
      "self_cptl_ntin_inrt": "3.22",
      "sale_ntin_rate": "4.78",
      "sale_totl_rate": "29.76"
    },
    {
      "stac_yymm": "202306",
      "cptl_ntin_rate": "1.47",
      "self_cptl_ntin_inrt": "1.70",
      "sale_ntin_rate": "2.67",
      "sale_totl_rate": "29.17"
    },
    {
      "stac_yymm": "202303",
      "cptl_ntin_rate": "1.40",
      "self_cptl_ntin_inrt": "1.61",
      "sale_ntin_rate": "2.47",
      "sale_totl_rate": "27.83"
    },
    {
      "stac_yymm": "202212",
      "cptl_ntin_rate": "12.72",
      "self_cptl_ntin_inrt": "17.07",
      "sale_ntin_rate": "18.41",
      "sale_totl_rate": "37.12"
    },
    {
      "stac_yymm": "202209",
      "cptl_ntin_rate": "9.46",
      "self_cptl_ntin_inrt": "13.18",
      "sale_ntin_rate": "13.73",
      "sale_totl_rate": "38.98"
    },
    {
      "stac_yymm": "202206",
      "cptl_ntin_rate": "10.25",
      "self_cptl_ntin_inrt": "14.36",
      "sale_ntin_rate": "14.47",
      "sale_totl_rate": "39.77"
    },
    {
      "stac_yymm": "202203",
      "cptl_ntin_rate": "10.46",
      "self_cptl_ntin_inrt": "14.77",
      "sale_ntin_rate": "14.56",
      "sale_totl_rate": "39.48"
    },
    {
      "stac_yymm": "202112",
      "cptl_ntin_rate": "9.92",
      "self_cptl_ntin_inrt": "13.92",
      "sale_ntin_rate": "14.27",
      "sale_totl_rate": "40.48"
    },
    {
      "stac_yymm": "202109",
      "cptl_ntin_rate": "9.83",
      "self_cptl_ntin_inrt": "13.72",
      "sale_ntin_rate": "14.32",
      "sale_totl_rate": "40.18"
    },
    {
      "stac_yymm": "202106",
      "cptl_ntin_rate": "8.79",
      "self_cptl_ntin_inrt": "12.21",
      "sale_ntin_rate": "13.00",
      "sale_totl_rate": "39.12"
    },
    {
      "stac_yymm": "202103",
      "cptl_ntin_rate": "7.41",
      "self_cptl_ntin_inrt": "10.64",
      "sale_ntin_rate": "10.92",
      "sale_totl_rate": "36.53"
    },
    {
      "stac_yymm": "202012",
      "cptl_ntin_rate": "7.23",
      "self_cptl_ntin_inrt": "9.99",
      "sale_ntin_rate": "11.15",
      "sale_totl_rate": "38.98"
    },
    {
      "stac_yymm": "202009",
      "cptl_ntin_rate": "7.25",
      "self_cptl_ntin_inrt": "10.02",
      "sale_ntin_rate": "11.30",
      "sale_totl_rate": "39.13"
    },
    {
      "stac_yymm": "202006",
      "cptl_ntin_rate": "5.88",
      "self_cptl_ntin_inrt": "8.04",
      "sale_ntin_rate": "9.64",
      "sale_totl_rate": "38.39"
    },
    {
      "stac_yymm": "202003",
      "cptl_ntin_rate": "5.50",
      "self_cptl_ntin_inrt": "7.62",
      "sale_ntin_rate": "8.83",
      "sale_totl_rate": "37.09"
    },
    {
      "stac_yymm": "201912",
      "cptl_ntin_rate": "6.28",
      "self_cptl_ntin_inrt": "8.69",
      "sale_ntin_rate": "9.44",
      "sale_totl_rate": "36.09"
    },
    {
      "stac_yymm": "201909",
      "cptl_ntin_rate": "6.36",
      "self_cptl_ntin_inrt": "8.76",
      "sale_ntin_rate": "9.68",
      "sale_totl_rate": "36.26"
    },
    {
      "stac_yymm": "201906",
      "cptl_ntin_rate": "5.99",
      "self_cptl_ntin_inrt": "8.30",
      "sale_ntin_rate": "9.42",
      "sale_totl_rate": "36.70"
    },
    {
      "stac_yymm": "201903",
      "cptl_ntin_rate": "5.90",
      "self_cptl_ntin_inrt": "8.41",
      "sale_ntin_rate": "9.63",
      "sale_totl_rate": "37.49"
    },
    {
      "stac_yymm": "201812",
      "cptl_ntin_rate": "13.83",
      "self_cptl_ntin_inrt": "19.63",
      "sale_ntin_rate": "18.19",
      "sale_totl_rate": "45.69"
    },
    {
      "stac_yymm": "201809",
      "cptl_ntin_rate": "14.98",
      "self_cptl_ntin_inrt": "21.47",
      "sale_ntin_rate": "19.45",
      "sale_totl_rate": "46.68"
    },
    {
      "stac_yymm": "201806",
      "cptl_ntin_rate": "14.66",
      "self_cptl_ntin_inrt": "20.88",
      "sale_ntin_rate": "19.10",
      "sale_totl_rate": "46.92"
    },
    {
      "stac_yymm": "201803",
      "cptl_ntin_rate": "15.22",
      "self_cptl_ntin_inrt": "21.96",
      "sale_ntin_rate": "19.30",
      "sale_totl_rate": "47.31"
    },
    {
      "stac_yymm": "201712",
      "cptl_ntin_rate": "14.96",
      "self_cptl_ntin_inrt": "21.01",
      "sale_ntin_rate": "17.61",
      "sale_totl_rate": "46.03"
    },
    {
      "stac_yymm": "201709",
      "cptl_ntin_rate": "14.28",
      "self_cptl_ntin_inrt": "20.06",
      "sale_ntin_rate": "17.24",
      "sale_totl_rate": "46.11"
    },
    {
      "stac_yymm": "201706",
      "cptl_ntin_rate": "13.89",
      "self_cptl_ntin_inrt": "19.25",
      "sale_ntin_rate": "16.80",
      "sale_totl_rate": "45.71"
    },
    {
      "stac_yymm": "201703",
      "cptl_ntin_rate": "11.68",
      "self_cptl_ntin_inrt": "16.21",
      "sale_ntin_rate": "15.20",
      "sale_totl_rate": "44.30"
    },
    {
      "stac_yymm": "201612",
      "cptl_ntin_rate": "9.01",
      "self_cptl_ntin_inrt": "12.48",
      "sale_ntin_rate": "11.26",
      "sale_totl_rate": "40.42"
    },
    {
      "stac_yymm": "201609",
      "cptl_ntin_rate": "8.57",
      "self_cptl_ntin_inrt": "11.94",
      "sale_ntin_rate": "10.53",
      "sale_totl_rate": "39.82"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```

