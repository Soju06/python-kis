# 해외주식 실시간체결통보[실시간-009]

> [해외주식] 실시간시세

[참고자료]

실시간시세(웹소켓) 파이썬 샘플코드는 한국투자증권 Github 참고 부탁드립니다.
https://github.com/koreainvestment/open-trading-api/blob/main/websocket/python/ws_domestic_overseas_all.py

실시간시세(웹소켓) API 사용방법에 대한 자세한 설명은 한국투자증권 Wikidocs 참고 부탁드립니다.
https://wikidocs.net/book/7847 (국내주식 업데이트 완료, 추후 해외주식·국내선물옵션 업데이트 예정)


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `fef3c007-4a03-4b3b-9d08-310b88912877` |
| **HTTP Method** | `POST` |
| **URL** | `/tryitout/H0GSCNI0` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `ws://ops.koreainvestment.com:21000` |
| **모의 도메인** | `ws://ops.koreainvestment.com:31000` |
| **TR ID (실전)** | `H0GSCNI0` |
| **TR ID (모의)** | `H0GSCNI9` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2022-09-05T15:26:46+09:00
- **최종 수정일**: 2025-05-23T18:40:01+09:00

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `approval_key` | 웹소켓 접속키 | String | 286 | Y | 실시간 (웹소켓) 접속키 발급 API(/oauth2/Approval)를 사용하여 발급받은 웹소켓 접속키 |
| `tr_type` | 등록/해제 | String | 1 | Y | 1: 등록, 2:해제 |
| `custtype` | 고객 타입 | String | 1 | Y | B : 법인 / P : 개인 |
| `content-type` | 컨텐츠타입 | String | 20 | Y | utf-8 |

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `tr_id` | 거래ID | String | 7 | Y | [실전투자] H0GSCNI0 : 실시간 해외주식 체결통보  [모의투자] H0GSCNI9 : 실시간 해외주식 체결통보 |
| `tr_key` | HTSID | String | 8 | Y | HTSID |

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
      "tr_id": "H0GSCNI0",
      "tr_key": "HTS ID"
    }
  }
}
```

## 응답

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `CUST_ID` | 고객 ID | String | 8 | Y | '각 항목사이에는 구분자로 ^ 사용, 모든 데이터타입은 String으로 변환되어 push 처리됨' |
| `ACNT_NO` | 계좌번호 | String | 10 | Y |  |
| `ODER_NO` | 주문번호 | String | 10 | Y |  |
| `OODER_NO` | 원주문번호 | String | 10 | Y |  |
| `SELN_BYOV_CLS` | 매도매수구분 | String | 2 | Y | 01:매도 02:매수 03:전매도 04:환매수 |
| `RCTF_CLS` | 정정구분 | String | 1 | Y | 0:정상 1:정정 2:취소 |
| `ODER_KIND2` | 주문종류2 | String | 1 | Y | 1:시장가 2:지정자 6:단주시장가 7:단주지정가 A:MOO B:LOO C:MOC D:LOC |
| `STCK_SHRN_ISCD` | 주식 단축 종목코드 | String | 9 | Y |  |
| `CNTG_QTY` | 체결수량 | String | 10 | Y | - 주문통보의 경우 해당 위치에 주문수량이 출력 - 체결통보인 경우 해당 위치에 체결수량이 출력 |
| `CNTG_UNPR` | 체결단가 | String | 9 | Y | ※ 주문통보 시에는 주문단가가, 체결통보 시에는 체결단가가 수신 됩니다. ※ 체결단가의 경우, 국가에 따라 소수점 생략 위치가 상이합니다. 미국 4 일본 1 중국 3 홍콩 3 베트남 0 EX) 미국 AAPL(현재가 : 148.0100)의 경우 001480100으로 체결단가가 오는데,  4번째 자리에 소수점을 찍어 148.01로 해석하시면 됩니다. |
| `STCK_CNTG_HOUR` | 주식 체결 시간 | String | 6 | Y | 특정 거래소의 체결시간 데이터는 수신되지 않습니다.  체결시간 데이터가 필요할 경우, 체결통보 데이터 수신 시 타임스탬프를 찍는 것으로 대체하시길 바랍니다. |
| `RFUS_YN` | 거부여부 | String | 1 | Y | 0:정상 1:거부 |
| `CNTG_YN` | 체결여부 | String | 1 | Y | 1:주문,정정,취소,거부 2:체결 |
| `ACPT_YN` | 접수여부 | String | 1 | Y | 1:주문접수 2:확인 3:취소(FOK/IOC) |
| `BRNC_NO` | 지점번호 | String | 5 | Y |  |
| `ODER_QTY` | 주문 수량 | String | 9 | Y | - 주문통보인 경우 해당 위치 미출력 (주문통보의 주문수량은 CNTG_QTY 위치에 출력) - 체결통보인 경우 해당 위치에 주문수량이 출력 |
| `ACNT_NAME` | 계좌명 | String | 12 | Y |  |
| `CNTG_ISNM` | 체결종목명 | String | 14 | Y |  |
| `ODER_COND` | 해외종목구분 | String | 1 | Y | 4:홍콩(HKD) 5:상해B(USD)  6:NASDAQ 7:NYSE 8:AMEX 9:OTCB C:홍콩(CNY) A:상해A(CNY) B:심천B(HKD) D:도쿄 E:하노이 F:호치민 |
| `DEBT_GB` | 담보유형코드 | String | 2 | Y | 10:현금 15:해외주식담보대출 |
| `DEBT_DATE` | 담보대출일자 | String | 8 | Y | 대출일(YYYYMMDD) |
| `START_TM` | 분할매수/매도 시작시간 | String | 6 | Y | HHMMSS |
| `END_TM` | 분할매수/매도 종료시간 | String | 6 | Y | HHMMSS |
| `TM_DIV_TP` | 시간분할타입유형 | String | 2 | Y | 00 시간직접설정, 02 : 정규장까지 |
| `CNTG_UNPR12` | 체결단가12 | String | 12 | Y |  |

### 응답 예시

```json
# output - 등록 성공 시
{
    "header": {
        "tr_id": "H0GSCNI0", 
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
1|H0GSCNI0|001|vebQjGIHMgFhxfNfvebQjGIHMgFhxfNfvebQjGIHMgFhxfNfvebQj...hxfNf

# output (복호화 후)
#### 해외주식 주문·정정·취소·거부 접수 통보 ####
고객 ID  [abcd1234]
계좌번호  [12345678]
주문번호  [3567]
원주문번호  []
매도매수구분  [02]
정정구분  [0]
주문종류2  [1]
단축종목코드  [7203]
주문수량  [0000000100]
체결단가  [000032200]
체결시간  []
거부여부  [0]
체결여부  [1]
접수여부  [1]
지점번호  []
체결수량  []
계좌명  [******]
체결종목명  [도요타자동차]
해외종목구분  [D]
담보유형코드  [10]
담보대출일자  []
분할매수매도시작시간  []
분할매수매도종료시간  []
시간분할타입유형  []
```

