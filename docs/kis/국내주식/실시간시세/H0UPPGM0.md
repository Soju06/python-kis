# 국내지수 실시간프로그램매매 [실시간-028]

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
| **API ID** | `7862b3ea-d28b-4995-8366-4965f96436c5` |
| **HTTP Method** | `POST` |
| **URL** | `/tryitout/H0UPPGM0` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `ws://ops.koreainvestment.com:21000` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `H0UPPGM0` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-04-19T09:36:20+09:00
- **최종 수정일**: 2025-04-30T13:12:07+09:00

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
| `tr_id` | 거래ID | String | 7 | Y | H0UPPGM0 |
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
      "tr_id": "H0UPPGM0",
      "tr_key": "0001"
    }
  }
}
```

## 응답

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `BSTP_CLS_CODE` | 업종 구분 코드 | String | 4 | Y | '각 항목사이에는 구분자로 ^ 사용, 모든 데이터타입은 String으로 변환되어 push 처리됨' |
| `BSOP_HOUR` | 영업 시간 | String | 6 | Y |  |
| `ARBT_SELN_ENTM_CNQN` | 차익 매도 위탁 체결량 | String | 1 | Y |  |
| `ARBT_SELN_ONSL_CNQN` | 차익 매도 자기 체결량 | String | 1 | Y |  |
| `ARBT_SHNU_ENTM_CNQN` | 차익 매수2 위탁 체결량 | String | 1 | Y |  |
| `ARBT_SHNU_ONSL_CNQN` | 차익 매수2 자기 체결량 | String | 1 | Y |  |
| `NABT_SELN_ENTM_CNQN` | 비차익 매도 위탁 체결량 | String | 1 | Y |  |
| `NABT_SELN_ONSL_CNQN` | 비차익 매도 자기 체결량 | String | 1 | Y |  |
| `NABT_SHNU_ENTM_CNQN` | 비차익 매수2 위탁 체결량 | String | 1 | Y |  |
| `NABT_SHNU_ONSL_CNQN` | 비차익 매수2 자기 체결량 | String | 1 | Y |  |
| `ARBT_SELN_ENTM_CNTG_AMT` | 차익 매도 위탁 체결 금액 | String | 1 | Y |  |
| `ARBT_SELN_ONSL_CNTG_AMT` | 차익 매도 자기 체결 금액 | String | 1 | Y |  |
| `ARBT_SHNU_ENTM_CNTG_AMT` | 차익 매수2 위탁 체결 금액 | String | 1 | Y |  |
| `ARBT_SHNU_ONSL_CNTG_AMT` | 차익 매수2 자기 체결 금액 | String | 1 | Y |  |
| `NABT_SELN_ENTM_CNTG_AMT` | 비차익 매도 위탁 체결 금액 | String | 1 | Y |  |
| `NABT_SELN_ONSL_CNTG_AMT` | 비차익 매도 자기 체결 금액 | String | 1 | Y |  |
| `NABT_SHNU_ENTM_CNTG_AMT` | 비차익 매수2 위탁 체결 금액 | String | 1 | Y |  |
| `NABT_SHNU_ONSL_CNTG_AMT` | 비차익 매수2 자기 체결 금액 | String | 1 | Y |  |
| `ARBT_SMTN_SELN_VOL` | 차익 합계 매도 거래량 | String | 1 | Y |  |
| `ARBT_SMTM_SELN_VOL_RATE` | 차익 합계 매도 거래량 비율 | String | 1 | Y |  |
| `ARBT_SMTN_SELN_TR_PBMN` | 차익 합계 매도 거래 대금 | String | 1 | Y |  |
| `ARBT_SMTM_SELN_TR_PBMN_RATE` | 차익 합계 매도 거래대금 비율 | String | 1 | Y |  |
| `ARBT_SMTN_SHNU_VOL` | 차익 합계 매수2 거래량 | String | 1 | Y |  |
| `ARBT_SMTM_SHNU_VOL_RATE` | 차익 합계 매수 거래량 비율 | String | 1 | Y |  |
| `ARBT_SMTN_SHNU_TR_PBMN` | 차익 합계 매수2 거래 대금 | String | 1 | Y |  |
| `ARBT_SMTM_SHNU_TR_PBMN_RATE` | 차익 합계 매수 거래대금 비율 | String | 1 | Y |  |
| `ARBT_SMTN_NTBY_QTY` | 차익 합계 순매수 수량 | String | 1 | Y |  |
| `ARBT_SMTM_NTBY_QTY_RATE` | 차익 합계 순매수 수량 비율 | String | 1 | Y |  |
| `ARBT_SMTN_NTBY_TR_PBMN` | 차익 합계 순매수 거래 대금 | String | 1 | Y |  |
| `ARBT_SMTM_NTBY_TR_PBMN_RATE` | 차익 합계 순매수 거래대금 비율 | String | 1 | Y |  |
| `NABT_SMTN_SELN_VOL` | 비차익 합계 매도 거래량 | String | 1 | Y |  |
| `NABT_SMTM_SELN_VOL_RATE` | 비차익 합계 매도 거래량 비율 | String | 1 | Y |  |
| `NABT_SMTN_SELN_TR_PBMN` | 비차익 합계 매도 거래 대금 | String | 1 | Y |  |
| `NABT_SMTM_SELN_TR_PBMN_RATE` | 비차익 합계 매도 거래대금 비율 | String | 1 | Y |  |
| `NABT_SMTN_SHNU_VOL` | 비차익 합계 매수2 거래량 | String | 1 | Y |  |
| `NABT_SMTM_SHNU_VOL_RATE` | 비차익 합계 매수 거래량 비율 | String | 1 | Y |  |
| `NABT_SMTN_SHNU_TR_PBMN` | 비차익 합계 매수2 거래 대금 | String | 1 | Y |  |
| `NABT_SMTM_SHNU_TR_PBMN_RATE` | 비차익 합계 매수 거래대금 비율 | String | 1 | Y |  |
| `NABT_SMTN_NTBY_QTY` | 비차익 합계 순매수 수량 | String | 1 | Y |  |
| `NABT_SMTM_NTBY_QTY_RATE` | 비차익 합계 순매수 수량 비율 | String | 1 | Y |  |
| `NABT_SMTN_NTBY_TR_PBMN` | 비차익 합계 순매수 거래 대금 | String | 1 | Y |  |
| `NABT_SMTM_NTBY_TR_PBMN_RATE` | 비차익 합계 순매수 거래대금 비 | String | 1 | Y |  |
| `WHOL_ENTM_SELN_VOL` | 전체 위탁 매도 거래량 | String | 1 | Y |  |
| `ENTM_SELN_VOL_RATE` | 위탁 매도 거래량 비율 | String | 1 | Y |  |
| `WHOL_ENTM_SELN_TR_PBMN` | 전체 위탁 매도 거래 대금 | String | 1 | Y |  |
| `ENTM_SELN_TR_PBMN_RATE` | 위탁 매도 거래대금 비율 | String | 1 | Y |  |
| `WHOL_ENTM_SHNU_VOL` | 전체 위탁 매수2 거래량 | String | 1 | Y |  |
| `ENTM_SHNU_VOL_RATE` | 위탁 매수 거래량 비율 | String | 1 | Y |  |
| `WHOL_ENTM_SHNU_TR_PBMN` | 전체 위탁 매수2 거래 대금 | String | 1 | Y |  |
| `ENTM_SHNU_TR_PBMN_RATE` | 위탁 매수 거래대금 비율 | String | 1 | Y |  |
| `WHOL_ENTM_NTBY_QT` | 전체 위탁 순매수 수량 | String | 1 | Y |  |
| `ENTM_NTBY_QTY_RAT` | 위탁 순매수 수량 비율 | String | 1 | Y |  |
| `WHOL_ENTM_NTBY_TR_PBMN` | 전체 위탁 순매수 거래 대금 | String | 1 | Y |  |
| `ENTM_NTBY_TR_PBMN_RATE` | 위탁 순매수 금액 비율 | String | 1 | Y |  |
| `WHOL_ONSL_SELN_VOL` | 전체 자기 매도 거래량 | String | 1 | Y |  |
| `ONSL_SELN_VOL_RATE` | 자기 매도 거래량 비율 | String | 1 | Y |  |
| `WHOL_ONSL_SELN_TR_PBMN` | 전체 자기 매도 거래 대금 | String | 1 | Y |  |
| `ONSL_SELN_TR_PBMN_RATE` | 자기 매도 거래대금 비율 | String | 1 | Y |  |
| `WHOL_ONSL_SHNU_VOL` | 전체 자기 매수2 거래량 | String | 1 | Y |  |
| `ONSL_SHNU_VOL_RATE` | 자기 매수 거래량 비율 | String | 1 | Y |  |
| `WHOL_ONSL_SHNU_TR_PBMN` | 전체 자기 매수2 거래 대금 | String | 1 | Y |  |
| `ONSL_SHNU_TR_PBMN_RATE` | 자기 매수 거래대금 비율 | String | 1 | Y |  |
| `WHOL_ONSL_NTBY_QTY` | 전체 자기 순매수 수량 | String | 1 | Y |  |
| `ONSL_NTBY_QTY_RATE` | 자기 순매수량 비율 | String | 1 | Y |  |
| `WHOL_ONSL_NTBY_TR_PBMN` | 전체 자기 순매수 거래 대금 | String | 1 | Y |  |
| `ONSL_NTBY_TR_PBMN_RATE` | 자기 순매수 대금 비율 | String | 1 | Y |  |
| `TOTAL_SELN_QTY` | 총 매도 수량 | String | 1 | Y |  |
| `WHOL_SELN_VOL_RATE` | 전체 매도 거래량 비율 | String | 1 | Y |  |
| `TOTAL_SELN_TR_PBMN` | 총 매도 거래 대금 | String | 1 | Y |  |
| `WHOL_SELN_TR_PBMN_RATE` | 전체 매도 거래대금 비율 | String | 1 | Y |  |
| `SHNU_CNTG_SMTN` | 총 매수 수량 | String | 1 | Y |  |
| `WHOL_SHUN_VOL_RATE` | 전체 매수 거래량 비율 | String | 1 | Y |  |
| `TOTAL_SHNU_TR_PBMN` | 총 매수2 거래 대금 | String | 1 | Y |  |
| `WHOL_SHUN_TR_PBMN_RATE` | 전체 매수 거래대금 비율 | String | 1 | Y |  |
| `WHOL_NTBY_QTY` | 전체 순매수 수량 | String | 1 | Y |  |
| `WHOL_SMTM_NTBY_QTY_RATE` | 전체 합계 순매수 수량 비율 | String | 1 | Y |  |
| `WHOL_NTBY_TR_PBMN` | 전체 순매수 거래 대금 | String | 1 | Y |  |
| `WHOL_NTBY_TR_PBMN_RATE` | 전체 순매수 거래대금 비율 | String | 1 | Y |  |
| `ARBT_ENTM_NTBY_QTY` | 차익 위탁 순매수 수량 | String | 1 | Y |  |
| `ARBT_ENTM_NTBY_TR_PBMN` | 차익 위탁 순매수 거래 대금 | String | 1 | Y |  |
| `ARBT_ONSL_NTBY_QTY` | 차익 자기 순매수 수량 | String | 1 | Y |  |
| `ARBT_ONSL_NTBY_TR_PBMN` | 차익 자기 순매수 거래 대금 | String | 1 | Y |  |
| `NABT_ENTM_NTBY_QTY` | 비차익 위탁 순매수 수량 | String | 1 | Y |  |
| `NABT_ENTM_NTBY_TR_PBMN` | 비차익 위탁 순매수 거래 대금 | String | 1 | Y |  |
| `NABT_ONSL_NTBY_QTY` | 비차익 자기 순매수 수량 | String | 1 | Y |  |
| `NABT_ONSL_NTBY_TR_PBMN` | 비차익 자기 순매수 거래 대금 | String | 1 | Y |  |
| `ACML_VOL` | 누적 거래량 | String | 1 | Y |  |
| `ACML_TR_PBMN` | 누적 거래 대금 | String | 1 | Y |  |

### 응답 예시

```json
# 연결 확인
{
    "header": {
        "tr_id": "H0UPPGM0", 
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
0|H0UPPGM0|001|0001^085913^0^0^0^0^0^0^1^0^0^0^0^0^1^0^10^0^0^0.00^0^0.00^0^
0.00^0^0.00^0^0.00^0^0.00^0^0.00^1^0.00^1^0.00^10^0.00^1^0.00^9^0.00^0^0.00^1^0.00^1^0.00^10^0
.00^1^0.00^9^0.00^0^0.00^0^0.00^0^0.00^0^0.00^0^0.00^0^0.00^0^0.00^1^0.00^1^0.00^10^0.00^1^0.0
0^9^0.00^0^0^0^0^1^9^0^0^0^0
```

