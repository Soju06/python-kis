# 해외선물 분봉조회[해외선물-016]

> [해외선물옵션] 기본시세

해외선물분봉조회 API입니다. ★ 반드시 아래 호출방법을 확인하시고 호출 사용하시기 바랍니다.
한국투자 HTS(eFriend Force) > [5502] 해외선물옵션 체결추이 화면에서 "분" 선택 시 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.


※ 해외선물분봉조회 조회 방법
params
. START_DATE_TIME: 공란 입력 ("")
. CLOSE_DATE_TIME: 조회일자 입력 ("20231214")
. QRY_CNT: 120 입력 시, 가장 최근 분봉 120건 조회( 한번에 최대 120건 조회 가능)
                240 입력 시, 240 이전 분봉 ~ 120 이전 분봉 조회
                360 입력 시, 360 이전 분봉 ~ 240 이전 분봉 조회
. QRY_TP: 처음조회시, 공백 입력
              다음조회시, P 입력
. INDEX_KEY: 처음조회시, 공백 입력
                  다음조회시, 이전 조회 응답의 output2 > index_key 값 입력

* 따라서 분봉데이터를 기간별로 수집하고자 하실 경우 QRY_TP, INDEX_KEY 값을 이용하시면서 다음조회하시면 됩니다.

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

