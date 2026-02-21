# 국내주식 실시간프로그램매매 (통합)

> [국내주식] 실시간시세



## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `416ebbf1-64b8-4d1e-be85-8fede035dec6` |
| **HTTP Method** | `POST` |
| **URL** | `/tryitout/H0UNPGM0` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `ws://ops.koreainvestment.com:21000` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `H0UNPGM0` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2025-02-28T13:31:30+09:00
- **최종 수정일**: 2025-04-30T13:16:27+09:00

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `approval_key` | 웹소켓 접속키 | String | 286 | N | 실시간 (웹소켓) 접속키 발급 API(/oauth2/Approval)를 사용하여 발급받은 웹소켓 접속키 |
| `custtype` | 고객타입 | String | 1 | N | 'B : 법인 P : 개인' |
| `tr_type` | 거래타입 | String | 1 | N | '1 : 등록 2 : 해제' |
| `content-type` | 컨텐츠타입 | String | 1 | N | '	utf-8' |

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `tr_id` | 거래ID | String | 2 | Y | H0UNPGM0 : 실시간 주식종목프로그램매매 통합 |
| `tr_key` | 구분값 | String | 12 | Y | 종목코드 (ex 005930 삼성전자) |

## 응답

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `MKSC_SHRN_ISCD` | 유가증권 단축 종목코드 | String | 9 | Y |  |
| `STCK_CNTG_HOUR` | 주식 체결 시간 | String | 6 | Y |  |
| `SELN_CNQN` | 매도 체결량 | String | 8 | Y |  |
| `SELN_TR_PBMN` | 매도 거래 대금 | String | 8 | Y |  |
| `SHNU_CNQN` | 매수2 체결량 | String | 8 | Y |  |
| `SHNU_TR_PBMN` | 매수2 거래 대금 | String | 8 | Y |  |
| `NTBY_CNQN` | 순매수 체결량 | String | 8 | Y |  |
| `NTBY_TR_PBMN` | 순매수 거래 대금 | String | 8 | Y |  |
| `SELN_RSQN` | 매도호가잔량 | String | 8 | Y |  |
| `SHNU_RSQN` | 매수호가잔량 | String | 8 | Y |  |
| `WHOL_NTBY_QTY` | 전체순매수호가잔량 | String | 8 | Y |  |

