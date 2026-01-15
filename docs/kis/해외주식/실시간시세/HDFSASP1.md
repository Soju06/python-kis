# 해외주식 지연호가(아시아)[실시간-008]

> [해외주식] 실시간시세

해외주식 지연호가(아시아)의 경우 아시아 무료시세(지연호가)가 제공됩니다.

HTS(efriend Plus) [7781] 시세신청(실시간) 화면에서 유료 서비스 신청 시, 
"해외주식 실시간호가 HDFSASP0" 을 이용하여 아시아국가 유료시세(실시간호가)를 받아보실 수 있습니다. (24.11.29 반영)

※ 지연시세 지연시간 : 홍콩, 베트남, 중국, 일본 - 15분지연

[참고자료]

실시간시세(웹소켓) 파이썬 샘플코드는 한국투자증권 Github 참고 부탁드립니다.
https://github.com/koreainvestment/open-trading-api/blob/main/websocket/python/ws_domestic_overseas_all.py

실시간시세(웹소켓) API 사용방법에 대한 자세한 설명은 한국투자증권 Wikidocs 참고 부탁드립니다.
https://wikidocs.net/book/7847 (국내주식 업데이트 완료, 추후 해외주식·국내선물옵션 업데이트 예정)


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `22cadc7e-10e1-4b97-a0e0-f1f41b0b67ac` |
| **HTTP Method** | `POST` |
| **URL** | `/tryitout/HDFSASP1` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `ws://ops.koreainvestment.com:21000` |
| **모의 도메인** | `제공 안함` |
| **TR ID (실전)** | `HDFSASP1` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2022-09-05
- **최종 수정일**: 2025-06-11

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `approval_key` | 웹소켓 접속키 | String | 286 | Y | 실시간 (웹소켓) 접속키 발급 API(/oauth2/Approval)를 사용하여 발급받은 웹소켓 접속키 |
| `custtype` | 고객 타입 | String | 1 | Y | B : 법인 / P : 개인 |
| `tr_type` | 등록/해제 | String | 1 | Y | "1: 등록, 2:해제" |
| `content-type` | 컨텐츠타입 | String | 20 | Y | utf-8 |

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `tr_id` | 거래ID | String | 7 | Y | HDFSASP1 |
| `tr_key` | D거래소명종목코드 | String | 6 | Y | D+시장구분(3자리)+종목코드 예) DHKS00003 : D+HKS(홍콩)+00003(홍콩중화가스) [시장구분] TSE : 도쿄, HKS : 홍콩, SHS : 상해, SZS ... |

## 응답

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `RSYM` | 실시간종목코드 | String | 16 | Y | '각 항목사이에는 구분자로 ^ 사용, 모든 데이터타입은 String으로 변환되어 push 처리됨' |
| `SYMB` | 종목코드 | String | 16 | Y |  |
| `ZDIV` | 소수점자리수 | String | 1 | Y |  |
| `XYMD` | 현지일자 | String | 8 | Y |  |
| `XHMS` | 현지시간 | String | 6 | Y |  |
| `KYMD` | 한국일자 | String | 8 | Y |  |
| `KHMS` | 한국시간 | String | 6 | Y |  |
| `BVOL` | 매수총잔량 | String | 10 | Y |  |
| `AVOL` | 매도총잔량 | String | 10 | Y |  |
| `BDVL` | 매수총잔량대비 | String | 10 | Y |  |
| `ADVL` | 매도총잔량대비 | String | 10 | Y |  |
| `PBID1` | 매수호가1 | String | 12 | Y |  |
| `PASK1` | 매도호가1 | String | 12 | Y |  |
| `VBID1` | 매수잔량1 | String | 10 | Y |  |
| `VASK1` | 매도잔량1 | String | 10 | Y |  |
| `DBID1` | 매수잔량대비1 | String | 10 | Y |  |
| `DASK1` | 매도잔량대비1 | String | 10 | Y |  |

