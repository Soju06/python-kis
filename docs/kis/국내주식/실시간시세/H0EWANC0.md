# ELW 실시간예상체결 [실시간-063]

> [국내주식] 실시간시세

ELW 실시간예상체결 API입니다.

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
| **API ID** | `d8302223-2381-46cc-81df-c756df21d12b` |
| **HTTP Method** | `POST` |
| **URL** | `/tryitout/H0EWANC0` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `ws://ops.koreainvestment.com:21000` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID** | `H0EWANC0`, `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-05-10
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
| `tr_id` | 거래ID | String | 2 | Y | H0EWANC0 |
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
      "tr_id": "H0EWANC0",
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
| `STCK_CNTG_HOUR` | 주식체결시간 | String | 6 | Y |  |
| `STCK_PRPR` | 주식현재가 | String | 1 | Y |  |
| `PRDY_VRSS_SIGN` | 전일대비부호 | String | 1 | Y |  |
| `PRDY_VRSS` | 전일대비 | String | 1 | Y |  |
| `PRDY_CTRT` | 전일대비율 | String | 1 | Y |  |
| `WGHN_AVRG_STCK_PRC` | 가중평균주식가격 | String | 1 | Y |  |
| `STCK_OPRC` | 주식시가2 | String | 1 | Y |  |
| `STCK_HGPR` | 주식최고가 | String | 1 | Y |  |
| `STCK_LWPR` | 주식최저가 | String | 1 | Y |  |
| `ASKP1` | 매도호가1 | String | 1 | Y |  |
| `BIDP1` | 매수호가1 | String | 1 | Y |  |
| `CNTG_VOL` | 체결거래량 | String | 1 | Y |  |
| `ACML_VOL` | 누적거래량 | String | 1 | Y |  |
| `ACML_TR_PBMN` | 누적거래대금 | String | 1 | Y |  |
| `SELN_CNTG_CSNU` | 매도체결건수 | String | 1 | Y |  |
| `SHNU_CNTG_CSNU` | 매수체결건수 | String | 1 | Y |  |
| `NTBY_CNTG_CSNU` | 순매수체결건수 | String | 1 | Y |  |
| `CTTR` | 체결강도 | String | 1 | Y |  |
| `SELN_CNTG_SMTN` | 총매도수량 | String | 1 | Y |  |
| `SHNU_CNTG_SMTN` | 총매수수량 | String | 1 | Y |  |
| `CNTG_CLS_CODE` | 체결구분코드 | String | 1 | Y |  |
| `SHNU_RATE` | 매수2비율 | String | 1 | Y |  |
| `PRDY_VOL_VRSS_ACML_VOL_RATE` | 전일거래량대비등락율 | String | 1 | Y |  |
| `OPRC_HOUR` | 시가시간 | String | 6 | Y |  |
| `OPRC_VRSS_PRPR_SIGN` | 시가2대비현재가부호 | String | 1 | Y |  |
| `OPRC_VRSS_PRPR` | 시가2대비현재가 | String | 1 | Y |  |
| `HGPR_HOUR` | 최고가시간 | String | 6 | Y |  |
| `HGPR_VRSS_PRPR_SIGN` | 최고가대비현재가부호 | String | 1 | Y |  |
| `HGPR_VRSS_PRPR` | 최고가대비현재가 | String | 1 | Y |  |
| `LWPR_HOUR` | 최저가시간 | String | 6 | Y |  |
| `LWPR_VRSS_PRPR_SIGN` | 최저가대비현재가부호 | String | 1 | Y |  |
| `LWPR_VRSS_PRPR` | 최저가대비현재가 | String | 1 | Y |  |
| `BSOP_DATE` | 영업일자 | String | 8 | Y |  |
| `NEW_MKOP_CLS_CODE` | 신장운영구분코드 | String | 2 | Y |  |
| `TRHT_YN` | 거래정지여부 | String | 1 | Y |  |
| `ASKP_RSQN1` | 매도호가잔량1 | String | 1 | Y |  |
| `BIDP_RSQN1` | 매수호가잔량1 | String | 1 | Y |  |
| `TOTAL_ASKP_RSQN` | 총매도호가잔량 | String | 1 | Y |  |
| `TOTAL_BIDP_RSQN` | 총매수호가잔량 | String | 1 | Y |  |
| `TMVL_VAL` | 시간가치값 | String | 1 | Y |  |
| `PRIT` | 패리티 | String | 1 | Y |  |
| `PRMM_VAL` | 프리미엄값 | String | 1 | Y |  |
| `GEAR` | 기어링 | String | 1 | Y |  |
| `PRLS_QRYR_RATE` | 손익분기비율 | String | 1 | Y |  |
| `INVL_VAL` | 내재가치값 | String | 1 | Y |  |
| `PRMM_RATE` | 프리미엄비율 | String | 1 | Y |  |
| `CFP` | 자본지지점 | String | 1 | Y |  |
| `LVRG_VAL` | 레버리지값 | String | 1 | Y |  |
| `DELTA` | 델타 | String | 1 | Y |  |
| `GAMA` | 감마 | String | 1 | Y |  |
| `VEGA` | 베가 | String | 1 | Y |  |
| `THETA` | 세타 | String | 1 | Y |  |
| `RHO` | 로우 | String | 1 | Y |  |
| `HTS_INTS_VLTL` | HTS내재변동성 | String | 1 | Y |  |
| `HTS_THPR` | HTS이론가 | String | 1 | Y |  |
| `VOL_TNRT` | 거래량회전율 | String | 1 | Y |  |
| `LP_HVOL` | LP보유량 | String | 1 | Y |  |
| `LP_HLDN_RATE` | LP보유비율 | String | 1 | Y |  |

### 응답 예시

```json
# 연결 확인
{
    "header": {
        "tr_id": "H0EWANC0", 
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
```
