# 주식선물 실시간예상체결 [실시간-031]

> [국내선물옵션] 실시간시세

[참고자료]

실시간시세(웹소켓) 파이썬 샘플코드는 한국투자증권 Github 참고 부탁드립니다.
https://github.com/koreainvestment/open-trading-api/blob/main/websocket/python/ws_domestic_overseas_all.py

실시간시세(웹소켓) API 사용방법에 대한 자세한 설명은 한국투자증권 Wikidocs 참고 부탁드립니다.
https://wikidocs.net/book/7847 (국내주식 업데이트 완료, 추후 해외주식·국내선물옵션 업데이트 예정)


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `6774932d-1c2d-44cb-b8fb-44b39bd5eed5` |
| **HTTP Method** | `POST` |
| **URL** | `/tryitout/H0ZFANC0` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `ws://ops.koreainvestment.com:21000` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `H0ZFANC0` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-05-10T10:12:22+09:00
- **최종 수정일**: 2025-04-30T13:30:32+09:00

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
| `tr_id` | 거래ID | String | 2 | Y | H0ZFANC0 |
| `tr_key` | 구분값 | String | 12 | Y | 주식선물 종목코드 |

## 응답

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `FUTS_SHRN_ISCD` | 선물단축종목코드 | String | 9 | Y |  |
| `BSOP_HOUR` | 영업시간 | String | 6 | Y |  |
| `ANTC_CNPR` | 예상체결가 | String | 8 | Y |  |
| `ANTC_CNTG_VRSS` | 예상체결대비 | String | 8 | Y |  |
| `ANTC_CNTG_VRSS_SIGN` | 예상체결대비부호 | String | 1 | Y |  |
| `ANTC_CNTG_PRDY_CTRT` | 예상체결전일대비율 | String | 8 | Y |  |
| `ANTC_MKOP_CLS_CODE` | 예상장운영구분코드 | String | 3 | Y |  |
| `ANTC_CNQN` | 예상체결수량 | String | 8 | Y |  |

