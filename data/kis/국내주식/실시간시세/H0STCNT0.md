# 국내주식 실시간체결가 (KRX) [실시간-003]

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

※ 데이터가 많은 경우 여러 건을 페이징 처리해서 데이터를 보내는 점 참고 부탁드립니다.
ex) 0|H0STCNT0|004|... 인 경우 004가 데이터 개수를 의미하여, 뒤에 체결데이터가 4건 들어옴
→ 0|H0STCNT0|004|005930^123929...(체결데이터1)...^005930^123929...(체결데이터2)...^005930^123929...(체결데이터3)...^005930^123929...(체결데이터4)...

[실시간-003] 국내주식 실시간체결가

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `714d1437-8f62-43db-a73c-cf509d3f6aa7` |
| **HTTP Method** | `POST` |
| **URL** | `/tryitout/H0STCNT0` |
| **Content-Type** | `text/plain` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | ` ws://ops.koreainvestment.com:21000` |
| **모의 도메인** | ` ws://ops.koreainvestment.com:31000` |
| **TR ID (실전)** | `H0STCNT0` |
| **TR ID (모의)** | `H0STCNT0` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2021-12-15T13:15:42+09:00
- **최종 수정일**: 2025-04-30T13:09:53+09:00

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `approval_key` | 웹소켓 접속키 | String | 286 | Y | 실시간 (웹소켓) 접속키 발급 API(/oauth2/Approval)를 사용하여 발급받은 웹소켓 접속키 |
| `custtype` | 고객타입 | String | 1 | Y | B : 법인 P : 개인 |
| `tr_type` | 거래타입 | String | 1 | Y | 1 : 등록 2 : 해제 |
| `content-type` | 컨텐츠타입 | String | 1 | Y | utf-8 |

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `tr_id` | 거래ID | String | 1 | Y | [실전/모의투자] H0STCNT0 : 실시간 주식 체결가 |
| `tr_key` | 구분값 | String | 1 | Y | 종목번호 (6자리) ETN의 경우, Q로 시작 (EX. Q500001) |

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
      "tr_id": "H0STCNT0",
      "tr_key": "005930"
    }
  }
}
```

## 응답

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `MKSC_SHRN_ISCD` | 유가증권 단축 종목코드 | String | 9 | Y |  |
| `STCK_CNTG_HOUR` | 주식 체결 시간 | String | 6 | Y |  |
| `STCK_PRPR` | 주식 현재가 | Number | 4 | Y | 체결가격 |
| `PRDY_VRSS_SIGN` | 전일 대비 부호 | String | 1 | Y | 1 : 상한 2 : 상승 3 : 보합 4 : 하한 5 : 하락 |
| `PRDY_VRSS` | 전일 대비 | Number | 4 | Y |  |
| `PRDY_CTRT` | 전일 대비율 | Number | 8 | Y |  |
| `WGHN_AVRG_STCK_PRC` | 가중 평균 주식 가격 | Number | 8 | Y |  |
| `STCK_OPRC` | 주식 시가 | Number | 4 | Y |  |
| `STCK_HGPR` | 주식 최고가 | Number | 4 | Y |  |
| `STCK_LWPR` | 주식 최저가 | Number | 4 | Y |  |
| `ASKP1` | 매도호가1 | Number | 4 | Y |  |
| `BIDP1` | 매수호가1 | Number | 4 | Y |  |
| `CNTG_VOL` | 체결 거래량 | Number | 8 | Y |  |
| `ACML_VOL` | 누적 거래량 | Number | 8 | Y |  |
| `ACML_TR_PBMN` | 누적 거래 대금 | Number | 8 | Y |  |
| `SELN_CNTG_CSNU` | 매도 체결 건수 | Number | 4 | Y |  |
| `SHNU_CNTG_CSNU` | 매수 체결 건수 | Number | 4 | Y |  |
| `NTBY_CNTG_CSNU` | 순매수 체결 건수 | Number | 4 | Y |  |
| `CTTR` | 체결강도 | Number | 8 | Y |  |
| `SELN_CNTG_SMTN` | 총 매도 수량 | Number | 8 | Y |  |
| `SHNU_CNTG_SMTN` | 총 매수 수량 | Number | 8 | Y |  |
| `CCLD_DVSN` | 체결구분 | String | 1 | Y | 1:매수(+)  3:장전  5:매도(-) |
| `SHNU_RATE` | 매수비율 | Number | 8 | Y |  |
| `PRDY_VOL_VRSS_ACML_VOL_RATE` | 전일 거래량 대비 등락율 | Number | 8 | Y |  |
| `OPRC_HOUR` | 시가 시간 | String | 6 | Y |  |
| `OPRC_VRSS_PRPR_SIGN` | 시가대비구분 | String | 1 | Y | 1 : 상한 2 : 상승 3 : 보합 4 : 하한 5 : 하락 |
| `OPRC_VRSS_PRPR` | 시가대비 | Number | 4 | Y |  |
| `HGPR_HOUR` | 최고가 시간 | String | 6 | Y |  |
| `HGPR_VRSS_PRPR_SIGN` | 고가대비구분 | String | 1 | Y | 1 : 상한 2 : 상승 3 : 보합 4 : 하한 5 : 하락 |
| `HGPR_VRSS_PRPR` | 고가대비 | Number | 4 | Y |  |
| `LWPR_HOUR` | 최저가 시간 | String | 6 | Y |  |
| `LWPR_VRSS_PRPR_SIGN` | 저가대비구분 | String | 1 | Y | 1 : 상한 2 : 상승 3 : 보합 4 : 하한 5 : 하락 |
| `LWPR_VRSS_PRPR` | 저가대비 | Number | 4 | Y |  |
| `BSOP_DATE` | 영업 일자 | String | 8 | Y |  |
| `NEW_MKOP_CLS_CODE` | 신 장운영 구분 코드 | String | 2 | Y | (1) 첫 번째 비트 1 : 장개시전 2 : 장중 3 : 장종료후 4 : 시간외단일가 7 : 일반Buy-in 8 : 당일Buy-in  (2) 두 번째 비트 0 : 보통 1 : 종가 2 : 대량 3 : 바스켓 7 : 정리매매 8 : Buy-in |
| `TRHT_YN` | 거래정지 여부 | String | 1 | Y | Y : 정지 N : 정상거래 |
| `ASKP_RSQN1` | 매도호가 잔량1 | Number | 8 | Y |  |
| `BIDP_RSQN1` | 매수호가 잔량1 | Number | 8 | Y |  |
| `TOTAL_ASKP_RSQN` | 총 매도호가 잔량 | Number | 8 | Y |  |
| `TOTAL_BIDP_RSQN` | 총 매수호가 잔량 | Number | 8 | Y |  |
| `VOL_TNRT` | 거래량 회전율 | Number | 8 | Y |  |
| `PRDY_SMNS_HOUR_ACML_VOL` | 전일 동시간 누적 거래량 | Number | 8 | Y |  |
| `PRDY_SMNS_HOUR_ACML_VOL_RATE` | 전일 동시간 누적 거래량 비율 | Number | 8 | Y |  |
| `HOUR_CLS_CODE` | 시간 구분 코드 | String | 1 | Y | 0 : 장중 A : 장후예상 B : 장전예상 C : 9시이후의 예상가, VI발동 D : 시간외 단일가 예상 |
| `MRKT_TRTM_CLS_CODE` | 임의종료구분코드 | String | 1 | Y |  |
| `VI_STND_PRC` | 정적VI발동기준가 | Number | 4 | Y |  |

### 응답 예시

```json
# 연결 확인
{
    "header": {
        "tr_id": "H0STCNT0", 
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
005930^093354^71900^5^-100^-0.14^72023.83^72100^72400^71700^71900^71800^1^3052
507^219853241700^5105^6937^1832^84.90^1366314^1159996^1^0.39^20.28^090020^5^-2
00^090820^5^-500^092619^2^200^20230612^20^N^65945^216924^1118750^2199206^0.05^
2424142^125.92^0^^72100
```

