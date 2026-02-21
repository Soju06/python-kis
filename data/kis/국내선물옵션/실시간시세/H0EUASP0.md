# KRX야간옵션 실시간호가 [실시간-033]

> [국내선물옵션] 실시간시세

[참고자료]

실시간시세(웹소켓) 파이썬 샘플코드는 한국투자증권 Github 참고 부탁드립니다.
https://github.com/koreainvestment/open-trading-api/blob/main/websocket/python/ws_domestic_overseas_all.py

실시간시세(웹소켓) API 사용방법에 대한 자세한 설명은 한국투자증권 Wikidocs 참고 부탁드립니다.
https://wikidocs.net/book/7847 (국내주식 업데이트 완료, 추후 해외주식·국내선물옵션 업데이트 예정)

종목코드 마스터파일 파이썬 정제코드는 한국투자증권 Github 참고 부탁드립니다.
https://github.com/koreainvestment/open-trading-api/tree/main/stocks_info


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `8e68c76f-58df-4a8e-ad57-09ec4fcea8ee` |
| **HTTP Method** | `POST` |
| **URL** | `/tryitout/H0EUASP0` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `ws://ops.koreainvestment.com:21000` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `H0EUASP0` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-05-17T10:31:25+09:00
- **최종 수정일**: 2025-06-13T09:59:25+09:00

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `approval_key` | 웹소켓 접속키 | String | 36 | Y | 실시간 (웹소켓) 접속키 발급 API(/oauth2/Approval)를 사용하여 발급받은 웹소켓 접속키 |
| `custtype` | 고객 타입 | String | 1 | Y | B : 법인 / P : 개인 |
| `tr_type` | 등록/해제 | String | 1 | Y | 1: 등록, 2:해제 |
| `content-type` | 컨텐츠타입 | String | 20 | Y | utf-8 |

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `tr_id` | 거래ID | String | 2 | Y | H0EUASP0 |
| `tr_key` | 구분값 | String | 12 | Y | 야간옵션 종목코드 |

### 요청 예시

```json
{
  "header": {
    "approval_key": "35xxxxxa-bxxa-4xxb-87xxx-f56xxxxxxxxxx",
    "custtype": "P",
    "tr_type": "1",
    "content-type": "utf-8"
  },
  "body": {
    "input": {
      "tr_id": "H0EUASP0",
      "tr_key": "301V06362"
    }
  }
}
```

