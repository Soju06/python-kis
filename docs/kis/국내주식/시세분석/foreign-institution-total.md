# 국내기관_외국인 매매종목가집계[국내주식-037]

> [국내주식] 시세분석

국내기관_외국인 매매종목가집계 API입니다.

HTS(efriend Plus) [0440] 외국인/기관 매매종목 가집계 화면을 API로 구현한 사항으로 화면을 함께 보시면 기능 이해가 쉽습니다.

증권사 직원이 장중에 집계/입력한 자료를 단순 누계한 수치로서, 
입력시간은 외국인 09:30, 11:20, 13:20, 14:30 / 기관종합 10:00, 11:20, 13:20, 14:30 이며, 
입력한 시간은 ±10분정도 차이가 발생할 수 있으며, 장운영 사정에 다라 변동될 수 있습니다.

국내기관_외국인 매매종목가집계[국내주식-037]

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `4a077f43-7053-47be-b811-8e35be4ea745` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/quotations/foreign-institution-total` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID** | `모의투자 미지원`, `FHPTJ04400000` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2023-01-06
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
| `tr_id` | 거래ID | String | 13 | Y | FHPTJ04400000 |
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
| `FID_COND_MRKT_DIV_CODE` | 시장 분류 코드 | String | 2 | Y | V(Default) |
| `FID_COND_SCR_DIV_CODE` | 조건 화면 분류 코드 | String | 5 | Y | 16449(Default) |
| `FID_INPUT_ISCD` | 입력 종목코드 | String | 12 | Y | 0000:전체, 0001:코스피, 1001:코스닥 ... 포탈 (FAQ : 종목정보 다운로드(국내) - 업종코드 참조) |
| `FID_DIV_CLS_CODE` | 분류 구분 코드 | String | 2 | Y | 0: 수량정열, 1: 금액정열 |
| `FID_RANK_SORT_CLS_CODE` | 순위 정렬 구분 코드 | String | 2 | Y | 0: 순매수상위, 1: 순매도상위 |
| `FID_ETC_CLS_CODE` | 기타 구분  정렬 | String | 2 | Y | 0:전체 1:외국인 2:기관계 3:기타 |

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
| `Output` | 응답상세1 | String |   | Y |  |
| `hts_kor_isnm` | HTS 한글 종목명 | String | 40 | Y |  |
| `mksc_shrn_iscd` | 유가증권 단축 종목코드 | String | 9 | Y |  |
| `ntby_qty` | 순매수 수량 | String | 18 | Y |  |
| `stck_prpr` | 주식 현재가 | String | 10 | Y |  |
| `prdy_vrss_sign` | 전일 대비 부호 | String | 1 | Y |  |
| `prdy_vrss` | 전일 대비 | String | 10 | Y |  |
| `prdy_ctrt` | 전일 대비율 | String | 8 | Y |  |
| `acml_vol` | 누적 거래량 | String | 18 | Y |  |
| `frgn_ntby_qty` | 외국인 순매수 수량 | String | 12 | Y |  |
| `orgn_ntby_qty` | 기관계 순매수 수량 | String | 18 | Y |  |
| `ivtr_ntby_qty` | 투자신탁 순매수 수량 | String | 12 | Y |  |
| `bank_ntby_qty` | 은행 순매수 수량 | String | 12 | Y |  |
| `insu_ntby_qty` | 보험 순매수 수량 | String | 12 | Y |  |
| `mrbn_ntby_qty` | 종금 순매수 수량 | String | 12 | Y |  |
| `fund_ntby_qty` | 기금 순매수 수량 | String | 12 | Y |  |
| `etc_orgt_ntby_vol` | 기타 단체 순매수 거래량 | String | 18 | Y |  |
| `etc_corp_ntby_vol` | 기타 법인 순매수 거래량 | String | 18 | Y |  |
| `frgn_ntby_tr_pbmn` | 외국인 순매수 거래 대금 | String | 18 | Y | frgn_ntby_tr_pbmn ~ etc_corp_ntby_tr_pbmn (단위 : 백만원, 수량*현재가) |
| `orgn_ntby_tr_pbmn` | 기관계 순매수 거래 대금 | String | 18 | Y |  |
| `ivtr_ntby_tr_pbmn` | 투자신탁 순매수 거래 대금 | String | 18 | Y |  |
| `bank_ntby_tr_pbmn` | 은행 순매수 거래 대금 | String | 18 | Y |  |
| `insu_ntby_tr_pbmn` | 보험 순매수 거래 대금 | String | 18 | Y |  |
| `mrbn_ntby_tr_pbmn` | 종금 순매수 거래 대금 | String | 18 | Y |  |
| `fund_ntby_tr_pbmn` | 기금 순매수 거래 대금 | String | 18 | Y |  |
| `etc_orgt_ntby_tr_pbmn` | 기타 단체 순매수 거래 대금 | String | 18 | Y |  |
| `etc_corp_ntby_tr_pbmn` | 기타 법인 순매수 거래 대금 | String | 18 | Y |  |
