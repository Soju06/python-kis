# 국내주식 실시간체결가 (NXT)

> [국내주식] 실시간시세



## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `ce1f9bd8-a9bf-41a8-9a01-32178b94c499` |
| **HTTP Method** | `POST` |
| **URL** | `/tryitout/H0NXCNT0` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `ws://ops.koreainvestment.com:21000` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `H0NXCNT0` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2025-03-06
- **최종 수정일**: 2025-04-30

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
| `tr_id` | 거래ID | String | 2 | Y | H0NXCNT0 : 주식종목체결 (NXT) |
| `tr_key` | 구분값 | String | 12 | Y | 종목코드 (ex 005930 삼성전자) |

## 응답

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `MKSC_SHRN_ISCD` | 유가증권 단축 종목코드 | String | 9 | Y |  |
| `STCK_CNTG_HOUR` | 주식 체결 시간 | String | 6 | Y |  |
| `STCK_PRPR` | 주식 현재가 | String | 4 | Y |  |
| `PRDY_VRSS_SIGN` | 전일 대비 부호 | String | 1 | Y |  |
| `PRDY_VRSS` | 전일 대비 | String | 4 | Y |  |
| `PRDY_CTRT` | 전일 대비율 | String | 8 | Y |  |
| `WGHN_AVRG_STCK_PRC` | 가중 평균 주식 가격 | String | 8 | Y |  |
| `STCK_OPRC` | 주식 시가 | String | 4 | Y |  |
| `STCK_HGPR` | 주식 최고가 | String | 4 | Y |  |
| `STCK_LWPR` | 주식 최저가 | String | 4 | Y |  |
| `ASKP1` | 매도호가1 | String | 4 | Y |  |
| `BIDP1` | 매수호가1 | String | 4 | Y |  |
| `CNTG_VOL` | 체결 거래량 | String | 8 | Y |  |
| `ACML_VOL` | 누적 거래량 | String | 8 | Y |  |
| `ACML_TR_PBMN` | 누적 거래 대금 | String | 8 | Y |  |
| `SELN_CNTG_CSNU` | 매도 체결 건수 | String | 4 | Y |  |
| `SHNU_CNTG_CSNU` | 매수 체결 건수 | String | 4 | Y |  |
| `NTBY_CNTG_CSNU` | 순매수 체결 건수 | String | 4 | Y |  |
| `CTTR` | 체결강도 | String | 8 | Y |  |
| `SELN_CNTG_SMTN` | 총 매도 수량 | String | 8 | Y |  |
| `SHNU_CNTG_SMTN` | 총 매수 수량 | String | 8 | Y |  |
| `CNTG_CLS_CODE` | 체결구분 | String | 1 | Y |  |
| `SHNU_RATE` | 매수비율 | String | 8 | Y |  |
| `PRDY_VOL_VRSS_ACML_VOL_RATE` | 전일 거래량 대비 등락율 | String | 8 | Y |  |
| `OPRC_HOUR` | 시가 시간 | String | 6 | Y |  |
| `OPRC_VRSS_PRPR_SIGN` | 시가대비구분 | String | 1 | Y |  |
| `OPRC_VRSS_PRPR` | 시가대비 | String | 4 | Y |  |
| `HGPR_HOUR` | 최고가 시간 | String | 6 | Y |  |
| `HGPR_VRSS_PRPR_SIGN` | 고가대비구분 | String | 1 | Y |  |
| `HGPR_VRSS_PRPR` | 고가대비 | String | 4 | Y |  |
| `LWPR_HOUR` | 최저가 시간 | String | 6 | Y |  |
| `LWPR_VRSS_PRPR_SIGN` | 저가대비구분 | String | 1 | Y |  |
| `LWPR_VRSS_PRPR` | 저가대비 | String | 4 | Y |  |
| `BSOP_DATE` | 영업 일자 | String | 8 | Y |  |
| `NEW_MKOP_CLS_CODE` | 신 장운영 구분 코드 | String | 2 | Y |  |
| `TRHT_YN` | 거래정지 여부 | String | 1 | Y |  |
| `ASKP_RSQN1` | 매도호가 잔량1 | String | 8 | Y |  |
| `BIDP_RSQN1` | 매수호가 잔량1 | String | 8 | Y |  |
| `TOTAL_ASKP_RSQN` | 총 매도호가 잔량 | String | 8 | Y |  |
| `TOTAL_BIDP_RSQN` | 총 매수호가 잔량 | String | 8 | Y |  |
| `VOL_TNRT` | 거래량 회전율 | String | 8 | Y |  |
| `PRDY_SMNS_HOUR_ACML_VOL` | 전일 동시간 누적 거래량 | String | 8 | Y |  |
| `PRDY_SMNS_HOUR_ACML_VOL_RATE` | 전일 동시간 누적 거래량 비율 | String | 8 | Y |  |
| `HOUR_CLS_CODE` | 시간 구분 코드 | String | 1 | Y |  |
| `MRKT_TRTM_CLS_CODE` | 임의종료구분코드 | String | 1 | Y |  |
| `VI_STND_PRC` | 정적VI발동기준가 | String | 4 | Y |  |

