# 지수선물 실시간체결가[실시간-010]

> [국내선물옵션] 실시간시세

[참고자료]

실시간시세(웹소켓) 파이썬 샘플코드는 한국투자증권 Github 참고 부탁드립니다.
https://github.com/koreainvestment/open-trading-api/blob/main/websocket/python/ws_domestic_overseas_all.py

실시간시세(웹소켓) API 사용방법에 대한 자세한 설명은 한국투자증권 Wikidocs 참고 부탁드립니다.
https://wikidocs.net/book/7847 (국내주식 업데이트 완료, 추후 해외주식·국내선물옵션 업데이트 예정)

종목코드 마스터파일 파이썬 정제코드는 한국투자증권 Github 참고 부탁드립니다.
https://github.com/koreainvestment/open-trading-api/tree/main/stocks_info

[실시간-010] 지수선물 실시간체결가

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `641bf3d8-f381-4661-aaad-d9ee05e05489` |
| **HTTP Method** | `POST` |
| **URL** | `/tryitout/H0IFCNT0` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `ws://ops.koreainvestment.com:21000` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `H0IFCNT0` |
| **TR ID (모의)** | `모의투자 미지원` |

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
| `custtype` | 고객 타입 | String | 1 | Y | B : 법인 / P : 개인 |
| `tr_type` | 등록/해제 | String | 1 | Y | "1: 등록, 2:해제" |
| `content-type` | 컨텐츠타입 | String | 20 | Y | utf-8 |

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `tr_id` | 거래ID | String | 7 | Y | H0IFCNT0 |
| `tr_key` | 코드 | String | 6 | Y | 예:101S12 |

## 응답

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `FUTS_SHRN_ISCD` | 선물 단축 종목코드 | String | 16 | Y | '각 항목사이에는 구분자로 ^ 사용, 모든 데이터타입은 String으로 변환되어 push 처리됨' |
| `BSOP_HOUR` | 영업 시간 | String | 16 | Y |  |
| `FUTS_PRDY_VRSS` | 선물 전일 대비 | String | 1 | Y |  |
| `PRDY_VRSS_SIGN` | 전일 대비 부호 | String | 8 | Y |  |
| `FUTS_PRDY_CTRT` | 선물 전일 대비율 | String | 8 | Y |  |
| `FUTS_PRPR` | 선물 현재가 | String | 8 | Y |  |
| `FUTS_OPRC` | 선물 시가2 | String | 8 | Y |  |
| `FUTS_HGPR` | 선물 최고가 | String | 8 | Y |  |
| `FUTS_LWPR` | 선물 최저가 | String | 8 | Y |  |
| `LAST_CNQN` | 최종 거래량 | String | 8 | Y | 체결량 |
| `ACML_VOL` | 누적 거래량 | String | 8 | Y |  |
| `ACML_TR_PBMN` | 누적 거래 대금 | String | 8 | Y |  |
| `HTS_THPR` | HTS 이론가 | String | 8 | Y |  |
| `MRKT_BASIS` | 시장 베이시스 | String | 8 | Y |  |
| `DPRT` | 괴리율 | String | 8 | Y |  |
| `NMSC_FCTN_STPL_PRC` | 근월물 약정가 | String | 8 | Y |  |
| `FMSC_FCTN_STPL_PRC` | 원월물 약정가 | String | 8 | Y |  |
| `SPEAD_PRC` | 스프레드1 | String | 8 | Y |  |
| `HTS_OTST_STPL_QTY` | HTS 미결제 약정 수량 | String | 8 | Y |  |
| `OTST_STPL_QTY_ICDC` | 미결제 약정 수량 증감 | String | 8 | Y |  |
| `OPRC_HOUR` | 시가 시간 | String | 8 | Y |  |
| `OPRC_VRSS_PRPR_SIGN` | 시가2 대비 현재가 부호 | String | 8 | Y |  |
| `OPRC_VRSS_NMIX_PRPR` | 시가 대비 지수 현재가 | String | 8 | Y |  |
| `HGPR_HOUR` | 최고가 시간 | String | 8 | Y |  |
| `HGPR_VRSS_PRPR_SIGN` | 최고가 대비 현재가 부호 | String | 8 | Y |  |
| `HGPR_VRSS_NMIX_PRPR` | 최고가 대비 지수 현재가 | String | 8 | Y |  |
| `LWPR_HOUR` | 최저가 시간 | String | 8 | Y |  |
| `LWPR_VRSS_PRPR_SIGN` | 최저가 대비 현재가 부호 | String | 8 | Y |  |
| `LWPR_VRSS_NMIX_PRPR` | 최저가 대비 지수 현재가 | String | 8 | Y |  |
| `SHNU_RATE` | 매수2 비율 | String | 8 | Y |  |
| `CTTR` | 체결강도 | String | 8 | Y |  |
| `ESDG` | 괴리도 | String | 8 | Y |  |
| `OTST_STPL_RGBF_QTY_ICDC` | 미결제 약정 직전 수량 증감 | String | 8 | Y |  |
| `THPR_BASIS` | 이론 베이시스 | String | 8 | Y |  |
| `FUTS_ASKP1` | 선물 매도호가1 | String | 8 | Y |  |
| `FUTS_BIDP1` | 선물 매수호가1 | String | 8 | Y |  |
| `ASKP_RSQN1` | 매도호가 잔량1 | String | 8 | Y |  |
| `BIDP_RSQN1` | 매수호가 잔량1 | String | 8 | Y |  |
| `SELN_CNTG_CSNU` | 매도 체결 건수 | String | 6 | Y |  |
| `SHNU_CNTG_CSNU` | 매수 체결 건수 | String | 6 | Y |  |
| `NTBY_CNTG_CSNU` | 순매수 체결 건수 | String | 6 | Y |  |
| `SELN_CNTG_SMTN` | 총 매도 수량 | String | 6 | Y |  |
| `SHNU_CNTG_SMTN` | 총 매수 수량 | String | 6 | Y |  |
| `TOTAL_ASKP_RSQN` | 총 매도호가 잔량 | String | 6 | Y |  |
| `TOTAL_BIDP_RSQN` | 총 매수호가 잔량 | String | 6 | Y |  |
| `PRDY_VOL_VRSS_ACML_VOL_RATE` | 전일 거래량 대비 등락율 | String | 6 | Y |  |
| `DSCS_BLTR_ACML_QTY` | 협의 대량 거래량 | String | 6 | Y |  |
| `DYNM_MXPR` | 실시간상한가 | String | 8 | Y |  |
| `DYNM_LLAM` | 실시간하한가 | String | 6 | Y |  |
| `DYNM_PRC_LIMT_YN` | 실시간가격제한구분 | String | 10 | Y |  |

