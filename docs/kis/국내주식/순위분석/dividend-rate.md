# 국내주식 배당률 상위[국내주식-106]

> [국내주식] 순위분석

국내주식 배당률 상위 API입니다. 
한국투자 HTS(eFriend Plus) > [0188] 배당률 상위 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.
최대 30건 확인 가능하며, 다음 조회가 불가합니다.

※ 30건 이상의 목록 조회가 필요한 경우, 대안으로 종목조건검색 API를 이용해서 원하는 종목 100개까지 검색할 수 있는 기능을 제공하고 있습니다.
종목조건검색 API는 HTS(efriend Plus) [0110] 조건검색에서 등록 및 서버저장한 나의 조건 목록을 확인할 수 있는 API로,
자세한 사용 방법은 공지사항 - [조건검색 필독] 조건검색 API 이용안내 참고 부탁드립니다.

## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `20027666-84aa-491a-9a95-644d8fbd7015` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/ranking/dividend-rate` |
| **Content-Type** | `` |
| **요청 포맷** | `` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `모의투자 미지원` |
| **TR ID** | `HHKDB13470100`, `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-04-05
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
| `tr_id` | 거래ID | String | 13 | Y | HHKDB13470100 |
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
| `CTS_AREA` | CTS_AREA | String | 17 | Y | 공백 |
| `GB1` | KOSPI | String | 1 | Y | 0:전체, 1:코스피,  2: 코스피200, 3: 코스닥, |
| `UPJONG` | 업종구분 | String | 4 | Y | '코스피(0001:종합, 0002:대형주.…0027:제조업 ),  코스닥(1001:종합, …. 1041:IT부품 코스피200 (2001:KOSPI200, 2007:KOSPI1... |
| `GB2` | 종목선택 | String | 1 | Y | 0:전체, 6:보통주, 7:우선주 |
| `GB3` | 배당구분 | String | 1 | Y | 1:주식배당, 2: 현금배당 |
| `F_DT` | 기준일From | String | 8 | Y |  |
| `T_DT` | 기준일To | String | 8 | Y |  |
| `GB4` | 결산/중간배당 | String | 1 | Y | 0:전체, 1:결산배당, 2:중간배당 |

### 요청 예시

```json
CTS_AREA:
GB1:0
UPJONG:0001
GB2:0
GB3:1
F_DT:20200101
T_DT:20240403
GB4:0
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
| `output1` | 응답상세 | Object |   | Y | array |
| `rank` | 순위 | String | 4 | Y |  |
| `sht_cd` | 종목코드 | String | 9 | Y |  |
| `isin_name` | 종목명 | String | 40 | Y |  |
| `record_date` | 기준일 | String | 8 | Y |  |
| `per_sto_divi_amt` | 현금/주식배당금 | String | 12 | Y |  |
| `divi_rate` | 현금/주식배당률(%) | String | 62 | Y |  |
| `divi_kind` | 배당종류 | String | 8 | Y |  |

### 응답 예시

