# KRX야간선물 실시간호가 [실시간-065]

> [국내선물옵션] 실시간시세

※ 선물옵션 호가 데이터는 0.2초 필터링 옵션이 있습니다.
  필터링 사유는 순간적으로 데이터가 폭증할 경우 서버 뿐만아니라 클라이언트 환경에도 부하를 줄 수 있어 적용된 사항인 점 양해 부탁드립니다.

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
| **API ID** | `480e727f-c7df-4b22-9d15-9c4567a8b849` |
| **HTTP Method** | `POST` |
| **URL** | `/tryitout/H0MFASP0` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `ws://ops.koreainvestment.com:21000` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `H0MFASP0` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-05-24
- **최종 수정일**: 2025-06-30

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
| `tr_id` | 거래ID | String | 2 | Y | H0MFASP0 |
| `tr_key` | 구분값 | String | 12 | Y | 야간선물 종목코드 |

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
      "tr_id": "H0MFASP0",
      "tr_key": "101V06"
    }
  }
}
```

## 응답

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `FUTS_SHRN_ISCD` | 선물 단축 종목코드 | String | 9 | Y |  |
| `BSOP_HOUR` | 영업 시간 | String | 6 | Y |  |
| `FUTS_ASKP1` | 선물 매도호가1 | String | 8 | Y |  |
| `FUTS_ASKP2` | 선물 매도호가2 | String | 8 | Y |  |
| `FUTS_ASKP3` | 선물 매도호가3 | String | 8 | Y |  |
| `FUTS_ASKP4` | 선물 매도호가4 | String | 8 | Y |  |
| `FUTS_ASKP5` | 선물 매도호가5 | String | 8 | Y |  |
| `FUTS_BIDP1` | 선물 매수호가1 | String | 8 | Y |  |
| `FUTS_BIDP2` | 선물 매수호가2 | String | 8 | Y |  |
| `FUTS_BIDP3` | 선물 매수호가3 | String | 8 | Y |  |
| `FUTS_BIDP4` | 선물 매수호가4 | String | 8 | Y |  |
| `FUTS_BIDP5` | 선물 매수호가5 | String | 8 | Y |  |
| `ASKP_CSNU1` | 매도호가 건수1 | String | 4 | Y |  |
| `ASKP_CSNU2` | 매도호가 건수2 | String | 4 | Y |  |
| `ASKP_CSNU3` | 매도호가 건수3 | String | 4 | Y |  |
| `ASKP_CSNU4` | 매도호가 건수4 | String | 4 | Y |  |
| `ASKP_CSNU5` | 매도호가 건수5 | String | 4 | Y |  |
| `BIDP_CSNU1` | 매수호가 건수1 | String | 4 | Y |  |
| `BIDP_CSNU2` | 매수호가 건수2 | String | 4 | Y |  |
| `BIDP_CSNU3` | 매수호가 건수3 | String | 4 | Y |  |
| `BIDP_CSNU4` | 매수호가 건수4 | String | 4 | Y |  |
| `BIDP_CSNU5` | 매수호가 건수5 | String | 4 | Y |  |
| `ASKP_RSQN1` | 매도호가 잔량1 | String | 8 | Y |  |
| `ASKP_RSQN2` | 매도호가 잔량2 | String | 8 | Y |  |
| `ASKP_RSQN3` | 매도호가 잔량3 | String | 8 | Y |  |
| `ASKP_RSQN4` | 매도호가 잔량4 | String | 8 | Y |  |
| `ASKP_RSQN5` | 매도호가 잔량5 | String | 8 | Y |  |
| `BIDP_RSQN1` | 매수호가 잔량1 | String | 8 | Y |  |
| `BIDP_RSQN2` | 매수호가 잔량2 | String | 8 | Y |  |
| `BIDP_RSQN3` | 매수호가 잔량3 | String | 8 | Y |  |
| `BIDP_RSQN4` | 매수호가 잔량4 | String | 8 | Y |  |
| `BIDP_RSQN5` | 매수호가 잔량5 | String | 8 | Y |  |
| `TOTAL_ASKP_CSNU` | 총 매도호가 건수 | String | 4 | Y |  |
| `TOTAL_BIDP_CSNU` | 총 매수호가 건수 | String | 4 | Y |  |
| `TOTAL_ASKP_RSQN` | 총 매도호가 잔량 | String | 8 | Y |  |
| `TOTAL_BIDP_RSQN` | 총 매수호가 잔량 | String | 8 | Y |  |
| `TOTAL_ASKP_RSQN_ICDC` | 총 매도호가 잔량 증감 | String | 4 | Y |  |
| `TOTAL_BIDP_RSQN_ICDC` | 총 매수호가 잔량 증감 | String | 4 | Y |  |

### 응답 예시

```json
# 연결 확인
{
    "header": {
        "tr_id": "H0MFASP0", 
        "tr_key": "101V06", 
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
0|H0MFASP0|001|101V06^190215^367.35^367.40^367.45^0.00^0.00^367.30^367.25^367.20^0.
00^0.00^0^0^0^0^0^0^0^0^0^0^24^21^21^0^0^2^28^20^0^0^0^0^0^0^^0^0^0^0^0^^000000^2^
```

