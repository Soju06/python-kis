# 채권지수 실시간체결가 [실시간-060]

> [장내채권] 실시간시세

채권지수 실시간체결가 API입니다.

[참고자료]
실시간시세(웹소켓) 파이썬 샘플코드는 한국투자증권 Github 참고 부탁드립니다.
https://github.com/koreainvestment/open-trading-api/blob/main/websocket/python/ws_domestic_overseas_all.py

실시간시세(웹소켓) API 사용방법에 대한 자세한 설명은 한국투자증권 Wikidocs 참고 부탁드립니다.
https://wikidocs.net/book/7847 (국내주식 업데이트 완료, 추후 해외주식·국내선물옵션 업데이트 예정)

채권 종목코드 마스터파일은 "포럼 > FAQ > 종목정보 다운로드(국내) > 장내채권 - 채권코드" 참고 부탁드립니다.

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
| **API ID** | `95690f51-c58b-47cb-850a-e0b70702e382` |
| **HTTP Method** | `POST` |
| **URL** | `/tryitout/H0BICNT0` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `ws://ops.koreainvestment.com:21000` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `H0BICNT0` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-05-10T10:23:47+09:00
- **최종 수정일**: 2025-04-30T13:26:42+09:00

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
| `tr_id` | 거래ID | String | 2 | Y | H0BICNT0 |
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
      "tr_id": "H0BICNT0",
      "tr_key": "KBPR01"
    }
  }
}
```

## 응답

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `NMIX_ID` | 지수ID | String | 6 | Y |  |
| `STND_DATE1` | 기준일자1 | String | 8 | Y |  |
| `TRNM_HOUR` | 전송시간 | String | 6 | Y |  |
| `TOTL_ERNN_NMIX_OPRC` | 총수익지수시가지수 | String | 1 | Y |  |
| `TOTL_ERNN_NMIX_HGPR` | 총수익지수최고가 | String | 1 | Y |  |
| `TOTL_ERNN_NMIX_LWPR` | 총수익지수최저가 | String | 1 | Y |  |
| `TOTL_ERNN_NMIX` | 총수익지수 | String | 1 | Y |  |
| `PRDY_TOTL_ERNN_NMIX` | 전일총수익지수 | String | 1 | Y |  |
| `TOTL_ERNN_NMIX_PRDY_VRSS` | 총수익지수전일대비 | String | 1 | Y |  |
| `TOTL_ERNN_NMIX_PRDY_VRSS_SIGN` | 총수익지수전일대비부호 | String | 1 | Y |  |
| `TOTL_ERNN_NMIX_PRDY_CTRT` | 총수익지수전일대비율 | String | 1 | Y |  |
| `CLEN_PRC_NMIX` | 순가격지수 | String | 1 | Y |  |
| `MRKT_PRC_NMIX` | 시장가격지수 | String | 1 | Y |  |
| `BOND_CALL_RNVS_NMIX` | Call재투자지수 | String | 1 | Y |  |
| `BOND_ZERO_RNVS_NMIX` | Zero재투자지수 | String | 1 | Y |  |
| `BOND_FUTS_THPR` | 선물이론가격 | String | 1 | Y |  |
| `BOND_AVRG_DRTN_VAL` | 평균듀레이션 | String | 1 | Y |  |
| `BOND_AVRG_CNVX_VAL` | 평균컨벡서티 | String | 1 | Y |  |
| `BOND_AVRG_YTM_VAL` | 평균YTM | String | 1 | Y |  |
| `BOND_AVRG_FRDL_YTM_VAL` | 평균선도YTM | String | 1 | Y |  |

### 응답 예시

```json
# 연결 확인
{
    "header": {
        "tr_id": "H0BICNT0", 
        "tr_key": "KBPR01", 
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
0|H0BICNT0|001|KBPR01^20240726^131500^163.55^163.56^163.52^163.54^163.53^0.00^2^0.00^98.92^99.50^163.54^161.83^0.00^9.45^181.22^3.07^0.00

# output - 정제 후
#### 채권지수 체결 ####
============================================
### [1 / 1]
지수ID         [KBPR01]
기준일자1        [20240726]
전송시간         [131500]
총수익지수시가지수    [163.55]
총수익지수최고가     [163.56]
총수익지수최저가     [163.52]
총수익지수        [163.54]
전일총수익지수      [163.53]
총수익지수전일대비    [0.00]
총수익지수전일대비부호  [2]
총수익지수전일대비율   [0.00]
순가격지수        [98.92]
시장가격지수       [99.50]
Call재투자지수    [163.54]
Zero재투자지수    [161.83]
선물이론가격       [0.00]
평균듀레이션       [9.45]
평균컨벡서티       [181.22]
평균YTM        [3.07]
평균선도YTM      [0.00]
```

