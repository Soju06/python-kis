# 해외옵션 호가 [해외선물-033]

> [해외선물옵션] 기본시세

해외옵션 호가 API입니다.
한국투자 HTS(eFriend Force) > [5501] 해외선물옵션 현재가 화면 의 "왼쪽 상단 현재가" 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `506cd6e9-97d9-4c4b-82bc-6a6c13586885` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/overseas-futureoption/v1/quotations/opt-asking-price` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `HHDFO86000000` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-05-24
- **최종 수정일**: 2025-04-30

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials G... |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | HHDFO86000000 |
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
| `SRS_CD` | 종목명 | String | 8 | Y | 예)OESM24 C5340 |

### 요청 예시

```json
SRS_CD:OTXM24 C22000
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
| `output1` | 응답상세 | String |   | Y |  |
| `open_price` | 시가 | String | 15 | Y |  |
| `high_price` | 고가 | String | 15 | Y |  |
| `lowp_rice` | 저가 | String | 15 | Y |  |
| `last_price` | 현재가 | String | 15 | Y |  |
| `sttl_price` | 정산가 | String | 15 | Y |  |
| `vol` | 거래량 | String | 10 | Y |  |
| `prev_diff_price` | 전일대비가 | String | 15 | Y |  |
| `prev_diff_rate` | 전일대비율 | String | 10 | Y |  |
| `quot_date` | 호가수신일자 | String | 8 | Y |  |
| `quot_time` | 호가수신시각 | String | 6 | Y |  |
| `output2` | 응답상세 | Object |   | Y | array (1호가~ 5호가 순서대로 표시) |
| `bid_qntt` | 매수수량 | String | 10 | Y |  |
| `bid_num` | 매수번호 | String | 10 | Y |  |
| `bid_price` | 매수호가 | String | 15 | Y |  |
| `ask_qntt` | 매도수량 | String | 10 | Y |  |
| `ask_num` | 매도번호 | String | 10 | Y |  |
| `ask_price` | 매도호가 | String | 15 | Y |  |

### 응답 예시

```json
{
  "output1": {
    "open_price": "          282.0",
    "high_price": "          295.0",
    "lowp_rice": "          280.0",
    "last_price": "          290.0",
    "sttl_price": "          288.0",
    "vol": "       100",
    "prev_diff_price": "            2.0",
    "prev_diff_rate": "      0.69",
    "quot_date": "20240528",
    "quot_time": "184601"
  },
  "output2": [
    {
      "bid_qntt": "        37",
      "bid_num": "         0",
      "bid_price": "          288.0",
      "ask_qntt": "         4",
      "ask_num": "         0",
      "ask_price": "          290.0"
    },
    {
      "bid_qntt": "        43",
      "bid_num": "         0",
      "bid_price": "          287.0",
      "ask_qntt": "         8",
      "ask_num": "         0",
      "ask_price": "          291.0"
    },
    {
      "bid_qntt": "        20",
      "bid_num": "         0",
      "bid_price": "          285.0",
      "ask_qntt": "        54",
      "ask_num": "         0",
      "ask_price": "          292.0"
    },
    {
      "bid_qntt": "         4",
      "bid_num": "         0",
      "bid_price": "          280.0",
      "ask_qntt": "        21",
      "ask_num": "         0",
      "ask_price": "          295.0"
    },
    {
      "bid_qntt": "         5",
      "bid_num": "         0",
      "bid_price": "          276.0",
      "ask_qntt": "         1",
      "ask_num": "         0",
      "ask_price": "          296.0"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```

