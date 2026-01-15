# 해외선물종목현재가 [v1_해외선물-009]

> [해외선물옵션] 기본시세

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


[참고자료]
※ 종목코드 마스터파일 파이썬 정제코드는 한국투자증권 Github 참고 부탁드립니다.
   https://github.com/koreainvestment/open-trading-api/tree/main/stocks_info
   
※ 모의투자는 실전투자계좌를 활용하여 조회 부탁드립니다.

※ CME, SGX 거래소 API시세는 유료시세로 HTS/MTS에서 유료가입 후 익일부터 시세 이용 가능합니다.
포럼 > FAQ > 해외선물옵션 API 유료시세 신청방법(CME, SGX 거래소)

해외선물종목현재가 [v1_해외선물-009]

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `3d3ad086-7c1b-41cb-9b76-ba05ccf6ba95` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/overseas-futureoption/v1/quotations/inquire-price` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `HHDFC55010000` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2022-09-02
- **최종 수정일**: 2025-04-30

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials G... |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | HHDFC55010000 |
| `tr_cont` | 연속 거래 여부 | String | 1 | N | tr_cont를 이용한 다음조회 불가 API |
| `custtype` | 고객 타입 | String | 1 | Y | B : 법인 / P : 개인 |
| `seq_no` | 일련번호 | String | 2 | N | 법인 : "001" / default   개인: "" |
| `mac_address` | 맥주소 | String | 12 | N | 법인고객 혹은 개인고객의 Mac address 값 |
| `phone_number` | 핸드폰번호 | String | 12 | N | [법인 필수] 제휴사APP을 사용하는 경우 사용자(회원) 핸드폰번호  ex) 01011112222 (하이픈 등 구분값 제거) |
| `ip_addr` | 접속 단말 공인 IP | String | 12 | N | [법인 필수] 사용자(회원)의 IP Address |
| `gt_uid` | Global UID | String | 32 | N | [법인 전용] 거래고유번호로 사용하므로 거래별로 UNIQUE해야 함 |

### Body

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `SRS_CD` | 종목코드 | String | 32 | Y | ex) CNHU24 ※ 종목코드 "포럼 > FAQ > 종목정보 다운로드(해외) - 해외지수선물" 참고 |

### 요청 예시

```json
SRS_CD:BRNF25
```

## 응답

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
| `output1` | 응답상세1 | String |  | N |  |
| `proc_date` | 최종처리일자 | String | 8 | N | 최종처리일자 |
| `high_price` | 고가 | String | 15 | N | 고가 ※ ffcode.mst(해외선물종목마스터 파일)의 sCalcDesz(계산 소수점) 값 참고 |
| `proc_time` | 최종처리시각 | String | 6 | N | 최종처리시각 |
| `open_price` | 시가 | String | 15 | N | 시가 ※ ffcode.mst(해외선물종목마스터 파일)의 sCalcDesz(계산 소수점) 값 참고 |
| `trst_mgn` | 증거금 | String | 19 | N | 증거금 |
| `low_price` | 저가 | String | 15 | N | 저가 ※ ffcode.mst(해외선물종목마스터 파일)의 sCalcDesz(계산 소수점) 값 참고 |
| `last_price` | 현재가 | String | 15 | N | 현재가 ※ ffcode.mst(해외선물종목마스터 파일)의 sCalcDesz(계산 소수점) 값 참고 |
| `vol` | 누적거래수량 | String | 10 | N | 누적거래수량 |
| `prev_diff_flag` | 전일대비구분 | String | 1 | N | 전일대비구분 '1':상한 '2':상승 '3':보합 '4':하한 '5':하락 |
| `prev_diff_price` | 전일대비가격 | String | 15 | N | 전일대비가격 |
| `prev_diff_rate` | 전일대비율 | String | 10 | N | 전일대비율 |
| `bid_qntt` | 매수1수량 | String | 10 | N | 매수1수량 |
| `bid_price` | 매수1호가 | String | 15 | N | 매수1호가 ※ ffcode.mst(해외선물종목마스터 파일)의 sCalcDesz(계산 소수점) 값 참고 |
| `ask_qntt` | 매도1수량 | String | 10 | N | 매도1수량 |
| `ask_price` | 매도1호가 | String | 15 | N | 매도1호가 ※ ffcode.mst(해외선물종목마스터 파일)의 sCalcDesz(계산 소수점) 값 참고 |
| `prev_price` | 전일종가 | String | 15 | N | 전일종가 ※ ffcode.mst(해외선물종목마스터 파일)의 sCalcDesz(계산 소수점) 값 참고 |
| `exch_cd` | 거래소코드 | String | 10 | N | 거래소코드 |
| `crc_cd` | 거래통화 | String | 10 | N | 거래통화 |
| `trd_fr_date` | 상장일 | String | 8 | N | 상장일 |
| `expr_date` | 만기일 | String | 8 | N | 만기일 |
| `trd_to_date` | 최종거래일 | String | 8 | N | 최종거래일 |
| `remn_cnt` | 잔존일수 | String | 4 | N | 잔존일수 |
| `last_qntt` | 체결량 | String | 10 | N | 체결량 |
| `tot_ask_qntt` | 총매도잔량 | String | 10 | N | 총매도잔량 |
| `tot_bid_qntt` | 총매수잔량 | String | 10 | N | 총매수잔량 |
| `tick_size` | 틱사이즈 | String | 19 | N | 틱사이즈 |
| `open_date` | 장개시일자 | String | 8 | N | 장개시일자 |
| `open_time` | 장개시시각 | String | 6 | N | 장개시시각 |
| `close_date` | 장종료일자 | String | 8 | N | 장종료일자 |
| `close_time` | 장종료시각 | String | 6 | N | 장종료시각 |
| `sbsnsdate` | 영업일자 | String | 8 | N | 영업일자 |
| `sttl_price` | 정산가 | String | 15 | N | 정산가 |

### 응답 예시

```json
{
  "output1": {
    "proc_date": "20241108",
    "proc_time": "173937",
    "open_price": "          75.55",
    "high_price": "          75.61",
    "low_price": "          74.66",
    "last_price": "          74.90",
    "vol": "33004",
    "prev_diff_flag": "5",
    "prev_diff_price": "           0.67",
    "prev_diff_rate": "     -0.89",
    "bid_qntt": "         7",
    "bid_price": "          74.89",
    "ask_qntt": "         4",
    "ask_price": "          74.90",
    "prev_price": "          75.57",
    "trst_mgn": "               3670",
    "exch_cd": "ICE",
    "crc_cd": "USD",
    "trd_fr_date": "20180110",
    "expr_date": "20241129",
    "trd_to_date": "20241129",
    "remn_cnt": "  22",
    "last_qntt": "1",
    "tot_ask_qntt": "       115",
    "tot_bid_qntt": "       157",
    "tick_size": "               0.01",
    "open_date": "20241108",
    "open_time": "100000",
    "close_date": "20241109",
    "close_time": "080000",
    "sbsnsdate": "20241108",
    "sttl_price": "  75.6300000000"
  },
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```

