# ELW 실시간호가 [실시간-062]

> [국내주식] 실시간시세

ELW 실시간호가 API입니다.

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
| **API ID** | `9995fff8-61d9-4e18-a2f4-e1ce457ee209` |
| **HTTP Method** | `POST` |
| **URL** | `/tryitout/H0EWASP0` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `ws://ops.koreainvestment.com:21000` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID** | `모의투자 미지원`, `H0EWASP0` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-04-26
- **최종 수정일**: 2025-04-30

## 요청 (Request)

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
| `tr_id` | 거래ID | String | 2 | Y | H0EWASP0 |
| `tr_key` | 구분값 | String | 12 | Y | ELW 종목코드(ex. 57LA24) |

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
      "tr_id": "H0EWASP0",
      "tr_key": "57JN53"
    }
  }
}
```

## 응답 (Response)

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
| `TOTAL_ASKP_RSQN` | 총매도호가잔량 | String | 1 | Y |  |
| `TOTAL_BIDP_RSQN` | 총매수호가잔량 | String | 1 | Y |  |
| `ANTC_CNPR` | 예상체결가 | String | 1 | Y |  |
| `ANTC_CNQN` | 예상체결량 | String | 1 | Y |  |
| `ANTC_CNTG_VRSS_SIGN` | 예상체결대비부호 | String | 1 | Y |  |
| `ANTC_CNTG_VRSS` | 예상체결대비 | String | 1 | Y |  |
| `ANTC_CNTG_PRDY_CTRT` | 예상체결전일대비율 | String | 1 | Y |  |
| `LP_ASKP_RSQN1` | LP매도호가잔량1 | String | 1 | Y |  |
| `LP_ASKP_RSQN2` | LP매도호가잔량2 | String | 1 | Y |  |
| `LP_ASKP_RSQN3` | LP매도호가잔량3 | String | 1 | Y |  |
| `LP_BIDP_RSQN4` | LP매수호가잔량4 | String | 1 | Y |  |
| `LP_ASKP_RSQN4` | LP매도호가잔량4 | String | 1 | Y |  |
| `LP_BIDP_RSQN5` | LP매수호가잔량5 | String | 1 | Y |  |
| `LP_ASKP_RSQN5` | LP매도호가잔량5 | String | 1 | Y |  |
| `LP_BIDP_RSQN6` | LP매수호가잔량6 | String | 1 | Y |  |
| `LP_ASKP_RSQN6` | LP매도호가잔량6 | String | 1 | Y |  |
| `LP_BIDP_RSQN7` | LP매수호가잔량7 | String | 1 | Y |  |
| `LP_ASKP_RSQN7` | LP매도호가잔량7 | String | 1 | Y |  |
| `LP_ASKP_RSQN8` | LP매도호가잔량8 | String | 1 | Y |  |
| `LP_BIDP_RSQN8` | LP매수호가잔량8 | String | 1 | Y |  |
| `LP_ASKP_RSQN9` | LP매도호가잔량9 | String | 1 | Y |  |
| `LP_BIDP_RSQN9` | LP매수호가잔량9 | String | 1 | Y |  |
| `LP_ASKP_RSQN10` | LP매도호가잔량10 | String | 1 | Y |  |
| `LP_BIDP_RSQN10` | LP매수호가잔량10 | String | 1 | Y |  |
| `LP_BIDP_RSQN1` | LP매수호가잔량1 | String | 1 | Y |  |
| `LP_TOTAL_ASKP_RSQN` | LP총매도호가잔량 | String | 1 | Y |  |
| `LP_BIDP_RSQN2` | LP매수호가잔량2 | String | 1 | Y |  |
| `LP_TOTAL_BIDP_RSQN` | LP총매수호가잔량 | String | 1 | Y |  |
| `LP_BIDP_RSQN3` | LP매수호가잔량3 | String | 1 | Y |  |
| `ANTC_VOL` | 예상거래량 | String | 1 | Y |  |

### 응답 예시

```json
# 연결 확인
{
    "header": {
        "tr_id": "H0EWASP0", 
        "tr_key": "57JN53", 
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
0|H0EWASP0|001|57JN53^090333^0^270^275^280^285^290^295^300^305^310
^315^265^260^255^250^245^240^235^230^225^220^132730^144770^53560^139510^104910^16386
0^111580^41530^66600^41040^119950^176460^142150^218620^148250^160210^154250^141660^1
40270^160640^1000090^1562460^0^0^3^0^0.00^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^0^
0^0
```
