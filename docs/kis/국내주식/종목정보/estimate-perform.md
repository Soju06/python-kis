# 국내주식 종목추정실적 [국내주식-187]

> [국내주식] 종목정보

국내주식 종목추정실적 API입니다.
한국투자 HTS(eFriend Plus) > [0613] 종목추정실적 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다. 
 
※ 본 화면의 추정실적 및 투자의견은 당월 초의 애널리스트의 의견사항이므로 월중 변동 사항이 있을 수 있음을 유의하시기 바랍니다.
※ 종목별 수익추정은 리서치본부에서 매월 발표되는 거래소, 코스닥 160여개 기업에 한정합니다. 구체적인 종목 리스트는 추정종목리스트를 참고하기 바랍니다.

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `fbb4bb45-57bb-4037-905d-dff0ff635cf6` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/quotations/estimate-perform` |
| **Content-Type** | `` |
| **요청 포맷** | `` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `미지원` |
| **TR ID** | `모의투자 미지원`, `HHKST668300C0` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-05-03
- **최종 수정일**: 2025-05-14

## 요청 (Request)

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials G... |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | HHKST668300C0 |
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
| `SHT_CD` | 종목코드 | String | 2 | Y | ex) 265520 |

### 요청 예시

```json
SHT_CD:005930
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
| `sht_cd` | ELW단축종목코드 | String | 9 | Y |  |
| `item_kor_nm` | HTS한글종목명 | String | 40 | Y |  |
| `name1` | ELW현재가 | String | 10 | Y |  |
| `name2` | 전일대비 | String | 10 | Y |  |
| `estdate` | 전일대비부호 | String | 1 | Y |  |
| `rcmd_name` | 전일대비율 | String | 82 | Y |  |
| `capital` | 누적거래량 | String | 18 | Y |  |
| `forn_item_lmtrt` | 행사가 | String | 112 | Y |  |
| `output2` | 응답상세 | Object |   | Y | '(추정손익계산서-6개 array)   매출액, 매출액증감율,   영업이익, 영업이익증감율,   순이익, 순이익증감율,' |
| `data1` | DATA1 | String | 15 | Y | 결산연월(outblock4) 참조 |
| `data2` | DATA2 | String | 15 | Y | 결산연월(outblock4) 참조 |
| `data3` | DATA3 | String | 15 | Y | 결산연월(outblock4) 참조 |
| `data4` | DATA4 | String | 15 | Y | 결산연월(outblock4) 참조 |
| `data5` | DATA5 | String | 15 | Y | 결산연월(outblock4) 참조 |
| `output3` | 응답상세 | Object |   | Y | '(투자지표-8개 array)   EBITDA(십억원), EPS(원),    EPS 증감율(0.1%),  PER(배, 0.1%),    EV/EBITDA(배, 0.1), RO... |
| `data1` | DATA1 | String | 15 | Y | 결산연월(outblock4) 참조 |
| `data2` | DATA2 | String | 15 | Y | 결산연월(outblock4) 참조 |
| `data3` | DATA3 | String | 15 | Y | 결산연월(outblock4) 참조 |
| `data4` | DATA4 | String | 15 | Y | 결산연월(outblock4) 참조 |
| `data5` | DATA5 | String | 15 | Y | 결산연월(outblock4) 참조 |
| `output4` | 응답상세 | Object |   | Y | array |
| `dt` | 결산년월 | String | 8 | Y | DATA1 ~5 결산월 정보 |

### 응답 예시

```json
{
  "output1": {
    "sht_cd": "A005930",
    "item_kor_nm": "삼성전자",
    "name1": "김한국",
    "name2": "",
    "estdate": "20240109",
    "rcmd_name": "매수",
    "capital": "8975.0",
    "forn_item_lmtrt": "0.00"
  },
  "output2": [
    {
      "data1": "2796048.0",
      "data2": "3022314.0",
      "data3": "2581509.0",
      "data4": "3048945.0",
      "data5": "3295675.0"
    },
    {
      "data1": "181.0",
      "data2": "81.0",
      "data3": "-146.0",
      "data4": "181.0",
      "data5": "81.0"
    },
    {
      "data1": "516339.0",
      "data2": "433766.0",
      "data3": "65405.0",
      "data4": "330172.0",
      "data5": "555410.0"
    },
    {
      "data1": "435.0",
      "data2": "-160.0",
      "data3": "-849.0",
      "data4": "4048.0",
      "data5": "682.0"
    },
    {
      "data1": "392438.0",
      "data2": "547300.0",
      "data3": "106144.0",
      "data4": "253332.0",
      "data5": "422055.0"
    },
    {
      "data1": "504.0",
      "data2": "395.0",
      "data3": "-806.0",
      "data4": "1387.0",
      "data5": "666.0"
    }
  ],
  "output3": [
    {
      "data1": "858812.0",
      "data2": "824843.0",
      "data3": "483199.0",
      "data4": "792602.0",
      "data5": "1043367.0"
    },
    {
      "data1": "57770.0",
      "data2": "80570.0",
      "data3": "15609.0",
      "data4": "36983.0",
      "data5": "61483.0"
    },
    {
      "data1": "504.0",
      "data2": "395.0",
      "data3": "-806.0",
      "data4": "1369.0",
      "data5": "662.0"
    },
    {
      "data1": "136.0",
      "data2": "69.0",
      "data3": "503.0",
      "data4": "207.0",
      "data5": "124.0"
    },
    {
      "data1": "50.0",
      "data2": "34.0",
      "data3": "95.0",
      "data4": "53.0",
      "data5": "39.0"
    },
    {
      "data1": "139.0",
      "data2": "171.0",
      "data3": "31.0",
      "data4": "70.0",
      "data5": "109.0"
    },
    {
      "data1": "399.0",
      "data2": "264.0",
      "data3": "255.0",
      "data4": "226.0",
      "data5": "163.0"
    },
    {
      "data1": "1197.0",
      "data2": "568.0",
      "data3": "58.0",
      "data4": "232.0",
      "data5": "655.0"
    }
  ],
  "output4": [
    {
      "dt": "2021.12"
    },
    {
      "dt": "2022.12"
    },
    {
      "dt": "2023.12E"
    },
    {
      "dt": "2024.12E"
    },
    {
      "dt": "2025.12E"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```
