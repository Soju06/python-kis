# 주식선물 실시간체결가 [실시간-029]

> [국내선물옵션] 실시간시세



## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `fc5bcd3a-4b96-423d-b315-ea3f758fbcd7` |
| **HTTP Method** | `POST` |
| **URL** | `/tryitout/H0ZFCNT0` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `ws://ops.koreainvestment.com:21000` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `H0ZFCNT0` |
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
| `tr_id` | 거래ID | String | 7 | Y | H0ZFCNT0 |
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
      "tr_id": "H0ZFCNT0",
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
| `STCK_PRPR` | 주식현재가 | String | 4 | Y |  |
| `PRDY_VRSS_SIGN` | 전일대비부호 | String | 1 | Y |  |
| `PRDY_VRSS` | 전일대비 | String | 4 | Y |  |
| `FUTS_PRDY_CTRT` | 선물전일대비율 | String | 8 | Y |  |
| `STCK_OPRC` | 주식시가2 | String | 4 | Y |  |
| `STCK_HGPR` | 주식최고가 | String | 4 | Y |  |
| `STCK_LWPR` | 주식최저가 | String | 4 | Y |  |
| `LAST_CNQN` | 최종거래량 | String | 8 | Y |  |
| `ACML_VOL` | 누적거래량 | String | 8 | Y |  |
| `ACML_TR_PBMN` | 누적거래대금 | String | 8 | Y |  |
| `HTS_THPR` | HTS이론가 | String | 8 | Y |  |
| `MRKT_BASIS` | 시장베이시스 | String | 8 | Y |  |
| `DPRT` | 괴리율 | String | 8 | Y |  |
| `NMSC_FCTN_STPL_PRC` | 근월물약정가 | String | 8 | Y |  |
| `FMSC_FCTN_STPL_PRC` | 원월물약정가 | String | 8 | Y |  |
| `SPEAD_PRC` | 스프레드1 | String | 8 | Y |  |
| `HTS_OTST_STPL_QTY` | HTS미결제약정수량 | String | 8 | Y |  |
| `OTST_STPL_QTY_ICDC` | 미결제약정수량증감 | String | 4 | Y |  |
| `OPRC_HOUR` | 시가시간 | String | 6 | Y |  |
| `OPRC_VRSS_PRPR_SIGN` | 시가2대비현재가부호 | String | 1 | Y |  |
| `OPRC_VRSS_PRPR` | 시가2대비현재가 | String | 4 | Y |  |
| `HGPR_HOUR` | 최고가시간 | String | 6 | Y |  |
| `HGPR_VRSS_PRPR_SIGN` | 최고가대비현재가부호 | String | 1 | Y |  |
| `HGPR_VRSS_PRPR` | 최고가대비현재가 | String | 4 | Y |  |
| `LWPR_HOUR` | 최저가시간 | String | 6 | Y |  |
| `LWPR_VRSS_PRPR_SIGN` | 최저가대비현재가부호 | String | 1 | Y |  |
| `LWPR_VRSS_PRPR` | 최저가대비현재가 | String | 4 | Y |  |
| `SHNU_RATE` | 매수2비율 | String | 8 | Y |  |
| `CTTR` | 체결강도 | String | 8 | Y |  |
| `ESDG` | 괴리도 | String | 8 | Y |  |
| `OTST_STPL_RGBF_QTY_ICDC` | 미결제약정직전수량증감 | String | 4 | Y |  |
| `THPR_BASIS` | 이론베이시스 | String | 8 | Y |  |
| `ASKP1` | 매도호가1 | String | 4 | Y |  |
| `BIDP1` | 매수호가1 | String | 4 | Y |  |
| `ASKP_RSQN1` | 매도호가잔량1 | String | 8 | Y |  |
| `BIDP_RSQN1` | 매수호가잔량1 | String | 8 | Y |  |
| `SELN_CNTG_CSNU` | 매도체결건수 | String | 4 | Y |  |
| `SHNU_CNTG_CSNU` | 매수체결건수 | String | 4 | Y |  |
| `NTBY_CNTG_CSNU` | 순매수체결건수 | String | 4 | Y |  |
| `SELN_CNTG_SMTN` | 총매도수량 | String | 8 | Y |  |
| `SHNU_CNTG_SMTN` | 총매수수량 | String | 8 | Y |  |
| `TOTAL_ASKP_RSQN` | 총매도호가잔량 | String | 8 | Y |  |
| `TOTAL_BIDP_RSQN` | 총매수호가잔량 | String | 8 | Y |  |
| `PRDY_VOL_VRSS_ACML_VOL_RATE` | 전일거래량대비등락율 | String | 8 | Y |  |
| `DYNM_MXPR` | 실시간상한가 | String | 4 | Y |  |
| `DYNM_LLAM` | 실시간하한가 | String | 4 | Y |  |
| `DYNM_PRC_LIMT_YN` | 실시간가격제한구분 | String | 1 | Y |  |

### 응답 예시

```json
# 연결 확인
{
    "header": {
        "tr_id": "H0ZFCNT0", 
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
0|H0ZFCNT0|001|111V06^091639^77900^5^-100^-0.13^77900^77900^77300^5^1724^13
37128000^77899.50^400.00^0.00^0.00^0.00^-500.00^32053^219^000000^3^0^000000^3^0^000000^2^600^
0.36^58.23^0.50^-1^399.50^77900^77800^0^0^105^36^-69^1075^626^0^0^6.23^0^0^0
```

