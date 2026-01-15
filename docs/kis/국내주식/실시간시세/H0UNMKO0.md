# 국내주식 장운영정보 (통합)

> [국내주식] 실시간시세

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `16ee04b1-9606-4852-a138-dbccb5b83834` |
| **HTTP Method** | `POST` |
| **URL** | `/tryitout/H0UNMKO0` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `ws://ops.koreainvestment.com:21000` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID** | `모의투자 미지원`, `H0UNMKO0` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2025-03-06
- **최종 수정일**: 2025-04-30

## 요청 (Request)

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `approval_key` | 웹소켓 접속키 | String | 286 | N | 실시간 (웹소켓) 접속키 발급 API(/oauth2/Approval)를 사용하여 발급받은 웹소켓 접속키 |
| `custtype` | 고객 타입 | String | 1 | Y | B : 법인  P : 개인 |
| `tr_type` | 거래타입 | String | 1 | N | 1 : 등록 2 : 해제 |
| `content-type` | 컨텐츠타입 | String | 1 | N | utf-8 |

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `tr_id` | 거래ID | String | 2 | Y | H0UNMKO0 : 국내주식 장운영정보 (통합) |
| `tr_key` | 구분값 | String | 12 | Y | 종목코드 (ex 005930 삼성전자) |

## 응답 (Response)

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `TRHT_YN` | 거래정지 여부 | String | 1 | Y |  |
| `TR_SUSP_REAS_CNTT` | 거래 정지 사유 내용 | String | 100 | Y |  |
| `MKOP_CLS_CODE` | 장운영 구분 코드 | String | 3 | Y |  |
| `ANTC_MKOP_CLS_CODE` | 예상 장운영 구분 코드 | String | 3 | Y |  |
| `MRKT_TRTM_CLS_CODE` | 임의연장구분코드 | String | 1 | Y |  |
| `DIVI_APP_CLS_CODE` | 동시호가배분처리구분코드 | String | 2 | Y |  |
| `ISCD_STAT_CLS_CODE` | 종목상태구분코드 | String | 2 | Y |  |
| `VI_CLS_CODE` | VI적용구분코드 | String | 1 | Y |  |
| `OVTM_VI_CLS_CODE` | 시간외단일가VI적용구분코드 | String | 1 | Y |  |
| `EXCH_CLS_CODE` | 거래소 구분코드 | String | 1 | Y |  |
