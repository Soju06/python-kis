# 국내지수 실시간예상체결 [실시간-027]

> [국내주식] 실시간시세

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
| **API ID** | `10443c63-715e-46ef-ab46-5a91b5913e87` |
| **HTTP Method** | `POST` |
| **URL** | `/tryitout/H0UPANC0` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `ws://ops.koreainvestment.com:21000` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID** | `H0UPANC0`, `모의투자 미지원` |

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
| `tr_id` | 거래ID | String | 7 | Y | H0UPANC0 |
| `tr_key` | 종목코드 | String | 6 | Y | 업종구분코드 |

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
      "tr_id": "H0UPANC0",
      "tr_key": "0001"
    }
  }
}
```

## 응답 (Response)

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `BSTP_CLS_CODE` | 업종 구분 코드 | String | 4 | Y | '각 항목사이에는 구분자로 ^ 사용, 모든 데이터타입은 String으로 변환되어 push 처리됨' |
| `BSOP_HOUR` | 영업 시간 | String | 6 | Y |  |
| `PRPR_NMIX` | 현재가 지수 | String | 1 | Y |  |
| `PRDY_VRSS_SIGN` | 전일 대비 부호 | String | 1 | Y |  |
| `BSTP_NMIX_PRDY_VRSS` | 업종 지수 전일 대비 | String | 1 | Y |  |
| `ACML_VOL` | 누적 거래량 | String | 1 | Y |  |
| `ACML_TR_PBMN` | 누적 거래 대금 | String | 1 | Y |  |
| `PCAS_VOL` | 건별 거래량 | String | 1 | Y |  |
| `PCAS_TR_PBMN` | 건별 거래 대금 | String | 1 | Y |  |
| `PRDY_CTRT` | 전일 대비율 | String | 1 | Y |  |
| `OPRC_NMIX` | 시가 지수 | String | 1 | Y |  |
| `NMIX_HGPR` | 지수 최고가 | String | 1 | Y |  |
| `NMIX_LWPR` | 지수 최저가 | String | 1 | Y |  |
| `OPRC_VRSS_NMIX_PRPR` | 시가 대비 지수 현재가 | String | 1 | Y |  |
| `OPRC_VRSS_NMIX_SIGN` | 시가 대비 지수 부호 | String | 1 | Y |  |
| `HGPR_VRSS_NMIX_PRPR` | 최고가 대비 지수 현재가 | String | 1 | Y |  |
| `HGPR_VRSS_NMIX_SIGN` | 최고가 대비 지수 부호 | String | 1 | Y |  |
| `LWPR_VRSS_NMIX_PRPR` | 최저가 대비 지수 현재가 | String | 1 | Y |  |
| `LWPR_VRSS_NMIX_SIGN` | 최저가 대비 지수 부호 | String | 1 | Y |  |
| `PRDY_CLPR_VRSS_OPRC_RATE` | 전일 종가 대비 시가2 비율 | String | 1 | Y |  |
| `PRDY_CLPR_VRSS_HGPR_RATE` | 전일 종가 대비 최고가 비율 | String | 1 | Y |  |
| `PRDY_CLPR_VRSS_LWPR_RATE` | 전일 종가 대비 최저가 비율 | String | 1 | Y |  |
| `UPLM_ISSU_CNT` | 상한 종목 수 | String | 1 | Y |  |
| `ASCN_ISSU_CNT` | 상승 종목 수 | String | 1 | Y |  |
| `STNR_ISSU_CNT` | 보합 종목 수 | String | 1 | Y |  |
| `DOWN_ISSU_CNT` | 하락 종목 수 | String | 1 | Y |  |
| `LSLM_ISSU_CNT` | 하한 종목 수 | String | 1 | Y |  |
| `QTQT_ASCN_ISSU_CNT` | 기세 상승 종목수 | String | 1 | Y |  |
| `QTQT_DOWN_ISSU_CNT` | 기세 하락 종목수 | String | 1 | Y |  |
| `TICK_VRSS` | TICK대비 | String | 1 | Y |  |

### 응답 예시

```json
# 연결 확인
{
    "header": {
        "tr_id": "H0UPANC0", 
        "tr_key": "0001", 
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
0|H0UPANC0|001|0001^085910^2607.71^2^15.85^5424^192338^5424^192338^0.61^0^43
9^201^251^201
```
