# 국내주식 시간외 실시간호가 (KRX) [실시간-025]

> [국내주식] 실시간시세

국내주식 시간외 실시간호가 API입니다.
국내주식 시간외 단일가(16:00~18:00) 시간대에 실시간호가 데이터 확인 가능합니다.

[참고자료]
실시간시세(웹소켓) 파이썬 샘플코드는 한국투자증권 Github 참고 부탁드립니다.
https://github.com/koreainvestment/open-trading-api/blob/main/websocket/python/ws_domestic_overseas_all.py

실시간시세(웹소켓) API 사용방법에 대한 자세한 설명은 한국투자증권 Wikidocs 참고 부탁드립니다.
https://wikidocs.net/book/7847 (국내주식 업데이트 완료, 추후 해외주식·국내선물옵션 업데이트 예정)

종목코드 마스터파일 파이썬 정제코드는 한국투자증권 Github 참고 부탁드립니다.
https://github.com/koreainvestment/open-trading-api/tree/main/stocks_info


[호출 데이터]
헤더와 바디 값을 합쳐 JSON 형태로 전송합니다.

[응답 데이터]
1. 정상 등록 여부 (JSON)
- JSON["body"]["msg1"] - 정상 응답 시, SUBSCRIBE SUCCESS
- JSON["body"]["output"]["iv"] - 실시간 결과 복호화에 필요한 AES256 IV (Initialize Vector)
- JSON["body"]["output"]["key"] - 실시간 결과 복호화에 필요한 AES256 Key

