# 주식옵션 실시간체결가 [실시간-044]

> [국내선물옵션] 실시간시세

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `ee7973de-54a7-4b34-9a31-b34a4294d606` |
| **HTTP Method** | `POST` |
| **URL** | `/tryitout/H0ZOCNT0` |
| **Content-Type** | `` |
| **요청 포맷** | `` |
| **실전 도메인** | `ws://ops.koreainvestment.com:21000` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID** | `모의투자 미지원`, `H0ZOCNT0` |

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
| `tr_id` | 거래ID | String | 7 | Y | H0ZOCNT0 |
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
      "tr_id": "H0ZOCNT0",
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
| `OPTN_PRPR` | 옵션현재가 | String | 1 | Y |  |
| `PRDY_VRSS_SIGN` | 전일대비부호 | String | 1 | Y |  |
| `OPTN_PRDY_VRSS` | 옵션전일대비 | String | 1 | Y |  |
| `PRDY_CTRT` | 전일대비율 | String | 1 | Y |  |
| `OPTN_OPRC` | 옵션시가2 | String | 1 | Y |  |
| `OPTN_HGPR` | 옵션최고가 | String | 1 | Y |  |
| `OPTN_LWPR` | 옵션최저가 | String | 1 | Y |  |
| `LAST_CNQN` | 최종거래량 | String | 1 | Y |  |
| `ACML_VOL` | 누적거래량 | String | 1 | Y |  |
| `ACML_TR_PBMN` | 누적거래대금 | String | 1 | Y |  |
| `HTS_THPR` | HTS이론가 | String | 1 | Y |  |
| `HTS_OTST_STPL_QTY` | HTS미결제약정수량 | String | 1 | Y |  |
| `OTST_STPL_QTY_ICDC` | 미결제약정수량증감 | String | 1 | Y |  |
| `OPRC_HOUR` | 시가시간 | String | 6 | Y |  |
| `OPRC_VRSS_PRPR_SIGN` | 시가2대비현재가부호 | String | 1 | Y |  |
| `OPRC_VRSS_NMIX_PRPR` | 시가대비지수현재가 | String | 1 | Y |  |
| `HGPR_HOUR` | 최고가시간 | String | 6 | Y |  |
| `HGPR_VRSS_PRPR_SIGN` | 최고가대비현재가부호 | String | 1 | Y |  |
| `HGPR_VRSS_NMIX_PRPR` | 최고가대비지수현재가 | String | 1 | Y |  |
| `LWPR_HOUR` | 최저가시간 | String | 6 | Y |  |
| `LWPR_VRSS_PRPR_SIGN` | 최저가대비현재가부호 | String | 1 | Y |  |
| `LWPR_VRSS_NMIX_PRPR` | 최저가대비지수현재가 | String | 1 | Y |  |
| `SHNU_RATE` | 매수2비율 | String | 1 | Y |  |
| `PRMM_VAL` | 프리미엄값 | String | 1 | Y |  |
| `INVL_VAL` | 내재가치값 | String | 1 | Y |  |
| `TMVL_VAL` | 시간가치값 | String | 1 | Y |  |
| `DELTA` | 델타 | String | 1 | Y |  |
| `GAMA` | 감마 | String | 1 | Y |  |
| `VEGA` | 베가 | String | 1 | Y |  |
| `THETA` | 세타 | String | 1 | Y |  |
| `RHO` | 로우 | String | 1 | Y |  |
| `HTS_INTS_VLTL` | HTS내재변동성 | String | 1 | Y |  |
| `ESDG` | 괴리도 | String | 1 | Y |  |
| `OTST_STPL_RGBF_QTY_ICDC` | 미결제약정직전수량증감 | String | 1 | Y |  |
| `THPR_BASIS` | 이론베이시스 | String | 1 | Y |  |
| `UNAS_HIST_VLTL` | 역사적변동성 | String | 1 | Y |  |
| `CTTR` | 체결강도 | String | 1 | Y |  |
| `DPRT` | 괴리율 | String | 1 | Y |  |
| `MRKT_BASIS` | 시장베이시스 | String | 1 | Y |  |
| `OPTN_ASKP1` | 옵션매도호가1 | String | 1 | Y |  |
| `OPTN_BIDP1` | 옵션매수호가1 | String | 1 | Y |  |
| `ASKP_RSQN1` | 매도호가잔량1 | String | 1 | Y |  |
| `BIDP_RSQN1` | 매수호가잔량1 | String | 1 | Y |  |
| `SELN_CNTG_CSNU` | 매도체결건수 | String | 1 | Y |  |
| `SHNU_CNTG_CSNU` | 매수체결건수 | String | 1 | Y |  |
| `NTBY_CNTG_CSNU` | 순매수체결건수 | String | 1 | Y |  |
| `SELN_CNTG_SMTN` | 총매도수량 | String | 1 | Y |  |
| `SHNU_CNTG_SMTN` | 총매수수량 | String | 1 | Y |  |
| `TOTAL_ASKP_RSQN` | 총매도호가잔량 | String | 1 | Y |  |
| `TOTAL_BIDP_RSQN` | 총매수호가잔량 | String | 1 | Y |  |
| `PRDY_VOL_VRSS_ACML_VOL_RATE` | 전일거래량대비등락율 | String | 1 | Y |  |

### 응답 예시

```json
# 연결 확인
{
    "header": {
        "tr_id": "H0ZOCNT0", 
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
0|H0ZOCNT0|001|211V05059^091940^1060.00^5^-120.00^-10.17^970.00^1140.00^970
.00^6^563^5933200^35464.07^1134^-2^000000^2^90.00^000000^5^-80.00^000000^2^90.00^0.43^0.00^0.
00^1060.00^1.00^0.00^0.00^-4.06^20.58^0.31^-34404.07^0^-41735.93^0.26^74.84^-97.01^-76140.00^
1100.00^1040.00^6^175^13^16^3^322^241^241^184^12.33
```
