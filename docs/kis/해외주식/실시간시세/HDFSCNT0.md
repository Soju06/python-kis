# 해외주식 실시간지연체결가[실시간-007]

> [해외주식] 실시간시세

해외주식 실시간지연체결가의 경우 기본적으로 무료시세(지연체결가)가 제공되며, 
아시아 국가의 경우 HTS(efriend Plus) [7781] 시세신청(실시간) 화면에서 유료 서비스 신청 시 API로도 유료시세(실시간체결가)를 받아보실 수 있습니다. (24.11.29 반영)

※ 지연시세 지연시간 : 미국 - 실시간무료(0분지연) / 홍콩, 베트남, 중국, 일본 - 15분지연 (중국은 실시간시세 신청 시 무료실시간시세 제공)
   미국의 경우 0분지연시세로 제공되나, 장중 당일 시가는 상이할 수 있으며, 익일 정정 표시됩니다.

해당 API로 미국주간거래(10:00~16:00) 시세 조회도 가능합니다. 
※ 미국주간거래 실시간 조회 시, 맨 앞자리(R), tr_key 중 시장구분 값을 다음과 같이 입력 → 나스닥: BAQ, 뉴욕: BAY, 아멕스: BAA

[참고자료]

실시간시세(웹소켓) 파이썬 샘플코드는 한국투자증권 Github 참고 부탁드립니다.
https://github.com/koreainvestment/open-trading-api/blob/main/websocket/python/ws_domestic_overseas_all.py

실시간시세(웹소켓) API 사용방법에 대한 자세한 설명은 한국투자증권 Wikidocs 참고 부탁드립니다.
https://wikidocs.net/book/7847 (국내주식 업데이트 완료, 추후 해외주식·국내선물옵션 업데이트 예정)

종목코드 마스터파일 파이썬 정제코드는 한국투자증권 Github 참고 부탁드립니다.
https://github.com/koreainvestment/open-trading-api/tree/main/stocks_info

[실시간-007] 해외주식 실시간지연체결통보

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `52290e93-e94c-4d2a-9ce3-c304681d3807` |
| **HTTP Method** | `POST` |
| **URL** | `/tryitout/HDFSCNT0` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `ws://ops.koreainvestment.com:21000` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `HDFSCNT0` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2022-09-05
- **최종 수정일**: 2025-07-29

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `approval_key` | 웹소켓 접속키 | String | 286 | Y | 실시간 (웹소켓) 접속키 발급 API(/oauth2/Approval)를 사용하여 발급받은 웹소켓 접속키 |
| `tr_type` | 등록/해제 | String | 1 | Y | 1: 등록, 2:해제 |
| `custtype` | 고객 타입 | String | 1 | Y | B : 법인 / P : 개인 |
| `content-type` | 컨텐츠타입 | String | 20 | Y | utf-8 |

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `tr_id` | 거래ID | String | 7 | Y | HDFSCNT0 |
| `tr_key` | D거래소명종목코드 | String | 6 | Y | D+시장구분(3자리)+종목코드 예) DNASAAPL : D+NAS(나스닥)+AAPL(애플) [시장구분] NYS : 뉴욕, NAS : 나스닥, AMS : 아멕스 , TSE : ... |

## 응답

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `RSYM` | 실시간종목코드 | String | 16 | Y | '각 항목사이에는 구분자로 ^ 사용, 모든 데이터타입은 String으로 변환되어 push 처리됨' |
| `SYMB` | 종목코드 | String | 16 | Y |  |
| `ZDIV` | 수수점자리수 | String | 1 | Y |  |
| `TYMD` | 현지영업일자 | String | 8 | Y |  |
| `XYMD` | 현지일자 | String | 6 | Y |  |
| `XHMS` | 현지시간 | String | 6 | Y |  |
| `KYMD` | 한국일자 | String | 6 | Y |  |
| `KHMS` | 한국시간 | String | 6 | Y |  |
| `OPEN` | 시가 | String | 6 | Y |  |
| `HIGH` | 고가 | String | 6 | Y |  |
| `LOW` | 저가 | String | 6 | Y |  |
| `LAST` | 현재가 | String | 6 | Y |  |
| `SIGN` | 대비구분 | String | 6 | Y |  |
| `DIFF` | 전일대비 | String | 8 | Y |  |
| `RATE` | 등락율 | String | 6 | Y |  |
| `PBID` | 매수호가 | String | 10 | Y |  |
| `PASK` | 매도호가 | String | 10 | Y |  |
| `VBID` | 매수잔량 | String | 10 | Y |  |
| `VASK` | 매도잔량 | String | 10 | Y |  |
| `EVOL` | 체결량 | String | 12 | Y |  |
| `TVOL` | 거래량 | String | 12 | Y |  |
| `TAMT` | 거래대금 | String | 10 | Y |  |
| `BIVL` | 매도체결량 | String | 10 | Y | 매수호가가 매도주문 수량을 따라가서 체결된것을 표현하여 BIVL 이라는 표현을 사용 |
| `ASVL` | 매수체결량 | String | 10 | Y | 매도호가가 매수주문 수량을 따라가서 체결된것을 표현하여 ASVL 이라는 표현을 사용 |
| `STRN` | 체결강도 | String | 10 | Y |  |
| `MTYP` | 시장구분 1:장중,2:장전,3:장후 | String | 10 | Y |  |

