# 일반채권 실시간호가 [실시간-053]

> [장내채권] 실시간시세

일반채권 실시간호가 API입니다.

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
| **API ID** | `242ea47d-150e-4c8f-88a1-50fba4b822c5` |
| **HTTP Method** | `POST` |
| **URL** | `/tryitout/H0BJASP0` |
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
- **생성일**: 2024-05-10T10:23:16+09:00
- **최종 수정일**: 2025-04-30T13:26:46+09:00

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `approval_key` | 웹소켓 접속키 | String | 36 | Y | 실시간 (웹소켓) 접속키 발급 API(/oauth2/Approval)를 사용하여 발급받은 웹소켓 접속키 |
| `custtype` | 고객 타입 | String | 1 | Y | B : 법인 / P : 개인 |
| `custtype` | 등록/해제 | String | 1 | Y | 1: 등록, 2:해제 |
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
      "tr_id": "H0BJASP0",
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
| `STCK_CNTG_HOUR` | 주식체결시간 | String | 6 | Y |  |
| `ASKP_ERT1` | 매도호가수익률 | String | 10 | Y |  |
| `BIDP_ERT1` | 매수호가수익률1 | String | 10 | Y |  |
| `ASKP1` | 매도호가1 | String | 8 | Y |  |
| `BIDP1` | 매수호가1 | String | 8 | Y |  |
| `ASKP_RSQN1` | 매도호가잔량1 | String | 8 | Y |  |
| `BIDP_RSQN1` | 매수호가잔량1 | String | 8 | Y |  |
| `ASKP_ERT2` | 매도호가수익률2 | String | 10 | Y |  |
| `BIDP_ERT2` | 매수호가수익률2 | String | 10 | Y |  |
| `ASKP2` | 매도호가2 | String | 8 | Y |  |
| `BIDP2` | 매수호가2 | String | 8 | Y |  |
| `ASKP_RSQN2` | 매도호가잔량2 | String | 8 | Y |  |
| `BIDP_RSQN2` | 매수호가잔량2 | String | 8 | Y |  |
| `ASKP_ERT3` | 매도호가수익률3 | String | 10 | Y |  |
| `BIDP_ERT3` | 매수호가수익률3 | String | 10 | Y |  |
| `ASKP3` | 매도호가3 | String | 8 | Y |  |
| `BIDP3` | 매수호가3 | String | 8 | Y |  |
| `ASKP_RSQN3` | 매도호가잔량3 | String | 8 | Y |  |
| `BIDP_RSQN3` | 매수호가잔량3 | String | 8 | Y |  |
| `ASKP_ERT4` | 매도호가수익률4 | String | 10 | Y |  |
| `BIDP_ERT4` | 매수호가수익률4 | String | 10 | Y |  |
| `ASKP4` | 매도호가4 | String | 8 | Y |  |
| `BIDP4` | 매수호가4 | String | 8 | Y |  |
| `ASKP_RSQN4` | 매도호가잔량4 | String | 8 | Y |  |
| `BIDP_RSQN4` | 매수호가잔량4 | String | 8 | Y |  |
| `ASKP_ERT5` | 매도호가수익률5 | String | 10 | Y |  |
| `BIDP_ERT5` | 매수호가수익률5 | String | 10 | Y |  |
| `ASKP5` | 매도호가5 | String | 8 | Y |  |
| `BIDP5` | 매수호가5 | String | 8 | Y |  |
| `ASKP_RSQN52` | 매도호가잔량5 | String | 8 | Y |  |
| `BIDP_RSQN53` | 매수호가잔량5 | String | 8 | Y |  |
| `TOTAL_ASKP_RSQN` | 총매도호가잔량 | String | 8 | Y |  |
| `TOTAL_BIDP_RSQN` | 총매수호가잔량 | String | 8 | Y |  |

### 응답 예시

```json
# 연결 확인
{
    "header": {
        "tr_id": "H0BJASP0", 
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
0|H0BJASP0|001|KR103502GD31^131743^3.012^3.020^10575.00^10560.00^416090^323813^3.011^3.022^10576.00^10556.00^405284^57^3.010^3.022^10578.0
0^10555.00^177098^500000^3.009^3.024^10580.00^10551.00^97637^363079^3.001^3.025^10597.00^10550.00^80000^379920^1698609^4112382

# output - 정제 후
#### 장내채권 호가 ####
채권종목코드  [KR103502GD31]
영업시간  [131743]
====================================
채권매도호가1   [10575.00],    매도호가수익률1  [3.012],    매도호가잔량1      [416090]
채권매도호가2   [10576.00],    매도호가수익률2  [3.011],    매도호가잔량2      [405284]
채권매도호가3   [10578.00],    매도호가수익률3  [3.010],    매도호가잔량3      [177098]
채권매도호가4   [10580.00],    매도호가수익률4  [3.009],    매도호가잔량4      [97637]
채권매도호가5   [10597.00],    매도호가수익률5  [3.001],    매도호가잔량5      [80000]
채권매수호가1   [10560.00],    매수호가수익률1  [3.020],    매수호가잔량1      [323813]
채권매수호가2   [10556.00],    매수호가수익률2  [3.022],    매수호가잔량2      [57]
채권매수호가3   [10555.00],    매수호가수익률3  [3.022],    매수호가잔량3      [500000]
채권매수호가4   [10551.00],   매수호가수익률4   [3.024],    매수호가잔량4      [363079]
채권매수호가5   [10550.00],    매수호가수익률5  [3.025],    매수호가잔량5      [379920]
====================================
총매도호가잔량  [1698609]
총매수호가잔량  [4112382]
```

