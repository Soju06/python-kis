# 해외선물 체결추이(주간)[해외선물-017]

> [해외선물옵션] 기본시세

해외선물옵션 체결추이(주간) API입니다. 
한국투자 HTS(eFriend Force) > [5502] 해외선물옵션 체결추이 화면에서 "주간" 선택 시 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

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
| **API ID** | `cd2e4d9a-7e3d-44ff-9b68-36d971655c24` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/overseas-futureoption/v1/quotations/weekly-ccnl` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID (실전)** | `HHDFC55020000` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-04-05T13:28:11+09:00
- **최종 수정일**: 2025-04-30T12:57:14+09:00

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials Grant 절차를 준용)  법인(Access token 유효기간 3개월, Refresh token 유효기간 1년, OAuth 2.0의 Authorization Code Grant 절차를 준용) |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | HHDFC55020000 |
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
    "index_key": "20230522"
  },
  "output2": [
    {
      "data_date": "20230522",
      "data_time": "",
      "open_price": "         6713.0",
      "high_price": "         6713.0",
      "low_price": "         6620.0",
      "last_price": "         6620.0",
      "last_qntt": "",
      "vol": "        10",
      "prev_diff_flag": "5",
      "prev_diff_price": "             93",
      "prev_diff_rate": "     -1.39"
    },
    {
      "data_date": "20230612",
      "data_time": "",
      "open_price": "         6809.5",
      "high_price": "         6817.0",
      "low_price": "         6809.0",
      "last_price": "         6817.0",
      "last_qntt": "",
      "vol": "        20",
      "prev_diff_flag": "2",
      "prev_diff_price": "            197",
      "prev_diff_rate": "      2.98"
    },
    {
      "data_date": "20230626",
      "data_time": "",
      "open_price": "         6692.0",
      "high_price": "         6692.0",
      "low_price": "         6692.0",
      "last_price": "         6692.0",
      "last_qntt": "",
      "vol": "5         ",
      "prev_diff_flag": "5",
      "prev_diff_price": "            125",
      "prev_diff_rate": "     -1.83"
    },
    {
      "data_date": "20230710",
      "data_time": "",
      "open_price": "         6840.5",
      "high_price": "         6840.5",
      "low_price": "         6840.0",
      "last_price": "         6840.0",
      "last_qntt": "",
      "vol": "5         ",
      "prev_diff_flag": "2",
      "prev_diff_price": "            148",
      "prev_diff_rate": "      2.21"
    },
    {
      "data_date": "20230731",
      "data_time": "",
      "open_price": "         6702.0",
      "high_price": "         6702.0",
      "low_price": "         6605.0",
      "last_price": "         6605.0",
      "last_qntt": "",
      "vol": "        11",
      "prev_diff_flag": "5",
      "prev_diff_price": "            235",
      "prev_diff_rate": "     -3.44"
    },
    {
      "data_date": "20230807",
      "data_time": "",
      "open_price": "         6594.5",
      "high_price": "         6594.5",
      "low_price": "         6594.5",
      "last_price": "         6594.5",
      "last_qntt": "",
      "vol": "5         ",
      "prev_diff_flag": "5",
      "prev_diff_price": "           10.5",
      "prev_diff_rate": "     -0.16"
    },
    {
      "data_date": "20230904",
      "data_time": "",
      "open_price": "         6535.0",
      "high_price": "         6535.0",
      "low_price": "         6535.0",
      "last_price": "         6535.0",
      "last_qntt": "",
      "vol": "1         ",
      "prev_diff_flag": "5",
      "prev_diff_price": "           59.5",
      "prev_diff_rate": "     -0.90"
    },
    {
      "data_date": "20230911",
      "data_time": "",
      "open_price": "         6494.0",
      "high_price": "         6512.5",
      "low_price": "         6470.0",
      "last_price": "         6512.5",
      "last_qntt": "",
      "vol": "         8",
      "prev_diff_flag": "5",
      "prev_diff_price": "           22.5",
      "prev_diff_rate": "     -0.34"
    },
    {
      "data_date": "20230918",
      "data_time": "",
      "open_price": "         6500.5",
      "high_price": "         6558.5",
      "low_price": "         6459.5",
      "last_price": "         6479.5",
      "last_qntt": "",
      "vol": "        43",
      "prev_diff_flag": "5",
      "prev_diff_price": "             33",
      "prev_diff_rate": "     -0.51"
    },
    {
      "data_date": "20230925",
      "data_time": "",
      "open_price": "         6439.5",
      "high_price": "         6450.5",
      "low_price": "         6430.0",
      "last_price": "         6450.5",
      "last_qntt": "",
      "vol": "         3",
      "prev_diff_flag": "5",
      "prev_diff_price": "             29",
      "prev_diff_rate": "     -0.45"
    },
    {
      "data_date": "20231002",
      "data_time": "",
      "open_price": "         6480.5",
      "high_price": "         6480.5",
      "low_price": "         6360.0",
      "last_price": "         6406.0",
      "last_qntt": "",
      "vol": "        40",
      "prev_diff_flag": "5",
      "prev_diff_price": "           44.5",
      "prev_diff_rate": "     -0.69"
    },
    {
      "data_date": "20231009",
      "data_time": "",
      "open_price": "         6410.0",
      "high_price": "         6471.5",
      "low_price": "         6388.5",
      "last_price": "         6388.5",
      "last_qntt": "",
      "vol": "        21",
      "prev_diff_flag": "5",
      "prev_diff_price": "           17.5",
      "prev_diff_rate": "     -0.27"
    },
    {
      "data_date": "20231016",
      "data_time": "",
      "open_price": "         6381.0",
      "high_price": "         6423.0",
      "low_price": "         6345.0",
      "last_price": "         6360.0",
      "last_qntt": "",
      "vol": "        16",
      "prev_diff_flag": "5",
      "prev_diff_price": "           28.5",
      "prev_diff_rate": "     -0.45"
    },
    {
      "data_date": "20231023",
      "data_time": "",
      "open_price": "         6361.5",
      "high_price": "         6366.0",
      "low_price": "         6361.5",
      "last_price": "         6366.0",
      "last_qntt": "",
      "vol": "6         ",
      "prev_diff_flag": "2",
      "prev_diff_price": "              6",
      "prev_diff_rate": "      0.09"
    },
    {
      "data_date": "20231030",
      "data_time": "",
      "open_price": "         6460.5",
      "high_price": "         6547.0",
      "low_price": "         6460.5",
      "last_price": "         6530.0",
      "last_qntt": "",
      "vol": "       102",
      "prev_diff_flag": "2",
      "prev_diff_price": "            164",
      "prev_diff_rate": "      2.58"
    },
    {
      "data_date": "20231106",
      "data_time": "",
      "open_price": "         6502.0",
      "high_price": "         6502.0",
      "low_price": "         6395.0",
      "last_price": "         6395.0",
      "last_qntt": "",
      "vol": "        34",
      "prev_diff_flag": "5",
      "prev_diff_price": "            135",
      "prev_diff_rate": "     -2.07"
    },
    {
      "data_date": "20231113",
      "data_time": "",
      "open_price": "         6410.0",
      "high_price": "         6548.0",
      "low_price": "         6410.0",
      "last_price": "         6529.5",
      "last_qntt": "",
      "vol": "        18",
      "prev_diff_flag": "2",
      "prev_diff_price": "          134.5",
      "prev_diff_rate": "      2.10"
    },
    {
      "data_date": "20231120",
      "data_time": "",
      "open_price": "         6564.0",
      "high_price": "         6622.0",
      "low_price": "         6561.0",
      "last_price": "         6620.5",
      "last_qntt": "",
      "vol": "       190",
      "prev_diff_flag": "2",
      "prev_diff_price": "             91",
      "prev_diff_rate": "      1.39"
    },
    {
      "data_date": "20231127",
      "data_time": "",
      "open_price": "         6610.0",
      "high_price": "         6703.0",
      "low_price": "         6610.0",
      "last_price": "         6702.0",
      "last_qntt": "",
      "vol": "       326",
      "prev_diff_flag": "2",
      "prev_diff_price": "           81.5",
      "prev_diff_rate": "      1.23"
    },
    {
      "data_date": "20231204",
      "data_time": "",
      "open_price": "         6697.5",
      "high_price": "         6697.5",
      "low_price": "         6565.0",
      "last_price": "         6614.0",
      "last_qntt": "",
      "vol": "       296",
      "prev_diff_flag": "5",
      "prev_diff_price": "             88",
      "prev_diff_rate": "     -1.31"
    },
    {
      "data_date": "20231211",
      "data_time": "",
      "open_price": "         6605.0",
      "high_price": "         6760.5",
      "low_price": "         6578.0",
      "last_price": "         6730.0",
      "last_qntt": "",
      "vol": "       510",
      "prev_diff_flag": "2",
      "prev_diff_price": "            116",
      "prev_diff_rate": "      1.75"
    },
    {
      "data_date": "20231218",
      "data_time": "",
      "open_price": "         6731.0",
      "high_price": "         6855.5",
      "low_price": "         6725.0",
      "last_price": "         6827.0",
      "last_qntt": "",
      "vol": "       617",
      "prev_diff_flag": "2",
      "prev_diff_price": "             97",
      "prev_diff_rate": "      1.44"
    },
    {
      "data_date": "20231225",
      "data_time": "",
      "open_price": "         6834.0",
      "high_price": "         6900.0",
      "low_price": "         6811.5",
      "last_price": "         6858.5",
      "last_qntt": "",
      "vol": "       353",
      "prev_diff_flag": "2",
      "prev_diff_price": "           31.5",
      "prev_diff_rate": "      0.46"
    },
    {
      "data_date": "20240101",
      "data_time": "",
      "open_price": "         6841.0",
      "high_price": "         6864.5",
      "low_price": "         6683.0",
      "last_price": "         6742.0",
      "last_qntt": "",
      "vol": "       325",
      "prev_diff_flag": "5",
      "prev_diff_price": "          116.5",
      "prev_diff_rate": "     -1.70"
    },
    {
      "data_date": "20240108",
      "data_time": "",
      "open_price": "         6762.0",
      "high_price": "         6762.0",
      "low_price": "         6678.0",
      "last_price": "         6711.0",
      "last_qntt": "",
      "vol": "       310",
      "prev_diff_flag": "5",
      "prev_diff_price": "             31",
      "prev_diff_rate": "     -0.46"
    },
    {
      "data_date": "20240115",
      "data_time": "",
      "open_price": "         6709.5",
      "high_price": "         6728.0",
      "low_price": "         6556.0",
      "last_price": "         6624.5",
      "last_qntt": "",
      "vol": "       900",
      "prev_diff_flag": "5",
      "prev_diff_price": "           86.5",
      "prev_diff_rate": "     -1.29"
    },
    {
      "data_date": "20240122",
      "data_time": "",
      "open_price": "         6622.0",
      "high_price": "         6643.0",
      "low_price": "         6579.5",
      "last_price": "         6600.0",
      "last_qntt": "",
      "vol": "       389",
      "prev_diff_flag": "5",
      "prev_diff_price": "           24.5",
      "prev_diff_rate": "     -0.37"
    },
    {
      "data_date": "20240129",
      "data_time": "",
      "open_price": "         6598.0",
      "high_price": "         6646.5",
      "low_price": "         6529.0",
      "last_price": "         6539.5",
      "last_qntt": "",
      "vol": "       962",
      "prev_diff_flag": "5",
      "prev_diff_price": "           60.5",
      "prev_diff_rate": "     -0.92"
    },
    {
      "data_date": "20240205",
      "data_time": "",
      "open_price": "         6520.5",
      "high_price": "         6563.5",
      "low_price": "         6494.5",
      "last_price": "         6549.5",
      "last_qntt": "",
      "vol": "      1019",
      "prev_diff_flag": "2",
      "prev_diff_price": "             10",
      "prev_diff_rate": "      0.15"
    },
    {
      "data_date": "20240212",
      "data_time": "",
      "open_price": "         6553.0",
      "high_price": "         6568.0",
      "low_price": "         6469.0",
      "last_price": "         6557.5",
      "last_qntt": "",
      "vol": "       891",
      "prev_diff_flag": "2",
      "prev_diff_price": "              8",
      "prev_diff_rate": "      0.12"
    },
    {
      "data_date": "20240219",
      "data_time": "",
      "open_price": "         6564.0",
      "high_price": "         6616.5",
      "low_price": "         6544.5",
      "last_price": "         6584.0",
      "last_qntt": "",
      "vol": "      1773",
      "prev_diff_flag": "2",
      "prev_diff_price": "           26.5",
      "prev_diff_rate": "      0.40"
    },
    {
      "data_date": "20240226",
      "data_time": "",
      "open_price": "         6588.5",
      "high_price": "         6588.5",
      "low_price": "         6509.5",
      "last_price": "         6546.0",
      "last_qntt": "",
      "vol": "      3428",
      "prev_diff_flag": "5",
      "prev_diff_price": "             38",
      "prev_diff_rate": "     -0.58"
    },
    {
      "data_date": "20240304",
      "data_time": "",
      "open_price": "         6546.0",
      "high_price": "         6686.5",
      "low_price": "         6498.0",
      "last_price": "         6644.0",
      "last_qntt": "",
      "vol": "     35069",
      "prev_diff_flag": "2",
      "prev_diff_price": "             98",
      "prev_diff_rate": "      1.50"
    },
    {
      "data_date": "20240311",
      "data_time": "",
      "open_price": "         6645.0",
      "high_price": "         6646.0",
      "low_price": "        0.66235",
      "last_price": "         6577.5",
      "last_qntt": "",
      "vol": "    115245",
      "prev_diff_flag": "5",
      "prev_diff_price": "           66.5",
      "prev_diff_rate": "     -1.00"
    },
    {
      "data_date": "20240318",
      "data_time": "",
      "open_price": "         6576.5",
      "high_price": "         6650.5",
      "low_price": "         6525.5",
      "last_price": "         6530.5",
      "last_qntt": "",
      "vol": "    328691",
      "prev_diff_flag": "5",
      "prev_diff_price": "             47",
      "prev_diff_rate": "     -0.71"
    },
    {
      "data_date": "20240325",
      "data_time": "",
      "open_price": "           6530",
      "high_price": "         6574.5",
      "low_price": "         6499.5",
      "last_price": "           6530",
      "last_qntt": "",
      "vol": "    301604",
      "prev_diff_flag": "5",
      "prev_diff_price": "            0.5",
      "prev_diff_rate": "     -0.01"
    },
    {
      "data_date": "20240401",
      "data_time": "",
      "open_price": "         6531.5",
      "high_price": "           6633",
      "low_price": "         6495.0",
      "last_price": "           6593",
      "last_qntt": "",
      "vol": "    474911",
      "prev_diff_flag": "2",
      "prev_diff_price": "             63",
      "prev_diff_rate": "      0.96"
    },
    {
      "data_date": "20240408",
      "data_time": "",
      "open_price": "           6590",
      "high_price": "         6657.5",
      "low_price": "         6468.0",
      "last_price": "         6474.0",
      "last_qntt": "",
      "vol": "    594239",
      "prev_diff_flag": "5",
      "prev_diff_price": "            119",
      "prev_diff_rate": "     -1.80"
    },
    {
      "data_date": "20240415",
      "data_time": "",
      "open_price": "         6475.5",
      "high_price": "         6505.0",
      "low_price": "         6373.0",
      "last_price": "         6428.5",
      "last_qntt": "",
      "vol": "    540988",
      "prev_diff_flag": "5",
      "prev_diff_price": "           45.5",
      "prev_diff_rate": "     -0.70"
    },
    {
      "data_date": "20240422",
      "data_time": "",
      "open_price": "         6430.0",
      "high_price": "         6466.5",
      "low_price": "         6425.0",
      "last_price": "         6460.0",
      "last_qntt": "",
      "vol": "82245     ",
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

