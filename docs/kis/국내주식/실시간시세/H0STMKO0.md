# 국내주식 장운영정보 (KRX) [실시간-049]

> [국내주식] 실시간시세

국내주식 장운영정보 연결 시, 연결종목의 VI 발동 시와 VI 해제 시에 데이터 수신됩니다. 

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
| **API ID** | `6500be39-a989-4c30-abbb-197bd3890eb8` |
| **HTTP Method** | `POST` |
| **URL** | `/tryitout/H0STMKO0` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `ws://ops.koreainvestment.com:21000` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `H0STMKO0` |
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
| `tr_id` | 거래ID | String | 7 | Y | H0STMKO0 |
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
      "tr_id": "H0STMKO0",
      "tr_key": "396300"
    }
  }
}
```

## 응답

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `MKSC_SHRN_ISCD` | 유가증권단축종목코드 | String | 9 | Y | '각 항목사이에는 구분자로 ^ 사용, 모든 데이터타입은 String으로 변환되어 push 처리됨' |
| `TRHT_YN` | 거래정지여부 | String | 1 | Y |  |
| `TR_SUSP_REAS_CNTT` | 거래정지사유내용 | String | 100 | Y |  |
| `MKOP_CLS_CODE` | 장운영구분코드 | String | 3 | Y | 110        장전 동시호가 개시                       112        장개시                                   121 ... |
| `ANTC_MKOP_CLS_CODE` | 예상장운영구분코드 | String | 3 | Y | 112    장전예상종료  121   장후예상시작 129   장후예상종료 311  장전예상시작 |
| `MRKT_TRTM_CLS_CODE` | 임의연장구분코드 | String | 1 | Y | 1  시초동시 임의종료 지정 2  시초동시 임의종료 해제  3  마감동시 임의종료 지정  4  마감동시 임의종료 해제   5  시간외단일가임의종료 지정  6  시간외단일가임의... |
| `DIVI_APP_CLS_CODE` | 동시호가배분처리구분코드 | String | 2 | Y | divi_app_cls_code[0]  1: 배분개시 2: 배분해제 divi_app_cls_code[1] 1: 매수상한 2: 매수하한 3: 매도상한 4: 매도하한 |
| `ISCD_STAT_CLS_CODE` | 종목상태구분코드 | String | 2 | Y | 51  관리종목 지정 종목 52  시장경고 구분이 '투자위험'인 종목 53  시장경고 구분이 '투자경고'인 종목 54  시장경고 구분이 '투자주의'인 종목 55  당사 신용가... |
| `VI_CLS_CODE` | VI적용구분코드 | String | 1 | Y | Y  VI적용된 종목 N  VI적용되지 않은 종목 |
| `OVTM_VI_CLS_CODE` | 시간외단일가VI적용구분코드 | String | 1 | Y | Y 시간외단일가VI 적용된 종목 N 시간외단일가VI 적용되지 않은 종목 |
| `EXCH_CLS_CODE` | 거래소구분코드 | String | 1 | Y |  |

### 응답 예시

```json
# 연결 확인
{
    "header": {
        "tr_id": "H0STMKO0", 
        "tr_key": "396300", 
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
0|H0STMKO0|001|396300^N^(null)^^311^^^55^N^N
```

