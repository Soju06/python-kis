# 선물옵션 실시간체결통보[실시간-012]

> [국내선물옵션] 실시간시세

[참고자료]

실시간시세(웹소켓) 파이썬 샘플코드는 한국투자증권 Github 참고 부탁드립니다.
https://github.com/koreainvestment/open-trading-api/blob/main/websocket/python/ws_domestic_overseas_all.py

실시간시세(웹소켓) API 사용방법에 대한 자세한 설명은 한국투자증권 Wikidocs 참고 부탁드립니다.
https://wikidocs.net/book/7847 (국내주식 업데이트 완료, 추후 해외주식·국내선물옵션 업데이트 예정)

[실시간-012] 지수선물옵션 실시간체결 통보

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `1d9a993b-18ff-40f6-891f-8a450e68f15a` |
| **HTTP Method** | `POST` |
| **URL** | `/tryitout/H0IFCNI0` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `ws://ops.koreainvestment.com:21000` |
| **모의 도메인** | `ws://ops.koreainvestment.com:31000` |
| **TR ID (실전)** | `H0IFCNI0` |
| **TR ID (모의)** | `H0IFCNI9` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2022-11-25
- **최종 수정일**: 2025-04-30

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `approval_key` | 웹소켓접속키 | String | 36 | Y | 실시간 (웹소켓) 접속키 발급 API(/oauth2/Approval)를 사용하여 발급받은 웹소켓 접속키 |
| `tr_type` | 등록/해제 | String | 1 | Y | 1: 등록, 2:해제 |
| `custtype` | 고객 타입 | String | 1 | Y | B : 법인 / P : 개인 |
| `content-type` | 컨텐츠타입 | String | 20 | Y | utf-8 |

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `tr_id` | 거래ID | String | 7 | Y | [실전투자] H0IFCNI0 : 실시간 선물옵션 체결통보  [모의투자] H0IFCNI9 : 실시간 선물옵션 체결통보 |
| `tr_key` | 코드 | String | 6 | Y | 예:101S12 |

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
      "tr_id": "H0IFCNI0",
      "tr_key": "HTS ID"
    }
  }
}
```

## 응답

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `CUST_ID` | 고객 ID | String | 16 | Y | '각 항목사이에는 구분자로 ^ 사용, 모든 데이터타입은 String으로 변환되어 push 처리됨' |
| `ACNT_NO` | 계좌번호 | String | 16 | Y |  |
| `ODER_NO` | 주문번호 | String | 1 | Y |  |
| `OODER_NO` | 원주문번호 | String | 8 | Y |  |
| `SELN_BYOV_CLS` | 매도매수구분 | String | 8 | Y | 01:매도, 02매수 |
| `RCTF_CLS` | 정정구분 | String | 8 | Y |  |
| `ODER_KIND2` | 주문종류2 | String | 8 | Y | L: 주문접수통보, 0: 체결통보 |
| `STCK_SHRN_ISCD` | 주식 단축 종목코드 | String | 8 | Y |  |
| `CNTG_QTY` | 체결 수량 | String | 8 | Y |  |
| `CNTG_UNPR` | 체결단가 | String | 8 | Y |  |
| `STCK_CNTG_HOUR` | 주식 체결 시간 | String | 8 | Y |  |
| `RFUS_YN` | 거부여부 | String | 8 | Y |  |
| `CNTG_YN` | 체결여부 | String | 8 | Y | 1: 주문,정정,취소,거부 통보, 2 체결 |
| `ACPT_YN` | 접수여부 | String | 8 | Y | 1:주문접수, 2:확인, 3, 취소 |
| `BRNC_NO` | 지점번호 | String | 8 | Y |  |
| `ODER_QTY` | 주문수량 | String | 8 | Y |  |
| `ACNT_NAME` | 계좌명 | String | 8 | Y |  |
| `CNTG_ISNM` | 체결종목명 | String | 8 | Y |  |
| `ODER_COND` | 주문조건 | String | 8 | Y |  |
| `ORD_GRP` | 주문그룹ID | String | 8 | Y |  |
| `ORD_GRPSEQ` | 주문그룹SEQ | String | 8 | Y |  |
| `ORDER_PRC` | 주문가격 | String | 8 | Y |  |

### 응답 예시

```json
# output - 등록 성공 시
{
    "header": {
        "tr_id": "H0IFCNI0", 
        "tr_key": "HTS ID", 
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

# output (복호화 전) 
1|H0IFCNI0|001|vebQjGIHMgFhxfNfvebQjGIHMgFhxfNfvebQjGIHMgFhxfNfvebQj...hxfNf

# output (복호화 후)
#### 지수선물옵션 체결 통보 ####
고객ID  [abcd1234]
계좌번호  [1234567803]
주문번호  [0000001666]
원주문번호  []
매도매수구분  [02]
정정구분  [0]
주문종류  [0]
단축종목코드  [111V06]
체결수량  [0000000002]
체결단가  [007840000]
체결시간  [095835]
거부여부  [0]
체결여부  [2]
접수여부  [2]
지점번호  [00950]
주문수량  [000000000]
계좌명  [김한국]
체결종목명  [삼성전자   F 2]
주문조건  []
주문그룹ID  []
주문그룹SEQ  []
주문가격  [000000000]
```

