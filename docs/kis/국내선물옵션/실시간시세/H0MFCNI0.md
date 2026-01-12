# KRX야간선물 실시간체결통보 [실시간-066]

> [국내선물옵션] 실시간시세

[참고자료]

실시간시세(웹소켓) 파이썬 샘플코드는 한국투자증권 Github 참고 부탁드립니다.
https://github.com/koreainvestment/open-trading-api/blob/main/websocket/python/ws_domestic_overseas_all.py

실시간시세(웹소켓) API 사용방법에 대한 자세한 설명은 한국투자증권 Wikidocs 참고 부탁드립니다.
https://wikidocs.net/book/7847 (국내주식 업데이트 완료, 추후 해외주식·국내선물옵션 업데이트 예정)

종목코드 마스터파일 파이썬 정제코드는 한국투자증권 Github 참고 부탁드립니다.
https://github.com/koreainvestment/open-trading-api/tree/main/stocks_info

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `70845e60-37a9-4849-a563-bc613b419599` |
| **HTTP Method** | `POST` |
| **URL** | `/tryitout/H0MFCNI0` |
| **Content-Type** | `` |
| **요청 포맷** | `` |
| **실전 도메인** | `ws://ops.koreainvestment.com:21000` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID** | `모의투자 미지원`, `H0MFCNI0` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-05-24
- **최종 수정일**: 2025-06-30

## 요청 (Request)

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
| `tr_id` | 거래ID | String | 2 | Y | H0MFCNI0 |
| `tr_key` | 구분값 | String | 12 | Y | HTS ID |

## 응답 (Response)

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `CUST_ID` | 고객 ID | String | 8 | Y |  |
| `ACNT_NO` | 계좌번호 | String | 10 | Y |  |
| `ODER_NO` | 주문번호 | String | 10 | Y |  |
| `OODER_NO` | 원주문번호 | String | 10 | Y |  |
| `SELN_BYOV_CLS` | 매도매수구분 | String | 2 | Y |  |
| `RCTF_CLS` | 정정구분 | String | 1 | Y |  |
| `ODER_KIND2` | 주문종류2 | String | 1 | Y |  |
| `STCK_SHRN_ISCD` | 주식 단축 종목코드 | String | 9 | Y |  |
| `CNTG_QTY` | 체결 수량 | String | 10 | Y |  |
| `CNTG_UNPR` | 체결단가 | String | 9 | Y |  |
| `STCK_CNTG_HOUR` | 주식 체결 시간 | String | 6 | Y |  |
| `RFUS_YN` | 거부여부 | String | 1 | Y |  |
| `CNTG_YN` | 체결여부 | String | 1 | Y |  |
| `ACPT_YN` | 접수여부 | String | 1 | Y |  |
| `BRNC_NO` | 지점번호 | String | 5 | Y |  |
| `ODER_QTY` | 주문수량 | String | 9 | Y |  |
| `ACNT_NAME` | 계좌명 | String | 12 | Y |  |
| `CNTG_ISNM` | 체결종목명 | String | 14 | Y |  |
| `ODER_COND` | 주문조건 | String | 1 | Y |  |