※ CME, SGX 거래소 API시세는 유료시세로 HTS/MTS에서 유료가입 후 익일부터 시세 이용 가능합니다.
포럼 > FAQ > 해외선물옵션 API 유료시세 신청방법(CME, SGX 거래소)

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `31d46ebe-2a19-4467-9dfb-a2d21adb1e61` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/overseas-futureoption/v1/quotations/inquire-time-futurechartprice` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID** | `모의투자 미지원`, `HHDFC55020400` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2023-10-20
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
| `tr_id` | 거래ID | String | 13 | Y | HHDFC55020400 |
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
| `SRS_CD` | 종목코드 | String | 32 | Y | ex) CNHU24 ※ 종목코드 "포럼 > FAQ > 종목정보 다운로드(해외) - 해외지수선물" 참고 |
| `EXCH_CD` | 거래소코드 | String | 10 | Y | CME |
| `START_DATE_TIME` | 조회시작일시 | String | 12 | Y | 공백 |
| `CLOSE_DATE_TIME` | 조회종료일시 | String | 12 | Y | ex) 20230823 |
| `QRY_TP` | 조회구분 | String | 1 | Y | Q : 최초조회시 , P : 다음키(INDEX_KEY) 입력하여 조회시 |
| `QRY_CNT` | 요청개수 | String | 4 | Y | 120 (조회갯수) |
| `QRY_GAP` | 묶음개수 | String | 3 | Y | 5 (분간격) |
| `INDEX_KEY` | 이전조회KEY | String | 30 | Y | 다음조회(QRY_TP를 P로 입력) 시, 이전 호출의 "output1 > index_key" 기입하여 조회 |

### 요청 예시

```json
SRS_CD:BRNQ24
EXCH_CD:ICE
START_DATE_TIME:
CLOSE_DATE_TIME:20231212
QRY_TP:P
QRY_CNT:500
QRY_GAP:1
INDEX_KEY:20231211       128
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
| `output2` | 응답상세 | String |   | Y |  |
| `ret_cnt` | 자료개수 | String | 4 | Y |  |
| `last_n_cnt` | N틱최종개수 | String | 4 | Y |  |
| `index_key` | 이전조회KEY | String | 30 | Y |  |
| `output1` | 응답상세 | Object |   | Y | array |
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
    "output2": {
        "ret_cnt": "0500",
        "last_n_cnt": "",
        "index_key": "20231208       246"
    },
    "output1": [
        {
            "data_date": "20231208",
            "data_time": "202100",
            "open_price": "75.41",
            "high_price": "75.41",
            "low_price": "75.41",
            "last_price": "75.41",
            "last_qntt": "5",
            "vol": "3985",
            "prev_diff_flag": "3",
            "prev_diff_price": "0",
            "prev_diff_rate": "0"
        },
        {
            "data_date": "20231208",
            "data_time": "202200",
            "open_price": "75.41",
            "high_price": "75.43",
            "low_price": "75.41",
            "last_price": "75.43",
            "last_qntt": "3",
            "vol": "3988",
            "prev_diff_flag": "2",
            "prev_diff_price": "0.02",
            "prev_diff_rate": "0.02652168"
        },
        {
            "data_date": "20231208",
            "data_time": "202300",
            "open_price": "75.45",
            "high_price": "75.45",
            "low_price": "75.45",
            "last_price": "75.45",
            "last_qntt": "19",
            "vol": "4007",
            "prev_diff_flag": "2",
            "prev_diff_price": "0.02",
            "prev_diff_rate": "0.02651464"
        },
        {
            "data_date": "20231208",
            "data_time": "202400",
            "open_price": "75.45",
            "high_price": "75.45",
            "low_price": "75.45",
            "last_price": "75.45",
            "last_qntt": "2",
            "vol": "4009",
            "prev_diff_flag": "3",
            "prev_diff_price": "0",
            "prev_diff_rate": "0"
        },
        {
            "data_date": "20231208",
            "data_time": "202600",
            "open_price": "75.45",
            "high_price": "75.47",
            "low_price": "75.45",
            "last_price": "75.47",
            "last_qntt": "4",
            "vol": "4013",
            "prev_diff_flag": "2",
            "prev_diff_price": "0.02",
            "prev_diff_rate": "0.02650762"
        },
        {
            "data_date": "20231208",
            "data_time": "202700",
            "open_price": "75.49",
            "high_price": "75.49",
            "low_price": "75.48",
            "last_price": "75.48",
            "last_qntt": "3",
            "vol": "4016",
            "prev_diff_flag": "2",
            "prev_diff_price": "0.01",
            "prev_diff_rate": "0.01325029"
        },
        {
            "data_date": "20231208",
            "data_time": "202800",
            "open_price": "75.45",
            "high_price": "75.46",
            "low_price": "75.45",
            "last_price": "75.46",
            "last_qntt": "3",
            "vol": "4019",
            "prev_diff_flag": "5",
            "prev_diff_price": "0.02",
            "prev_diff_rate": "-0.0264970"
        },
        {
            "data_date": "20231208",
            "data_time": "203100",
            "open_price": "75.46",
            "high_price": "75.46",
            "low_price": "75.46",
            "last_price": "75.46",
            "last_qntt": "1",
            "vol": "4020",
            "prev_diff_flag": "3",
            "prev_diff_price": "0",
            "prev_diff_rate": "0"
        },
        {
            "data_date": "20231208",
            "data_time": "203300",
            "open_price": "75.43",
            "high_price": "75.43",
            "low_price": "75.43",
            "last_price": "75.43",
            "last_qntt": "1",
            "vol": "4021",
            "prev_diff_flag": "5",
            "prev_diff_price": "0.03",
            "prev_diff_rate": "-0.0397561"
        },
        {
            "data_date": "20231208",
            "data_time": "203400",
            "open_price": "75.41",
            "high_price": "75.41",
            "low_price": "75.4",
            "last_price": "75.4",
            "last_qntt": "6",
            "vol": "4027",
            "prev_diff_flag": "5",
            "prev_diff_price": "0.03",
            "prev_diff_rate": "-0.0397719"
        },
        {
            "data_date": "20231208",
            "data_time": "203500",
            "open_price": "75.41",
            "high_price": "75.41",
            "low_price": "75.41",
            "last_price": "75.41",
            "last_qntt": "2",
            "vol": "4029",
            "prev_diff_flag": "2",
            "prev_diff_price": "0.01",
            "prev_diff_rate": "0.01326259"
        },
        {
            "data_date": "20231208",
            "data_time": "203700",
            "open_price": "75.43",
            "high_price": "75.43",
            "low_price": "75.41",
            "last_price": "75.41",
            "last_qntt": "30",
            "vol": "4060",
            "prev_diff_flag": "3",
            "prev_diff_price": "0",
            "prev_diff_rate": "0"
        },
        {
            "data_date": "20231208",
            "data_time": "204000",
            "open_price": "75.41",
            "high_price": "75.41",
            "low_price": "75.41",
            "last_price": "75.41",
            "last_qntt": "54",
            "vol": "4113",
            "prev_diff_flag": "3",
            "prev_diff_price": "0",
            "prev_diff_rate": "0"
        },
        {
            "data_date": "20231208",
            "data_time": "204200",
            "open_price": "75.37",
            "high_price": "75.38",
            "low_price": "75.37",
            "last_price": "75.38",
            "last_qntt": "2",
            "vol": "4118",
            "prev_diff_flag": "5",
            "prev_diff_price": "0.03",
            "prev_diff_rate": "-0.0397825"
        },...
    ],
    "rt_cd": "0",
    "msg_cd": "MCA00000",
    "msg1": "정상처리 되었습니다."
}
```
