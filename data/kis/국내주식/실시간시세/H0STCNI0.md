# 국내주식 실시간체결통보 [실시간-005]

> [국내주식] 실시간시세

국내주식 실시간 체결통보 수신 시에 (1) 주문·정정·취소·거부 접수 통보 와 (2) 체결 통보 가 모두 수신됩니다.
(14번째 값(CNTG_YN;체결여부)가 2이면 체결통보, 1이면 주문·정정·취소·거부 접수 통보입니다.)

※ 모의투자는 H0STCNI9 로 변경하여 사용합니다.

[참고자료]
실시간시세(웹소켓) 파이썬 샘플코드는 한국투자증권 Github 참고 부탁드립니다.
https://github.com/koreainvestment/open-trading-api/blob/main/websocket/python/ws_domestic_overseas_all.py

실시간시세(웹소켓) API 사용방법에 대한 자세한 설명은 한국투자증권 Wikidocs 참고 부탁드립니다.
https://wikidocs.net/book/7847 (국내주식 업데이트 완료, 추후 해외주식·국내선물옵션 업데이트 예정)

[호출 데이터]
헤더와 바디 값을 합쳐 JSON 형태로 전송합니다.

[응답 데이터]
1. 정상 등록 여부 (JSON)
- JSON["body"]["msg1"] - 정상 응답 시, SUBSCRIBE SUCCESS
- JSON["body"]["output"]["iv"] - 실시간 결과 복호화에 필요한 AES256 IV (Initialize Vector)
- JSON["body"]["output"]["key"] - 실시간 결과 복호화에 필요한 AES256 Key

2. 실시간 결과 응답 ( | 로 구분되는 값)
- 암호화 유무 : 0 암호화 되지 않은 데이터 / 1 암호화된 데이터
- TR_ID : 등록한 tr_id
- 데이터 건수 : (ex. 001 데이터 건수를 참조하여 활용)
- 응답 데이터 : 아래 response 데이터 참조 ( ^로 구분됨)

체결 통보 응답 결과는 암호화되어 출력됩니다. AES256 KEY IV를 활용해 복호화하여 활용하세요. 자세한 예제는 [도구>wikidocs]에 준비되어 있습니다.