## 응답

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `OPTN_SHRN_ISCD` | 옵션단축종목코드 | String | 9 | Y |  |
| `BSOP_HOUR` | 영업시간 | String | 6 | Y |  |
| `OPTN_ASKP1` | 옵션매도호가1 | String | 1 | Y |  |
| `OPTN_ASKP2` | 옵션매도호가2 | String | 1 | Y |  |
| `OPTN_ASKP3` | 옵션매도호가3 | String | 1 | Y |  |
| `OPTN_ASKP4` | 옵션매도호가4 | String | 1 | Y |  |
| `OPTN_ASKP5` | 옵션매도호가5 | String | 1 | Y |  |
| `OPTN_BIDP1` | 옵션매수호가1 | String | 1 | Y |  |
| `OPTN_BIDP2` | 옵션매수호가2 | String | 1 | Y |  |
| `OPTN_BIDP3` | 옵션매수호가3 | String | 1 | Y |  |
| `OPTN_BIDP4` | 옵션매수호가4 | String | 1 | Y |  |
| `OPTN_BIDP5` | 옵션매수호가5 | String | 1 | Y |  |
| `ASKP_CSNU1` | 매도호가건수1 | String | 1 | Y |  |
| `ASKP_CSNU2` | 매도호가건수2 | String | 1 | Y |  |
| `ASKP_CSNU3` | 매도호가건수3 | String | 1 | Y |  |
| `ASKP_CSNU4` | 매도호가건수4 | String | 1 | Y |  |
| `ASKP_CSNU5` | 매도호가건수5 | String | 1 | Y |  |
| `BIDP_CSNU1` | 매수호가건수1 | String | 1 | Y |  |
| `BIDP_CSNU2` | 매수호가건수2 | String | 1 | Y |  |
| `BIDP_CSNU3` | 매수호가건수3 | String | 1 | Y |  |
| `BIDP_CSNU4` | 매수호가건수4 | String | 1 | Y |  |
| `BIDP_CSNU5` | 매수호가건수5 | String | 1 | Y |  |
| `ASKP_RSQN1` | 매도호가잔량1 | String | 1 | Y |  |
| `ASKP_RSQN2` | 매도호가잔량2 | String | 1 | Y |  |
| `ASKP_RSQN3` | 매도호가잔량3 | String | 1 | Y |  |
| `ASKP_RSQN4` | 매도호가잔량4 | String | 1 | Y |  |
| `ASKP_RSQN5` | 매도호가잔량5 | String | 1 | Y |  |
| `BIDP_RSQN1` | 매수호가잔량1 | String | 1 | Y |  |
| `BIDP_RSQN2` | 매수호가잔량2 | String | 1 | Y |  |
| `BIDP_RSQN3` | 매수호가잔량3 | String | 1 | Y |  |
| `BIDP_RSQN4` | 매수호가잔량4 | String | 1 | Y |  |
| `BIDP_RSQN5` | 매수호가잔량5 | String | 1 | Y |  |
| `TOTAL_ASKP_CSNU` | 총매도호가건수 | String | 1 | Y |  |
| `TOTAL_BIDP_CSNU` | 총매수호가건수 | String | 1 | Y |  |
| `TOTAL_ASKP_RSQN` | 총매도호가잔량 | String | 1 | Y |  |
| `TOTAL_BIDP_RSQN` | 총매수호가잔량 | String | 1 | Y |  |
| `TOTAL_ASKP_RSQN_ICDC` | 총매도호가잔량증감 | String | 1 | Y |  |
| `TOTAL_BIDP_RSQN_ICDC` | 총매수호가잔량증감 | String | 1 | Y |  |

### 응답 예시

```json
# 연결 확인
{
    "header": {
        "tr_id": "H0EUASP0", 
        "tr_key": "301V06362", 
        "encrypt": "N"
        }, 
    "body": {
        "rt_cd": "0", 
        "msg_cd": "OPSP0000",
        "msg1": "SUBSCRIBE SUCCESS", 
        "output": {
            "iv": "0123456789abcdef", 
            "key": "abcdefghijklmnopabcdefghijklmnop"}
        }
}

# output
0|H0EUASP0|001|301V06362^190159^2.98^2.99^3.00^0.00^0.00^2.97^2.96^2.95^0.00^0.00^0
^0^0^0^0^0^0^0^0^0^1^3^12^0^0^9^21^16^0^0^0^0^16^46^5^0

# output - 복호화 후
#### 야간옵션(EUREX) 호가 ####
야간옵션(EUREX)  [301V06362]
영업시간  [190215]
====================================
옵션매도호가1   [2.98],    매도호가건수1        [0],    매도호가잔량1   [1]
옵션매도호가2   [3.00],    매도호가건수2        [0],    매도호가잔량2   [6]
옵션매도호가3   [3.01],    매도호가건수3        [0],    매도호가잔량3   [15]
옵션매도호가4   [0.00],    매도호가건수4        [0],    매도호가잔량4   [0]
옵션매도호가5   [0.00],    매도호가건수5        [0],    매도호가잔량5   [0]
옵션매수호가1   [2.97],    매수호가건수1        [0],    매수호가잔량1   [10]
옵션매수호가2   [2.96],    매수호가건수2        [0],    매수호가잔량2   [21]
옵션매수호가3   [2.95],    매수호가건수3        [0],    매수호가잔량3   [16]
옵션매수호가4   [0.00],   매수호가건수4 [0],    매수호가잔량4   [0]
옵션매수호가5   [0.00],    매수호가건수5        [0],    매수호가잔량5   [0]
====================================
총매도호가건수  [0],    총매도호가잔량  [22],    총매도호가잔량증감     [-1]
총매수호가건수  [0],    총매수호가잔량  [47],    총매수호가잔량증감     [1]
```

