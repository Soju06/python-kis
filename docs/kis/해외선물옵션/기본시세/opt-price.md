# 해외옵션종목현재가 [해외선물-035]

> [해외선물옵션] 기본시세

해외옵션종목현재가 API입니다.

(중요) 해외옵션시세 출력값을 해석하실 때 focode.mst(해외지수옵션 종목마스터파일), fostkcode.mst(해외주식옵션 종목마스터파일)에 있는 sCalcDesz(계산 소수점) 값을 활용하셔야 정확한 값을 받아오실 수 있습니다.

- focode.mst(해외지수옵션 종목마스터파일), (해외주식옵션 종목마스터파일) 다운로드 방법
  1) focode.mst(해외지수옵션 종목마스터파일)
     : 포럼 > FAQ > 종목정보 다운로드(해외) - 해외지수옵션 클릭하여 다운로드 후
       Github의 헤더정보(https://github.com/koreainvestment/open-trading-api/blob/main/stocks_info/해외옵션정보.h)를 참고하여 해석
  2) fostkcode.mst(해외주식옵션 종목마스터파일)
     : 포럼 > FAQ > 종목정보 다운로드(해외) - 해외주식옵션 클릭하여 다운로드 후
       Github의 헤더정보(https://github.com/koreainvestment/open-trading-api/blob/main/stocks_info/해외주식옵션정보.h)를 참고하여 해석

- 소수점 계산 시, focode.mst(해외지수옵션 종목마스터파일), fostkcode.mst(해외주식옵션 종목마스터파일)의 sCalcDesz(계산 소수점) 값 참고
  EX) focode.mst 파일의 sCalcDesz(계산 소수점) 값
       품목코드 OES 계산소수점 -2 → 시세 7525 수신 시 75.25 로 해석
       품목코드 O6E 계산소수점 -4 → 시세 54.0 수신 시 0.0054 로 해석


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `621bdd34-a902-4117-98b8-57733197742a` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/overseas-futureoption/v1/quotations/opt-price` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `HHDFO55010000` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-08-23
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
| `tr_id` | 거래ID | String | 13 | Y | HHDFO55010000 |
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
| `SRS_CD` | 종목명 | String | 32 | Y | ex) OESU24 C5500 ※ 종목코드 "포럼 > FAQ > 종목정보 다운로드(해외) - 해외지수옵션/해외주식옵션" 참고 |

### 요청 예시

```json
SRS_CD:OGXX24 C19500
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
| `output1` | 응답상세 | String |  | Y |  |
| `proc_date` | 최종처리일자 | String | 8 | Y |  |
| `proc_time` | 최종처리시각 | String | 6 | Y |  |
| `open_price` | 시가 | String | 15 | Y |  |
| `high_price` | 고가 | String | 15 | Y |  |
| `low_price` | 저가 | String | 15 | Y |  |
| `last_price` | 현재가 | String | 15 | Y | 현재가 ※ focode.mst, fostkcode.mst* 의 sCalcDesz(계산 소수점) 값 참고 * 포럼 > FAQ > 종목정보 다운로드(해외) - 해외지수옵션/해외주식옵션 |
| `vol` | 누적거래수량 | String | 10 | Y |  |
| `prev_diff_flag` | 전일대비구분 | String | 1 | Y |  |
| `prev_diff_price` | 전일대비가격 | String | 15 | Y |  |
| `prev_diff_rate` | 전일대비율 | String | 10 | Y |  |
| `bid_qntt` | 매수1수량 | String | 10 | Y |  |
| `bid_price` | 매수1호가 | String | 15 | Y |  |
| `ask_qntt` | 매도1수량 | String | 10 | Y |  |
| `ask_price` | 매도1호가 | String | 15 | Y |  |
| `trst_mgn` | 증거금 | String | 19 | Y |  |
| `exch_cd` | 거래소코드 | String | 10 | Y |  |
| `crc_cd` | 거래통화 | String | 10 | Y |  |
| `trd_fr_date` | 상장일 | String | 8 | Y |  |
| `expr_date` | 만기일 | String | 8 | Y |  |
| `trd_to_date` | 최종거래일 | String | 8 | Y |  |
| `remn_cnt` | 잔존일수 | String | 4 | Y |  |
| `last_qntt` | 체결량 | String | 10 | Y |  |
| `tot_ask_qntt` | 총매도잔량 | String | 10 | Y |  |
| `tot_bid_qntt` | 총매수잔량 | String | 10 | Y |  |
| `tick_size` | 틱사이즈 | String | 19 | Y |  |
| `open_date` | 장개시일자 | String | 8 | Y |  |
| `open_time` | 장개시시각 | String | 6 | Y |  |
| `close_date` | 장종료일자 | String | 8 | Y |  |
| `close_time` | 장종료시각 | String | 6 | Y |  |
| `sbsnsdate` | 영업일자 | String | 8 | Y |  |
| `sttl_price` | 정산가 | String | 15 | N | 정산가 |

### 응답 예시

```json
{
  "output1": {
    "proc_date": "20241108",
    "proc_time": "173441",
    "open_price": "           84.0",
    "high_price": "           84.0",
    "low_price": "           83.0",
    "last_price": "           83.0",
    "vol": "         3",
    "prev_diff_flag": "5",
    "prev_diff_price": "           38.0",
    "prev_diff_rate": "    -31.40",
    "bid_qntt": "       275",
    "bid_price": "           83.0",
    "ask_qntt": "       425",
    "ask_price": "           87.0",
    "prev_price": "          121.0",
    "trst_mgn": "               4101",
    "exch_cd": "EUREX",
    "crc_cd": "EUR",
    "trd_fr_date": "20240816",
    "expr_date": "20240816",
    "trd_to_date": "20241115",
    "remn_cnt": "0008",
    "last_qntt": "         2",
    "tot_ask_qntt": "       952",
    "tot_bid_qntt": "       726",
    "tick_size": "                0.1",
    "open_date": "20241108",
    "open_time": "150000",
    "close_date": "20241109",
    "close_time": "013000",
    "sbsnsdate": "20241108",
    "sttl_price": "          102.2"
  },
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```

