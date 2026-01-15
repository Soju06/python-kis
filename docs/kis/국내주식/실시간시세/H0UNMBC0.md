# 국내주식 실시간회원사 (통합)

> [국내주식] 실시간시세

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `8e1f270a-98d0-4b2a-8b5e-15ff6db6b5db` |
| **HTTP Method** | `POST` |
| **URL** | `/tryitout/H0UNMBC0` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `ws://ops.koreainvestment.com:21000` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID** | `H0UNMBC0`, `모의투자 미지원` |

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
| `custtype` | 고객타입 | String | 1 | N | 'B : 법인 P : 개인' |
| `tr_type` | 거래타입 | String | 1 | N | '1 : 등록 2 : 해제' |
| `content-type` | 컨텐츠타입 | String | 1 | N | '	utf-8' |

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `tr_id` | 거래ID | String | 2 | Y | H0UNMBC0 : 국내주식 주식종목회원사 (통합) |
| `tr_key` | 구분값 | String | 12 | Y | 종목코드 (ex 005930 삼성전자) |

## 응답 (Response)

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `MKSC_SHRN_ISCD` | 유가증권 단축 종목코드 | String | 9 | Y |  |
| `SELN2_MBCR_NAME1` | 매도2 회원사명1 | String | 16 | Y |  |
| `SELN2_MBCR_NAME2` | 매도2 회원사명2 | String | 16 | Y |  |
| `SELN2_MBCR_NAME3` | 매도2 회원사명3 | String | 16 | Y |  |
| `SELN2_MBCR_NAME4` | 매도2 회원사명4 | String | 16 | Y |  |
| `SELN2_MBCR_NAME5` | 매도2 회원사명5 | String | 16 | Y |  |
| `BYOV_MBCR_NAME1` | 매수 회원사명1 | String | 16 | Y |  |
| `BYOV_MBCR_NAME2` | 매수 회원사명2 | String | 16 | Y |  |
| `BYOV_MBCR_NAME3` | 매수 회원사명3 | String | 16 | Y |  |
| `BYOV_MBCR_NAME4` | 매수 회원사명4 | String | 16 | Y |  |
| `BYOV_MBCR_NAME5` | 매수 회원사명5 | String | 16 | Y |  |
| `TOTAL_SELN_QTY1` | 총 매도 수량1 | String | 8 | Y |  |
| `TOTAL_SELN_QTY2` | 총 매도 수량2 | String | 8 | Y |  |
| `TOTAL_SELN_QTY3` | 총 매도 수량3 | String | 8 | Y |  |
| `TOTAL_SELN_QTY4` | 총 매도 수량4 | String | 8 | Y |  |
| `TOTAL_SELN_QTY5` | 총 매도 수량5 | String | 8 | Y |  |
| `TOTAL_SHNU_QTY1` | 총 매수2 수량1 | String | 8 | Y |  |
| `TOTAL_SHNU_QTY2` | 총 매수2 수량2 | String | 8 | Y |  |
| `TOTAL_SHNU_QTY3` | 총 매수2 수량3 | String | 8 | Y |  |
| `TOTAL_SHNU_QTY4` | 총 매수2 수량4 | String | 8 | Y |  |
| `TOTAL_SHNU_QTY5` | 총 매수2 수량5 | String | 8 | Y |  |
| `SELN_MBCR_GLOB_YN_1` | 매도거래원구분1 | String | 1 | Y |  |
| `SELN_MBCR_GLOB_YN_2` | 매도거래원구분2 | String | 1 | Y |  |
| `SELN_MBCR_GLOB_YN_3` | 매도거래원구분3 | String | 1 | Y |  |
| `SELN_MBCR_GLOB_YN_4` | 매도거래원구분4 | String | 1 | Y |  |
| `SELN_MBCR_GLOB_YN_5` | 매도거래원구분5 | String | 1 | Y |  |
| `SHNU_MBCR_GLOB_YN_1` | 매수거래원구분1 | String | 1 | Y |  |
| `SHNU_MBCR_GLOB_YN_2` | 매수거래원구분2 | String | 1 | Y |  |
| `SHNU_MBCR_GLOB_YN_3` | 매수거래원구분3 | String | 1 | Y |  |
| `SHNU_MBCR_GLOB_YN_4` | 매수거래원구분4 | String | 1 | Y |  |
| `SHNU_MBCR_GLOB_YN_5` | 매수거래원구분5 | String | 1 | Y |  |
| `SELN_MBCR_NO1` | 매도거래원코드1 | String | 5 | Y |  |
| `SELN_MBCR_NO2` | 매도거래원코드2 | String | 5 | Y |  |
| `SELN_MBCR_NO3` | 매도거래원코드3 | String | 5 | Y |  |
| `SELN_MBCR_NO4` | 매도거래원코드4 | String | 5 | Y |  |
| `SELN_MBCR_NO5` | 매도거래원코드5 | String | 5 | Y |  |
| `SHNU_MBCR_NO1` | 매수거래원코드1 | String | 5 | Y |  |
| `SHNU_MBCR_NO2` | 매수거래원코드2 | String | 5 | Y |  |
| `SHNU_MBCR_NO3` | 매수거래원코드3 | String | 5 | Y |  |
| `SHNU_MBCR_NO4` | 매수거래원코드4 | String | 5 | Y |  |
| `SHNU_MBCR_NO5` | 매수거래원코드5 | String | 5 | Y |  |
| `SELN_MBCR_RLIM1` | 매도 회원사 비중1 | String | 8 | Y |  |
| `SELN_MBCR_RLIM2` | 매도 회원사 비중2 | String | 8 | Y |  |
| `SELN_MBCR_RLIM3` | 매도 회원사 비중3 | String | 8 | Y |  |
| `SELN_MBCR_RLIM4` | 매도 회원사 비중4 | String | 8 | Y |  |
| `SELN_MBCR_RLIM5` | 매도 회원사 비중5 | String | 8 | Y |  |
| `SHNU_MBCR_RLIM1` | 매수2 회원사 비중1 | String | 8 | Y |  |
| `SHNU_MBCR_RLIM2` | 매수2 회원사 비중2 | String | 8 | Y |  |
| `SHNU_MBCR_RLIM3` | 매수2 회원사 비중3 | String | 8 | Y |  |
| `SHNU_MBCR_RLIM4` | 매수2 회원사 비중4 | String | 8 | Y |  |
| `SHNU_MBCR_RLIM5` | 매수2 회원사 비중5 | String | 8 | Y |  |
| `SELN_QTY_ICDC1` | 매도 수량 증감1 | String | 4 | Y |  |
| `SELN_QTY_ICDC2` | 매도 수량 증감2 | String | 4 | Y |  |
| `SELN_QTY_ICDC3` | 매도 수량 증감3 | String | 4 | Y |  |
| `SELN_QTY_ICDC4` | 매도 수량 증감4 | String | 4 | Y |  |
| `SELN_QTY_ICDC5` | 매도 수량 증감5 | String | 4 | Y |  |
| `SHNU_QTY_ICDC1` | 매수2 수량 증감1 | String | 4 | Y |  |
| `SHNU_QTY_ICDC2` | 매수2 수량 증감2 | String | 4 | Y |  |
| `SHNU_QTY_ICDC3` | 매수2 수량 증감3 | String | 4 | Y |  |
| `SHNU_QTY_ICDC4` | 매수2 수량 증감4 | String | 4 | Y |  |
| `SHNU_QTY_ICDC5` | 매수2 수량 증감5 | String | 4 | Y |  |
| `GLOB_TOTAL_SELN_QTY` | 외국계 총 매도 수량 | String | 8 | Y |  |
| `GLOB_TOTAL_SHNU_QTY` | 외국계 총 매수2 수량 | String | 8 | Y |  |
| `GLOB_TOTAL_SELN_QTY_ICDC` | 외국계 총 매도 수량 증감 | String | 4 | Y |  |
| `GLOB_TOTAL_SHNU_QTY_ICDC` | 외국계 총 매수2 수량 증감 | String | 4 | Y |  |
| `GLOB_NTBY_QTY` | 외국계 순매수 수량 | String | 8 | Y |  |
| `GLOB_SELN_RLIM` | 외국계 매도 비중 | String | 8 | Y |  |
| `GLOB_SHNU_RLIM` | 외국계 매수2 비중 | String | 8 | Y |  |
| `SELN2_MBCR_ENG_NAME1` | 매도2 영문회원사명1 | String | 20 | Y |  |
| `SELN2_MBCR_ENG_NAME2` | 매도2 영문회원사명2 | String | 20 | Y |  |
| `SELN2_MBCR_ENG_NAME3` | 매도2 영문회원사명3 | String | 20 | Y |  |
| `SELN2_MBCR_ENG_NAME4` | 매도2 영문회원사명4 | String | 20 | Y |  |
| `SELN2_MBCR_ENG_NAME5` | 매도2 영문회원사명5 | String | 20 | Y |  |
| `BYOV_MBCR_ENG_NAME1` | 매수 영문회원사명1 | String | 20 | Y |  |
| `BYOV_MBCR_ENG_NAME2` | 매수 영문회원사명2 | String | 20 | Y |  |
| `BYOV_MBCR_ENG_NAME3` | 매수 영문회원사명3 | String | 20 | Y |  |
| `BYOV_MBCR_ENG_NAME4` | 매수 영문회원사명4 | String | 20 | Y |  |
| `BYOV_MBCR_ENG_NAME5` | 매수 영문회원사명5 | String | 20 | Y |  |
