# 예탁원정보(주식매수청구일정)[국내주식-146]

> [국내주식] 종목정보

예탁원정보(주식매수청구일정) API입니다. 
한국투자 HTS(eFriend Plus) > [0663] 주식매수청구 화면의 기능을 API로 개발한 사항으로, 해당 화면을 참고하시면 기능을 이해하기 쉽습니다.

※ 예탁원에서 제공한 자료이므로 정보용으로만 사용하시기 바랍니다.


## 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **API ID** | `664138c4-6417-45a0-bbcc-da4eb4317edf` |
| **HTTP Method** | `GET` |
| **URL** | `/uapi/domestic-stock/v1/ksdinfo/purreq` |
| **Content-Type** | `application/json` |
| **요청 포맷** | `JSON` |
| **실전 도메인** | `https://openapi.koreainvestment.com:9443` |
| **모의 도메인** | `미지원` |
| **TR ID (실전)** | `HHKDB669103C0` |
| **TR ID (모의)** | `모의투자 미지원` |

## 메타 정보

- **제공 기관**: 한국투자증권
- **과금 정책**: 무과금
- **상태**: RUNNING
- **생성일**: 2024-03-27
- **최종 수정일**: 2025-05-14

## 요청

### Headers

| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |
|--------|--------|------|------|------|------|
| `content-type` | 컨텐츠타입 | String | 40 | Y | application/json; charset=utf-8 |
| `authorization` | 접근토큰 | String | 350 | Y | OAuth 토큰이 필요한 API 경우 발급한 Access token  일반고객(Access token 유효기간 1일, OAuth 2.0의 Client Credentials G... |
| `appkey` | 앱키 | String | 36 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `appsecret` | 앱시크릿키 | String | 180 | Y | 한국투자증권 홈페이지에서 발급받은 appkey (절대 노출되지 않도록 주의해주세요.) |
| `personalseckey` | 고객식별키 | String | 180 | N | [법인 필수] 제휴사 회원 관리를 위한 고객식별키 |
| `tr_id` | 거래ID | String | 13 | Y | HHKDB669103C0 |
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
| `SHT_CD` | 종목코드 | String | 9 | Y | 공백: 전체,  특정종목 조회시 : 종목코드 |
| `T_DT` | 조회일자To | String | 8 | Y | ~ 일자 |
| `F_DT` | 조회일자From | String | 8 | Y | 일자 ~ |
| `CTS` | CTS | String | 17 | Y | 공백 |

### 요청 예시

```json
cts:
f_dt:20230301
t_dt:20240326
sht_cd:
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
| `output1` | 응답상세 | Object |   | Y | array |
| `record_date` | 기준일 | String | 8 | Y |  |
| `sht_cd` | 종목코드 | String | 9 | Y |  |
| `isin_name` | 종목명 | String | 40 | Y |  |
| `stk_kind` | 주식종류 | String | 8 | Y |  |
| `opp_opi_rcpt_term` | 반대의사접수시한 | String | 9 | Y |  |
| `buy_req_rcpt_term` | 매수청구접수시한 | String | 12 | Y |  |
| `buy_req_price` |  매수청구가격 | String | 62 | Y |  |
| `buy_amt_pay_dt` | 매수대금지급일 | String | 62 | Y |  |
| `get_meet_dt` | 주총일 | String | 10 | Y |  |

### 응답 예시

```json
{
  "output1": [
    {
      "record_date": "20240313",
      "sht_cd": "065350",
      "isin_name": "신성델타테크",
      "stk_kind": "보통",
      "opp_opi_rcpt_term": "020240326",
      "buy_req_rcpt_term": "",
      "buy_req_price": "000000000000",
      "buy_amt_pay_dt": "",
      "get_meet_dt": ""
    },
    {
      "record_date": "20240311",
      "sht_cd": "472850",
      "isin_name": "폰드그룹",
      "stk_kind": "보통",
      "opp_opi_rcpt_term": "020240325",
      "buy_req_rcpt_term": "",
      "buy_req_price": "000000000000",
      "buy_amt_pay_dt": "",
      "get_meet_dt": ""
    },
    {
      "record_date": "20240306",
      "sht_cd": "238930",
      "isin_name": "제이비케이랩",
      "stk_kind": "보통",
      "opp_opi_rcpt_term": "020240319",
      "buy_req_rcpt_term": "",
      "buy_req_price": "000000000000",
      "buy_amt_pay_dt": "",
      "get_meet_dt": ""
    },
    {
      "record_date": "20240305",
      "sht_cd": "435620",
      "isin_name": "하나금융25호기업인수목적",
      "stk_kind": "보통",
      "opp_opi_rcpt_term": "020240409",
      "buy_req_rcpt_term": "020240430",
      "buy_req_price": "000000010578",
      "buy_amt_pay_dt": "2024/05/16",
      "get_meet_dt": "2024/04/12"
    },
    {
      "record_date": "20240305",
      "sht_cd": "452450",
      "isin_name": "피아이이",
      "stk_kind": "보통",
      "opp_opi_rcpt_term": "020240409",
      "buy_req_rcpt_term": "020240430",
      "buy_req_price": "000000006733",
      "buy_amt_pay_dt": "2024/05/16",
      "get_meet_dt": "2024/04/12"
    },
    {
      "record_date": "20240304",
      "sht_cd": "065150",
      "isin_name": "대산에프앤비",
      "stk_kind": "보통",
      "opp_opi_rcpt_term": "020240327",
      "buy_req_rcpt_term": "020240417",
      "buy_req_price": "000000000260",
      "buy_amt_pay_dt": "2024/05/17",
      "get_meet_dt": "2024/03/29"
    },
    {
      "record_date": "20240229",
      "sht_cd": "034110",
      "isin_name": "조선호텔앤리조트",
      "stk_kind": "보통",
      "opp_opi_rcpt_term": "020240322",
      "buy_req_rcpt_term": "020240412",
      "buy_req_price": "000000016577",
      "buy_amt_pay_dt": "2024/05/14",
      "get_meet_dt": "2024/03/26"
    },
    {
      "record_date": "20240229",
      "sht_cd": "034300",
      "isin_name": "신세계건설",
      "stk_kind": "보통",
      "opp_opi_rcpt_term": "020240322",
      "buy_req_rcpt_term": "020240412",
      "buy_req_price": "000000011865",
      "buy_amt_pay_dt": "2024/05/14",
      "get_meet_dt": "2024/03/26"
    },
    {
      "record_date": "20240228",
      "sht_cd": "011690",
      "isin_name": "와이투솔루션",
      "stk_kind": "보통",
      "opp_opi_rcpt_term": "020240312",
      "buy_req_rcpt_term": "",
      "buy_req_price": "000000000000",
      "buy_amt_pay_dt": "",
      "get_meet_dt": ""
    },
    {
      "record_date": "20240222",
      "sht_cd": "021240",
      "isin_name": "코웨이",
      "stk_kind": "보통",
      "opp_opi_rcpt_term": "020240320",
      "buy_req_rcpt_term": "020240409",
      "buy_req_price": "000000056357",
      "buy_amt_pay_dt": "2024/05/07",
      "get_meet_dt": "2024/03/22"
    },
    {
      "record_date": "20240222",
      "sht_cd": "035720",
      "isin_name": "카카오",
      "stk_kind": "보통",
      "opp_opi_rcpt_term": "020240307",
      "buy_req_rcpt_term": "",
      "buy_req_price": "000000000000",
      "buy_amt_pay_dt": "",
      "get_meet_dt": ""
    },
    {
      "record_date": "20240221",
      "sht_cd": "039310",
      "isin_name": "세중",
      "stk_kind": "보통",
      "opp_opi_rcpt_term": "020240305",
      "buy_req_rcpt_term": "",
      "buy_req_price": "000000000000",
      "buy_amt_pay_dt": "",
      "get_meet_dt": ""
    },
    {
      "record_date": "20240216",
      "sht_cd": "101000",
      "isin_name": "상상인인더스트리",
      "stk_kind": "보통",
      "opp_opi_rcpt_term": "020240308",
      "buy_req_rcpt_term": "020240329",
      "buy_req_price": "000000002310",
      "buy_amt_pay_dt": "2024/04/30",
      "get_meet_dt": "2024/03/12"
    },
    {
      "record_date": "20240216",
      "sht_cd": "101005",
      "isin_name": "상상인인더스트리1우",
      "stk_kind": "우선",
      "opp_opi_rcpt_term": "020240308",
      "buy_req_rcpt_term": "020240329",
      "buy_req_price": "000000000000",
      "buy_amt_pay_dt": "2024/04/30",
      "get_meet_dt": "2024/03/12"
    },
    {
      "record_date": "20240216",
      "sht_cd": "101007",
      "isin_name": "상상인인더스트리2우",
      "stk_kind": "2우선",
      "opp_opi_rcpt_term": "020240308",
      "buy_req_rcpt_term": "020240329",
      "buy_req_price": "000000000000",
      "buy_amt_pay_dt": "2024/04/30",
      "get_meet_dt": "2024/03/12"
    },
    {
      "record_date": "20240216",
      "sht_cd": "101009",
      "isin_name": "상상인인더스트리3우",
      "stk_kind": "3우선",
      "opp_opi_rcpt_term": "020240308",
      "buy_req_rcpt_term": "020240329",
      "buy_req_price": "000000000000",
      "buy_amt_pay_dt": "2024/04/30",
      "get_meet_dt": "2024/03/12"
    },
    {
      "record_date": "20240214",
      "sht_cd": "053300",
      "isin_name": "한국정보인증",
      "stk_kind": "보통",
      "opp_opi_rcpt_term": "020240322",
      "buy_req_rcpt_term": "",
      "buy_req_price": "000000000000",
      "buy_amt_pay_dt": "",
      "get_meet_dt": ""
    },
    {
      "record_date": "20240214",
      "sht_cd": "123010",
      "isin_name": "아이윈플러스",
      "stk_kind": "보통",
      "opp_opi_rcpt_term": "020240227",
      "buy_req_rcpt_term": "",
      "buy_req_price": "000000000000",
      "buy_amt_pay_dt": "",
      "get_meet_dt": ""
    },
    {
      "record_date": "20240214",
      "sht_cd": "123015",
      "isin_name": "아이윈플러스1우",
      "stk_kind": "우선",
      "opp_opi_rcpt_term": "020240227",
      "buy_req_rcpt_term": "",
      "buy_req_price": "000000000000",
      "buy_amt_pay_dt": "",
      "get_meet_dt": ""
    },
    {
      "record_date": "20240214",
      "sht_cd": "123017",
      "isin_name": "아이윈플러스2우",
      "stk_kind": "2우선",
      "opp_opi_rcpt_term": "020240227",
      "buy_req_rcpt_term": "",
      "buy_req_price": "000000000000",
      "buy_amt_pay_dt": "",
      "get_meet_dt": ""
    },
    {
      "record_date": "20240214",
      "sht_cd": "123019",
      "isin_name": "아이윈플러스3우",
      "stk_kind": "3우선",
      "opp_opi_rcpt_term": "020240227",
      "buy_req_rcpt_term": "",
      "buy_req_price": "000000000000",
      "buy_amt_pay_dt": "",
      "get_meet_dt": ""
    },
    {
      "record_date": "20240214",
      "sht_cd": "12301A",
      "isin_name": "아이윈플러스4우",
      "stk_kind": "4우선",
      "opp_opi_rcpt_term": "020240227",
      "buy_req_rcpt_term": "",
      "buy_req_price": "000000000000",
      "buy_amt_pay_dt": "",
      "get_meet_dt": ""
    },
    {
      "record_date": "20240208",
      "sht_cd": "044180",
      "isin_name": "KD",
      "stk_kind": "보통",
      "opp_opi_rcpt_term": "020240226",
      "buy_req_rcpt_term": "",
      "buy_req_price": "000000000000",
      "buy_amt_pay_dt": "",
      "get_meet_dt": ""
    },
    {
      "record_date": "20240208",
      "sht_cd": "095190",
      "isin_name": "이엠코리아",
      "stk_kind": "보통",
      "opp_opi_rcpt_term": "020240222",
      "buy_req_rcpt_term": "",
      "buy_req_price": "000000000000",
      "buy_amt_pay_dt": "",
      "get_meet_dt": ""
    },
    {
      "record_date": "20240208",
      "sht_cd": "097780",
      "isin_name": "에코볼트",
      "stk_kind": "보통",
      "opp_opi_rcpt_term": "020240222",
      "buy_req_rcpt_term": "",
      "buy_req_price": "000000000000",
      "buy_amt_pay_dt": "",
      "get_meet_dt": ""
    },
    {
      "record_date": "20240208",
      "sht_cd": "097785",
      "isin_name": "에코볼트1우",
      "stk_kind": "우선",
      "opp_opi_rcpt_term": "020240222",
      "buy_req_rcpt_term": "",
      "buy_req_price": "000000000000",
      "buy_amt_pay_dt": "",
      "get_meet_dt": ""
    },
    {
      "record_date": "20240208",
      "sht_cd": "457190",
      "isin_name": "이수스페셜티케미컬",
      "stk_kind": "보통",
      "opp_opi_rcpt_term": "020240221",
      "buy_req_rcpt_term": "",
      "buy_req_price": "000000000000",
      "buy_amt_pay_dt": "",
      "get_meet_dt": ""
    },
    {
      "record_date": "20240207",
      "sht_cd": "019440",
      "isin_name": "세아특수강",
      "stk_kind": "보통",
      "opp_opi_rcpt_term": "020240220",
      "buy_req_rcpt_term": "",
      "buy_req_price": "000000000000",
      "buy_amt_pay_dt": "",
      "get_meet_dt": ""
    },
    {
      "record_date": "20240205",
      "sht_cd": "140430",
      "isin_name": "카티스",
      "stk_kind": "보통",
      "opp_opi_rcpt_term": "020240313",
      "buy_req_rcpt_term": "020240403",
      "buy_req_price": "000000003359",
      "buy_amt_pay_dt": "2024/04/12",
      "get_meet_dt": "2024/03/15"
    },
    {
      "record_date": "20240205",
      "sht_cd": "296170",
      "isin_name": "에스엘바이젠",
      "stk_kind": "보통",
      "opp_opi_rcpt_term": "020240219",
      "buy_req_rcpt_term": "",
      "buy_req_price": "000000000000",
      "buy_amt_pay_dt": "",
      "get_meet_dt": ""
    },
    {
      "record_date": "20240205",
      "sht_cd": "29617K",
      "isin_name": "에스엘바이젠1우",
      "stk_kind": "우선",
      "opp_opi_rcpt_term": "020240219",
      "buy_req_rcpt_term": "",
      "buy_req_price": "000000000000",
      "buy_amt_pay_dt": "",
      "get_meet_dt": ""
    },
    {
      "record_date": "20240205",
      "sht_cd": "29617L",
      "isin_name": "에스엘바이젠2우",
      "stk_kind": "2우선",
      "opp_opi_rcpt_term": "020240219",
      "buy_req_rcpt_term": "",
      "buy_req_price": "000000000000",
      "buy_amt_pay_dt": "",
      "get_meet_dt": ""
    },
    {
      "record_date": "20240205",
      "sht_cd": "29617M",
      "isin_name": "에스엘바이젠3우",
      "stk_kind": "3우선",
      "opp_opi_rcpt_term": "020240219",
      "buy_req_rcpt_term": "",
      "buy_req_price": "000000000000",
      "buy_amt_pay_dt": "",
      "get_meet_dt": ""
    },
    {
      "record_date": "20240205",
      "sht_cd": "29617N",
      "isin_name": "에스엘바이젠4우",
      "stk_kind": "4우선",
      "opp_opi_rcpt_term": "020240219",
      "buy_req_rcpt_term": "",
      "buy_req_price": "000000000000",
      "buy_amt_pay_dt": "",
      "get_meet_dt": ""
    },
    {
      "record_date": "20240205",
      "sht_cd": "29617P",
      "isin_name": "에스엘바이젠5우",
      "stk_kind": "5우선",
      "opp_opi_rcpt_term": "020240219",
      "buy_req_rcpt_term": "",
      "buy_req_price": "000000000000",
      "buy_amt_pay_dt": "",
      "get_meet_dt": ""
    },
    {
      "record_date": "20240205",
      "sht_cd": "419270",
      "isin_name": "신영해피투모로우제7호기업인수목적",
      "stk_kind": "보통",
      "opp_opi_rcpt_term": "020240229",
      "buy_req_rcpt_term": "020240322",
      "buy_req_price": "000000002092",
      "buy_amt_pay_dt": "2024/04/05",
      "get_meet_dt": "2024/03/05"
    },
    {
      "record_date": "20240205",
      "sht_cd": "436530",
      "isin_name": "케이비제22호기업인수목적",
      "stk_kind": "보통",
      "opp_opi_rcpt_term": "020240313",
      "buy_req_rcpt_term": "020240403",
      "buy_req_price": "000000002093",
      "buy_amt_pay_dt": "2024/04/12",
      "get_meet_dt": "2024/03/15"
    },
    {
      "record_date": "20240205",
      "sht_cd": "451250",
      "isin_name": "삐아",
      "stk_kind": "보통",
      "opp_opi_rcpt_term": "020240229",
      "buy_req_rcpt_term": "020240322",
      "buy_req_price": "000000007334",
      "buy_amt_pay_dt": "2024/04/05",
      "get_meet_dt": "2024/03/05"
    },
    {
      "record_date": "20240129",
      "sht_cd": "299910",
      "isin_name": "베스파",
      "stk_kind": "보통",
      "opp_opi_rcpt_term": "020240213",
      "buy_req_rcpt_term": "",
      "buy_req_price": "000000000000",
      "buy_amt_pay_dt": "",
      "get_meet_dt": ""
    },
    {
      "record_date": "20240126",
      "sht_cd": "217270",
      "isin_name": "넵튠",
      "stk_kind": "보통",
      "opp_opi_rcpt_term": "020240208",
      "buy_req_rcpt_term": "",
      "buy_req_price": "000000000000",
      "buy_amt_pay_dt": "",
      "get_meet_dt": ""
    },
    {
      "record_date": "20240119",
      "sht_cd": "151860",
      "isin_name": "케이지이티에스",
      "stk_kind": "보통",
      "opp_opi_rcpt_term": "020240208",
      "buy_req_rcpt_term": "020240304",
      "buy_req_price": "000000011116",
      "buy_amt_pay_dt": "2024/04/04",
      "get_meet_dt": "2024/02/14"
    },
    {
      "record_date": "20240118",
      "sht_cd": "391060",
      "isin_name": "엔에이치기업인수목적20호",
      "stk_kind": "보통",
      "opp_opi_rcpt_term": "020240221",
      "buy_req_rcpt_term": "099991229",
      "buy_req_price": "000000010580",
      "buy_amt_pay_dt": "9999/12/31",
      "get_meet_dt": "2024/02/23"
    },
    {
      "record_date": "20240118",
      "sht_cd": "439270",
      "isin_name": "크리에이츠",
      "stk_kind": "보통",
      "opp_opi_rcpt_term": "020240221",
      "buy_req_rcpt_term": "099991229",
      "buy_req_price": "000000024996",
      "buy_amt_pay_dt": "9999/12/31",
      "get_meet_dt": "2024/02/23"
    },
    {
      "record_date": "20240112",
      "sht_cd": "445090",
      "isin_name": "에이직랜드",
      "stk_kind": "보통",
      "opp_opi_rcpt_term": "020240125",
      "buy_req_rcpt_term": "",
      "buy_req_price": "000000000000",
      "buy_amt_pay_dt": "",
      "get_meet_dt": ""
    },
    {
      "record_date": "20240112",
      "sht_cd": "44509K",
      "isin_name": "에이직랜드1우",
      "stk_kind": "우선",
      "opp_opi_rcpt_term": "020240125",
      "buy_req_rcpt_term": "",
      "buy_req_price": "000000000000",
      "buy_amt_pay_dt": "",
      "get_meet_dt": ""
    },
    {
      "record_date": "20240112",
      "sht_cd": "44509L",
      "isin_name": "에이직랜드2우",
      "stk_kind": "2우선",
      "opp_opi_rcpt_term": "020240125",
      "buy_req_rcpt_term": "",
      "buy_req_price": "000000000000",
      "buy_amt_pay_dt": "",
      "get_meet_dt": ""
    },
    {
      "record_date": "20240111",
      "sht_cd": "177350",
      "isin_name": "베셀",
      "stk_kind": "보통",
      "opp_opi_rcpt_term": "020240124",
      "buy_req_rcpt_term": "",
      "buy_req_price": "000000000000",
      "buy_amt_pay_dt": "",
      "get_meet_dt": ""
    },
    {
      "record_date": "20240111",
      "sht_cd": "17735K",
      "isin_name": "베셀1우",
      "stk_kind": "우선",
      "opp_opi_rcpt_term": "020240124",
      "buy_req_rcpt_term": "",
      "buy_req_price": "000000000000",
      "buy_amt_pay_dt": "",
      "get_meet_dt": ""
    },
    {
      "record_date": "20240111",
      "sht_cd": "222080",
      "isin_name": "씨아이에스",
      "stk_kind": "보통",
      "opp_opi_rcpt_term": "020240124",
      "buy_req_rcpt_term": "",
      "buy_req_price": "000000000000",
      "buy_amt_pay_dt": "",
      "get_meet_dt": ""
    },
    {
      "record_date": "20240111",
      "sht_cd": "445090",
      "isin_name": "에이직랜드",
      "stk_kind": "보통",
      "opp_opi_rcpt_term": "020240124",
      "buy_req_rcpt_term": "",
      "buy_req_price": "000000000000",
      "buy_amt_pay_dt": "",
      "get_meet_dt": ""
    },
    {
      "record_date": "20240111",
      "sht_cd": "44509K",
      "isin_name": "에이직랜드1우",
      "stk_kind": "우선",
      "opp_opi_rcpt_term": "020240124",
      "buy_req_rcpt_term": "",
      "buy_req_price": "000000000000",
      "buy_amt_pay_dt": "",
      "get_meet_dt": ""
    },
    {
      "record_date": "20240111",
      "sht_cd": "44509L",
      "isin_name": "에이직랜드2우",
      "stk_kind": "2우선",
      "opp_opi_rcpt_term": "020240124",
      "buy_req_rcpt_term": "",
      "buy_req_price": "000000000000",
      "buy_amt_pay_dt": "",
      "get_meet_dt": ""
    },
    {
      "record_date": "20240105",
      "sht_cd": "009730",
      "isin_name": "코센",
      "stk_kind": "보통",
      "opp_opi_rcpt_term": "020240118",
      "buy_req_rcpt_term": "020240213",
      "buy_req_price": "000000003054",
      "buy_amt_pay_dt": "2024/03/13",
      "get_meet_dt": "2024/01/22"
    },
    {
      "record_date": "20240103",
      "sht_cd": "012160",
      "isin_name": "영흥",
      "stk_kind": "보통",
      "opp_opi_rcpt_term": "020240123",
      "buy_req_rcpt_term": "020240213",
      "buy_req_price": "000000000566",
      "buy_amt_pay_dt": "2024/03/13",
      "get_meet_dt": "2024/01/25"
    },
    {
      "record_date": "20240102",
      "sht_cd": "023530",
      "isin_name": "롯데쇼핑",
      "stk_kind": "보통",
      "opp_opi_rcpt_term": "020240115",
      "buy_req_rcpt_term": "",
      "buy_req_price": "000000000000",
      "buy_amt_pay_dt": "",
      "get_meet_dt": ""
    },
    {
      "record_date": "20231231",
      "sht_cd": "017680",
      "isin_name": "데코앤에프",
      "stk_kind": "보통",
      "opp_opi_rcpt_term": "020240327",
      "buy_req_rcpt_term": "020240417",
      "buy_req_price": "000000063827",
      "buy_amt_pay_dt": "2024/06/17",
      "get_meet_dt": "2024/03/29"
    },
    {
      "record_date": "20231231",
      "sht_cd": "017685",
      "isin_name": "데코앤에프1우",
      "stk_kind": "우선",
      "opp_opi_rcpt_term": "020240327",
      "buy_req_rcpt_term": "020240417",
      "buy_req_price": "000000000000",
      "buy_amt_pay_dt": "2024/06/17",
      "get_meet_dt": "2024/03/29"
    },
    {
      "record_date": "20231231",
      "sht_cd": "033540",
      "isin_name": "파라텍",
      "stk_kind": "보통",
      "opp_opi_rcpt_term": "020240325",
      "buy_req_rcpt_term": "020240415",
      "buy_req_price": "000000002607",
      "buy_amt_pay_dt": "2024/05/14",
      "get_meet_dt": "2024/03/27"
    },
    {
      "record_date": "20231231",
      "sht_cd": "037710",
      "isin_name": "광주신세계",
      "stk_kind": "보통",
      "opp_opi_rcpt_term": "020240326",
      "buy_req_rcpt_term": "020240416",
      "buy_req_price": "000000030905",
      "buy_amt_pay_dt": "2024/05/10",
      "get_meet_dt": "2024/03/28"
    },
    {
      "record_date": "20231231",
      "sht_cd": "065650",
      "isin_name": "메디프론디비티",
      "stk_kind": "보통",
      "opp_opi_rcpt_term": "020240326",
      "buy_req_rcpt_term": "020240416",
      "buy_req_price": "000000001336",
      "buy_amt_pay_dt": "2024/05/16",
      "get_meet_dt": "2024/03/28"
    },
    {
      "record_date": "20231231",
      "sht_cd": "06565K",
      "isin_name": "메디프론디비티 1우",
      "stk_kind": "우선",
      "opp_opi_rcpt_term": "020240326",
      "buy_req_rcpt_term": "020240416",
      "buy_req_price": "000000001336",
      "buy_amt_pay_dt": "2024/05/16",
      "get_meet_dt": "2024/03/28"
    },
    {
      "record_date": "20231231",
      "sht_cd": "215000",
      "isin_name": "골프존",
      "stk_kind": "보통",
      "opp_opi_rcpt_term": "020240327",
      "buy_req_rcpt_term": "020240417",
      "buy_req_price": "000000087629",
      "buy_amt_pay_dt": "2024/04/26",
      "get_meet_dt": "2024/03/29"
    },
    {
      "record_date": "20231231",
      "sht_cd": "234690",
      "isin_name": "녹십자웰빙",
      "stk_kind": "보통",
      "opp_opi_rcpt_term": "020240325",
      "buy_req_rcpt_term": "020240415",
      "buy_req_price": "000000009043",
      "buy_amt_pay_dt": "2024/05/10",
      "get_meet_dt": "2024/03/27"
    },
    {
      "record_date": "20231231",
      "sht_cd": "278270",
      "isin_name": "네오임플란트",
      "stk_kind": "보통",
      "opp_opi_rcpt_term": "020240322",
      "buy_req_rcpt_term": "020240412",
      "buy_req_price": "000000000000",
      "buy_amt_pay_dt": "2024/04/30",
      "get_meet_dt": "2024/03/26"
    },
    {
      "record_date": "20231231",
      "sht_cd": "371110",
      "isin_name": "포인트임플란트",
      "stk_kind": "보통",
      "opp_opi_rcpt_term": "020240327",
      "buy_req_rcpt_term": "020240417",
      "buy_req_price": "000000002400",
      "buy_amt_pay_dt": "2024/06/17",
      "get_meet_dt": "2024/03/29"
    },
    {
      "record_date": "20231229",
      "sht_cd": "356950",
      "isin_name": "클래스101",
      "stk_kind": "보통",
      "opp_opi_rcpt_term": "020240116",
      "buy_req_rcpt_term": "",
      "buy_req_price": "000000000000",
      "buy_amt_pay_dt": "",
      "get_meet_dt": ""
    },
    {
      "record_date": "20231229",
      "sht_cd": "35695K",
      "isin_name": "클래스101 1우",
      "stk_kind": "우선",
      "opp_opi_rcpt_term": "020240116",
      "buy_req_rcpt_term": "",
      "buy_req_price": "000000000000",
      "buy_amt_pay_dt": "",
      "get_meet_dt": ""
    },
    {
      "record_date": "20231229",
      "sht_cd": "35695L",
      "isin_name": "클래스101 2우",
      "stk_kind": "2우선",
      "opp_opi_rcpt_term": "020240116",
      "buy_req_rcpt_term": "",
      "buy_req_price": "000000000000",
      "buy_amt_pay_dt": "",
      "get_meet_dt": ""
    },
    {
      "record_date": "20231229",
      "sht_cd": "35695M",
      "isin_name": "클래스101 3우",
      "stk_kind": "3우선",
      "opp_opi_rcpt_term": "020240116",
      "buy_req_rcpt_term": "",
      "buy_req_price": "000000000000",
      "buy_amt_pay_dt": "",
      "get_meet_dt": ""
    },
    {
      "record_date": "20231229",
      "sht_cd": "35695N",
      "isin_name": "클래스101 4우",
      "stk_kind": "4우선",
      "opp_opi_rcpt_term": "020240116",
      "buy_req_rcpt_term": "",
      "buy_req_price": "000000000000",
      "buy_amt_pay_dt": "",
      "get_meet_dt": ""
    },
    {
      "record_date": "20231229",
      "sht_cd": "35695P",
      "isin_name": "클래스101 5우",
      "stk_kind": "5우선",
      "opp_opi_rcpt_term": "020240116",
      "buy_req_rcpt_term": "",
      "buy_req_price": "000000000000",
      "buy_amt_pay_dt": "",
      "get_meet_dt": ""
    },
    {
      "record_date": "20231229",
      "sht_cd": "35695Q",
      "isin_name": "클래스101 6우",
      "stk_kind": "6우선",
      "opp_opi_rcpt_term": "020240116",
      "buy_req_rcpt_term": "",
      "buy_req_price": "000000000000",
      "buy_amt_pay_dt": "",
      "get_meet_dt": ""
    },
    {
      "record_date": "20231229",
      "sht_cd": "35695R",
      "isin_name": "클래스101 7우",
      "stk_kind": "7우선",
      "opp_opi_rcpt_term": "020240116",
      "buy_req_rcpt_term": "",
      "buy_req_price": "000000000000",
      "buy_amt_pay_dt": "",
      "get_meet_dt": ""
    },
    {
      "record_date": "20231229",
      "sht_cd": "35695S",
      "isin_name": "클래스101 8우",
      "stk_kind": "8우선",
      "opp_opi_rcpt_term": "020240116",
      "buy_req_rcpt_term": "",
      "buy_req_price": "000000000000",
      "buy_amt_pay_dt": "",
      "get_meet_dt": ""
    },
    {
      "record_date": "20231226",
      "sht_cd": "016880",
      "isin_name": "웅진",
      "stk_kind": "보통",
      "opp_opi_rcpt_term": "020240108",
      "buy_req_rcpt_term": "",
      "buy_req_price": "000000000000",
      "buy_amt_pay_dt": "",
      "get_meet_dt": ""
    },
    {
      "record_date": "20231222",
      "sht_cd": "397880",
      "isin_name": "교보11호기업인수목적",
      "stk_kind": "보통",
      "opp_opi_rcpt_term": "020240130",
      "buy_req_rcpt_term": "020240220",
      "buy_req_price": "000000002126",
      "buy_amt_pay_dt": "2024/02/29",
      "get_meet_dt": "2024/02/01"
    },
    {
      "record_date": "20231222",
      "sht_cd": "420570",
      "isin_name": "제이투케이바이오",
      "stk_kind": "보통",
      "opp_opi_rcpt_term": "020240130",
      "buy_req_rcpt_term": "020240220",
      "buy_req_price": "000000017267",
      "buy_amt_pay_dt": "2024/02/29",
      "get_meet_dt": "2024/02/01"
    },
    {
      "record_date": "20231214",
      "sht_cd": "227100",
      "isin_name": "에이치앤비디자인",
      "stk_kind": "보통",
      "opp_opi_rcpt_term": "020231227",
      "buy_req_rcpt_term": "",
      "buy_req_price": "000000000000",
      "buy_amt_pay_dt": "",
      "get_meet_dt": ""
    },
    {
      "record_date": "20231214",
      "sht_cd": "22710K",
      "isin_name": "에이치앤비디자인1우",
      "stk_kind": "우선",
      "opp_opi_rcpt_term": "020231227",
      "buy_req_rcpt_term": "",
      "buy_req_price": "000000000000",
      "buy_amt_pay_dt": "",
      "get_meet_dt": ""
    },
    {
      "record_date": "20231212",
      "sht_cd": "369370",
      "isin_name": "블리츠웨이",
      "stk_kind": "보통",
      "opp_opi_rcpt_term": "020240108",
      "buy_req_rcpt_term": "020240129",
      "buy_req_price": "000000002022",
      "buy_amt_pay_dt": "2024/02/08",
      "get_meet_dt": "2024/01/10"
    },
    {
      "record_date": "20231211",
      "sht_cd": "041520",
      "isin_name": "이라이콤",
      "stk_kind": "보통",
      "opp_opi_rcpt_term": "020231221",
      "buy_req_rcpt_term": "",
      "buy_req_price": "000000000000",
      "buy_amt_pay_dt": "",
      "get_meet_dt": ""
    },
    {
      "record_date": "20231211",
      "sht_cd": "123840",
      "isin_name": "한일진공",
      "stk_kind": "보통",
      "opp_opi_rcpt_term": "020240124",
      "buy_req_rcpt_term": "020240214",
      "buy_req_price": "000000000465",
      "buy_amt_pay_dt": "2024/03/15",
      "get_meet_dt": "2024/01/26"
    },
    {
      "record_date": "20231211",
      "sht_cd": "452240",
      "isin_name": "뉴온",
      "stk_kind": "보통",
      "opp_opi_rcpt_term": "020240124",
      "buy_req_rcpt_term": "020240214",
      "buy_req_price": "000000011964",
      "buy_amt_pay_dt": "2024/02/27",
      "get_meet_dt": "2024/01/26"
    },
    {
      "record_date": "20231211",
      "sht_cd": "45224K",
      "isin_name": "뉴온 1우",
      "stk_kind": "우선",
      "opp_opi_rcpt_term": "020240124",
      "buy_req_rcpt_term": "020240214",
      "buy_req_price": "000000000000",
      "buy_amt_pay_dt": "2024/02/27",
      "get_meet_dt": "2024/01/26"
    },
    {
      "record_date": "20231206",
      "sht_cd": "054210",
      "isin_name": "이랜텍",
      "stk_kind": "보통",
      "opp_opi_rcpt_term": "020231219",
      "buy_req_rcpt_term": "",
      "buy_req_price": "000000000000",
      "buy_amt_pay_dt": "",
      "get_meet_dt": ""
    },
    {
      "record_date": "20231206",
      "sht_cd": "05421K",
      "isin_name": "이랜텍1우",
      "stk_kind": "우선",
      "opp_opi_rcpt_term": "020231219",
      "buy_req_rcpt_term": "",
      "buy_req_price": "000000000000",
      "buy_amt_pay_dt": "",
      "get_meet_dt": ""
    },
    {
      "record_date": "20231129",
      "sht_cd": "034300",
      "isin_name": "신세계건설",
      "stk_kind": "보통",
      "opp_opi_rcpt_term": "020231220",
      "buy_req_rcpt_term": "020240110",
      "buy_req_price": "000000013424",
      "buy_amt_pay_dt": "2024/01/22",
      "get_meet_dt": "2023/12/22"
    },
    {
      "record_date": "20231129",
      "sht_cd": "375730",
      "isin_name": "퀄슨",
      "stk_kind": "보통",
      "opp_opi_rcpt_term": "020231220",
      "buy_req_rcpt_term": "020240110",
      "buy_req_price": "000000023704",
      "buy_amt_pay_dt": "2024/01/18",
      "get_meet_dt": "2023/12/22"
    },
    {
      "record_date": "20231129",
      "sht_cd": "37573K",
      "isin_name": "퀄슨1우",
      "stk_kind": "우선",
      "opp_opi_rcpt_term": "020231220",
      "buy_req_rcpt_term": "020240110",
      "buy_req_price": "000000023704",
      "buy_amt_pay_dt": "2024/01/18",
      "get_meet_dt": "2023/12/22"
    },
    {
      "record_date": "20231129",
      "sht_cd": "37573L",
      "isin_name": "퀄슨2우",
      "stk_kind": "2우선",
      "opp_opi_rcpt_term": "020231220",
      "buy_req_rcpt_term": "020240110",
      "buy_req_price": "000000023704",
      "buy_amt_pay_dt": "2024/01/18",
      "get_meet_dt": "2023/12/22"
    },
    {
      "record_date": "20231129",
      "sht_cd": "37573M",
      "isin_name": "퀄슨3우",
      "stk_kind": "3우선",
      "opp_opi_rcpt_term": "020231220",
      "buy_req_rcpt_term": "020240110",
      "buy_req_price": "000000023704",
      "buy_amt_pay_dt": "2024/01/18",
      "get_meet_dt": "2023/12/22"
    },
    {
      "record_date": "20231129",
      "sht_cd": "37573N",
      "isin_name": "퀄슨4우",
      "stk_kind": "4우선",
      "opp_opi_rcpt_term": "020231220",
      "buy_req_rcpt_term": "020240110",
      "buy_req_price": "000000023704",
      "buy_amt_pay_dt": "2024/01/18",
      "get_meet_dt": "2023/12/22"
    },
    {
      "record_date": "20231127",
      "sht_cd": "372290",
      "isin_name": "하나머스트7호기업인수목적",
      "stk_kind": "보통",
      "opp_opi_rcpt_term": "020231220",
      "buy_req_rcpt_term": "020240110",
      "buy_req_price": "000000002084",
      "buy_amt_pay_dt": "2024/01/19",
      "get_meet_dt": "2023/12/22"
    },
    {
      "record_date": "20231127",
      "sht_cd": "452430",
      "isin_name": "사피엔반도체",
      "stk_kind": "보통",
      "opp_opi_rcpt_term": "020231220",
      "buy_req_rcpt_term": "020240110",
      "buy_req_price": "000000015330",
      "buy_amt_pay_dt": "2024/01/19",
      "get_meet_dt": "2023/12/22"
    },
    {
      "record_date": "20231123",
      "sht_cd": "183410",
      "isin_name": "골프존데카",
      "stk_kind": "보통",
      "opp_opi_rcpt_term": "020231226",
      "buy_req_rcpt_term": "020240116",
      "buy_req_price": "000000001118",
      "buy_amt_pay_dt": "2024/01/24",
      "get_meet_dt": "2023/12/28"
    },
    {
      "record_date": "20231123",
      "sht_cd": "18341K",
      "isin_name": "골프존데카1우",
      "stk_kind": "우선",
      "opp_opi_rcpt_term": "020231226",
      "buy_req_rcpt_term": "020240116",
      "buy_req_price": "000000000000",
      "buy_amt_pay_dt": "2024/01/24",
      "get_meet_dt": "2023/12/28"
    },
    {
      "record_date": "20231123",
      "sht_cd": "18341L",
      "isin_name": "골프존데카2우",
      "stk_kind": "2우선",
      "opp_opi_rcpt_term": "020231226",
      "buy_req_rcpt_term": "020240116",
      "buy_req_price": "000000000000",
      "buy_amt_pay_dt": "2024/01/24",
      "get_meet_dt": "2023/12/28"
    },
    {
      "record_date": "20231123",
      "sht_cd": "215000",
      "isin_name": "골프존",
      "stk_kind": "보통",
      "opp_opi_rcpt_term": "020231206",
      "buy_req_rcpt_term": "",
      "buy_req_price": "000000000000",
      "buy_amt_pay_dt": "",
      "get_meet_dt": ""
    },
    {
      "record_date": "20231122",
      "sht_cd": "426550",
      "isin_name": "아이비케이에스제19호기업인수목적",
      "stk_kind": "보통",
      "opp_opi_rcpt_term": "020231220",
      "buy_req_rcpt_term": "020240110",
      "buy_req_price": "000000002055",
      "buy_amt_pay_dt": "2024/01/18",
      "get_meet_dt": "2023/12/22"
    },
    {
      "record_date": "20231122",
      "sht_cd": "443670",
      "isin_name": "에스피소프트",
      "stk_kind": "보통",
      "opp_opi_rcpt_term": "020231220",
      "buy_req_rcpt_term": "020240110",
      "buy_req_price": "000000003203",
      "buy_amt_pay_dt": "2024/01/18",
      "get_meet_dt": "2023/12/22"
    }
  ],
  "rt_cd": "0",
  "msg_cd": "MCA00000",
  "msg1": "정상처리 되었습니다."
}
```

