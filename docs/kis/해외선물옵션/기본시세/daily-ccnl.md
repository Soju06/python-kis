# 해외선물 체결추이(일간)[해외선물-018]

> [해외선물옵션] 기본시세

해외선물옵션 체결추이(일간) API입니다. 
한국투자 HTS(eFriend Force) > [5502] 해외선물옵션 체결추이 화면에서 "일간" 선택 시 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

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
| **API ID** | `8c473311-ecfd-428f-9ec2-0b574d8592b9` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/overseas-futureoption/v1/quotations/daily-ccnl` |
| **Content-Type** | `` |
| **요청 포맷** | `` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID** | `HHDFC55020100`, `모의투자 미지원` |

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
| `tr_id` | 거래ID | String | 13 | Y | HHDFC55020100 |
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
CLOSE_DATE_TIME:20240424
QRY_TP:
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
| `last_price` | 체결가격 | String | 15 | Y |  |
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
    "last_n_cnt": "",
    "index_key": "20240226"
  },
  "output2": [
    {
      "data_date": "20240226",
      "data_time": "",
      "open_price": "         6588.5",
      "high_price": "         6588.5",
      "low_price": "         6555.0",
      "last_price": "         6562.5",
      "last_qntt": "",
      "vol": "       639",
      "prev_diff_flag": "5",
      "prev_diff_price": "           21.5",
      "prev_diff_rate": "     -0.33"
    },
    {
      "data_date": "20240227",
      "data_time": "",
      "open_price": "         6555.0",
      "high_price": "         6577.5",
      "low_price": "         6549.0",
      "last_price": "         6565.0",
      "last_qntt": "",
      "vol": "       134",
      "prev_diff_flag": "2",
      "prev_diff_price": "            2.5",
      "prev_diff_rate": "      0.04"
    },
    {
      "data_date": "20240228",
      "data_time": "",
      "open_price": "         6567.0",
      "high_price": "         6568.5",
      "low_price": "         6511.0",
      "last_price": "         6515.0",
      "last_qntt": "",
      "vol": "      1210",
      "prev_diff_flag": "5",
      "prev_diff_price": "             50",
      "prev_diff_rate": "     -0.76"
    },
    {
      "data_date": "20240229",
      "data_time": "",
      "open_price": "         6516.0",
      "high_price": "         6551.0",
      "low_price": "         6509.5",
      "last_price": "         6519.0",
      "last_qntt": "",
      "vol": "       503",
      "prev_diff_flag": "2",
      "prev_diff_price": "              4",
      "prev_diff_rate": "      0.06"
    },
    {
      "data_date": "20240301",
      "data_time": "",
      "open_price": "         6517.5",
      "high_price": "         6554.5",
      "low_price": "         6510.5",
      "last_price": "         6546.0",
      "last_qntt": "",
      "vol": "       942",
      "prev_diff_flag": "2",
      "prev_diff_price": "             27",
      "prev_diff_rate": "      0.41"
    },
    {
      "data_date": "20240304",
      "data_time": "",
      "open_price": "         6546.0",
      "high_price": "         6549.0",
      "low_price": "         6528.5",
      "last_price": "         6528.5",
      "last_qntt": "",
      "vol": "      2298",
      "prev_diff_flag": "5",
      "prev_diff_price": "           17.5",
      "prev_diff_rate": "     -0.27"
    },
    {
      "data_date": "20240305",
      "data_time": "",
      "open_price": "         6530.5",
      "high_price": "         6541.0",
      "low_price": "         6498.0",
      "last_price": "         6523.5",
      "last_qntt": "",
      "vol": "     13778",
      "prev_diff_flag": "5",
      "prev_diff_price": "              5",
      "prev_diff_rate": "     -0.08"
    },
    {
      "data_date": "20240306",
      "data_time": "",
      "open_price": "         6522.0",
      "high_price": "         6600.5",
      "low_price": "         6512.5",
      "last_price": "         6584.5",
      "last_qntt": "",
      "vol": "      3269",
      "prev_diff_flag": "2",
      "prev_diff_price": "             61",
      "prev_diff_rate": "      0.94"
    },
    {
      "data_date": "20240307",
      "data_time": "",
      "open_price": "         6582.0",
      "high_price": "         6643.5",
      "low_price": "         6582.0",
      "last_price": "         6639.0",
      "last_qntt": "",
      "vol": "     10466",
      "prev_diff_flag": "2",
      "prev_diff_price": "           54.5",
      "prev_diff_rate": "      0.83"
    },
    {
      "data_date": "20240308",
      "data_time": "",
      "open_price": "         6637.0",
      "high_price": "         6686.5",
      "low_price": "         6632.5",
      "last_price": "         6644.0",
      "last_qntt": "",
      "vol": "      5258",
      "prev_diff_flag": "2",
      "prev_diff_price": "              5",
      "prev_diff_rate": "      0.08"
    },
    {
      "data_date": "20240311",
      "data_time": "",
      "open_price": "         6645.0",
      "high_price": "         6646.0",
      "low_price": "         6616.0",
      "last_price": "         6633.0",
      "last_qntt": "",
      "vol": "     39035",
      "prev_diff_flag": "5",
      "prev_diff_price": "             11",
      "prev_diff_rate": "     -0.17"
    },
    {
      "data_date": "20240312",
      "data_time": "",
      "open_price": "         0.6624",
      "high_price": "         0.6624",
      "low_price": "        0.66235",
      "last_price": "         0.6625",
      "last_qntt": "",
      "vol": "        11",
      "prev_diff_flag": "5",
      "prev_diff_price": "      6632.3375",
      "prev_diff_rate": "    -99.99"
    },
    {
      "data_date": "20240313",
      "data_time": "",
      "open_price": "          0.664",
      "high_price": "         0.6641",
      "low_price": "          0.664",
      "last_price": "          0.664",
      "last_qntt": "",
      "vol": "        50",
      "prev_diff_flag": "2",
      "prev_diff_price": "         0.0015",
      "prev_diff_rate": "      0.23"
    },
    {
      "data_date": "20240314",
      "data_time": "",
      "open_price": "         6598.5",
      "high_price": "         6598.5",
      "low_price": "         6598.5",
      "last_price": "         6598.5",
      "last_qntt": "",
      "vol": "        83",
      "prev_diff_flag": "2",
      "prev_diff_price": "       6597.836",
      "prev_diff_rate": " 993650.00"
    },
    {
      "data_date": "20240315",
      "data_time": "",
      "open_price": "         6598.5",
      "high_price": "         6599.5",
      "low_price": "         6569.5",
      "last_price": "         6577.5",
      "last_qntt": "",
      "vol": "     76056",
      "prev_diff_flag": "5",
      "prev_diff_price": "             21",
      "prev_diff_rate": "     -0.32"
    },
    {
      "data_date": "20240318",
      "data_time": "",
      "open_price": "         6576.5",
      "high_price": "         6576.5",
      "low_price": "         6576.5",
      "last_price": "         6576.5",
      "last_qntt": "",
      "vol": "         1",
      "prev_diff_flag": "5",
      "prev_diff_price": "              1",
      "prev_diff_rate": "     -0.02"
    },
    {
      "data_date": "20240319",
      "data_time": "",
      "open_price": "           6548",
      "high_price": "           6549",
      "low_price": "           6548",
      "last_price": "         6548.5",
      "last_qntt": "",
      "vol": "        44",
      "prev_diff_flag": "5",
      "prev_diff_price": "             28",
      "prev_diff_rate": "     -0.43"
    },
    {
      "data_date": "20240320",
      "data_time": "",
      "open_price": "         6548.0",
      "high_price": "         6603.5",
      "low_price": "         6528.0",
      "last_price": "         6602.5",
      "last_qntt": "",
      "vol": "    100506",
      "prev_diff_flag": "2",
      "prev_diff_price": "             54",
      "prev_diff_rate": "      0.82"
    },
    {
      "data_date": "20240321",
      "data_time": "",
      "open_price": "         6598.0",
      "high_price": "         6650.5",
      "low_price": "         6577.0",
      "last_price": "         6586.0",
      "last_qntt": "",
      "vol": "    126413",
      "prev_diff_flag": "5",
      "prev_diff_price": "           16.5",
      "prev_diff_rate": "     -0.25"
    },
    {
      "data_date": "20240322",
      "data_time": "",
      "open_price": "         6585.5",
      "high_price": "         6592.5",
      "low_price": "         6525.5",
      "last_price": "         6530.5",
      "last_qntt": "",
      "vol": "    101727",
      "prev_diff_flag": "5",
      "prev_diff_price": "           55.5",
      "prev_diff_rate": "     -0.84"
    },
    {
      "data_date": "20240325",
      "data_time": "",
      "open_price": "           6530",
      "high_price": "         6562.5",
      "low_price": "           6525",
      "last_price": "         6555.5",
      "last_qntt": "",
      "vol": "     70152",
      "prev_diff_flag": "2",
      "prev_diff_price": "             25",
      "prev_diff_rate": "      0.38"
    },
    {
      "data_date": "20240326",
      "data_time": "",
      "open_price": "         6555.5",
      "high_price": "         6574.5",
      "low_price": "         6545.5",
      "last_price": "         6548.5",
      "last_qntt": "",
      "vol": "     58147",
      "prev_diff_flag": "5",
      "prev_diff_price": "              7",
      "prev_diff_rate": "     -0.11"
    },
    {
      "data_date": "20240327",
      "data_time": "",
      "open_price": "           6548",
      "high_price": "           6553",
      "low_price": "         6525.5",
      "last_price": "           6549",
      "last_qntt": "",
      "vol": "     68767",
      "prev_diff_flag": "2",
      "prev_diff_price": "            0.5",
      "prev_diff_rate": "      0.01"
    },
    {
      "data_date": "20240328",
      "data_time": "",
      "open_price": "         6548.5",
      "high_price": "         6555.5",
      "low_price": "         6499.5",
      "last_price": "           6530",
      "last_qntt": "",
      "vol": "    104538",
      "prev_diff_flag": "5",
      "prev_diff_price": "             19",
      "prev_diff_rate": "     -0.29"
    },
    {
      "data_date": "20240401",
      "data_time": "",
      "open_price": "         6531.5",
      "high_price": "         6554.0",
      "low_price": "         6495.0",
      "last_price": "         6504.0",
      "last_qntt": "",
      "vol": "     74942",
      "prev_diff_flag": "5",
      "prev_diff_price": "             26",
      "prev_diff_rate": "     -0.40"
    },
    {
      "data_date": "20240402",
      "data_time": "",
      "open_price": "         6504.0",
      "high_price": "         6538.0",
      "low_price": "         6496.5",
      "last_price": "         6531.5",
      "last_qntt": "",
      "vol": "     83996",
      "prev_diff_flag": "2",
      "prev_diff_price": "           27.5",
      "prev_diff_rate": "      0.42"
    },
    {
      "data_date": "20240403",
      "data_time": "",
      "open_price": "           6532",
      "high_price": "           6584",
      "low_price": "         6517.5",
      "last_price": "         6579.5",
      "last_qntt": "",
      "vol": "     94108",
      "prev_diff_flag": "2",
      "prev_diff_price": "             48",
      "prev_diff_rate": "      0.73"
    },
    {
      "data_date": "20240404",
      "data_time": "",
      "open_price": "           6577",
      "high_price": "           6633",
      "low_price": "           6577",
      "last_price": "         6601.5",
      "last_qntt": "",
      "vol": "    115253",
      "prev_diff_flag": "2",
      "prev_diff_price": "             22",
      "prev_diff_rate": "      0.33"
    },
    {
      "data_date": "20240405",
      "data_time": "",
      "open_price": "         6601.5",
      "high_price": "         6606.5",
      "low_price": "           6563",
      "last_price": "           6593",
      "last_qntt": "",
      "vol": "    106612",
      "prev_diff_flag": "5",
      "prev_diff_price": "            8.5",
      "prev_diff_rate": "     -0.13"
    },
    {
      "data_date": "20240408",
      "data_time": "",
      "open_price": "           6590",
      "high_price": "         6623.5",
      "low_price": "           6573",
      "last_price": "         6617.5",
      "last_qntt": "",
      "vol": "     71474",
      "prev_diff_flag": "2",
      "prev_diff_price": "           24.5",
      "prev_diff_rate": "      0.37"
    },
    {
      "data_date": "20240409",
      "data_time": "",
      "open_price": "           6617",
      "high_price": "         6657.5",
      "low_price": "           6612",
      "last_price": "         6641.5",
      "last_qntt": "",
      "vol": "     88858",
      "prev_diff_flag": "2",
      "prev_diff_price": "             24",
      "prev_diff_rate": "      0.36"
    },
    {
      "data_date": "20240410",
      "data_time": "",
      "open_price": "         6641.5",
      "high_price": "         6644.5",
      "low_price": "         6512.0",
      "last_price": "         6525.0",
      "last_qntt": "",
      "vol": "    186665",
      "prev_diff_flag": "5",
      "prev_diff_price": "          116.5",
      "prev_diff_rate": "     -1.75"
    },
    {
      "data_date": "20240411",
      "data_time": "",
      "open_price": "         6524.5",
      "high_price": "         6565.0",
      "low_price": "         6514.5",
      "last_price": "         6550.5",
      "last_qntt": "",
      "vol": "    121379",
      "prev_diff_flag": "2",
      "prev_diff_price": "           25.5",
      "prev_diff_rate": "      0.39"
    },
    {
      "data_date": "20240412",
      "data_time": "",
      "open_price": "         6550.5",
      "high_price": "         6555.5",
      "low_price": "         6468.0",
      "last_price": "         6474.0",
      "last_qntt": "",
      "vol": "    125863",
      "prev_diff_flag": "5",
      "prev_diff_price": "           76.5",
      "prev_diff_rate": "     -1.17"
    },
    {
      "data_date": "20240415",
      "data_time": "",
      "open_price": "         6475.5",
      "high_price": "         6505.0",
      "low_price": "         6449.0",
      "last_price": "         6453.5",
      "last_qntt": "",
      "vol": "    113834",
      "prev_diff_flag": "5",
      "prev_diff_price": "           20.5",
      "prev_diff_rate": "     -0.32"
    },
    {
      "data_date": "20240416",
      "data_time": "",
      "open_price": "         6456.5",
      "high_price": "         6456.5",
      "low_price": "         6401.0",
      "last_price": "         6414.0",
      "last_qntt": "",
      "vol": "    120271",
      "prev_diff_flag": "5",
      "prev_diff_price": "           39.5",
      "prev_diff_rate": "     -0.61"
    },
    {
      "data_date": "20240417",
      "data_time": "",
      "open_price": "         6413.5",
      "high_price": "         6457.5",
      "low_price": "         6411.5",
      "last_price": "         6446.0",
      "last_qntt": "",
      "vol": "    110152",
      "prev_diff_flag": "2",
      "prev_diff_price": "             32",
      "prev_diff_rate": "      0.50"
    },
    {
      "data_date": "20240418",
      "data_time": "",
      "open_price": "         6446.0",
      "high_price": "         6467.0",
      "low_price": "         6427.5",
      "last_price": "         6432.0",
      "last_qntt": "",
      "vol": "     76120",
      "prev_diff_flag": "5",
      "prev_diff_price": "             14",
      "prev_diff_rate": "     -0.22"
    },
    {
      "data_date": "20240419",
      "data_time": "",
      "open_price": "         6431.5",
      "high_price": "         6444.0",
      "low_price": "         6373.0",
      "last_price": "         6428.5",
      "last_qntt": "",
      "vol": "    120611",
      "prev_diff_flag": "5",
      "prev_diff_price": "            3.5",
      "prev_diff_rate": "     -0.05"
    },
    {
      "data_date": "20240422",
      "data_time": "",
      "open_price": "         6430.0",
      "high_price": "         6466.5",
      "low_price": "         6425.0",
      "last_price": "         6460.0",
      "last_qntt": "",
      "vol": "     82245",
      "prev_diff_flag": "2",
      "prev_diff_price": "           31.5",
      "prev_diff_rate": "      0.49"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```
