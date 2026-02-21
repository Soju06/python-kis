# 국내주식 실시간회원사 (KRX) [실시간-047]

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
| **API ID** | `dbd893be-725c-429d-81eb-8b69cbeb3222` |
| **HTTP Method** | `POST` |
| **URL** | `/tryitout/H0STMBC0` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `ws://ops.koreainvestment.com:21000` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `H0STMBC0` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-04-19T09:39:33+09:00
- **최종 수정일**: 2025-04-30T13:10:48+09:00

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
| `tr_id` | 거래ID | String | 7 | Y | H0STMBC0 |
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
      "tr_id": "H0STMBC0",
      "tr_key": "005930"
    }
  }
}
```

## 응답

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `MKSC_SHRN_ISCD` | 유가증권단축종목코드 | String | 9 | Y | '각 항목사이에는 구분자로 ^ 사용, 모든 데이터타입은 String으로 변환되어 push 처리됨' |
| `SELN2_MBCR_NAME1` | 매도2회원사명1 | String | 16 | Y |  |
| `SELN2_MBCR_NAME2` | 매도2회원사명2 | String | 16 | Y |  |
| `SELN2_MBCR_NAME3` | 매도2회원사명3 | String | 16 | Y |  |
| `SELN2_MBCR_NAME4` | 매도2회원사명4 | String | 16 | Y |  |
| `SELN2_MBCR_NAME5` | 매도2회원사명5 | String | 16 | Y |  |
| `BYOV_MBCR_NAME1` | 매수회원사명1 | String | 16 | Y |  |
| `BYOV_MBCR_NAME2` | 매수회원사명2 | String | 16 | Y |  |
| `BYOV_MBCR_NAME3` | 매수회원사명3 | String | 16 | Y |  |
| `BYOV_MBCR_NAME4` | 매수회원사명4 | String | 16 | Y |  |
| `BYOV_MBCR_NAME5` | 매수회원사명5 | String | 16 | Y |  |
| `TOTAL_SELN_QTY1` | 총매도수량1 | String | 8 | Y |  |
| `TOTAL_SELN_QTY2` | 총매도수량2 | String | 8 | Y |  |
| `TOTAL_SELN_QTY3` | 총매도수량3 | String | 8 | Y |  |
| `TOTAL_SELN_QTY4` | 총매도수량4 | String | 8 | Y |  |
| `TOTAL_SELN_QTY5` | 총매도수량5 | String | 8 | Y |  |
| `TOTAL_SHNU_QTY1` | 총매수2수량1 | String | 8 | Y |  |
| `TOTAL_SHNU_QTY2` | 총매수2수량2 | String | 8 | Y |  |
| `TOTAL_SHNU_QTY3` | 총매수2수량3 | String | 8 | Y |  |
| `TOTAL_SHNU_QTY4` | 총매수2수량4 | String | 8 | Y |  |
| `TOTAL_SHNU_QTY5` | 총매수2수량5 | String | 8 | Y |  |
| `SELN_MBCR_GLOB_YN_1` | 매도거래원구분1 | String | 1 | Y |  |
| `SELN_MBCR_GLOB_YN_2` | 매도거래원구분2 | String | 1 | Y |  |
| `SELN_MBCR_GLOB_YN_3` | 매도거래원구분3 | String | 1 | Y |  |
| `SELN_MBCR_GLOB_YN_4` | 매도거래원구분4 | String | 1 | Y |  |
| `SELN_MBCR_GLOB_YN_5` | 매도거래원구분5 | String | 1 | Y |  |
| `SHNU_MBCR_GLOB_YN_1` | 매수거래원구분1 | String | 1 | Y |  |
| `SHNU_MBCR_GLOB_YN_2` | 매수거래원구분2 | String | 1 | Y |  |
| `SHNU_MBCR_GLOB_YN_3` | 매수거래원구분3 | String | 1 | Y |  |
| `SHNU_MBCR_GLOB_YN_4` | 매수거래원구분4 | String | 1 | Y |  |
| `SHNU_MBCR_GLOB_YN_5` | 매수거래원구분5 | String | 1 | Y |  |
| `SELN_MBCR_NO1` | 매도거래원코드1 | String | 5 | Y |  |
| `SELN_MBCR_NO2` | 매도거래원코드2 | String | 5 | Y |  |
| `SELN_MBCR_NO3` | 매도거래원코드3 | String | 5 | Y |  |
| `SELN_MBCR_NO4` | 매도거래원코드4 | String | 5 | Y |  |
| `SELN_MBCR_NO5` | 매도거래원코드5 | String | 5 | Y |  |
| `SHNU_MBCR_NO1` | 매수거래원코드1 | String | 5 | Y |  |
| `SHNU_MBCR_NO2` | 매수거래원코드2 | String | 5 | Y |  |
| `SHNU_MBCR_NO3` | 매수거래원코드3 | String | 5 | Y |  |
| `SHNU_MBCR_NO4` | 매수거래원코드4 | String | 5 | Y |  |
| `SHNU_MBCR_NO5` | 매수거래원코드5 | String | 5 | Y |  |
| `SELN_MBCR_RLIM1` | 매도회원사비중1 | String | 8 | Y |  |
| `SELN_MBCR_RLIM2` | 매도회원사비중2 | String | 8 | Y |  |
| `SELN_MBCR_RLIM3` | 매도회원사비중3 | String | 8 | Y |  |
| `SELN_MBCR_RLIM4` | 매도회원사비중4 | String | 8 | Y |  |
| `SELN_MBCR_RLIM5` | 매도회원사비중5 | String | 8 | Y |  |
| `SHNU_MBCR_RLIM1` | 매수2회원사비중1 | String | 8 | Y |  |
| `SHNU_MBCR_RLIM2` | 매수2회원사비중2 | String | 8 | Y |  |
| `SHNU_MBCR_RLIM3` | 매수2회원사비중3 | String | 8 | Y |  |
| `SHNU_MBCR_RLIM4` | 매수2회원사비중4 | String | 8 | Y |  |
| `SHNU_MBCR_RLIM5` | 매수2회원사비중5 | String | 8 | Y |  |
| `SELN_QTY_ICDC1` | 매도수량증감1 | String | 4 | Y |  |
| `SELN_QTY_ICDC2` | 매도수량증감2 | String | 4 | Y |  |
| `SELN_QTY_ICDC3` | 매도수량증감3 | String | 4 | Y |  |
| `SELN_QTY_ICDC4` | 매도수량증감4 | String | 4 | Y |  |
| `SELN_QTY_ICDC5` | 매도수량증감5 | String | 4 | Y |  |
| `SHNU_QTY_ICDC1` | 매수2수량증감1 | String | 4 | Y |  |
| `SHNU_QTY_ICDC2` | 매수2수량증감2 | String | 4 | Y |  |
| `SHNU_QTY_ICDC3` | 매수2수량증감3 | String | 4 | Y |  |
| `SHNU_QTY_ICDC4` | 매수2수량증감4 | String | 4 | Y |  |
| `SHNU_QTY_ICDC5` | 매수2수량증감5 | String | 4 | Y |  |
| `GLOB_TOTAL_SELN_QTY` | 외국계총매도수량 | String | 8 | Y |  |
| `GLOB_TOTAL_SHNU_QTY` | 외국계총매수2수량 | String | 8 | Y |  |
| `GLOB_TOTAL_SELN_QTY_ICDC` | 외국계총매도수량증감 | String | 4 | Y |  |
| `GLOB_TOTAL_SHNU_QTY_ICDC` | 외국계총매수2수량증감 | String | 4 | Y |  |
| `GLOB_NTBY_QTY` | 외국계순매수수량 | String | 8 | Y |  |
| `GLOB_SELN_RLIM` | 외국계매도비중 | String | 8 | Y |  |
| `GLOB_SHNU_RLIM` | 외국계매수2비중 | String | 8 | Y |  |
| `SELN2_MBCR_ENG_NAME1` | 매도2영문회원사명1 | String | 20 | Y |  |
| `SELN2_MBCR_ENG_NAME2` | 매도2영문회원사명2 | String | 20 | Y |  |
| `SELN2_MBCR_ENG_NAME3` | 매도2영문회원사명3 | String | 20 | Y |  |
| `SELN2_MBCR_ENG_NAME4` | 매도2영문회원사명4 | String | 20 | Y |  |
| `SELN2_MBCR_ENG_NAME5` | 매도2영문회원사명5 | String | 20 | Y |  |
| `BYOV_MBCR_ENG_NAME1` | 매수영문회원사명1 | String | 20 | Y |  |
| `BYOV_MBCR_ENG_NAME2` | 매수영문회원사명2 | String | 20 | Y |  |
| `BYOV_MBCR_ENG_NAME3` | 매수영문회원사명3 | String | 20 | Y |  |
| `BYOV_MBCR_ENG_NAME4` | 매수영문회원사명4 | String | 20 | Y |  |
| `BYOV_MBCR_ENG_NAME5` | 매수영문회원사명5 | String | 20 | Y |  |

### 응답 예시

```json
# 연결 확인
{
    "header": {
        "tr_id": "H0STMBC0", 
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
0|H0STMBC0|001|005930^씨티그룹^미래에셋증권^모간서울^BNK증권^키움증권^미래
에셋증권^BNK증권^맥쿼리^NH투자증권^한국증권^903482^703873^484082^471203^246578^946273^571760^
343109^313536^311982^Y^N^Y^N^N^N^N^Y^N^N^00037^00005^00036^00086^00050^00005^00086^00035^0001
2^00003^19.06^14.85^10.21^9.94^5.20^19.96^12.06^7.24^6.61^6.58^14913^5054^7240^80000^3532^280
24^42986^0^5612^3043^1387564^681749^22153^0^-705815^29.27^14.38^^^^^^^^^^
```