[실시간-005] 국내주식 실시간체결통보

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `1e3c056d-1b42-461c-b8fb-631bb48e1ee2` |
| **HTTP Method** | `POST` |
| **URL** | `/tryitout/H0STCNI0` |
| **Content-Type** | `test/plain` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | ` ws://ops.koreainvestment.com:21000` |
| **모의 도메인** | ` ws://ops.koreainvestment.com:31000` |
| **TR ID (실전)** | `H0STCNI0` |
| **TR ID (모의)** | `H0STCNI9` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2021-12-15T13:16:12+09:00
- **최종 수정일**: 2025-04-30T13:10:28+09:00

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `approval_key` | 웹소켓 접속키 | String | 286 | N | 실시간 (웹소켓) 접속키 발급 API(/oauth2/Approval)를 사용하여 발급받은 웹소켓 접속키 |
| `custtype` | 고객 타입 | String | 1 | Y | B : 법인  P : 개인 |
| `tr_type` | 거래타입 | String | 1 | N | 1: 등록 2 : 해제 |
| `content-type` | 컨텐츠타입 | String | 1 | N | utf-8 |

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `tr_id` | 거래ID | String | 2 | Y | '[실전/모의투자] H0STCNI0 : 국내주식 실시간체결통보 H0STCNI9 : 모의투자 실시간 체결통보 |
| `tr_key` | 구분값 | String | 12 | Y | HTS ID |

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
      "tr_id": "H0STCNI0",
      "tr_key": "HTS ID"
    }
  }
}
```

## 응답

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `CUST_ID` | 고객 ID | String | 8 | Y |  |
| `ACNT_NO` | 계좌번호 | String | 10 | Y |  |
| `ODER_NO` | 주문번호 | String | 10 | Y |  |
| `OODER_NO` | 원주문번호 | String | 10 | Y |  |
| `SELN_BYOV_CLS` | 매도매수구분 | String | 2 | Y | 01 : 매도  02 : 매수 |
| `RCTF_CLS` | 정정구분 | String | 1 | Y | 0:정상  1:정정  2:취소 |
| `ODER_KIND` | 주문종류 | String | 2 | Y | [KRX] 00 : 지정가 01 : 시장가 02 : 조건부지정가 03 : 최유리지정가 04 : 최우선지정가 05 : 장전 시간외 06 : 장후 시간외 07 : 시간외 단일가 11 : IOC지정가 (즉시체결,잔량취소) 12 : FOK지정가 (즉시체결,전량취소) 13 : IOC시장가 (즉시체결,잔량취소) 14 : FOK시장가 (즉시체결,전량취소) 15 : IOC최유리 (즉시체결,잔량취소) 16 : FOK최유리 (즉시체결,전량취소) 21 : 중간가 22 : 스톱지정가 23 : 중간가IOC 24 : 중간가FOK  [NXT] 00 : 지정가 03 : 최유리지정가 04 : 최우선지정가 11 : IOC지정가 (즉시체결,잔량취소) 12 : FOK지정가 (즉시체결,전량취소) 13 : IOC시장가 (즉시체결,잔량취소) 14 : FOK시장가 (즉시체결,전량취소) 15 : IOC최유리 (즉시체결,잔량취소) 16 : FOK최유리 (즉시체결,전량취소) 21 : 중간가 22 : 스톱지정가 23 : 중간가IOC 24 : 중간가FOK  [SOR] 00 : 지정가 01 : 시장가 03 : 최유리지정가 04 : 최우선지정가 11 : IOC지정가 (즉시체결,잔량취소) 12 : FOK지정가 (즉시체결,전량취소) 13 : IOC시장가 (즉시체결,잔량취소) 14 : FOK시장가 (즉시체결,전량취소) 15 : IOC최유리 (즉시체결,잔량취소) 16 : FOK최유리 (즉시체결,전량취소) |
| `ODER_COND` | 주문조건 | String | 1 | Y | 0:없음 1:IOC  2:FOK |
| `STCK_SHRN_ISCD` | 주식 단축 종목코드 | String | 9 | Y |  |
| `CNTG_QTY` | 체결 수량 | String | 10 | Y |  |
| `CNTG_UNPR` | 체결단가 | String | 9 | Y |  |
| `STCK_CNTG_HOUR` | 주식 체결 시간 | String | 6 | Y |  |
| `RFUS_YN` | 거부여부 | String | 1 | Y | 0 : 승인  1 : 거부 |
| `CNTG_YN` | 체결여부 | String | 1 | Y | 1 : 주문,정정,취소,거부 2 : 체결 |
| `ACPT_YN` | 접수여부 | String | 1 | Y | 1 : 주문접수 2 : 확인 3 : 취소(FOK/IOC) |
| `BRNC_NO` | 지점번호 | String | 5 | Y |  |
| `ODER_QTY` | 주문수량 | String | 9 | Y |  |
| `ACNT_NAME` | 계좌명 | String | 12 | Y |  |
| `ORD_COND_PRC` | 호가조건가격 | String | 9 | Y | 스톱지정가 시 표시 |
| `ORD_EXG_GB` | 주문거래소 구분 | String | 1 | Y | 1:KRX, 2:NXT, 3:SOR-KRX, 4:SOR-NXT |
| `POPUP_YN` | 실시간체결창 표시여부 | String | 1 | Y | Y/N |
| `FILLER` | 필러 | String | 3 | Y |  |
| `CRDT_CLS` | 신용구분 | String | 2 | Y |  |
| `CRDT_LOAN_DATE` | 신용대출일자 | String | 8 | Y |  |
| `CNTG_ISNM40` | 체결종목명 | String | 40 | Y |  |
| `ODER_PRC` | 주문가격 | String | 9 | Y |  |

### 응답 예시

```json
{
    "header": {
        "tr_id": "H0STCNI0", 
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

# output - 주문·정정·취소·거부 접수 통보
HTS ID^1234567801^0000002891^^02^0^01^0^136480^0000000001^000000000^094941^0
^1^1^06010^000000001^김한투^하림^10^^하림^

# output - 체결 통보
HTS ID^1234567801^0000002891^^02^0^00^0^136480^0000000001^000003190^094941^0
^2^2^06010^000000001^김한투^하림^10^^하림^000000000
```

