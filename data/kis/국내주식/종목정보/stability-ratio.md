# 국내주식 안정성비율[v1_국내주식-083]

> [국내주식] 종목정보

국내주식 안정성비율 API입니다.
한국투자 HTS(eFriend Plus) > [0635] 재무분석종합 화면의 하단 '5. 안정성비율' 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `a27c026a-744f-4ddd-9d35-c35b285af74c` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/finance/stability-ratio` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `FHKST66430600` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-02-29T09:30:14+09:00
- **최종 수정일**: 2025-05-14T13:19:41+09:00

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials Grant 절차를 준용)  법인(Access token 유효기간 3개월, Refresh token 유효기간 1년, OAuth 2.0의 Authorization Code Grant 절차를 준용) |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | FHKST66430600 |
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
| `lblt_rate` | 부채 비율 | String | 84 | Y |  |
| `bram_depn` | 차입금 의존도 | String | 92 | Y |  |
| `crnt_rate` | 유동 비율 | String | 84 | Y |  |
| `quck_rate` | 당좌 비율 | String | 84 | Y |  |

### 응답 예시

```json
{
  "output": [
    {
      "stac_yymm": "202312",
      "lblt_rate": "25.36",
      "bram_depn": "2.78",
      "crnt_rate": "258.77",
      "quck_rate": "190.59"
    },
    {
      "stac_yymm": "202309",
      "lblt_rate": "24.89",
      "bram_depn": "2.21",
      "crnt_rate": "280.39",
      "quck_rate": "205.34"
    },
    {
      "stac_yymm": "202306",
      "lblt_rate": "24.80",
      "bram_depn": "2.04",
      "crnt_rate": "288.18",
      "quck_rate": "209.76"
    },
    {
      "stac_yymm": "202303",
      "lblt_rate": "26.21",
      "bram_depn": "2.19",
      "crnt_rate": "281.95",
      "quck_rate": "210.40"
    },
    {
      "stac_yymm": "202212",
      "lblt_rate": "26.41",
      "bram_depn": "2.30",
      "crnt_rate": "278.86",
      "quck_rate": "212.24"
    },
    {
      "stac_yymm": "202209",
      "lblt_rate": "36.35",
      "bram_depn": "2.65",
      "crnt_rate": "294.17",
      "quck_rate": "226.96"
    },
    {
      "stac_yymm": "202206",
      "lblt_rate": "36.64",
      "bram_depn": "3.89",
      "crnt_rate": "283.45",
      "quck_rate": "220.96"
    },
    {
      "stac_yymm": "202203",
      "lblt_rate": "39.34",
      "bram_depn": "4.11",
      "crnt_rate": "256.86",
      "quck_rate": "204.26"
    },
    {
      "stac_yymm": "202112",
      "lblt_rate": "39.92",
      "bram_depn": "4.31",
      "crnt_rate": "247.58",
      "quck_rate": "200.62"
    },
    {
      "stac_yymm": "202109",
      "lblt_rate": "38.30",
      "bram_depn": "4.65",
      "crnt_rate": "259.91",
      "quck_rate": "213.74"
    },
    {
      "stac_yymm": "202106",
      "lblt_rate": "36.29",
      "bram_depn": "4.35",
      "crnt_rate": "263.75",
      "quck_rate": "217.39"
    },
    {
      "stac_yymm": "202103",
      "lblt_rate": "43.23",
      "bram_depn": "5.08",
      "crnt_rate": "232.11",
      "quck_rate": "198.13"
    },
    {
      "stac_yymm": "202012",
      "lblt_rate": "37.07",
      "bram_depn": "5.35",
      "crnt_rate": "262.17",
      "quck_rate": "219.79"
    },
    {
      "stac_yymm": "202009",
      "lblt_rate": "36.09",
      "bram_depn": "5.22",
      "crnt_rate": "278.77",
      "quck_rate": "234.36"
    },
    {
      "stac_yymm": "202006",
      "lblt_rate": "32.67",
      "bram_depn": "4.66",
      "crnt_rate": "300.88",
      "quck_rate": "252.96"
    },
    {
      "stac_yymm": "202003",
      "lblt_rate": "34.19",
      "bram_depn": "4.38",
      "crnt_rate": "288.34",
      "quck_rate": "244.41"
    },
    {
      "stac_yymm": "201912",
      "lblt_rate": "34.12",
      "bram_depn": "5.22",
      "crnt_rate": "284.38",
      "quck_rate": "242.41"
    },
    {
      "stac_yymm": "201909",
      "lblt_rate": "34.14",
      "bram_depn": "4.57",
      "crnt_rate": "293.89",
      "quck_rate": "245.06"
    },
    {
      "stac_yymm": "201906",
      "lblt_rate": "33.05",
      "bram_depn": "4.51",
      "crnt_rate": "292.42",
      "quck_rate": "239.74"
    },
    {
      "stac_yymm": "201903",
      "lblt_rate": "36.27",
      "bram_depn": "3.83",
      "crnt_rate": "263.37",
      "quck_rate": "216.66"
    },
    {
      "stac_yymm": "201812",
      "lblt_rate": "36.97",
      "bram_depn": "4.32",
      "crnt_rate": "252.89",
      "quck_rate": "210.93"
    },
    {
      "stac_yymm": "201809",
      "lblt_rate": "39.28",
      "bram_depn": "6.43",
      "crnt_rate": "235.97",
      "quck_rate": "198.16"
    },
    {
      "stac_yymm": "201806",
      "lblt_rate": "36.70",
      "bram_depn": "5.05",
      "crnt_rate": "239.29",
      "quck_rate": "197.58"
    },
    {
      "stac_yymm": "201803",
      "lblt_rate": "39.96",
      "bram_depn": "4.12",
      "crnt_rate": "226.86",
      "quck_rate": "188.10"
    },
    {
      "stac_yymm": "201712",
      "lblt_rate": "40.68",
      "bram_depn": "6.23",
      "crnt_rate": "218.80",
      "quck_rate": "181.61"
    },
    {
      "stac_yymm": "201709",
      "lblt_rate": "40.76",
      "bram_depn": "6.26",
      "crnt_rate": "219.61",
      "quck_rate": "178.76"
    },
    {
      "stac_yymm": "201706",
      "lblt_rate": "38.31",
      "bram_depn": "6.02",
      "crnt_rate": "226.06",
      "quck_rate": "186.68"
    },
    {
      "stac_yymm": "201703",
      "lblt_rate": "39.20",
      "bram_depn": "5.01",
      "crnt_rate": "227.44",
      "quck_rate": "188.99"
    },
    {
      "stac_yymm": "201612",
      "lblt_rate": "35.87",
      "bram_depn": "5.83",
      "crnt_rate": "258.54",
      "quck_rate": "224.99"
    },
    {
      "stac_yymm": "201609",
      "lblt_rate": "36.17",
      "bram_depn": "5.30",
      "crnt_rate": "261.93",
      "quck_rate": "225.50"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```

