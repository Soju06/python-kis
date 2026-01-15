# 지수옵션 실시간호가[실시간-015]

> [국내선물옵션] 실시간시세

[참고자료]

실시간시세(웹소켓) 파이썬 샘플코드는 한국투자증권 Github 참고 부탁드립니다.
https://github.com/koreainvestment/open-trading-api/blob/main/websocket/python/ws_domestic_overseas_all.py

실시간시세(웹소켓) API 사용방법에 대한 자세한 설명은 한국투자증권 Wikidocs 참고 부탁드립니다.
https://wikidocs.net/book/7847 (국내주식 업데이트 완료, 추후 해외주식·국내선물옵션 업데이트 예정)

[실시간-015] 지수옵션 실시간호가

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `ee7c4225-61e7-4d2d-b9ac-e8b00ccacdad` |
| **HTTP Method** | `POST` |
| **URL** | `/tryitout/H0IOASP0` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `ws://ops.koreainvestment.com:21000` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID** | `H0IOASP0`, `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2022-11-25
- **최종 수정일**: 2025-04-30

## 요청 (Request)

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `approval_key` | 웹소켓접속키 | String | 36 | Y | 실시간 (웹소켓) 접속키 발급 API(/oauth2/Approval)를 사용하여 발급받은 웹소켓 접속키 |
| `tr_type` | 등록/해제 | String | 1 | Y | "1: 등록, 2:해제" |
| `custtype` | 고객 타입 | String | 1 | Y | B : 법인 / P : 개인 |
| `content-type` | 컨텐츠타입 | String | 20 | Y | utf-8 |

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `tr_id` | 거래ID | String | 7 | Y | H0IOASP0 |
| `tr_key` | 코드 | String | 6 | Y | 예:201S11305 |

## 응답 (Response)

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `OPTN_SHRN_ISCD` | 옵션 단축 종목코드 | String | 16 | Y | '각 항목사이에는 구분자로 ^ 사용, 모든 데이터타입은 String으로 변환되어 push 처리됨' |
| `BSOP_HOUR` | 영업 시간 | String | 16 | Y |  |
| `OPTN_ASKP1` | 옵션 매도호가1 | String | 1 | Y |  |
| `OPTN_ASKP2` | 옵션 매도호가2 | String | 8 | Y |  |
| `OPTN_ASKP3` | 옵션 매도호가3 | String | 8 | Y |  |
| `OPTN_ASKP4` | 옵션 매도호가4 | String | 8 | Y |  |
| `OPTN_ASKP5` | 옵션 매도호가5 | String | 8 | Y |  |
| `OPTN_BIDP1` | 옵션 매수호가1 | String | 8 | Y |  |
| `OPTN_BIDP2` | 옵션 매수호가2 | String | 8 | Y |  |
| `OPTN_BIDP3` | 옵션 매수호가3 | String | 8 | Y |  |
| `OPTN_BIDP4` | 옵션 매수호가4 | String | 8 | Y |  |
| `OPTN_BIDP5` | 옵션 매수호가5 | String | 8 | Y |  |
| `ASKP_CSNU1` | 매도호가 건수1 | String | 8 | Y |  |
| `ASKP_CSNU2` | 매도호가 건수2 | String | 8 | Y |  |
| `ASKP_CSNU3` | 매도호가 건수3 | String | 8 | Y |  |
| `ASKP_CSNU4` | 매도호가 건수4 | String | 8 | Y |  |
| `ASKP_CSNU5` | 매도호가 건수5 | String | 8 | Y |  |
| `BIDP_CSNU1` | 매수호가 건수1 | String | 8 | Y |  |
| `BIDP_CSNU2` | 매수호가 건수2 | String | 8 | Y |  |
| `BIDP_CSNU3` | 매수호가 건수3 | String | 8 | Y |  |
| `BIDP_CSNU4` | 매수호가 건수4 | String | 8 | Y |  |
| `BIDP_CSNU5` | 매수호가 건수5 | String | 8 | Y |  |
| `ASKP_RSQN1` | 매도호가 잔량1 | String | 8 | Y |  |
| `ASKP_RSQN2` | 매도호가 잔량2 | String | 8 | Y |  |
| `ASKP_RSQN3` | 매도호가 잔량3 | String | 8 | Y |  |
| `ASKP_RSQN4` | 매도호가 잔량4 | String | 8 | Y |  |
| `ASKP_RSQN5` | 매도호가 잔량5 | String | 8 | Y |  |
| `BIDP_RSQN1` | 매수호가 잔량1 | String | 8 | Y |  |
| `BIDP_RSQN2` | 매수호가 잔량2 | String | 8 | Y |  |
| `BIDP_RSQN3` | 매수호가 잔량3 | String | 8 | Y |  |
| `BIDP_RSQN4` | 매수호가 잔량4 | String | 8 | Y |  |
| `BIDP_RSQN5` | 매수호가 잔량5 | String | 8 | Y |  |
| `TOTAL_ASKP_CSNU` | 총 매도호가 건수 | String | 8 | Y |  |
| `TOTAL_BIDP_CSNU` | 총 매수호가 건수 | String | 8 | Y |  |
| `TOTAL_ASKP_RSQN` | 총 매도호가 잔량 | String | 8 | Y |  |
| `TOTAL_BIDP_RSQN` | 총 매수호가 잔량 | String | 8 | Y |  |
| `TOTAL_ASKP_RSQN_ICDC` | 총 매도호가 잔량 증감 | String | 8 | Y |  |
| `TOTAL_BIDP_RSQN_ICDC` | 총 매수호가 잔량 증감 | String | 8 | Y |  |