2. 실시간 결과 응답 ( | 로 구분되는 값)
ex) 0|H0STCNT0|004|005930^123929^73100^5^...
- 암호화 유무 : 0 암호화 되지 않은 데이터 / 1 암호화된 데이터
- TR_ID : 등록한 tr_id (ex. H0STCNT0)
- 데이터 건수 : (ex. 001 인 경우 데이터 건수 1건, 004인 경우 데이터 건수 4건)
- 응답 데이터 : 아래 response 데이터 참조 ( ^로 구분됨)


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `3e56c064-ef28-45ba-a681-6d164703af14` |
| **HTTP Method** | `POST` |
| **URL** | `/tryitout/H0STOAA0` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `ws://ops.koreainvestment.com:21000` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `H0STOAA0` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-05-03T12:52:20+09:00
- **최종 수정일**: 2025-04-30T13:15:01+09:00

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
| `tr_id` | 거래ID | String | 2 | Y | H0STOAA0 |
| `tr_key` | 구분값 | String | 12 | Y | 종목코드 (ex 005930 삼성전자) |

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
      "tr_id": "H0STOAA0",
      "tr_key": "005930"
    }
  }
}
```

## 응답

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `MKSC_SHRN_ISCD` | 유가증권단축종목코드 | String | 9 | Y |  |
| `BSOP_HOUR` | 영업시간 | String | 6 | Y |  |
| `HOUR_CLS_CODE` | 시간구분코드 | String | 1 | Y |  |
| `ASKP1` | 매도호가1 | String | 1 | Y |  |
| `ASKP2` | 매도호가2 | String | 1 | Y |  |
| `ASKP3` | 매도호가3 | String | 1 | Y |  |
| `ASKP4` | 매도호가4 | String | 1 | Y |  |
| `ASKP5` | 매도호가5 | String | 1 | Y |  |
| `ASKP6` | 매도호가6 | String | 1 | Y |  |
| `ASKP7` | 매도호가7 | String | 1 | Y |  |
| `ASKP8` | 매도호가8 | String | 1 | Y |  |
| `ASKP9` | 매도호가9 | String | 1 | Y |  |
| `BIDP1` | 매수호가1 | String | 1 | Y |  |
| `BIDP2` | 매수호가2 | String | 1 | Y |  |
| `BIDP3` | 매수호가3 | String | 1 | Y |  |
| `BIDP4` | 매수호가4 | String | 1 | Y |  |
| `BIDP5` | 매수호가5 | String | 1 | Y |  |
| `BIDP6` | 매수호가6 | String | 1 | Y |  |
| `BIDP7` | 매수호가7 | String | 1 | Y |  |
| `BIDP8` | 매수호가8 | String | 1 | Y |  |
| `BIDP9` | 매수호가9 | String | 1 | Y |  |
| `ASKP_RSQN1` | 매도호가잔량1 | String | 1 | Y |  |
| `ASKP_RSQN2` | 매도호가잔량2 | String | 1 | Y |  |
| `ASKP_RSQN3` | 매도호가잔량3 | String | 1 | Y |  |
| `ASKP_RSQN4` | 매도호가잔량4 | String | 1 | Y |  |
| `ASKP_RSQN5` | 매도호가잔량5 | String | 1 | Y |  |
| `ASKP_RSQN6` | 매도호가잔량6 | String | 1 | Y |  |
| `ASKP_RSQN7` | 매도호가잔량7 | String | 1 | Y |  |
| `ASKP_RSQN8` | 매도호가잔량8 | String | 1 | Y |  |
| `ASKP_RSQN9` | 매도호가잔량9 | String | 1 | Y |  |
| `BIDP_RSQN1` | 매수호가잔량1 | String | 1 | Y |  |
| `BIDP_RSQN2` | 매수호가잔량2 | String | 1 | Y |  |
| `BIDP_RSQN3` | 매수호가잔량3 | String | 1 | Y |  |
| `BIDP_RSQN4` | 매수호가잔량4 | String | 1 | Y |  |
| `BIDP_RSQN5` | 매수호가잔량5 | String | 1 | Y |  |
| `BIDP_RSQN6` | 매수호가잔량6 | String | 1 | Y |  |
| `BIDP_RSQN7` | 매수호가잔량7 | String | 1 | Y |  |
| `BIDP_RSQN8` | 매수호가잔량8 | String | 1 | Y |  |
| `BIDP_RSQN9` | 매수호가잔량9 | String | 1 | Y |  |
| `TOTAL_ASKP_RSQN` | 총매도호가잔량 | String | 1 | Y |  |
| `TOTAL_BIDP_RSQN` | 총매수호가잔량 | String | 1 | Y |  |
| `OVTM_TOTAL_ASKP_RSQN` | 시간외총매도호가잔량 | String | 1 | Y |  |
| `OVTM_TOTAL_BIDP_RSQN` | 시간외총매수호가잔량 | String | 1 | Y |  |
| `ANTC_CNPR` | 예상체결가 | String | 1 | Y |  |
| `ANTC_CNQN` | 예상체결량 | String | 1 | Y |  |
| `ANTC_VOL` | 예상거래량 | String | 1 | Y |  |
| `ANTC_CNTG_VRSS` | 예상체결대비 | String | 1 | Y |  |
| `ANTC_CNTG_VRSS_SIGN` | 예상체결대비부호 | String | 1 | Y |  |
| `ANTC_CNTG_PRDY_CTRT` | 예상체결전일대비율 | String | 1 | Y |  |
| `ACML_VOL` | 누적거래량 | String | 1 | Y |  |
| `TOTAL_ASKP_RSQN_ICDC` | 총매도호가잔량증감 | String | 1 | Y |  |
| `TOTAL_BIDP_RSQN_ICDC` | 총매수호가잔량증감 | String | 1 | Y |  |
| `OVTM_TOTAL_ASKP_ICDC` | 시간외총매도호가증감 | String | 1 | Y |  |
| `OVTM_TOTAL_BIDP_ICDC` | 시간외총매수호가증감 | String | 1 | Y |  |

### 응답 예시

```json
# 연결 확인
{
    "header": {
        "tr_id": "H0STOAA0", 
        "tr_key": "005930", 
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
0|H0STOAA0|001|005930^164128^B^77800^77900^78000^0^0^0^0^0^0^0^77700^
77600^77500^0^0^0^0^0^0^0^8005^7355^9284^0^0^0^0^0^0^0^4^16654^14297^0^0^0^0^0^0^0^2464
4^30955^0^37426^77700^82^82^100^2^0.13^13069425^-1^0^0^0
```

