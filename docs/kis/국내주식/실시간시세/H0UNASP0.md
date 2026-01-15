# 국내주식 실시간호가 (통합)

> [국내주식] 실시간시세

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `5dbf113a-f697-4295-8168-a93812aa3bfb` |
| **HTTP Method** | `POST` |
| **URL** | `/tryitout/H0UNASP0` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `ws://ops.koreainvestment.com:21000` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID** | `모의투자 미지원`, `H0UNASP0` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2025-02-28
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
| `tr_id` | 거래ID | String | 2 | Y | H0UNASP0 : 실시간 주식 체결가 통합 |
| `tr_key` | 구분값 | String | 12 | Y | 종목코드 (ex 005930 삼성전자) |

## 응답 (Response)

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `MKSC_SHRN_ISCD` | 유가증권 단축 종목코드 | String | 9 | Y |  |
| `BSOP_HOUR` | 영업 시간 | String | 6 | Y |  |
| `HOUR_CLS_CODE` | 시간 구분 코드 | String | 1 | Y |  |
| `ASKP1` | 매도호가1 | String | 4 | Y |  |
| `ASKP2` | 매도호가2 | String | 4 | Y |  |
| `ASKP3` | 매도호가3 | String | 4 | Y |  |
| `ASKP4` | 매도호가4 | String | 4 | Y |  |
| `ASKP5` | 매도호가5 | String | 4 | Y |  |
| `ASKP6` | 매도호가6 | String | 4 | Y |  |
| `ASKP7` | 매도호가7 | String | 4 | Y |  |
| `ASKP8` | 매도호가8 | String | 4 | Y |  |
| `ASKP9` | 매도호가9 | String | 4 | Y |  |
| `ASKP10` | 매도호가10 | String | 4 | Y |  |
| `BIDP1` | 매수호가1 | String | 4 | Y |  |
| `BIDP2` | 매수호가2 | String | 4 | Y |  |
| `BIDP3` | 매수호가3 | String | 4 | Y |  |
| `BIDP4` | 매수호가4 | String | 4 | Y |  |
| `BIDP5` | 매수호가5 | String | 4 | Y |  |
| `BIDP6` | 매수호가6 | String | 4 | Y |  |
| `BIDP7` | 매수호가7 | String | 4 | Y |  |
| `BIDP8` | 매수호가8 | String | 4 | Y |  |
| `BIDP9` | 매수호가9 | String | 4 | Y |  |
| `BIDP10` | 매수호가10 | String | 4 | Y |  |
| `ASKP_RSQN1` | 매도호가 잔량1 | String | 8 | Y |  |
| `ASKP_RSQN2` | 매도호가 잔량2 | String | 8 | Y |  |
| `ASKP_RSQN3` | 매도호가 잔량3 | String | 8 | Y |  |
| `ASKP_RSQN4` | 매도호가 잔량4 | String | 8 | Y |  |
| `ASKP_RSQN5` | 매도호가 잔량5 | String | 8 | Y |  |
| `ASKP_RSQN6` | 매도호가 잔량6 | String | 8 | Y |  |
| `ASKP_RSQN7` | 매도호가 잔량7 | String | 8 | Y |  |
| `ASKP_RSQN8` | 매도호가 잔량8 | String | 8 | Y |  |
| `ASKP_RSQN9` | 매도호가 잔량9 | String | 8 | Y |  |
| `ASKP_RSQN10` | 매도호가 잔량10 | String | 8 | Y |  |
| `BIDP_RSQN1` | 매수호가 잔량1 | String | 8 | Y |  |
| `BIDP_RSQN2` | 매수호가 잔량2 | String | 8 | Y |  |
| `BIDP_RSQN3` | 매수호가 잔량3 | String | 8 | Y |  |
| `BIDP_RSQN4` | 매수호가 잔량4 | String | 8 | Y |  |
| `BIDP_RSQN5` | 매수호가 잔량5 | String | 8 | Y |  |
| `BIDP_RSQN6` | 매수호가 잔량6 | String | 8 | Y |  |
| `BIDP_RSQN7` | 매수호가 잔량7 | String | 8 | Y |  |
| `BIDP_RSQN8` | 매수호가 잔량8 | String | 8 | Y |  |
| `BIDP_RSQN9` | 매수호가 잔량9 | String | 8 | Y |  |
| `BIDP_RSQN10` | 매수호가 잔량10 | String | 8 | Y |  |
| `TOTAL_ASKP_RSQN` | 총 매도호가 잔량 | String | 8 | Y |  |
| `TOTAL_BIDP_RSQN` | 총 매수호가 잔량 | String | 8 | Y |  |
| `OVTM_TOTAL_ASKP_RSQN` | 시간외 총 매도호가 잔량 | String | 8 | Y |  |
| `OVTM_TOTAL_BIDP_RSQN` | 시간외 총 매수호가 잔량 | String | 8 | Y |  |
| `ANTC_CNPR` | 예상 체결가 | String | 4 | Y |  |
| `ANTC_CNQN` | 예상 체결량 | String | 8 | Y |  |
| `ANTC_VOL` | 예상 거래량 | String | 8 | Y |  |
| `ANTC_CNTG_VRSS` | 예상 체결 대비 | String | 4 | Y |  |
| `ANTC_CNTG_VRSS_SIGN` | 예상 체결 대비 부호 | String | 1 | Y |  |
| `ANTC_CNTG_PRDY_CTRT` | 예상 체결 전일 대비율 | String | 8 | Y |  |
| `ACML_VOL` | 누적 거래량 | String | 8 | Y |  |
| `TOTAL_ASKP_RSQN_ICDC` | 총 매도호가 잔량 증감 | String | 4 | Y |  |
| `TOTAL_BIDP_RSQN_ICDC` | 총 매수호가 잔량 증감 | String | 4 | Y |  |
| `OVTM_TOTAL_ASKP_ICDC` | 시간외 총 매도호가 증감 | String | 4 | Y |  |
| `OVTM_TOTAL_BIDP_ICDC` | 시간외 총 매수호가 증감 | String | 4 | Y |  |
| `STCK_DEAL_CLS_CODE` | 주식 매매 구분 코드 | String | 2 | Y |  |
| `KMID_PRC` | KRX 중간가 | String | 4 | Y |  |
| `KMID_TOTAL_RSQN` | KRX 중간가잔량합계수량 | String | 8 | Y |  |
| `KMID_CLS_CODE` | KRX 중간가 매수매도 구분 | String | 1 | Y |  |
| `NMID_PRC` | NXT 중간가 | String | 4 | Y |  |
| `NMID_TOTAL_RSQN` | NXT 중간가잔량합계수량 | String | 8 | Y |  |
| `NMID_CLS_CODE` | NXT 중간가 매수매도 구분 | String | 1 | Y |  |
