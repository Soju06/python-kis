# 해외옵션 체결추이(틱) [해외선물-038]

> [해외선물옵션] 기본시세

해외옵션 체결추이(틱) API입니다. 
한 번의 호출에 40건까지 확인 가능하며, QRY_TP, INDEX_KEY 를 이용하여 다음조회 가능합니다.

※ 다음조회 방법
(처음조회) "QRY_TP":"Q", "QRY_CNT":"40", "INDEX_KEY":""
(다음조회) "QRY_TP":"P", "QRY_CNT":"40", "INDEX_KEY":"20240906       221"  ◀ 이전 호출의 "output1 > index_key" 기입

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
| **API ID** | `41290e2a-6e25-49c0-91a1-99b96ce53efe` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/overseas-futureoption/v1/quotations/opt-tick-ccnl` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `HHDFO55020200` |
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
| `tr_id` | 거래ID | String | 13 | Y | HHDFO55020200 |
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
| `SRS_CD` | 종목코드 | String | 32 | Y | ex) OESU24 C5500 ※ 종목코드 "포럼 > FAQ > 종목정보 다운로드(해외) - 해외지수옵션/해외주식옵션" 참고 |
| `EXCH_CD` | 거래소코드 | String | 10 | Y | 종목코드에 맞는 거래소 코드 ex) CME |
| `START_DATE_TIME` | 조회시작일시 | String | 12 | Y | "" 공란 입력 |
| `CLOSE_DATE_TIME` | 조회종료일시 | String | 12 | Y | "" 공란 입력 ※ 날짜 입력해도 처리 안됨 |
| `QRY_TP` | 조회구분 | String | 1 | Y | Q : 최초조회시 , P : 다음키(INDEX_KEY) 입력하여 조회시 |
| `QRY_CNT` | 요청개수 | String | 4 | Y | 예) 30 (최대 40) |
| `QRY_GAP` | 묶음개수 | String | 3 | Y | 공백 |
| `INDEX_KEY` | 이전조회KEY | String | 30 | Y | 다음조회(QRY_TP를 P로 입력) 시, 이전 호출의 "output1 > index_key" 기입하여 조회 |

### 요청 예시

```json
SRS_CD:OESU24 C5600
EXCH_CD:CME
START_DATE_TIME:
CLOSE_DATE_TIME:
QRY_TP:Q
QRY_CNT:30
QRY_GAP:
INDEX_KEY:
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
| `output1` | 응답상세 | String |   | Y |  |
| `ret_cnt` | 자료개수 | String | 4 | Y |  |
| `last_n_cnt` | N틱최종개수 | String | 4 | Y |  |
| `index_key` | 이전조회KEY | String | 30 | Y |  |
| `output2` | 응답상세 | Object |   | Y | array |
| `data_date` | 일자 | String | 8 | Y | 과거일자 ~ 최근일자 순으로 조회됨 |
| `data_time` | 시간 | String | 6 | Y | HHMMSS |
| `open_price` | 시가 | String | 15 | Y |  |
| `high_price` | 고가 | String | 15 | Y |  |
| `low_price` | 저가 | String | 15 | Y |  |
| `last_price` | 체결가격 | String | 15 | Y | 체결가격 ※ focode.mst, fostkcode.mst* 의 sCalcDesz(계산 소수점) 값 참고 * 포럼 > FAQ > 종목정보 다운로드(해외) - 해외지수옵션/해외... |
| `last_qntt` | 체결수량 | String | 10 | Y |  |
| `vol` | 누적거래수량 | String | 10 | Y |  |
| `prev_diff_flag` | 전일대비구분 | String | 1 | Y |  |
| `prev_diff_price` | 전일대비가격 | String | 15 | Y |  |
| `prev_diff_rate` | 전일대비율 | String | 10 | Y |  |

### 응답 예시

```json
{
    "output1": {
        "ret_cnt": "0030",
        "last_n_cnt": "0001",
        "index_key": "20240823       146"
    },
    "output2": [
        {
            "data_date": "20240824",
            "data_time": "024037",
            "open_price": "9900",
            "high_price": "9900",
            "low_price": "9900",
            "last_price": "9900",
            "last_qntt": "6",
            "vol": "343",
            "prev_diff_flag": "2",
            "prev_diff_price": "1700",
            "prev_diff_rate": "20.73"
        },
        {
            "data_date": "20240824",
            "data_time": "024417",
            "open_price": "10050",
            "high_price": "10050",
            "low_price": "10050",
            "last_price": "10050",
            "last_qntt": "6",
            "vol": "349",
            "prev_diff_flag": "2",
            "prev_diff_price": "1850",
            "prev_diff_rate": "22.56"
        },...
        {
            "data_date": "20240826",
            "data_time": "081707",
            "open_price": "10375",
            "high_price": "10375",
            "low_price": "10375",
            "last_price": "10375",
            "last_qntt": "1",
            "vol": "7",
            "prev_diff_flag": "5",
            "prev_diff_price": "-400",
            "prev_diff_rate": "-3.71"
        }
    ],
    "rt_cd": "0",
    "msg_cd": "MCA00000",
    "msg1": "정상처리 되었습니다."
}
```

