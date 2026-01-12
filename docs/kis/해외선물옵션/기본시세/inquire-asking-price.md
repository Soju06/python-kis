# 해외선물 호가 [해외선물-031]

> [해외선물옵션] 기본시세

해외선물 호가 API입니다. 
한국투자 HTS(eFriend Force) > [8602] 해외선물옵션 종합주문(Ⅰ) 화면에서 "왼쪽 호가 창" 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

(중요) 해외선물옵션시세 출력값을 해석하실 때 ffcode.mst(해외선물종목마스터 파일)에 있는 sCalcDesz(계산 소수점) 값을 활용하셔야 정확한 값을 받아오실 수 있습니다.

- ffcode.mst(해외선물종목마스터 파일) 다운로드 방법 2가지
  1) 한국투자증권 Github의 파이썬 샘플코드를 사용하여 mst 파일 다운로드 및 excel 파일로 정제   
     https://github.com/koreainvestment/open-trading-api/blob/main/stocks_info/overseas_future_code.py
   
  2) 혹은 포럼 - FAQ - 종목정보 다운로드 - 해외선물옵션 클릭하셔서 ffcode.mst(해외선물종목마스터 파일)을 다운로드 후
     Github의 헤더정보(https://github.com/koreainvestment/open-trading-api/blob/main/stocks_info/해외선물옵션정보.h)를 참고하여 해석

- 소수점 계산 시, ffcode.mst(해외선물종목마스터 파일)의 sCalcDesz(계산 소수점) 값 참고
  EX) ffcode.mst 파일의 sCalcDesz(계산 소수점) 값
       품목코드 6A 계산소수점 -4 → 시세 6882.5 수신 시 0.68825 로 해석
       품목코드 GC 계산소수점 -1 → 시세 19225 수신 시 1922.5 로 해석


[참고자료]
※ 종목코드 마스터파일 파이썬 정제코드는 한국투자증권 Github 참고 부탁드립니다.
   https://github.com/koreainvestment/open-trading-api/tree/main/stocks_info

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `1a07c21c-5fca-4d8f-a780-d861a7f80eb8` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/overseas-futureoption/v1/quotations/inquire-asking-price` |
| **Content-Type** | `` |
| **요청 포맷** | `` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID** | `모의투자 미지원`, `HHDFC86000000` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-04-19
- **최종 수정일**: 2025-04-30

## 요청 (Request)

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials G... |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | HHDFC86000000 |
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
| `SRS_CD` | 종목명 | String | 32 | Y | 종목코드 |

### 요청 예시

```json
SRS_CD:6AM24
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
| `output1` | 응답상세 | String |   | Y |  |
| `open_price` | 시가 | String | 15 | Y |  |
| `high_price` | 고가 | String | 15 | Y |  |
| `lowp_rice` | 저가 | String | 15 | Y |  |
| `last_price` | 현재가 | String | 15 | Y |  |
| `prev_price` | 전일종가 | String | 15 | Y |  |
| `vol` | 거래량 | String | 10 | Y |  |
| `prev_diff_price` | 전일대비가 | String | 15 | Y |  |
| `prev_diff_rate` | 전일대비율 | String | 10 | Y |  |
| `quot_date` | 호가수신일자 | String | 8 | Y |  |
| `quot_time` | 호가수신시각 | String | 6 | Y |  |
| `output2` | 응답상세 | Object |   | Y | array |
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
    "open_price": "         6430.0",
    "high_price": "         6466.5",
    "lowp_rice": "         6425.0",
    "last_price": "         6443.5",
    "prev_price": "         6428.5",
    "vol": "27383",
    "prev_diff_price": "             15",
    "prev_diff_rate": "      0.23",
    "quot_date": "20240422",
    "quot_time": "160201"
  },
  "output2": [
    {
      "bid_qntt": "        35",
      "bid_num": "        11",
      "bid_price": "         6443.0",
      "ask_qntt": "        11",
      "ask_num": "         7",
      "ask_price": "         6443.5"
    },
    {
      "bid_qntt": "       108",
      "bid_num": "        25",
      "bid_price": "         6442.5",
      "ask_qntt": "       137",
      "ask_num": "        23",
      "ask_price": "         6444.0"
    },
    {
      "bid_qntt": "       145",
      "bid_num": "        28",
      "bid_price": "         6442.0",
      "ask_qntt": "       120",
      "ask_num": "        24",
      "ask_price": "         6444.5"
    },
    {
      "bid_qntt": "       139",
      "bid_num": "        29",
      "bid_price": "         6441.5",
      "ask_qntt": "       142",
      "ask_num": "        21",
      "ask_price": "         6445.0"
    },
    {
      "bid_qntt": "       128",
      "bid_num": "        25",
      "bid_price": "         6441.0",
      "ask_qntt": "       127",
      "ask_num": "        20",
      "ask_price": "         6445.5"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```
