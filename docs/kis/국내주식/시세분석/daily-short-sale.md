# 국내주식 공매도 일별추이[국내주식-134]

> [국내주식] 시세분석

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `1069f2bf-962f-48db-8dc4-54d362065431` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/quotations/daily-short-sale` |
| **Content-Type** | `` |
| **요청 포맷** | `` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `미지` |
| **TR ID** | `FHPST04830000`, `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-04-01
- **최종 수정일**: 2025-05-14

## 요청 (Request)

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials G... |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | FHPST04830000 |
| `tr_cont` | 연속 거래 여부 | String | 1 | N | tr_cont를 이용한 다음조회 불가 API |
| `custtype` | 고객 타입 | String | 1 | Y | B : 법인  P : 개인 |
| `seq_no` | 일련번호 | String | 2 | N | [법인 필수] 001 |
| `mac_address` | 맥주소 | String | 12 | N | 법인고객 혹은 개인고객의 Mac address 값 |
| `phone_number` | 핸드폰번호 | String | 12 | N | [법인 필수] 제휴사APP을 사용하는 경우 사용자(회원) 핸드폰번호  ex) 01011112222 (하이픈 등 구분값 제거) |
| `ip_addr` | 접속 단말 공인 IP | String | 12 | N | [법인 필수] 사용자(회원)의 IP Address |
| `gt_uid` | Global UID | String | 32 | N | [법인 전용] 거래고유번호로 사용하므로 거래별로 UNIQUE해야 함 |

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `FID_INPUT_DATE_2` | 입력 날짜2 | String | 10 | Y | ~ 누적 |
| `FID_COND_MRKT_DIV_CODE` | 조건 시장 분류 코드 | String | 2 | Y | 시장구분코드 (주식 J) |
| `FID_INPUT_ISCD` | 입력 종목코드 | String | 12 | Y | 종목코드 |
| `FID_INPUT_DATE_1` | 입력 날짜1 | String | 10 | Y | 공백시 전체 (기간 ~) |

## 응답 (Response)

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `tr_id` | 거래ID | String | 13 | Y | 요청한 tr_id |
| `tr_cont` | 연속 거래 여부 | String | 1 | N | tr_cont를 이용한 다음조회 불가 API |
| `gt_uid` | Global UID | String | 32 | N | [법인 전용] 거래고유번호로 사용하므로 거래별로 UNIQUE해야 함 |

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `rt_cd` | 성공 실패 여부 | String | 1 | Y |  |
| `msg_cd` | 응답코드 | String | 8 | Y |  |
| `msg1` | 응답메세지 | String | 80 | Y |  |
| `output1` | 응답상세 | String |   | Y |  |
| `stck_prpr` | 주식 현재가 | String | 10 | Y |  |
| `prdy_vrss` | 전일 대비 | String | 10 | Y |  |
| `prdy_vrss_sign` | 전일 대비 부호 | String | 1 | Y |  |
| `prdy_ctrt` | 전일 대비율 | String | 82 | Y |  |
| `acml_vol` | 누적 거래량 | String | 18 | Y |  |
| `prdy_vol` | 전일 거래량 | String | 18 | Y |  |
| `output2` | 응답상세 | Object |   | Y | array |
| `stck_bsop_date` | 주식 영업 일자 | String | 8 | Y |  |
| `stck_clpr` | 주식 종가 | String | 10 | Y |  |
| `prdy_vrss` | 전일 대비 | String | 10 | Y |  |
| `prdy_vrss_sign` | 전일 대비 부호 | String | 1 | Y |  |
| `prdy_ctrt` | 전일 대비율 | String | 82 | Y |  |
| `acml_vol` | 누적 거래량 | String | 18 | Y |  |
| `stnd_vol_smtn` | 기준 거래량 합계 | String | 18 | Y |  |
| `ssts_cntg_qty` | 공매도 체결 수량 | String | 12 | Y |  |
| `ssts_vol_rlim` | 공매도 거래량 비중 | String | 62 | Y |  |
| `acml_ssts_cntg_qty` | 누적 공매도 체결 수량 | String | 13 | Y |  |
| `acml_ssts_cntg_qty_rlim` | 누적 공매도 체결 수량 비중 | String | 72 | Y |  |
| `acml_tr_pbmn` | 누적 거래 대금 | String | 18 | Y |  |
| `stnd_tr_pbmn_smtn` | 기준 거래대금 합계 | String | 18 | Y |  |
| `ssts_tr_pbmn` | 공매도 거래 대금 | String | 18 | Y |  |
| `ssts_tr_pbmn_rlim` | 공매도 거래대금 비중 | String | 62 | Y |  |
| `acml_ssts_tr_pbmn` | 누적 공매도 거래 대금 | String | 19 | Y |  |
| `acml_ssts_tr_pbmn_rlim` | 누적 공매도 거래 대금 비중 | String | 72 | Y |  |
| `stck_oprc` | 주식 시가2 | String | 10 | Y |  |
| `stck_hgpr` | 주식 최고가 | String | 10 | Y |  |
| `stck_lwpr` | 주식 최저가 | String | 10 | Y |  |
| `avrg_prc` | 평균가격 | String | 11 | Y |  |
