# 일반채권 실시간체결가 [실시간-052]

> [장내채권] 실시간시세

일반채권 실시간체결가 API입니다.

[참고자료]
실시간시세(웹소켓) 파이썬 샘플코드는 한국투자증권 Github 참고 부탁드립니다.
https://github.com/koreainvestment/open-trading-api/blob/main/websocket/python/ws_domestic_overseas_all.py

실시간시세(웹소켓) API 사용방법에 대한 자세한 설명은 한국투자증권 Wikidocs 참고 부탁드립니다.
https://wikidocs.net/book/7847 (국내주식 업데이트 완료, 추후 해외주식·국내선물옵션 업데이트 예정)

채권 종목코드 마스터파일은 "포럼 >  FAQ > 종목정보 다운로드(국내) > 장내채권 - 채권코드" 참고 부탁드립니다.

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
| **API ID** | `a5e03bf1-e7ef-4587-9d13-159376b444b8` |
| **HTTP Method** | `POST` |
| **URL** | `/tryitout/H0BJCNT0` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `ws://ops.koreainvestment.com:21000` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `H0BJCNT0` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-05-10T10:22:40+09:00
- **최종 수정일**: 2025-04-30T13:26:48+09:00

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
| `tr_id` | 거래ID | String | 2 | Y | H0BJCNT0 |
| `tr_key` | 구분값 | String | 12 | Y | 채권 종목코드 (ex. KR103502GA34) |

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
      "tr_id": "H0BJCNT0",
      "tr_key": "KR103502GD31"
    }
  }
}
```

## 응답

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `STND_ISCD` | 표준종목코드 | String | 12 | Y |  |
| `BOND_ISNM` | 채권종목명 | String | 80 | Y |  |
| `STCK_CNTG_HOUR` | 주식체결시간 | String | 6 | Y |  |
| `PRDY_VRSS_SIGN` | 전일대비부호 | String | 1 | Y |  |
| `PRDY_VRSS` | 전일대비 | String | 8 | Y |  |
| `PRDY_CTRT` | 전일대비율 | String | 8 | Y |  |
| `STCK_PRPR` | 현재가 | String | 8 | Y |  |
| `CNTG_VOL` | 체결거래량 | String | 8 | Y |  |
| `STCK_OPRC` | 시가 | String | 8 | Y |  |
| `STCK_HGPR` | 고가 | String | 8 | Y |  |
| `STCK_LWPR` | 저가 | String | 8 | Y |  |
| `STCK_PRDY_CLPR` | 전일종가 | String | 8 | Y |  |
| `BOND_CNTG_ERT` | 현재수익률 | String | 10 | Y |  |
| `OPRC_ERT` | 시가수익률 | String | 10 | Y |  |
| `HGPR_ERT` | 고가수익률 | String | 10 | Y |  |
| `LWPR_ERT` | 저가수익률 | String | 10 | Y |  |
| `ACML_VOL` | 누적거래량 | String | 8 | Y |  |
| `PRDY_VOL` | 전일거래량 | String | 8 | Y |  |
| `CNTG_TYPE_CLS_CODE` | 체결유형코드 | String | 1 | Y |  |

### 응답 예시

```json
# 연결 확인
{
    "header": {
        "tr_id": "H0BJCNT0", 
        "tr_key": "KR103502GD31", 
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

# output - 정제 전
0|H0BJCNT0|001|KR103502GD31^국고03250-5303(23-2)^131743^2^5.00^0.05^10575.00^1^10525.00^10578.00^10525.00^0.00^3.012^3.037^3.010^3.037^659
4124^9874082^2

# output - 정제 후
#### 장내채권 체결 ####
============================================
### [1 / 1]
표준종목코드       [KR103502GD31]
채권종목명        [국고03250-5303(23-2)]
주식체결시간       [131743]
전일대비부호       [2]
전일대비         [5.00]
전일대비율        [0.05]
현재가          [10575.00]
체결거래량        [1]
시가           [10525.00]
고가           [10578.00]
저가           [10525.00]
전일종가         [0.00]
현재수익률        [3.012]
시가수익률        [3.037]
고가수익률        [3.010]
저가수익률        [3.037]
누적거래량        [6594124]
전일거래량        [9874082]
체결유형코드       [2]
```

