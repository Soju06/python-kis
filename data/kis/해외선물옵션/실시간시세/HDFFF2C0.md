# 해외선물옵션 실시간체결내역통보[실시간-020]

> [해외선물옵션]실시간시세


해외선물옵션체결내역통보[실시간-020]

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `cb0618f5-967f-4d26-a6eb-527bfd693041` |
| **HTTP Method** | `POST` |
| **URL** | `/tryitout/HDFFF2C0` |
| **Content-Type** | `application/json; charset=utf-8` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `ws://ops.koreainvestment.com:21000` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `HDFFF2C0` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2023-01-06T09:10:32+09:00
- **최종 수정일**: 2025-04-30T13:22:11+09:00

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `approval_key` | 웹소켓 접속키 | String | 36 | Y | 실시간 (웹소켓) 접속키 발급 API(/oauth2/Approval)를 사용하여 발급받은 웹소켓 접속키 |
| `tr_type` | 등록/해제 | String | 1 | Y | "1: 등록, 2:해제" |
| `custtype` | 고객 타입 | String | 1 | Y | B : 법인 / P : 개인 |
| `content-type` | 컨텐츠타입 | String | 20 | Y | utf-8 |

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `tr_id` | 거래ID | String | 7 | Y | HDFFF2C0 |
| `tr_key` | HTSID | String | 8 | Y | HTSID |

## 응답

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `USER_ID` | 유저ID | String | 8 | Y | '각 항목사이에는 구분자로 ^ 사용, 모든 데이터타입은 String으로 변환되어 push 처리됨' |
| `ACCT_NO` | 계좌번호 | String | 10 | Y |  |
| `ORD_DT` | 주문일자 | String | 8 | Y |  |
| `ODNO` | 주문번호 | String | 10 | Y |  |
| `ORGN_ORD_DT` | 원주문일자 | String | 8 | Y |  |
| `ORGN_ODNO` | 원주문번호 | String | 10 | Y |  |
| `SERIES` | 종목명 | String | 32 | Y |  |
| `RVSE_CNCL_DVSN_CD` | 정정취소구분코드 | String | 2 | Y | 해당없음 : 00 , 정정 : 01 , 취소 : 02 |
| `SLL_BUY_DVSN_CD` | 매도매수구분코드 | String | 2 | Y | 01 : 매도,  02 : 매수 |
| `CPLX_ORD_DVSN_CD` | 복합주문구분코드 | String | 1 | Y | 0 (hedge청산만 이용) |
| `PRCE_TP` | 가격구분코드 | String | 1 | Y |  |
| `FM_EXCG_RCIT_DVSN_CD` | FM거래소접수구분코드 | String | 2 | Y |  |
| `ORD_QTY` | 주문수량 | String | 18 | Y |  |
| `FM_LMT_PRIC` | FMLIMIT가격 | String | 21 | Y |  |
| `FM_STOP_ORD_PRIC` | FMSTOP주문가격 | String | 21 | Y |  |
| `TOT_CCLD_QTY` | 총체결수량 | String | 18 | Y | 동일한 주문건에 대한 누적된 체결수량 (하나의 주문건에 여러건의 체결내역 발생) |
| `TOT_CCLD_UV` | 총체결단가 | String | 21 | Y |  |
| `ORD_REMQ` | 잔량 | String | 21 | Y |  |
| `FM_ORD_GRP_DT` | FM주문그룹일자 | String | 8 | Y |  |
| `ORD_GRP_STNO` | 주문그룹번호 | String | 12 | Y |  |
| `ORD_DTL_DTIME` | 주문상세일시 | String | 17 | Y |  |
| `OPRT_DTL_DTIME` | 조작상세일시 | String | 17 | Y |  |
| `WORK_EMPL` | 주문자 | String | 8 | Y |  |
| `CCLD_DT` | 체결일자 | String | 8 | Y |  |
| `CCNO` | 체결번호 | String | 11 | Y |  |
| `API_CCNO` | API 체결번호 | String | 20 | Y |  |
| `CCLD_QTY` | 체결수량 | String | 18 | Y | 매 체결 단위 체결수량임 (여러건 체결내역 누적 체결수량인 총체결수량과 다름) |
| `FM_CCLD_PRIC` | FM체결가격 | String | 21 | Y |  |
| `CRCY_CD` | 통화코드 | String | 3 | Y |  |
| `TRST_FEE` | 위탁수수료 | String | 21 | Y |  |
| `ORD_MDIA_ONLINE_YN` | 주문매체온라인여부 | String | 1 | Y |  |
| `FM_CCLD_AMT` | FM체결금액 | String | 21 | Y |  |
| `FUOP_ITEM_DVSN_CD` | 선물옵션종목구분코드 | String | 2 | Y |  |

