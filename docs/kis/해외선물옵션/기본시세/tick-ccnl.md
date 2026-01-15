# 해외선물 체결추이(틱)[해외선물-019]

> [해외선물옵션] 기본시세

해외선물옵션 체결추이(틱) API입니다. 
한국투자 HTS(eFriend Force) > [5502] 해외선물옵션 체결추이 화면에서 "Tick" 선택 시 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

(중요) 해외선물시세 출력값을 해석하실 때 ffcode.mst(해외선물종목마스터 파일)에 있는 sCalcDesz(계산 소수점) 값을 활용하셔야 정확한 값을 받아오실 수 있습니다.

- ffcode.mst(해외선물종목마스터 파일) 다운로드 방법 2가지
  1) 한국투자증권 Github의 파이썬 샘플코드를 사용하여 mst 파일 다운로드 및 excel 파일로 정제   
     https://github.com/koreainvestment/open-trading-api/blob/main/stocks_info/overseas_future_code.py
   
  2) 혹은 포럼 - FAQ - 종목정보 다운로드(해외) - 해외지수선물 클릭하셔서 ffcode.mst(해외선물종목마스터 파일)을 다운로드 후
     Github의 헤더정보(https://github.com/koreainvestment/open-trading-api/blob/main/stocks_info/해외선물정보.h)를 참고하여 해석

- 소수점 계산 시, ffcode.mst(해외선물종목마스터 파일)의 sCalcDesz(계산 소수점) 값 참고
  EX) ffcode.mst 파일의 sCalcDesz(계산 소수점) 값
       품목코드 6A 계산소수점 -4 → 시세 6882.5 수신 시 0.68825 로 해석
       품목코드 GC 계산소수점 -1 → 시세 19225 수신 시 1922.5 로 해석

