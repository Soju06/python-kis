# 상품선물 실시간호가[실시간-023]

> [국내선물옵션] 실시간시세

※ 선물옵션 호가 데이터는 0.2초 필터링 옵션이 있습니다.
  필터링 사유는 순간적으로 데이터가 폭증할 경우 서버 뿐만아니라 클라이언트 환경에도 부하를 줄 수 있어 적용된 사항인 점 양해 부탁드립니다.

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `932e6da0-9454-47d6-b26d-0cceb3349438` |
| **HTTP Method** | `POST` |
| **URL** | `/tryitout/H0CFASP0` |
| **Content-Type** | `` |
| **요청 포맷** | `` |
| **실전 도메인** | `ws://ops.koreainvestment.com:21000` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID** | `H0CFASP0`, `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2023-10-20
- **최종 수정일**: 2025-05-21

## 요청 (Request)

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `approval_key` | 웹소켓 접속키 | String | 36 | Y | 실시간 (웹소켓) 접속키 발급 API(/oauth2/Approval)를 사용하여 발급받은 웹소켓 접속키 |
| `custtype` | 고객 타입 | String | 1 | Y | B : 법인 / P : 개인 |
| `tr_type` | 등록/해제 | String | 1 | Y | "1: 등록, 2:해제" |
| `content-type` | 컨텐츠타입 | String | 20 | Y | utf-8 |

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `tr_id` | 거래ID | String | 7 | Y | H0CFASP0 |
| `tr_key` | 종목코드 | String | 6 | Y | 종목코드 |

## 응답 (Response)

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `FUTS_SHRN_ISCD` | 선물 단축 종목코드 | String | 32 | Y | '각 항목사이에는 구분자로 ^ 사용, 모든 데이터타입은 String으로 변환되어 push 처리됨' |
| `BSOP_HOUR` | 영업 시간 | String | 9 | Y |  |
| `FUTS_ASKP1` | 선물 매도호가1 | String | 6 | Y |  |
| `FUTS_ASKP2` | 선물 매도호가2 | String | 8 | Y |  |
| `FUTS_ASKP3` | 선물 매도호가3 | String | 1 | Y |  |
| `FUTS_ASKP4` | 선물 매도호가4 | String | 8 | Y |  |
| `FUTS_ASKP5` | 선물 매도호가5 | String | 8 | Y |  |
| `FUTS_BIDP1` | 선물 매수호가1 | String | 8 | Y |  |
| `FUTS_BIDP2` | 선물 매수호가2 | String | 8 | Y |  |
| `FUTS_BIDP3` | 선물 매수호가3 | String | 8 | Y |  |
| `FUTS_BIDP4` | 선물 매수호가4 | String | 8 | Y |  |
| `FUTS_BIDP5` | 선물 매수호가5 | String | 8 | Y |  |
| `ASKP_CSNU1` | 매도호가 건수1 | String | 8 | Y |  |
| `ASKP_CSNU2` | 매도호가 건수2 | String | 8 | Y |  |
| `ASKP_CSNU3` | 매도호가 건수3 | String | 8 | Y |  |
| `ASKP_CSNU4` | 매도호가 건수4 | String | 8 | Y |  |
| `ASKP_CSNU5` | 매도호가 건수5 | String | 8 | Y |  |
| `BIDP_CSNU1` | 매수호가 건수1 | String | 8 | Y |  |
| `BIDP_CSNU2` | 매수호가 건수2 | String | 8 | Y |  |
| `BIDP_CSNU3` | 매수호가 건수3 | String | 8 | Y |  |
| `BIDP_CSNU4` | 매수호가 건수4 | String | 4 | Y |  |
| `BIDP_CSNU5` | 매수호가 건수5 | String | 6 | Y |  |
| `ASKP_RSQN1` | 매도호가 잔량1 | String | 1 | Y |  |
| `ASKP_RSQN2` | 매도호가 잔량2 | String | 8 | Y |  |
| `ASKP_RSQN3` | 매도호가 잔량3 | String | 6 | Y |  |
| `ASKP_RSQN4` | 매도호가 잔량4 | String | 1 | Y |  |
| `ASKP_RSQN5` | 매도호가 잔량5 | String | 8 | Y |  |
| `BIDP_RSQN1` | 매수호가 잔량1 | String | 6 | Y |  |
| `BIDP_RSQN2` | 매수호가 잔량2 | String | 1 | Y |  |
| `BIDP_RSQN3` | 매수호가 잔량3 | String | 8 | Y |  |
| `BIDP_RSQN4` | 매수호가 잔량4 | String | 8 | Y |  |
| `BIDP_RSQN5` | 매수호가 잔량5 | String | 8 | Y |  |
| `TOTAL_ASKP_CSNU` | 총 매도호가 건수 | String | 8 | Y |  |
| `TOTAL_BIDP_CSNU` | 총 매수호가 건수 | String | 4 | Y |  |
| `TOTAL_ASKP_RSQN` | 총 매도호가 잔량 | String | 8 | Y |  |
| `TOTAL_BIDP_RSQN` | 총 매수호가 잔량 | String | 8 | Y |  |
| `TOTAL_ASKP_RSQN_ICDC` | 총 매도호가 잔량 증감 | String | 8 | Y |  |
| `TOTAL_BIDP_RSQN_ICDC` | 총 매수호가 잔량 증감 | String | 8 | Y |  |
