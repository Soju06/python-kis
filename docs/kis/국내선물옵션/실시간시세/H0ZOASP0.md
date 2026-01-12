# 주식옵션 실시간호가 [실시간-045]

> [국내선물옵션] 실시간시세

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `00eafa0f-820b-4a12-91dc-a65593a8322e` |
| **HTTP Method** | `POST` |
| **URL** | `/tryitout/H0ZOASP0` |
| **Content-Type** | `` |
| **요청 포맷** | `` |
| **실전 도메인** | `ws://ops.koreainvestment.com:21000` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID** | `모의투자 미지원`, `H0ZOASP0` |

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
| `approval_key` | 웹소켓 접속키 | String | 36 | Y | 실시간 (웹소켓) 접속키 발급 API(/oauth2/Approval)를 사용하여 발급받은 웹소켓 접속키 |
| `custtype` | 고객 타입 | String | 1 | Y | B : 법인 / P : 개인 |
| `tr_type` | 등록/해제 | String | 1 | Y | "1: 등록, 2:해제" |
| `content-type` | 컨텐츠타입 | String | 20 | Y | utf-8 |

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `tr_id` | 거래ID | String | 7 | Y | H0ZOASP0 |
| `tr_key` | 종목코드 | String | 6 | Y | 종목코드 |

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
      "tr_id": "H0ZOASP0",
      "tr_key": "211V05059"
    }
  }
}
```

## 응답 (Response)

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `OPTN_SHRN_ISCD` | 옵션단축종목코드 | String | 9 | Y | '각 항목사이에는 구분자로 ^ 사용, 모든 데이터타입은 String으로 변환되어 push 처리됨' |
| `BSOP_HOUR` | 영업시간 | String | 6 | Y |  |
| `OPTN_ASKP1` | 옵션매도호가1 | String | 8 | Y |  |
| `OPTN_ASKP2` | 옵션매도호가2 | String | 8 | Y |  |
| `OPTN_ASKP3` | 옵션매도호가3 | String | 8 | Y |  |
| `OPTN_ASKP4` | 옵션매도호가4 | String | 8 | Y |  |
| `OPTN_ASKP5` | 옵션매도호가5 | String | 8 | Y |  |
| `OPTN_BIDP1` | 옵션매수호가1 | String | 8 | Y |  |
| `OPTN_BIDP2` | 옵션매수호가2 | String | 8 | Y |  |
| `OPTN_BIDP3` | 옵션매수호가3 | String | 8 | Y |  |
| `OPTN_BIDP4` | 옵션매수호가4 | String | 8 | Y |  |
| `OPTN_BIDP5` | 옵션매수호가5 | String | 8 | Y |  |
| `ASKP_CSNU1` | 매도호가건수1 | String | 4 | Y |  |
| `ASKP_CSNU2` | 매도호가건수2 | String | 4 | Y |  |
| `ASKP_CSNU3` | 매도호가건수3 | String | 4 | Y |  |
| `ASKP_CSNU4` | 매도호가건수4 | String | 4 | Y |  |
| `ASKP_CSNU5` | 매도호가건수5 | String | 4 | Y |  |
| `BIDP_CSNU1` | 매수호가건수1 | String | 4 | Y |  |
| `BIDP_CSNU2` | 매수호가건수2 | String | 4 | Y |  |
| `BIDP_CSNU3` | 매수호가건수3 | String | 4 | Y |  |
| `BIDP_CSNU4` | 매수호가건수4 | String | 4 | Y |  |
| `BIDP_CSNU5` | 매수호가건수5 | String | 4 | Y |  |
| `ASKP_RSQN1` | 매도호가잔량1 | String | 8 | Y |  |
| `ASKP_RSQN2` | 매도호가잔량2 | String | 8 | Y |  |
| `ASKP_RSQN3` | 매도호가잔량3 | String | 8 | Y |  |
| `ASKP_RSQN4` | 매도호가잔량4 | String | 8 | Y |  |
| `ASKP_RSQN5` | 매도호가잔량5 | String | 8 | Y |  |
| `BIDP_RSQN1` | 매수호가잔량1 | String | 8 | Y |  |
| `BIDP_RSQN2` | 매수호가잔량2 | String | 8 | Y |  |
| `BIDP_RSQN3` | 매수호가잔량3 | String | 8 | Y |  |
| `BIDP_RSQN4` | 매수호가잔량4 | String | 8 | Y |  |
| `BIDP_RSQN5` | 매수호가잔량5 | String | 8 | Y |  |
| `TOTAL_ASKP_CSNU` | 총매도호가건수 | String | 4 | Y |  |
| `TOTAL_BIDP_CSNU` | 총매수호가건수 | String | 4 | Y |  |
| `TOTAL_ASKP_RSQN` | 총매도호가잔량 | String | 8 | Y |  |
| `TOTAL_BIDP_RSQN` | 총매수호가잔량 | String | 8 | Y |  |
| `TOTAL_ASKP_RSQN_ICDC` | 총매도호가잔량증감 | String | 4 | Y |  |
| `TOTAL_BIDP_RSQN_ICDC` | 총매수호가잔량증감 | String | 4 | Y |  |
| `OPTN_ASKP6` | 옵션매도호가6 | String | 8 | Y |  |
| `OPTN_ASKP7` | 옵션매도호가7 | String | 8 | Y |  |
| `OPTN_ASKP8` | 옵션매도호가8 | String | 8 | Y |  |
| `OPTN_ASKP9` | 옵션매도호가9 | String | 8 | Y |  |
| `OPTN_ASKP10` | 옵션매도호가10 | String | 8 | Y |  |
| `OPTN_BIDP6` | 옵션매수호가6 | String | 8 | Y |  |
| `OPTN_BIDP7` | 옵션매수호가7 | String | 8 | Y |  |
| `OPTN_BIDP8` | 옵션매수호가8 | String | 8 | Y |  |
| `OPTN_BIDP9` | 옵션매수호가9 | String | 8 | Y |  |
| `OPTN_BIDP10` | 옵션매수호가10 | String | 8 | Y |  |
| `ASKP_CSNU6` | 매도호가건수6 | String | 4 | Y |  |
| `ASKP_CSNU7` | 매도호가건수7 | String | 4 | Y |  |
| `ASKP_CSNU8` | 매도호가건수8 | String | 4 | Y |  |
| `ASKP_CSNU9` | 매도호가건수9 | String | 4 | Y |  |
| `ASKP_CSNU10` | 매도호가건수10 | String | 4 | Y |  |
| `BIDP_CSNU6` | 매수호가건수6 | String | 4 | Y |  |
| `BIDP_CSNU7` | 매수호가건수7 | String | 4 | Y |  |
| `BIDP_CSNU8` | 매수호가건수8 | String | 4 | Y |  |
| `BIDP_CSNU9` | 매수호가건수9 | String | 4 | Y |  |
| `BIDP_CSNU10` | 매수호가건수10 | String | 4 | Y |  |
| `ASKP_RSQN6` | 매도호가잔량6 | String | 8 | Y |  |
| `ASKP_RSQN7` | 매도호가잔량7 | String | 8 | Y |  |
| `ASKP_RSQN8` | 매도호가잔량8 | String | 8 | Y |  |
| `ASKP_RSQN9` | 매도호가잔량9 | String | 8 | Y |  |
| `ASKP_RSQN10` | 매도호가잔량10 | String | 8 | Y |  |
| `BIDP_RSQN6` | 매수호가잔량6 | String | 8 | Y |  |
| `BIDP_RSQN7` | 매수호가잔량7 | String | 8 | Y |  |
| `BIDP_RSQN8` | 매수호가잔량8 | String | 8 | Y |  |
| `BIDP_RSQN9` | 매수호가잔량9 | String | 8 | Y |  |
| `BIDP_RSQN10` | 매수호가잔량10 | String | 8 | Y |  |

### 응답 예시

```json
# 연결 확인
{
    "header": {
        "tr_id": "H0ZOASP0", 
        "tr_key": "211V05059", 
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
0|H0ZOASP0|001|211V05059^091509^1140.00^1160.00^1200.00^1300.00^1400.00^1120
.00^1080.00^620.00^580.00^530.00^2^1^1^1^1^1^2^1^1^1^187^12^10^10^10^12^187^3^3^3^9^6^241^208^
0^0^1500.00^1520.00^1700.00^0.00^0.00^0.00^0.00^0.00^0.00^0.00^1^1^1^0^0^0^0^0^0^0^10^1^1^0^0^
0^0^0^0^0
```