※ CME, SGX 거래소 API시세는 유료시세로 HTS/MTS에서 유료가입 후 익일부터 시세 이용 가능합니다.
포럼 > FAQ > 해외선물옵션 API 유료시세 신청방법(CME, SGX 거래소)

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `c7be7c01-6f43-4576-b1fd-84d0102ce4c3` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/overseas-futureoption/v1/quotations/tick-ccnl` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID** | `모의투자 미지원`, `HHDFC55020200` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-04-05
- **최종 수정일**: 2025-04-30

## 요청 (Request)

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials G... |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | HHDFC55020200 |
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
| `SRS_CD` | 종목코드 | String | 32 | Y | 예) 6AM24 |
| `EXCH_CD` | 거래소코드 | String | 10 | Y | 예) CME |
| `START_DATE_TIME` | 조회시작일시 | String | 12 | Y | 공백 |
| `CLOSE_DATE_TIME` | 조회종료일시 | String | 12 | Y | 예) 20240402 |
| `QRY_TP` | 조회구분 | String | 1 | Y | Q : 최초조회시 , P : 다음키(INDEX_KEY) 입력하여 조회시 |
| `QRY_CNT` | 요청개수 | String | 4 | Y | 예) 30 (최대 40) |
| `QRY_GAP` | 묶음개수 | String | 3 | Y | 공백 (분만 사용) |
| `INDEX_KEY` | 이전조회KEY | String | 30 | Y | 공백 |

### 요청 예시

```json
SRS_CD:6AM24
EXCH_CD:CME
START_DATE_TIME:
CLOSE_DATE_TIME:20240423
QRY_TP:Q
QRY_CNT:40
QRY_GAP:
INDEX_KEY:
```

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
| `tret_cnt` | 자료개수 | String | 4 | Y |  |
| `last_n_cnt` | N틱최종개수 | String | 4 | Y |  |
| `index_key` | 이전조회KEY | String | 30 | Y |  |
| `output2` | 응답상세 | Object |   | Y | array |
| `data_date` | 일자 | String | 8 | Y |  |
| `data_time` | 시각 | String | 6 | Y |  |
| `open_price` | 시가 | String | 15 | Y |  |
| `high_price` | 고가 | String | 15 | Y |  |
| `low_price` | 저가 | String | 15 | Y |  |
| `last_price` | 체결가격 | String | 15 | Y | 체결가격 ※ ffcode.mst(해외선물종목마스터 파일)의 sCalcDesz(계산 소수점) 값 참고 |
| `last_qntt` | 체결수량 | String | 10 | Y |  |
| `vol` | 누적거래수량 | String | 10 | Y |  |
| `prev_diff_flag` | 전일대비구분 | String | 1 | Y |  |
| `prev_diff_price` | 전일대비가격 | String | 15 | Y |  |
| `prev_diff_rate` | 전일대비율 | String | 10 | Y |  |

### 응답 예시

```json
{
  "output1": {
    "ret_cnt": "0040",
    "last_n_cnt": "0001",
    "index_key": "20240423      6445"
  },
  "output2": [
    {
      "data_date": "20240423",
      "data_time": "164434",
      "open_price": "         6464.5",
      "high_price": "         6464.5",
      "low_price": "         6464.5",
      "last_price": "         6464.5",
      "last_qntt": "         4",
      "vol": "27806",
      "prev_diff_flag": "2",
      "prev_diff_price": "            4.5",
      "prev_diff_rate": "      0.07"
    },
    {
      "data_date": "20240423",
      "data_time": "164434",
      "open_price": "         6464.5",
      "high_price": "         6464.5",
      "low_price": "         6464.5",
      "last_price": "         6464.5",
      "last_qntt": "         1",
      "vol": "27807",
      "prev_diff_flag": "2",
      "prev_diff_price": "            4.5",
      "prev_diff_rate": "      0.07"
    },
    {
      "data_date": "20240423",
      "data_time": "164450",
      "open_price": "         6464.5",
      "high_price": "         6464.5",
      "low_price": "         6464.5",
      "last_price": "         6464.5",
      "last_qntt": "         5",
      "vol": "27812",
      "prev_diff_flag": "2",
      "prev_diff_price": "            4.5",
      "prev_diff_rate": "      0.07"
    },
    {
      "data_date": "20240423",
      "data_time": "164501",
      "open_price": "         6464.5",
      "high_price": "         6464.5",
      "low_price": "         6464.5",
      "last_price": "         6464.5",
      "last_qntt": "         2",
      "vol": "27814",
      "prev_diff_flag": "2",
      "prev_diff_price": "            4.5",
      "prev_diff_rate": "      0.07"
    },
    {
      "data_date": "20240423",
      "data_time": "164503",
      "open_price": "         6464.5",
      "high_price": "         6464.5",
      "low_price": "         6464.5",
      "last_price": "         6464.5",
      "last_qntt": "         9",
      "vol": "27823",
      "prev_diff_flag": "2",
      "prev_diff_price": "            4.5",
      "prev_diff_rate": "      0.07"
    },
    {
      "data_date": "20240423",
      "data_time": "164503",
      "open_price": "         6464.5",
      "high_price": "         6464.5",
      "low_price": "         6464.5",
      "last_price": "         6464.5",
      "last_qntt": "         1",
      "vol": "27824",
      "prev_diff_flag": "2",
      "prev_diff_price": "            4.5",
      "prev_diff_rate": "      0.07"
    },
    {
      "data_date": "20240423",
      "data_time": "164507",
      "open_price": "         6464.5",
      "high_price": "         6464.5",
      "low_price": "         6464.5",
      "last_price": "         6464.5",
      "last_qntt": "         1",
      "vol": "27825",
      "prev_diff_flag": "2",
      "prev_diff_price": "            4.5",
      "prev_diff_rate": "      0.07"
    },
    {
      "data_date": "20240423",
      "data_time": "164517",
      "open_price": "         6464.5",
      "high_price": "         6464.5",
      "low_price": "         6464.5",
      "last_price": "         6464.5",
      "last_qntt": "         1",
      "vol": "27826",
      "prev_diff_flag": "2",
      "prev_diff_price": "            4.5",
      "prev_diff_rate": "      0.07"
    },
    {
      "data_date": "20240423",
      "data_time": "164517",
      "open_price": "         6464.5",
      "high_price": "         6464.5",
      "low_price": "         6464.5",
      "last_price": "         6464.5",
      "last_qntt": "         2",
      "vol": "27828",
      "prev_diff_flag": "2",
      "prev_diff_price": "            4.5",
      "prev_diff_rate": "      0.07"
    },
    {
      "data_date": "20240423",
      "data_time": "164526",
      "open_price": "           6465",
      "high_price": "           6465",
      "low_price": "           6465",
      "last_price": "           6465",
      "last_qntt": "         2",
      "vol": "27830",
      "prev_diff_flag": "2",
      "prev_diff_price": "              5",
      "prev_diff_rate": "      0.08"
    },
    {
      "data_date": "20240423",
      "data_time": "164542",
      "open_price": "         6464.5",
      "high_price": "         6464.5",
      "low_price": "         6464.5",
      "last_price": "         6464.5",
      "last_qntt": "         1",
      "vol": "27831",
      "prev_diff_flag": "2",
      "prev_diff_price": "            4.5",
      "prev_diff_rate": "      0.07"
    },
    {
      "data_date": "20240423",
      "data_time": "164551",
      "open_price": "           6464",
      "high_price": "           6464",
      "low_price": "           6464",
      "last_price": "           6464",
      "last_qntt": "         1",
      "vol": "27832",
      "prev_diff_flag": "2",
      "prev_diff_price": "              4",
      "prev_diff_rate": "      0.06"
    },
    {
      "data_date": "20240423",
      "data_time": "164555",
      "open_price": "         6463.5",
      "high_price": "         6463.5",
      "low_price": "         6463.5",
      "last_price": "         6463.5",
      "last_qntt": "         1",
      "vol": "27833",
      "prev_diff_flag": "2",
      "prev_diff_price": "            3.5",
      "prev_diff_rate": "      0.05"
    },
    {
      "data_date": "20240423",
      "data_time": "164611",
      "open_price": "           6463",
      "high_price": "           6463",
      "low_price": "           6463",
      "last_price": "           6463",
      "last_qntt": "         1",
      "vol": "27834",
      "prev_diff_flag": "2",
      "prev_diff_price": "              3",
      "prev_diff_rate": "      0.05"
    },
    {
      "data_date": "20240423",
      "data_time": "164613",
      "open_price": "           6463",
      "high_price": "           6463",
      "low_price": "           6463",
      "last_price": "           6463",
      "last_qntt": "         1",
      "vol": "27835",
      "prev_diff_flag": "2",
      "prev_diff_price": "              3",
      "prev_diff_rate": "      0.05"
    },
    {
      "data_date": "20240423",
      "data_time": "164620",
      "open_price": "           6463",
      "high_price": "           6463",
      "low_price": "           6463",
      "last_price": "           6463",
      "last_qntt": "         2",
      "vol": "27837",
      "prev_diff_flag": "2",
      "prev_diff_price": "              3",
      "prev_diff_rate": "      0.05"
    },
    {
      "data_date": "20240423",
      "data_time": "164620",
      "open_price": "           6463",
      "high_price": "           6463",
      "low_price": "           6463",
      "last_price": "           6463",
      "last_qntt": "         1",
      "vol": "27838",
      "prev_diff_flag": "2",
      "prev_diff_price": "              3",
      "prev_diff_rate": "      0.05"
    },
    {
      "data_date": "20240423",
      "data_time": "164634",
      "open_price": "         6463.5",
      "high_price": "         6463.5",
      "low_price": "         6463.5",
      "last_price": "         6463.5",
      "last_qntt": "        10",
      "vol": "27848",
      "prev_diff_flag": "2",
      "prev_diff_price": "            3.5",
      "prev_diff_rate": "      0.05"
    },
    {
      "data_date": "20240423",
      "data_time": "164634",
      "open_price": "         6463.5",
      "high_price": "         6463.5",
      "low_price": "         6463.5",
      "last_price": "         6463.5",
      "last_qntt": "         1",
      "vol": "27849",
      "prev_diff_flag": "2",
      "prev_diff_price": "            3.5",
      "prev_diff_rate": "      0.05"
    },
    {
      "data_date": "20240423",
      "data_time": "164634",
      "open_price": "         6463.5",
      "high_price": "         6463.5",
      "low_price": "         6463.5",
      "last_price": "         6463.5",
      "last_qntt": "         1",
      "vol": "27850",
      "prev_diff_flag": "2",
      "prev_diff_price": "            3.5",
      "prev_diff_rate": "      0.05"
    },
    {
      "data_date": "20240423",
      "data_time": "164634",
      "open_price": "         6463.5",
      "high_price": "         6463.5",
      "low_price": "         6463.5",
      "last_price": "         6463.5",
      "last_qntt": "        25",
      "vol": "27875",
      "prev_diff_flag": "2",
      "prev_diff_price": "            3.5",
      "prev_diff_rate": "      0.05"
    },
    {
      "data_date": "20240423",
      "data_time": "164634",
      "open_price": "           6464",
      "high_price": "           6464",
      "low_price": "           6464",
      "last_price": "           6464",
      "last_qntt": "         5",
      "vol": "27880",
      "prev_diff_flag": "2",
      "prev_diff_price": "              4",
      "prev_diff_rate": "      0.06"
    },
    {
      "data_date": "20240423",
      "data_time": "164650",
      "open_price": "           6464",
      "high_price": "           6464",
      "low_price": "           6464",
      "last_price": "           6464",
      "last_qntt": "         2",
      "vol": "27882",
      "prev_diff_flag": "2",
      "prev_diff_price": "              4",
      "prev_diff_rate": "      0.06"
    },
    {
      "data_date": "20240423",
      "data_time": "164658",
      "open_price": "           6464",
      "high_price": "           6464",
      "low_price": "           6464",
      "last_price": "           6464",
      "last_qntt": "       400",
      "vol": "28282",
      "prev_diff_flag": "2",
      "prev_diff_price": "              4",
      "prev_diff_rate": "      0.06"
    },
    {
      "data_date": "20240423",
      "data_time": "164658",
      "open_price": "           6464",
      "high_price": "           6464",
      "low_price": "           6464",
      "last_price": "           6464",
      "last_qntt": "         3",
      "vol": "28285",
      "prev_diff_flag": "2",
      "prev_diff_price": "              4",
      "prev_diff_rate": "      0.06"
    },
    {
      "data_date": "20240423",
      "data_time": "164707",
      "open_price": "         6464.5",
      "high_price": "         6464.5",
      "low_price": "         6464.5",
      "last_price": "         6464.5",
      "last_qntt": "         2",
      "vol": "28287",
      "prev_diff_flag": "2",
      "prev_diff_price": "            4.5",
      "prev_diff_rate": "      0.07"
    },
    {
      "data_date": "20240423",
      "data_time": "164714",
      "open_price": "         6464.5",
      "high_price": "         6464.5",
      "low_price": "         6464.5",
      "last_price": "         6464.5",
      "last_qntt": "         1",
      "vol": "28288",
      "prev_diff_flag": "2",
      "prev_diff_price": "            4.5",
      "prev_diff_rate": "      0.07"
    },
    {
      "data_date": "20240423",
      "data_time": "164714",
      "open_price": "         6464.5",
      "high_price": "         6464.5",
      "low_price": "         6464.5",
      "last_price": "         6464.5",
      "last_qntt": "         2",
      "vol": "28290",
      "prev_diff_flag": "2",
      "prev_diff_price": "            4.5",
      "prev_diff_rate": "      0.07"
    },
    {
      "data_date": "20240423",
      "data_time": "164715",
      "open_price": "         6464.5",
      "high_price": "         6464.5",
      "low_price": "         6464.5",
      "last_price": "         6464.5",
      "last_qntt": "         4",
      "vol": "28294",
      "prev_diff_flag": "2",
      "prev_diff_price": "            4.5",
      "prev_diff_rate": "      0.07"
    },
    {
      "data_date": "20240423",
      "data_time": "164716",
      "open_price": "         6464.5",
      "high_price": "         6464.5",
      "low_price": "         6464.5",
      "last_price": "         6464.5",
      "last_qntt": "       315",
      "vol": "28609",
      "prev_diff_flag": "2",
      "prev_diff_price": "            4.5",
      "prev_diff_rate": "      0.07"
    },
    {
      "data_date": "20240423",
      "data_time": "164735",
      "open_price": "         6464.5",
      "high_price": "         6464.5",
      "low_price": "         6464.5",
      "last_price": "         6464.5",
      "last_qntt": "         2",
      "vol": "28611",
      "prev_diff_flag": "2",
      "prev_diff_price": "            4.5",
      "prev_diff_rate": "      0.07"
    },
    {
      "data_date": "20240423",
      "data_time": "164735",
      "open_price": "         6464.5",
      "high_price": "         6464.5",
      "low_price": "         6464.5",
      "last_price": "         6464.5",
      "last_qntt": "         3",
      "vol": "28614",
      "prev_diff_flag": "2",
      "prev_diff_price": "            4.5",
      "prev_diff_rate": "      0.07"
    },
    {
      "data_date": "20240423",
      "data_time": "164817",
      "open_price": "           6464",
      "high_price": "           6464",
      "low_price": "           6464",
      "last_price": "           6464",
      "last_qntt": "         7",
      "vol": "28621",
      "prev_diff_flag": "2",
      "prev_diff_price": "              4",
      "prev_diff_rate": "      0.06"
    },
    {
      "data_date": "20240423",
      "data_time": "164828",
      "open_price": "         6463.5",
      "high_price": "         6463.5",
      "low_price": "         6463.5",
      "last_price": "         6463.5",
      "last_qntt": "         2",
      "vol": "28623",
      "prev_diff_flag": "2",
      "prev_diff_price": "            3.5",
      "prev_diff_rate": "      0.05"
    },
    {
      "data_date": "20240423",
      "data_time": "164837",
      "open_price": "           6463",
      "high_price": "           6463",
      "low_price": "           6463",
      "last_price": "           6463",
      "last_qntt": "         1",
      "vol": "28624",
      "prev_diff_flag": "2",
      "prev_diff_price": "              3",
      "prev_diff_rate": "      0.05"
    },
    {
      "data_date": "20240423",
      "data_time": "164838",
      "open_price": "           6463",
      "high_price": "           6463",
      "low_price": "           6463",
      "last_price": "           6463",
      "last_qntt": "         1",
      "vol": "28625",
      "prev_diff_flag": "2",
      "prev_diff_price": "              3",
      "prev_diff_rate": "      0.05"
    },
    {
      "data_date": "20240423",
      "data_time": "164856",
      "open_price": "         6462.5",
      "high_price": "         6462.5",
      "low_price": "         6462.5",
      "last_price": "         6462.5",
      "last_qntt": "         2",
      "vol": "28627",
      "prev_diff_flag": "2",
      "prev_diff_price": "            2.5",
      "prev_diff_rate": "      0.04"
    },
    {
      "data_date": "20240423",
      "data_time": "164856",
      "open_price": "         6462.5",
      "high_price": "         6462.5",
      "low_price": "         6462.5",
      "last_price": "         6462.5",
      "last_qntt": "         5",
      "vol": "28632",
      "prev_diff_flag": "2",
      "prev_diff_price": "            2.5",
      "prev_diff_rate": "      0.04"
    },
    {
      "data_date": "20240423",
      "data_time": "164856",
      "open_price": "         6462.5",
      "high_price": "         6462.5",
      "low_price": "         6462.5",
      "last_price": "         6462.5",
      "last_qntt": "        10",
      "vol": "28642",
      "prev_diff_flag": "2",
      "prev_diff_price": "            2.5",
      "prev_diff_rate": "      0.04"
    },
    {
      "data_date": "20240423",
      "data_time": "164856",
      "open_price": "         6462.5",
      "high_price": "         6462.5",
      "low_price": "         6462.5",
      "last_price": "         6462.5",
      "last_qntt": "         2",
      "vol": "28644",
      "prev_diff_flag": "2",
      "prev_diff_price": "            2.5",
      "prev_diff_rate": "      0.04"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```
