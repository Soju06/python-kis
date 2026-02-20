# 해외선물옵션 실시간체결가[실시간-017]

> [해외선물옵션]실시간시세

※ CME, SGX 실시간시세 유료시세 신청 필수 (포럼 > FAQ > 해외선물옵션 API 유료시세 신청방법(CME, SGX 거래소))
- CME, SGX 거래소 실시간시세는 유료시세 신청 후 이용하시는 모든 계좌에 대해서 접근토큰발급 API 호출하셔야 하며, 
  접근토큰발급 이후 2시간 이내로 신청정보가 동기화되어 유료시세 수신이 가능해집니다.
- CME, SGX 거래소 종목은 유료시세 신청되어 있지 않으면 실시간시세 종목등록이 불가하며, 
  등록 시도 시 "SUBSCRIBE ERROR : mci send failed" 에러가 발생합니다.


(중요) 해외선물옵션시세 출력값을 해석하실 때 ffcode.mst(해외선물종목마스터 파일)에 있는 sCalcDesz(계산 소수점) 값을 활용하셔야 정확한 값을 받아오실 수 있습니다.

- ffcode.mst(해외선물종목마스터 파일) 다운로드 방법 2가지
  1) 한국투자증권 Github의 파이썬 샘플코드를 사용하여 mst 파일 다운로드 및 excel 파일로 정제   
     https://github.com/koreainvestment/open-trading-api/blob/main/stocks_info/overseas_future_code.py
   
  2) 혹은 포럼 - FAQ - 종목정보 다운로드 - 해외선물옵션 클릭하셔서 ffcode.mst(해외선물종목마스터 파일)을 다운로드 후
     Github의 헤더정보(https://github.com/koreainvestment/open-trading-api/blob/main/stocks_info/해외선물옵션정보.h)를 참고하여 해석

- 소수점 계산 시, ffcode.mst(해외선물종목마스터 파일)의 sCalcDesz(계산 소수점) 값 참고
  EX) ffcode.mst 파일의 sCalcDesz(계산 소수점) 값
       품목코드 6A 계산소수점 -4 → 시세 6882.5 수신 시 0.68825 로 해석
       품목코드 GC 계산소수점 -1 → 시세 19225 수신 시 1922.5 로 해석


[참고자료]

실시간시세(웹소켓) 파이썬 샘플코드는 한국투자증권 Github 참고 부탁드립니다.
https://github.com/koreainvestment/open-trading-api/blob/main/websocket/python/ws_domestic_overseas_all.py

실시간시세(웹소켓) API 사용방법에 대한 자세한 설명은 한국투자증권 Wikidocs 참고 부탁드립니다.
https://wikidocs.net/book/7847 (국내주식 업데이트 완료, 추후 해외주식·국내선물옵션 업데이트 예정)

종목코드 마스터파일 파이썬 정제코드는 한국투자증권 Github 참고 부탁드립니다.
https://github.com/koreainvestment/open-trading-api/tree/main/stocks_info

해외선물옵션체결[실시간-017]

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `f30d6f30-54f2-480c-bf7a-3e4086fa71b0` |
| **HTTP Method** | `POST` |
| **URL** | `/tryitout/HDFFF020` |
| **Content-Type** | `utf-8` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `ws://ops.koreainvestment.com:21000` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `HDFFF020` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2022-12-27T12:36:01+09:00
- **최종 수정일**: 2025-04-30T13:21:39+09:00

## 요청

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
| `tr_id` | 거래ID | String | 7 | Y | HDFFF020 |
| `tr_key` | 종목코드 | String | 6 | Y | 종목코드  ※ CME, SGX 실시간시세 유료시세 신청 필수  "포럼 > FAQ > 해외선물옵션 API 유료시세 신청방법(CME, SGX 거래소)" |

## 응답

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `SERIES_CD` | 종목코드 | String | 32 | Y | '각 항목사이에는 구분자로 ^ 사용, 모든 데이터타입은 String으로 변환되어 push 처리됨' |
| `BSNS_DATE` | 영업일자 | String | 8 | Y |  |
| `MRKT_OPEN_DATE` | 장개시일자 | String | 8 | Y |  |
| `MRKT_OPEN_TIME` | 장개시시각 | String | 6 | Y |  |
| `MRKT_CLOSE_DATE` | 장종료일자 | String | 8 | Y |  |
| `MRKT_CLOSE_TIME` | 장종료시각 | String | 6 | Y |  |
| `PREV_PRICE` | 전일종가 | String | 15 | Y | 전일종가, 체결가격, 전일대비가, 시가, 고가, 저가 ※ ffcode.mst(해외선물종목마스터 파일)의 sCalcDesz(계산 소수점) 값 참고 |
| `RECV_DATE` | 수신일자 | String | 8 | Y |  |
| `RECV_TIME` | 수신시각 | String | 6 | Y | 수신시각(recv_time) = 실제 체결시각 |
| `ACTIVE_FLAG` | 본장_전산장구분 | String | 1 | Y |  |
| `LAST_PRICE` | 체결가격 | String | 15 | Y |  |
| `LAST_QNTT` | 체결수량 | String | 10 | Y |  |
| `PREV_DIFF_PRICE` | 전일대비가 | String | 15 | Y |  |
| `PREV_DIFF_RATE` | 등락률 | String | 10 | Y |  |
| `OPEN_PRICE` | 시가 | String | 15 | Y |  |
| `HIGH_PRICE` | 고가 | String | 15 | Y |  |
| `LOW_PRICE` | 저가 | String | 15 | Y |  |
| `VOL` | 누적거래량 | String | 10 | Y |  |
| `PREV_SIGN` | 전일대비부호 | String | 1 | Y |  |
| `QUOTSIGN` | 체결구분 | String | 1 | Y | 2:매수체결 5:매도체결 |
| `RECV_TIME2` | 수신시각2 만분의일초 | String | 4 | Y |  |
| `PSTTL_PRICE` | 전일정산가 | String | 15 | Y |  |
| `PSTTL_SIGN` | 전일정산가대비 | String | 1 | Y |  |
| `PSTTL_DIFF_PRICE` | 전일정산가대비가격 | String | 15 | Y |  |
| `PSTTL_DIFF_RATE` | 전일정산가대비율 | String | 10 | Y |  |

