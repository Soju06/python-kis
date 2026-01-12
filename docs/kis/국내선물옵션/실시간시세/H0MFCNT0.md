# KRX야간선물 실시간종목체결 [실시간-064]

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
| **API ID** | `3d10c790-f3dd-4837-b048-cc5a45b678b8` |
| **HTTP Method** | `POST` |
| **URL** | `/tryitout/H0MFCNT0` |
| **Content-Type** | `` |
| **요청 포맷** | `` |
| **실전 도메인** | `ws://ops.koreainvestment.com:21000` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID** | `모의투자 미지원`, `H0MFCNT0` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-05-24
- **최종 수정일**: 2025-06-30

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
| `tr_id` | 거래ID | String | 2 | Y | H0MFCNT0 |
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
      "tr_id": "H0MFCNT0",
      "tr_key": "101V06"
    }
  }
}
```

## 응답 (Response)

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `FUTS_SHRN_ISCD` | 선물 단축 종목코드 | String | 9 | Y |  |
| `BSOP_HOUR` | 영업 시간 | String | 6 | Y |  |
| `FUTS_PRDY_VRSS` | 선물 전일 대비 | String | 1 | Y |  |
| `PRDY_VRSS_SIGN` | 전일 대비 부호 | String | 1 | Y |  |
| `FUTS_PRDY_CTRT` | 선물 전일 대비율 | String | 1 | Y |  |
| `FUTS_PRPR` | 선물 현재가 | String | 1 | Y |  |
| `FUTS_OPRC` | 선물 시가2 | String | 1 | Y |  |
| `FUTS_HGPR` | 선물 최고가 | String | 1 | Y |  |
| `FUTS_LWPR` | 선물 최저가 | String | 1 | Y |  |
| `LAST_CNQN` | 최종 거래량 | String | 1 | Y |  |
| `ACML_VOL` | 누적 거래량 | String | 1 | Y |  |
| `ACML_TR_PBMN` | 누적 거래 대금 | String | 1 | Y |  |
| `HTS_THPR` | HTS 이론가 | String | 1 | Y |  |
| `MRKT_BASIS` | 시장 베이시스 | String | 1 | Y |  |
| `DPRT` | 괴리율 | String | 1 | Y |  |
| `NMSC_FCTN_STPL_PRC` | 근월물 약정가 | String | 1 | Y |  |
| `FMSC_FCTN_STPL_PRC` | 원월물 약정가 | String | 1 | Y |  |
| `SPEAD_PRC` | 스프레드1 | String | 1 | Y |  |
| `HTS_OTST_STPL_QTY` | HTS 미결제 약정 수량 | String | 1 | Y |  |
| `OTST_STPL_QTY_ICDC` | 미결제 약정 수량 증감 | String | 1 | Y |  |
| `OPRC_HOUR` | 시가 시간 | String | 6 | Y |  |
| `OPRC_VRSS_PRPR_SIGN` | 시가2 대비 현재가 부호 | String | 1 | Y |  |
| `OPRC_VRSS_NMIX_PRPR` | 시가 대비 지수 현재가 | String | 1 | Y |  |
| `HGPR_HOUR` | 최고가 시간 | String | 6 | Y |  |
| `HGPR_VRSS_PRPR_SIGN` | 최고가 대비 현재가 부호 | String | 1 | Y |  |
| `HGPR_VRSS_NMIX_PRPR` | 최고가 대비 지수 현재가 | String | 1 | Y |  |
| `LWPR_HOUR` | 최저가 시간 | String | 6 | Y |  |
| `LWPR_VRSS_PRPR_SIGN` | 최저가 대비 현재가 부호 | String | 1 | Y |  |
| `LWPR_VRSS_NMIX_PRPR` | 최저가 대비 지수 현재가 | String | 1 | Y |  |
| `SHNU_RATE` | 매수2 비율 | String | 1 | Y |  |
| `CTTR` | 체결강도 | String | 1 | Y |  |
| `ESDG` | 괴리도 | String | 1 | Y |  |
| `OTST_STPL_RGBF_QTY_ICDC` | 미결제 약정 직전 수량 증감 | String | 1 | Y |  |
| `THPR_BASIS` | 이론 베이시스 | String | 1 | Y |  |
| `FUTS_ASKP1` | 선물 매도호가1 | String | 1 | Y |  |
| `FUTS_BIDP1` | 선물 매수호가1 | String | 1 | Y |  |
| `ASKP_RSQN1` | 매도호가 잔량1 | String | 1 | Y |  |
| `BIDP_RSQN1` | 매수호가 잔량1 | String | 1 | Y |  |
| `SELN_CNTG_CSNU` | 매도 체결 건수 | String | 1 | Y |  |
| `SHNU_CNTG_CSNU` | 매수 체결 건수 | String | 1 | Y |  |
| `NTBY_CNTG_CSNU` | 순매수 체결 건수 | String | 1 | Y |  |
| `SELN_CNTG_SMTN` | 총 매도 수량 | String | 1 | Y |  |
| `SHNU_CNTG_SMTN` | 총 매수 수량 | String | 1 | Y |  |
| `TOTAL_ASKP_RSQN` | 총 매도호가 잔량 | String | 1 | Y |  |
| `TOTAL_BIDP_RSQN` | 총 매수호가 잔량 | String | 1 | Y |  |
| `PRDY_VOL_VRSS_ACML_VOL_RATE` | 전일 거래량 대비 등락율 | String | 1 | Y |  |
| `DYNM_MXPR` | 실시간상한가 | String | 8 | Y |  |
| `DYNM_LLAM` | 실시간하한가 | String | 8 | Y |  |
| `DYNM_PRC_LIMT_YN` | 실시간가격제한구분 | String | 1 | Y |  |

### 응답 예시

```json
# 연결 확인
{
    "header": {
        "tr_id": "H0MFCNT0", 
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
0|H0MFCNT0|001|101V06^190215^0.75^2^0.20^367.30^367.10^367.60^367.05^2^1596^1465526
87^366.08^1.22^0.33^0.00^0.00^0.00^268223^0^000000^2^0.20^000000^5^-0.30^000000^2^0.25^0.49^96.31^1.2
2^0^0.00^367.35^367.30^0^0^345^358^13^813^783^0^0^0.00
```
