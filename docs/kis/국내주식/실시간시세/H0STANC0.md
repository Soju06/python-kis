# 국내주식 실시간예상체결 (KRX) [실시간-041]

> [국내주식] 실시간시세

국내주식 실시간예상체결 API입니다.

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
| **API ID** | `970a5802-434c-4a45-b714-5325385d47a3` |
| **HTTP Method** | `POST` |
| **URL** | `/tryitout/H0STANC0` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `ws://ops.koreainvestment.com:21000` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `H0STANC0` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-04-26T09:34:16+09:00
- **최종 수정일**: 2025-04-30T13:12:35+09:00

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
| `tr_id` | 거래ID | String | 2 | Y | H0STANC0 |
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
      "tr_id": "H0STANC0",
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
| `STCK_CNTG_HOUR` | 주식체결시간 | String | 6 | Y |  |
| `STCK_PRPR` | 주식현재가 | String | 4 | Y |  |
| `PRDY_VRSS_SIGN` | 전일대비구분 | String | 1 | Y |  |
| `PRDY_VRSS` | 전일대비 | String | 4 | Y |  |
| `PRDY_CTRT` | 등락율 | String | 8 | Y |  |
| `WGHN_AVRG_STCK_PRC` | 가중평균주식가격 | String | 8 | Y |  |
| `STCK_OPRC` | 시가 | String | 4 | Y |  |
| `STCK_HGPR` | 고가 | String | 4 | Y |  |
| `STCK_LWPR` | 저가 | String | 4 | Y |  |
| `ASKP1` | 매도호가 | String | 4 | Y |  |
| `BIDP1` | 매수호가 | String | 4 | Y |  |
| `CNTG_VOL` | 거래량 | String | 8 | Y |  |
| `ACML_VOL` | 누적거래량 | String | 8 | Y |  |
| `ACML_TR_PBMN` | 누적거래대금 | String | 8 | Y |  |
| `SELN_CNTG_CSNU` | 매도체결건수 | String | 4 | Y |  |
| `SHNU_CNTG_CSNU` | 매수체결건수 | String | 4 | Y |  |
| `NTBY_CNTG_CSNU` | 순매수체결건수 | String | 4 | Y |  |
| `CTTR` | 체결강도 | String | 8 | Y |  |
| `SELN_CNTG_SMTN` | 총매도수량 | String | 8 | Y |  |
| `SHNU_CNTG_SMTN` | 총매수수량 | String | 8 | Y |  |
| `CNTG_CLS_CODE` | 체결구분 | String | 1 | Y |  |
| `SHNU_RATE` | 매수비율 | String | 8 | Y |  |
| `PRDY_VOL_VRSS_ACML_VOL_RATE` | 전일거래량대비등락율 | String | 8 | Y |  |
| `OPRC_HOUR` | 시가시간 | String | 6 | Y |  |
| `OPRC_VRSS_PRPR_SIGN` | 시가대비구분 | String | 1 | Y |  |
| `OPRC_VRSS_PRPR` | 시가대비 | String | 4 | Y |  |
| `HGPR_HOUR` | 최고가시간 | String | 6 | Y |  |
| `HGPR_VRSS_PRPR_SIGN` | 고가대비구분 | String | 1 | Y |  |
| `HGPR_VRSS_PRPR` | 고가대비 | String | 4 | Y |  |
| `LWPR_HOUR` | 최저가시간 | String | 6 | Y |  |
| `LWPR_VRSS_PRPR_SIGN` | 저가대비구분 | String | 1 | Y |  |
| `LWPR_VRSS_PRPR` | 저가대비 | String | 4 | Y |  |
| `BSOP_DATE` | 영업일자 | String | 8 | Y |  |
| `NEW_MKOP_CLS_CODE` | 신장운영구분코드 | String | 2 | Y |  |
| `TRHT_YN` | 거래정지여부 | String | 1 | Y |  |
| `ASKP_RSQN1` | 매도호가잔량1 | String | 8 | Y |  |
| `BIDP_RSQN1` | 매수호가잔량1 | String | 8 | Y |  |
| `TOTAL_ASKP_RSQN` | 총매도호가잔량 | String | 8 | Y |  |
| `TOTAL_BIDP_RSQN` | 총매수호가잔량 | String | 8 | Y |  |
| `VOL_TNRT` | 거래량회전율 | String | 8 | Y |  |
| `PRDY_SMNS_HOUR_ACML_VOL` | 전일동시간누적거래량 | String | 8 | Y |  |
| `PRDY_SMNS_HOUR_ACML_VOL_RATE` | 전일동시간누적거래량비율 | String | 8 | Y |  |
| `HOUR_CLS_CODE` | 시간구분코드 | String | 1 | Y |  |
| `MRKT_TRTM_CLS_CODE` | 임의종료구분코드 | String | 1 | Y |  |

### 응답 예시

```json
# 연결 확인
{
    "header": {
        "tr_id": "H0STANC0", 
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
0|H0STANC0|001|005930^084945^77600^2^1300^1.70^0.00^0^0^0^77600^77
500^64^221986^17226113600^0^0^0^0.00^0^0^1^0.01^0.00^000000^3^0^000000^3^0^000000^3^
0^20240426^00^N^11591^2878^41034^6265^0.00^0^0.00^B^
```