```json
{
  "output": [
    {
      "rank": "1",
      "sht_cd": "089600",
      "isin_name": "나스미디어",
      "record_date": "20211231",
      "per_sto_divi_amt": "0",
      "divi_rate": "0.00",
      "divi_kind": "결산"
    },
    {
      "rank": "2",
      "sht_cd": "089600",
      "isin_name": "나스미디어",
      "record_date": "20201231",
      "per_sto_divi_amt": "0",
      "divi_rate": "0.00",
      "divi_kind": "결산"
    },
    {
      "rank": "3",
      "sht_cd": "089600",
      "isin_name": "나스미디어",
      "record_date": "20221231",
      "per_sto_divi_amt": "0",
      "divi_rate": "0.00",
      "divi_kind": "결산"
    },
    {
      "rank": "4",
      "sht_cd": "243070",
      "isin_name": "휴온스",
      "record_date": "20211231",
      "per_sto_divi_amt": "0",
      "divi_rate": "0.00",
      "divi_kind": "결산"
    },
    {
      "rank": "5",
      "sht_cd": "243070",
      "isin_name": "휴온스",
      "record_date": "20201231",
      "per_sto_divi_amt": "0",
      "divi_rate": "0.00",
      "divi_kind": "결산"
    },
    {
      "rank": "6",
      "sht_cd": "086520",
      "isin_name": "에코프로",
      "record_date": "20221231",
      "per_sto_divi_amt": "0",
      "divi_rate": "0.00",
      "divi_kind": "결산"
    },
    {
      "rank": "7",
      "sht_cd": "084110",
      "isin_name": "휴온스글로벌",
      "record_date": "20211231",
      "per_sto_divi_amt": "0",
      "divi_rate": "0.00",
      "divi_kind": "결산"
    },
    {
      "rank": "8",
      "sht_cd": "119610",
      "isin_name": "인터로조",
      "record_date": "20211231",
      "per_sto_divi_amt": "0",
      "divi_rate": "0.00",
      "divi_kind": "결산"
    },
    {
      "rank": "9",
      "sht_cd": "086520",
      "isin_name": "에코프로",
      "record_date": "20211231",
      "per_sto_divi_amt": "0",
      "divi_rate": "0.00",
      "divi_kind": "결산"
    },
    {
      "rank": "10",
      "sht_cd": "084110",
      "isin_name": "휴온스글로벌",
      "record_date": "20201231",
      "per_sto_divi_amt": "0",
      "divi_rate": "0.00",
      "divi_kind": "결산"
    },
    {
      "rank": "11",
      "sht_cd": "239610",
      "isin_name": "에이치엘사이언스",
      "record_date": "20201231",
      "per_sto_divi_amt": "0",
      "divi_rate": "0.00",
      "divi_kind": "결산"
    },
    {
      "rank": "12",
      "sht_cd": "068270",
      "isin_name": "셀트리온",
      "record_date": "20211231",
      "per_sto_divi_amt": "0",
      "divi_rate": "0.00",
      "divi_kind": "결산"
    },
    {
      "rank": "13",
      "sht_cd": "049950",
      "isin_name": "미래컴퍼니",
      "record_date": "20221231",
      "per_sto_divi_amt": "0",
      "divi_rate": "0.00",
      "divi_kind": "결산"
    },
    {
      "rank": "14",
      "sht_cd": "068930",
      "isin_name": "디지털대성",
      "record_date": "20211231",
      "per_sto_divi_amt": "0",
      "divi_rate": "0.00",
      "divi_kind": "결산"
    },
    {
      "rank": "15",
      "sht_cd": "086520",
      "isin_name": "에코프로",
      "record_date": "20201231",
      "per_sto_divi_amt": "0",
      "divi_rate": "0.00",
      "divi_kind": "결산"
    },
    {
      "rank": "16",
      "sht_cd": "119610",
      "isin_name": "인터로조",
      "record_date": "20201231",
      "per_sto_divi_amt": "0",
      "divi_rate": "0.00",
      "divi_kind": "결산"
    },
    {
      "rank": "17",
      "sht_cd": "003300",
      "isin_name": "한일홀딩스",
      "record_date": "20211231",
      "per_sto_divi_amt": "0",
      "divi_rate": "0.00",
      "divi_kind": "결산"
    },
    {
      "rank": "18",
      "sht_cd": "001530",
      "isin_name": "디아이동일",
      "record_date": "20231231",
      "per_sto_divi_amt": "0",
      "divi_rate": "0.00",
      "divi_kind": "결산"
    },
    {
      "rank": "19",
      "sht_cd": "282880",
      "isin_name": "코윈테크",
      "record_date": "20231231",
      "per_sto_divi_amt": "0",
      "divi_rate": "0.00",
      "divi_kind": "결산"
    },
    {
      "rank": "20",
      "sht_cd": "001530",
      "isin_name": "디아이동일",
      "record_date": "20221231",
      "per_sto_divi_amt": "0",
      "divi_rate": "0.00",
      "divi_kind": "결산"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```
