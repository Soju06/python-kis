# 주식선물 실시간호가 [실시간-030]

> [국내선물옵션] 실시간시세

※ 선물옵션 호가 데이터는 0.2초 필터링 옵션이 있습니다.
  필터링 사유는 순간적으로 데이터가 폭증할 경우 서버 뿐만아니라 클라이언트 환경에도 부하를 줄 수 있어 적용된 사항인 점 양해 부탁드립니다.


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `c4ded44e-26fe-4b9f-b8d7-10e1ba4020a4` |
| **HTTP Method** | `POST` |
| **URL** | `/tryitout/H0ZFASP0` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `ws://ops.koreainvestment.com:21000` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `H0ZFASP0` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-04-19
- **최종 수정일**: 2025-04-30

## 요청

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
| `tr_id` | 거래ID | String | 7 | Y | H0ZFASP0 |
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
      "tr_id": "H0ZFASP0",
      "tr_key": "111V06"
    }
  }
}
```

## 응답

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `FUTS_SHRN_ISCD` | 선물단축종목코드 | String | 9 | Y | '각 항목사이에는 구분자로 ^ 사용, 모든 데이터타입은 String으로 변환되어 push 처리됨' |
| `BSOP_HOUR` | 영업시간 | String | 6 | Y |  |
| `ASKP1` | 매도호가1 | String | 1 | Y |  |
| `ASKP2` | 매도호가2 | String | 1 | Y |  |
| `ASKP3` | 매도호가3 | String | 1 | Y |  |
| `ASKP4` | 매도호가4 | String | 1 | Y |  |
| `ASKP5` | 매도호가5 | String | 1 | Y |  |
| `ASKP6` | 매도호가6 | String | 1 | Y |  |
| `ASKP7` | 매도호가7 | String | 1 | Y |  |
| `ASKP8` | 매도호가8 | String | 1 | Y |  |
| `ASKP9` | 매도호가9 | String | 1 | Y |  |
| `ASKP10` | 매도호가10 | String | 1 | Y |  |
| `BIDP1` | 매수호가1 | String | 1 | Y |  |
| `BIDP2` | 매수호가2 | String | 1 | Y |  |
| `BIDP3` | 매수호가3 | String | 1 | Y |  |
| `BIDP4` | 매수호가4 | String | 1 | Y |  |
| `BIDP5` | 매수호가5 | String | 1 | Y |  |
| `BIDP6` | 매수호가6 | String | 1 | Y |  |
| `BIDP7` | 매수호가7 | String | 1 | Y |  |
| `BIDP8` | 매수호가8 | String | 1 | Y |  |
| `BIDP9` | 매수호가9 | String | 1 | Y |  |
| `BIDP10` | 매수호가10 | String | 1 | Y |  |
| `ASKP_CSNU1` | 매도호가건수1 | String | 1 | Y |  |
| `ASKP_CSNU2` | 매도호가건수2 | String | 1 | Y |  |
| `ASKP_CSNU3` | 매도호가건수3 | String | 1 | Y |  |
| `ASKP_CSNU4` | 매도호가건수4 | String | 1 | Y |  |
| `ASKP_CSNU5` | 매도호가건수5 | String | 1 | Y |  |
| `ASKP_CSNU6` | 매도호가건수6 | String | 1 | Y |  |
| `ASKP_CSNU7` | 매도호가건수7 | String | 1 | Y |  |
| `ASKP_CSNU8` | 매도호가건수8 | String | 1 | Y |  |
| `ASKP_CSNU9` | 매도호가건수9 | String | 1 | Y |  |
| `ASKP_CSNU10` | 매도호가건수10 | String | 1 | Y |  |
| `BIDP_CSNU1` | 매수호가건수1 | String | 1 | Y |  |
| `BIDP_CSNU2` | 매수호가건수2 | String | 1 | Y |  |
| `BIDP_CSNU3` | 매수호가건수3 | String | 1 | Y |  |
| `BIDP_CSNU4` | 매수호가건수4 | String | 1 | Y |  |
| `BIDP_CSNU5` | 매수호가건수5 | String | 1 | Y |  |
| `BIDP_CSNU6` | 매수호가건수6 | String | 1 | Y |  |
| `BIDP_CSNU7` | 매수호가건수7 | String | 1 | Y |  |
| `BIDP_CSNU8` | 매수호가건수8 | String | 1 | Y |  |
| `BIDP_CSNU9` | 매수호가건수9 | String | 1 | Y |  |
| `BIDP_CSNU10` | 매수호가건수10 | String | 1 | Y |  |
| `ASKP_RSQN1` | 매도호가잔량1 | String | 1 | Y |  |
| `ASKP_RSQN2` | 매도호가잔량2 | String | 1 | Y |  |
| `ASKP_RSQN3` | 매도호가잔량3 | String | 1 | Y |  |
| `ASKP_RSQN4` | 매도호가잔량4 | String | 1 | Y |  |
| `ASKP_RSQN5` | 매도호가잔량5 | String | 1 | Y |  |
| `ASKP_RSQN6` | 매도호가잔량6 | String | 1 | Y |  |
| `ASKP_RSQN7` | 매도호가잔량7 | String | 1 | Y |  |
| `ASKP_RSQN8` | 매도호가잔량8 | String | 1 | Y |  |
| `ASKP_RSQN9` | 매도호가잔량9 | String | 1 | Y |  |
| `ASKP_RSQN10` | 매도호가잔량10 | String | 1 | Y |  |
| `BIDP_RSQN1` | 매수호가잔량1 | String | 1 | Y |  |
| `BIDP_RSQN2` | 매수호가잔량2 | String | 1 | Y |  |
| `BIDP_RSQN3` | 매수호가잔량3 | String | 1 | Y |  |
| `BIDP_RSQN4` | 매수호가잔량4 | String | 1 | Y |  |
| `BIDP_RSQN5` | 매수호가잔량5 | String | 1 | Y |  |
| `BIDP_RSQN6` | 매수호가잔량6 | String | 1 | Y |  |
| `BIDP_RSQN7` | 매수호가잔량7 | String | 1 | Y |  |
| `BIDP_RSQN8` | 매수호가잔량8 | String | 1 | Y |  |
| `BIDP_RSQN9` | 매수호가잔량9 | String | 1 | Y |  |
| `BIDP_RSQN10` | 매수호가잔량10 | String | 1 | Y |  |
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
        "tr_id": "H0ZFASP0", 
        "tr_key": "111V06", 
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
0|H0ZFASP0|001|111V06^092304^79700^79800^79900^80000^80200^80300^80500^81100^8490
0^85900^79500^79400^79300^79200^79100^79000^78900^78800^78700^78600^1^18^6^2^2^1^3^1^1^1^8^6^4^8^4^
8^7^11^11^3^950^4148^988^6^9^1^3^15^5^10^4404^2277^1321^3440^330^2237^1835^362^83^15^36^97^6135^165
09^950^0
```

